import os
from pathlib import Path

from text_renderer.config import (GeneratorCfg, NormPerspectiveTransformCfg,
                                  RenderCfg, RandomColorCfg)
from text_renderer.corpus import *
from text_renderer.effect import *
from text_renderer.effect.curve import Curve

import imgaug.augmenters as iaa
CURRENT_DIR = Path(os.path.abspath(os.path.dirname(__file__)))

def story_data():
    return GeneratorCfg(
        num_image=50000,
        save_dir=CURRENT_DIR / "output_boxes",
        render_cfg=RenderCfg(
            bg_dir=CURRENT_DIR / "example_data/bg",
            height=32,
            perspective_transform=NormPerspectiveTransformCfg(20, 20, 1.5),
            corpus=DictCorpus(
                DictCorpusCfg(
                    text_paths=[CURRENT_DIR / "example_data/text/processed_box_corpus.json"],
                    font_dir=CURRENT_DIR / "example_data/font/po_vie_font",
                    font_size=(40, 80),
                    char_spacing=(0,0.2)
                ),
            ),
            # custom_corpus_effects=CustomEffects(CustomBoxes(1, thickness=(1, 2))),
            corpus_effects=Effects(
                [
                    Padding(p=.3, w_ratio=[0.2, 0.21], h_ratio=[0.4, 0.6], center=True),
                    Curve(p=.3, period=180, amplitude=(4, 5)),
                    ImgAugEffect(p=.3, aug=iaa.Emboss(alpha=(0.9, 1.0), strength=(1.5, 1.6))),
                    ImgAugEffect(p=.3, aug=iaa.SaltAndPepper((0.1, 0.3), per_channel=True)),
                    ImgAugEffect(p=.3, aug=iaa.Multiply((0.9, 1.2))),
                    Line(p=.3, thickness=(3, 4)),
                ]
            ),
            gray=False,
            text_color_cfg=RandomColorCfg(),
        ),
    )

configs = [story_data()]