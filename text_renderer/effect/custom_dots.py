import typing
from typing import Tuple
import PIL

import numpy as np
from PIL import ImageDraw

from text_renderer.utils.bbox import BBox
from text_renderer.utils.draw_utils import transparent_img
from text_renderer.utils.types import PILImage
import math
import random

if typing.TYPE_CHECKING:
    from text_renderer.config import TextColorCfg

from .base_effect import Effect

class CustomDots(Effect):
    def __init__(
            self,
            p=0.5,
            thickness=(1, 3),
            lr_in_offset=(0, 10),
            lr_out_offset=(0, 5),
            tb_in_offset=(0, 3),
            tb_out_offset=(0, 3),
            line_pos_p=(0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1),
            dots_intensity=(10, 100),
            alpha=(110,255),
            background_color_base=True,
            color_cfg: 'TextColorCfg' = None,
        ):
        super().__init__(p)
        self.thickness = thickness
        self.lr_in_offset = lr_in_offset
        self.lr_out_offset = lr_out_offset
        self.tb_in_offset = tb_in_offset
        self.tb_out_offset = tb_out_offset
        self.line_pos_p = line_pos_p
        self.color_cfg = color_cfg
        self.dots_intensity = dots_intensity
        self.alpha = alpha
        self.background_color_base = background_color_base
    
    def __call__(self, img: PILImage, text_bbox: BBox, font_text) -> Tuple[PILImage, BBox]:
        return self.apply(img, text_bbox, font_text)

    def apply(self, img: PILImage, text_bbox: BBox, font_text) -> Tuple[PILImage, BBox]:
        func = np.random.choice(
            [
                self.apply_bottom
            ]
        )
        return func(img, text_bbox, font_text)

    def apply_bottom(self, img: PILImage, text_bbox: BBox, font_text) -> Tuple[PILImage, BBox]:
        if font_text.meta['underdot_index'] != []:
            background = font_text.meta['bg']
            in_offset, thickness, out_offset, fill_color, outline_color = \
                self._get_tb_param(background=background)
            new_w = img.width
            new_h = img.height + thickness + in_offset + out_offset

            new_img = transparent_img((new_w, new_h))
            new_img.paste(img, (0, 0))

            draw = ImageDraw.Draw(new_img)

            text_bbox.bottom += in_offset
            
            for underdot_index in font_text.meta['underdot_index']:
                text = font_text.text

                # xy is the top left of the font text.
                xy = font_text.xy
                font = font_text.font
                char_spacings = font_text.meta['char_spacings']

                left_bottom, right_bottom = self._get_rendered_underdot_index(underdot_index, text, xy, font, char_spacings)
                line_pixels = xiaoline(left_bottom, right_bottom)

                dot_step = random.randint(self.dots_intensity[0], self.dots_intensity[1])
                if random.random() < 0.5:
                    for i, pts in enumerate(line_pixels):
                        if i % dot_step == 0:
                            x, y = pts
                            draw.ellipse((x-thickness, y-thickness, x+thickness, y+thickness), 
                                        fill = fill_color, outline = outline_color)
                else:
                    for i, pts in enumerate(line_pixels):
                        if i % dot_step == 0:
                            x, y = pts
                            draw.rectangle((x-thickness, y-thickness, x+thickness, y+thickness), 
                                        fill = fill_color, outline = outline_color)                    

            text_bbox.bottom += thickness
            text_bbox.bottom += out_offset
        else:
            new_img = img

        return new_img, text_bbox

    def _get_tb_param(self, background=None) -> Tuple[int, int, int]:
        in_offset = np.random.randint(*self.tb_in_offset)
        out_offset = np.random.randint(*self.tb_out_offset)
        thickness = np.random.randint(*self.thickness)
        if background is not None and self.background_color_base:
            if isinstance(background, PILImage):
                background = np.array(background)
            
            mean = np.mean(background)
            alpha = np.random.randint(*self.alpha)
            fill_color = (random.randint(0, int(mean * 0.7)), 
                          random.randint(0, int(mean * 0.7)), 
                          random.randint(0, int(mean * 0.7)), 
                          alpha)
            outline_color = (random.randint(0, int(mean * 0.7)), 
                            random.randint(0, int(mean * 0.7)), 
                            random.randint(0, int(mean * 0.7)), 
                            alpha)
        else:
            fill_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            outline_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        return in_offset, thickness, out_offset, fill_color, outline_color

    def _get_line_color(self, img: PILImage, text_bbox: BBox):
        if self.color_cfg is not None:
            # TODO: pass background image
            return self.color_cfg.get_color(img)

        return (
            np.random.randint(0, 170),
            np.random.randint(0, 170),
            np.random.randint(0, 170),
            np.random.randint(90, 255),
        )
    
    def _get_rendered_underdot_index(self, underdot_index, text, xy, font, char_spacings):
        start, end = underdot_index

        if char_spacings == -1:
            right1, bottom1 = font.getsize(text[:start])
            right2, bottom2 = font.getsize(text[:end])
            if bottom1 == 0:
                bottom1 = bottom2
        else:
            char_widths = []
            for c in text:
                size = font.getsize(c)
                char_widths.append(size[0])

            right1 = sum(char_widths[:start]) + sum(char_spacings[:start])
            right2 = sum(char_widths[:end]) + sum(char_spacings[:end])
            _, bottom = font.getsize(text[:end])
            bottom1 = bottom2 = bottom

        right1 += xy[0]
        right2 += xy[0]
        bottom1 += xy[1]
        bottom2 += xy[1]

        left_bottom = (right1, bottom1)
        right_bottom = (right2, bottom2)

        return left_bottom, right_bottom

def xiaoline(p0, p1):
    x0, y0 = p0
    x1, y1 = p1

    x=[]
    y=[]
    dx = x1-x0
    dy = y1-y0
    steep = abs(dx) < abs(dy)

    if steep:
        x0,y0 = y0,x0
        x1,y1 = y1,x1
        dy,dx = dx,dy

    if x0 > x1:
        x0,x1 = x1,x0
        y0,y1 = y1,y0

    gradient = float(dy) / float(dx)  # slope

    """ handle first endpoint """
    xend = round(x0)
    yend = y0 + gradient * (xend - x0)
    xpxl0 = int(xend)
    ypxl0 = int(yend)
    x.append(xpxl0)
    y.append(ypxl0) 
    x.append(xpxl0)
    y.append(ypxl0+1)
    intery = yend + gradient

    """ handles the second point """
    xend = round (x1);
    yend = y1 + gradient * (xend - x1);
    xpxl1 = int(xend)
    ypxl1 = int (yend)
    x.append(xpxl1)
    y.append(ypxl1) 
    x.append(xpxl1)
    y.append(ypxl1 + 1)

    """ main loop """
    for px in range(xpxl0 + 1 , xpxl1):
        x.append(px)
        y.append(int(intery))
        x.append(px)
        y.append(int(intery) + 1)
        intery = intery + gradient;

    if steep:
        y,x = x,y

    coords=zip(x,y)

    return coords