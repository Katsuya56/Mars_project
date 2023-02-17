from tkinter import *
import tkinter as tk
import tkinter.filedialog
import numpy as np
import socket
import threading
import time

#データ処理部
class Model:
	def __init__(self) -> None:
		self.commandList = []


	# 選択ボタンに関する処理
	def select_btn_click(self):
		typ = [('テキストファイル','*.txt')] 
		dir = 'C:/Users/Gin/Code/python/Mars_project/'
		filePath = tk.filedialog.askopenfilename(filetypes = typ, initialdir = dir)

		self.commandList.clear()
		with open(filePath) as f:
			for s in f.read().split("\n"):
				self.commandList.append(s)
	
	# 実行ボタンに関する処理
	def entry_btn_click(self):
		# ファイル読み込み
		if len(self.commandList) <= 2: return

		# tello_address = ('192.168.10.1', 8889)
		tello_address = ('192.168.0.106', 8889)
		utf8 = "utf-8"

		# Telloへコマンドを送信するためのソケット作成
		sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP
		sock.bind(("", 8889))  # tello標準の8889ポートと同じに
		# commandコマンドを送信
		sock.sendto("command".encode(utf8), tello_address)
		data, _ = sock.recvfrom(1024)
		print(data)
		
		# 命令の実行
		index = 0 
		while index < len(self.commandList):
			try:
				msg = self.commandList[index]  # コマンド入力
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

			

	def run_order(self):
		index = 0
		while index < len(self.commandList):
			try:
				msg = self.commandList[index]  # コマンド入力
				index = index + 1
		
			# msgが無いとき
				if not msg:
					print("continue...")
					continue
				if "end" in msg:
					print("...")
					self.sock.close()  # 切断
					break
			# コマンド送信
				self.sock.sendto(msg.encode(self.utf8), self.tello_address)
		
				# 時間を取得
				start = time.time()
				# ドローンからの結果を取得
				data, _ = self.sock.recvfrom(1024)
			# コマンド送信してから受信までの時間を表示
				print(msg)
				print(data.decode(self.utf8), f"{time.time()-start:.1f}s\n")
			except KeyboardInterrupt:
				print("...")
				self.sock.close()
				break
	 

#ユーザが見る画面
#Controllerから受けたデータを表示
class View(tk.Frame):
	def __init__(self, parent):
		super().__init__(parent)
		self.parent = parent

		self.parent.title("Drone GUI Test") #ウィンドウタイトル
		self.parent.geometry("1000x500")    #ウィンドウサイズ（横x縦）
		
		# ファイル選択用ボタン
		self.select_btn = tk.Button(text="Select")
		self.select_btn.place(x=400, y=470)

		# 実行用ボタン
		self.enter_btn = tk.Button(text="Start")
		self.enter_btn.place(x=500, y=470)
		

#ModelとViewの仲介役
class Controller:
	def __init__(self, root) -> None:

		self.view = View(root)
		self.model = Model()

		#ボタンのイベント
		self.view.select_btn.config(command=self.model.select_btn_click)
		self.view.enter_btn.config(command=self.model.entry_btn_click)


if __name__ == "__main__":
	root = tk.Tk()
	app = Controller(root)	
	root.mainloop()
