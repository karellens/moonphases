#!/usr/bin/env python
import os
from PIL import Image, ImageDraw, ImageFilter
import math


MOON_DIMMING = (0, 0, 0, 200)
RADIUS_BLUR = 3


def draw_moon(phase, offset_x, offset_y, width, height, moon_file, moon_dimming=MOON_DIMMING, radius_blur=RADIUS_BLUR):
    cur_dir = os.path.dirname(__file__)
    sin = math.sin(phase)
    cos = math.cos(phase)
    radius_x = width / 2

    im = Image.open(moon_file)

    mask_circle = Image.new('L', im.size, color=0)
    mask_phase = Image.new('RGBA', im.size, color=0)
    draw_circle = ImageDraw.Draw(mask_circle)
    draw_phase = ImageDraw.Draw(mask_phase)

    # full circle
    draw_circle.ellipse((offset_x, offset_y, offset_x + width, offset_y + height), fill=255, outline=255)

    # overlap phase (1q - left, 2q - left, 3q - right, 2q - right,)
    draw_phase.rectangle((
        (0 if sin > 0 else offset_x + radius_x, 0),
        (offset_x + radius_x if sin > 0 else im.size[0], im.size[1])),
     fill=moon_dimming, outline=moon_dimming)
    # overlap phase ellipse (1q - black, 2q - white, 3q - white, 2q - black,)
    draw_phase.ellipse((
            ((offset_x + radius_x) - (radius_x * abs(cos))),
            offset_y - radius_blur,
            offset_x + radius_x + (radius_x * abs(cos)),
            offset_y + height + radius_blur
        ),
     fill=moon_dimming if cos > 0 else 255, outline=moon_dimming if cos > 0 else 255)
    mask_phase = mask_phase.filter(ImageFilter.GaussianBlur(radius=radius_blur))

    im = Image.alpha_composite(im, mask_phase)
    im.putalpha(mask_circle)

    # mask_circle.show()
    # mask_phase.show()
    # im.show()
    im.save(os.path.join(cur_dir, 'output.png'))


if __name__ == '__main__':
    import moon

    m = moon.MoonPhase()

    draw_moon(math.radians(m.angle), 2, 2, 397, 397, os.path.join(os.path.dirname(__file__), 'full_moon.png'))
