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
                    text_paths=[CURRENT_DIR / "example_data/text/eng_text.txt"],
                    font_dir=CURRENT_DIR / "example_data/font",
                    font_size=(20, 30),
                    num_word=(10,10),
                ),
            ),
            corpus_effects=Effects(Dots(1, thickness=(1, 2))),
            gray=False,
            text_color_cfg=SimpleTextColorCfg(),
        ),
    )

configs = [story_data()]
