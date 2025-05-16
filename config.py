from typing import Set

class Config:
    def __init__(self):
        # 目标群列表
        self.target_groups: Set[int] = {867522755}  
        
        # 弹幕显示配置
        self.font_size = 24
        self.font_color = "#FFFFFF"
        self.danmu_speed = 10  # 像素/秒
        self.danmu_opacity = 0  # 透明度
        self.max_danmu = 50  # 最大同时显示弹幕数