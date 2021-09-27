from typing import Tuple, Union

from PIL import ImageDraw, Image, ImageFont
from PIL.Image import Image as PILImage
import numpy as np
import random
from text_renderer.utils.font_text import FontText
from text_renderer.utils.errors import PanicError
import string
from pathlib import Path

def transparent_img(size: Tuple[int, int]) -> PILImage:
    """
    Args:
        size: (width, height)

    Returns:

    """
    return Image.new("RGBA", (size[0], size[1]), (255, 255, 255, 0))


def draw_text_on_bg_with_checkmarks(
    font_text: FontText,
    text_color: Tuple[int, int, int, int] = (0, 0, 0, 255),
    char_spacing: Union[float, Tuple[float, float]] = -1,
) -> PILImage:
    """
    Parameters
    ----------
    font_text : FontText
    text_color : RGBA
        Default is black
    char_spacing : Union[float, Tuple[float, float]]
        Draw character with spacing. If tuple, random choice between [min, max)
        Set -1 to disable

    Returns
    -------
        PILImage:
            RGBA Pillow image with text on a transparent image
    -------

    """
    text = font_text.text
    kv_border = text.find(': ')
    font = font_text.font
    checkmark_index = font_text.meta['checkmark_index']
    checkmark_type = font_text.meta['checkmark_type']
    line_color = (random.randint(0,50), random.randint(0,50), random.randint(0,50))
    line_width = random.randint(2,5)

    base_font_size = font.size
    if random.random() < 0.4:
        key_font_size = int(base_font_size*random.uniform(0.9,1.))
        value_font_size = int(base_font_size*random.uniform(1.1,1.3))

        key_font = ImageFont.truetype(font_text.font_path, key_font_size)
        value_font = ImageFont.truetype(font_text.font_path, value_font_size)
    else:
        key_font_size = value_font_size = base_font_size
        key_font = value_font = font

    # special_char_font_list = list(Path('example_data/font/special_character').glob('**/*.ttf'))
    special_char_font = ImageFont.truetype('example_data/font/special_character/ArialUnicodeMS.ttf', value_font_size)

    char_spacings = []
    cs_height = font_text.size[1]
    char_spacings = [int(np.random.uniform(*char_spacing)* cs_height)] * len(text)

    coords, text_width, text_height = _get_boxes(text, key_font, value_font, char_spacings, checkmark_index, kv_border, line_width)

    text_mask = transparent_img((text_width+2*line_width, text_height+2*line_width))
    draw = ImageDraw.Draw(text_mask)

    if font_text.horizontal:
        for i, c in enumerate(font_text.text):
            if i <= kv_border:
                x1, y1, x2, y2 = coords[i]
                draw.text((x1, y1), c, fill=text_color, font=key_font)
            else:
                if i in checkmark_index:
                    x1, y1, x2, y2 = coords[i]
                    
                    if checkmark_type[checkmark_index.index(i)] == 'box':
                        tl = (x1, y1)
                        tr = (x2, y1)
                        br = (x2, y2)
                        bl = (x1, y2)
                        draw.line([tl, tr], fill=line_color, width=line_width)
                        draw.line([tl, bl], fill=line_color, width=line_width)
                        draw.line([br, tr], fill=line_color, width=line_width)
                        draw.line([br, bl], fill=line_color, width=line_width)
                    
                    if c == 'E':
                        c = ''
                    elif c == 'V':
                        # '\u1F5F8' Something wrong with dis.
                        c = random.choice(['\u2713', '\u2714'])
                    elif c == 'X':
                        # '\u10102' Something wrong with dis.
                        c = random.choice(['\u2717', '\u2718'])

                    char_width, char_height = special_char_font.getmask(c).size
                    x1 += int((x2-x1)/2 - char_width/2)
                    y1 += int((y2-y1)/2 - char_height/2)
                    offset_x, offset_y = special_char_font.getoffset(c)
                    draw.text((x1-offset_x, y1-offset_y), c, fill=text_color, font=special_char_font)
                else:
                    x1, y1, x2, y2 = coords[i]
                    draw.text((x1, y1), c, fill=text_color, font=value_font)
    else:
        raise PanicError(f'Non-horizontal text is not supported.')

    return text_mask, char_spacings


def _get_boxes(text, key_font, value_font, char_spacings, checkmark_index, kv_border, line_width):
    coords = {}
    char_rights = []
    
    key_height = key_font.getmask(text).size[1]
    key_top = key_font.getoffset(text)[1]
    value_height = value_font.getmask(text).size[1]
    key_bottom = key_font.getsize(text)[1]
    value_top = value_font.getoffset(text)[1]
    value_bottom = value_font.getsize(text)[1]
    box_length = int((value_bottom-value_top)*random.uniform(1,1.2))
    text_height = int(max(box_length, key_bottom, value_bottom))

    for i, char in enumerate(text):
        if i <= kv_border:
            font = key_font
            height = key_height
            offset = key_top
        else:
            font = value_font
            height = value_height
            offset = value_top

        if i in checkmark_index:
            top = int((text_height-box_length)/2)+line_width
            char_right = width = box_length
            bottom = top + box_length
        else:
            top = int((text_height-height)/2)+line_width-offset
            char_right = font.getsize(char)[0]
            width = font.getmask(char).size[0]
            bottom = top+height

        char_rights.append(char_right)   
        right = sum(char_rights) + sum(char_spacings[:i])
        left = max(0,right-width)

        coords[i] = (left, top, right, bottom)

    text_width = right
    return coords, text_width, text_height