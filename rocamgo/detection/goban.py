import numpy as np
from copy import copy
from cv2 import (
        COLOR_BGR2Lab,
        HOUGH_GRADIENT,
        HoughCircles,
        circle,
        cvtColor,
)
import math

from rocamgo.detection.search_goban import search_goban
from rocamgo.detection.check_goban_moved import check_goban_moved
from rocamgo.detection.perspective import perspective
from rocamgo.detection.search_stones import check_color_stone
from rocamgo.detection.search_stones import search_stones
from rocamgo.detection.search_stones import check_color_stone_LaB
from rocamgo.cte import BLACK
from rocamgo.cte import WHITE
from rocamgo.cte import GOBAN_SIZE
from rocamgo.game.move import Move


class Goban:
    def __init__(self):
        self._prev_corners = None
        self._good_corners = None
        self.current_corners = None
        self.search_stones = None
        self.select_stone_search_algo('old')

    def extract(self, image):
        self._prev_corners = copy(self.current_corners)
        self.current_corners = search_goban(image)
        if not self.current_corners:
            self.current_corners = copy(self._prev_corners)
        if check_goban_moved(self._prev_corners, self.current_corners):
            self._good_corners = copy(self.current_corners)
            # print("MOVED")
        if self._good_corners:
            return perspective(image, self._good_corners), self._good_corners
        return None, []

    def select_stone_search_algo(self, method):
        self.search_stones = eval("self.search_stones_" + method)

    def search_stones_LaB(self,image,th):
        stones = []
        false_stones = 0
        circles = search_stones(image, None)
        lab_img = np.zeros(image.shape[:2], np.uint8)
        lab_img = cvtColor(image, COLOR_BGR2Lab)
        for n in range(circles.cols):
            pixel = Get1D(circles, n)
            pt = (Round(pixel[0]), Round(pixel[1]))
            radious = Round(pixel[2])
            color = check_color_stone_LaB(pt, radious, lab_img)
            position = Move.pixel_to_position(image.width, pixel)
            if color == BLACK:
                # print("BLACK")
                circle(image, pt, radious, (255, 0, 0), 2)
                stones.append(Move(color, position))
            elif color == WHITE:
                # print("WHITE")
                circle(image, pt, radious, (0, 255, 0), 2)
                stones.append(Move(color, position))
            else:
                false_stones += 1
        return image, stones

    def search_stones_old(self, image, threshold):
        circles = search_stones(image, None)
        false_stones = 0
        stones = []
        for n in range(circles.cols):
            pixel = Get1D(circles, n)
            pt = (Round(pixel[0]), Round(pixel[1]))
            radious = Round(pixel[2])
            # Comprobar el color en la imagen
            color = check_color_stone(pt, radious, image, threshold)
            position = Move.pixel_to_position(image.width, pixel)
            if color == BLACK:
                circle(image, pt, radious, CV_RGB(255, 0, 0), 2)
                stones.append(Move(color, position))
            elif color == WHITE:
                circle(image, pt, radious, CV_RGB(0, 255, 0), 2)
                stones.append(Move(color, position))
            else:
                #circle(image, pt, radious, (255,255,0), 2)
                false_stones += 1
        return image, stones

    def search_stones_mask(self, image, threshold):
        stones = []
        smooth = image.clone()
        Smooth(image, smooth, CV_GAUSSIAN, 5, 5)
        hsv_img = np.zeros(image.shape[:2], np.uint8)
        hsv_img = cvtColor(smooth, COLOR_RGB2HSV)

        masked_img = CreateImage(GetSize(hsv_img), 8, 1)
        #FIXME: Illumination has a strong effect in white detection, try to fix
        # it by tweaking the threshold or reduce contrast in the image
        trickeryfu = {WHITE: [(0, 0, 191), (180, 255, 255)],
            BLACK: [(0, 0, 0), (180, 255, 64)]}
        for k in trickeryfu.keys():
            color_range = trickeryfu.get(k)
            inRangeS(hsv_img, color_range[0], color_range[1], masked_img)
            circles = self._get_circles(masked_img)
            for n in range(circles.cols):
                # TODO: Try to make this less ugly
                pixel = Get1D(circles, n)
                pt = (Round(pixel[0]), Round(pixel[1]))
                radius = Round(pixel[2])
                position = Move.pixel_to_position(image.width, pt)
                stones.append(Move(k, position))
                circle(image, pt, radius, CV_RGB(255, 255, 255)
                    if k == BLACK else CV_RGB(0, 0, 0), 2)
        return image, stones

    def search_stones_simple(self, image, threshold):
        stones = []
        smooth = image.clone()
        Smooth(image, smooth, CV_GAUSSIAN, 5, 5)
        hsv_img = np.zeros(image.shape[:2], np.uint8)
        hsv_img = cvtColor(smooth, COLOR_RGB2HSV)

        masked_img = CreateImage(GetSize(hsv_img), 8, 1)
        trickeryfu = {WHITE: [(0, 0, 191), (180, 255, 255)],
            BLACK: [(0, 0, 0), (180, 255, 64)]}
        for k in trickeryfu.keys():
            color_range = trickeryfu.get(k)
            inRangeS(hsv_img, color_range[0], color_range[1], masked_img)
            storage = CreateMemStorage()
            contours = findContours(masked_img, storage,
                RETR_EXTERNAL, CHAIN_APPROX_SIMPLE,
                offset=(0, 0))
            while contours:
                # The original idea was to find the centroids.
                #   This seems simpler
                perimeter = arcLength(contours)
                expected_perim = math.pi * image.width / GOBAN_SIZE
                if (perimeter < 1.1 * expected_perim and
                    perimeter > 0.9 * expected_perim):
                    __, center, radius = minEnclosingCircle(contours)
                    position = Move.pixel_to_position(image.width, center)
                    stones.append(Move(k, position))
                    center = tuple(Round(v) for v in center)
                    radius = Round(radius)
                    circle(image, center, radius, CV_RGB(255, 255, 255)
                        if k == BLACK else CV_RGB(0, 0, 0), 2)
                contours = contours.h_next()
        return image, stones

    def _get_circles(self, image, dp=1.7):
        # TODO: HoughCircles calls Canny itself, get rid of this by
        #  adjusting parameters
        Canny(image, image, 50, 55)
        r = image.width / (GOBAN_SIZE * 2)
        circles = CreateMat(1, image.height * image.width, CV_32FC3)
        HoughCircles(image, circles, HOUGH_GRADIENT, dp,
            int(r * 0.5), 50, 55, int(r * 0.7), int(r * 1.2))
        return circles
