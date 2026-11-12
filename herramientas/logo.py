"""Komprá logo builder: glyph outlines from Unbounded + a drawn brand tilde."""
import math
import uharfbuzz as hb
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.boundsPen import BoundsPen

import os
FONTDIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'node_modules', '@fontsource') + '/'
FONTS = {
    ('unb', 600): FONTDIR + 'unbounded/files/unbounded-latin-600-normal.woff2',
    ('unb', 700): FONTDIR + 'unbounded/files/unbounded-latin-700-normal.woff2',
    ('unb', 800): FONTDIR + 'unbounded/files/unbounded-latin-800-normal.woff2',
    ('unb', 900): FONTDIR + 'unbounded/files/unbounded-latin-900-normal.woff2',
    ('ins', 400): FONTDIR + 'instrument-sans/files/instrument-sans-latin-400-normal.woff2',
    ('ins', 500): FONTDIR + 'instrument-sans/files/instrument-sans-latin-500-normal.woff2',
    ('ins', 600): FONTDIR + 'instrument-sans/files/instrument-sans-latin-600-normal.woff2',
    ('ins', 700): FONTDIR + 'instrument-sans/files/instrument-sans-latin-700-normal.woff2',
}
_cache = {}


def _font(key):
    if key not in _cache:
        tt = TTFont(FONTS[key])
        tt.flavor = None
        import io
        buf = io.BytesIO()
        tt.save(buf)
        face = hb.Face(buf.getvalue())
        _cache[key] = (tt, hb.Font(face))
    return _cache[key]


def text_path(text, key, size, x=0.0, y=0.0, tracking=0.0):
    """SVG path 'd' for text at pixel size; (x, y) is the baseline start. tracking in em."""
    tt, font = _font(key)
    upm = tt['head'].unitsPerEm
    buf = hb.Buffer()
    buf.add_str(text)
    buf.guess_segment_properties()
    hb.shape(font, buf, {'kern': True, 'liga': True})
    gs = tt.getGlyphSet()
    order = tt.getGlyphOrder()
    s = size / upm
    pen = SVGPathPen(gs)
    cx = 0
    for info, pos in zip(buf.glyph_infos, buf.glyph_positions):
        name = order[info.codepoint]
        tp = TransformPen(pen, (s, 0, 0, -s, x + (cx + pos.x_offset) * s, y - pos.y_offset * s))
        gs[name].draw(tp)
        cx += pos.x_advance + tracking * upm
    return pen.getCommands(), (cx - tracking * upm) * s


def text_width(text, key, size, tracking=0.0):
    return text_path(text, key, size, tracking=tracking)[1]


# ---------- the wordmark ----------
def capsule(p1, p2, r):
    """Path for a stadium shape between centers p1 and p2 (y-up font units already flipped by caller)."""
    (x1, y1), (x2, y2) = p1, p2
    a = math.atan2(y2 - y1, x2 - x1)
    nx, ny = -math.sin(a) * r, math.cos(a) * r
    return (f'M{x1+nx:.1f},{y1+ny:.1f} L{x2+nx:.1f},{y2+ny:.1f} '
            f'A{r:.1f},{r:.1f} 0 0 0 {x2-nx:.1f},{y2-ny:.1f} '
            f'L{x1-nx:.1f},{y1-ny:.1f} A{r:.1f},{r:.1f} 0 0 0 {x1+nx:.1f},{y1+ny:.1f} Z')


def wordmark(angle=38, length=300, thick=150, gap=70, cx_off=40, tracking=-0.035):
    """Returns (letters_d, accent_d, (minx, miny, w, h)) in font units, y down, baseline at y=0."""
    key = ('unb', 800)
    d, adv = text_path('kompra', key, 1000, tracking=tracking)
    # locate the final 'a'
    tt, _ = _font(key)
    gs = tt.getGlyphSet()
    a_w = tt['hmtx']['a'][0]
    a_x0 = adv - a_w
    bp = BoundsPen(gs)
    gs['a'].draw(bp)
    ax0, _, ax1, atop = bp.bounds
    xh = 590  # top of a's bowl
    cx = a_x0 + (ax0 + ax1) / 2 + cx_off
    r = thick / 2
    th = math.radians(angle)
    half = length / 2
    # centre so that the lowest point of the capsule sits gap above the x-height
    lowest_from_center = half * math.sin(th) + r
    cy = xh + gap + lowest_from_center
    p1 = (cx - half * math.cos(th), -(cy - half * math.sin(th)))
    p2 = (cx + half * math.cos(th), -(cy + half * math.sin(th)))
    acc = capsule(p1, p2, r)
    top = cy + half * math.sin(th) + r
    right = max(adv, p2[0] + r)
    return d, acc, (0, -top, right, top + 170)


def logo_svg(height, letters='#0E2A1F', accent='#FF5FA2', bg=None, pad=0, **kw):
    d, acc, (x, y, w, h) = wordmark(**kw)
    x -= pad; y -= pad; w += 2 * pad; h += 2 * pad
    width = height * w / h
    bgrect = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{bg}"/>' if bg else ''
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{x:.0f} {y:.0f} {w:.0f} {h:.0f}" '
            f'width="{width:.1f}" height="{height:.1f}">{bgrect}'
            f'<path d="{d}" fill="{letters}"/><path d="{acc}" fill="{accent}"/></svg>')


PILL = dict(angle=45, length=230, thick=200, gap=55, cx_off=40)


def pill_at(cx, cy, angle=45, length=230, thick=200):
    th = math.radians(angle)
    half = length / 2
    p1 = (cx - half * math.cos(th), cy + half * math.sin(th))
    p2 = (cx + half * math.cos(th), cy - half * math.sin(th))
    return capsule(p1, p2, thick / 2)


def iso_parts(letter='k', key=('unb', 900), pdx=0, pdy=0):
    """Letter path + pill in font units (y down, baseline 0). Pill sits above-right of the letter."""
    d, adv = text_path(letter, key, 1000)
    tt, _ = _font(key)
    gs = tt.getGlyphSet()
    name = tt.getBestCmap()[ord(letter)]
    bp = BoundsPen(gs)
    gs[name].draw(bp)
    x0, y0, x1, y1 = bp.bounds
    xh = tt['OS/2'].sxHeight + 17  # overshoot of round letters
    lowest = 230 / 2 * math.sin(math.radians(45)) + 100
    cx = (x0 + x1) / 2 + 150 + pdx
    cy = -(xh + 55 + lowest) + pdy
    acc = pill_at(cx, cy)
    # bbox of the union (approx: pill extents)
    r = 100
    ext = 230 / 2 * math.cos(math.radians(45)) + r
    bx0, bx1 = min(x0, cx - ext), max(x1, cx + ext)
    by0, by1 = min(-y1, cy - ext), max(-y0, cy + ext)
    return d, acc, (bx0, by0, bx1 - bx0, by1 - by0)


def iso_svg(size, bg='#0E2A1F', fg='#C8F03C', accent='#FF5FA2', letter='k', key=('unb', 900),
            scale=0.56, pdx=0, pdy=0, circle=False):
    d, acc, (x, y, w, h) = iso_parts(letter, key, pdx, pdy)
    s = size * scale / max(w, h)
    tx = size / 2 - (x + w / 2) * s
    ty = size / 2 - (y + h / 2) * s
    shape = (f'<circle cx="{size/2}" cy="{size/2}" r="{size/2}" fill="{bg}"/>' if circle
             else f'<rect width="{size}" height="{size}" fill="{bg}"/>')
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 {size} {size}">'
            f'{shape}<g transform="translate({tx:.2f},{ty:.2f}) scale({s:.5f})">'
            f'<path d="{d}" fill="{fg}"/><path d="{acc}" fill="{accent}"/></g></svg>')
