"""Normalize DOCX text fonts without changing text, images or intended weight.

Requires lxml (available in the document workspace runtime). Writes a new file.
Use --check for a read-only audit. Font installation and visual QA remain separate.
"""
import argparse
import re
from pathlib import Path
from zipfile import ZipFile
from lxml import etree

W = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
A = 'http://schemas.openxmlformats.org/drawingml/2006/main'
NS = {'w': W, 'a': A}


def w(tag):
    return '{' + W + '}' + tag


def target(name):
    name = name.replace('\\', '/')
    return bool(re.fullmatch(r'word/(document|styles|stylesWithEffects|header\d*|footer\d*|footnotes|endnotes|comments)\.xml', name))


def update_xml(data, family, is_theme=False):
    root = etree.fromstring(data)
    if is_theme:
        for node in root.xpath('//a:fontScheme/a:majorFont/* | //a:fontScheme/a:minorFont/*', namespaces=NS):
            if etree.QName(node).localname in ('latin', 'ea', 'cs') or node.get('script') in ('Hans', 'Hant'):
                node.set('typeface', family)
    else:
        for pr in root.xpath('//w:rPr', namespaces=NS):
            rf = pr.find(w('rFonts'))
            if rf is None:
                rf = etree.Element(w('rFonts'))
                pr.insert(0, rf)
            rf.attrib.clear()
            for role in ('ascii', 'hAnsi', 'eastAsia', 'cs'):
                rf.set(w(role), family)
            rf.set(w('hint'), 'eastAsia')
            for basic, complex_tag in [('b', 'bCs'), ('i', 'iCs'), ('sz', 'szCs')]:
                node = pr.find(w(basic))
                if node is not None:
                    mirror = pr.find(w(complex_tag))
                    if mirror is None:
                        mirror = etree.SubElement(pr, w(complex_tag))
                    mirror.attrib.clear()
                    mirror.set(w('val'), node.get(w('val'), '1'))
    return etree.tostring(root, xml_declaration=True, encoding='UTF-8', standalone=True)


def audit(path, family):
    problems = []
    count = 0
    with ZipFile(path) as z:
        for name in z.namelist():
            if not target(name):
                continue
            count += 1
            root = etree.fromstring(z.read(name))
            for pr in root.xpath('//w:rPr', namespaces=NS):
                rf = pr.find(w('rFonts'))
                if rf is None or any(rf.get(w(k)) != family for k in ('ascii', 'hAnsi', 'eastAsia', 'cs')):
                    problems.append(name + ': non-unified or inherited font')
                elif any('theme' in etree.QName(k).localname.lower() for k in rf.attrib):
                    problems.append(name + ': theme font override')
                for basic, complex_tag in [('b', 'bCs'), ('i', 'iCs'), ('sz', 'szCs')]:
                    node, mirror = pr.find(w(basic)), pr.find(w(complex_tag))
                    if node is not None and (mirror is None or mirror.get(w('val'), '1') != node.get(w('val'), '1')):
                        problems.append(name + ': inconsistent ' + basic + '/' + complex_tag)
    return count, sorted(set(problems))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input', type=Path)
    parser.add_argument('output', nargs='?', type=Path)
    parser.add_argument('--font', default='Microsoft YaHei')
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    if not args.font.strip():
        parser.error('--font must not be empty')
    if args.check:
        if args.output:
            parser.error('--check accepts only an input file')
        count, problems = audit(args.input, args.font)
        print('\n'.join(problems) if problems else f'PASS: {count} XML parts use consistent text fonts and explicit weights.')
        return 1 if problems else 0
    if args.output is None:
        parser.error('provide a new output path or use --check')
    if args.output.resolve() == args.input.resolve() or args.output.exists():
        parser.error('output must be a new file; input is preserved')
    with ZipFile(args.input) as src, ZipFile(args.output, 'x') as dst:
        for info in src.infolist():
            data = src.read(info.filename)
            name = info.filename.replace('\\', '/')
            if target(name) or name == 'word/theme/theme1.xml':
                data = update_xml(data, args.font, name == 'word/theme/theme1.xml')
            dst.writestr(info, data)
    count, problems = audit(args.output, args.font)
    if problems:
        raise RuntimeError('; '.join(problems))
    print(f'PASS: normalized {count} XML parts. Output: {args.output}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
