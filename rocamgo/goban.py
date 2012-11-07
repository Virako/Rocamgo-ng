#!/usr/bin/env python
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
:var goban: matriz de piedras puestas
:Type goban: list
:var statistical: matriz de estadísticas para comprobar piedras buenas o malas
:Type statistical: list
:var stones: piedras a comprobar para añadir a estadísticas
:Type stones: list
:var kifu: Objeto Kifu
:Type kifu: Kifu
:var igs: Objeto Igs
:Type igs: Igs
"""

from rocamgo.cte import GOBAN_SIZE
from rocamgo.cte import WHITE
from rocamgo.cte import BLACK
from rocamgo.game.kifu import Kifu


class Goban:
    """Clase tablero, contiene la matriz de estadíticas y funciones para
    rellenar el tablero. """

    def __init__(self, size):
        """Crea dos matrices de tamaño pasado por parámetro, una para
        estadísticas y otra para guardar el estado de las piedras. Creamos un
        set de piedras para ir guardando las piedras que estemos comprobando.
        También inicializa un kifu para guardar la partida y un el objetos igs
        que se encargará de conectarse con el servidor que subirá la partida.

        :Param size: tamaño del tablero
        :Type size: int """
        self.size = size
        # El valor 0 es para ir sumando(hay piedra) o restando(no hay)
        # El valor 8 es el nº de veces a buscar antes de hacer la estadística
        self.goban = [[None] * size for i in range(size)]
        self.moves = []
        self.statistical = [[[0, 8]] * size for i in range(size)]
        self.stones = set()
        self.kifu = Kifu()

    def invalid_move(self, move):
        return self.invalid_ko_move(move)

    def get_group(self, pos, color, group=set()):
        """ Funcion recursiva que busca, a partir de una posición, el grupo
        correspondiente a esa posición.
        :Param pos: Posición perteneciente al grupo en la buscaremos si sus
        vecinos pertenecen o no al grupo.
        :Type pos: tuple.
        :Param group: grupo de posiciones que se encuentran dentro del grupo.
        :Type group: set. """

        # Out of range
        if pos[0] in (-1, GOBAN_SIZE) or pos[1] in (-1, GOBAN_SIZE):
            return group
        if self.goban[pos[0]][pos[1]] != color:
            return group
        group.add(pos)
        neighbour = ((0, -1), (0, 1), (1, 0), (-1, 0))
        for n in neighbour:
            pos_neig = (pos[0] + n[0], pos[1] + n[1])
            if not pos_neig in group:
                group = self.get_group(pos_neig, color, group)
        return group

    def get_liberties(self, pos, color):
        """ Función que comprueba las libertades que tiene el grupo al que
        pertenece la posición pasada por parámetro.
        :Param pos: Posición perteneciente al grupo en la buscaremos si sus
        vecinos pertenecen o no al grupo.
        :Type pos: tuple.
        :Param group: grupo de posiciones que se encuentran dentro del grupo.
        :Type group: set. """

        liberties = set()
        group = self.get_group(pos, color)
        neighbour = ((0, -1), (0, 1), (1, 0), (-1, 0))
        for pos in group:
            for n in neighbour:
                pos_neig = (pos[0] - n[0], pos[1] - n[1])
                if not self.goban[pos_neig[0]][pos_neig[1]]:
                    liberties.add(pos_neig)
        return liberties

    def is_last_liberty(self, pos, color):
        """ Comprobamos que la posición dada sea la última libertad del
        grupo.
        :Param pos: Posición perteneciente al grupo en la buscaremos si sus
        vecinos pertenecen o no al grupo.
        :Type pos: tuple.
        :Param group: grupo de posiciones que se encuentran dentro del grupo.
        :Type group: set. """

        neighbour = ((0, -1), (0, 1), (1, 0), (-1, 0))
        for n in neighbour:
            pos_neig = (pos[0] - n[0], pos[1] - n[1])
            if len(get_liberties(pos_neig, color)) == 1:
                return True
        return False

    def is_move_kill(self, pos, color):
        """ Comprobamos que un movimiento capture un grupo.
        :Param pos: Posición perteneciente al grupo en la buscaremos si sus
        vecinos pertenecen o no al grupo.
        :Type pos: tuple.
        :Param group: grupo de posiciones que se encuentran dentro del grupo.
        :Type group: set. """
        if color == BLACK:
            return is_last_liberty(pos, WHITE)
        elif color == WHITE:
            return is_last_liberty(pos, BLACK)

    def invalid_ko_move(self, move):
        """ Comprueba si el movimiento es un movimiento inválido de ko.
        :Param move: Movimiento a comprobar.
        :Type move: Move. """
        if not self.moves:
            return False
        prev_move = self.moves[-1]
        around_pos = ((-1, 0), (1, 0), (0, -1), (0, 1))
        if not (prev_move.x - move.x, prev_move.y - move.y) in around_pos:
            return False
        for p in around_pos:
            try:
                if self.goban[move.x + p[0]][move.y + p[1]] == move.color:
                    return False
            except IndexError: # Stone is in the edge goban
                pass
        return True

    def add_move(self, move):
        """ Agregamos movimiento al tablero y a la lista de movimientos.
        Comprobando anteriormente si ese movimiento es válido. """
        print self.invalid_move(move), "MOVE"
        if not self.invalid_move(move):
            print "add", move.color
            self.goban[move.x][move.y] = move.color
            self.moves.append(move)

    def add_stones_to_statistical(self, stones):
        """Recorremos la lista de piedras pasadas por parámetros para buscar
        hacer comprobaciones estadísticas en esas piedras, luego recorremos la
        lista de piedras guardada y la actualizamos. Actualiza kifu, igs y el
        tablero donde guardamos el estado de las piedras cuando detecta
        estadísticamente que una piedra se ha puesto.

        :Param stones: lista de piedras
        :Type stones: list """

        for st in stones:
            self.statistical[st.x][st.y][0] += 1
            self.statistical[st.x][st.y][1] -= 1
            values = self.statistical[st.x][st.y]
            if values[1] <= 0 and values[0] > 0:
                if not self.goban[st.x][st.y]:
                    print "Add", st.x + 1, st.y + 1
                    self.kifu.add_stone(st)
                    self.statistical[st.x][st.y] = [0, 8]
                    self.add_move(st)

        for st in self.stones.difference(stones):
            self.statistical[st.x][st.y][0] -= 1
            self.statistical[st.x][st.y][1] -= 1
            values = self.statistical[st.x][st.y]
            if values[1] <= 0 and values[0] > 0:
                if not self.goban[st.x][st.y]:
                    print "Add", st.x + 1, st.y + 1
                    self.kifu.add_stone(st)
                    self.statistical[st.x][st.y] = [0, 8]
                    self.add_move(st)
            elif values[1] <= 0 and values[0] > 0:
                self.statistical[st.x][st.y] = [0, 8]
                if self.goban[st.x][st.y]:
                    print "Piedra %d, %d quitada?." % (st.x, st.y)
                    # TODO comprobar piedras capturadas
                # falsa piedra
        self.stones.update(stones)

    def print_st(self):
        string = ""
        for x in range(self.size):
            for y in range(self.size):
                string += '%s' % str(self.statistical[y][x])
            string += "   " + str(x + 1) + "\n"
        return string

    def __str__(self):
        string = ""
        for x in range(self.size):
            for y in range(self.size):
                if self.goban[y][x] == BLACK:
                    string += " x "
                elif self.goban[y][x] == WHITE:
                    string += " o "
                elif not self.goban[y][x]:
                    string += " · "
            string += "   " + str(x + 1) + "\n"
        return string
