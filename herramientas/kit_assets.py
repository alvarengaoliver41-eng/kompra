"""Builds every image/vector asset of the Komprá brand kit."""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cairosvg
from PIL import Image
from logo import wordmark, iso_parts, text_path, text_width, pill_at, PILL

Y, L, P, C, A = '#0E2A1F', '#C8F03C', '#FF5FA2', '#F6F1E7', '#ECE5D5'
SLOGAN = 'Komprá de todo, en un solo lugar.'
KIT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'kit-de-marca') + '/'

WM = wordmark(**PILL)  # d, acc, (bx, by, bw, bh)
ISO = iso_parts('k', ('unb', 900), 60, 0)


def mk(path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    return path


def svg_doc(w, h, body, vb=None):
    vb = vb or f'0 0 {w} {h}'
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="{vb}">{body}</svg>'


def save(svg, svg_path=None, png_path=None, png_w=None):
    if svg_path:
        open(mk(svg_path), 'w').write(svg)
    if png_path:
        cairosvg.svg2png(bytestring=svg.encode(), write_to=mk(png_path), output_width=png_w)


# ---------- building blocks ----------
def logo_g(x, y, height, letters, accent):
    d, acc, (bx, by, bw, bh) = WM
    s = height / bh
    return (f'<g transform="translate({x - bx * s:.2f},{y - by * s:.2f}) scale({s:.5f})">'
            f'<path d="{d}" fill="{letters}"/><path d="{acc}" fill="{accent}"/></g>')


def logo_w(height):
    return WM[2][2] * height / WM[2][3]


def iso_g(cx, cy, size, fg, ac, scale=0.58):
    d, acc, (x, y, w, h) = ISO
    s = size * scale / max(w, h)
    tx = cx - (x + w / 2) * s
    ty = cy - (y + h / 2) * s
    return (f'<g transform="translate({tx:.2f},{ty:.2f}) scale({s:.5f})">'
            f'<path d="{d}" fill="{fg}"/><path d="{acc}" fill="{ac}"/></g>')


def T(text, x, y, size, color, key=('ins', 500), anchor='start', tracking=0.0):
    w = text_width(text, key, size, tracking)
    if anchor == 'middle':
        x -= w / 2
    elif anchor == 'end':
        x -= w
    d, _ = text_path(text, key, size, x=x, y=y, tracking=tracking)
    return f'<path d="{d}" fill="{color}"/>'


def wrap(text, key, size, maxw, tracking=0.0):
    lines, cur = [], ''
    for word in text.split(' '):
        t = (cur + ' ' + word).strip()
        if cur and text_width(t, key, size, tracking) > maxw:
            lines.append(cur)
            cur = word
        else:
            cur = t
    if cur:
        lines.append(cur)
    return lines


def PAR(text, x, y, size, maxw, color, key=('ins', 400), lh=1.45, anchor='start', tracking=0.0):
    out = []
    for i, line in enumerate(wrap(text, key, size, maxw, tracking)):
        out.append(T(line, x, y + i * size * lh, size, color, key, anchor, tracking))
    return ''.join(out), len(wrap(text, key, size, maxw, tracking)) * size * lh


def pill(cx, cy, length, thick, color, angle=45):
    return f'<path d="{pill_at(cx, cy, angle, length, thick)}" fill="{color}"/>'


def sticker(cx, cy, text, size, bg, fg, rot, key=('unb', 800), border=None):
    w = text_width(text, key, size)
    bw, bh = w + 1.8 * size, size * 2.24
    d, _ = text_path(text, key, size, x=-w / 2, y=size * 0.36)
    stroke = f' stroke="{border}" stroke-width="{size*0.12:.1f}"' if border else ''
    return (f'<g transform="translate({cx},{cy}) rotate({rot})">'
            f'<rect x="{-bw/2:.1f}" y="{-bh/2:.1f}" width="{bw:.1f}" height="{bh:.1f}" rx="{bh/2:.1f}" fill="{bg}"{stroke}/>'
            f'<path d="{d}" fill="{fg}"/></g>')


ICONS = {
    'como-komprar': '<path d="M3 4h2l2.4 11h11l2-8H6.2"/><circle cx="9" cy="20" r="1.4"/><circle cx="17" cy="20" r="1.4"/>',
    'envios': '<path d="M2.5 6.5h11v9.5h-11z"/><path d="M13.5 10h4l3 3.2v2.8h-7z"/><circle cx="6.5" cy="17.8" r="1.9"/><circle cx="17" cy="17.8" r="1.9"/>',
    'novedades': '<path d="M12 3l2.2 5.8L20 11l-5.8 2.2L12 19l-2.2-5.8L4 11l5.8-2.2z"/>',
    'opiniones': '<path d="M4 20l1.3-3.9A8 8 0 1 1 8 19z"/><path d="M9 11h6"/>',
    'ofertas': '<path d="M3 12.2V4h8.2l9.8 9.8-8.2 8.2z"/><circle cx="7.6" cy="7.6" r="1.4"/>',
    'freidora': '<path d="M5 9h14v7a4 4 0 0 1-4 4H9a4 4 0 0 1-4-4z"/><path d="M3 9h18M10 5.5c0-1 .8-1.5 2-1.5s2 .5 2 1.5V9h-4z"/>',
}


def icon(name, cx, cy, size, color, sw=1.5):
    s = size / 24
    return (f'<g transform="translate({cx - size/2:.1f},{cy - size/2:.1f}) scale({s:.4f})" fill="none" stroke="{color}" '
            f'stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round">{ICONS[name]}</g>')


# ---------- 01 logo ----------
def logos():
    d, acc, (bx, by, bw, bh) = WM
    vb = f'{bx:.0f} {by:.0f} {bw:.0f} {bh:.0f}'
    variants = {
        'komprá-logo-principal': (Y, P),
        'komprá-logo-fondo-oscuro': (C, L),
        'komprá-logo-una-tinta-yerba': (Y, Y),
        'komprá-logo-negro': ('#000000', '#000000'),
        'komprá-logo-blanco': ('#FFFFFF', '#FFFFFF'),
    }
    for name, (lc, ac) in variants.items():
        svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{bw/2:.0f}" height="{bh/2:.0f}" viewBox="{vb}">'
               f'<path d="{d}" fill="{lc}"/><path d="{acc}" fill="{ac}"/></svg>')
        save(svg, KIT + f'01 Logo/SVG/{name}.svg', KIT + f'01 Logo/PNG/{name}.png', 3000)
    # lockup with slogan
    for name, (lc, ac, sc) in {'komprá-logo-con-eslogan': (Y, P, Y),
                               'komprá-logo-con-eslogan-fondo-oscuro': (C, L, C)}.items():
        lh = 300
        lw = logo_w(lh)
        ss = 58
        sw = text_width(SLOGAN, ('unb', 600), ss, -0.02)
        W = max(lw, sw) + 40
        H = lh + 40 + ss * 1.6
        body = logo_g((W - lw) / 2, 0, lh, lc, ac) + T(SLOGAN, W / 2, lh + 40 + ss * 0.95, ss, sc, ('unb', 600), 'middle', -0.02)
        svg = svg_doc(round(W), round(H), body)
        save(svg, KIT + f'01 Logo/SVG/{name}.svg', KIT + f'01 Logo/PNG/{name}.png', 3000)


# ---------- 02 isotipo ----------
def isotipos():
    for name, (bg, fg, ac) in {'komprá-isotipo-yerba': (Y, L, P), 'komprá-isotipo-terere': (L, Y, P),
                               'komprá-isotipo-lapacho': (P, Y, L), 'komprá-isotipo-sin-fondo': (None, Y, P)}.items():
        rect = f'<rect width="1080" height="1080" fill="{bg}"/>' if bg else ''
        svg = svg_doc(1080, 1080, rect + iso_g(540, 540, 1080, fg, ac))
        save(svg, KIT + f'02 Isotipo/SVG/{name}.svg', KIT + f'02 Isotipo/PNG/{name}.png', 1080)
    fav = svg_doc(512, 512, f'<rect width="512" height="512" fill="{Y}"/>' + iso_g(256, 256, 512, L, P, 0.74))
    for px, nm in [(512, 'favicon-512.png'), (192, 'favicon-192.png'), (180, 'apple-touch-icon-180.png'), (32, 'favicon-32.png')]:
        save(fav, None, KIT + f'02 Isotipo/Favicon/{nm}', px)
    Image.open(KIT + '02 Isotipo/Favicon/favicon-512.png').save(KIT + '02 Isotipo/Favicon/favicon.ico', sizes=[(16, 16), (32, 32), (48, 48)])


# ---------- 03 redes ----------
def redes():
    R = KIT + '03 Redes/'
    perfil = svg_doc(1080, 1080, f'<rect width="1080" height="1080" fill="{Y}"/>' + iso_g(540, 540, 1080, L, P))
    save(perfil, None, R + 'perfil-instagram-facebook-whatsapp-1080.png', 1080)

    W, H = 1640, 624
    b = [f'<rect width="{W}" height="{H}" fill="{Y}"/>',
         pill(120, 90, 260, 120, P), pill(250, 560, 200, 90, L), pill(1530, 120, 220, 100, L),
         pill(1450, 540, 300, 130, P), pill(80, 360, 90, 44, C), pill(1600, 330, 90, 44, C)]
    mh = 210
    b.append(logo_g(W / 2 - logo_w(mh) / 2, 120, mh, C, L))
    b.append(T(SLOGAN, W / 2, 120 + mh + 78, 40, C, ('unb', 600), 'middle', -0.02))
    b.append(sticker(W / 2 - 250, 120 + mh + 170, 'Pagás al recibir', 26, L, Y, -4))
    b.append(sticker(W / 2 + 230, 120 + mh + 168, 'Envíos a todo Paraguay', 26, P, Y, 3))
    save(svg_doc(W, H, ''.join(b)), None, R + 'portada-facebook-1640x624.png', W)

    # post: background template + example
    def post(example):
        b = [f'<rect width="1080" height="1080" fill="{Y}"/>', logo_g(72, 72, 64, C, L), pill(1010, 90, 120, 50, P)]
        b.append(f'<g transform="rotate(-8 790 760)"><rect x="560" y="530" width="460" height="460" rx="64" fill="{A}"/></g>')
        if example:
            b.append(icon('freidora', 790, 760, 230, '#8A9A91', 1.1))
            for i, line in enumerate(wrap('Papas crocantes sin bañarlas en aceite.', ('unb', 800), 74, 560, -0.04)):
                b.append(T(line, 72, 300 + i * 80, 74, C, ('unb', 800), tracking=-0.04))
            b.append(sticker(250, 720, 'Gs. 420.000', 34, L, Y, -5))
            b.append(T('Envíos a todo Paraguay', 72, 1010, 30, L, ('ins', 600)))
        else:
            b.append(T('TU FOTO', 790, 772, 34, '#8A9A91', ('unb', 700), 'middle'))
        return svg_doc(1080, 1080, ''.join(b))
    save(post(False), None, R + 'plantillas/post-1080-fondo.png', 1080)
    save(post(True), None, R + 'plantillas/post-1080-ejemplo.png', 1080)

    def story(example):
        b = [f'<rect width="1080" height="1920" fill="{P}"/>',
             f'<g transform="rotate(-45 540 620)"><rect x="-300" y="510" width="1680" height="230" rx="115" fill="{Y}"/></g>',
             logo_g(540 - logo_w(90) / 2, 150, 90, Y, Y)]
        if example:
            b.append(T('BLACK', 96, 1400, 190, C, ('unb', 900), tracking=-0.05))
            b.append(T('FRIDAY', 96, 1580, 190, C, ('unb', 900), tracking=-0.05))
            b.append(T('Viernes 27 de noviembre', 96, 1700, 56, Y, ('unb', 800), tracking=-0.03))
            b.append(sticker(380, 1810, 'Avisame por WhatsApp', 40, L, Y, -4, border=Y))
        return svg_doc(1080, 1920, ''.join(b))
    save(story(False), None, R + 'plantillas/story-1080x1920-fondo.png', 1080)
    save(story(True), None, R + 'plantillas/story-1080x1920-ejemplo.png', 1080)

    for name in ['como-komprar', 'envios', 'novedades', 'opiniones', 'ofertas']:
        b = [f'<rect width="1080" height="1920" fill="{Y}"/>', icon(name, 540, 960, 400, L, 1.6),
             pill(760, 720, 120, 52, P)]
        save(svg_doc(1080, 1920, ''.join(b)), None, R + f'destacadas/destacada-{name}.png', 1080)


# ---------- 04 colores ----------
COLORS = [
    ('Yerba', Y, 'Fondos fuertes, textos, botones'),
    ('Tereré', L, 'Acento principal, botones, stickers'),
    ('Lapacho', P, 'Segundo acento, promos, la tilde en fondo claro'),
    ('Hueso', C, 'Fondo general'),
    ('Arena', A, 'Fondo de las fotos de producto, tarjetas'),
]


def rgb(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def cmyk(h):
    r, g, b = [v / 255 for v in rgb(h)]
    k = 1 - max(r, g, b)
    if k >= 1:
        return (0, 0, 0, 100)
    c, m, y = [(1 - v - k) / (1 - k) for v in (r, g, b)]
    return tuple(round(v * 100) for v in (c, m, y, k))


def colores():
    out = KIT + '04 Colores/'
    lines = ['KOMPRÁ · COLORES DE MARCA', '',
             'CMYK aproximado: pedile siempre una prueba de color a la imprenta.', '']
    for n, h, use in COLORS:
        lines += [n.upper(), f'  HEX   {h}', f'  RGB   {", ".join(map(str, rgb(h)))}',
                  f'  CMYK  {" / ".join(map(str, cmyk(h)))}', f'  Uso   {use}', '']
    lines += ['Texto secundario sobre Hueso: #4E5F57', '',
              'Proporción sugerida: 50 % Hueso o Arena, 30 % Yerba, 15 % Tereré, 5 % Lapacho.']
    open(mk(out + 'colores-komprá.txt'), 'w').write('\n'.join(lines))
    W, H = 2000, 900
    b = [f'<rect width="{W}" height="{H}" fill="#FFFFFF"/>']
    sw = (W - 160 - 4 * 30) / 5
    for i, (n, h, use) in enumerate(COLORS):
        x = 80 + i * (sw + 30)
        b.append(f'<rect x="{x:.1f}" y="80" width="{sw:.1f}" height="460" rx="36" fill="{h}" stroke="#E2DACA" stroke-width="2"/>')
        b.append(T(n, x, 610, 44, Y, ('unb', 700)))
        b.append(T(h, x, 665, 30, '#4E5F57', ('ins', 600)))
        b.append(T('RGB ' + ' '.join(map(str, rgb(h))), x, 708, 26, '#4E5F57', ('ins', 400)))
        b.append(T('CMYK ' + ' '.join(map(str, cmyk(h))), x, 746, 26, '#4E5F57', ('ins', 400)))
    save(svg_doc(W, H, ''.join(b)), None, out + 'paleta-komprá.png', W)


# ---------- 05 tipografias ----------
def tipografias():
    from fontTools.ttLib import TTFont
    out = mk(KIT + '05 Tipografías/x')
    out = os.path.dirname(out) + '/'
    base = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'node_modules', '@fontsource') + '/'
    for fam, folder, weights, nice in [('unbounded', 'unbounded', [600, 700, 800, 900], 'Unbounded'),
                                       ('instrument-sans', 'instrument-sans', [400, 500, 600, 700], 'InstrumentSans')]:
        names = {400: 'Regular', 500: 'Medium', 600: 'SemiBold', 700: 'Bold', 800: 'ExtraBold', 900: 'Black'}
        for w in weights:
            f = TTFont(f'{base}{folder}/files/{fam}-latin-{w}-normal.woff2')
            f.flavor = None
            f.save(f'{out}{nice}-{names[w]}.ttf')
        os.makedirs(out + 'Licencias', exist_ok=True)
        open(f'{out}Licencias/OFL-{nice}.txt', 'w').write(open(f'{base}{folder}/LICENSE').read())
    open(out + 'LEEME.txt', 'w').write(
        'TIPOGRAFÍAS DE KOMPRÁ\n\n'
        'Unbounded: títulos, precios, botones y stickers. Pesos: SemiBold, Bold, ExtraBold y Black.\n'
        'Instrument Sans: textos, descripciones y datos. Pesos: Regular, Medium, SemiBold y Bold.\n\n'
        'Para instalarlas: doble clic en cada archivo .ttf y después "Instalar".\n'
        'En Canva: Marca > Fuentes > Subir fuente.\n\n'
        'Estos archivos traen los caracteres del español (á, é, í, ó, ú, ñ, ü, ¿, ¡).\n'
        'Si necesitás letras del guaraní como ẽ, ĩ, ũ o ỹ, bajá las versiones completas gratis en\n'
        'fonts.google.com/specimen/Unbounded y fonts.google.com/specimen/Instrument+Sans\n\n'
        'Ambas son gratuitas y de uso comercial libre (licencia SIL Open Font License, en la carpeta Licencias).\n'
        '\nIMPORTANTE: el logo NO se escribe con la fuente. Usá siempre los archivos de la carpeta 01 Logo,\n'
        'porque la tilde del logo está dibujada a mano y no es la tilde de la tipografía.\n')


if __name__ == '__main__':
    logos(); print('logos')
    isotipos(); print('isotipos')
    redes(); print('redes')
    colores(); print('colores')
    tipografias(); print('tipografias')
