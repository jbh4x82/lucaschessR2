import builtins
import locale
import os

import polib

import Code


class Translations:
    def __init__(self, lang):
        self.lang = self.check_lang(lang)
        self.dic_translate = self.read_mo()
        self.dic_openings = self.read_po_openings()
        builtins.__dict__["_X"] = self.x
        builtins.__dict__["_F"] = self.f
        builtins.__dict__["_FO"] = self.translate_opening
        builtins.__dict__["_SP"] = self.sp
        builtins.__dict__["_"] = self.translate
        Code.lucas_chess = "%s %s" % (self.translate("Lucas Chess"), Code.VERSION)

    @staticmethod
    def sinonimos(dic):
        def pon(key, keybase):
            if keybase in dic:
                dic[key] = dic[keybase]

        pon("X-ray attack", "X-Ray attack")
        pon("Attacking Defender", "Attacking defender")

    def read_mo(self):
        path_mo = self.get_path(self.lang)
        mofile = polib.mofile(path_mo)
        dic = {entry.msgid: entry.msgstr for entry in mofile}
        self.sinonimos(dic)
        return dic

    def read_po_openings(self):
        path_po = self.get_path_openings(self.lang)
        pofile = polib.pofile(path_po)
        return {entry.msgid: entry.msgstr for entry in pofile}

    def translate(self, txt):
        trans = self.dic_translate.get(txt)
        if trans is None:
            trans = txt
            if "||" in txt:
                trans = txt[: txt.index("||")].strip()
            self.dic_translate[txt] = trans
        return trans

    def translate_opening(self, opening):
        return self.dic_openings.get(opening, opening)

    @staticmethod
    def get_path(lang):
        path_locale = Code.path_resource("Locale")
        return "%s/%s/LC_MESSAGES/lucaschess.mo" % (path_locale, lang)

    @staticmethod
    def get_path_openings(lang):
        path_locale = Code.path_resource("Locale")
        return "%s/%s/LC_MESSAGES/lcopenings.po" % (path_locale, lang)

    def check_lang(self, lang):
        if not lang:
            lang = "en"
            li_info = locale.getdefaultlocale()
            if len(li_info) == 2:
                if li_info[0]:
                    lang = li_info[0][:2]
        path = self.get_path(lang)
        return lang if os.path.isfile(path) else "en"

    def f(self, txt):
        return self.translate(txt) if txt else ""

    def sp(self, key):
        if not key:
            return ""
        key = key.strip()
        t = self.f(key)
        if t == key:
            li = []
            for x in key.split(" "):
                if x:
                    li.append(_F(x))
            return " ".join(li)
        else:
            return t

    @staticmethod
    def x(key, op1, op2=None, op3=None):
        if not key:
            return ""
        resp = key.replace("%1", op1)
        if op2:
            resp = resp.replace("%2", op2)
            if op3:
                resp = resp.replace("%3", op3)
        return resp


def install(lang):
    if Code.translations is None or Code.translations.lang != lang:
        Code.translations = Translations(lang)
