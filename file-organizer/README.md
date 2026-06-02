# 📂 文件整理小助手

自动按文件类型（文档/图片/音频/视频/压缩包/代码）分类整理文件夹。

## 版本

| 文件 | 说明 |
|------|------|
| `file_organizer.py` | 命令行版本，适合脚本和自动化 |
| `file_organizer_gui.py` | 图形界面版本，双击运行，无需命令行 |
| `hello.py` | Python 入门示例 |

## 使用方法

### GUI 版本（推荐）

```bash
python file_organizer_gui.py
```

1. 点击 **选择文件夹**
2. 点击 **开始整理**
3. 完成！

### 命令行版本

```bash
# 整理当前目录
python file_organizer.py

# 整理指定目录
python file_organizer.py "D:/要整理的文件夹"
```

## 分类规则

| 类别 | 扩展名 |
|------|--------|
| 📄 文档 | .pdf .docx .doc .txt .xlsx .pptx |
| 🖼️ 图片 | .jpg .jpeg .png .gif .bmp .svg |
| 🎵 音频 | .mp3 .wav .flac .aac .m4a |
| 🎬 视频 | .mp4 .avi .mkv .mov .wmv |
| 📦 压缩包 | .zip .rar .7z .tar .gz |
| 💻 代码 | .py .js .html .css .json .java |
| 📁 其他 | 以上都不匹配的文件 |

## 打包为 exe

```bash
pip install pyinstaller
pyinstaller --onefile --name "文件整理小助手" file_organizer_gui.py
```

生成的 exe 在 `dist/` 目录下。
