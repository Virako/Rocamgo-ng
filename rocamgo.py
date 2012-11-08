#!/usr/bin/python
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

""":var good_corners: últimas esquinas buenas encontradas
:Type good_corners: list
:var img: imagen actual sacada de la cámara o video
:Type img: IplImage
:var ideal_img: tablero en formato ideal
:Type ideal_img: IplImage
:var goban: Objeto tablero
:Type goban: Goban
:var stones: piedras detectadas como negras o blancas
:Type stones: list
:var key: tecla pulsada
:Type key: int
"""
import argparse

from cv import ShowImage
from cv import WaitKey
from cv import Circle

from rocamgo.cte import GOBAN_SIZE
from rocamgo.cte import __version__
from rocamgo.detection.capture_source import CaptureSource
from rocamgo.detection.goban import Goban as gdetect
from rocamgo.detection.record import Record
from rocamgo.replay.igs import Igs
from rocamgo.game.sgf_writer import SGFWriter
from rocamgo.goban import Goban


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
        img = cs.get_frame()
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
    parser.add_argument('--version', action='version', version=__version__)
    capture_source_arg_group = parser.add_mutually_exclusive_group(
        required='true')
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
