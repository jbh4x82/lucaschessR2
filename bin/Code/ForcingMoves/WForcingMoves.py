import time

import FasterCode
from PySide2 import QtCore, QtGui

import Code
from Code.Board import Board
from Code.QT import Colocacion, Controles, Iconos, QTUtil, QTVarios, QTUtil2
from Code.QT import LCDialog


class WForcingMoves(LCDialog.LCDialog):
    def __init__(self, owner):
        """
        @type owner: Code.ForcingMoves.ForcingMoves.ForcingMoves
        """

        LCDialog.LCDialog.__init__(self, owner.owner, _("Forcing moves"), Iconos.Count(), "runcounts")
        self.owner = owner
        self.pvs = owner.rm.pv.split(" ")

        self.configuration = Code.configuration

        conf_board = self.configuration.config_board("RUNCOUNTS", 64)

        # self.board = Board.BoardEstaticoMensaje(self, conf_board, None)
        self.board = Board.BoardEstatico(self, conf_board)
        self.board.crea()
        self.board.set_dispatcher(self.player_has_moved)
        self.board.dbvisual_set_show_allways(False)
        self.board.enable_all()
        self.li_checks_found = []
        self.li_captures_found = []
        self.must_find_best_move = False
        self.found_best_move = False

        self.level = 0

        # Rotulo informacion
        self.lb_info_game = Controles.LB(self, _("You can indicate the moves directly on the board.")).ponTipoLetra(
            puntos=self.configuration.x_pgn_fontpoints
        )

        # Movimientos
        self.ed_moves = Controles.ED(self, "").ponTipoLetra(puntos=32)
        #  self.ed_moves.setValidator(QtGui.QIntValidator(self.ed_moves))
        self.ed_moves.setAlignment(QtCore.Qt.AlignRight)
        self.ed_moves.anchoFijo(72)

        ly = Colocacion.H().relleno().control(self.ed_moves).relleno()

        self.gb_counts = Controles.GB(self, _("Number of checks"), ly).ponFuente(Controles.TipoLetra(puntos=10, peso=75))

        self.lb_result = Controles.LB(self).ponTipoLetra(puntos=10, peso=500).anchoFijo(254).altoFijo(32).set_wrap()
        self.lb_info = (
            Controles.LB(self).ponTipoLetra(puntos=14, peso=500).anchoFijo(254).set_foreground_backgound("white", "#496075").align_center()
        )

        # Botones
        li_acciones = (
            (_("Close"), Iconos.MainMenu(), self.terminar),
            None,
            (_("Begin"), Iconos.Empezar(), self.begin),
            (_("Check"), Iconos.Check(), self.check),
            (_("Continue"), Iconos.Pelicula_Seguir(), self.seguir),
        )
        self.tb = QTVarios.LCTB(self, li_acciones, style=QtCore.Qt.ToolButtonTextBesideIcon, icon_size=32)
        self.show_tb(self.terminar, self.begin)

        ly_right = (
            Colocacion.V()
                .control(self.tb)
                .controlc(self.lb_info)
                .relleno()
                .control(self.gb_counts)
                .relleno()
                .control(self.lb_result)
                .relleno()
        )

        ly_center = Colocacion.H().control(self.board).otro(ly_right)

        ly = Colocacion.V().otro(ly_center).control(self.lb_info_game).margen(3)

        self.setLayout(ly)

        self.restore_video()
        self.adjustSize()

        # Tiempo
        self.time_base = time.time()

        self.gb_counts.setDisabled(True)

        self.pon_info_posic()
        self.set_position()
        self.begin()

    def player_has_moved(self, from_sq, to_sq, promotion=""):
        move = from_sq + to_sq
        # print(move)
        if self.must_find_best_move:
            if move in self.owner.li_best_moves:
                self.board.remove_arrows()
                self.board.creaFlechaTmp(move[:2], move[-2:], False)
                self.lb_result.set_foreground("green")
                self.lb_result.set_text(_("You found the best move!"))
                self.lb_info.set_text(_("Success!"))
                self.found_best_move = True
                self.ed_moves.set_text("")
                # self.ed_moves.hide()
                # self.gb_counts.hide()
                self.show_tb(self.seguir)
            return

        if self.level == 1:
            if move in self.owner.li_checks and move not in self.li_checks_found:
                self.board.creaFlechaTmp(move[:2], move[-2:], False)
                self.li_checks_found.append(move)
                self.ed_moves.set_text("%s" % len(self.li_checks_found))
                if len(self.owner.li_checks) == len(self.li_checks_found):
                    self.check()
        else:
            if move in self.owner.li_captures and move not in self.li_captures_found:
                self.board.creaFlechaTmp(move[:2], move[-2:], False)
                self.li_captures_found.append(move)
                self.ed_moves.set_text("%s" % len(self.li_captures_found))
                if len(self.owner.li_captures) == len(self.li_captures_found):
                    self.check()

    def pulsada_celda(self, celda):  # Incluida por compatibilidad del Board
        if not self.found_best_move:
            return
        if (self.level + 1) > len(self.pvs):
            QTUtil2.message_bold(self, _("You reached the end of the line!"))
            return
        if self.pvs[self.level].startswith(celda):
            self.ed_moves.set_text(celda)
        elif self.pvs[self.level].startswith(self.ed_moves.text() + celda):
            self.board.creaFlechaTmp(self.ed_moves.text(), celda, False)
            self.level += 1
            self.lb_info.set_text(_("PV level %s" % self.level))
            self.ed_moves.set_text("")
            if (self.level + 1) > len(self.pvs):
                self.lb_info.set_text(_("PV level %s" % self.level))
                self.lb_result.set_text(_("You reached the end of the line!"))
                self.lb_info.set_text(_("Finished PV level %s!" % self.level))
                self.ed_moves.hide()
                self.gb_counts.hide()
                return

    def set_position(self):
        self.board.set_position(self.owner.board.last_position)
        siW = self.owner.board.last_position.is_white
        self.board.set_side_bottom(siW)
        self.board.set_side_indicator(siW)
        self.board.activate_side(siW)
        self.ed_moves.setFocus()

    def pon_info_posic(self):
        self.lb_info.set_text(_("Find forcing moves"))

    def closeEvent(self, event):
        self.save_video()
        event.accept()

    def terminar(self):
        self.save_video()
        self.reject()

    def show_tb(self, *lista):
        for opc in self.tb.dic_toolbar:
            self.tb.setAccionVisible(opc, opc in lista)
        QTUtil.refresh_gui()

    def begin(self):
        self.seguir()

    def ask_is_bm_check(self):
        if self.owner.checks > 0:
            if QTUtil2.pregunta(self, _("Is one of the checks the best move?")):
                if self.owner.bm_is_check:
                    if self.owner.rm.mate > 0:
                        QTUtil2.message_bold(self, _("Correct. The best check forces mate! Find it."))
                    else:
                        QTUtil2.message_bold(self, _("Correct! Now play the winning check."))
                    return True
                else:
                    QTUtil2.message_bold(self, _("The best move is not a check."))
                    return False
            else:
                if self.owner.bm_is_check:
                    if self.owner.rm.mate > 0:
                        QTUtil2.message_bold(self, _("The best move is a check and forces mate! Find it."))
                        return True
                    else:
                        QTUtil2.message_bold(self, _("The best move is a check. Now play it."))
                        return True
        return False

    def ask_is_bm_capture(self):
        if self.owner.captures > 0:
            if QTUtil2.pregunta(self, _("Is one of the captures the best move?")):
                if self.owner.bm_is_capture:
                    if self.owner.rm.mate > 0:
                        QTUtil2.message_bold(self, _("Correct. The best capture forces mate! Find it."))
                    elif self.owner.bm_is_discovered_attack:
                        QTUtil2.message_bold(self, _("Correct! It creates a discovered attack. Now play the winning capture."))
                    else:
                        QTUtil2.message_bold(self, _("Correct! Now play the winning capture."))
                    return True
                else:
                    QTUtil2.message_bold(self, _("The best move is not a capture."))
                    return False
            else:
                if self.owner.bm_is_capture:
                    if self.owner.rm.mate > 0:
                        QTUtil2.message_bold(self, _("The best move is a capture and forces mate! Find it."))
                    elif self.owner.bm_is_discovered_attack:
                        QTUtil2.message_bold(self, _("The best move is a capture and creates a discovered attack. Now play it."))
                    else:
                        QTUtil2.message_bold(self, _("The best move is a capture. Now play it."))
                    return True
            return False
        return False

    def ask_is_bm_threat(self):
        if QTUtil2.pregunta(self, _("Is the best move threatening anything new?")):
            if not self.owner.bm_is_threat and self.owner.rm.mate == 0:
                QTUtil2.message_bold(self, _("The best move is not threatening anything new - try to find it."))
            else:
                if self.owner.rm.mate > 0:
                    QTUtil2.message_bold(self, _("Correct. The best move forces mate! Find it."))
                elif self.owner.bm_is_mate_threat:
                    QTUtil2.message_bold(self, _("Correct. The best move threatens mate! Find it."))
                else:
                    QTUtil2.message_bold(self, _("Correct. Find it."))
        else:
            if not self.owner.bm_is_threat and self.owner.rm.mate == 0:
                QTUtil2.message_bold(self, _("Correct."))
            else:
                if self.owner.rm.mate > 0:
                    QTUtil2.message_bold(self, _("The best move forces mate! Find it."))
                elif self.owner.bm_is_mate_threat:
                    QTUtil2.message_bold(self, _("The best move threatens mate! Find it."))
                elif self.owner.bm_is_discovered_attack:
                    QTUtil2.message_bold(self, _("The best move creates a discovered attack! Find it."))
                else:
                    QTUtil2.message_bold(self, _("The best move creates a new threat! Find it."))

        self.board.remove_arrows()
        arrow_count = 0
        for move in self.owner.li_all_moves:
            if move not in self.owner.li_checks and move not in self.owner.li_captures:
                if "q" in move:
                    move = move[:4]  # handle crowning
                if arrow_count <= 6 or move in self.owner.li_best_moves:
                    if self.owner.bm_is_threat and move in self.owner.li_threats:
                        self.board.creaFlechaTmp(move[:2], move[-2:], False)
                        arrow_count += 1
                    elif not self.owner.bm_is_threat:
                        self.board.creaFlechaTmp(move[:2], move[-2:], False)
                        arrow_count += 1

    def seguir(self):
        if self.found_best_move:
            self.lb_result.set_text(_("Click the board to indicate the best continuation"))
            self.lb_info.set_text(_("PV level 1"))
            self.gb_counts.set_text(_("Next move"))
            self.lb_info_game.set_text(_("If you click the right square, the square name will appear in the text box."))
            self.level = 1
            self.gb_counts.show()
            self.ed_moves.show()
            self.show_tb(self.terminar)
            return

        if self.level == 1:
            if self.ask_is_bm_check():
                self.lb_result.set_text(_("Which check is the best move?"))
                self.must_find_best_move = True
                self.gb_counts.hide()
                self.ed_moves.hide()
                self.show_tb(self.terminar)
                return
        if self.level == 2:
            if self.ask_is_bm_capture():
                self.lb_result.set_text(_("Which capture is the best move?"))
                self.must_find_best_move = True
                self.gb_counts.hide()
                self.ed_moves.hide()
                self.show_tb(self.terminar)
                return
            else:
                self.ask_is_bm_threat()
                self.must_find_best_move = True
                self.lb_result.set_text(_("Indicate the best move!"))
                self.gb_counts.hide()
                self.ed_moves.hide()
                self.show_tb(self.terminar)
                return

        self.board.remove_arrows()
        self.lb_result.set_text("")
        self.ed_moves.set_text("")

        self.show_tb()

        # Ponemos el toolbar
        self.show_tb(self.check, self.terminar)

        # Activamos capturas
        self.gb_counts.setEnabled(True)

        # Marcamos el tiempo
        self.time_base = time.time()

        self.ed_moves.setFocus()
        self.level += 1
        if self.level == 2:
            self.gb_counts.set_text(_("Number of captures"))

    def check(self):
        tiempo = time.time() - self.time_base

        try:
            num_moves_calculated = int(self.ed_moves.texto())
        except:
            num_moves_calculated = 0

        if self.level == 1:  # checks

            ok = num_moves_calculated == self.owner.checks #  len(moves)
            self.lb_result.set_text(_("There are %s check(s).") % self.owner.checks)
            if ok:
                self.lb_result.set_foreground("green")
                self.gb_counts.setEnabled(False)
            else:
                self.lb_result.set_foreground("red")

            self.board.remove_arrows()
            for move in self.owner.li_checks:
                self.board.creaFlechaTmp(move[:2], move[-2:], False)

            self.show_tb(self.terminar, self.seguir)
        else:  # captures
            ok = num_moves_calculated == self.owner.captures #  len(moves)
            self.lb_result.set_text(_("There are %s capture(s).") % self.owner.captures)
            if ok:
                self.lb_result.set_foreground("green")
                self.gb_counts.setEnabled(False)
            else:
                self.lb_result.set_foreground("red")

            self.board.remove_arrows()
            for move in self.owner.li_captures:
                self.board.creaFlechaTmp(move[:2], move[-2:], False)

            self.show_tb(self.terminar, self.seguir)


