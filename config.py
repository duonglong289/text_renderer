import os
from pathlib import Path

from text_renderer.effect import *
from text_renderer.corpus import *
from text_renderer.config import (
    RenderCfg,
    NormPerspectiveTransformCfg,
    GeneratorCfg,
    SimpleTextColorCfg,
)

CURRENT_DIR = Path(os.path.abspath(os.path.dirname(__file__)))

def story_data():
    return GeneratorCfg(
        num_image=1,
        save_dir=CURRENT_DIR / "output",
        render_cfg=RenderCfg(
            bg_dir=CURRENT_DIR / "example_data/bg",
            height=32,
            perspective_transform=NormPerspectiveTransformCfg(20, 20, 1.5),
            corpus=WordCorpus(
                WordCorpusCfg(
                    text_paths=[CURRENT_DIR / "example_data/text/kv_text.txt"],
                    font_dir=CURRENT_DIR / "example_data/font/vie",
                    font_size=(20, 30),
                    num_word=(2,2),
                ),
            ),
            custom_corpus_effects=CustomEffects(CustomDots(1, thickness=(1, 2))),
            gray=False,
            text_color_cfg=SimpleTextColorCfg(),
        ),
    )

configs = [story_data()]
