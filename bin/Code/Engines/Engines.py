import copy
import os
import os.path

import Code
from Code import Util
from Code.Engines import EngineRunDirect
from Code.Base.Constantes import ENG_EXTERNAL, ENG_INTERNAL


class Engine:
    def __init__(self, key="", autor="", version="", url="", path_exe="", args=None):
        self.key = key
        self.alias = key
        self.autor = autor
        self.args = [] if args is None else args
        self.version = version
        self.liUCI = []
        self.multiPV = 0
        self.maxMultiPV = 0
        self.siDebug = False
        self.nomDebug = None
        self.parent_external = None
        self.url = url
        self.path_exe = Util.relative_path(path_exe) if path_exe else ""
        self._name = None
        self.elo = 0
        self.id_info = ""
        self.max_depth = 0
        self.max_time = 0  # Seconds
        self.id_name = key
        self.id_author = autor
        self.book = None
        self.emulate_movetime = False

        self.menu = key
        self.type = ENG_INTERNAL
        # self.fixed_depth = None

        self.__li_uci_options = None

    def save(self):

        return Util.save_obj_pickle(self)

    def restore(self, txt):
        Util.restore_obj_pickle(self, txt)
        if self.parent_external:
            conf_parent = Code.configuration.dic_engines.get(self.parent_external)
            if conf_parent:
                self.path_exe = conf_parent.path_exe
        try:
            self.read_uci_options()
            return True
        except:
            return False

    def exists(self):
        return os.path.isfile(self.path_exe)

    def set_extern(self):
        self.type = ENG_EXTERNAL

    @property
    def is_external(self):
        return self.type == ENG_EXTERNAL

    @is_external.setter
    def is_external(self, value):
        self.type = ENG_EXTERNAL if value else ENG_INTERNAL

    def nombre_ext(self):
        name = self.name
        if self.is_external:
            name += " *"
        return name

    def clone(self):
        eng = Engine()
        eng.restore(self.save())
        return eng

    def argumentos(self):
        return self.args

    def debug(self, txt):
        self.siDebug = True
        self.nomDebug = self.key + "-" + txt

    def reset_uci_options(self):
        li_uci_options = self.li_uci_options()
        for op in li_uci_options:
            op.valor = op.default
        self.liUCI = []

    def ordenUCI(self, name, valor):
        li_uci_options = self.li_uci_options()
        is_changed = False
        for op in li_uci_options:
            if op.name == name:
                if op.tipo == "check":
                    if valor in ("true", "false"):
                        valor = valor == "true"
                op.valor = valor
                if op.default != valor:
                    is_changed = True
                    break
        for pos, (xcomando, xvalor) in enumerate(self.liUCI):
            if xcomando == name:
                if is_changed:
                    self.liUCI[pos] = (name, valor)
                else:
                    del self.liUCI[pos]
                return
        if is_changed:
            self.liUCI.append((name, valor))

    def set_multipv(self, num, maximo):
        self.multiPV = num
        self.maxMultiPV = maximo

    def update_multipv(self, xmultipv):
        if xmultipv == "PD":
            multiPV = min(self.maxMultiPV, 10)
            multiPV = max(multiPV, self.multiPV)
            for comando, valor in self.liUCI:
                if comando == "MultiPV":
                    multiPV = int(valor)
                    break
            self.multiPV = multiPV

        elif xmultipv == "MX":
            self.multiPV = self.maxMultiPV
        else:
            self.multiPV = int(xmultipv)
            if self.multiPV > self.maxMultiPV:
                self.multiPV = self.maxMultiPV

    def can_be_tutor(self):
        return self.maxMultiPV >= 4 and not self.is_maia()

    def is_maia(self):
        return "maia" in self.key

    def remove_log(self, fich):
        Util.remove_file(os.path.join(os.path.dirname(self.path_exe), fich))

    @property
    def name(self):
        if self._name:
            return self._name
        return Util.primera_mayuscula(self.key) + " " + self.version

    @name.setter
    def name(self, value):
        self._name = value

    def clona(self):
        return copy.deepcopy(self)

    def ejecutable(self):
        return self.path_exe

    def read_uci_options(self):
        name = Util.valid_filename("%s.uci_options" % self.key)
        path_uci_options = os.path.join(os.path.dirname(self.path_exe), name)
        if os.path.isfile(path_uci_options):
            with open(path_uci_options, "rt", encoding="utf-8", errors="ignore") as f:
                lines = f.read().split("\n")

        else:
            engine = EngineRunDirect.DirectEngine("-", self.path_exe, args=self.args)
            if engine.uci_ok:
                lines = engine.uci_lines
                engine.close()
                try:
                    with open(path_uci_options, "wt", encoding="utf-8", errors="ignore") as q:
                        for line in lines:
                            line = line.strip()
                            if line:
                                q.write(line + "\n")
                except:
                    pass

            else:
                lines = []

        self.__li_uci_options = []
        dc_op = {}

        for line in lines:
            line = line.strip()
            if line.startswith("id name"):
                self.id_name = line[8:]
            elif line.startswith("id author"):
                self.id_author = line[10:]
            elif line.startswith("option name "):
                op = OpcionUCI()
                if op.lee(line):
                    self.__li_uci_options.append(op)
                    dc_op[op.name] = op
                    if op.name == "MultiPV":
                        self.set_multipv(op.default, op.maximo)

        for comando, valor in self.liUCI:
            if comando in dc_op:
                op = dc_op[comando]
                op.valor = valor
                if op.name == "MultiPV":
                    self.set_multipv(valor, op.maximo)

        return self.__li_uci_options

    def li_uci_options(self):
        if self.__li_uci_options is None:
            self.read_uci_options()
        return self.__li_uci_options

    def li_uci_options_editable(self):
        return [op for op in self.li_uci_options() if op.tipo != "button"]

    def has_multipv(self):
        for op in self.li_uci_options_editable():
            if op.name == "MultiPV":
                return op.maximo > 3
        return False

    def current_multipv(self):
        for op in self.li_uci_options_editable():
            if op.name == "MultiPV":
                return int(op.valor)
        return self.multiPV

    def list_uci_changed(self):
        return self.liUCI

    def xhash(self):
        return hash(self.name + self.key)


class OpcionUCI:
    name = ""
    tipo = ""
    default = ""
    valor = ""
    minimo = 0
    maximo = 0
    li_vars = []

    def __str__(self):
        return "Name:%s - Type:%s - Default:%s - Value:%s - Min:%d - Max:%d - Vars:%s" % (
            self.name,
            self.tipo,
            self.default,
            self.valor,
            self.minimo,
            self.maximo,
            str(self.li_vars),
        )

    def lee(self, txt):
        while "  " in txt:
            txt = txt.replace("  ", " ")

        n = txt.find("type")
        if (n < 10) or ("chess960" in txt.lower()):
            return False

        self.name = txt[11:n].strip()
        li = txt[n:].split(" ")
        self.tipo = li[1]

        if self.tipo == "spin":
            resp = self.lee_spin(li)

        elif self.tipo == "check":
            resp = self.lee_check(li)

        elif self.tipo == "combo":
            resp = self.lee_combo(li)

        elif self.tipo == "string":
            resp = self.lee_string(li)

        elif self.tipo == "button":
            resp = True

        else:
            resp = False

        if resp:
            self.valor = self.default

        return resp

    def lee_spin(self, li):
        if len(li) >= 8:
            for x in [2, 4, 6]:
                n = li[x + 1]
                nm = n[1:] if n.startswith("-") else n
                if not nm.isdigit():
                    return False
                n = int(n)
                cl = li[x].lower()
                if cl == "default":
                    self.default = n
                elif cl == "min":
                    self.minimo = n
                elif cl == "max":
                    self.maximo = n
            return True
        else:
            return False

    def lee_check(self, li):
        if len(li) == 4 and li[2] == "default":
            self.default = li[3] == "true"
            return True
        else:
            return False

    def lee_string(self, li):
        if (len(li) == 3 or len(li) == 4) and li[
            2
        ] == "default":  # proposed by tico-tico in https://github.com/lukasmonk/lucaschess/issues/18
            self.default = "" if len(li) == 3 or li[3] == "<empty>" else li[3]  # proposed by tico-tico
            return True
        else:
            return False

    def lee_combo(self, li):
        self.li_vars = []
        self.default = ""
        siDefault = False
        nvar = -1
        for x in li[2:]:
            if x == "var":
                siDefault = False
                nvar += 1
                self.li_vars.append("")
            elif x == "default":
                siDefault = True
            else:
                if siDefault:
                    if self.default:
                        self.default += " "
                    self.default += x
                else:
                    c = self.li_vars[nvar]
                    if c:
                        c += " " + x
                    else:
                        c = x
                    self.li_vars[nvar] = c

        return self.default and (self.default in self.li_vars)

    def restore_dic(self, dic):
        self.tipo = dic["tipo"]
        self.name = dic["name"]
        self.default = dic["default"]
        self.valor = dic["valor"]

        if self.tipo == "spin":
            self.minimo = dic["minimo"]
            self.maximo = dic["maximo"]

        elif self.tipo == "combo":
            self.li_vars = dic["li_vars"]

    def save_dic(self):
        dic = {
            "tipo": self.tipo,
            "name": self.name,
            "default": self.default,
            "valor": self.valor,
            "minimo": self.minimo,
            "maximo": self.maximo,
            "li_vars": self.li_vars,
        }
        return dic

    def label_default(self):
        if self.tipo == "spin":
            return "%d:%d-%d" % (self.default, self.minimo, self.maximo)

        elif self.tipo == "check":
            return str(self.default).lower()

        elif self.tipo == "button":
            return str(self.default).lower()

        elif self.tipo == "combo":
            return self.default
        return ""


def engine_from_txt(pk_txt):
    engine = Engine()
    engine.restore(pk_txt)
    return engine


def read_engine_uci(exe, args=None):
    path_exe = Util.relative_path(exe)

    if args is None:
        args = []

    engine = EngineRunDirect.DirectEngine("-", exe, args=args)
    if engine.uci_ok:
        id_name = "-"
        id_author = "-"
        for linea in engine.uci_lines:
            linea = linea.strip()
            if linea.startswith("id name"):
                id_name = linea[8:]
            elif linea.startswith("id author"):
                id_author = linea[10:]
        me = Engine(id_name, id_author, id_name, "", path_exe)
        me._name = id_name
    else:
        me = None
    engine.close()
    return me
