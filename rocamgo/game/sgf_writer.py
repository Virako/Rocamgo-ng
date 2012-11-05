import os
import datetime as dt

from rocamgo.cte import HEADER_SGF, WHITE, BLACK

class SGFWriter:
    """ Crea el SGF de una partida a partir de la lista de movimientos. """
    @staticmethod
    def write(game):
        path = "sgf"
        filename = str(dt.datetime.now().strftime("%Y-%m-%d %H.%M.%S")) + " white vs_black"
        out = os.path.join(path, filename + ".sgf")
        with open(out, "w") as f:
            #TODO: Get proper values from game information
            f.writelines(HEADER_SGF)
            for m in game.move_list:
                coord = chr(m.x + 97) + chr(m.y + 97)
                if m.color == BLACK:
                    f.write("\n;B[%s]" %coord)
                elif m.color == WHITE:
                    f.write("\n;W[%s]" %coord)
            f.write(")")
        f.close