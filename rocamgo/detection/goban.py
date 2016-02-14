from copy import copy
import cv2
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
        lab_img = cv2.CreateImage(cv2.GetSize(image), 8, 3)
        cv2.cvtColor(image, lab_img, cv2.COLOR_BGR2Lab)
        for n in range(circles.cols):
            pixel = cv2.Get1D(circles, n)
            pt = (cv2.Round(pixel[0]), cv2.Round(pixel[1]))
            radious = cv2.Round(pixel[2])
            color = check_color_stone_LaB(pt, radious, lab_img)
            position = Move.pixel_to_position(image.width, pixel)
            if color == BLACK:
                # print("BLACK")
                cv2.circle(image, pt, radious, cv2.CV_RGB(255, 0, 0), 2)
                stones.append(Move(color, position))
            elif color == WHITE:
                # print("WHITE")
                cv2.circle(image, pt, radious, cv2.CV_RGB(0, 255, 0), 2)
                stones.append(Move(color, position))
            else:
                false_stones += 1
        return image, stones

    def search_stones_old(self, image, threshold):
        circles = search_stones(image, None)
        false_stones = 0
        stones = []
        for n in range(circles.cols):
            pixel = cv2.Get1D(circles, n)
            pt = (cv2.Round(pixel[0]), cv2.Round(pixel[1]))
            radious = cv2.Round(pixel[2])
            # Comprobar el color en la imagen
            color = check_color_stone(pt, radious, image, threshold)
            position = Move.pixel_to_position(image.width, pixel)
            if color == BLACK:
                cv2.circle(image, pt, radious, cv2.CV_RGB(255, 0, 0), 2)
                stones.append(Move(color, position))
            elif color == WHITE:
                cv2.circle(image, pt, radious, cv2.CV_RGB(0, 255, 0), 2)
                stones.append(Move(color, position))
            else:
                #cv2.circle(image, pt, radious, cv2.CV_RGB(255,255,0), 2)
                false_stones += 1
        return image, stones

    def search_stones_mask(self, image, threshold):
        stones = []
        smooth = image.clone()
        cv2.Smooth(image, smooth, cv2.CV_GAUSSIAN, 5, 5)
        hsv_img = cv2.CreateImage(cv2.GetSize(image), 8, 3)
        cv2.cvtColor(smooth, hsv_img, cv2.COLOR_RGB2HSV)

        masked_img = cv2.CreateImage(cv2.GetSize(hsv_img), 8, 1)
        #FIXME: Illumination has a strong effect in white detection, try to fix
        # it by tweaking the threshold or reduce contrast in the image
        trickeryfu = {WHITE: [(0, 0, 191), (180, 255, 255)],
            BLACK: [(0, 0, 0), (180, 255, 64)]}
        for k in trickeryfu.keys():
            color_range = trickeryfu.get(k)
            cv2.inRangeS(hsv_img, color_range[0], color_range[1], masked_img)
            circles = self._get_circles(masked_img)
            for n in range(circles.cols):
                # TODO: Try to make this less ugly
                pixel = cv2.Get1D(circles, n)
                pt = (cv2.Round(pixel[0]), cv2.Round(pixel[1]))
                radius = cv2.Round(pixel[2])
                position = Move.pixel_to_position(image.width, pt)
                stones.append(Move(k, position))
                cv2.circle(image, pt, radius, cv2.CV_RGB(255, 255, 255)
                    if k == BLACK else cv2.CV_RGB(0, 0, 0), 2)
        return image, stones

    def search_stones_simple(self, image, threshold):
        stones = []
        smooth = image.clone()
        cv2.Smooth(image, smooth, cv2.CV_GAUSSIAN, 5, 5)
        hsv_img = cv2.CreateImage(cv2.GetSize(image), 8, 3)
        cv2.cvtColor(smooth, hsv_img, cv2.COLOR_RGB2HSV)

        masked_img = cv2.CreateImage(cv2.GetSize(hsv_img), 8, 1)
        trickeryfu = {WHITE: [(0, 0, 191), (180, 255, 255)],
            BLACK: [(0, 0, 0), (180, 255, 64)]}
        for k in trickeryfu.keys():
            color_range = trickeryfu.get(k)
            cv2.inRangeS(hsv_img, color_range[0], color_range[1], masked_img)
            storage = cv2.CreateMemStorage()
            contours = cv2.findContours(masked_img, storage,
                cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE,
                offset=(0, 0))
            while contours:
                # The original idea was to find the centroids.
                #   This seems simpler
                perimeter = cv2.arcLength(contours)
                expected_perim = math.pi * image.width / GOBAN_SIZE
                if (perimeter < 1.1 * expected_perim and
                    perimeter > 0.9 * expected_perim):
                    __, center, radius = cv2.minEnclosingCircle(contours)
                    position = Move.pixel_to_position(image.width, center)
                    stones.append(Move(k, position))
                    center = tuple(cv2.Round(v) for v in center)
                    radius = cv2.Round(radius)
                    cv2.circle(image, center, radius, cv2.CV_RGB(255, 255, 255)
                        if k == BLACK else cv2.CV_RGB(0, 0, 0), 2)
                contours = contours.h_next()
        return image, stones

    def _get_circles(self, image, dp=1.7):
        # TODO: HoughCircles calls Canny itself, get rid of this by
        #  adjusting parameters
        cv2.Canny(image, image, 50, 55)
        r = image.width / (GOBAN_SIZE * 2)
        circles = cv2.CreateMat(1, image.height * image.width, cv2.CV_32FC3)
        cv2.HoughCircles(image, circles, cv2.HOUGH_GRADIENT, dp,
            int(r * 0.5), 50, 55, int(r * 0.7), int(r * 1.2))
        return circles
