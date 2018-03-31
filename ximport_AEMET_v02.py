# -*- coding: latin-1 -*-

"""
lee el fichero de P, Tmax y Tmin diaria de un único fichero de AEMET que
contiene todos tipos de datos
"""

if __name__ == "__main__":

    try:
        import traceback
        import logging
        from parameters import Parameters
        from comunes import query_yes_no
        from import_AEMET import Import_AEMET

        par = Parameters()

        par.print()
        a = 1
#        a = query_yes_no('desea continuar?')

        if a:
            print('Procesando')
            aemet = Import_AEMET()
#            aemet.new_format_pt()
#
#            print('Fichero de dias sin datos')
#            aemet.write_voids_files()

            # para crear un fichero de huecos especifico
            aemet.write_voids_file(r'E:\WORK\CHS\aemet\out\TDIFD.txt')

        else:
            print('script interrumpido por el usuario')

        print('ok', end=' ')
    except Exception as e:
        logging.error(traceback.format_exc())
    finally:
        print('fin')
