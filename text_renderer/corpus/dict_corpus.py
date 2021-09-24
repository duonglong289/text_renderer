import json
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Tuple, Union

import numpy as np
from loguru import logger
from tenacity import retry, stop_after_attempt
from text_renderer.utils import FontText
from text_renderer.utils.errors import PanicError, RetryError
import random
import string
from .corpus import Corpus, CorpusCfg


@dataclass
class DictCorpusCfg(CorpusCfg):
    """
    Word corpus config

    args:
        text_paths (List[Path]): Text file paths
        separator (str): word separator of texts and join char in get_text()
        num_word (Tuple[int, int]): Range of output word count  [min_length, max_length)
        filter_by_chars (bool): If True, filtering text by character set
        chars_file (Path): Character set
        filter_font (bool): Only work when filter_by_chars is True. If True filter font file
                            by intersection of font support chars with chars file
        filter_font_min_support_chars (int): If intersection of font support chars with chars file is lower
                                             than filter_font_min_support_chars, filter this font file.

    """

    text_paths: List[Path] = field(default_factory=list)
    separator: str = " "
    num_word: (int, int) = (1, 5)
    filter_by_chars: bool = False
    chars_file: Path = None
    filter_font: bool = False
    filter_font_min_support_chars: int = 100


class DictCorpus(Corpus):
    """
    Output contiguous words of a certain length
    """

    def __init__(self, cfg: "CorpusCfg"):
        super().__init__(cfg)

        self.cfg: DictCorpusCfg
        if len(self.cfg.text_paths) == 0:
            raise PanicError("text_paths must not be empty")

        self.words: List[str] = []

        for text_path in self.cfg.text_paths:
            with open(text_path, "r", encoding="utf-8") as f:
                self.texts = json.load(f)

        self.keys = [*self.texts]
        self.current_key_index = 0

    def __len__(self):
        return len(self.keys)

    def get_text(self):
        key = self.keys[self.current_key_index]
        value = self.texts[key]
        self.current_key_index += 1

        return value

    @retry
    def sample(self):
        """
        This method ensures that the selected font supports all characters.

        Returns:
            FontText: A FontText object contains text and font.

        """
        try:
            text_info = self.get_text()
            text = text_info['text']
            meta = {k:v for k,v in text_info.items() if k!='text'}
            for underdot_index in meta['underdot_index']:
                text = text.replace('.',' ',underdot_index[1]-underdot_index[0]+1)
        except Exception as e:
            logger.exception(e)
            raise RetryError()

        font, support_chars, font_path = self.font_manager.get_font()
        status, intersect = self.font_manager.check_support(text, support_chars)
        if not status:
            err_msg = (
                f"{self.__class__.__name__} {font_path} not support chars: {intersect}"
            )
            logger.debug(err_msg)
            raise RetryError(err_msg)

        return FontText(font, text, font_path, self.cfg.horizontal, meta)
