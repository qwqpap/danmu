from nonebot import get_driver
from nonebot.plugin import PluginMetadata
from nonebot.adapters.onebot.v11 import Message, GroupMessageEvent
from nonebot.rule import to_me
from nonebot.matcher import Matcher
from nonebot import on_message
from pathlib import Path
import os
from .danmu_window import write_danmu, DANMU_FILE
from .config import Config
import logging

# 配置日志
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

__plugin_meta__ = PluginMetadata(
    name="弹幕显示",
    description="捕获群消息并显示为弹幕",
    usage="在群内发送消息即可显示弹幕",
    type="application",
    homepage="https://github.com/qwqpap/danmu",
    supported_adapters={"~onebot.v11"},
)

driver = get_driver()
config = Config()

@driver.on_startup
async def startup():
    """插件启动时的初始化操作"""
    logger.debug("Starting up danmu plugin...")
    # 确保弹幕队列文件存在
    if not DANMU_FILE.exists():
        with open(DANMU_FILE, 'w', encoding='utf-8') as f:
            f.write('[]')
    logger.debug("Danmu plugin initialized")

@driver.on_shutdown
async def shutdown():
    """插件关闭时的清理操作"""
    logger.debug("Shutting down danmu plugin...")
    # 清理弹幕队列文件
    if DANMU_FILE.exists():
        DANMU_FILE.unlink()
    logger.debug("Danmu plugin shutdown complete")

# 创建消息处理器
danmu_matcher = on_message(priority=1)

@danmu_matcher.handle()
async def handle_danmu(event: GroupMessageEvent, matcher: Matcher):
    """处理群消息并显示为弹幕"""
    # 检查是否是目标群
    if event.group_id not in config.target_groups:
        logger.debug(f"Message from non-target group: {event.group_id}")
        return
    
    # 获取消息内容
    message = event.get_message()
    # 只处理纯文本消息
    if not message.extract_plain_text():
        logger.debug("Non-text message received, ignoring")
        return
    
    logger.debug(f"Processing message from group {event.group_id}")
    # 写入弹幕
    write_danmu(
        text=message.extract_plain_text(),
        sender=event.sender.nickname or str(event.sender.user_id)
    )
