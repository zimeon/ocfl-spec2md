#!/usr/bin/env python3
"""Hack to help convert OCFL specs to Markdown."""
import pathlib
import re
import textwrap
import xml.etree.ElementTree as ET

spec_src = "../ocfl-spec/draft/spec/index.html"
spec_dst = "docs/spec.md"
impl_src = "../ocfl-spec/draft/implementation-notes/index.html"
impl_dst = "docs/impl.md"
text_width = 72


class Bwaa(Exception):
    """My exception."""

    pass


class Markdown_Writer(object):
    """Write markdown output."""

    def __init__(self, ofh):
        """Initialize and set output filehandle."""
        self.ofh = ofh

    def line(self, *args):
        """Write a line."""
        text = " ".join(args)
        text = re.sub(r'''\s+''', ' ', text)
        self.ofh.write(textwrap.fill(text.strip(), width=text_width, break_long_words=False) + "\n")

    def para(self, *args):
        """Write a paragraph or block of Markdown, line with blank line following."""
        self.line(*args)
        self.ofh.write("\n")

    def example(self, text):
        """Write a preformatted example in Markdown."""
        self.ofh.write("```\n" + text.strip() + "\n```\n\n")


class Converter(object):
    """Convert from ReSpec HTML to Markdown."""

    def __init__(self):
        """Initialize."""
        self.writer = None

    def get_anchor(self, element):
        """Look for id tags in element and make markdown anchor."""
        anchor = element.attrib.get('id', None)
        return anchor

    def process_para(self, element, prefix=''):
        """Process a paragraph."""
        txt = prefix
        if element.text is not None:
            txt += element.text
        for child in element:
            text = child.text.strip() if child.text is not None else None
            if child.tag == 'a':
                if text is None:
                    print("FIXME need section label for " + child.attrib['href'])
                    text = 'FIXME'
                if 'href' in child.attrib:
                    txt += "[" + text + "](" + child.attrib['href'] + ")"
                else:
                    txt += "[" + text + "](#" + text + ")"
            elif child.tag == 'code':
                txt += "`" + text + "`"
            elif child.tag == 'span':
                # We only use <span. for id= anchors for errors and warnings,
                # we just replicate this in output
                txt += "<span id=" + child.attrib['id'] + ">" + text + "</span>"
            elif child.tag == 'i':
                txt += "_" + text + "_"
            elif child.tag == 'pre':
                self.process_pre(child, prefix)
            else:
                raise Bwaa("Unrecognized element in para: " + child.tag)
            if child.tail.strip() not in (None, ''):
                txt += child.tail
        if element.tail.strip() not in (None, ''):
            txt += element.tail
        self.writer.para(txt)

    def process_pre(self, element, prefix=''):
        """Process a pre example block."""
        self.writer.example(prefix + element.text)
        tail = element.tail.strip()
        if tail not in (None, ""):
            raise Bwaa("Unexpected tail text ", tail)

    def process_section(self, element, level=1):
        """Process one <section> block."""
        print("> level" + str(level) + ": ", element.tag, element.attrib)
        if 'id' not in element.attrib:
            pass
        elif element.attrib['id'] == 'sotd':
            self.writer.line("## Status of This Document")
            self.writer.para("{. #sotd}")
            self.writer.para("This document is draft of a potential specification. It has no official standing of any kind and does not represent the support or consensus of any standards organisation.")
            self.writer.para("INSERT_TOC_HERE")
            return
        elif element.attrib['id'] == 'conformance':
            self.writer.para("## Conformance")
            self.writer.para("As well as sections marked as non-normative, all authoring guidelines, diagrams, examples, and notes in this specification are non-normative. Everything else in this specification is normative.")
            self.writer.para("The key words may, must, must not, should, and should not are to be interpreted as described in [RFC2119].")
            return
        anchor = self.get_anchor(element)
        for child in element:
            if child.tag == 'section':
                self.process_section(child, (level + 1))
            elif child.tag in ('h1', 'h2', 'h3'):
                self.writer.line("#" * level, " ", child.text)
                if anchor is None:
                    self.writer.line('')
                else:
                    self.writer.para("{. #%s}" % (anchor))
                if child.tail.strip() not in (None, ""):
                    raise Bwaa("Unexpected tail text ", child.tail)
            elif child.tag == 'p':
                self.process_para(child)
            elif child.tag == 'pre':
                self.process_pre(child)
            elif child.tag == 'ul':
                for item in child:
                    self.process_para(item, prefix="  * ")
            elif child.tag == 'ol':
                n = 1
                for item in child:
                    self.process_para(item, prefix="  %d. " % n)
                    n += 1
            elif child.tag == 'dl':
                self.writer.para('DL LIST')
            elif child.tag == "table":
                self.writer.para('TABLE')
            elif child.tag == "blockquote":
                # We expect just paragraps inside blockquote
                for p in child:
                    if p.tag == 'p':
                        self.process_para(p, prefix='> ')
                    elif p.tag == 'pre':
                        self.process_pre(p, prefix='> ')
                    else:
                        raise Bwaa("Unexpected element in blockquote: " + p.tag)

            else:
                raise Bwaa("level%d unknown child: ", level, child.tag, child.attrib)

    def convert(self, src, dst, pre_amble=None):
        """Convert src ReSpec HTML to dst in Markdown."""
        # Read XML
        print("Reading %s" % (src))
        path = pathlib.Path(src)
        src_xml = path.read_text()
        # Remove non-XML bit
        src_xml = re.sub(' async ', ' ', src_xml)
        src_xml = re.sub('&mdash;', '&#x2014;', src_xml)
        root = ET.fromstring(src_xml)
        # Have parsed XML in root, now open dst for output and
        # then convert the chunks of the file by <section>
        with open(dst, 'w', encoding='utf-8') as ofh:
            self.writer = Markdown_Writer(ofh)
            body = root.find('body')
            for child in body:
                # At the top level we expect only <section> blocks, we will
                # parse these recursively
                if child.tag != 'section':
                    raise Bwaa("Unexpected tag")
                self.process_section(child, 2)


cnv = Converter()
try:
    cnv.convert(src=spec_src, dst=spec_dst)
    cnv.convert(src=impl_src, dst=impl_dst)
except Bwaa as e:
    print(e)