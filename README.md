# Komprá

**Komprá de todo, en un solo lugar.**

Marca y diseño de Komprá, tienda online multiproducto para Paraguay.

## Qué hay en este repo

| Carpeta | Contenido |
|---|---|
| `kit-de-marca/` | El kit de marca listo para usar: logos (SVG y PNG), isotipo y favicon, piezas para redes, paleta de colores, tipografías y el **Manual de marca** en PDF. Empezá por `LEEME.txt`. |
| `diseno/` | El diseño de la marca y la tienda: hoja de marca, aplicaciones, perfil y portada de redes, home, página de producto y checkout. Son los archivos del lienzo de diseño (`canvas.json` + un `.dc.html` por pantalla). |
| `herramientas/` | Los scripts que generan el kit. El logo está dibujado con los contornos reales de la tipografía y la tilde está hecha a medida, así que cualquier cambio se regenera desde acá. |

## Marca en 30 segundos

- **Nombre:** komprá, el verbo comprar con voseo. La K lo convierte en marca y la tilde es su firma.
- **Logo:** siempre en minúsculas. La tilde está dibujada a medida, a 45° y con puntas redondas. **Nunca escribas el logo con la fuente:** usá los archivos de `kit-de-marca/01 Logo`.
- **Colores:**

| Nombre | HEX | Uso |
|---|---|---|
| Yerba | `#0E2A1F` | Fondos fuertes, textos, botones |
| Tereré | `#C8F03C` | Acento principal, botones, stickers |
| Lapacho | `#FF5FA2` | Segundo acento, promos, la tilde sobre fondo claro |
| Hueso | `#F6F1E7` | Fondo general |
| Arena | `#ECE5D5` | Fondo de las fotos de producto |

- **Tipografías:** Unbounded para títulos, precios y botones; Instrument Sans para textos. Las dos son gratuitas (SIL Open Font License).
- **Tono:** de vos, claro y sin gritar. Por ejemplo, "Lo quiero" en vez de "Agregar al carrito".

## Regenerar el kit

```bash
cd herramientas
npm install                 # tipografías (Fontsource)
pip install -r requirements.txt
python kit_assets.py        # logos, isotipos, redes, colores y tipografías
python manual.py            # Manual de marca en PDF
```

Los archivos se escriben en `kit-de-marca/`. Los parámetros de la tilde (ángulo, largo, grosor y separación) están en `PILL`, dentro de `herramientas/logo.py`.
