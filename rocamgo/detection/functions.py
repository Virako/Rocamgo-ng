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
from rocamgo.cte import NUM_EDGES
from rocamgo.cte import GOBAN_SIZE
from math import hypot

def distance_between_two_points(p1, p2):
    """Halla la distancia entre dos puntos dados. 

    :Param p1: punto 1
    :Type p1: tuple
    :Param p2: punto 2
    :Type p2: tuple
    :Return: distancia entre dos puntos
    :Rtype: float
    """
    return hypot( p1[0]-p2[0], p1[1]-p2[1] )


def direction_between_two_points(p1, p2):
    """Halla la direccion entre dos puntos dados. 

    :Param p1: punto 1
    :Type p1: tuple
    :Param p2: punto 2
    :Type p2: tuple
    :Return: dirección del punto 1 al punto 2
    :Rtype: tuple
    """
    return (p2[0]-p1[0], p2[1]-p1[1])


def get_max_edge(corners):
    """Halla la arista más larga dado 4 puntos. 

    :Param corners: lista de 4 puntos
    :Type corners: list
    :Return: máxima distancia entre 4 puntos
    :Rtype: int
    """
    edges = []
    for c in range(NUM_EDGES):
        if c == 0 or c == 2:
            edges.append(distance_between_two_points(corners[c],corners[(c+1)%4]))
        else:
            edges.append(distance_between_two_points(corners[c],corners[(c+2)%4]))
    return int(max(edges))


def get_xy_correction(p1,p2):
    """Retorna la componente media X e Y de una cuadrícula de un tablero. 

    :Param p1: punto 1
    :Type p1: tuple
    :Param p2: punto 2
    :Type p2: tuple
    :Return: componentes X e Y
    :Rtype: float
    """
    return abs(p1[0]-p2[0])/(GOBAN_SIZE-1.0)/2,abs(p1[1]-p2[1])/(GOBAN_SIZE-1.0)/2

def get_external_corners_prespective_correction(corners):
    """Retorna la correción de la lista de 4 puntos. 

    :Param corners: lista de 4 puntos
    :Type corners: list
    :Return: máxima distancia entre 4 puntos
    :Rtype: corners correction
    :RType correction: list
    """
    left = distance_between_two_points(corners[0],corners[1])/distance_between_two_points(corners[2],corners[3])
    top = distance_between_two_points(corners[0],corners[2])/distance_between_two_points(corners[1],corners[3])
    X1,Y1 = get_xy_correction(corners[0],corners[3])
    X2,Y2 = get_xy_correction(corners[1],corners[2])
    correction = np.zeros((4, 2), dtype=np.float32)
    correction[0] = (corners[0][0]-X1*top*left, corners[0][1]-Y1*top*left)
    correction[1] = (corners[1][0]-X2*left/top, corners[1][1]+Y2*left/top)
    correction[2] = (corners[2][0]+X2*top/left, corners[2][1]-Y2*top/left)
    correction[3] = (corners[3][0]+X1/(left*top), corners[3][1]+Y1/(left*top))
    return correction

def get_external_corners(corners):
    """Halla los corners externos en el caso de que haber capturando los internos. 

    :Param corners: lista de 4 puntos
    :Type corners: list
    :Return: lista con los 4 corners exteriores
    :Rtype: list
    """
    external_corners = [] # the orden of corners are ul, dl, dr, ur
    for c in range(len(corners)):
        if c >= 2:
            x = corners[c][0] + (corners[c][0]-corners[(c+2)%4][0])/(GOBAN_SIZE-1.0)/2.0
            #distance_between_two_points(corners[c],\
            #corners[(c+2)%4])/(GOBAN_SIZE-1)/2
        else:
            #x = corners[c][0] - distance_between_two_points(corners[c],\
            #corners[(c+2)%4])/(GOBAN_SIZE-1)/2
            x = corners[c][0] + (corners[c][0]-corners[(c+2)%4][0])/(GOBAN_SIZE-1.0)/2.0
        if c == 1 or c == 3:
            #y = corners[c][1] + distance_between_two_points(corners[c],\
            #corners[(c+3)%4])/(GOBAN_SIZE-1)/2
            y = corners[c][1] + (corners[c][1]-corners[(c+3)%4][1])/(GOBAN_SIZE-1.0)/2.0
        else:
            #y = corners[c][1] - distance_between_two_points(corners[c],\
            #corners[(c+1)%4])/(GOBAN_SIZE-1)/2
            y = corners[c][1] + (corners[c][1]-corners[(c+3)%4][1])/(GOBAN_SIZE-1.0)/2.0
        external_corners.append((x,y))
    return external_corners
