from typing import Tuple, Union

from PIL import ImageDraw, Image, ImageFont
from PIL.Image import Image as PILImage
import numpy as np
import random
from text_renderer.utils.font_text import FontText
from text_renderer.utils.errors import PanicError
import string

def transparent_img(size: Tuple[int, int]) -> PILImage:
    """
    Args:
        size: (width, height)

    Returns:

    """
    return Image.new("RGBA", (size[0], size[1]), (255, 255, 255, 0))


def draw_text_on_bg_with_boxes(
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
    font = font_text.font
    non_box_index = font_text.meta['non_box_index']
    line_color = (random.randint(0,50), random.randint(0,50), random.randint(0,50))
    line_width = random.randint(2,5)

    base_font_size = font.size
    if random.random() < 0.4:
        key_font_size = int(base_font_size*random.uniform(0.9,1.))
        value_font_size = int(base_font_size*random.uniform(1.1,1.3))

        key_font = ImageFont.truetype(font_text.font_path, key_font_size)
        value_font = ImageFont.truetype(font_text.font_path, value_font_size)
    else:
        key_font = value_font = font

    char_spacings = []
    cs_height = font_text.size[1]
    char_spacings = [int(np.random.uniform(*char_spacing)* cs_height)] * len(text)

    coords, link_indexes, link_coords, text_width, text_height = _get_boxes(text, key_font, value_font, char_spacings, non_box_index)

    text_mask = transparent_img((text_width+line_width, text_height+line_width))
    draw = ImageDraw.Draw(text_mask)

    key_offset_ratio = random.uniform(0.5, 1.)
    no_random_link_offset = True
    no_random_value_offset = True

    if font_text.horizontal:
        for i, c in enumerate(font_text.text):
            if i in link_indexes:
                x1, y1, x2, y2 = link_coords[i]

                offset_x, offset_y = value_font.getoffset(c)
                char_width, char_height = value_font.getmask(c).size
                if no_random_link_offset:
                    link_random_offset_x = random.randint(0, max(0,x2-x1-char_width))
                    link_random_offset_y = random.randint(0, max(0,y2-y1-char_height))
                    no_random_link_offset = False
                offset_x -= link_random_offset_x
                offset_y -= link_random_offset_y
                draw.text((x1-offset_x, y1-offset_y), c, fill=text_color, font=value_font)
                continue

            if i in non_box_index:
                x1, y1, x2, y2 = coords[i]
                # offset_x, offset_y = key_font.getoffset(c)
                # offset = int((text_height-y2)*key_offset_ratio)
                draw.text((x1, y1), c, fill=text_color, font=key_font)
            else:
                x1, y1, x2, y2 = coords[i]
                tl = (x1, y1)
                tr = (x2, y1)
                br = (x2, y2)
                bl = (x1, y2)
                draw.line([tl, tr], fill=line_color, width=line_width)
                draw.line([tl, bl], fill=line_color, width=line_width)
                draw.line([br, tr], fill=line_color, width=line_width)
                draw.line([br, bl], fill=line_color, width=line_width)
                
                char_width, char_height = value_font.getmask(c).size
                # random_offset_x = random.randint(0, max(0,x2-x1-char_width))
                # random_offset_y = random.randint(0, max(0,y2-y1-char_height))
                random_offset_x = 0
                random_offset_y = 0

                x1 += int((x2-x1)/2 - char_width/2)
                y1 += int((y2-y1)/2 - char_height/2)

                offset_x, offset_y = value_font.getoffset(c)
                offset_x -= random_offset_x
                offset_y -= random_offset_y
                # offset_x = 0
                # offset_y = 0
                draw.text((x1-offset_x, y1-offset_y), c, fill=text_color, font=value_font)
    else:
        raise PanicError(f'Non-horizontal text is not supported.')

    return text_mask, char_spacings


def _get_boxes(text, key_font, value_font, char_spacings, non_box_index):
    coords = {}
    char_rights = []
    block = []
    blocks = []

    # key_top = key_font.getoffset(text)[1]
    key_top = 0
    key_bottom = key_font.getsize(text)[1]
    value_top = value_font.getoffset(text)[1]
    value_bottom = value_font.getsize(text)[1]
    box_length = int((value_bottom-value_top)*random.uniform(1,1.2))

    for i, char in enumerate(text):
        if i in non_box_index:
            font = key_font
            pass
        else:
            font = value_font
            if len(block) == 0:
                block.append(i)
            else:
                if i == block[-1]+1:
                    block.append(i)
                    if i == len(text)-1:
                        blocks.append(block)
                else:
                    blocks.append(block)
                    block = [i]

        size = font.getsize(char)
        width = font.getmask(char).size[0]
        char_rights.append(size[0])   

        right = sum(char_rights) + sum(char_spacings[:i])
        left = max(0,right-width)

        if i in non_box_index:
            coords[i] = (left, key_top, right, key_bottom)

    first_box_index  = blocks[0][0]
    right = sum(char_rights[:first_box_index+1]) + sum(char_spacings[:first_box_index])
    width = font.getmask(text[first_box_index]).size[0]
    left = right-width+int(random.uniform(0.5,1.)*box_length)

    shift = int((max(box_length, key_bottom, value_bottom)-min(box_length, key_bottom, value_bottom))/2)
    center = (int((left+right)/2), int(box_length/2)+shift)

    if random.random() < 0.5:
        style = 'merge'
    else:
        style = 'separate'
        separate_offset = int(box_length/2)

    link_coords = {}
    link_indexes = []
    block_link_length = int(box_length)
    x1_base = center[0]-int(box_length/2)
    y1 = center[1]-int(box_length/2)
    x2 = center[0]+int(box_length/2)
    y2 = center[1]+int(box_length/2)
    for block_id in range(len(blocks)):
        block = blocks[block_id]
        if block_id == 0:
            pass
        else:
            x1_base = x2 + block_link_length
            
        for i in range(len(block)):
            if style == 'merge':
                x1 = x1_base + i*box_length
                x2 = x1 + box_length
            elif style == 'separate':
                if i == 0:
                    x1 = x1_base
                else:                    
                    x1 = x2 + separate_offset
                x2 = x1 + box_length
            
            coords[block[i]] = (x1,y1,x2,y2)

        if block[i]+1 != len(text):
            link_indexes.append(block[i]+1)
            link_coords[block[i]+1] = (x2,y1,x2+block_link_length,y2)

    text_width = x2
    text_height = int(max(box_length, key_bottom, value_bottom))
    return coords, link_indexes, link_coords, text_width, text_height