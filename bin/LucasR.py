#!/usr/bin/env python
# ==============================================================================
# Author : Lucas Monge, lukasmonk@gmail.com
# Web : http://lucaschess.pythonanywhere.com/
# Blog : http://lucaschess.blogspot.com
# Licence : GPL 3.0
# ==============================================================================

# Chess leagues.
# Chess league es una herramienta que permite jugar contra un conjunto de motores o los motores entre sí.
# Toma el sistema de organización de las ligas de fútbol.
# Está organizada en divisiones ordenadas por nivel de mayor nivel a menor.
# Se juega todos contra todos, con blancas y con negras en cada temporada y por jornadas.
# De una temporada a la siguiente un número determinado de oponentes cambia de división, los primeros a la división anterior y los últimos a la siguiente.
# Se puede decidir que este número sea cero y no haya cambios de división.

# TODO cuando no está activado el background del tutor, se puede seguir el background, controlando que si llega a alguno de los límites, se pare el proceso
#      el mismo método, pero en el dispatch se comprueba time/depth del tutor.
#      Poder seleccionar el tipo de tutor, work in background, analysis previous, analysis after, analysis parallel without limit, analysis in parallel

# TODO ventana de variantes, rastrear cambios en el tamaño, cuando graba un cambio diferente, debiera permitirse unicamente cuando se haga manualmente

# TODO puzzles lichess, crear la super database_puzzles_lichess para operar con las openings lines especíicamente, se puede pedir que descargue de

# TODO analisis de variantes cuando el movimiento original está analizado y no se quiere reanalizar

# TODO incluir en el análisis la gráfica de tiempo usado en cada jugada

# TODO consultando database, Siguiente, no cambia el título de la ventana.

# TODO XXIII) Maybe some of these links could be useful in documents. I let you see.
#   Opening lines : http://lucaschess.blogspot.com/2018/02/version-1106-opening-lines.html + http://lucaschess.blogspot.com/2018/07/version-1110-opening-lines-training.html
#   Scanner : http://lucaschess.blogspot.com/2015/12/future-version-10-step-05-scanner-of.html
#   Personalities : http://lucaschess.blogspot.com/2011/09/version-60-beta-1-personalities.html

# TODO, cuarta opción para seleccionar el color a jugar, la siguiente, teniendo en cuenta la última vez.

# TODO STS https://rebel13.nl/misc/sts.html

# TODO links to eboards in about/web

# TODO I am thinking about a cache with all information of all moves, analysis, variations, comments, that user can import/export to the games

# TODO para comprobar que un movimiento es brillante, hay que ver que en las anteriores profundidades la diferencia con el elegido es de al menos 0.9 pawn

# TODO base de datos con puzzles, download complete.

# TODO en linux, comprobar que cambia iconos bien

# TODO Databases New, cambios, guardar, cambios en tags, grabar, no lo permite de nuevo, porque lo considera duplicado
# TODO Databases New, cambios, replay, bien, replay otra vez no hace nada.


# TODO lcbook: all positions of a player or a database, todas se ponen en modo espejo y se buscan en modo espejo como white, espejo = se cambia la fila=abs(fila-9)
#       sqlite clave = Util.lc_md5(fen espejo) valor=movimiento=numero|movimiento=numero|....
#       se elige como um libro bin normal, el mejor, random, random según peso.
#

# Para determinar que un puzzle ha terminado, es necesario que los movimientos no sean unicos/precisos, que se abran las posibilidades con la puntuación consolidada.


import sys

import warnings

warnings.simplefilter("ignore") #, UserWarning)

n_args = len(sys.argv)
if n_args == 1:
    import Code.Base.Init

    Code.Base.Init.init()

elif n_args >= 2:
    arg = sys.argv[1].lower()
    if arg.endswith(".pgn") or arg.endswith(".lcdb") or arg.endswith(".lcsb") or arg == "-play" or arg.endswith(".bmt"):
        import Code.Base.Init

        Code.Base.Init.init()

    elif arg == "-kibitzer":
        import Code.Kibitzers.RunKibitzer

        Code.Kibitzers.RunKibitzer.run(sys.argv[2])

    elif arg == "-translate":
        import Code.Translations.RunTranslate

        Code.Translations.RunTranslate.run_wtranslation(sys.argv[2])

    elif arg == "-tournament":
        import Code.Tournaments.RunTournament

        user = sys.argv[4] if len(sys.argv) >= 5 else ""
        Code.Tournaments.RunTournament.run(user, sys.argv[2], sys.argv[3])

    elif arg == "-league":
        import Code.Leagues.RunLeague

        user = sys.argv[3] if len(sys.argv) >= 4 else ""
        Code.Leagues.RunLeague.run(user, sys.argv[2])
