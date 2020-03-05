import shutil
from main import conv, videoCut
import os
import time
import json


# 创建临时文件夹
def createTempFolder():
    create_path = ['temp1', 'temp2', 'temp3', 'temp4']
    for cpath in create_path:
        if not os.path.exists(cpath):
            os.makedirs(cpath)


def createVideoFrameTemp(d2rs):
    tempFolder = ['temp2', 'temp3', 'temp4']
    for tf in tempFolder:
        if not os.path.exists(f'{tf}/{d2rs}'):
            os.makedirs(f'{tf}/{d2rs}')


# 删除临时文件夹
def removeTempFolder():
    remove_path = ['temp1', 'temp2', 'temp3', 'temp4']
    for rpath in remove_path:
        shutil.rmtree(rpath)


# 读取配置文件，返回配置字典对象
def readConfiguration():
    with open("config.json", 'r') as load_f:
        load_dict = json.load(load_f)
        return load_dict


# 视频切片
def startVideoCut(video_src_path, frame_width, frame_height, interval):
    videos_name = videoCut.video2frame(video_src_path, 'temp1/', frame_width, frame_height, interval)
    return videos_name


# 帧图片处理
def frameProcess():
    for dirs in os.walk('temp1'):
        for d2rs in dirs[1]:
            createVideoFrameTemp(d2rs)
            data = os.listdir(f'temp1/{d2rs}')  # 循环切片图片转换为灰度图像
            for dat in data:
                conv.conv2(f'temp1/{d2rs}/{dat}', f'temp2/{d2rs}/{dat}')  # 转换成灰度图像
            data2 = os.listdir(f'temp2/{d2rs}')  # 循环图片二值化
            for dat2 in data2:
                conv.conv4(f'temp2/{d2rs}/{dat2}', f'temp3/{d2rs}/{dat2}')  # 二值化操作
            data3 = os.listdir(f'temp3/{d2rs}')  # 循环二值化完成的图片转为1位图
            for dat3 in data3:
                conv.conv3(f'temp3/{d2rs}/{dat3}', f'temp4/{d2rs}/{dat3}')  # 转换1位图操作
            d3ta = {}  # 定义一个字典来存储数据
            data4 = os.listdir(f'temp4/{d2rs}')  # 获取一位图
            d3ta.update({'fc_len': str(len(data4))})  # 获取所有帧数添加到字典
            for dat4 in data4:  # 开始循环
                res = conv.createCode(f'temp4/{d2rs}/{dat4}')  # 1位图转换到字码
                d3ta.update({str(dat4[:-4]): str(res)})  # 每一帧的字码存储到字典
                del res[:]  # 清空数组
            d2ta = open(f'fc/{d2rs}.fc', 'w')  # 打开文件
            d2ta.write(str(d3ta))  # 写入文件
            d2ta.close()  # 关闭
            d3ta.clear()
            del res[:]  # 清空数组


if __name__ == '__main__':
    try:

        config = readConfiguration()
        print('读取配置...')
        ver = config['ver']
        print(f'欢迎使用ESP32 P2layer 视频转换工具(彩色视频专用)>>当前版本{ver}')
        print('Powered by iCOMgx\'s Atai')
        print('bilibili:https://space.bilibili.com/23106193 ||github:https://github.com/icomgx')
        time.sleep(1)
        createTempFolder()
        print('创建临时文件夹...')
        print('开始切片视频...')
        startVideoCut(
            video_src_path=config['video_path'],
            frame_height=int(config['frame_height']),
            frame_width=int(config['frame_width']),
            interval=int(config['frame_sampling'])
        )
        print('开始处理帧...')
        frameProcess()
        print('删除临时文件...')
        removeTempFolder()
        print('转换完成请查看/fc 文件夹下是否生成成功，3秒后退出...')
        time.sleep(3)
    except Exception as ex:
        print(f'发生错误： {ex}')
        print('3秒后退出...')
        time.sleep(3)
