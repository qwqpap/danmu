import tkinter as tk
from tkinter import font
import random
import time
import logging
import json
import os
from typing import List
from pathlib import Path

# 配置日志
logging.basicConfig(
    level=logging.ERROR,  
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# 获取弹幕文件路径
DANMU_FILE = Path(__file__).parent / "danmu_queue.json"
logger.debug(f"Danmu file path: {DANMU_FILE}")

class Danmu:
    def __init__(self, text: str, sender: str, canvas, font_size: int = 24):
        # 限制文本长度与各种神人
        if len(text) > 50:
            text = text[:47] + "..."
        if "%" in text:
            text = text.replace("%", " ")
        if "/" in text:
            text = text.replace("/", " ")
        if "\\" in text:
            text = text.replace("\\", " ")
        if ":" in text:
            text = text.replace(":", " ")
        if "*" in text:
            text = text.replace("*", " ")
            
        # 配置弹幕参数
        self.text = f"{sender}: {text}"
        self.canvas = canvas
        self.font_size = font_size
        self.color = "#FFFFFF"  # 白色
        self.speed = 5  # 像素/帧
        self.start_time = time.time()
        
        # 创建文本对象
        self.font = font.Font(family="Microsoft YaHei", size=font_size)
        # 等待画布更新完成
        self.canvas.update_idletasks()
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        
        # 确保画布尺寸有效
        if canvas_height <= 100:
            canvas_height = 600  # 默认高度
        
        self.text_id = canvas.create_text(
            canvas_width,
            random.randint(0, canvas_height - 100),
            text=self.text,
            fill=self.color,
            font=self.font,
            anchor="w"
        )
        logger.debug(f"Created danmu: {self.text}")
        
    def update(self):
        # 移动文本
        self.canvas.move(self.text_id, -self.speed, 0)
        # 获取当前位置
        pos = self.canvas.coords(self.text_id)
        return pos[0] > -1000  # 当文本完全移出屏幕时返回False

class DanmuWindow:
    def __init__(self):
        logger.debug("Initializing DanmuWindow")
        
        # 创建主窗口
        self.root = tk.Tk()
        self.root.title("弹幕窗口")
        
        # 设置窗口属性
        self.root.attributes('-alpha', 1)  # 设置透明度
        self.root.attributes('-topmost', True)  # 窗口置顶
        self.root.overrideredirect(True)  # 无边框
        
        # 获取屏幕尺寸
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        # 设置窗口大小和位置
        self.root.geometry(f"{screen_width}x{screen_height}+0+0")
        
        # 创建画布
        self.canvas = tk.Canvas(
            self.root,
            width=screen_width,
            height=screen_height,
            highlightthickness=0,
            bg='black'
        )
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # 绑定事件
        self.root.bind('<Escape>', lambda e: self.close())
        
        # 设置窗口样式
        self.root.wm_attributes('-transparentcolor', 'black')  # 设置黑色为透明色
        
        self.danmu_list: List[Danmu] = []
        self.running = True
        
        # 启动更新循环
        self._schedule_update()
        
        # 确保窗口和画布完全初始化
        self.root.update_idletasks()
        
        # 启动弹幕检查
        self._start_danmu_check()
        
        logger.debug("DanmuWindow initialized")

    def _start_danmu_check(self):
        """启动弹幕检查循环"""
        def check_danmu():
            if self.running:
                try:
                    logger.debug("Checking for new danmu...")
                    danmu_list = read_danmu()
                    if danmu_list:
                        logger.debug(f"Found {len(danmu_list)} new danmu")
                        for danmu in danmu_list:
                            logger.debug(f"Adding danmu: {danmu['sender']}: {danmu['text']}")
                            self.add_danmu(danmu['text'], danmu['sender'])
                    self.root.after(100, check_danmu)  # 每100ms检查一次
                except Exception as e:
                    logger.error(f"Error in check_danmu: {e}")
                    self.root.after(100, check_danmu)  # 发生错误时也要继续检查
        
        logger.debug("Starting danmu check loop...")
        check_danmu()

    def _schedule_update(self):
        """安排下一次更新"""
        if self.running:
            self._update()
            self.root.after(16, self._schedule_update)  # 约60fps

    def _update(self):
        """更新弹幕"""
        try:
            # 更新弹幕
            self.danmu_list = [danmu for danmu in self.danmu_list if danmu.update()]
        except Exception as e:
            logger.error(f"Error in update: {e}")

    def add_danmu(self, text: str, sender: str):
        """添加弹幕"""
        logger.debug(f"Adding danmu: {sender}: {text}")
        danmu = Danmu(text, sender, self.canvas)
        self.danmu_list.append(danmu)

    def close(self):
        """关闭窗口"""
        logger.debug("Closing window")
        self.running = False
        self.root.destroy()

    def run(self):
        """运行窗口主循环"""
        self.root.mainloop()

def write_danmu(text: str, sender: str):
    """写入弹幕信息到文件"""
    try:
        # 读取现有弹幕
        if DANMU_FILE.exists():
            with open(DANMU_FILE, 'r', encoding='utf-8') as f:
                danmu_list = json.load(f)
        else:
            danmu_list = []
        
        # 添加新弹幕
        danmu_list.append({
            'text': text,
            'sender': sender,
            'timestamp': time.time()
        })
        
        # 写入文件
        with open(DANMU_FILE, 'w', encoding='utf-8') as f:
            json.dump(danmu_list, f, ensure_ascii=False, indent=2)
        logger.debug(f"Wrote danmu to file: {sender}: {text}")
            
    except Exception as e:
        logger.error(f"Error writing danmu: {e}")

def read_danmu():
    """读取弹幕信息"""
    if not DANMU_FILE.exists():
        logger.debug("Danmu file does not exist")
        return []
    
    try:
        with open(DANMU_FILE, 'r', encoding='utf-8') as f:
            danmu_list = json.load(f)
        logger.debug(f"Read {len(danmu_list)} danmu from file")
        # 清空文件
        with open(DANMU_FILE, 'w', encoding='utf-8') as f:
            json.dump([], f)
        return danmu_list
    except Exception as e:
        logger.error(f"Error reading danmu: {e}")
        return []

if __name__ == '__main__':
    # 创建弹幕窗口
    window = DanmuWindow()
    
    try:
        window.run()
    except KeyboardInterrupt:
        window.close() 