import tkinter as tk
from PIL import ImageTk, Image
import numpy as np
import tkinter.messagebox

#データ処理部
class Model:
	def __init__(self) -> None:
		self.filePath = ""
		self.commandList = []

	#リセットボタンに関する処理
	def reset_btn_click(self):
		self.posList.clear()
		self.degList.clear()
		self.lenList.clear()
		self.commandList.clear()
		self.origin.set(0)
		self.radio_click()
	
	#決定ボタンに関する処理
	def entry_btn_click(self):
		self.entry_cnt = self.entry_cnt + 1
		self.posList.append([0,0])
		self.commandList.append("takeoff")
		for i in range(len(self.posList)-2):
			if self.degList[i] > 0:
				self.commandList.append(f"cw " + str(int((self.degList[i] * 2 + 1) // 2)))
			else:
				self.commandList.append(f"ccw " + str(int(((-1 * self.degList[i]) * 2 + 1) // 2)))
			self.commandList.append(f"forward " + str(int((self.lenList[i] * 2 + 1) // 2)))
		self.commandList.append("land")

		with open("order{:02}.txt".format(self.entry_cnt),"w") as f:
			for s in self.commandList:
				f.write(s+"\n")
	 

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
		self.view.select_btn.config(command=lambda :[self.model.reset_btn_click(),self.view.point_delete(),self.view.radio_click()])
		self.view.enter_btn.config(command=self.model.entry_btn_click)


if __name__ == "__main__":
	root = tk.Tk()
	app = Controller(root)	
	root.mainloop()
