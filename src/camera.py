#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Rocamgo is recogniter of the go games by processing digital images with opencv.
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


from cv import QueryFrame
from cv import CaptureFromCAM

class Camera:
    """ Class for initialite camera. """
    def __init__(self):
        self.capture = None
        self.index = None
    
    def open_camera(self, index):
        """ Open camera with opencv. """
        self.capture = CaptureFromCAM(index)
        self.index = index

    def get_frame(self):
        """ Get image from camera. """
        return QueryFrame( self.capture )

    def is_open(self):
        return self.capture
        
    def close_camera(self):
        """ Close open camera. """
        self.capture = None
