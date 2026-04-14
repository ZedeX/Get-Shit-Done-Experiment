#!/usr/bin/env python3
"""
PNG到WebP批量转换工具 - non-GSD模式 (第二次重复)
"""
import os
import argparse
from PIL import Image


def main():
    parser = argparse.ArgumentParser(description='Convert PNG to WebP')
    parser.add_argument('directory', help='Directory with PNG images')
    parser.add_argument('-q', '--quality', type=int, default=80, help='Quality (1-100)')
    args = parser.parse_args()

    directory = args.directory

    for filename in os.listdir(directory):
        if filename.lower().endswith('.png'):
            png_path = os.path.join(directory, filename)
            webp_path = os.path.join(directory, filename[:-4] + '.webp')

            img = Image.open(png_path)
            img.save(webp_path, 'WebP', quality=args.quality)
            print(f'Converted: {filename}')


if __name__ == '__main__':
    main()
