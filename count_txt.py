#!/usr/bin/env python3
"""统计文本文件的字数。中文按字计，英文/数字按词计，标点不计。"""

import re
import sys


def is_chinese_char(ch: str) -> bool:
    """判断一个字符是否是中文字符（CJK统一汉字）。"""
    cp = ord(ch)
    if 0x4E00 <= cp <= 0x9FFF:
        return True
    if 0x3400 <= cp <= 0x4DBF:
        return True
    if 0x20000 <= cp <= 0x2A6DF:
        return True
    if 0x2A700 <= cp <= 0x2B73F:
        return True
    if 0x2B740 <= cp <= 0x2B81F:
        return True
    if 0xF900 <= cp <= 0xFAFF:
        return True
    return False


def is_ascii_alnum(ch: str) -> bool:
    """判断字符是否是ASCII字母或数字。"""
    return ('a' <= ch <= 'z') or ('A' <= ch <= 'Z') or ('0' <= ch <= '9')


def count_words(text: str) -> int:
    """
    统计字数：
    - 中文字符逐字计数
    - 连续ASCII字母/数字混合序列算一个词
    - 标点符号不计入
    """
    count = 0
    i = 0
    n = len(text)

    while i < n:
        ch = text[i]

        # 中文字符：计1
        if is_chinese_char(ch):
            count += 1
            i += 1
        # ASCII字母或数字：找到连续序列，整体计1
        elif is_ascii_alnum(ch):
            count += 1
            i += 1
            while i < n and is_ascii_alnum(text[i]):
                i += 1
        # 其他字符（标点、空格等）：跳过
        else:
            i += 1

    return count


def main():
    if len(sys.argv) != 2:
        print(f"用法: {sys.argv[0]} <文本文件路径>", file=sys.stderr)
        sys.exit(1)

    filepath = sys.argv[1]
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            text = f.read()
    except FileNotFoundError:
        print(f"错误: 文件不存在 - {filepath}", file=sys.stderr)
        sys.exit(1)
    except UnicodeDecodeError:
        print(f"错误: 文件编码不是UTF-8 - {filepath}", file=sys.stderr)
        sys.exit(1)

    print(count_words(text))


if __name__ == "__main__":
    main()
