#!/usr/bin/env python
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

"""
:var color: color de la piedra
:Type color: int
:var img: imagen donde se encuentra la piedra
:Type img: IplImage
:var pix: pixel donde se encuentra la piedra dentro de la imagen
:Type pix: tuple
:var pt: coordenada del tablero donde se encuentra la piedra
:Type pt: tuple
:var x: coordenada x del tablero donde se encuentra la piedra 
:Type x: int
:var y: coordenada y del tablero donde se encuentra la piedra 
:Type y: int
"""

from src.cte import GOBAN_SIZE
from src.cte import WHITE
from src.cte import BLACK


class Stone:
    """Clase piedra. """
    def __init__(self, color, pt):
        """Inicializamos una piedra, si no tenemos la posición, buscamos cual es esa posición dado una imagen ideal y un pixel. 

        :Param color: color de la piedra, BLACK or WHITE
        :Type color: int
        :Param pt: punto donde se encuentra la piedra en el tablero
        :Type pt: tuple
        """
        self.pt = pt
        self.color = color
        self.x, self.y = self.pt
        
    @staticmethod    
    def pixel_to_position(width, pixel):
        """ Calcula las coordenadas en el tablero a partir de un pixel en el mismo. """
        square_size = float(width) / GOBAN_SIZE
        border_size = square_size / 2
        x = int(round((pixel[0] - border_size) / square_size))
        y = int(round((pixel[1] - border_size) / square_size))
        return x, y

    def __str__(self):
        color = 'black' if self.color==BLACK else 'white'
        return "(%d, %d) --> %s" %(self.x, self.y, color)

    
    def __eq__(self, st):
        return self.pt == st.pt and self.color == st.color

    def __cmp__(self, st):
        x = self.st.x - st.x
        y = self.st.y - st.y
        if x > 0:
            return x
        elif x == 0:
            if x == y:
                return self.color - st.color
            else:
                return y

    def __hash__(self):
        return hash(self.x)^hash(self.y)^hash(self.color)
