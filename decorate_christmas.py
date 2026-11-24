# -*- coding: utf-8 -*-
"""為兩張明信片圖片加入聖誕節氣氛：飄雪、吊飾球、聖誕燈串、金色節慶邊框。
第二張圖片左上角有 QR code，該區域會被避開。"""
import math
import random
from PIL import Image, ImageDraw, ImageFilter, ImageFont

SRC_1 = "postcard.jpg"
SRC_2 = "image_with_qr.jpg"
OUT_1 = "postcard_christmas.jpg"
OUT_2 = "image_with_qr_christmas.jpg"

# QR code 保護區域 (x0, y0, x1, y1)，留安全邊距
QR_SAFE = (0, 0, 200, 200)

BULB_COLORS = [
    (255, 60, 60),    # 紅
    (60, 220, 90),    # 綠
    (255, 200, 40),   # 金
    (90, 150, 255),   # 藍
    (255, 120, 200),  # 粉
]


def in_qr(x, y, rect):
    if rect is None:
        return False
    x0, y0, x1, y1 = rect
    return x0 <= x <= x1 and y0 <= y <= y1


def add_garland_lights(img, rect, rng):
    """頂端垂掛的聖誕燈串與裝飾球。"""
    w, h = img.size
    overlay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)

    # 燈串的垂墜曲線（多段弧線）
    span = 160  # 每段燈串寬度
    n_seg = max(3, w // span + 1)
    step = w / n_seg
    pts = []
    for i in range(n_seg + 1):
        x = i * step
        # 頂端起點與下垂中點
        pts.append((x, 26))

    # 畫連接線（用平滑拋物線取樣）
    wire = []
    for i in range(n_seg):
        x0, y0 = pts[i]
        x1, y1 = pts[i + 1]
        mid_x = (x0 + x1) / 2
        for t in [k / 12 for k in range(13)]:
            x = (1 - t) ** 2 * x0 + 2 * (1 - t) * t * mid_x + t ** 2 * x1
            y = (1 - t) ** 2 * y0 + 2 * (1 - t) * t * (y0 + 58) + t ** 2 * y1
            wire.append((x, y))
    if len(wire) > 1:
        d.line(wire, fill=(40, 90, 50, 235), width=4)

    # 沿線掛燈泡
    for idx in range(0, len(wire), 7):
        x, y = wire[idx]
        if in_qr(x, y, rect):
            continue
        col = BULB_COLORS[(idx // 7) % len(BULB_COLORS)]
        # 燈座
        d.line([(x, y), (x, y + 8)], fill=(30, 60, 35, 255), width=3)
        # 光暈
        glow = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        gd = ImageDraw.Draw(glow)
        r = 13
        gd.ellipse([x - r, y + 4 - r, x + r, y + 4 + r], fill=col + (110,))
        glow = glow.filter(ImageFilter.GaussianBlur(6))
        overlay.alpha_composite(glow)
        d = ImageDraw.Draw(overlay)
        # 燈泡本體
        d.ellipse([x - 6, y + 4 - 6, x + 6, y + 4 + 6], fill=col + (255,),
                  outline=(255, 255, 255, 200), width=1)
        # 高光
        d.ellipse([x - 3, y + 1, x + 1, y + 5], fill=(255, 255, 255, 230))

    # 裝飾球（吊繩 + 彩球）
    ornament_spots = []
    for i in range(n_seg):
        # 在每段的 1/3 與 2/3 處垂掛
        for frac in (0.33, 0.72):
            cx = (i + frac) * step
            if in_qr(cx, 60, rect):
                continue
            drop = 62 + (i % 3) * 16 + int(frac * 10)
            ornament_spots.append((cx, drop, (i + int(frac * 10)) % 5))

    for cx, cy, ci in ornament_spots:
        col = BULB_COLORS[ci]
        # 吊繩
        d.line([(cx, 30), (cx, cy - 14)], fill=(230, 200, 60, 255), width=2)
        # 金屬蓋
        d.rectangle([cx - 5, cy - 18, cx + 5, cy - 12], fill=(240, 205, 70, 255))
        # 光暈
        glow = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        gd = ImageDraw.Draw(glow)
        gd.ellipse([cx - 22, cy - 22, cx + 22, cy + 22], fill=col + (80,))
        glow = glow.filter(ImageFilter.GaussianBlur(10))
        overlay.alpha_composite(glow)
        d = ImageDraw.Draw(overlay)
        # 球體
        r = 15
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=col + (255,),
                  outline=(255, 245, 210, 255), width=2)
        # 反光
        d.ellipse([cx - 8, cy - 9, cx - 1, cy - 2], fill=(255, 255, 255, 190))
        # 底部暗面
        d.arc([cx - r, cy - r, cx + r, cy + r], 20, 160,
              fill=(0, 0, 0, 90), width=3)

    img.alpha_composite(overlay)
    return img


def add_snow(img, rect, rng, count=420):
    """整幅飄雪（近景大雪模糊、遠景小雪清晰）。"""
    w, h = img.size
    # 遠景小雪
    far = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    fd = ImageDraw.Draw(far)
    for _ in range(count):
        x = rng.randint(0, w - 1)
        y = rng.randint(0, h - 1)
        if in_qr(x, y, rect):
            continue
        r = rng.randint(1, 3)
        a = rng.randint(110, 200)
        fd.ellipse([x - r, y - r, x + r, y + r], fill=(255, 255, 255, a))
    img.alpha_composite(far)

    # 近景大雪（模糊散景）
    near = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    nd = ImageDraw.Draw(near)
    for _ in range(70):
        x = rng.randint(0, w - 1)
        y = rng.randint(0, h - 1)
        if in_qr(x, y, rect):
            continue
        r = rng.randint(5, 11)
        a = rng.randint(60, 120)
        nd.ellipse([x - r, y - r, x + r, y + r], fill=(255, 255, 255, a))
    near = near.filter(ImageFilter.GaussianBlur(4))
    img.alpha_composite(near)
    return img


def add_frame(img, rect):
    """節慶金紅雙線邊框（避開 QR 側的過多裝飾，僅畫邊線）。"""
    w, h = img.size
    overlay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)
    # 外框紅
    d.rectangle([6, 6, w - 7, h - 7], outline=(170, 24, 34, 235), width=6)
    # 內框金
    d.rectangle([18, 18, w - 19, h - 19], outline=(230, 195, 70, 230), width=3)
    # 四角雪花裝飾
    corners = [(34, 34), (w - 34, 34), (34, h - 34), (w - 34, h - 34)]
    for i, (cx, cy) in enumerate(corners):
        if i == 0 and rect is not None:  # 左上角保護 QR
            continue
        draw_snowflake(d, cx, cy, 16, (255, 245, 215, 245), width=3)
    img.alpha_composite(overlay)
    return img


def draw_snowflake(d, cx, cy, r, fill, width=2):
    for k in range(6):
        ang = math.pi / 3 * k
        x = cx + r * math.cos(ang)
        y = cy + r * math.sin(ang)
        d.line([(cx, cy), (x, y)], fill=fill, width=width)
        # 分枝
        bx = cx + r * 0.6 * math.cos(ang)
        by = cy + r * 0.6 * math.sin(ang)
        for off in (-0.5, 0.5):
            ang2 = ang + off
            d.line([(bx, by), (bx + r * 0.35 * math.cos(ang2),
                               by + r * 0.35 * math.sin(ang2))],
                   fill=fill, width=max(1, width - 1))


def add_sparkles(img, rect, rng):
    """零星光芒點綴。"""
    w, h = img.size
    overlay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)
    for _ in range(26):
        x = rng.randint(30, w - 30)
        y = rng.randint(30, h - 30)
        if in_qr(x, y, rect):
            continue
        r = rng.randint(5, 12)
        a = rng.randint(120, 210)
        # 四芒星
        d.line([(x - r, y), (x + r, y)], fill=(255, 250, 220, a), width=2)
        d.line([(x, y - r), (x, y + r)], fill=(255, 250, 220, a), width=2)
        rr = max(2, r // 3)
        d.ellipse([x - rr, y - rr, x + rr, y + rr], fill=(255, 255, 240, a))
    overlay = overlay.filter(ImageFilter.GaussianBlur(0.6))
    img.alpha_composite(overlay)
    return img


def process(src, dst, rect, seed):
    rng = random.Random(seed)
    base = Image.open(src).convert("RGBA")
    base = add_garland_lights(base, rect, rng)
    base = add_snow(base, rect, rng)
    base = add_sparkles(base, rect, rng)
    base = add_frame(base, rect)
    base.convert("RGB").save(dst, quality=92)
    print(f"OK -> {dst}  size={base.size}")


if __name__ == "__main__":
    process(SRC_1, OUT_1, None, seed=20251225)
    process(SRC_2, OUT_2, QR_SAFE, seed=20251225)
