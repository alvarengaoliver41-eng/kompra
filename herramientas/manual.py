"""Komprá brand manual: one SVG per 16:9 page -> PDF."""
import base64
import io
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cairosvg
from pypdf import PdfWriter, PdfReader
from kit_assets import (Y, L, P, C, A, SLOGAN, KIT, WM, T, PAR, logo_g, logo_w, iso_g, pill, sticker,
                        icon, svg_doc, COLORS, rgb, cmyk, text_path)

W, H = 1920, 1080
MUTED = '#4E5F57'
RED = '#D7263D'
H1 = ('unb', 800)
H2 = ('unb', 700)
SUB = ('unb', 600)
BODY = ('ins', 400)
BODYM = ('ins', 500)
BOLD = ('ins', 700)
SEMI = ('ins', 600)


def img(path, x, y, w, h, extra=''):
    data = base64.b64encode(open(path, 'rb').read()).decode()
    return f'<image x="{x}" y="{y}" width="{w}" height="{h}" href="data:image/png;base64,{data}" {extra}/>'


def frame(num, section, body, bg=C, dark=False):
    fg = C if dark else MUTED
    head = T(f'{num:02d}  ·  {section}', 96, 92, 22, fg, SEMI)
    foot = (logo_g(W - 96 - logo_w(30), H - 78, 30, C if dark else Y, L if dark else P)
            + T('Manual de marca', 96, H - 56, 20, fg, BODYM))
    return svg_doc(W, H, f'<rect width="{W}" height="{H}" fill="{bg}"/>' + head + body + foot)


def title(text, y=210, color=Y, size=64):
    return T(text, 96, y, size, color, H1, tracking=-0.04)


def card(x, y, w, h, fill='#FFFFFF', r=36, stroke=None):
    s = f' stroke="{stroke}" stroke-width="2"' if stroke else ''
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}"{s}/>'


pages = []

# 1 cover
b = [f'<rect width="{W}" height="{H}" fill="{Y}"/>',
     pill(180, 160, 360, 150, P), pill(1760, 930, 380, 160, L), pill(1700, 170, 140, 60, C), pill(250, 930, 160, 66, L)]
lh = 300
b.append(logo_g(W / 2 - logo_w(lh) / 2, 330, lh, C, L))
b.append(T('Manual de marca', W / 2, 760, 48, C, SUB, 'middle', -0.02))
b.append(T('Versión 1  ·  Noviembre 2026', W / 2, 820, 24, '#B9C7BF', BODYM, 'middle'))
pages.append(svg_doc(W, H, ''.join(b)))

# 2 la marca
b = [title('Qué es Komprá')]
t, _ = PAR('Komprá es una tienda online paraguaya de todo un poco: tecnología, hogar, cocina, belleza y mascotas, '
           'con envío a todo el país.', 96, 300, 34, 820, Y, BODYM, 1.4)
b.append(t)
t, _ = PAR('El nombre es el verbo comprar dicho como se habla acá, con voseo: komprá. La K lo convierte en marca '
           'y la tilde es su firma. Ninguna tienda grande la usa, y cualquier paraguayo la lee de una.',
           96, 470, 26, 820, MUTED, BODY, 1.5)
b.append(t)
b.append(card(1040, 150, 784, 300, Y))
b.append(T('Eslogan', 1100, 230, 22, '#B9C7BF', SEMI))
b.append(T('Komprá de todo,', 1100, 320, 52, C, H1, tracking=-0.04))
b.append(T('en un solo lugar.', 1100, 390, 52, L, H1, tracking=-0.04))
traits = [('Cercana', 'Habla de vos, como un amigo que te recomienda algo.', L),
          ('Clara', 'Dice el precio, cómo pagar y cuándo llega. Sin letra chica.', P),
          ('Con chispa', 'Un poco de humor y mucho color. Nunca grita.', L)]
for i, (n, d, c) in enumerate(traits):
    x = 96 + i * 590
    b.append(card(x, 700, 560, 230))
    b.append(pill(x + 70, 770, 60, 26, c))
    b.append(T(n, x + 120, 782, 34, Y, H2, tracking=-0.03))
    t, _ = PAR(d, x + 50, 850, 24, 470, MUTED, BODY, 1.45)
    b.append(t)
pages.append(frame(2, 'La marca', ''.join(b)))

# 3 logo principal
b = [title('Logo principal')]
b.append(card(96, 250, 1100, 560, '#FFFFFF'))
b.append(logo_g(96 + 550 - logo_w(220) / 2, 415, 220, Y, P))
b.append(card(1236, 250, 588, 560, Y))
b.append(logo_g(1236 + 294 - logo_w(110) / 2, 475, 110, C, L))
b.append(T('En fondo claro: letras Yerba, tilde Lapacho.', 96, 860, 24, Y, SEMI))
b.append(T('En fondo oscuro: letras Hueso, tilde Tereré.', 1236, 860, 24, Y, SEMI))
t, _ = PAR('Siempre en minúsculas. La tilde es un trazo dibujado a medida, con el mismo grosor que las letras e inclinado a 45°. '
           'No es la tilde de la tipografía: usá siempre los archivos de la carpeta 01 Logo.', 96, 910, 22, 1600, MUTED, BODY, 1.4)
b.append(t)
pages.append(frame(3, 'Logo', ''.join(b)))

# 4 versiones
b = [title('Versiones')]
vers = [('Una tinta Yerba', '#FFFFFF', Y, Y), ('Negro, para sellos e impresión B/N', '#FFFFFF', '#000000', '#000000'),
        ('Blanco, sobre fotos o colores fuertes', P, '#FFFFFF', '#FFFFFF')]
for i, (n, bg, lc, ac) in enumerate(vers):
    x = 96 + i * 590
    b.append(card(x, 260, 560, 300, bg, stroke='#E2DACA' if bg == '#FFFFFF' else None))
    b.append(logo_g(x + 280 - logo_w(100) / 2, 350, 100, lc, ac))
    b.append(T(n, x, 600, 22, Y, SEMI))
b.append(card(96, 650, 1150, 270, '#FFFFFF', stroke='#E2DACA'))
ss = 34
b.append(logo_g(96 + 575 - logo_w(120) / 2, 690, 120, Y, P))
b.append(T(SLOGAN, 96 + 575, 690 + 120 + 55, ss, Y, SUB, 'middle', -0.02))
b.append(T('Con eslogan: para cartelería, cierres de video y presentaciones.', 96, 960, 22, Y, SEMI))
for i, (bg, fg, ac) in enumerate([(Y, L, P), (L, Y, P), (P, Y, L)]):
    x = 1300 + i * 180
    b.append(card(x, 650, 160, 160, bg, 32))
    b.append(iso_g(x + 80, 730, 160, fg, ac))
b.append(T('Isotipo: la k con su tilde.', 1300, 870, 22, Y, SEMI))
t, _ = PAR('Para perfiles de redes, favicon e ícono de app, donde el nombre completo no se lee.', 1300, 910, 20, 520, MUTED, BODY, 1.4)
b.append(t)
pages.append(frame(4, 'Logo', ''.join(b)))

# 5 area de respeto
b = [title('Espacio y tamaño mínimo')]
b.append(card(96, 260, 1100, 700, '#FFFFFF'))
lh = 180
lw = logo_w(lh)
s = lh / WM[2][3]
xh = 590 * s  # x-height of the logo at this size
lx, ly = 96 + 550 - lw / 2, 610 - lh / 2
b.append(f'<rect x="{lx - xh:.1f}" y="{ly - xh:.1f}" width="{lw + 2*xh:.1f}" height="{lh + 2*xh:.1f}" fill="none" stroke="{P}" stroke-width="3" stroke-dasharray="14 10"/>')
b.append(f'<rect x="{lx:.1f}" y="{ly:.1f}" width="{lw:.1f}" height="{lh:.1f}" fill="{A}"/>')
b.append(logo_g(lx, ly, lh, Y, P))
b.append(f'<rect x="{lx - xh:.1f}" y="{ly + lh/2 - 20:.1f}" width="{xh:.1f}" height="40" fill="{P}" opacity="0.25"/>')
b.append(T('x', lx - xh / 2, ly + lh / 2 + 12, 32, Y, H2, 'middle'))
b.append(T('x = alto de la letra o', 96 + 550, 920, 22, MUTED, SEMI, 'middle'))
rows = [('Espacio libre', 'Alrededor del logo dejá como mínimo el alto de una "o" sin textos ni otros elementos.'),
        ('Mínimo en pantalla', 'Logo: 90 px de ancho. Isotipo: 24 px.'),
        ('Mínimo impreso', 'Logo: 25 mm de ancho. Isotipo: 8 mm.')]
for i, (n, d) in enumerate(rows):
    y = 300 + i * 210
    b.append(T(n, 1260, y, 30, Y, H2, tracking=-0.03))
    t, _ = PAR(d, 1260, y + 50, 24, 560, MUTED, BODY, 1.45)
    b.append(t)
pages.append(frame(5, 'Logo', ''.join(b)))

# 6 usos incorrectos
b = [title('Lo que no se hace')]
d, acc, (bx, by, bw, bh) = WM


def mini(x, y, w, h, inner, label):
    out = card(x, y, w, h, '#FFFFFF', 28, '#E2DACA') + inner
    out += f'<circle cx="{x + w - 40}" cy="{y + 40}" r="22" fill="{RED}"/>'
    out += f'<path d="M{x + w - 50},{y + 30} l20,20 M{x + w - 30},{y + 30} l-20,20" stroke="#FFFFFF" stroke-width="5" stroke-linecap="round"/>'
    out += T(label, x, y + h + 40, 22, Y, SEMI)
    return out


def lg(cx, cy, hgt, lc, ac, extra=''):
    s = hgt / bh
    x0 = cx - bw * s / 2
    y0 = cy - hgt / 2
    return (f'<g transform="translate({x0 - bx*s:.1f},{y0 - by*s:.1f}) scale({s:.5f})" {extra}>'
            f'<path d="{d}" fill="{lc}"/><path d="{acc}" fill="{ac}"/></g>')


cw, ch = 540, 270
cells = []
cx0 = [96, 96 + 590, 96 + 1180]
cy0 = [260, 640]
# 1 stretched
cells.append(mini(cx0[0], cy0[0], cw, ch,
                  f'<g transform="translate({cx0[0] + cw/2},{cy0[0] + ch/2}) scale(1.35,0.75) translate({-(cx0[0] + cw/2)},{-(cy0[0] + ch/2)})">'
                  + lg(cx0[0] + cw / 2, cy0[0] + ch / 2, 70, Y, P) + '</g>', 'Deformarlo'))
# 2 other colors
cells.append(mini(cx0[1], cy0[0], cw, ch, lg(cx0[1] + cw / 2, cy0[0] + ch / 2, 70, '#1D4ED8', '#F97316'), 'Cambiar los colores'))
# 3 rotated
cells.append(mini(cx0[2], cy0[0], cw, ch, f'<g transform="rotate(-12 {cx0[2] + cw/2} {cy0[0] + ch/2})">'
                  + lg(cx0[2] + cw / 2, cy0[0] + ch / 2, 70, Y, P) + '</g>', 'Rotarlo'))
# 4 typed with the font accent
dd, wdt = text_path('komprá', ('unb', 800), 70)
cells.append(mini(cx0[0], cy0[1], cw, ch, f'<g transform="translate({cx0[0] + cw/2 - wdt/2},{cy0[1] + ch/2 + 26})"><path d="{dd}" fill="{Y}"/></g>',
                  'Escribirlo con la tipografía'))
# 5 low contrast
cells.append(mini(cx0[1], cy0[1], cw, ch, f'<rect x="{cx0[1]+2}" y="{cy0[1]+2}" width="{cw-4}" height="{ch-4}" rx="27" fill="{C}"/>'
                  + lg(cx0[1] + cw / 2, cy0[1] + ch / 2, 70, L, P), 'Usarlo con poco contraste'))
# 6 effects
cells.append(mini(cx0[2], cy0[1], cw, ch,
                  lg(cx0[2] + cw / 2 + 8, cy0[1] + ch / 2 + 8, 70, '#00000055', '#00000055')
                  + lg(cx0[2] + cw / 2, cy0[1] + ch / 2, 70, L, P, f'stroke="{Y}" stroke-width="40"'), 'Agregarle sombras o bordes'))
b += cells
pages.append(frame(6, 'Logo', ''.join(b)))

# 7 colores
b = [title('Colores')]
sw = (W - 192 - 4 * 30) / 5
for i, (n, h, use) in enumerate(COLORS):
    x = 96 + i * (sw + 30)
    b.append(card(x, 260, sw, 340, h, 32, '#E2DACA'))
    b.append(T(n, x, 660, 34, Y, H2, tracking=-0.03))
    b.append(T(h, x, 705, 22, Y, SEMI))
    b.append(T('RGB ' + ' '.join(map(str, rgb(h))), x, 740, 20, MUTED, BODY))
    b.append(T('CMYK ' + ' '.join(map(str, cmyk(h))), x, 772, 20, MUTED, BODY))
    t, _ = PAR(use, x, 815, 20, sw - 10, MUTED, BODY, 1.4)
    b.append(t)
b.append(T('Proporción', 96, 905, 22, Y, SEMI))
x = 260
for frac, col in [(0.5, C), (0.3, Y), (0.15, L), (0.05, P)]:
    wpx = frac * 1560
    b.append(f'<rect x="{x:.1f}" y="879" width="{wpx:.1f}" height="40" fill="{col}" stroke="#E2DACA" stroke-width="1"/>')
    x += wpx
b.append(T('50 % Hueso/Arena · 30 % Yerba · 15 % Tereré · 5 % Lapacho. CMYK aproximado: pedí prueba de color a la imprenta.', 260, 955, 18, MUTED, BODY))
pages.append(frame(7, 'Color', ''.join(b)))

# 8 tipografia
b = [title('Tipografía')]
b.append(card(96, 260, 840, 700, '#FFFFFF'))
b.append(T('Unbounded', 146, 340, 30, MUTED, SEMI))
b.append(T('Aa', 146, 560, 210, Y, ('unb', 800), tracking=-0.05))
t, _ = PAR('Títulos, precios, botones y stickers. Pesos SemiBold a Black. Siempre con el interletrado un poco cerrado.', 146, 660, 24, 720, MUTED, BODY, 1.45)
b.append(t)
b.append(T('Gs. 420.000', 146, 880, 64, Y, ('unb', 800), tracking=-0.04))
b.append(card(984, 260, 840, 700, '#FFFFFF'))
b.append(T('Instrument Sans', 1034, 340, 30, MUTED, SEMI))
b.append(T('Aa', 1034, 560, 210, Y, ('ins', 600), tracking=-0.03))
t, _ = PAR('Textos, descripciones y datos. Pesos Regular a Bold. Cómoda de leer en el celular.', 1034, 660, 24, 720, MUTED, BODY, 1.45)
b.append(t)
t, _ = PAR('Todo lo que necesitás para tu casa y tu día, con envío a todo el país.', 1034, 820, 30, 720, Y, BODY, 1.4)
b.append(t)
pages.append(frame(8, 'Tipografía', ''.join(b)))

# 9 recursos graficos
b = [title('La tilde como recurso')]
b.append(card(96, 260, 860, 700, Y))
for (cx, cy, ln, th, col) in [(330, 470, 300, 120, P), (620, 400, 160, 64, L), (760, 640, 260, 104, L), (360, 760, 120, 50, C)]:
    b.append(pill(cx, cy, ln, th, col))
t, _ = PAR('La tilde del logo sale a jugar: como barritas de fondo, como viñeta y como subrayado. '
           'Siempre a 45° y con las puntas redondas.', 146, 900, 22, 780, '#B9C7BF', BODY, 1.4)
b.append(t)
b.append(card(1000, 260, 824, 330, '#FFFFFF'))
b.append(T('Stickers', 1050, 330, 30, Y, H2, tracking=-0.03))
b.append(sticker(1210, 430, 'Pagás al recibir', 24, L, Y, -5))
b.append(sticker(1560, 420, 'Nuevo', 24, P, Y, 4))
b.append(sticker(1290, 525, 'Lo más komprado', 24, Y, L, -2))
b.append(sticker(1640, 520, 'Para el tereré', 24, L, Y, 5))
b.append(card(1000, 630, 824, 330, '#FFFFFF'))
b.append(T('Fotos de producto', 1050, 700, 30, Y, H2, tracking=-0.03))
b.append(f'<g transform="rotate(-6 1180 840)"><rect x="1090" y="750" width="180" height="180" rx="30" fill="{A}"/></g>')
b.append(icon('freidora', 1180, 840, 100, '#8A9A91', 1.2))
t, _ = PAR('Producto recortado, centrado y sobre fondo Arena. Nunca la foto de WhatsApp del proveedor con textos encima. '
           'Así el catálogo se ve como una tienda grande.', 1320, 770, 22, 460, MUTED, BODY, 1.45)
b.append(t)
pages.append(frame(9, 'Recursos gráficos', ''.join(b)))

# 10 tono de voz
b = [title('Cómo hablamos')]
rules = [('De vos, siempre', '"Komprá", "pagá", "elegí". Como se habla acá.'),
         ('Claro y corto', 'Precio, forma de pago y cuándo llega, sin vueltas.'),
         ('Sin gritar', 'Nada de MAYÚSCULAS sostenidas ni "!!!". Emojis, pocos.')]
for i, (n, dsc) in enumerate(rules):
    y = 300 + i * 140
    b.append(pill(130, y - 10, 50, 22, P if i % 2 else L))
    b.append(T(n, 180, y, 30, Y, H2, tracking=-0.03))
    b.append(T(dsc, 180, y + 44, 22, MUTED, BODY))
b.append(card(800, 240, 1024, 600, '#FFFFFF'))
b.append(T('DECIMOS', 850, 310, 18, MUTED, BOLD, tracking=0.08))
b.append(T('EN VEZ DE', 1380, 310, 18, MUTED, BOLD, tracking=0.08))
pairs = [('Lo quiero', 'Agregar al carrito'),
         ('¡Listo! Ya está en camino. Te avisamos por WhatsApp.', 'Su pedido ha sido procesado exitosamente.'),
         ('Se agotó (todos lo kompraron). Avisame cuando vuelva.', 'Producto sin stock.'),
         ('Tu carrito está más vacío que la heladera un domingo.', 'No hay productos en el carrito.')]
y = 370
for a, c in pairs:
    ta, ha = PAR(a, 850, y, 24, 480, Y, SEMI, 1.35)
    tc, hc = PAR(c, 1380, y, 24, 400, MUTED, BODY, 1.35)
    b += [ta, tc]
    y += max(ha, hc) + 30
    b.append(f'<rect x="850" y="{y - 40}" width="924" height="1" fill="#E2DACA"/>')
pages.append(frame(10, 'Tono de voz', ''.join(b)))

# 11 aplicaciones
R = KIT + '03 Redes/'
b = [title('Aplicaciones')]
b.append(img(R + 'portada-facebook-1640x624.png', 96, 260, 1100, 418, 'preserveAspectRatio="xMidYMid slice"'))
b.append(T('Portada de Facebook', 96, 720, 22, Y, SEMI))
b.append(f'<clipPath id="circ"><circle cx="1400" cy="400" r="140"/></clipPath>')
b.append(img(R + 'perfil-instagram-facebook-whatsapp-1080.png', 1260, 260, 280, 280, 'clip-path="url(#circ)"'))
b.append(T('Perfil', 1400, 590, 22, Y, SEMI, 'middle'))
b.append(img(R + 'plantillas/story-1080x1920-ejemplo.png', 1600, 260, 224, 398))
b.append(T('Story', 1600, 700, 22, Y, SEMI))
b.append(img(R + 'plantillas/post-1080-ejemplo.png', 96, 750, 200, 200))
for i, n in enumerate(['como-komprar', 'envios', 'novedades', 'opiniones', 'ofertas']):
    b.append(f'<clipPath id="h{i}"><circle cx="{400 + i * 150}" cy="850" r="60"/></clipPath>')
    b.append(img(R + f'destacadas/destacada-{n}.png', 400 + i * 150 - 60, 850 - 107, 120, 213, f'clip-path="url(#h{i})"'))
b.append(T('Post y portadas de historias destacadas', 340, 950, 22, Y, SEMI))
pages.append(frame(11, 'Aplicaciones', ''.join(b)))

# 12 back cover
b = [f'<rect width="{W}" height="{H}" fill="{Y}"/>', pill(1640, 220, 300, 120, P), pill(260, 860, 260, 104, L)]
b.append(logo_g(W / 2 - logo_w(200) / 2, 380, 200, C, L))
b.append(T(SLOGAN, W / 2, 680, 40, C, SUB, 'middle', -0.02))
pages.append(svg_doc(W, H, ''.join(b)))

if __name__ == '__main__':
    writer = PdfWriter()
    for i, svg in enumerate(pages):
        pdf = cairosvg.svg2pdf(bytestring=svg.encode())
        writer.append(PdfReader(io.BytesIO(pdf)))
        if '--png' in sys.argv:
            cairosvg.svg2png(bytestring=svg.encode(), write_to=f'/tmp/page{i+1:02d}.png', output_width=960)
    with open(KIT + 'Manual de marca Komprá.pdf', 'wb') as f:
        writer.write(f)
    print('pages', len(pages))
