#coding:utf-8
from datetime import datetime


class GameInfo:
    """ Informacion de la partida: Nombre y rango de los jugadores,
    reglas, etc. """
    def __init__(self):
        self.white_name = "White"
        """ Nombre del jugador que juega con piedras blancas
        :Type _white_name: str"""
        self.black_name = "Black"
        """ Nombre del jugador que juega con piedras negras
        :Type _black_name: str"""
        self.white_rank = None
        """ Rango del jugador que juega con piedras blancas
        :Type _white_rank: str"""
        self.black_rank = None
        """ Rango del jugador que juega con piedras negras
        :Type _black_rank: str"""
        self.size = 19
        """ Tamaño del tablero
        :Type _size: int"""
        self.komi = "6.5"
        """ Valor del komi (compensacion para blancas por jugar segundo)
        :Type _komi: str"""
        self.handicap = 0
        """ Handicap (piedras de ventaja para negras)
        :Type _handicap:int"""
        self.ruleset = "Japanese"
        """ Conjunto de reglas usadas
        :Type _ruleset: str"""
        self.date = datetime.now().strftime("%Y-%m-%d")
        """ Fecha de juego de la partida
        :Type _date: str"""
        self.event = None
        """ Nombre del evento (p.e. "III Open de Sevilla")
        :Type _event: str"""
        