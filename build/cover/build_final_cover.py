#!/usr/bin/env python3
"""Build the "Stas' Python Cookbook" book cover into <repo>/images/.

The central art (a cast-iron pot "cooking up" glowing code, with the title
engraved into the pot) lives in sources/pot-cover-art.png (1536x1024, landscape).
It is composited into a portrait US-Letter canvas (8.5:11) with dark bands top
and bottom, and the title / subtitle / author are overlaid as crisp vector text
(so text stays sharp and is never at the mercy of the raster art).

Outputs:
  - Python-Cookbook-book-cover-1536x1988.png : full-resolution flat cover
  - Python-Cookbook-book-cover.png           : optimized display image
  - Python-Cookbook-book-cover-<wxh>.png     : small thumbnail (size in name)
  - Python-Cookbook-book-cover.pdf           : vector PDF at US Letter size
                                               (612x792pt, 8.5x11in)
  - Python-Cookbook-book-cover.svg           : editable master SVG

Requires: rsvg-convert (librsvg) + ImageMagick (magick). zopflipng optional
(used to further shrink the PNGs when present).
"""
import base64
import pathlib
import shutil
import subprocess
import tempfile

HERE = pathlib.Path(__file__).parent
IMAGES = HERE.parent.parent / "images"   # <repo>/images
ART = HERE / "sources" / "pot-cover-art.png"
STEM = "Python-Cookbook-book-cover"

# --- canvas / layout geometry -------------------------------------------------
W, H = 1536, 1988          # US Letter aspect (8.5:11) portrait cover
ARTW, ARTH = 1536, 1024    # landscape art band placed inside the portrait
ART_Y = 582                # y where the art band begins (balanced: 4 equal ~150px gaps)
CX = W // 2
FONT = "Avenir Next, Helvetica Neue, Arial"
DARK = "#04060c"           # near-black matching the art's edges

DEFS = """  <defs>
    <linearGradient id="titleGrad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#ffe1a3"/>
      <stop offset="1" stop-color="#f0b347"/>
    </linearGradient>
  </defs>"""

# Each text section: label -> inner SVG markup on the full WxH canvas.
LAYERS = {
    "title-line-1": (
        f'<text x="{CX}" y="241" text-anchor="middle" font-family="{FONT}" '
        f'font-weight="600" font-size="120" fill="#f6c879" letter-spacing="2">Stas\u2019 Python</text>'
    ),
    "title-line-2": (
        f'<text x="{CX}" y="427" text-anchor="middle" font-family="{FONT}" '
        f'font-weight="800" font-size="196" fill="url(#titleGrad)" letter-spacing="1">Cookbook</text>'
    ),
    "author": (
        f'<text x="{CX}" y="1817" text-anchor="middle" font-family="{FONT}" '
        f'font-weight="500" font-size="80" fill="#ededed" letter-spacing="17">by Stas Bekman</text>'
    ),
}


def run(*args):
    subprocess.run([str(a) for a in args], check=True)


def b64(path: pathlib.Path) -> str:
    return base64.b64encode(path.read_bytes()).decode("ascii")


def svg_open() -> str:
    return (
        '<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n'
        '<svg xmlns="http://www.w3.org/2000/svg" '
        'xmlns:xlink="http://www.w3.org/1999/xlink" '
        'xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape" '
        f'width="{W}" height="{H}" viewBox="0 0 {W} {H}">\n{DEFS}\n'
    )


def bg_layer_markup() -> str:
    """Solid dark canvas + the landscape art band placed inside it."""
    return (
        f'<rect x="0" y="0" width="{W}" height="{H}" fill="{DARK}"/>\n'
        f'    <image x="0" y="{ART_Y}" width="{ARTW}" height="{ARTH}" '
        f'xlink:href="data:image/png;base64,{b64(ART)}"/>'
    )


def write_master_svg() -> pathlib.Path:
    parts = [svg_open()]
    parts.append(
        '  <g inkscape:groupmode="layer" inkscape:label="background">\n'
        f'    {bg_layer_markup()}\n  </g>\n'
    )
    for label, inner in LAYERS.items():
        parts.append(
            f'  <g inkscape:groupmode="layer" inkscape:label="{label}">\n'
            f'    {inner}\n  </g>\n'
        )
    parts.append("</svg>\n")
    out = IMAGES / f"{STEM}.svg"
    out.write_text("".join(parts))
    return out


def render_png(svg_path: pathlib.Path, out_png: pathlib.Path):
    run("rsvg-convert", "-o", out_png, svg_path)


# US Letter page in px so rsvg-convert (96dpi: 1px=0.75pt) yields 612x792pt.
LETTER_W, LETTER_H = 816, 1056   # -> 612 x 792 pt (8.5 x 11 in)


def letter_pdf(svg_path: pathlib.Path, out_pdf: pathlib.Path):
    run("rsvg-convert", "-f", "pdf", "-w", LETTER_W, "-h", LETTER_H,
        "-o", out_pdf, svg_path)


def optimize_small(full_png: pathlib.Path, out_png: pathlib.Path, box: str):
    """Resize within `box` (WxH, aspect preserved) + strip + zopfli-optimize."""
    with tempfile.TemporaryDirectory() as d:
        tmp = pathlib.Path(d) / "small.png"
        run("magick", full_png, "-resize", box, "-strip", tmp)
        if out_png.exists():
            out_png.unlink()
        if shutil.which("zopflipng"):
            run("zopflipng", "-y", tmp, out_png)
        else:
            shutil.copy(tmp, out_png)


def main():
    if not ART.exists():
        raise SystemExit(f"missing cover art: {ART}")
    IMAGES.mkdir(exist_ok=True)
    for stale in IMAGES.glob(f"{STEM}-*x*.png"):
        stale.unlink()

    svg = write_master_svg()
    png_full = IMAGES / f"{STEM}-{W}x{H}.png"
    render_png(svg, png_full)
    pdf = IMAGES / f"{STEM}.pdf"
    letter_pdf(svg, pdf)

    png_small = IMAGES / f"{STEM}.png"
    optimize_small(png_full, png_small, "548x754")

    thumb_tmp = IMAGES / f"{STEM}-thumb.png"
    optimize_small(png_full, thumb_tmp, "200x300")
    dims = subprocess.check_output(
        ["magick", "identify", "-format", "%wx%h", str(thumb_tmp)]
    ).decode().strip()
    png_thumb = IMAGES / f"{STEM}-{dims}.png"
    if png_thumb.exists():
        png_thumb.unlink()
    thumb_tmp.rename(png_thumb)

    for p in (png_small, png_thumb, png_full, pdf, svg):
        print(f"wrote images/{p.name} ({p.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
