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


import numpy as np
from cv2 import (
        ADAPTIVE_THRESH_MEAN_C,
        CHAIN_APPROX_NONE,
        COLOR_RGB2GRAY,
        Canny,
        RETR_CCOMP,
        THRESH_BINARY_INV,
        adaptiveThreshold,
        approxPolyDP,
        arcLength,
        contourArea,
        contourArea,
        cvtColor,
        findContours,
        medianBlur,
)
from math import sqrt
from rocamgo.cte import (
        MAX_BOARD_AREA,
        MAX_BOARD_PERIMETER,
        MAX_POLY_APPROX_ERROR,
        MIN_BOARD_AREA,
        MIN_BOARD_PERIMETER,
        NUM_EDGES,
)


def count_perimeter(seq):
    """Contamos el perímetro de una secuencia dada.

    :Param seq: secuencia de puntos
    :Type seq: CvSeq
    :Return: distancia del perímetro
    :Rtype: float
    """
    ant = False
    perimeter = 0
    for (a,b) in seq:
        if ant:
            perimeter += sqrt((ant[0]-a)**2 + (ant[1]-b)**2)
        else:
            perimeter = sqrt((seq[-1][0]-a)**2 + (seq[-1][1]-b)**2)
        ant = (a,b)
    return perimeter

def get_corners(contour):
    """Hallamos las esquinas a partir de un contorno y las ordenamos de la siguiente manera: ul, dl, ur, dr.  u = up, l = left, d = down, r = right.

    :Param contour: contorno del tablero obtenido
    :Type contour: CvSeq
    :Return: lista de esquinas
    :Rtype: list """
    corners = np.zeros((4,2))
    # [ [[x,y]], [[x,y]], ... ] to [ [x,y], [x,y], ... ]
    for n in range(len(contour)):
        corners[n] = contour[n][0]
    corners.view('f8,f8').sort(order=['f0'], axis=0)
    corners[:2].view('f8,f8').sort(order=['f1'], axis=0)
    corners[2:].view('f8,f8').sort(order=['f1'], axis=0)
    return corners



def filter_image(img):
    """Aplicamos unos filtros a las imágenes para facilitar su tratamiento. Buscamos contornos y suavizamos.

    :Param img: imagen sin filtrar
    :Type img: CvMat
    :Return: imagen filtrada
    :Rtype: CvMat """
    aux_1 = np.zeros((img.rows, img.cols), np.uint8)
    aux_2 = np.zeros((img.rows, img.cols), np.uint8)
    Canny(img, aux_2, 50, 200, 3)
    #Smooth(aux_2, aux_1, CV_GAUSSIAN, 1, 3) # The function is now obsolete. Use GaussianBlur(), blur(), medianBlur() or bilateralFilter().
    medianBlur(aux_2, aux_1, 1, 3)
    return aux_1


def detect_contour(img):
    """Buscamos contornos con unas características determinadas para encontrar un tablero de go en una imagen.

    :Param img: imagen filtrada para buscar contornos en ella
    :Type img: CvMat
    :Return: Contorno si no lo encuentra, sino None
    :Rtype: CvSeq """
    retimg, contours, hier = findContours(img, RETR_CCOMP, CHAIN_APPROX_NONE, offset=(0, 0))
    contornos=[]
    imrow = img.shape[0]
    imcol = img.shape[1]
    for contour in contours:
        if len(contour) >= NUM_EDGES and \
                ((imcol*2 + imrow*2) * MAX_BOARD_PERIMETER) > arcLength(contour, True) > ((imcol*2 + imrow*2) * MIN_BOARD_PERIMETER)  and \
                (imcol * imrow) * MAX_BOARD_AREA > contourArea(contour) > ((imcol * imrow) * MIN_BOARD_AREA):
            perimeter = arcLength(contour, True)
            seq_app = approxPolyDP(contour, perimeter*MAX_POLY_APPROX_ERROR, 1)
            if len(seq_app) == NUM_EDGES:
                contornos.append(seq_app)
    if len(contornos):
        return contornos[0]
    return None


def search_goban(img):
    """Busca el tablero en una imagen.

    :Param img: imagen del tablero
    :Type img: IplImage # TODO comprobar tipo imagen
    :Return: lista de esquinas si las encuentra, sino None
    :Rtype: list or None """
    aux_gray = np.zeros(img.shape[:2])
    aux_gray = cvtColor(img, COLOR_RGB2GRAY)
    #img_gray = GetMat(aux_gray, 0)
    img_gray = aux_gray.copy()
    img_gray = adaptiveThreshold(img_gray, 255, ADAPTIVE_THRESH_MEAN_C,
            THRESH_BINARY_INV, 7, 2)
    #img_filtered = filter_image(img_gray)
    contour = detect_contour(img_gray)
    if contour != None and contour.any():
        return get_corners(contour)
    else:
        return None

