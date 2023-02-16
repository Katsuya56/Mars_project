import socket 
import threading 
import cv2 
import time

utf8="utf-8"
sock = socket. socket (socket.AF_INET, socket. SOCK_DGRAM)
sock.bind( ("",8889) )


#データ受け取り用の関数
def udp_receiver():
    while True:
        try:
            data, _ = sock. recvfrom (1024)
            print (data.decode (encoding=utf8))
        except Exception as e:
            print(e)
            break

#Tello の IP とポート
TELLO_IP = "192.168.10.1"
TELLO_PORT = 8889
TELLO_ADDRESS = (TELLO_IP, TELLO_PORT)

#Tello からの映像受信用のローカル IP アドレスとポート
TELLO_CAMERA_ADDRESS = 'udp://@192.168.10.3:11111'

#キャプチャ用オブジェクト
cap = None

#データ受信用オブジェクト
response_obj = None

#受信用スレッドの作成
thread = threading.Thread( target=udp_receiver, args=())
thread.daemon = True
thread.start()

#コマンドモードを送信
sock. sendto('command'. encode(utf8), TELLO_ADDRESS)

time.sleep(1)

#カメラ映像のストリーミング開始
sock.sendto("streamon". encode(utf8), TELLO_ADDRESS)

if cap is None:
    cap = cv2.VideoCapture(TELLO_CAMERA_ADDRESS)

if not cap.isOpened():
    cap.open(TELLO_CAMERA_ADDRESS)

time.sleep(1)


while True:
    ret, frame = cap.read()
    #動画フレームが空ならスキップ
    if frame is None or frame.size == 0:
        continue

    #カメラ映像のサイズを半分にしてウィンドウい表示
    frame_height, frame_width = frame.shape[:2]
    frame = cv2.resize (frame, (int (frame_width/2), int (frame_height /2))
        )

    cv2. imshow ("Tello Camera View", frame)
    
    #q キーで終了
    if cv2.waitKey (1) & 0xFF == ord ('q'):
        break

cap.release()
cv2.destroyAllWindows()

#ビデオストリーミング停止
sock.sendto ("streamoff".encode(utf8),TELLO_ADDRESS)