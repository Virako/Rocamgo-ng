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

"""
:var player1: nombre del jugador 1
:type player1: str
:var player2: nombre del jugador 2
:type player2: str
:var handicap: numero de piedras de ventaja 
:type handicap: int
:var path: directorio donde guardaremos las partidas 
:type path: str
:var rank_player1: nivel del jugador 1
:type rank_player1: str
:var rank_player2: nivel del jugador 2
:type rank_player2: str
:var num_jug: número de jugada actual
:type num_jug: int
:var dir: dirección del directorio donde guardaremos la partida
:type dir: str
"""

import os.path
from datetime import datetime
from cte import BLACK
from cte import WHITE
from cte import HEADER_SGF
import cte

class Kifu:
    """ Clase para crear un fichero .sgf y guardar la partida. """

    def __init__(self, player1="j1", player2="j2", handicap=0, path="sgf", \
            rank_player1='20k', rank_player2='20k'):
        """ Inicializamos configuración del archivo sgf. 
        :param  player1: nombre del jugador 1
        :type  player1: str
        :keyword  player1: j1 por defecto
        :param  player2: nombre del jugador 2
        :type  player2: str
        :keyword  player2: j2 por defecto
        :param  handicap: handicap dado en la partida
        :type  handicap: int
        :keyword  handicap: ninguno por defecto (0)
        :param  path: ruta relativa donde guardamos el fichero
        :type  path: str
        :keyword  path: carpeta sgf por defecto
        :param  rank_player1: rango del jugador 1
        :type  rank_player1: str
        :keyword  rank_player1: 20k por defecto, nivel de inicio en el go
        :param  rank_player2: rango del jugador 2
        :type  rank_player2: str
        :keyword  rank_player2: 20k por defecto, nivel de inicio en el go """
        self.num_jug = 0
        self.player_black = player1
        self.player_white = player2
        filename = str(datetime.now())  + "_" + player1 + "_vs_" + player2
        self.dir = os.path.join(path, filename + ".sgf") 
        header_file = HEADER_SGF
        header_file += [ "\nPB[%s]" %player1, "\nBR[%s]" %rank_player1, \
                         "\nPW[%s]" %player2, "\nWR[%s]" %rank_player2]
        with open(self.dir, "w") as f:
            f.writelines(header_file)


    def add_stone(self, pos, color):
        """ Añadir piedra al sgf. 
        :param pos: posición de la piedra
        :type pos: tuple
        :param color: color de la piedra 
        :type color: int """
        coord = chr(pos[0]+97) + chr(pos[1]+97) 
        with open(self.dir, "a") as f:
            if color == BLACK:
                f.write("\n;B[%s]" %coord)
            elif color == WHITE:
                f.write("\n;W[%s]" %coord)
            else:
                print _("el color debe ser BLACK or WHITE")
        self.num_jug += 1


    def end_file(self):
        """ Cerrar el fichero y dejarlo listo para poder abrirlo."""
        with open(self.dir, "a") as f:
            f.write(")")

