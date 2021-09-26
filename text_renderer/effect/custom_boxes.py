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

class CustomBoxes(Effect):
    def __init__(
            self,
            p=0.5,
            thickness=(1, 3),
            lr_in_offset=(0, 10),
            lr_out_offset=(0, 5),
            tb_in_offset=(0, 3),
            tb_out_offset=(0, 3),
            line_pos_p=(0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1),
            Boxes_intensity=(10, 100),
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
        self.Boxes_intensity = Boxes_intensity
        self.alpha = alpha
        self.background_color_base = background_color_base
    
    def __call__(self, img: PILImage, text_bbox: BBox, font_text) -> Tuple[PILImage, BBox]:
        return self.apply(img, text_bbox, font_text)

    def apply(self, img: PILImage, text_bbox: BBox, font_text) -> Tuple[PILImage, BBox]:
        func = np.random.choice(
            [
                self.apply_separated_box
            ]
        )
        return func(img, text_bbox, font_text)

    def apply_separated_box(self, img: PILImage, text_bbox: BBox, font_text) -> Tuple[PILImage, BBox]:
        background = font_text.meta['bg']
        non_box_index = font_text.meta['non_box_index']
        text = font_text.text
        xy = font_text.xy # xy is the top left of the font text.
        font = font_text.font
        char_spacings = font_text.meta['char_spacings']

        in_offset, thickness, out_offset, fill_color, outline_color = \
            self._get_tb_param(background=background)

        new_w = img.width
        new_h = img.height + thickness + in_offset + out_offset
        new_img = transparent_img((new_w, new_h))
        new_img.paste(img, (0, 0))
        draw = ImageDraw.Draw(new_img)

        text_bbox.bottom += in_offset
        text_bbox.bottom += thickness
        text_bbox.bottom += out_offset

        text_bbox.top += in_offset
        text_bbox.top += thickness
        text_bbox.top += out_offset

        box_coords = self._get_text_box_coords(text, xy, font, char_spacings)
        for i in range(len(text)):
            if i not in non_box_index:
                x1, y1, x2, y2 = box_coords[i]
                tl = (x1, y1)
                tr = (x2, y1)
                br = (x2, y2)
                bl = (x1, y2)
                draw.line([tl, tr], fill=fill_color, width=thickness)
                draw.line([tl, bl], fill=fill_color, width=thickness)
                draw.line([br, tr], fill=fill_color, width=thickness)
                draw.line([br, bl], fill=fill_color, width=thickness)

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
    
    def _get_text_box_coords(self, text, xy, font, char_spacings):
        coords = []
        _, bottom = font.getsize(text)
        bottom -= xy[1]
        _, height = font.getmask(text).size
        top = bottom - height
        
        char_rights = []
        for i, char in enumerate(text):
            size = font.getsize(char)
            width, _ = font.getmask(char).size
            char_rights.append(size[0])   

            # right = sum(char_rights) + sum(char_spacings[:i]) + xy[0]
            right = sum(char_rights) + sum(char_spacings[:i])

            left = right-width

            coords.append((left, top, right, bottom))

        return coords
