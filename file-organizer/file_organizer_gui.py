"""
文件整理小助手（带界面的版本）
双击就能运行，不需要命令行
"""

import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

# 文件分类规则
RULES = {
    "文档": [".pdf", ".docx", ".doc", ".txt", ".xlsx", ".pptx"],
    "图片": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg"],
    "音频": [".mp3", ".wav", ".flac", ".aac", ".m4a"],
    "视频": [".mp4", ".avi", ".mkv", ".mov", ".wmv"],
    "压缩包": [".zip", ".rar", ".7z", ".tar", ".gz"],
    "代码": [".py", ".js", ".html", ".css", ".json", ".java"],
}


def organize_folder(folder_path, progress_callback=None):
    """整理文件夹，progress_callback 用于更新进度"""
    if not os.path.exists(folder_path):
        return 0, 0, "文件夹不存在"

    files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
    total = len(files)
    moved = 0
    skipped = 0
    logs = []

    for i, filename in enumerate(files):
        file_path = os.path.join(folder_path, filename)
        _, ext = os.path.splitext(filename)
        ext = ext.lower()

        target_folder = "其他"
        for category, extensions in RULES.items():
            if ext in extensions:
                target_folder = category
                break

        target_path = os.path.join(folder_path, target_folder)
        os.makedirs(target_path, exist_ok=True)

        try:
            shutil.move(file_path, os.path.join(target_path, filename))
            logs.append(f"✅ {filename} → {target_folder}")
            moved += 1
        except Exception as e:
            logs.append(f"⚠️  {filename} 跳过：{e}")
            skipped += 1

        if progress_callback:
            progress_callback(int((i + 1) / total * 100))

    return moved, skipped, "\n".join(logs)


class FileOrganizerApp:
    """图形界面应用"""

    def __init__(self):
        self.window = tk.Tk()
        self.window.title("文件整理小助手")
        self.window.geometry("550x500")
        self.window.resizable(False, False)

        # 标题
        title = tk.Label(self.window, text="📂 文件整理小助手",
                         font=("Microsoft YaHei", 18, "bold"))
        title.pack(pady=15)

        # 说明文字
        desc = tk.Label(self.window,
                        text="选择一个文件夹，自动按类型分类整理\n"
                             "文档/图片/音频/视频/压缩包/代码/其他",
                        font=("Microsoft YaHei", 10), fg="#666")
        desc.pack(pady=5)

        # 文件夹选择区域
        path_frame = tk.Frame(self.window)
        path_frame.pack(pady=20)

        self.path_var = tk.StringVar()
        path_entry = tk.Entry(path_frame, textvariable=self.path_var,
                              width=40, font=("Microsoft YaHei", 10))
        path_entry.pack(side=tk.LEFT, padx=(0, 5))

        browse_btn = tk.Button(path_frame, text="选择文件夹",
                               command=self.browse_folder,
                               font=("Microsoft YaHei", 10))
        browse_btn.pack(side=tk.LEFT)

        # 整理按钮
        self.organize_btn = tk.Button(self.window, text="🔍 开始整理",
                                      command=self.start_organize,
                                      font=("Microsoft YaHei", 12, "bold"),
                                      bg="#4CAF50", fg="white",
                                      width=15, height=2)
        self.organize_btn.pack(pady=15)

        # 进度条
        self.progress = ttk.Progressbar(self.window, length=400, mode='determinate')
        self.progress.pack(pady=10)

        # 日志区域
        log_label = tk.Label(self.window, text="操作记录：",
                             font=("Microsoft YaHei", 9), anchor="w")
        log_label.pack(anchor="w", padx=50)

        self.log_text = tk.Text(self.window, width=55, height=8,
                                font=("Consolas", 9), state="disabled")
        self.log_text.pack(pady=5)

        # 版本信息
        version = tk.Label(self.window, text="v1.0 | 无需安装 Python 即可使用",
                           font=("Microsoft YaHei", 8), fg="#999")
        version.pack(side=tk.BOTTOM, pady=8)

    def browse_folder(self):
        folder = filedialog.askdirectory(title="选择要整理的文件夹")
        if folder:
            self.path_var.set(folder)

    def update_progress(self, value):
        self.progress["value"] = value
        self.window.update_idletasks()

    def set_log(self, text):
        self.log_text.config(state="normal")
        self.log_text.delete(1.0, tk.END)
        self.log_text.insert(tk.END, text)
        self.log_text.config(state="disabled")

    def start_organize(self):
        folder = self.path_var.get().strip()
        if not folder:
            messagebox.showwarning("提示", "请先选择一个文件夹！")
            return

        if not os.path.exists(folder):
            messagebox.showerror("错误", f"文件夹不存在：\n{folder}")
            return

        self.organize_btn.config(state="disabled", text="整理中...")
        self.progress["value"] = 0

        try:
            moved, skipped, logs = organize_folder(folder, self.update_progress)
            self.set_log(logs)
            self.progress["value"] = 100
            messagebox.showinfo("完成",
                                f"🎉 整理完成！\n移动 {moved} 个文件，跳过 {skipped} 个")
        except Exception as e:
            messagebox.showerror("出错", f"整理过程中出现问题：\n{e}")
        finally:
            self.organize_btn.config(state="normal", text="🔍 开始整理")

    def run(self):
        self.window.mainloop()


if __name__ == "__main__":
    app = FileOrganizerApp()
    app.run()
