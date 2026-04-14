#!/usr/bin/env python3
"""
简单生成测试用PNG图片
"""

from PIL import Image
import os

def create_simple_image(size, color, filename):
    """创建简单的纯色图片"""
    img = Image.new('RGB', size, color)
    img.save(filename)
    print(f"创建: {filename} {size}")

def create_alpha_image(size, color, filename):
    """创建带透明通道的图片"""
    img = Image.new('RGBA', size, color)
    img.save(filename)
    print(f"创建: {filename} {size} (RGBA)")

def main():
    base_dir = "test_images"
    os.makedirs(base_dir, exist_ok=True)

    # 简单测试图片
    test_images = [
        ("test_100x100.png", (100, 100), (255, 100, 100)),
        ("test_200x200.png", (200, 200), (100, 255, 100)),
        ("test_400x300.png", (400, 300), (100, 100, 255)),
        ("test_800x600.png", (800, 600), (200, 200, 100)),
        ("test_1920x1080.png", (1920, 1080), (150, 150, 150)),
    ]

    for filename, size, color in test_images:
        filepath = os.path.join(base_dir, filename)
        create_simple_image(size, color, filepath)

    # RGBA图片
    alpha_images = [
        ("alpha_100x100.png", (100, 100), (255, 100, 100, 200)),
        ("alpha_200x200.png", (200, 200), (100, 255, 100, 150)),
        ("alpha_300x300.png", (300, 300), (100, 100, 255, 100)),
    ]

    for filename, size, color in alpha_images:
        filepath = os.path.join(base_dir, filename)
        create_alpha_image(size, color, filepath)

    # 子目录
    subdir = os.path.join(base_dir, "subdir")
    os.makedirs(subdir, exist_ok=True)

    subdir_images = [
        ("nested_150x150.png", (150, 150), (255, 200, 100)),
        ("nested_250x250.png", (250, 250), (200, 100, 255)),
    ]

    for filename, size, color in subdir_images:
        filepath = os.path.join(subdir, filename)
        create_simple_image(size, color, filepath)

    print(f"\n测试图片生成完成!")
    print(f"目录: {os.path.abspath(base_dir)}")

if __name__ == "__main__":
    main()
