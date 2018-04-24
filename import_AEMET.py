# -*- coding: latin-1 -*-

"""
lectura y escritura en nuevo formato
"""

import import_AEMET_parameters as par
BUFSIZE_WESTACIONES = 10240
BUFSIZE_WRESTO = 102400
SUFFIX_FILE_NODAT = '_void'


def print_parameters():
    """imprime los parámetros del script"""
    print('dir datos: {}'.format(par.DIR_DAT))
    print('Fichero en formato AEMET: {}'.format(par.AEMETPT))
    print('ficheros de salida nuevo formato')
    print('dir resultados: {}'.format(par.DIR_OUT))
    print('Estaciones: {}'.format(par.FESTACIONES))
    print('P dmm {}'.format(par.FP))
    print('Tmax dgradoC {}'.format(par.FTMAX))
    print('Tmin dgradoC {}'.format(par.FTMIN))


def get_name(name):
    """añade el sufijo SUFFIX_FILE_NODAT al nombre de un fichero"""
    from os.path import splitext
    a = splitext(name)
    return a[0] + SUFFIX_FILE_NODAT + a[1]


def change_format():
    """
    lee el fichero suministrado por AEMET y escribe varios ficheros en el
        formato deseado:
            Un fichero de estaciones en el fichero de AEMET
            Un fichero para cada variable Pdiaria, Tmax diaria, Tmin diaria
            Un fichero con sufijo SUFFIX_FILE_NODAT para cada variable que
                indica los datos que faltan
    """
    from calendar import monthrange
    from datetime import date, timedelta
    from os.path import join

    festaciones = open(join(par.DIR_OUT, par.FESTACIONES),
                       'w', BUFSIZE_WESTACIONES)
    festaciones.write('INDICATIVO\tNOMBRE\tALTITUD\tC_X\tC_Y\tNOM_PROV\t' +
                      'LONGITUD\tLATITUD\n')

    fp = open(join(par.DIR_OUT, par.FP), 'w', BUFSIZE_WRESTO)
    name = get_name(par.FP)
    fp_void = open(join(par.DIR_OUT, name), 'w', BUFSIZE_WRESTO)

    ftmax = open(join(par.DIR_OUT, par.FTMAX), 'w', BUFSIZE_WRESTO)
    name = get_name(par.FTMAX)
    ftmax_void = open(join(par.DIR_OUT, name), 'w', BUFSIZE_WRESTO)

    ftmin = open(join(par.DIR_OUT, par.FTMIN), 'w', BUFSIZE_WRESTO)
    name = get_name(par.FTMIN)
    ftmin_void = open(join(par.DIR_OUT, name), 'w', BUFSIZE_WRESTO)

    D1 = timedelta(days=1)
    P1 = 10
    estaciones = []

    lines = [line.rstrip('\n') for line in open(join(par.DIR_DAT,
             par.AEMETPT), 'r')]
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
        d0 = date(int(words[1]), int(words[2]), 1)
        ip = P1

        # P
        for i in range(nd):
            if len(words[ip]) > 0:
                if int(words[ip]) < 0:
                    words[ip] = '0'
                fp.write('{0}\t{1}\t{2}\n'.format(words[0],
                         d0.strftime('%d/%m/%Y'), words[ip]))
            else:
                fp_void.write('{0}\t{1}\n'.format(words[0],
                              d0.strftime('%d/%m/%Y')))
            d0 = d0 + D1
            ip += 1

        # TMAX
        itmax = 41
        d0 = date(int(words[1]), int(words[2]), 1)
        for i in range(nd):
            if len(words[itmax]) > 0:
                ftmax.write('{0}\t{1}\t{2}\n'.format(words[0],
                            d0.strftime('%d/%m/%Y'), words[itmax]))
            else:
                ftmax_void.write('{0}\t{1}\n'.format(words[0],
                                 d0.strftime('%d/%m/%Y')))
            d0 = d0 + D1
            itmax += 1

        # TMIN
        itmin = 72
        d0 = date(int(words[1]), int(words[2]), 1)
        for i in range(nd):
            if len(words[itmin]) > 0:
                ftmin.write('{0}\t{1}\t{2}\n'.format(words[0],
                            d0.strftime('%d/%m/%Y'), words[itmin]))
            else:
                ftmin_void.write('{0}\t{1}\n'.format(words[0],
                                 d0.strftime('%d/%m/%Y')))
            d0 = d0 + D1
            itmin += 1

    files = [festaciones, fp, fp_void, ftmax, ftmax_void, ftmin, ftmin_void]
    for file in files:
        file.flush()
        file.close()
