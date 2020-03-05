from main import conv
import socket
import struct
import time
import json
import os

totalTime = 0
avg_frame = 0


# 读取配置文件，返回配置字典对象
def readConfiguration():
    with open("config.json", 'r') as load_f:
        load_dict = json.load(load_f)
        return load_dict


def main(fcFileName, ip, port):

    global totalTime, avg_frame
    # 1. 创建套接字 socket
    tcp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 2. 绑定本地信息 bind
    tcp_server_socket.bind((ip, port))
    # 3. 让默认的套接字由主动变为被动 listen
    tcp_server_socket.listen(128)
    print("启动TCP服务器\r\n" + f'启动在{ip}:{port}上')
    # 4. 等待客户端的链接 accept
    print("等待客户端的链接，可以给ESP32上电了~\r\n")
    new_client_socket, client_addr = tcp_server_socket.accept()
    print(f'当前链接：{client_addr}')
    # 接收客户端发送过来的请求
    # recv_data = new_client_socket.recv(1024)
    # print(recv_data)
    res = conv.flTodic(f'fc/{fcFileName}')  # 读取.fc文件
    fc_len = int(res['fc_len'])  # 获取总帧数
    print(f'文件长度：{fc_len}')
    for dat in range(fc_len):
        start_time = time.perf_counter()
        recv_data = new_client_socket.recv(1024)
        # print(recv_data)
        imageCode = conv.flH2xToList(res[str(dat)])
        # print(imageCode)
        d2ata = struct.pack("%dB" % (len(imageCode)), *imageCode)
        # print(len(d2ata))
        # 回送一部分数据给客户端
        new_client_socket.send(d2ata)
        del imageCode[:]
        end_time = time.perf_counter()
        cost = end_time - start_time
        totalTime += round(cost, 4) * 1000
        avg_frame += round((1000 / (round(cost, 4) * 1000)), 4)
        print(f'传输中：当前{dat}帧/共{fc_len}帧，用时{round(cost,4) * 1000 }ms '
              f'约等于{round((1000 / (round(cost,4) * 1000)), 4)}FPS')
        # 关闭套接字
    new_client_socket.close()
    tcp_server_socket.close()
    print(f'传输完成 共耗时{totalTime}ms|平均帧率{round((avg_frame / fc_len), 2)}FPS')


if __name__ == "__main__":
    try:
        config = readConfiguration()
        ver = config['ver']
        print(f'欢迎使用ESP32 P2layer 播放器>>当前版本{ver}')
        print('Powered by iCOMgx\'s Atai')
        print('bilibili:https://space.bilibili.com/23106193 ||github:https://github.com/icomgx')
        time.sleep(1)
        numList = {}
        fcdata = os.listdir('fc')
        for num in range(len(fcdata)):
            numList.update({str(num): fcdata[num]})
            print(f'序号：{str(num)}>> {numList[str(num)]}')
        inp = input('请选择想要播放的文件 输入序号按回车即可>>>')
        print(f'您选择了序号为 {inp} - {numList[str(inp)]}')
        print('准备播放，读取配置...')
        fcFileName = numList[str(inp)]
        ip = config['host']
        port = config['port']
        main(
            fcFileName=fcFileName,
            ip=ip,
            port=int(port)
        )
        print('传输完成，程序3秒后退出...')
        time.sleep(3)
    except Exception as ex:
        print('发生错误： ' + ex)
        print('程序3秒后退出...')
        time.sleep(3)


