"""Generate Warmth app icon — orange cat head in multiple sizes, pack into ICO + PNG.

Pure Pillow ImageDraw rendering, no external dependencies beyond Pillow.
"""

from PIL import Image, ImageDraw, ImageFilter
import math
import os
import struct
import io

# ── Color palette ──────────────────────────────────────────────
CAT_BODY   = (0xf5, 0xb8, 0x78)   # warm orange face/ears
INNER_EAR  = (0xf0, 0xa0, 0xa0)   # pink inner ear
EYE_COLOR  = (0x1a, 0x08, 0x04)   # dark brown-black
EYE_SHINE  = (255, 255, 255)       # white highlight
BLUSH      = (0xff, 0xb0, 0xa0)    # soft pink blush
NOSE       = (0xe0, 0x90, 0x80)    # warm pink nose
MOUTH      = (0xd4, 0xa0, 0x80)    # light brown mouth
WHISKER    = (0xe8, 0xb8, 0x98)    # pale whisker
SHADOW     = (0, 0, 0, 64)         # drop shadow (RGBA for separate pass)

SIZES = [16, 24, 32, 48, 64, 128, 256]


def scale(v, size):
    """Scale a value from the 256×256 design space to the target size."""
    return v * size / 256.0


def draw_cat(draw, im, size):
    """Draw the complete cat icon at the given size using ImageDraw."""

    # ── Helper scale ──
    s = lambda v: scale(v, size)

    # ── Shadow (draw slightly offset, then blur if possible) ──
    shadow_im = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    shadow_draw = ImageDraw.Draw(shadow_im)
    r = s(58)
    ox, oy = s(0), s(3)  # shadow offset
    shadow_draw.ellipse(
        [s(128) - r + ox, s(132) - r + oy,
         s(128) + r + ox, s(132) + r + oy],
        fill=(0, 0, 0, 60)
    )
    # Blur shadow
    if size >= 32:
        blur_r = max(1, int(s(4)))
        shadow_im = shadow_im.filter(ImageFilter.GaussianBlur(blur_r))
    im.alpha_composite(shadow_im)

    # ── Ears ──
    # Left ear (rounded triangle)
    ear_left = [
        (s(74),  s(118)),
        (s(66),  s(80)),
        (s(80),  s(58)),
        (s(88),  s(48)),
        (s(98),  s(54)),
        (s(106), s(58)),
        (s(110), s(82)),
        (s(110), s(118)),
    ]
    draw.polygon(ear_left, fill=CAT_BODY)

    # Right ear
    ear_right = [
        (s(182), s(118)),
        (s(190), s(80)),
        (s(176), s(58)),
        (s(168), s(48)),
        (s(158), s(54)),
        (s(150), s(58)),
        (s(146), s(82)),
        (s(146), s(118)),
    ]
    draw.polygon(ear_right, fill=CAT_BODY)

    # Inner ears
    inner_left = [
        (s(80),  s(110)),
        (s(76),  s(82)),
        (s(86),  s(66)),
        (s(92),  s(58)),
        (s(96),  s(62)),
        (s(100), s(66)),
        (s(102), s(84)),
    ]
    draw.polygon(inner_left, fill=INNER_EAR)

    inner_right = [
        (s(176), s(110)),
        (s(180), s(82)),
        (s(170), s(66)),
        (s(164), s(58)),
        (s(160), s(62)),
        (s(156), s(66)),
        (s(154), s(84)),
    ]
    draw.polygon(inner_right, fill=INNER_EAR)

    # ── Head ──
    r = s(58)
    cx, cy = s(128), s(132)
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=CAT_BODY)

    # ── Eyes ──
    eye_r = s(10.5)
    draw.ellipse([s(104)-eye_r, s(128)-eye_r, s(104)+eye_r, s(128)+eye_r], fill=EYE_COLOR)
    draw.ellipse([s(152)-eye_r, s(128)-eye_r, s(152)+eye_r, s(128)+eye_r], fill=EYE_COLOR)

    # Eye highlights
    shine_r = s(4.2)
    draw.ellipse([s(101)-shine_r, s(123)-shine_r, s(101)+shine_r, s(123)+shine_r], fill=EYE_SHINE)
    draw.ellipse([s(149)-shine_r, s(123)-shine_r, s(149)+shine_r, s(123)+shine_r], fill=EYE_SHINE)

    # ── Blush ──
    blush_r = s(9)
    draw.ellipse([s(86)-blush_r, s(144)-blush_r, s(86)+blush_r, s(144)+blush_r], fill=BLUSH)
    draw.ellipse([s(170)-blush_r, s(144)-blush_r, s(170)+blush_r, s(144)+blush_r], fill=BLUSH)

    # ── Nose ──
    nrx, nry = s(5), s(3.5)
    draw.ellipse([s(128)-nrx, s(150)-nry, s(128)+nrx, s(150)+nry], fill=NOSE)

    # ── Mouth (W shape) ──
    lw = max(1, int(s(2)))
    # Center vertical
    draw.line([(s(128), s(153.5)), (s(128), s(160))], fill=MOUTH, width=lw)
    # Left arc
    draw.arc([s(114), s(156), s(128), s(166)], start=180, end=270, fill=MOUTH, width=lw)
    # Right arc
    draw.arc([s(128), s(156), s(142), s(166)], start=270, end=360, fill=MOUTH, width=lw)

    # ── Whiskers ──
    ww = max(1, int(s(1.8)))
    draw.line([(s(78), s(142)), (s(52), s(136))], fill=WHISKER, width=ww)
    draw.line([(s(78), s(148)), (s(50), s(150))], fill=WHISKER, width=ww)
    draw.line([(s(178), s(142)), (s(204), s(136))], fill=WHISKER, width=ww)
    draw.line([(s(178), s(148)), (s(206), s(150))], fill=WHISKER, width=ww)


def make_icon_frame(size):
    """Create a single RGBA frame of the icon at the given size."""
    im = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(im)
    draw_cat(draw, im, size)
    return im


def save_multi_ico(frames_dict, path):
    """Save a dict of {size: Image} as a multi-resolution ICO file.

    Uses raw binary ICO format (header + directory entries + PNG data).
    """
    ordered = sorted(frames_dict.items(), key=lambda x: -x[0])

    # Convert each frame to PNG bytes in memory
    png_data_list = []
    for sz, img in ordered:
        buf = io.BytesIO()
        img.convert('RGBA').save(buf, format='PNG')
        png_data_list.append((sz, buf.getvalue()))

    # Build ICO
    count = len(png_data_list)
    # Header: reserved(2) + type(2) + count(2)
    header = struct.pack('<HHH', 0, 1, count)

    # Directory entries
    dir_entries = b''
    offset = 6 + 16 * count  # data starts after header + all dir entries
    img_datas = b''
    for sz, data in png_data_list:
        w = sz if sz < 256 else 0
        h = sz if sz < 256 else 0
        size = len(data)
        entry = struct.pack('<BBBBHHII',
            w,      # width (0 = 256)
            h,      # height (0 = 256)
            0,      # color palette count
            0,      # reserved
            1,      # color planes
            32,     # bits per pixel
            size,   # image data size
            offset  # offset from start of file
        )
        dir_entries += entry
        img_datas += data
        offset += size

    with open(path, 'wb') as f:
        f.write(header)
        f.write(dir_entries)
        f.write(img_datas)


def main():
    project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.chdir(project_dir)

    print("Generating Warmth icon...")
    print(f"  Target sizes: {SIZES}")

    # Generate all frames
    frames = {}
    for sz in SIZES:
        frames[sz] = make_icon_frame(sz)
        print(f"    {sz}x{sz} OK")

    # Save 256x256 PNG
    png_path = os.path.join(project_dir, 'icon.png')
    frames[256].save(png_path, format='PNG')
    print(f"  Saved: icon.png")

    # Save multi-resolution ICO
    ico_path = os.path.join(project_dir, 'icon.ico')
    save_multi_ico(frames, ico_path)
    print(f"  Saved: icon.ico")

    # Verify
    ico_size = os.path.getsize(ico_path)
    png_size = os.path.getsize(png_path)
    print(f"\nDone! icon.ico: {ico_size:,} bytes, icon.png: {png_size:,} bytes")


if __name__ == '__main__':
    main()
