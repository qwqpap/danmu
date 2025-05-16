# Damm MU~

## 简介

这是一个使用NoneBot作消息处理，LLOneBot插件捕获qq消息，然后用tk渲染的插件。旨在从指定Q群获取所有的文字消息发送到屏幕上

## 光速上手

首先你需要安装[NoneBot](https://nonebot.dev/docs)与[LLOneBot](https://llonebot.com/zh-CN/guide/getting-started)

在这里不再赘述安装过程

之后把本项目全部文件放到`/plugs`下，在`config.py`中添加你的群组号，运行你的NoneBot。

在`danmu_queue.json`创建后，运行同目录下的`run_danmu.py`此时你的弹幕系统应该就好起来了。

相关的弹幕配置在`danmu_window.py`中，请自己更改一下（我懒