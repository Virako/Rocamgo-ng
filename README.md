# Rocamgo

Recognition of a [go](http://en.wikipedia.org/wiki/Go_(game)) game by processing digital images with opencv.


## Install

You need a opencv >= 3. For install, you can visit the next
[link](http://docs.opencv.org/master/d7/d9f/tutorial_linux_install.html#gsc.tab=0)

IMPORTANT: Like this project use python3, you should install python3-dev and python3-numpy.
Also, when you are configuring opencv with cmake, you should set the python3 parameters.

When you finish the installation of opencv3, you can get an error when use `import cv2`, then, you
should export opencv lib: export PYTHONPATH="<cmake-build-dir>/lib/python3"


## Run

```
python rocamgo.py --help
```

Examples:

If you have two cameras and want recognition by one of them:

```
python rocamgo.py --camera 2
```

If you want recognition a video:

```
python rocamgo.py --video FILEPATH
```
