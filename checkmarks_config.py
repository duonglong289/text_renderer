import os
from pathlib import Path

from text_renderer.config import (GeneratorCfg, NormPerspectiveTransformCfg,
                                  RenderCfg, RandomColorCfg)
from text_renderer.corpus import *
from text_renderer.effect import *
from text_renderer.effect.curve import Curve

import imgaug.augmenters as iaa
CURRENT_DIR = Path(os.path.abspath(os.path.dirname(__file__)))
import imgaug.augmenters as iaa
import imgaug.parameters as iap
import imgaug as ia

aug_final = iaa.Sequential([
    iaa.Sometimes(0.75, 
        iaa.OneOf(
            [
                iaa.Add((-30, 30)),
                iaa.AddToHueAndSaturation((-20, 20)),
                iaa.LinearContrast((0.4, 2.5)),
                iaa.Multiply((0.75, 1.25)),
                iaa.AddToBrightness((-30, 30)),
                iaa.MultiplyBrightness((0.75, 1.25)),
                iaa.BlendAlphaHorizontalLinearGradient(iaa.Add(iap.Normal(iap.Choice([-30, 30]), 20)), start_at=(0, 0.25), end_at=(0.75, 1)),
                iaa.BlendAlphaHorizontalLinearGradient(iaa.Add(iap.Normal(iap.Choice([-30, 30]), 20)), start_at=(0.75, 1), end_at=(0, 0.25)),
                iaa.imgcorruptlike.Brightness(severity=(1,3)),
                iaa.ChangeColorTemperature((3000, 15000)),
                iaa.ChannelShuffle(1),
                iaa.BlendAlphaSimplexNoise(iaa.Multiply(iap.Choice([0.9,1.1]), per_channel=True)),
                iaa.Grayscale(alpha=(0.0, 1.0)),
                iaa.ChangeColorTemperature((3000, 15000)),

                iaa.LinearContrast((0.4, 2.5)),
                iaa.GammaContrast((0.7, 1.5)),
                iaa.LogContrast(gain=(0.6, 1.4)),
                iaa.SigmoidContrast(gain= (3, 7), cutoff=(0.3, 0.6)),
                iaa.SigmoidContrast(gain=(3, 10), cutoff=(0.1, 0.9), per_channel=True),
                iaa.ReplaceElementwise(0.05, iap.Normal(128, 0.4*128), per_channel=0.5),
                iaa.Emboss(alpha=(0.1, 0.5), strength=(0.8, 1.2)),
                iaa.Invert(0.01, per_channel=True),
                iaa.imgcorruptlike.Contrast(severity=(1,2)),
                iaa.pillike.Autocontrast((2, 5)),
            ]
        )
    ),
    
    # Noise and change background
    iaa.Sometimes(0.6,
        iaa.OneOf([
            iaa.imgcorruptlike.Spatter(severity=(1,3)),
            iaa.AdditiveLaplaceNoise(scale=(0.07 * 255, 0.08 * 255)),
            iaa.AdditiveLaplaceNoise(scale=(0.07 * 255, 0.08 * 255), per_channel=True),
            iaa.AdditiveGaussianNoise(scale=(0.02 * 255, 0.1 * 255)),
            iaa.AdditiveGaussianNoise(scale=(0.02 * 255, 0.1 * 255), per_channel=True),
            iaa.Sometimes(0.1, iaa.CoarseDropout(0.02, size_percent=0.1, per_channel=True)),
            iaa.SaltAndPepper(p=0.01),
            iaa.Sharpen(alpha=(0.1, 0.5)),
            iaa.MultiplyElementwise((0.8, 1.2), per_channel=0.5),
            iaa.Dropout((0, 0.1), per_channel=True),
        ])
    ),

    iaa.Sometimes(0.2,
        iaa.OneOf([
            iaa.AverageBlur(k=(1, 2)),
            iaa.GaussianBlur(sigma=(0.5, 2.5)),
            iaa.MotionBlur(k=(3, 5), angle=(-90, 90)),
            iaa.imgcorruptlike.DefocusBlur(severity=1),
            iaa.pillike.FilterSmooth(),
            iaa.pillike.FilterSmoothMore((100, 170)),
            iaa.MedianBlur(k=(3,5)),
        ])
    ),

    # compress image
    iaa.Sometimes(0.2,
        iaa.OneOf([
            iaa.JpegCompression(compression=(30, 80)),
            iaa.imgcorruptlike.Pixelate(severity=(1,2))
        ])
    ),
])


def story_data():
    return GeneratorCfg(
        num_image=1000,
        save_dir=CURRENT_DIR / "output_checkmarks",
        render_cfg=RenderCfg(
            bg_dir=CURRENT_DIR / "example_data/bg",
            height=48,
            perspective_transform=NormPerspectiveTransformCfg(20, 20, 1.5),
            corpus=DictCorpus(
                DictCorpusCfg(
                    text_paths=[CURRENT_DIR / "example_data/text/checkmark_corpus.json"],
                    font_dir=CURRENT_DIR / "example_data/font/po_vie_font",
                    font_size=(40, 80),
                    char_spacing=(0, 0.2)
                ),
            ),
            # custom_corpus_effects=CustomEffects(CustomCheckmarks(1, thickness=(1, 2))),
            layout_effects=Effects(
                [
                    Curve(p=.3, period=180, amplitude=(4, 5)),
                    ImgAugEffect(p=.3, aug=iaa.OneOf([
                            iaa.SaltAndPepper(0.07),
                            iaa.Salt(0.07),
                            iaa.AdditiveLaplaceNoise(scale=0.2*50, per_channel=True),
                            iaa.AdditivePoissonNoise(lam=(0, 50)),
                        ]),
                    ),
                    ImgAugEffect(p=.3, aug=iaa.Multiply((0.9, 1.2))),
                    Line(p=.3, thickness=(3, 4)),
                    DropoutHorizontal(p=0.1),
                    DropoutVertical(p=0.1),
                ]
            ),
            render_effects=Effects(
                [
                    ImgAugEffect(p=.75, aug=aug_final),
                ]
            ),
            gray=False,
            text_color_cfg=RandomColorCfg(),
        ),
    )

configs = [story_data()]
