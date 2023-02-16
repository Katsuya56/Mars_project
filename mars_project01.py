import socket
import threading
import time
tello_address = ('192.168.0.102', 8889)
utf8 = "utf-8"
# Telloへコマンドを送信するためのソケット作成
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP
sock.bind(("", 8889))  # tello標準の8889ポートと同じに
# commandコマンドを送信
sock.sendto("command".encode(utf8), tello_address)
data, _ = sock.recvfrom(1024)
print(data)
# print("繰り返しで命令できるように")
# print("移動操作1:takeoff land forward back left right")
# print("移動操作2:up down cw ccw flip speed")
# print("状態確認: speed?height?temp?battery?time?acceleration?attitude?sn?sdk?")
# print("終了:end")

order = ["takeoff",
	"forward 20", "cw 10",
"land"]
index = 0
while index < len(order):
    try:
        # msg = input(">")  # コマンド入力
        msg = order[index]  # コマンド入力
        index = index + 1

    # msgが無いとき
        if not msg:
            print("continue...")
            continue
        if "end" in msg:
            print("...")
            sock.close()  # 切断
            break
    # コマンド送信
        sock.sendto(msg.encode(utf8), tello_address)

        # 時間を取得
        start = time.time()
        # ドローンからの結果を取得
        data, _ = sock.recvfrom(1024)
    # コマンド送信してから受信までの時間を表示
        print(msg)
        print(data.decode(utf8), f"{time.time()-start:.1f}s\n")
    except KeyboardInterrupt:
        print("...")
        sock.close()
        break
