#!/usr/bin/env python3

import fire
import re
from diffusers import StableDiffusionPipeline
import torch
import unicodedata

MODEL = "CompVis/stable-diffusion-v1-4"
GPU = "cuda"

def slugify(value, allow_unicode=False):
    """
    Taken from https://github.com/django/django/blob/master/django/utils/text.py
    Convert to ASCII if 'allow_unicode' is False. Convert spaces or repeated
    dashes to single dashes. Remove characters that aren't alphanumerics,
    underscores, or hyphens. Convert to lowercase. Also strip leading and
    trailing whitespace, dashes, and underscores.
    """
    value = str(value)
    if allow_unicode:
        value = unicodedata.normalize('NFKC', value)
    else:
        value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
    value = re.sub(r'[^\w\s-]', '', value.lower())
    return re.sub(r'[-\s]+', '-', value).strip('-_')

def main(textinput, over10gb=True):

    fp16args = dict()
    if not over10gb:
        fp16args = {"torch_dtype": torch.float16, "revision": "fp16"}  # pylint: disable=no-member

    pipe = StableDiffusionPipeline.from_pretrained(MODEL, use_auth_token=True, **fp16args)
    pipe = pipe.to(GPU)

    with torch.autocast(GPU):
        image = pipe(textinput, guidance_scale=7.5)["sample"][0] 
    imgname = f"{slugify(textinput)}.png"
    image.save(imgname)
    print(f"SUCCESS: image: {imgname}")

if __name__ == '__main__':
    fire.Fire(main)