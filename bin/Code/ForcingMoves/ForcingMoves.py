import FasterCode
from Code.QT import FormLayout
from Code.QT import Iconos
from Code.QT import QTUtil2
from Code.ForcingMoves import WForcingMoves


class ForcingMoves:
    def __init__(self, board, mrm, owner):
        """
        @type mrm: Code.Engines.EngineResponse.EngineResponse
        """

        self.board = board
        fen = self.board.last_position.fen()
        self.fen = fen
        self.li_checks = []
        self.li_captures = []
        self.li_threats = []
        self.li_check_targets = []
        self.li_capture_targets = []
        self.li_best_moves = []
        if len(mrm.li_rm) == 0:
            return
        self.rm = mrm.li_rm[0]
        self.li_best_moves.append(self.rm.from_sq + self.rm.to_sq)
        for rm in mrm.li_rm:
            if hasattr(rm, "nivelBMT"):
                if rm.nivelBMT == 0:
                    if (rm.from_sq + rm.to_sq) not in self.li_best_moves:
                        self.li_best_moves.append(rm.from_sq + rm.to_sq)

        FasterCode.set_fen(self.cut_fen(fen))
        self.position_is_check = FasterCode.ischeck()
        lista = FasterCode.get_exmoves()

        self.owner = owner
        self.checks = 0
        self.captures = 0
        self.bm_is_check = False
        self.bm_is_capture = False
        self.bm_is_threat = False
        self.bm_is_mate_threat = False
        self.bm_is_discovered_attack = False
        move_index = -1
        self.bm_move_index = 0
        self.nextmove_checks = 0
        self.nextmove_captures = 0
        self.nextmove_li_checks = []
        self.nextmove_li_captures = []
        self.li_all_moves = []
        self.nextmove_li_all_moves = []

        for infoMove in lista:
            move_index += 1
            self.li_all_moves.append(infoMove.move())

            if infoMove.move() in self.li_best_moves:
                self.bm_move_index = move_index

            if infoMove._check:
                print("Check: %s" % infoMove.move())
                self.checks += 1
                self.li_checks.append(infoMove.move())
                self.li_check_targets.append(infoMove.xto())
                if infoMove.move() in self.li_best_moves:
                    self.bm_is_check = True

            if infoMove._capture:
                print("Capture: %s" % infoMove.move())
                self.captures += 1
                self.li_captures.append(infoMove.move())
                self.li_capture_targets.append(infoMove.xto())
                if infoMove.move() in self.li_best_moves:
                    self.bm_is_capture = True

        for move in self.li_all_moves:
            print("Checking [%s] for new threats" % move)
            FasterCode.set_fen(self.cut_fen(self.fen))
            FasterCode.make_move(move)  # Make the first best move
            new_fen = FasterCode.get_fen()
            if " b " in new_fen:  # Change side so we get another move
                new_fen = new_fen.replace(" b ", " w ")
            else:
                new_fen = new_fen.replace(" w ", " b ")
            new_fen = self.cut_fen(new_fen)
            FasterCode.set_fen(new_fen)
            print("FEN after [%s]: %s" % (move, FasterCode.get_fen()))

            if move in self.li_best_moves:
                self.fen_after_best_move_and_null_move = new_fen

            print('All follow up moves: ' + ', '.join(FasterCode.get_moves()))
            lista = FasterCode.get_exmoves()
            for infoMove in lista:
               #  print("[%s] checking follow up move %s" % (move, infoMove.move()))
                if move in self.li_best_moves:
                    self.nextmove_li_all_moves.append(infoMove.move())
                if infoMove._mate:
                    print("Threatening mate on next move: %s" % infoMove.move())
                    self.add_threat(move)
                    if move in self.li_best_moves:
                        self.bm_is_threat = self.bm_is_mate_threat = True
                if infoMove._check:
                    print("Next move [%s] check: %s" % (move, infoMove.move()))
                    if move in self.li_best_moves:
                        self.nextmove_checks += 1
                        self.nextmove_li_checks.append(infoMove.move())
                    if infoMove.xto() not in self.li_check_targets:  # new check = threat
                        print("New check is threatened: %s" % infoMove.move())
                        self.add_threat(move)
                        if move in self.li_best_moves:
                            self.bm_is_threat = True
                if infoMove._capture:
                    print("Next move [%s] capture: %s" % (move, infoMove.move()))
                    if move in self.li_best_moves:
                        self.nextmove_captures += 1
                        self.nextmove_li_captures.append(infoMove.move())
                    if infoMove.xto() not in self.li_capture_targets:  # new capture = threat
                        if infoMove.xfrom() != self.rm.to_sq:  # a different piece now is attacking something
                            print("New discovered attack: %s" % infoMove.move())
                            self.add_threat(move)
                            if move in self.li_best_moves:
                                self.bm_is_discovered_attack = True
                                self.bm_is_threat = True
                        else:
                            print("New capture is threatened: %s" % infoMove.move())
                            self.add_threat(move)
                            if move in self.li_best_moves:
                                self.bm_is_threat = True

    def add_threat(self, move):
        print("%s is a threat!" % move)
        if move not in self.li_threats:
            self.li_threats.append(move)

    def fm_show_checklist(self):
        # Start with checks
        w = WForcingMoves.WForcingMoves(self)
        w.exec_()

    def cut_fen(self, fen):
        if " w " in fen:
            new_str = fen.partition(' w ')[0] + " w - 0 1"
        else:
            new_str = fen.partition(' b ')[0] + " b - 0 1"
        return new_str
