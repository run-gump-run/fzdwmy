import os
import re
from pathlib import Path

BASE_DIR = Path(__file__).parent
IMAGE_FOLDERS = {
    "fanzhendong.html": BASE_DIR / "images" / "fanzhendong",
    "wangmanyu.html": BASE_DIR / "images" / "wangmanyu",
}
IMAGE_EXTENSIONS = (".jpg", ".jpeg", ".png", ".webp", ".gif")


def generate_slides(folder: Path) -> str:
    """根据文件夹中的图片生成轮播 HTML。"""
    images = sorted(
        f for f in folder.iterdir()
        if f.is_file() and f.suffix.lower() in IMAGE_EXTENSIONS
    )
    if not images:
        return '  <div class="hero-slides"></div>'

    relative_folder = folder.relative_to(BASE_DIR).as_posix()
    lines = ['  <div class="hero-slides">']
    for i, img in enumerate(images):
        path = f"{relative_folder}/{img.name}"
        active = " active" if i == 0 else ""
        lines.append(
            f'    <div class="hero-slide{active}" style="background-image: url(\'{path}\')"></div>'
        )
    lines.append('  </div>')
    return "\n".join(lines)


def update_html(html_file: Path, folder: Path):
    """替换 HTML 中 HERO_SLIDES_START 与 HERO_SLIDES_END 之间的内容。"""
    content = html_file.read_text(encoding="utf-8")
    slides = generate_slides(folder)

    # 匹配 START 标记后换行到 END 标记前的全部内容（END 前可能有缩进空格）
    pattern = r"(<!-- HERO_SLIDES_START -->)\r?\n.*?\r?\n(\s*<!-- HERO_SLIDES_END -->)"
    replacement = f"<!-- HERO_SLIDES_START -->\n{slides}\n  <!-- HERO_SLIDES_END -->"
    new_content, count = re.subn(pattern, replacement, content, count=1, flags=re.DOTALL)

    if count == 0:
        print(f"警告：未在 {html_file.name} 中找到 HERO_SLIDES 标记")
        return

    html_file.write_text(new_content, encoding="utf-8")
    image_count = len(
        [f for f in folder.iterdir() if f.is_file() and f.suffix.lower() in IMAGE_EXTENSIONS]
    )
    print(f"已更新 {html_file.name}，共 {image_count} 张轮播图片")


def main():
    for html_name, folder in IMAGE_FOLDERS.items():
        html_file = BASE_DIR / html_name
        if not html_file.exists():
            print(f"跳过：{html_file} 不存在")
            continue
        if not folder.exists():
            print(f"跳过：{folder} 不存在")
            continue
        update_html(html_file, folder)


if __name__ == "__main__":
    main()
