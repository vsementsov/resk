"""Create the sharing card from the existing vector logo and brand font.

Requires fontTools, Pillow and the rsvg-convert CLI (librsvg2-bin on Ubuntu).
The artwork is composed as SVG; JPEG is the delivery format for link previews.
"""
from io import BytesIO
from pathlib import Path
import subprocess
import xml.etree.ElementTree as ET

from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.ttLib import TTFont
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
SVG = 'http://www.w3.org/2000/svg'
ET.register_namespace('', SVG)
font = TTFont(ROOT / 'content/source-assets/noto-bold.ttf')
glyphs = font.getGlyphSet()
cmap = font.getBestCmap()
units = font['head'].unitsPerEm


def heading(text, baseline, size, color):
    group = ET.Element(f'{{{SVG}}}g', {
        'transform': f'translate(210 {baseline}) scale({size / units} {-size / units})',
        'fill': color,
    })
    offset = 0
    for char in text:
        glyph = glyphs[cmap[ord(char)]]
        pen = SVGPathPen(glyphs)
        glyph.draw(pen)
        if pen.getCommands():
            ET.SubElement(group, f'{{{SVG}}}path', {
                'd': pen.getCommands(), 'transform': f'translate({offset} 0)',
            })
        offset += glyph.width
    return group


card = ET.fromstring(f'''<svg xmlns="{SVG}" width="1200" height="630" viewBox="0 0 1200 630">
<title>РЕСК — комплексный сервис для вашего объекта</title>
<rect width="1200" height="630" fill="#ffffff"/>
<path d="M1010 0H1200V630H1120Q990 400 1010 0" fill="#f0f6f9"/>
<rect x="0" y="614" width="1200" height="16" fill="#102942"/>
<rect x="0" y="614" width="210" height="16" fill="#CC4751"/>
</svg>''')
logo = ET.parse(ROOT / 'content/source-assets/logo.svg').getroot()
logo.attrib.update({'x': '210', 'y': '100', 'width': '720', 'height': '223.2'})
card.append(logo)
card.append(heading('Комплексный сервис', 425, 48, '#102942'))
card.append(heading('для вашего объекта', 490, 48, '#326891'))

source = ROOT / 'content/source-assets/social-preview.svg'
ET.ElementTree(card).write(source, encoding='utf-8', xml_declaration=True)
png = subprocess.run(['rsvg-convert', str(source)], check=True, capture_output=True).stdout
dest = ROOT / 'dist/assets/social-preview.jpg'
Image.open(BytesIO(png)).convert('RGB').save(dest, quality=90, optimize=True, progressive=True)
print(f'Sharing card: {dest.name}, 1200×630, {dest.stat().st_size / 1024:.0f} KB')
