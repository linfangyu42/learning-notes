"""
文件整理小助手
功能：把一个文件夹里的文件按类型（文档、图片、压缩包等）自动分类到不同子文件夹
比如：所有 .pdf 放到「PDF文档」、所有 .jpg/.png 放到「图片」
"""

import os
import shutil

# 文件分类规则：扩展名 → 目标文件夹名
RULES = {
    "文档": [".pdf", ".docx", ".doc", ".txt", ".xlsx", ".pptx"],
    "图片": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg"],
    "音频": [".mp3", ".wav", ".flac", ".aac", ".m4a"],
    "视频": [".mp4", ".avi", ".mkv", ".mov", ".wmv"],
    "压缩包": [".zip", ".rar", ".7z", ".tar", ".gz"],
    "代码": [".py", ".js", ".html", ".css", ".json", ".java"],
}


def organize_folder(folder_path):
    """整理指定文件夹的所有文件"""
    if not os.path.exists(folder_path):
        print(f"❌ 文件夹不存在：{folder_path}")
        return

    moved_count = 0
    skipped_count = 0

    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)

        # 跳过文件夹
        if os.path.isdir(file_path):
            continue

        # 获取文件扩展名（小写）
        _, ext = os.path.splitext(filename)
        ext = ext.lower()

        # 查找匹配的分类
        target_folder = "其他"
        for category, extensions in RULES.items():
            if ext in extensions:
                target_folder = category
                break

        # 创建目标文件夹（如果不存在）
        target_path = os.path.join(folder_path, target_folder)
        if not os.path.exists(target_path):
            os.makedirs(target_path)
            print(f"📁 创建文件夹：{target_folder}")

        # 移动文件
        try:
            shutil.move(file_path, os.path.join(target_path, filename))
            print(f"✅ {filename} → {target_folder}")
            moved_count += 1
        except Exception as e:
            print(f"⚠️  跳过 {filename}：{e}")
            skipped_count += 1

    print(f"\n🎉 整理完成！移动 {moved_count} 个文件，跳过 {skipped_count} 个")


if __name__ == "__main__":
    import sys

    # 如果命令行传了路径就用命令行参数，否则整理当前目录
    path = sys.argv[1] if len(sys.argv) > 1 else "."
    print(f"🔍 正在整理：{os.path.abspath(path)}\n")
    organize_folder(path)
