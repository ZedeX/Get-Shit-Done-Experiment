#!/usr/bin/env python3
import os
import argparse
from PIL import Image

def convert_image(input_path, output_path, quality=85):
    img = Image.open(input_path)
    if img.mode in ('RGBA', 'LA'):
        background = Image.new('RGB', img.size, (255, 255, 255))
        background.paste(img, mask=img.split()[-1])
        img = background
    img.save(output_path, 'WebP', quality=quality)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', required=True)
    parser.add_argument('--output', required=True)
    parser.add_argument('--quality', type=int, default=85)
    args = parser.parse_args()

    for root, dirs, files in os.walk(args.input):
        for file in files:
            if file.endswith('.png'):
                in_path = os.path.join(root, file)
                rel_path = os.path.relpath(in_path, args.input)
                out_path = os.path.join(args.output, rel_path[:-4] + '.webp')
                os.makedirs(os.path.dirname(out_path), exist_ok=True)
                convert_image(in_path, out_path, args.quality)

if __name__ == "__main__":
    main()
