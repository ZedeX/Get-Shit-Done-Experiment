#!/usr/bin/env python3
"""
PNG to WebP批量转换脚本

将指定目录下所有PNG图片批量转换为WebP格式,保留原始文件名结构。

使用方法:
    python png2webp.py --input INPUT_DIR --output OUTPUT_DIR --quality 85
"""

import os
import argparse
from pathlib import Path
from PIL import Image
from typing import List, Tuple


def find_png_files(input_dir: str) -> List[Tuple[str, str]]:
    """
    递归查找目录下所有PNG文件

    Args:
        input_dir: 输入目录路径

    Returns:
        列表,每个元素为 (完整路径, 相对路径) 的元组
    """
    png_files = []
    input_path = Path(input_dir)

    for root, dirs, files in os.walk(input_dir):
        for file in files:
            if file.lower().endswith('.png'):
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, input_dir)
                png_files.append((full_path, rel_path))

    return png_files


def convert_png_to_webp(png_path: str, webp_path: str, quality: int = 85) -> None:
    """
    将单个PNG文件转换为WebP格式

    Args:
        png_path: 输入PNG文件路径
        webp_path: 输出WebP文件路径
        quality: WebP质量 (1-100)
    """
    img = Image.open(png_path)

    # 处理带透明通道的图片
    if img.mode in ('RGBA', 'LA'):
        background = Image.new('RGB', img.size, (255, 255, 255))
        background.paste(img, mask=img.split()[-1])
        img = background

    # 确保输出目录存在
    os.makedirs(os.path.dirname(webp_path), exist_ok=True)

    # 保存为WebP格式
    img.save(webp_path, 'WebP', quality=quality)


def main():
    """主函数"""
    # 解析命令行参数
    parser = argparse.ArgumentParser(
        description='PNG到WebP批量转换工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python png2webp.py --input ./images --output ./webp
  python png2webp.py --input ./images --output ./webp --quality 90
        """
    )
    parser.add_argument('--input', required=True, help='输入目录路径')
    parser.add_argument('--output', required=True, help='输出目录路径')
    parser.add_argument(
        '--quality',
        type=int,
        default=85,
        choices=range(1, 101),
        metavar='[1-100]',
        help='WebP质量 (1-100, 默认: 85)'
    )

    args = parser.parse_args()

    # 查找所有PNG文件
    print(f"正在扫描目录: {args.input}")
    png_files = find_png_files(args.input)

    if not png_files:
        print("未找到PNG文件!")
        return

    print(f"找到 {len(png_files)} 个PNG文件")

    # 批量转换
    success_count = 0
    for i, (png_path, rel_path) in enumerate(png_files, 1):
        # 生成输出路径
        webp_rel_path = os.path.splitext(rel_path)[0] + '.webp'
        webp_path = os.path.join(args.output, webp_rel_path)

        print(f"[{i}/{len(png_files)}] 转换: {rel_path}")

        try:
            convert_png_to_webp(png_path, webp_path, args.quality)
            success_count += 1
        except Exception as e:
            print(f"  错误: {e}")

    print(f"\n转换完成! 成功: {success_count}/{len(png_files)}")


if __name__ == "__main__":
    main()
