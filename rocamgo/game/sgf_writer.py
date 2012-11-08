import os
import datetime as dt

from rocamgo.cte import WHITE, BLACK


class SGFWriter:
    """ Crea el SGF de una partida a partir de la lista de movimientos. """
    @staticmethod
    def write(game):
        path = "sgf"
        filename = (str(dt.datetime.now().strftime("%Y-%m-%d %H.%M.%S")) +
            " white vs_black")
        out = os.path.join(path, filename + ".sgf")
        # Mandatory
        header = ["(;FF[4]GM[1]\n"]
        # Known
        header.append("AP[Rocamgo 0.33]\n")
        header.append("DT[%s]" % game.info.date)
        header.append("PB[%s]\n" % game.info.black_name)
        header.append("PW[%s]\n" % game.info.white_name)
        header.append("RU[%s]\n" % game.info.ruleset)
        header.append("KM[%s]\n" % game.info.komi)
        header.append("SZ[%s]\n" % game.info.size)
        # Optional
        if game.info.black_rank:
            header.append("BR[%s]\n" % game.info.black_rank)
        if game.info.white_rank:
            header.append("WR[%s]\n" % game.info.white_rank)

        with open(out, "w") as f:
            # TODO: Get proper values from game information
            f.writelines(header)
            for m in game.move_list:
                coord = chr(m.x + 97) + chr(m.y + 97)
                if m.color == BLACK:
                    f.write("\n;B[%s]" % coord)
                elif m.color == WHITE:
                    f.write("\n;W[%s]" % coord)
            f.write(")")
        f.close
