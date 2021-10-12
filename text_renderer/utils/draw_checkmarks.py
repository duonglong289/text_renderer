from typing import Tuple, Union

from PIL import ImageDraw, Image, ImageFont
from PIL.Image import Image as PILImage
import numpy as np
import random
from text_renderer.utils.font_text import FontText
from text_renderer.utils.errors import PanicError
from .draw_bezier_curve import draw_bezier_x_checkmark, draw_bezier_v_checkmark

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
    # checkmark_type = font_text.meta['checkmark_type']
    checkmark_color, checkmark_width, checkmark_fill, box_color, box_line_width, box_rectangle_rate = get_checkmark_params()

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

    coords, text_width, text_height = _get_boxes(text, key_font, value_font, char_spacings, checkmark_index, kv_border, box_line_width)

    text_mask = transparent_img((text_width+2*box_line_width, text_height+2*box_line_width))
    draw = ImageDraw.Draw(text_mask)

    rectangle = box_rectangle_rate > random.random()
    if font_text.horizontal:
        for i, c in enumerate(font_text.text):
            if i <= kv_border:
                x1, y1, x2, y2 = coords[i]
                draw.text((x1, y1), c, fill=text_color, font=key_font)
            else:
                if i in checkmark_index:
                    x1, y1, x2, y2 = coords[i]
                    tl = (x1, y1)
                    br = (x2, y2)
                    
                    chmk = text[i]
                    c = ''
                    if chmk == 'X':
                        tick_shape = random.choice(['square', 'circle'])
                        tick_type = random.choice(['x', 'v'])
                        is_dense = random.random() < 1/3

                        if tick_shape == 'square':
                            if is_dense:
                                draw.rectangle([tl, br], fill=checkmark_color, outline=box_color, width=box_line_width)
                            else:
                                draw.rectangle([tl, br], fill=None, outline=box_color, width=box_line_width)
                        elif tick_shape == 'circle':
                            if is_dense:
                                draw.ellipse([tl, br], fill=checkmark_color, outline=box_color, width=box_line_width)
                            else:
                                draw.ellipse([tl, br], fill=None, outline=box_color, width=box_line_width)
                        
                        if not is_dense:
                            if tick_type == 'x':
                                if checkmark_fill == 'machine':
                                    c = random.choice(['\u2717', '\u2718'])
                                elif checkmark_fill == 'hand':
                                    draw = draw_bezier_x_checkmark(draw, coords[i], text_color, checkmark_width)
                            elif tick_type == 'v':
                                if checkmark_fill == 'machine':
                                    c = random.choice(['\u2713', '\u2714'])
                                elif checkmark_fill == 'hand':
                                    draw = draw_bezier_v_checkmark(draw, coords[i], text_color, checkmark_width)
                    else:
                        tick_shape = random.choice(['square', 'circle'])
                        if tick_shape == 'square':
                            draw.rectangle([tl, br], fill=None, outline=box_color, width=box_line_width)
                        elif tick_shape == 'circle':
                            draw.ellipse([tl, br], fill=None, outline=box_color, width=box_line_width)

                    # if chmk == '\u25a0':
                    #     if chmk_type == '\u25a0':
                    #         draw.rectangle([tl, br], fill=checkmark_color, outline=box_color, width=box_line_width)
                    #     else:
                    #         draw.rectangle([tl, br], fill=None, outline=box_color, width=box_line_width)
                    # elif chmk_type in ['\u24cd', '\u24cb', '\u25cb', '\u25cf']:
                    #     if chmk_type == '\u25cf':
                    #         draw.ellipse([tl, br], fill=checkmark_color, outline=box_color, width=box_line_width)
                    #     else:
                    #         draw.ellipse([tl, br], fill=None, outline=box_color, width=box_line_width)
                    
                    # if c == 'V':
                    #     # '\u1F5F8' Something wrong with dis.
                    #     if checkmark_fill == 'machine':
                    #         c = random.choice(['\u2713', '\u2714'])
                    #     elif checkmark_fill == 'hand':
                    #         c = ''
                    #         draw = draw_bezier_v_checkmark(draw, coords[i], text_color, checkmark_width)
                    # elif c == 'X':
                    #     # '\u10102' Something wrong with dis.
                    #     if checkmark_fill == 'machine':
                    #         c = random.choice(['\u2717', '\u2718'])
                    #     elif checkmark_fill == 'hand':
                    #         c = ''
                    #         draw = draw_bezier_x_checkmark(draw, coords[i], text_color, checkmark_width)
                    # else:
                    #     c = ''

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


def get_checkmark_params():
    ### Checkmark color
    checkmark_color_list = ['red', 'blue', 'black']
    checkmark_color = random.choice(checkmark_color_list)
    if checkmark_color == 'red':
        r = random.randint(200, 255)
        g = random.randint(0, 50)
        b = random.randint(0, 50)
        checkmark_color = (r,g,b)
    elif checkmark_color == 'blue':
        r = random.randint(0, 50)
        g = random.randint(0, 50)
        b = random.randint(200, 255)
        checkmark_color = (r,g,b)
    else:
        r = random.randint(0, 50)
        g = random.randint(0, 50)
        b = random.randint(0, 50)
        checkmark_color = (r,g,b)
    ##############################

    ### Checkmark width
    checkmark_width = random.randint(6, 12)
    ##############################

    ### Checkmark type
    checkmark_fill_list = ['hand', 'machine']
    checkmark_fill = random.choice(checkmark_fill_list)
    ##############################

    ### Box color
    r = random.randint(0, 50)
    g = random.randint(0, 50)
    b = random.randint(0, 50)
    box_color = (r,g,b)
    ##############################

    ### Box line width
    box_line_width = random.randint(2,6)
    ##############################

    ### Box rectangle rate, if not rectanlge then ellipse
    box_rectangle_rate = 0.8
    ##############################

    return checkmark_color, checkmark_width, checkmark_fill, box_color, box_line_width, box_rectangle_rate