#!/usr/bin/env python3
"""
PNG到WebP批量转换脚本 - non-GSD模式 (修复版)
"""
import os
import argparse
from PIL import Image


def convert_image(input_path, output_path, quality=85):
    """转换单个PNG图片为WebP"""
    try:
        img = Image.open(input_path)
        # 处理带透明通道的图片
        if img.mode in ('RGBA', 'LA'):
            background = Image.new('RGB', img.size, (255, 255, 255))
            background.paste(img, mask=img.split()[-1])
            img = background
        img.save(output_path, 'WebP', quality=quality)
        return True
    except Exception as e:
        print(f"转换失败 {input_path}: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(description='PNG到WebP批量转换')
    parser.add_argument('--input', required=True, help='输入目录')
    parser.add_argument('--output', required=True, help='输出目录')
    parser.add_argument('--quality', type=int, default=85, help='WebP质量 (1-100)')
    args = parser.parse_args()

    # 确保输入目录存在
    if not os.path.exists(args.input):
        print(f"错误: 输入目录不存在: {args.input}")
        return

    # 统计
    success_count = 0
    total_count = 0

    # 遍历目录
    for root, dirs, files in os.walk(args.input):
        for file in files:
            if file.lower().endswith('.png'):
                total_count += 1
                in_path = os.path.join(root, file)
                # 计算相对路径
                rel_path = os.path.relpath(in_path, args.input)
                # 生成输出路径
                out_rel_path = os.path.splitext(rel_path)[0] + '.webp'
                out_path = os.path.join(args.output, out_rel_path)
                # 确保输出目录存在
                os.makedirs(os.path.dirname(out_path), exist_ok=True)
                # 转换
                print(f"正在转换: {rel_path}")
                if convert_image(in_path, out_path, args.quality):
                    success_count += 1

    print(f"\n完成! 成功: {success_count}/{total_count}")


if __name__ == "__main__":
    main()
