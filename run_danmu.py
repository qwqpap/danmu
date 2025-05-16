import sys
from pathlib import Path

# 添加父目录到 Python 路径
current_dir = Path(__file__).parent
sys.path.append(str(current_dir))

from danmu_window import DanmuWindow

if __name__ == '__main__':
    window = DanmuWindow()
    try:
        window.run()
    except KeyboardInterrupt:
        window.close() 