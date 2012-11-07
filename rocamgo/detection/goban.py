from copy import copy

from rocamgo.detection.search_goban import search_goban
from rocamgo.detection.check_goban_moved import check_goban_moved
from rocamgo.detection.perspective import perspective


class Goban:
    def __init__(self):
        self._prev_corners = None
        self._good_corners = None
        self.current_corners = None

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
