from copy import copy

from cv import Circle
from cv import Get1D
from cv import Round
from cv import CV_RGB

from rocamgo.detection.search_goban import search_goban
from rocamgo.detection.check_goban_moved import check_goban_moved
from rocamgo.detection.perspective import perspective

from rocamgo.cte import BLACK
from rocamgo.cte import WHITE
from rocamgo.cte import GOBAN_SIZE
from rocamgo.game.move import Move
from rocamgo.detection.search_stones import check_color_stone, search_stones


class Goban:
    def __init__(self):
        self._prev_corners = None
        self._good_corners = None
        self.current_corners = None
        self.search_stones = None
        self.select_stone_search_algo('old')

    def extract(self, image):

        # previous corners
        self._prev_corners = copy(self.current_corners)

        # Detect goban
        self.current_corners = search_goban(image)
        if not self.current_corners:
            self.current_corners = copy(self._prev_corners)

        # Check goban moved
        if check_goban_moved(self._prev_corners, self.current_corners):
            self._good_corners = copy(self.current_corners)
            # print "MOVED"
        if self._good_corners:
            return perspective(image, self._good_corners), self._good_corners
        return None, []

    def select_stone_search_algo(self, method):
        self.search_stones = eval("self.search_stones_" + method)

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
                # print "BLACK"
                Circle(image, pt, radious, CV_RGB(255, 0, 0), 2)
                stones.append(Move(color, position))
            elif color == WHITE:
                # print "WHITE"
                Circle(image, pt, radious, CV_RGB(0, 255, 0), 2)
                stones.append(Move(color, position))
            else:
                # Circle(ideal_img, pt, radious, CV_RGB(255,255,0),2)
                false_stones += 1
        return image, stones

    def search_stones_mask(self, image, threshold):
        # Apply color mask for black. Find circles. Repeat for white. Return union
        pass

    def search_stones_simple(self, image, threshold):
        # Apply color mask as in search_stones_mask. Find contours with approx area of a circle. Find centroids. 
        pass
