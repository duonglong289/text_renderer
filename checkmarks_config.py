import os
from pathlib import Path

from text_renderer.config import (GeneratorCfg, NormPerspectiveTransformCfg,
                                  RenderCfg, SimpleTextColorCfg)
from text_renderer.corpus import *
from text_renderer.effect import *
from text_renderer.effect.curve import Curve

import imgaug.augmenters as iaa
CURRENT_DIR = Path(os.path.abspath(os.path.dirname(__file__)))

def story_data():
    return GeneratorCfg(
        num_image=1000,
        save_dir=CURRENT_DIR / "output_checkmarks",
        render_cfg=RenderCfg(
            bg_dir=CURRENT_DIR / "example_data/bg",
            height=32,
            perspective_transform=NormPerspectiveTransformCfg(20, 20, 1.5),
            corpus=DictCorpus(
                DictCorpusCfg(
                    text_paths=[CURRENT_DIR / "example_data/text/checkmark_corpus.json"],
                    font_dir=CURRENT_DIR / "example_data/font/vie",
                    font_size=(40, 70),
                    char_spacing=(-0.2,0.2)
                ),
            ),
            # custom_corpus_effects=CustomEffects(CustomCheckmarks(1, thickness=(1, 2))),
            corpus_effects=Effects(
                [
                    DropoutRand(p=.1, dropout_p=(0.3, 0.5)),
                    DropoutHorizontal(p=.1, num_line=2, thickness=3),
                    DropoutVertical(p=.1, num_line=15),
                    Padding(p=.1, w_ratio=[0.2, 0.21], h_ratio=[0.7, 0.71], center=True),
                    Curve(p=.1, period=180, amplitude=(4, 5)),
                    ImgAugEffect(p=.1, aug=iaa.Emboss(alpha=(0.9, 1.0), strength=(1.5, 1.6))),
                ]
            ),
            gray=False,
            text_color_cfg=SimpleTextColorCfg(),
        ),
    )

configs = [story_data()]
