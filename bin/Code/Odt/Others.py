import os
import datetime
from Code.Odt import XML


class Manifest(XML.XML):
    def __init__(self):
        XML.XML.__init__(self, "rdf:RDF")
        self.add_param("xmlns:rdf", "http://www.w3.org/1999/02/22-rdf-syntax-ns#")
        element1 = XML.Element("rdf:Description")
        element1.add_param("rdf:about", "styles.xml")
        self.add_content(element1)
        element2 = XML.Element("rdf:type")
        element2.add_param("rdf:resource", "http://docs.oasis-open.org/ns/office/1.2/meta/odf#StylesFile")
        element1.add_content(element2)
        element3 = XML.Element("rdf:Description")
        element3.add_param("rdf:about", "")
        self.add_content(element3)
        element4 = XML.Element("ns0:hasPart")
        element4.add_param("xmlns:ns0", "http://docs.oasis-open.org/ns/office/1.2/meta/pkg#")
        element4.add_param("rdf:resource", "styles.xml")
        element3.add_content(element4)
        element5 = XML.Element("rdf:Description")
        element5.add_param("rdf:about", "content.xml")
        self.add_content(element5)
        element6 = XML.Element("rdf:type")
        element6.add_param("rdf:resource", "http://docs.oasis-open.org/ns/office/1.2/meta/odf#ContentFile")
        element5.add_content(element6)
        element7 = XML.Element("rdf:Description")
        element7.add_param("rdf:about", "")
        self.add_content(element7)
        element8 = XML.Element("ns0:hasPart")
        element8.add_param("xmlns:ns0", "http://docs.oasis-open.org/ns/office/1.2/meta/pkg#")
        element8.add_param("rdf:resource", "content.xml")
        element7.add_content(element8)
        element9 = XML.Element("rdf:Description")
        element9.add_param("rdf:about", "")
        self.add_content(element9)
        element10 = XML.Element("rdf:type")
        element10.add_param("rdf:resource", "http://docs.oasis-open.org/ns/office/1.2/meta/pkg#Document")
        element9.add_content(element10)

    def run(self, folder):
        path_manifest = os.path.join(folder, "manifest.rdf")
        self.save(path_manifest)


class Meta(XML.XML):
    def __init__(self):
        XML.XML.__init__(self, "office:document-meta")
        self.add_param("xmlns:grddl", "http://www.w3.org/2003/g/data-view#")
        self.add_param("xmlns:meta", "urn:oasis:names:tc:opendocument:xmlns:meta:1.0")
        self.add_param("xmlns:office", "urn:oasis:names:tc:opendocument:xmlns:office:1.0")
        self.add_param("xmlns:ooo", "http://openoffice.org/2004/office")
        self.add_param("xmlns:xlink", "http://www.w3.org/1999/xlink")
        self.add_param("xmlns:dc", "http://purl.org/dc/elements/1.1/")
        self.add_param("office:version", "1.3")
        element1 = XML.Element("office:meta")
        self.add_content(element1)
        element2 = XML.Element("meta:creation-date")
        element1.add_content(element2)
        hoy = datetime.datetime.now()
        element2.set_value(hoy.strftime("%Y-%m-%dT%H:%M:%S.%f"))
        element3 = XML.Element("meta:document-statistic")
        element3.add_param("meta:table-count", "0")
        element3.add_param("meta:image-count", "0")
        element3.add_param("meta:object-count", "0")
        element3.add_param("meta:page-count", "1")
        element3.add_param("meta:paragraph-count", "0")
        element3.add_param("meta:word-count", "0")
        element3.add_param("meta:character-count", "0")
        element3.add_param("meta:non-whitespace-character-count", "0")
        element1.add_content(element3)
        element4 = XML.Element("meta:generator")
        element1.add_content(element4)
        element4.set_value("Lucas Chess")

    def run(self, folder):
        path_manifest = os.path.join(folder, "meta.xml")
        self.save(path_manifest)


class MetaINF(XML.XML):
    def __init__(self):
        XML.XML.__init__(self, "manifest:manifest")
        self.add_param("xmlns:manifest", "urn:oasis:names:tc:opendocument:xmlns:manifest:1.0")
        self.add_param("manifest:version", "1.3")
        self.add_param("xmlns:loext", "urn:org:documentfoundation:names:experimental:office:xmlns:loext:1.0")
        element1 = XML.Element("manifest:file-entry")
        element1.add_param("manifest:full-path", "/")
        element1.add_param("manifest:version", "1.3")
        element1.add_param("manifest:media-type", "application/vnd.oasis.opendocument.text")
        self.add_content(element1)
        element2 = XML.Element("manifest:file-entry")
        element2.add_param("manifest:full-path", "Configurations2/accelerator/current.xml")
        element2.add_param("manifest:media-type", "")
        self.add_content(element2)
        element3 = XML.Element("manifest:file-entry")
        element3.add_param("manifest:full-path", "Configurations2/")
        element3.add_param("manifest:media-type", "application/vnd.sun.xml.ui.configuration")
        self.add_content(element3)
        element4 = XML.Element("manifest:file-entry")
        element4.add_param("manifest:full-path", "manifest.rdf")
        element4.add_param("manifest:media-type", "application/rdf+xml")
        self.add_content(element4)
        element5 = XML.Element("manifest:file-entry")
        element5.add_param("manifest:full-path", "styles.xml")
        element5.add_param("manifest:media-type", "text/xml")
        self.add_content(element5)
        element6 = XML.Element("manifest:file-entry")
        element6.add_param("manifest:full-path", "meta.xml")
        element6.add_param("manifest:media-type", "text/xml")
        self.add_content(element6)
        element7 = XML.Element("manifest:file-entry")
        element7.add_param("manifest:full-path", "settings.xml")
        element7.add_param("manifest:media-type", "text/xml")
        self.add_content(element7)
        element8 = XML.Element("manifest:file-entry")
        element8.add_param("manifest:full-path", "content.xml")
        element8.add_param("manifest:media-type", "text/xml")
        self.add_content(element8)
        element9 = XML.Element("manifest:file-entry")
        element9.add_param("manifest:full-path", "layout-cache")
        element9.add_param("manifest:media-type", "application/binary")
        self.add_content(element9)
        element10 = XML.Element("manifest:file-entry")
        element10.add_param("manifest:full-path", "Thumbnails/thumbnail.png")
        element10.add_param("manifest:media-type", "image/png")
        self.add_content(element10)

    def add_png(self, internal_path):
        element = XML.Element("manifest:file-entry")
        element.add_param("manifest:full-path", internal_path)
        element.add_param("manifest:media-type", "image/png")
        self.add_content(element)

    def run(self, folder):
        folder_meta = os.path.join(folder, "META-INF")
        os.mkdir(folder_meta)
        path_manifest = os.path.join(folder_meta, "manifest.xml")
        self.save(path_manifest)
