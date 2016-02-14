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

from game_info import GameInfo
from rocamgo.cte import BLACK
from rocamgo.cte import WHITE
from rocamgo.game.move import Move


class Kifu:
    """ Contiene la lista de movimientos que conforman una partida. """
    def __init__(self):
        self.move_list = []
        self._observers = []
        self.info = GameInfo()
        self.previous_color = WHITE

    def add_stone(self, stone):
        if stone.color == self.previous_color:
            if stone.color == BLACK:
                stone_pass = Move(WHITE, (None, None))
            elif stone.color == WHITE:
                stone_pass = Move(BLACK, (None, None))
            else:
                print("Error: stone's color invalid")
            self.move_list.append(stone_pass)
            self.notify(stone_pass)
        self.move_list.append(stone)
        self.notify(stone)
        self.previous_color = stone.color

    def attach(self, observer):
        self._observers.append(observer)

    def notify(self, stone):
        """ Notificamos el cambio a los servidores añadidos. """
        if stone.color == BLACK:
            try:
                print("B(%d, %d)" % (stone.x, stone.y))
            except TypeError:
                print("B()")
        else:
            try:
                print("W(%d, %d)" % (stone.x, stone.y))
            except TypeError:
                print("W()")
        for o in self._observers:
            o.add_stone(stone.pt)
