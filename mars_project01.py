import socket
import threading
import time
# tello_address = ('192.168.0.102', 8889)
tello_address = ('192.168.10.1', 8889)
utf8 = "utf-8"

# Telloへコマンドを送信するためのソケット作成
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP
sock.bind(("", 8889))  # tello標準の8889ポートと同じに
# commandコマンドを送信
sock.sendto("command".encode(utf8), tello_address)
data, _ = sock.recvfrom(1024)
print(data)
# cw 右

order= []
# ファイル読み込み
with open("testorder.txt") as f:
    for s in f.read().split("\n"):
        order.append(s)

# 命令の実行
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
