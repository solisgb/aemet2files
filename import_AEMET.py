# -*- coding: latin-1 -*-

"""
lectura y escritura en nuevo formato
"""


class Import_AEMET():

    BUFSIZE_WESTACIONES = 10240
    BUFSIZE_WRESTO = 102400

    def __init__(self):
        pass

    @staticmethod
    def get_name(fname, suffix):
        """
        inserta un sufijo en el nombre de un fichero fname
        """
        from os.path import splitext
        a = splitext(fname)
        return a[0] + suffix + a[1]

    @staticmethod
    def new_format_pt():
        """
        a partir de un fichero de texto del aemet con datos de p tmax y tmin y
        separador ;
        escribe 3 ficheros (p, tmax, timin) con format estacion fecha dato y
        separador \t
        """

        from calendar import monthrange
        from datetime import date, timedelta
        from os.path import join
        from parameters import Parameters

        par = Parameters()
        festaciones = open(join(par.dir_out, par.festaciones), 'w',
                           Import_AEMET.BUFSIZE_WESTACIONES)
        festaciones.write('INDICATIVO\tNOMBRE\tALTITUD\tC_X\tC_Y\tNOM_PROV\t' +
                          'LONGITUD\tLATITUD\n')

        fp = open(join(par.dir_out, par.fp), 'w', Import_AEMET.BUFSIZE_WRESTO)
        ftmax = open(join(par.dir_out, par.ftmax), 'w',
                     Import_AEMET.BUFSIZE_WRESTO)
        ftmin = open(join(par.dir_out, par.ftmin), 'w',
                     Import_AEMET.BUFSIZE_WRESTO)

        d1 = timedelta(days=1)
        P1 = 10
        TMAX1 = 41
        TMIN1 = 72
        estaciones = []

        lines = [line.rstrip('\n') for line in
                 open(join(par.dir_dat, par.aemetpt), 'r')]
        for line in lines[1:]:
            words = line.split(';')
            if words[0] not in estaciones:
                print(words[0])
                estaciones.append(words[0])
                festaciones.write('{0}\t{1}\t{2}\t{3}\t{4}\t{5}\t{6}\t{7}\n'
                                  .format(words[0], words[3], words[4],
                                          words[5], words[6], words[7],
                                          words[8], words[9]))
            nd = monthrange(int(words[1]), int(words[2]))[1]
            ip = P1
            itmax = TMAX1
            itmin = TMIN1

            # P
            d0 = date(int(words[1]), int(words[2]), 1)
            for i in range(nd-1):
                if len(words[ip]) > 0:
                    if int(words[ip]) < 0:
                        words[ip] = '0'
                    fp.write('{0}\t{1}\t{2}\n'.format(words[0],
                             d0.strftime('%d/%m/%Y'), words[ip]))
                d0 = 0+d1
                ip += 1

            # MAX
            d0 = date(int(words[1]), int(words[2]), 1)
            for i in range(nd-1):
                if len(words[itmax]) > 0:
                    ftmax.write('{0}\t{1}\t{2}\n'.format(words[0],
                                d0.strftime('%d/%m/%Y'), words[itmax]))
                d0 = d0 + d1
                itmax += 1

            # TMIN
            d0 = date(int(words[1]), int(words[2]), 1)
            for i in range(nd-1):
                if len(words[itmin]) > 0:
                    ftmin.write('{0}\t{1}\t{2}\n'.format(words[0],
                                d0.strftime('%d/%m/%Y'), words[itmin]))
                d0 = d0 + d1
                itmin += 1

        festaciones.flush()
        festaciones.close()
        fp.flush()
        fp.close()
        ftmax.flush()
        ftmax.close()
        ftmin.flush()
        ftmin.close()

    def write_voids_files(self, pv=True, tmaxv=True, tminv=True):
        """
        a partir de los ficheros de p tmax y tmin
        grabados con el método new_format_pt
        escribe los huevos (sin datos) de cada uno de los ficheros
        controlado por pv tmaxv tminv
        """
        from os.path import join
        from parameters import Parameters

        par = Parameters()

        if pv:
            print('Huecos de p')
            fname = join(par.dir_out, par.fp)
            self.write_voids_file(fname)

        if tmaxv:
            print('Huecos de tmax')
            fname = join(par.dir_out, par.ftmax)
            self.write_voids_file(fname)

        if tminv:
            print('Huecos de tmin')
            fname = join(par.dir_out, par.ftmin)
            self.write_voids_file(fname)

    def write_voids_file(self, fname):
        """
        fname es uno de los nombres de ficheros grabados con new_format_pt
        escribe el fichero de huecos del fichero
        y también un fichero de estaciones que tienen hueco para ese tipo
        de datos
        """

        from datetime import date, timedelta

        name = Import_AEMET.get_name(fname, '_voids')
        fvoid = open(name, 'w', Import_AEMET.BUFSIZE_WRESTO)
        name = Import_AEMET.get_name(fname, '_estaciones')
        festaciones = open(name, 'w', Import_AEMET.BUFSIZE_WRESTO)

        d1 = timedelta(days=1)
        estaciones = []

        lines = [line.rstrip('\n') for line in open(fname, 'r')]
        for line in lines:
            words = line.split('\t')
            if words[0] not in estaciones:
                print(words[0])
                estaciones.append(words[0])
                festaciones.write('{0}\n'.format(words[0]))
                sdate = words[1].split('/')
                d0 = date(int(sdate[2]), int(sdate[1]), int(sdate[0]))
                continue

            d0 += d1
            sdate = words[1].split('/')
            dl = date(int(sdate[2]), int(sdate[1]), int(sdate[0]))

            while True:
                if d0 == dl:
                    break
                else:
                    fvoid.write('{0}\t{1}\n'.format(words[0],
                                d0.strftime('%d/%m/%Y')))
                    d0 += d1

        festaciones.flush()
        festaciones.close()
        fvoid.flush()
        fvoid.close()
