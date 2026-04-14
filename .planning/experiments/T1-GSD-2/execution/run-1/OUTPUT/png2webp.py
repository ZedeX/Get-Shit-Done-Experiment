#!/usr/bin/env python3
"""
PNG到WebP批量转换工具 - GSD模式 (第二次重复)
"""
import os
import argparse
from pathlib import Path
from PIL import Image


def convert_image(png_path: Path, webp_path: Path, quality: int = 80) -> None:
    """将单个PNG图片转换为WebP格式"""
    img = Image.open(png_path)

    # 保留透明度信息
    if img.mode in ('RGBA', 'LA') or (img.mode == 'P' and 'transparency' in img.info):
        img.save(webp_path, 'WebP', quality=quality, lossless=False)
    else:
        img.save(webp_path, 'WebP', quality=quality)


def convert_directory(source_dir: str, output_dir: str = None,
                     quality: int = 80, recursive: bool = False) -> int:
    """批量转换目录下的PNG图片"""
    source_path = Path(source_dir)

    if not source_path.exists():
        raise FileNotFoundError(f"目录不存在: {source_dir}")

    # 确定输出目录
    if output_dir is None:
        output_path = source_path
    else:
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

    # 查找PNG文件
    pattern = '**/*.png' if recursive else '*.png'
    png_files = list(source_path.glob(pattern))

    converted = 0
    for png_file in png_files:
        # 计算相对路径以保持目录结构
        if recursive:
            rel_path = png_file.relative_to(source_path)
            webp_file = output_path / rel_path.with_suffix('.webp')
            webp_file.parent.mkdir(parents=True, exist_ok=True)
        else:
            webp_file = output_path / png_file.with_suffix('.webp').name

        convert_image(png_file, webp_file, quality)
        converted += 1
        print(f"已转换: {png_file.name} -> {webp_file.name}")

    return converted


def main():
    parser = argparse.ArgumentParser(
        description='批量将PNG图片转换为WebP格式',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  %(prog)s ./images/                    # 转换当前目录
  %(prog)s ./images/ --quality 90       # 设置质量为90
  %(prog)s ./images/ -o ./webp/         # 指定输出目录
  %(prog)s ./images/ --recursive         # 递归处理子目录
        """
    )
    parser.add_argument('source', help='包含PNG图片的源目录')
    parser.add_argument('-o', '--output-dir', help='输出目录（默认同源目录）')
    parser.add_argument('-q', '--quality', type=int, default=80,
                        help='WebP质量 (1-100, 默认: 80)')
    parser.add_argument('-r', '--recursive', action='store_true',
                        help='递归处理子目录')

    args = parser.parse_args()

    try:
        count = convert_directory(
            args.source,
            args.output_dir,
            args.quality,
            args.recursive
        )
        print(f"\n完成! 共转换 {count} 张图片")
    except Exception as e:
        print(f"错误: {e}")
        return 1

    return 0


if __name__ == '__main__':
    exit(main())
