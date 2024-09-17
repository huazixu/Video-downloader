"""
作者：huaz
"""
import os
import yt_dlp
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox

def progress_hook(d):
    if d['status'] == 'downloading':
        # 更新进度条
        percent = d['_percent_str'].strip('%')
        progress_var.set(float(percent))
        progress_bar.update()

def download_video():
    try:
        url = url_entry.get()
        resolution = resolution_combo.get()
        save_path = path_entry.get()

        if not url:
            messagebox.showerror("Error", "请输入视频 URL")
            return
        if not save_path:
            messagebox.showerror("Error", "请选择保存路径")
            return

        # 清空进度条
        progress_var.set(0)
        progress_bar.update()

        # yt-dlp 配置选项，选择已合并的最佳 mp4 格式
        ydl_opts = {
            'format': f'best[height<={resolution}][ext=mp4]/best[ext=mp4]',
            'outtmpl': os.path.join(save_path, '%(title)s.%(ext)s'),
            'progress_hooks': [progress_hook]  # 添加进度条回调函数
        }

        # 使用 yt-dlp 下载视频
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
            messagebox.showinfo("Success", f"视频已成功下载到 {save_path}")

    except Exception as e:
        messagebox.showerror("Error", f"下载时发生错误：{e}")

def choose_path():
    folder_selected = filedialog.askdirectory()
    path_entry.delete(0, END)
    path_entry.insert(0, folder_selected)

# 创建 GUI 界面
root = Tk()
root.title("万能视频下载器")

# 视频 URL 标签和输入框
url_label = Label(root, text="视频 URL：")
url_label.grid(row=0, column=0, padx=10, pady=10)
url_entry = Entry(root, width=50)
url_entry.grid(row=0, column=1, padx=10, pady=10)

# 分辨率标签和下拉选择框
resolution_label = Label(root, text="分辨率：")
resolution_label.grid(row=1, column=0, padx=10, pady=10)
resolutions = ["360", "720", "1080", "1440", "2160"]  # 常见分辨率
resolution_combo = ttk.Combobox(root, values=resolutions)
resolution_combo.current(2)  # 默认选择1080p
resolution_combo.grid(row=1, column=1, padx=10, pady=10)

# 保存路径标签和输入框
path_label = Label(root, text="保存路径：")
path_label.grid(row=2, column=0, padx=10, pady=10)
path_entry = Entry(root, width=50)
path_entry.grid(row=2, column=1, padx=10, pady=10)

# 浏览按钮
browse_button = Button(root, text="浏览", command=choose_path)
browse_button.grid(row=2, column=2, padx=10, pady=10)

# 进度条
progress_var = DoubleVar()
progress_bar = ttk.Progressbar(root, variable=progress_var, maximum=100)
progress_bar.grid(row=3, column=1, padx=10, pady=20)

# 下载按钮
download_button = Button(root, text="下载视频", command=download_video)
download_button.grid(row=4, column=1, padx=10, pady=20)

root.mainloop()