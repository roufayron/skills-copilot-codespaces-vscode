"""Generates the decal / sign textures and Content Library icons for the
XI School Bus "Prison Police" preset.

Usage:  python3 DAZ/tools/make_textures.py
Requires Pillow (pip install pillow).
"""
import math
import os

from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.join(os.path.dirname(__file__), "..", "Vehicles", "Xivon",
                    "XI School Bus", "Prison Police")
TEX = os.path.join(ROOT, "Textures")

FONT_BOLD = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"

WHITE = (245, 245, 242, 255)
BLACK = (18, 18, 20, 255)
NAVY = (22, 34, 64, 255)
GOLD = (196, 160, 60, 255)
CLEAR = (0, 0, 0, 0)


def font(size):
    return ImageFont.truetype(FONT_BOLD, size)


def fit_font(draw, text, max_w, max_h, start=400):
    size = start
    while size > 8:
        f = font(size)
        l, t, r, b = draw.textbbox((0, 0), text, font=f)
        if r - l <= max_w and b - t <= max_h:
            return f
        size -= 2
    return font(size)


def centered_text(draw, box, text, fill, max_h=None):
    x0, y0, x1, y1 = box
    f = fit_font(draw, text, x1 - x0, max_h or (y1 - y0))
    l, t, r, b = draw.textbbox((0, 0), text, font=f)
    x = x0 + (x1 - x0 - (r - l)) / 2 - l
    y = y0 + (y1 - y0 - (b - t)) / 2 - t
    draw.text((x, y), text, font=f, fill=fill)


def sign(path, lines, size=(2048, 512), bg=WHITE, fg=BLACK, border=True):
    """Rectangular sign that replaces the yellow 'SCHOOL BUS' header sign."""
    w, h = size
    img = Image.new("RGBA", size, bg)
    d = ImageDraw.Draw(img)
    if border:
        d.rectangle([12, 12, w - 13, h - 13], outline=fg, width=18)
    pad = 60
    row_h = (h - 2 * pad) / len(lines)
    for i, line in enumerate(lines):
        y0 = pad + i * row_h
        centered_text(d, (pad, y0, w - pad, y0 + row_h), line, fg,
                      max_h=row_h * 0.8)
    img.save(path)


def lettering(path, lines, size=(4096, 1024), fg=BLACK):
    """Transparent lettering for DAZ decal nodes (sides of the bus)."""
    w, h = size
    img = Image.new("RGBA", size, CLEAR)
    d = ImageDraw.Draw(img)
    row_h = h / len(lines)
    for i, (line, scale) in enumerate(lines):
        y0 = i * row_h
        centered_text(d, (w * 0.04, y0, w * 0.96, y0 + row_h), line, fg,
                      max_h=row_h * scale)
    img.save(path)


def star_points(cx, cy, r_out, r_in, n=7):
    pts = []
    for i in range(2 * n):
        r = r_out if i % 2 == 0 else r_in
        a = math.pi * i / n - math.pi / 2
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts


def badge(path, top, bottom, size=1024):
    """Seven-point sheriff star with text, transparent background."""
    img = Image.new("RGBA", (size, size), CLEAR)
    d = ImageDraw.Draw(img)
    c = size / 2
    d.polygon(star_points(c, c, c * 0.96, c * 0.62), fill=GOLD)
    for i, (x, y) in enumerate(star_points(c, c, c * 0.96, c * 0.62)):
        if i % 2 == 0:
            d.ellipse([x - 34, y - 34, x + 34, y + 34], fill=GOLD)
    d.ellipse([c - c * 0.5, c - c * 0.5, c + c * 0.5, c + c * 0.5],
              fill=NAVY)
    d.ellipse([c - c * 0.44, c - c * 0.44, c + c * 0.44, c + c * 0.44],
              outline=GOLD, width=10)
    centered_text(d, (c - c * 0.36, c - c * 0.30, c + c * 0.36, c - c * 0.02),
                  top, GOLD)
    centered_text(d, (c - c * 0.36, c + c * 0.04, c + c * 0.36, c + c * 0.30),
                  bottom, GOLD)
    img.save(path)


def icon(path, title, subtitle, size=(256, 256)):
    """Content Library thumbnail shown next to the script."""
    w, h = size
    img = Image.new("RGBA", size, WHITE)
    d = ImageDraw.Draw(img)
    # stylised bus silhouette
    d.rounded_rectangle([18, 60, w - 18, 170], radius=18, fill=WHITE,
                        outline=BLACK, width=5)
    d.rectangle([20, 138, w - 20, 152], fill=NAVY)
    for i in range(6):
        x = 36 + i * 32
        d.rectangle([x, 76, x + 24, 112], fill=(40, 44, 52, 255))
        for bx in range(x + 6, x + 24, 6):
            d.line([bx, 76, bx, 112], fill=(150, 150, 150, 255), width=2)
    d.ellipse([46, 150, 86, 190], fill=BLACK)
    d.ellipse([w - 86, 150, w - 46, 190], fill=BLACK)
    d.rectangle([90, 50, 110, 60], fill=(200, 20, 20, 255))
    d.rectangle([w - 110, 50, w - 90, 60], fill=(20, 60, 220, 255))
    centered_text(d, (10, 196, w - 10, 226), title, BLACK)
    centered_text(d, (10, 228, w - 10, 250), subtitle, NAVY)
    img.save(path)


def main():
    os.makedirs(TEX, exist_ok=True)
    sign(os.path.join(TEX, "XI_PrisonBus_Sign_DOC.png"),
         ["DEPARTMENT OF CORRECTIONS"])
    sign(os.path.join(TEX, "XI_PrisonBus_Sign_Sheriff.png"),
         ["COUNTY SHERIFF"], bg=BLACK, fg=WHITE)
    lettering(os.path.join(TEX, "XI_PrisonBus_Side_DOC.png"),
              [("DEPARTMENT OF CORRECTIONS", 0.75),
               ("INMATE TRANSPORT", 0.6)])
    lettering(os.path.join(TEX, "XI_PrisonBus_Side_Sheriff.png"),
              [("COUNTY SHERIFF", 0.8), ("PRISONER TRANSPORT", 0.6)],
              fg=NAVY)
    lettering(os.path.join(TEX, "XI_PrisonBus_Warning.png"),
              [("DO NOT FOLLOW", 0.7), ("INMATE TRANSPORT VEHICLE", 0.5)],
              size=(2048, 512))
    badge(os.path.join(TEX, "XI_PrisonBus_Badge_Sheriff.png"),
          "COUNTY", "SHERIFF")

    icon(os.path.join(ROOT, "!XI School Bus - Prison Police.png"),
         "PRISON POLICE", "apply preset")
    icon(os.path.join(ROOT, "XI School Bus - List Surfaces.png"),
         "LIST SURFACES", "diagnostics")


if __name__ == "__main__":
    main()
