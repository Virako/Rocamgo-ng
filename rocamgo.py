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

""":var cam: Objeto Cameras
:Type cam: Cameras
:var cams_found: número de cámaras encontradas en el ordenador
:Type cams_found: int
:var camera: cámara que estamos usando
:Type camera: Camera
:var prev_corners: esquinas del tablero anteriores encontradas
:Type prev_corners: list
:var current_corners: esquinas actuales del tablero encontradas
:Type current_corners: list
:var good_corners: últimas esquinas buenas encontradas
:Type good_corners: list
:var img: imagen actual sacada de la cámara o video
:Type img: IplImage
:var ideal_img: tablero en formato ideal
:Type ideal_img: IplImage
:var goban: Objeto tablero
:Type goban: Goban
:var circles: circulos encontrado en la imagen
:Type circles: CvMat
:var false_stones: contador para piedras falsas, no son negras o blancas
:Type false_stones: int
:var stones: piedras detectadas como negras o blancas
:Type stones: list
:var pt: centro de la piedra
:Type pt: tuple
:var radious: radio de la piedra
:Type radious: float
:var color: color de la piedra
:Type color: int
:var key: tecla pulsada
:Type key: int
"""

from rocamgo.detection.cameras import Cameras
from rocamgo.detection.search_goban import search_goban
from rocamgo.detection.check_goban_moved import check_goban_moved
from rocamgo.detection.perspective import perspective
from rocamgo.detection.search_stones import search_stones
from rocamgo.detection.search_stones import check_color_stone
from rocamgo.game.move import Move
from rocamgo.game.sgf_writer import SGFWriter
from rocamgo.goban import Goban
from rocamgo.cte import BLACK
from rocamgo.cte import WHITE
from rocamgo.cte import GOBAN_SIZE
from copy import copy
from rocamgo.detection.record import Record
from cv import ShowImage
from cv import WaitKey
from cv import Circle
from cv import Get1D
from cv import Round
from cv import CV_RGB
import argparse
from rocamgo.replay.igs import Igs
from rocamgo.detection.capture_source import CaptureSource
from rocamgo.detection.goban import Goban as gdetect


def main(parser):

    print "Camer, video, record"
    print parser.camera
    print parser.video
    print parser.record

    cs = CaptureSource()
    gd = gdetect()

    if parser.camera:
        cs.camera(int(parser.camera))
        # TODO
        threshold = 190
    elif parser.video:
        cs.video(parser.video)
        threshold = 150
    if parser.record:
        record = Record(parser.record, cs.get_resolution())


    goban = Goban(GOBAN_SIZE)

    if parser.igs:
        igs = Igs(parser.igs[0], parser.igs[1])
        goban.kifu.attach(igs)
        # goban.set_igs_connection(igs)

    while True:
        # Select image from camera
        # TODO
        # img = camera.get_frame()
        img = cs.get_frame()  # Test videos
        if not img:
            break
        if parser.record:
            record.add_frame(img)

        ideal_img, good_corners = gd.extract(img)
        if good_corners:
            # Paint corners for tested
            for corner in good_corners:
                Circle(img, corner, 4, (255, 0, 0), 4, 8, 0)

        if ideal_img:
            ideal_img, stones = gd.search_stones(ideal_img, threshold)

            # Añadimos las piedras para trabajar con ellas estadísticamente
            goban.add_stones_to_statistical(stones)

            ShowImage("Ideal", ideal_img)

        ShowImage("Camera", img)

        key = WaitKey(1)
        if key == 27:  # Esc
            break
    SGFWriter.write(goban.kifu)
    if parser.igs is not None:
        igs.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Rocamgo option. ')
    parser.add_argument('--record', action='store',
         help='Record video for help to developers. ')
    parser.add_argument('--version', action='version', version='Rocamgo 0.33')
    capture_source_arg_group = parser.add_mutually_exclusive_group(required='true')
    capture_source_arg_group.add_argument('--camera', action='store',
        help='Numbers of cameras in the computer. ')
    capture_source_arg_group.add_argument('--video', action='store',
        help='Filename video. ')

    replay_arg_group = parser.add_argument_group('Available replayers:')
    # FIXME: Possible credential leak via shell history
    replay_arg_group.add_argument('--igs', nargs=2, metavar=('USER', 'PASS'),
        help='Replay game in IGS. Use USER and PASS as login credentials')


    results = parser.parse_args()

    main(results)
