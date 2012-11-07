from cv import QueryFrame, LoadImage, CaptureFromFile, GetCaptureProperty
from cv import CV_CAP_PROP_FRAME_HEIGHT, CV_CAP_PROP_FRAME_WIDTH

from cameras import Cameras


class CaptureSource:
    def __init__(self):
        self._video = None
        self._image = None

    def get_resolution(self):
        if (self._video):
            return (int(GetCaptureProperty(self._video, CV_CAP_PROP_FRAME_WIDTH)),
                    int(GetCaptureProperty(self._video, CV_CAP_PROP_FRAME_HEIGHT)))

    def camera(self, num_cams):
        cam = Cameras()
        cams_found = cam.check_cameras(num_cams)
        self._video = cam.show_and_select_camera()

    def video(self, filename):
        self._video = CaptureFromFile(filename)

    def image(self, filename):
        self._image = filename

    def get_frame(self):
        if self._video:
            return QueryFrame(self._video)
        return LoadImage(self._image)
