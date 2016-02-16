from cv2 import imread
from cv2 import VideoCapture
from cv2 import CAP_PROP_FRAME_HEIGHT
from cv2 import CAP_PROP_FRAME_WIDTH

from rocamgo.detection.cameras import Cameras


class CaptureSource:
    def __init__(self):
        self._video = None
        self._image = None

    def get_resolution(self):
        if (self._video):
            return (int(self._video.get(CAP_PROP_FRAME_WIDTH)),
                    int(self._video.get(CAP_PROP_FRAME_HEIGHT)))

    def camera(self, num_cams):
        cam = Cameras()
        cam.check_cameras(num_cams)
        self._video = cam.show_and_select_camera()

    def video(self, filename):
        self._video = VideoCapture(filename)

    def image(self, filename):
        self._image = filename

    def get_frame(self):
        if self._video:
            retval, frame = self._video.read()
            return retval, frame
        return True, imread(self._image)
