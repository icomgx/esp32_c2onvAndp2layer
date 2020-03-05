# esp32_c2onvAndp2layer 
## ESP32 P2layer 包括转换程序和播放器上位机...
## 关于效果可以看一下这个视频：https://www.bilibili.com/video/av93223051
## B站主页 https://space.bilibili.com/23106193 有想法和建议欢迎私信我
## 开发工具：pycharm 环境：Anaconda3（python 3.7.4）  
## 使用库： pillow, opencv-python, numpy  
## 目录结构
### -fc/ 是转换完成可以播放的fc文件存放位置
### -video/ 待转换视频存放位置 最好是mp4文件
### - c2onv.exe 彩色视频用转换程序
### - c3onv.exe 单色视频转换用程序(类似 bad apple的视频用)
### - p2lyer.exe 播放器上位机程序
### - config.json 配置文件
```json
{
      "host": "0.0.0.0",  TCP监听地址，一般设置为0.0.0.0
      "port": "715",	  TCP监听端口，下位机默认715
      "frame_width": "128",  视频切片图片的宽度
      "frame_height": "64",   视频切片图片的高度
      "frame_sampling": "1",切片的间隔 1为1帧一切
      "video_path": "video/", 待转换视频存放位置默认即可
      "ver": "v0.3"	           版本号
}
```
## 使用说明
## 先看好视频类型选用合适的转换器，可以一次转换很多视频不过耗费的时间也是加倍的，待转换视频最好不要含有特殊字符
## 重要说明*** 转换过程中会产生 temp 临时文件夹 请勿随意改动文件夹及文件夹内的任何内容否则会导致报错！！！
## 转换完毕后生成的fc文件会保存至fc/目录下
##  
## 关于播放
## 首先要烧录好ESP32的程序，然后打开p2layer.exe 按提示输入序号即可 然后给ESP32上电即可播放
##  
## 请勿用于商业用途 保留一切权利追究
## Powered by iCOMgx's Atai
## 2020-03-05
