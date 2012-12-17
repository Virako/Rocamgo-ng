from copy import copy

import cv

from rocamgo.detection.search_goban import search_goban
from rocamgo.detection.check_goban_moved import check_goban_moved
from rocamgo.detection.perspective import perspective
from rocamgo.detection.search_stones import check_color_stone, search_stones,check_color_stone_LaB

from rocamgo.cte import BLACK
from rocamgo.cte import WHITE
from rocamgo.cte import GOBAN_SIZE
from rocamgo.game.move import Move
import math


class Goban:
    def __init__(self):
        self._prev_corners = None
        self._good_corners = None
        self.current_corners = None
        self.search_stones = None
        self.select_stone_search_algo('LaB')

    def extract(self, image):
        self._prev_corners = copy(self.current_corners)
        self.current_corners = search_goban(image)
        if not self.current_corners:
            self.current_corners = copy(self._prev_corners)
        if check_goban_moved(self._prev_corners, self.current_corners):
            self._good_corners = copy(self.current_corners)
            # print "MOVED"
        if self._good_corners:
            return perspective(image, self._good_corners), self._good_corners
        return None, []

    def select_stone_search_algo(self, method):
        self.search_stones = eval("self.search_stones_" + method)
         
    def search_stones_LaB(self,image,th):
        stones=[]
        false_stones=0
        circles = search_stones(image, None)
        lab_img = cv.CreateImage(cv.GetSize(image), 8, 3)
        cv.CvtColor(image, lab_img, cv.CV_BGR2Lab)
        for n in range(circles.cols):
            pixel = cv.Get1D(circles, n)
            pt = (cv.Round(pixel[0]), cv.Round(pixel[1]))
            radious = cv.Round(pixel[2])
            color=check_color_stone_LaB(pt, radious, lab_img)
            position = Move.pixel_to_position(image.width, pixel)
            if color == BLACK:
                # print "BLACK"
                cv.Circle(image, pt, radious, cv.CV_RGB(255, 0, 0), 2)
                stones.append(Move(color, position))
            elif color == WHITE:
                # print "WHITE"
                cv.Circle(image, pt, radious, cv.CV_RGB(0, 255, 0), 2)
                stones.append(Move(color, position))
            else:
                #cv.Line(image, (pt[0]-radious,pt[1]), (pt[0]+radious,pt[1]), cv.CV_RGB(255, 255, 0),1)
                #cv.Line(image, (pt[0],pt[1]-radious), (pt[0],pt[1]+radious), cv.CV_RGB(255, 255, 0),1)
                false_stones += 1
        print "desechados",false_stones
        return image, stones

    def search_stones_old(self, image, threshold):
        circles = search_stones(image, None)
        false_stones = 0
        stones = []
        for n in range(circles.cols):
            pixel = cv.Get1D(circles, n)
            pt = (cv.Round(pixel[0]), cv.Round(pixel[1]))
            radious = cv.Round(pixel[2])
            # Comprobar el color en la imagen
            color = check_color_stone(pt, radious, image, threshold)
            position = Move.pixel_to_position(image.width, pixel)
            if color == BLACK:
                # print "BLACK"
                cv.Circle(image, pt, radious, cv.CV_RGB(255, 0, 0), 2)
                stones.append(Move(color, position))
            elif color == WHITE:
                # print "WHITE"
                cv.Circle(image, pt, radious, cv.CV_RGB(0, 255, 0), 2)
                stones.append(Move(color, position))
            else:
                # Circle(ideal_img, pt, radious, CV_RGB(255,255,0),2)
                false_stones += 1
        print "falsas=", false_stones
        return image, stones

    def search_stones_mask(self, image, threshold):
        stones = []
        smooth = cv.CloneImage(image)
        cv.Smooth(image, smooth, cv.CV_GAUSSIAN, 5, 5)
        hsv_img = cv.CreateImage(cv.GetSize(image), 8, 3)
        cv.CvtColor(smooth, hsv_img, cv.CV_RGB2HSV)

        masked_img = cv.CreateImage(cv.GetSize(hsv_img), 8, 1)
        #FIXME: Illumination has a strong effect in white detection, try to fix
        # it by tweaking the threshold or reduce contrast in the image
        trickeryfu = {WHITE: [(0, 0, 191), (180, 255, 255)],
            BLACK: [(0, 0, 0), (180, 255, 64)]}
        for k in trickeryfu.keys():
            color_range = trickeryfu.get(k)
            cv.InRangeS(hsv_img, color_range[0], color_range[1], masked_img)
            circles = self._get_circles(masked_img)
            for n in range(circles.cols):
                # TODO: Try to make this less ugly
                pixel = cv.Get1D(circles, n)
                pt = (cv.Round(pixel[0]), cv.Round(pixel[1]))
                radius = cv.Round(pixel[2])
                position = Move.pixel_to_position(image.width, pt)
                stones.append(Move(k, position))
                cv.Circle(image, pt, radius, cv.CV_RGB(255, 255, 255)
                    if k == BLACK else cv.CV_RGB(0, 0, 0), 2)
        return image, stones

    def search_stones_simple(self, image, threshold):
        stones = []
        smooth = cv.CloneImage(image)
        cv.Smooth(image, smooth, cv.CV_GAUSSIAN, 5, 5)
        hsv_img = cv.CreateImage(cv.GetSize(image), 8, 3)
        cv.CvtColor(smooth, hsv_img, cv.CV_RGB2HSV)

        masked_img = cv.CreateImage(cv.GetSize(hsv_img), 8, 1)
        trickeryfu = {WHITE: [(0, 0, 191), (180, 255, 255)],
            BLACK: [(0, 0, 0), (180, 255, 64)]}
        for k in trickeryfu.keys():
            color_range = trickeryfu.get(k)
            cv.InRangeS(hsv_img, color_range[0], color_range[1], masked_img)
            storage = cv.CreateMemStorage()
            contours = cv.FindContours(masked_img, storage,
                cv.CV_RETR_EXTERNAL, cv.CV_CHAIN_APPROX_SIMPLE,
                offset=(0, 0))
            while contours:
                # The original idea was to find the centroids.
                #   This seems simpler
                perimeter = cv.ArcLength(contours)
                expected_perim = math.pi * image.width / GOBAN_SIZE
                if (perimeter < 1.1 * expected_perim and
                    perimeter > 0.9 * expected_perim):
                    __, center, radius = cv.MinEnclosingCircle(contours)
                    position = Move.pixel_to_position(image.width, center)
                    stones.append(Move(k, position))
                    center = tuple(cv.Round(v) for v in center)
                    radius = cv.Round(radius)
                    cv.Circle(image, center, radius, cv.CV_RGB(255, 255, 255)
                        if k == BLACK else cv.CV_RGB(0, 0, 0), 2)
                contours = contours.h_next()
        return image, stones

    def _get_circles(self, image, dp=1.7):
        # TODO: HoughCircles calls Canny itself, get rid of this by
        #  adjusting parameters
        cv.Canny(image, image, 50, 55)
        r = image.width / (GOBAN_SIZE * 2)
        circles = cv.CreateMat(1, image.height * image.width, cv.CV_32FC3)
        cv.HoughCircles(image, circles, cv.CV_HOUGH_GRADIENT, dp,
            int(r * 0.5), 50, 55, int(r * 0.7), int(r * 1.2))
        return circles
