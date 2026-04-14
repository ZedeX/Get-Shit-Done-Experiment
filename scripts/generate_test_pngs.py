#!/usr/bin/env python3
"""
生成测试用PNG图片
创建各种尺寸、格式的PNG图片用于测试
"""

from PIL import Image, ImageDraw, ImageFont
import os

def create_test_image(size, mode, color, text=None, filename=None):
    """
    创建测试图片

    Args:
        size: (width, height)
        mode: 'RGB', 'RGBA', 'L', etc.
        color: 背景颜色
        text: 添加的文字
        filename: 保存文件名
    """
    img = Image.new(mode, size, color)

    if text:
        draw = ImageDraw.Draw(img)
        try:
            # 尝试使用系统字体
            try:
                font = ImageFont.truetype("arial.ttf", size=min(size) // 10)
            except:
                font = ImageFont.load_default()
        except:
            font = None

        if font:
            bbox = draw.textbbox((0, 0), text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            x = (size[0] - text_width) // 2
            y = (size[1] - text_height) // 2

            # 文字阴影
            draw.text((x+2, y+2), text, fill=(0,0,0,128), font=font)
            draw.text((x, y), text, fill=(255,255,255,255), font=font)

    if filename:
        img.save(filename)
        print(f"创建: {filename} ({mode}, {size})")

    return img

def main():
    """主函数 - 生成测试图片"""
    base_dir = "test_images"
    os.makedirs(base_dir, exist_ok=True)

    # 测试图片列表
    test_images = [
        # 小图片
        ("icon_small.png", (32, 32), "RGB", (255, 100, 100), "小"),
        ("icon_medium.png", (64, 64), "RGB", (100, 255, 100), "中"),
        ("icon_large.png", (128, 128), "RGB", (100, 100, 255), "大"),

        # 标准尺寸
        ("photo_small.png", (400, 300), "RGB", (200, 200, 200), "小照片\n400×300"),
        ("photo_medium.png", (800, 600), "RGB", (180, 180, 200), "中照片\n800×600"),
        ("photo_large.png", (1920, 1080), "RGB", (150, 150, 180), "大照片\n1920×1080"),

        # 带透明通道
        ("alpha_simple.png", (200, 200), "RGBA", (255, 150, 150, 200), "简单透明"),
        ("alpha_gradient.png", (200, 200), "RGBA", (0, 0, 0, 0), None),
        ("alpha_logo.png", (256, 256), "RGBA", (50, 50, 200, 180), "LOGO\n透明"),

        # 灰度图
        ("gray_photo.png", (500, 400), "L", 180, "灰度图\n500×400"),
        ("gray_pattern.png", (300, 300), "L", 128, "灰度图案"),

        # 特殊尺寸
        ("panorama.png", (1200, 300), "RGB", (100, 200, 150), "全景图\n1200×300"),
        ("tall.png", (300, 1200), "RGB", (150, 100, 200), "竖长图\n300×1200"),
        ("square_huge.png", (2048, 2048), "RGB", (200, 150, 100), "超大图\n2048×2048"),
    ]

    # 创建普通图片
    for filename, size, mode, color, text in test_images:
        filepath = os.path.join(base_dir, filename)
        create_test_image(size, mode, color, text, filepath)

    # 特殊处理：创建渐变透明图片
    img = Image.new("RGBA", (200, 200), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    for y in range(200):
        for x in range(200):
            alpha = int(255 * (1 - ((x-100)**2 + (y-100)**2)**0.5 / 141.42))
            alpha = max(0, min(255, alpha))
            draw.point((x, y), (255, 100, 200, alpha))
    img.save(os.path.join(base_dir, "alpha_gradient.png"))
    print(f"创建: alpha_gradient.png (RGBA渐变, 200×200)")

    # 创建子目录
    subdir = os.path.join(base_dir, "subdir")
    os.makedirs(subdir, exist_ok=True)

    subdir_images = [
        ("nested_1.png", (150, 150), "RGB", (255, 200, 100), "嵌套1"),
        ("nested_2.png", (150, 150), "RGBA", (100, 255, 200, 150), "嵌套2"),
        ("deep_photo.png", (600, 400), "RGB", (200, 220, 240), "深层图片"),
    ]

    for filename, size, mode, color, text in subdir_images:
        filepath = os.path.join(subdir, filename)
        create_test_image(size, mode, color, text, filepath)

    print(f"\n测试图片生成完成!")
    print(f"目录: {os.path.abspath(base_dir)}")

if __name__ == "__main__":
    main()
