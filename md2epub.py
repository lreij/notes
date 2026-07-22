#!/usr/bin/env python3
"""
将指定目录下的多个 md 文件转换为 epub，每个文件对应一个章节，标题为文件的第一个非空行。
pip install -r requirements.txt
python md2epub.py ./your_path/
"""

import sys
import os
import glob
import re

from charset_normalizer import from_bytes
from ebooklib import epub
import markdown


def detect_and_read(filepath: str) -> str:
    """读取文件并自动检测编码，返回 UTF-8 字符串。"""
    with open(filepath, "rb") as f:
        raw = f.read()
    result = from_bytes(raw).best()
    if result is None:
        raise ValueError(f"无法检测文件编码: {filepath}")
    return str(result)


def strip_md_heading(line: str) -> str:
    """去除 Markdown 标题标记，返回纯标题文本。"""
    # 去除开头的 # 号（ATX 标题）
    line = re.sub(r"^\s*#+\s*", "", line)
    # 去除 setext / 强调等常见符号
    line = line.strip().strip("*").strip("_").strip()
    return line


def parse_chapter(text: str) -> tuple[str, str]:
    """从 Markdown 文本中提取标题（第一个非空行）和正文 HTML。"""
    lines = text.splitlines()

    # 跳过开头的空行，找到第一个非空行作为标题
    title = ""
    content_start = 0
    for i, line in enumerate(lines):
        if line.strip():
            title = strip_md_heading(line)
            content_start = i + 1
            break

    if not title:
        raise ValueError("文件内容为空，无法提取标题")

    # 剩余内容作为 Markdown 正文渲染为 HTML
    body_md = "\n".join(lines[content_start:])
    body_html = markdown.markdown(
        body_md,
        extensions=["extra", "sane_lists", "nl2br"],
    )
    return title, body_html


def main():
    if len(sys.argv) != 2:
        print(f"用法: python {os.path.basename(sys.argv[0])} <md文件目录>")
        sys.exit(1)

    input_dir = sys.argv[1].rstrip(os.sep)

    if not os.path.isdir(input_dir):
        print(f"错误: 目录不存在: {input_dir}")
        sys.exit(1)

    # 扫描目录下所有 md 文件并按文件名排序
    md_files = sorted(
        glob.glob(os.path.join(input_dir, "*.md"))
        + glob.glob(os.path.join(input_dir, "*.markdown"))
    )

    if not md_files:
        print(f"错误: 目录中没有找到 .md 文件: {input_dir}")
        sys.exit(1)

    # 书名为目录最后一级文件夹名
    book_title = os.path.basename(os.path.abspath(input_dir))

    # 创建 epub
    book = epub.EpubBook()
    book.set_identifier("id_" + book_title)
    book.set_title(book_title)
    book.set_language("zh")
    book.add_author("Unknown")

    chapters = []

    for i, md_file in enumerate(md_files):
        text = detect_and_read(md_file)
        title, body_html = parse_chapter(text)

        chapter = epub.EpubHtml(
            title=title,
            file_name=f"chapter_{i + 1:03d}.xhtml",
            lang="zh",
        )
        chapter.content = (
            f"<html><head><title>{title}</title></head>"
            f"<body><h1>{title}</h1>{body_html}</body></html>"
        )
        book.add_item(chapter)
        chapters.append(chapter)
        print(f"  章节 {i + 1}: {title} ({os.path.basename(md_file)})")

    # 目录
    book.toc = [(epub.Section("目录"), chapters)]

    # 添加默认的导航文件
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())

    # 阅读顺序
    book.spine = ["nav"] + chapters

    # 输出到输入目录内
    output_path = os.path.join(input_dir, f"{book_title}.epub")
    epub.write_epub(output_path, book)
    print(f"\n完成! 已生成: {output_path}")


if __name__ == "__main__":
    main()
