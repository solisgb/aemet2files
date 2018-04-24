# -*- coding: latin-1 -*-

"""
lee el fichero de P, Tmax y Tmin diaria de un único fichero de AEMET que
    contiene todos tipos de datos1"""

if __name__ == "__main__":

    try:
        import traceback
        import logging
        from comunes import query_yes_no
        import import_AEMET as aemet

        aemet.print_parameters()
        a = query_yes_no('desea continuar?')

        if a:
            print('Procesando')
            aemet.change_format()

        else:
            print('script interrumpido por el usuario')

        print('proceso finalizado', end=' ')
    except Exception as e:
        logging.error(traceback.format_exc())
    finally:
        print('fin')
