# -*- coding: latin-1 -*-

"""
parametros
"""


class Parameters():

    # definifcion de los parametros

    # directorio fichero de datos de aemet
    # dir_dat=r'C:\Users\solil\Documents\_D\aemet_pt_2017'
    dir_dat = r'E:\WORK\CHS\aemet'

    # directorio fichero de resultados
    dir_out = r'E:\WORK\CHS\aemet\out'

    # fichero de datos de p tmax y tmin suministrado por aemet
    aemetpt = '300170346P_T.txt'

    # fichero de salida de estaciones en aemetpt
    festaciones = 'estaciones.txt'

    # fichero de salida de datos de p nuevo formato
    fp = 'p.txt'

    # fichero de salida de datos de tmax nuevo formato
    ftmax = 'tmax.txt'

    # fichero de salida de datos de tmain nuevo formato
    ftmin = 'tmin.txt'

    def __init__(self, sdir_dat=dir_dat, sdir_out=dir_out, saemetpt=aemetpt,
                 sfestaciones=festaciones, sfp=fp, sftmax=ftmax, sftmin=ftmin):

        self.dir_dat = sdir_dat
        self.dir_out = sdir_out
        self.aemetpt = saemetpt
        self.festaciones = sfestaciones
        self.fp = sfp
        self.ftmax = sftmax
        self.ftmin = sftmin

    def print(self):
        print('dir datas: ' + self.dir_dat)
        print('fichero único de datos p tmax tmin en formato AEMET: '
              + self.aemetpt)
        print('dir resultados: ' + self.dir_out)
        print('fichero de salida -> estaciones nuevo formato: '
              + self.festaciones)
        print('fichero de salida -> estacion fecha P dmm, nuevo formato: '
              + self.fp)
        print('fichero de salida -> estacion fecha Tmax dgradoC, ' +
              'nuevo formato: ' + self.ftmax)
        print('fichero de salida -> estacion fecha Tmax dgradoC, ' +
              'nuevo formato: ' + self.ftmin)
