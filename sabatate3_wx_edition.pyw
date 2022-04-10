from wx import *
from configparser import *
from subprocess import Popen, run
from sys import exit
from os import path, popen
from urllib.request import *
from threading import *
#from simpleaudio import *
from webbrowser import open_new, open_new_tab
from time import *
from re import *
from datetime import datetime
from plyer import *
from wxEventBT import *
import command
from yaml import *

#main window
class Window(Frame):
    
    def __init__(self):

        #setting file
        self.config = '.\\files\\config.yml'

        #main window setting
        super().__init__(None, ID_ANY, 'sabatate3 wx edition', size=(340,190),style=MINIMIZE_BOX | SYSTEM_MENU | CAPTION | CLOSE_BOX | CLIP_CHILDREN)
        
        #set icon
        self.SetIcon(Icon('files\\icon.ico', BITMAP_TYPE_ICO))

        #Commnand.py
        self.cmd = command.Command(self)

        #add widget
        self.widget()

        #add menu
        self.menu()

        #set menu event
        super().Bind(EVT_MENU,self.event)

    def event(self,e):
        eid = e.GetId()
        
        #IDでイベントの分別
        if eid == 1:
            #設定
            self.cmd.Setting(e)
        
        elif eid == 2:
            #終了
            self.cmd.Quit(e)
        
        elif eid == 3:
            #なし
            pass
        
        elif eid == 4:
            #サーバー起動
            self.cmd.Start(e)
        
        elif eid == 5:
            #サーバー新規作成
            self.cmd.Create(e)
        
        elif eid == 6:
            #サーバー設定
            MessageDialog(self, "サーバーの設定は未実装ですｽﾏｿ", "情報")
        
        elif eid == 7:
            #サーバーバックアップ
            self.cmd.Backup()
        
        elif eid == 8:
            #サーバーの場所を開く
            with open(self.config, 'r') as f:
                data = safe_load(f)['option']
                if not data['serverpath'] == "":
                    run(f"explorer {path.dirname(data['serverpath'])}")
                else:
                    MessageDialog(self, "サーバーのパスが設定されていません", "エラー", style=ICON_ERROR).ShowModal()
        
        elif eid == 9:
            #サーバーの設定ファイルを開く
            with open(self.config, 'r') as f:
                data = safe_load(f)['option']
                if not data['serverpath'] == "":
                    run(f"notepad {path.dirname(data['serverpath'])}\\server.properties")
                else:
                    MessageDialog(self, "サーバーのパスが設定されていません", "エラー", style=ICON_ERROR).ShowModal()
        
        elif eid == 10:
            #ngrokのセットアップ
            self.cmd.NgrokSetup(e)
        
        elif eid == 11:
            #ngrokの場所を開く
            with open(self.config, 'r') as f:
                data = safe_load(f)['option']
                if not data['ngrokpath'] == "":
                    run(f"explorer {path.dirname(data['ngrokpath'])}")
                else:
                    MessageDialog(self, "ngrokのパスが設定されていません", "エラー", style=ICON_ERROR).ShowModal()

        elif eid == 12:
            #ngrokダウンロードページ
            open_new_tab("https://ngrok.com/download")
        
        elif eid == 13:
            #java17ダウンロードページ
            open_new_tab("https://www.oracle.com/java/technologies/downloads/#JDK17")
        
        elif eid == 14:
            #java8ダウンロードページ
            open_new_tab("https://java.com/ja/download/")
        
        elif eid == 15:
            #openjdk8ダウンロードページ
            open_new_tab("https://jdk.java.net/jmc/8/")
        
        elif eid == 16:
            #openjdk16ダウンロードページ
            open_new_tab("https://jdk.java.net/java-se-ri/17")
        
        elif eid == 17:
            #openjdk17ダウンロードページ
            open_new_tab("https://jdk.java.net/17/")
        
        elif eid == 18:
            #紹介映像
            MessageDialog(self, "紹介映像は未実装ですｽﾏｿ", "情報")
        
        elif eid == 19:
            #このアプリについて
            dlg = Dialog(self, ID_ANY, "このアプリについて", size=(350, 500))

            box = BoxSizer(VERTICAL)
            
            stx1 = StaticText(dlg, ID_ANY, "SABATATE4 WX EDITION\n")
            stx1.SetFont(Font(20, FONTFAMILY_DEFAULT, FONTSTYLE_NORMAL, FONTWEIGHT_BOLD))

            stx2 = StaticText(dlg, ID_ANY, "Version 4\n")
            stx2.SetFont(Font(10, FONTFAMILY_DEFAULT, FONTSTYLE_NORMAL, FONTWEIGHT_BOLD))

            box.Add(stx1, flag=ALIGN_CENTER)
            box.Add(stx2, flag=ALIGN_CENTER)
            box.Add(StaticText(dlg, ID_ANY, "更新履歴ﾃｷﾄｰ\n", style=TE_LEFT), flag=ALIGN_CENTER)
            box.Add(StaticText(dlg, ID_ANY, "ver1.0 リリース\nver 1.2~2.0 基本機能の追加\nver 2.1 新規サーバーを1.18に対応\nver 2.2 バックアップ機能の追加\nver 2.3 javaランタイムのバグの修正\nver 2.5 modal最新版に対応\nver 3.0 見た目のアップデート\nver 3.1 位置の修正\nver 3.2 バージョン選択機能追加\nver 3.3 リセット機能の追加\nver 3.4 サーバーの場所を開けるように\nver 3.5 1.18.2に対応\nver 3.6 wxに対応\nver 3.7 ngrokのアドレスコピー機能追加\nver 3.8 サーバーの起動した通知領域に移動\nver 3.9 サーバーとngrokを自動で起動できるように\nver 4.0 細かいバグの修正"), flag=ALIGN_CENTER)
            box.Add(StaticText(dlg, ID_ANY, "\n作成者 nanashidesu152&harubocchi0422\n© 2021 harubocchi0422 and nanashidesu152"), flag=ALIGN_CENTER)
            
            dlg.SetSizer(box)

            dlg.ShowModal()

    def menu(self):
        #create menubar
        menu = MenuBar()

        #create menu
        flm = Menu()
        
        #create menu items
        flm.Append(1, '&設定\tCtrl+S')
        flm.AppendSeparator()
        flm.Append(2, '&終了\tCtrl+Q')

        #create menu
        svm = Menu()
        #create submenu items
        sbsv = Menu()
        sbsv.Append(4, "&サーバー起動\tCtrl+Alt+s")
        sbsv.Append(5, "&サーバー新規作成\tCtrl+Alt+m")
        sbsv.Append(6, "&サーバーの設定\tCtrl+Alt+C")
        sbsv.Append(7, "&サーバーのバックアップ\tCtrl+Alt+B")
        sbsv.Append(8, "&サーバーの場所を開く\tCtrl+Alt+F")
        sbsv.Append(9, "&サーバーの設定ファイルを開く\tCtrl+Alt+Shift+F")
        
        sbng = Menu()
        sbng.Append(10, "&ngrokのセットアップ\tCtrl+Alt+N")
        sbng.Append(11, "&ngrokの場所を開く\tCtrl+Alt+Shift+N")
        
        svm.AppendSubMenu(sbsv, "サーバー")
        svm.AppendSubMenu(sbng, "ngrok")
        
        #create menu
        dwm = Menu()
        
        #create menu items
        dwm.Append(12, "ngrokのダウンロードページ")
        dwm.AppendSeparator()
        dwm.Append(13, "java8のダウンロードページ")
        dwm.Append(14, "java17のダウンロードページ")
        dwm.AppendSeparator()
        dwm.Append(15, "openjdk-8のダウンロードページ")
        dwm.Append(16, "openjdk-16のダウンロードページ")
        dwm.Append(17, "openjdk-17のダウンロードページ")

        #create menu
        hlm = Menu()
        
        #create menu items
        hlm.Append(18, "紹介映像を見る")
        hlm.Append(19, "&このアプリについて\tCtrl+H")
        
        #append menu for menubar
        menu.Append(flm, "ファイル(&F)")
        menu.Append(svm, "サーバー(&S)")
        menu.Append(dwm, "ダウンロード(&D)")
        menu.Append(hlm, "ヘルプ(&H)")

        self.Bind(EVT_MENU, self.event)

        #set menubar for frame
        super().SetMenuBar(menu)

    def widget(self):
        #main panel
        mp = Panel(self, ID_ANY)
        mp.SetBackgroundColour('#FFFFFF')

        #grid sizer
        gsz = GridSizer(rows=5, cols=2, gap=(0,0))
        
        #server start
        gsz.Add(EventStyleImageBT(mp, ID_ANY, " 起動", self.cmd.Start, "files\\img\\power.png", style=BU_LEFT), flag=GROW | ALIGN_LEFT | EXPAND | RIGHT, border=5)
        gsz.Add(StaticText(mp, ID_ANY, '設定に基づいて起動します。'), flag=GROW | ALIGN_LEFT | EXPAND | LEFT | RIGHT, border=5)

        #setting
        gsz.Add(EventStyleImageBT(mp, ID_ANY, " 設定", self.cmd.Setting, "files\\img\\setup.png", style=BU_LEFT), flag=GROW | ALIGN_LEFT | EXPAND | RIGHT, border=5)
        gsz.Add(StaticText(mp, ID_ANY, 'sabatate3の設定をします。'), flag=GROW | ALIGN_LEFT | EXPAND | LEFT | RIGHT, border=5)
        
        #create server
        gsz.Add(EventStyleImageBT(mp, ID_ANY, " サーバー新規作成", self.cmd.Create, "files\\img\\server.png", style=BU_LEFT), flag=GROW | ALIGN_LEFT | EXPAND | RIGHT, border=5)
        gsz.Add(StaticText(mp, ID_ANY, 'サーバー新規作成を行います。'), flag=GROW | ALIGN_LEFT | EXPAND | LEFT | RIGHT, border=5)

        #ngrok setup
        gsz.Add(EventStyleImageBT(mp, ID_ANY, " ngrokのセットアップ", self.cmd.NgrokSetup, "files\\img\\ngrok.png", style=BU_LEFT), flag=GROW | ALIGN_LEFT | EXPAND | RIGHT, border=5)
        gsz.Add(StaticText(mp, ID_ANY, 'ngrokのセットアップを行います。'), flag=GROW | ALIGN_LEFT | EXPAND | LEFT | RIGHT, border=5)

        #exit
        gsz.Add(EventStyleImageBT(mp, ID_ANY, " 終了", self.cmd.Quit, "files\\img\\exit.png", style=BU_LEFT), flag=GROW | ALIGN_LEFT | EXPAND | RIGHT, border=5)
        gsz.Add(StaticText(mp, ID_ANY, 'sabatate!3を終了します。'), flag=GROW | ALIGN_LEFT | EXPAND | LEFT | RIGHT, border=5)

        #set sizer for panel
        mp.SetSizer(gsz)


if __name__=='__main__':
    #run
    app = App()
    win = Window()
    win.Show()
    app.MainLoop()