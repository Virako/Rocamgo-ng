#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Rocamgo is recogniter of the go games by processing digital images with 
# opencv.
# Copyright (C) 2012 Víctor Ramirez de la Corte <virako.9 at gmail dot com>
# Copyright (C) 2012 David Medina Velasco <cuidadoconeltecho at gmail dot com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
:var cameras: lista de cámaras
:Type cameras: list
:var camera: cámara seleccionada
:Type camera: Capture
"""

from cv import ShowImage
from cv import WaitKey
from cv import SetMouseCallback
from cv import CV_EVENT_LBUTTONDBLCLK
from cv import CaptureFromCAM
from cv import QueryFrame
from cv import DestroyWindow
from cv import NamedWindow
import sys

from rocamgo.cte import MAX_CAMERAS


class Cameras:
    """Clase para abrir las cámaras disponibles en el ordenador. """

    def __init__(self):
        #cam = Camera()
        #cam.index = 100
        #cam.capture = CreateFileCapture("http://192.168.1.2:5143/mjpeg")
        self.cameras = []
        self.camera = None
        if sys.platform == 'linux2':
            self.check_cameras = self.check_cameras_linux
        elif sys.platform == 'win32':
            self.check_cameras = self.check_cameras_windows
        else:
            raise NotImplementedError()

    def on_mouse(self, event, x, y, flags, camera):
        """Capturador de eventos de click de ratón.

        :Param event: Evento capturado.
        :Type event: int
        :Param x: posición x del ratón.
        :Type x: int
        :Param y: posición y del ratón.
        :Type y: int
        :Param camera: objeto Capture
        :Type camera: Capture
        """
        if event == CV_EVENT_LBUTTONDBLCLK:
            self.camera = self.cameras[camera]

    def check_cameras_linux(self, num=MAX_CAMERAS):
        """Comprueba las cámaras disponibles.

        :Param num: máximo número de cámaras a comprobar
        :Keyword num: 99 por defecto, ya que en Linux es lo permitido
        :Param num: int
        :Return: lista de cámaras disponibles
        :Rtype: list of Capture
        """
        n = 0
        while len(self.cameras) < num and n <= MAX_CAMERAS:
            camera = CaptureFromCAM(n)
            if QueryFrame(camera):
                self.cameras.append(camera)
            n += 1
        if num != MAX_CAMERAS and len(self.cameras) != num:
            print "Found %d of %d cameras. " % (len(self.cameras), num)
            exit()
        return len(self.cameras)

    def check_cameras_windows(self, num=MAX_CAMERAS):
        """Comprueba las cámaras disponibles.

        :Param num: máximo número de cámaras a comprobar
        :Keyword num: 99 por defecto, ya que en Linux es lo permitido
        :Param num: int
        :Return: lista de cámaras disponibles
        :Rtype: list of Capture
        """
        n = 0
        ierror = 0
        camList = []
        while len(camList) < num and n <= MAX_CAMERAS:
            camList.append(CaptureFromCAM(n))
            n += 1
        n = 0
        while n < num and n <= MAX_CAMERAS:
            frame = QueryFrame(camList[n])
            if frame and frame.height:
                camList[n] = None
            else:
                ierror += 1  # antes de salir debemos borrar todas las cams
            n += 1
        if ierror:
            self.cameras = None
            print "Found %d of %d cameras. " % (num - ierror, num)
            exit()
            # return None     #cámaras repetidas
        n = 0
        while len(self.cameras) < num and n <= MAX_CAMERAS:
            self.cameras.append(CaptureFromCAM(n))
            n += 1
        if num != MAX_CAMERAS and len(self.cameras) != num:
            print "Found %d of %d cameras. " % (len(self.cameras), num)
            exit()
            # return None
        return len(self.cameras)

    def show_and_select_camera(self):
        """Muestra las cámaras disponibles en ventanas y da la opción de
        seleccionar una de ellas pulsando doble click.

        :Return: cámara seleccionada
        :Rtype: Camera """
        if not self.cameras:
            return self.camera
        elif len(self.cameras) == 1:
            return self.cameras[0]
        elif len(self.cameras) > 1:
            for i in range(len(self.cameras)):
                NamedWindow(str(i))
                SetMouseCallback(str(i), self.on_mouse, i)
            while not self.camera:
                for i in range(len(self.cameras)):
                    img = QueryFrame(self.cameras[i])
                    ShowImage(str(i), img)
                    WaitKey(1)
            for i in range(len(self.cameras)):
                DestroyWindow(str(i))
            for i in range(len(self.cameras)):
                if self.cameras[i] != self.camera:
                    self.cameras[i] = None
        return self.camera
