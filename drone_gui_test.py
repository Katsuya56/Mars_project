import tkinter as tk
from PIL import ImageTk, Image
import numpy as np
import tkinter.messagebox

#データ処理部
class Model:
    def __init__(self) -> None:
        self.posX = tk.IntVar() #Widget変数でラベルと連動させる
        self.posY = tk.IntVar()
        self.posX.set(0)
        self.posY.set(0)
        self.pos = tk.StringVar() #Widget変数
        self.posList = []
        self.degList = []
        self.lenList = []
        self.commandList = []
        self.origin = tk.IntVar()
        self.entry_cnt = 0

        self.originVec = [ [0, 1], [0, 1], [0, -1], [0, -1] ]
        self.originPos = [ [0, 0], [900, 0], [0, 360], [900, 360]]
        
        self.radio_click()

    #マウス移動に関する処理
    def mouse_move(self, e):
        self.posX.set(e.x)
        self.posY.set(e.y)
        self.pos.set(f"X:{e.x} Y:{e.y}")

    #マウス左クリック処理
    def mouse_left_click(self, e):
        #登録数に制限かける時
        """if len(self.posList) < 10:"""
        self.posList.append([e.x, e.y])
        print("座標：" + str(self.posList))
        self.vec2deg()
        print("角度：" + str(self.degList))
        self.getLen()
        print("距離：" + str(self.lenList))
        print("")

    #マウス右クリックに関する処理
    def mouse_right_click(self, e):
        if len(self.posList) > 0:
            self.posList.pop()
        print("座標：" + str(self.posList))
        if len(self.degList) > 0:
            self.degList.pop()
        print("角度：" + str(self.degList))
        if len(self.lenList) > 0:
            self.lenList.pop()
        print("距離：" + str(self.lenList))

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
        self.posList.append([0,0])
        print("座標：" + str(self.posList))
        self.vec2deg()
        print("角度：" + str(self.degList))
        self.getLen()
        print("距離：" + str(self.lenList))
        print("")
        self.entry_cnt = self.entry_cnt + 1
        self.commandList.append("takeoff")
        for i in range(len(self.posList)-1):
            if self.degList[i] > 0:
                self.commandList.append(f"cw " + str(int((self.degList[i] * 2 + 1) // 2)))
            else:
                self.commandList.append(f"ccw " + str(int(((-1 * self.degList[i]) * 2 + 1) // 2)))
            self.commandList.append(f"forward " + str(int((self.lenList[i] * 2 + 1) // 2)))
        self.commandList.append("land")

        with open("order{:02}.txt".format(self.entry_cnt),"w") as f:
            for s in self.commandList:
                f.write(s+"\n")
        
    #ラジオボタンに関する処理
    def radio_click(self):
        self.posList.clear()
        self.degList.clear()
        self.lenList.clear()
        self.commandList.clear()
        self.posList.append(self.originPos[self.origin.get()])

        print(self.origin.get())

    #2つのベクトルから角度を求める（0～180度）
    def tanget_angle(self, u: np.ndarray, v:np.ndarray):
        #内積
        i = np.inner(u, v)
        #ベクトルのノルム（長さ）の掛け算
        n = np.linalg.norm(u) * np.linalg.norm(v)
        #内積を長さで割る
        costheta = i / n
        #角度theta（度）
        theta = np.rad2deg( np.arccos(np.clip(costheta, -1.0, 1.0)))
        #print(theta)

        return theta
    
    #最後に打った座標が、ベクトルの左右どちらにあるか調べる
    #vec2がvec1の左だとFalse、右だとTrue
    def getDirection(self, vec1, vec2):
        print( "外積：" + str(np.cross(vec1, vec2)))
        return np.cross(vec1, vec2) > 0
    
    #座標から距離を求める
    def getLen(self):
        a=np.array(self.posList[-2])
        b=np.array(self.posList[-1])
        
        distance=np.linalg.norm(b-a)

        if distance >= 500:
            tkinter.messagebox.showerror("最大値エラー","移動できる最大値を超えています。")
            self.mouse_right_click(None)
            return

        elif distance <= 2:
            tkinter.messagebox.showerror("最小値エラー","移動できる最小値を下回っています。")
            self.mouse_right_click(None)
            return
        
        # print(distance)
        self.lenList.append(distance)

    #座標からベクトルを求め、角度をリストに
    def vec2deg(self):
        #２つのベクトルの初期化
        vec1 = np.array([0, 0])
        vec2 = np.array([0, 0])
        
        
        #角度リストに登録が無いときは仮のベクトルを設定
        if len(self.degList) <= 0:    
            vec1 = np.array(self.originVec[self.origin.get()])
        
        if len(self.posList) == 1: 
            vec2 = np.array(self.posList[0]) - np.array(self.originPos[self.origin.get()]) 
        elif len(self.posList) == 2: 
            # vec1 = np.array(self.posList[0]) - np.array(self.originPos[self.origin.get()])
            vec2 = np.array( self.posList[1] ) - np.array(self.posList[0])
        else:
            vec1 = np.array(self.posList[-2]) - np.array(self.posList[-3])
            vec2 = np.array(self.posList[-1]) - np.array(self.posList[-2])
        
        flag = self.getDirection(vec1, vec2)
        self.degList.append( self.tanget_angle(vec1, vec2) if flag else -self.tanget_angle(vec1, vec2) )
        

#ユーザが見る画面
#Controllerから受けたデータを表示
class View(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        self.parent.title("Drone GUI Test") #ウィンドウタイトル
        self.parent.geometry("1000x500")    #ウィンドウサイズ（横x縦）
        
        #マウスポジション表示用
        self.pos_label = tk.Label(self)
        self.pos_label.pack()
        self.pack()

        #ラジオボタン表示用
        self.radio_lefttop = tk.Radiobutton(
            self,
            text="左上(LeftTop)",
            value=0
        )
        self.radio_lefttop.pack(padx=20, side="left")

        self.radio_righttop = tk.Radiobutton(
            self,
            text="右上(RightTop)",
            value=1
        )
        self.radio_righttop.pack(padx=20, side="left")

        self.radio_leftbottom = tk.Radiobutton(
            self,
            text="左下(LeftBottom)",
            value=2
        )
        self.radio_leftbottom.pack(padx=20, side="left")

        self.radio_rightbottom = tk.Radiobutton(
            self,
            text="右下(LeftBottom)",
            value=3
        )
        self.radio_rightbottom.pack(padx=20, side="left")

        self.ids = []

        #画像表示のためのCanvas
        self.canvas = tk.Canvas(
            self.parent,
            width=900,
            height=360,
            bg = "cyan",
            highlightthickness=0
        )
        self.canvas.place(x=50, y=100)

        #画像を開く
        self.map_image = ImageTk.PhotoImage(file="map.png")
        self.update() #画面情報を更新
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        #画像の描画
        self.canvas.create_image(
            canvas_width/2,
            canvas_height/2,
            image=self.map_image
        )

        #クリック情報削除用のボタン
        self.reset_btn = tk.Button(text="Reset")
        self.reset_btn.place(x=400, y=470)

        #決定ボタン
        self.enter_btn = tk.Button(text="Entry")
        self.enter_btn.place(x=500, y=470)

        #ラジオボタンの基準位置
        self.originPos = [ [0, 0], [900, 0], [0, 360], [900, 360]]
        self.radioID = self.canvas.create_oval(
             -10, -10, 10, 10, fill="red"
        )
        
    def setOrigin(self, origin):        
        self.origin = origin

    def mouse_click(self, e, posList):
        for id in self.ids:
            self.canvas.delete(id)
        self.ids.clear()
        
        for pos in posList:
            width, height = 5, 5           
            id = self.canvas.create_oval(pos[0] - width, pos[1]-height, pos[0]+width, pos[1]+height, fill="red")
            self.ids.append(id)
    
    def point_delete(self):
        for id in self.ids:
            self.canvas.delete(id)
        self.ids.clear()
        

        
    def radio_click(self):
        self.canvas.delete(self.radioID)
        self.point_delete()
        num = self.origin.get()
        width, height = 10, 10
        self.radioID = self.canvas.create_oval(
            self.originPos[num][0] - width,
            self.originPos[num][1] - height,
            self.originPos[num][0] + width,
            self.originPos[num][1] + height,
            fill="red"
        )
        

#ModelとViewの仲介役
class Controller:
    def __init__(self, root) -> None:

        self.view = View(root)
        self.model = Model()

        #Binding
        #マウス位置情報をViewに伝える
        self.view.pos_label.config(textvariable=self.model.pos) #wiget変数を指定
        #ラジオボタン
        self.view.radio_lefttop.config(variable=self.model.origin)
        self.view.radio_righttop.config(variable=self.model.origin)
        self.view.radio_leftbottom.config(variable=self.model.origin)
        self.view.radio_rightbottom.config(variable=self.model.origin)
        self.view.setOrigin(self.model.origin)

        #Callback
        #マウスのイベント
        self.view.canvas.bind("<Motion>", self.model.mouse_move)
        
        self.view.canvas.bind("<Button-1>", self.model.mouse_left_click )
        self.view.canvas.bind("<Button-1>", lambda e : self.view.mouse_click(e, self.model.posList), "+" )
        
        self.view.canvas.bind("<Button-3>", self.model.mouse_right_click)
        self.view.canvas.bind("<Button-3>", lambda e : self.view.mouse_click(e, self.model.posList), "+" )

        #ボタンのイベント
        self.view.reset_btn.config(command=lambda :[self.model.reset_btn_click(),self.view.point_delete(),self.view.radio_click()])
        self.view.enter_btn.config(command=self.model.entry_btn_click)

        #ラジオボタンのイベント(無理やり2つのメソッドを紐づけ)
        self.view.radio_lefttop.config(command= self.radio_click)
        self.view.radio_righttop.config(command= self.radio_click)
        self.view.radio_leftbottom.config(command= self.radio_click)
        self.view.radio_rightbottom.config(command= self.radio_click)
    
    def radio_click(self):
        self.model.radio_click()
        self.view.radio_click()


if __name__ == "__main__":
    root = tk.Tk()
    app = Controller(root)
    
    root.mainloop()

"""
1行目：座標
2行目：ベクトルの外積(すごい簡単に書くと1つ前に設定した座標とその時設定した座標の方向の左側だとマイナス、右側だとプラスになる)※尚、初期値はマップの上だと下向き、マップの下だと上向き
3行目：角度(左下からだとマイナスが反時計回りでプラスが時計回り)
"""