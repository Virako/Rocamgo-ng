#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Rocamgo is recogniter of the go games by processing digital images with opencv.
# Copyright (C) 2012 VÃ­ctor Ramirez de la Corte <virako.9 at gmail dot com>
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

import numpy as np
from cv2 import CV_8UC1
from cv2 import COLOR_BGR2GRAY
from cv2 import cvtColor
from cv2 import CV_32FC3
from cv2 import HOUGH_GRADIENT
from cv2 import HoughCircles
from rocamgo.cte import GOBAN_SIZE
from rocamgo.cte import BLACK
from rocamgo.cte import WHITE



def search_stones(img, corners, dp=2):
    """Devuelve las circunferencias encontradas en una imagen.

    :Param img: imagen donde buscaremos las circunferencias
    :Type img: IplImage
    :Param corners: lista de esquinas
    :Type corners: list
    :Param dp: profundidad de bÃºsqueda de cÃ­rculos
    :Type dp: int
    :Keyword dp: 2 era el valor que mejor funcionaba. Prueba y error """
    gray = cvtColor(img, COLOR_BGR2GRAY)
    # r es el la mitad del tamaño de un cuadrado, el radio deseado
    r = img.shape[0]/(GOBAN_SIZE*2)
    circles = HoughCircles(gray, HOUGH_GRADIENT, dp, int(r*0.5), 50, 55,
            int(r*0.7), int(r*1.2))
    return circles

def check_color_stone(pt, radious, img, threshold=190):
    """Devuelve el color de la piedra dado el centro y el radio de la piedra y
    una imagen. También desechamos las piedras que no sean negras o blancas.

    :Param pt: centro de la piedra
    :Type pt: tuple
    :Param radious: radio de la piedra
    :Type radious: int
    :Param img: imagen donde comprobaremos el color de ciertos pixeles
    :Type img: IplImage
    :Param threshold: umbral de blanco
    :Type threshold: int
    :Keyword threshold: 190 cuando hay buena luminosidad """

    black_total = 0
    white_total = 0
    no_color = 0
    for x in range(int(pt[0] - radious/2), int(pt[0] + radious/2)):
        try:
            pixel = img.at(pt[1], x)[:-1]
        except:
            continue
        if all(p > threshold for p in pixel):
            white_total += 1
        elif all(p < 50 for p in pixel):
            black_total += 1
        else:
            no_color += 1
    for y in range(int(pt[1] - radious/2), int(pt[1] + radious/2)):
        try:
            pixel = img.at(y, pt[0])
        except:
            continue
        if all(p > threshold for p in pixel):
            white_total += 1
        elif all(p < 50 for p in pixel):
            black_total += 1
        else:
            no_color += 1

    if white_total >= black_total and white_total >= no_color:
        return WHITE
    elif no_color >= black_total and no_color >= white_total:
        return -1
    elif black_total >= white_total and black_total >= no_color:
        return BLACK

def check_color_stone_LaB(pt, radious, img):
    """Devuelve el color de la piedra dado el centro y el radio de la piedra y
    una imagen. También desechamos las piedras que tengan tendencia al color.

    :Param pt: centro de la piedra
    :Type pt: tuple
    :Param radious: radio de la piedra
    :Type radious: int
    :Param img: imagen donde comprobaremos el color de ciertos pixeles
    :Type img: IplImage"""
    black_total = 0
    white_total = 0
    color = 0
    intensidad=0
    for x in range(pt[0] - radious/2, pt[0] + radious/2):
        try:
            pixel = img.at(pt[1], x)[:-1]
            #print(pt[1], x,"-",pixel)
        except:
            continue
        if 114<pixel[1]<140 and 114<pixel[2]<140:
            if pixel[0]>125:
                white_total+=1
            elif pixel[0]<90:
                black_total+=1
            else:
                intensidad+=1
                color+=1
        else:
            color+=1

    if white_total >= black_total and white_total >= color:
        return WHITE
    elif color >= black_total and color >= white_total:
        return -1
    elif black_total >= white_total and black_total >= color:
        return BLACK

