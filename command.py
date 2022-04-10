from distutils.version import StrictVersion
from email.message import Message
from posixpath import dirname
from shutil import rmtree
from struct import unpack
from turtle import back
from wxEventBT import *
from wx import *
from wx.adv import *
from wx.lib.dialogs import *
from yaml import *
from subprocess import Popen, run
from sys import exit
from os import path
from urllib.request import *
from threading import *
#from simpleaudio import *
from webbrowser import open_new, open_new_tab
from time import *
import re
from datetime import datetime
from plyer import notification
import traceback
from json import *
from requests import *
import pyperclip
from mcipc.rcon.je import Client
from pystray import Icon, MenuItem, Menu
from PIL import Image
from shutil import unpack_archive

#Command

class Command:
    def __init__(self, master):

        self.master = master
        self.config = '.\\files\\config.yml'

    def Quit(self, e):
        exit()

    def Start(self, e):
        
        #例外処理(addres)
        def address():
            try:
                url = "http://localhost:4040/api/tunnels"
                response = Session().get(url)
                jsonData = loads(response.text)
                print(jsonData['tunnels'][0]['public_url'])
                pyperclip.copy(jsonData['tunnels'][0]['public_url'])
                notification.notify(
                    title="ngrokアドレス",
                    message="アドレスをコピーしました。",
                    app_name="sabatate3! wx edition",
                    app_icon=".\\files\\icon.ico",
                    timeout=10
                )
            except:
                MessageDialog(self.master, traceback.format_exc(), 'エラー(adress)', style=ICON_ERROR).ShowModal()
        
        def controle():
            
            self.master.Hide()

            def serverquit():
                with Client('127.0.0.1', 25575, passwd='sabatate') as client:
                    log = client.stop()
                    print(log)
                run("taskkill /f /im ngrok.exe")
                self.master.Show()
                icon.stop()
            
            try:
                menu = Menu(MenuItem('サーバー終了', lambda: serverquit()))
                icon = Icon(name='sabatate3!', title='sabatate3!', icon=Image.open("files\\icon.ico"), menu=menu)
                icon.run()
            except:
                MessageDialog(self.master, traceback.format_exc(), 'エラー(CTRL)', style=ICON_ERROR).ShowModal()
            

        #例外処理(ngrok)
        try:
            with open(self.config, 'r') as f:
                data = safe_load(f)['option']
                Popen(f'{data["ngrokpath"]} tcp 25565 --region {data["region"]}')
        except:
            MessageDialog(self.master, traceback.format_exc(), 'エラー(ngrok)', style=ICON_ERROR).ShowModal()

        Thread(target=address).start()
        Thread(target=controle).start()

        #例外処理(server)
        try:
            with open(self.config, 'r') as f:
                data = safe_load(f)['option']
                Popen(f'{data["runtime"]} -jar {data["serverpath"]}',cwd=path.dirname(data["serverpath"]))
        except:
            MessageDialog(self.master, traceback.format_exc(), 'エラー(server)', style=ICON_ERROR)
        
        
    def Setting(self, e):
        #設定ファイルに書き込み
        def save(e):
            with open(self.config,mode='w') as yaml_file:
                ngpt = ngp.GetValue()
                svpt = svp.GetValue()
                ncbt = ncb.GetStringSelection()
                jvpt = jvp.GetValue()
                bkpt = bkp.GetValue()

                data = {'option': {
                    'ngrokpath':f'{ngpt}',
                    'serverpath':f'{svpt}',
                    'region':f'{ncbt}',
                    'runtime':f'{jvpt}',
                    'backups':f'{bkpt}'
                }}
                safe_dump(data, yaml_file)

            #サーバーの設定の調整
            if not svp.GetValue() == "":
                with open(f'{path.dirname(svpt)}/server.properties',mode='r') as f:
                    text = f.read()

                with open(f'{path.dirname(svpt)}/server.properties', 'w') as f:
                    text = text.replace('enable-rcon=false','enable-rcon=true')
                    if not 'rcon.password=sabatate' in text:
                        text = text.replace('rcon.password=','rcon.password=sabatate')
                    f.write(text)

            SettingDialog.Destroy()
        
        #ngrokのファイルの参照
        def ngrok_path(e):
            filter = "実行ファイル(*.exe) | *.exe | すべてのファイル(*.*) | *.*"
            pdd = FileDialog(SettingDialog, u"ファイルを選択してください")
            pdd.ShowModal()
            ngp.SetValue(pdd.GetPath())

        #server.jarのファイルの参照
        def server_path(e):
            filter = "Javaアーカイブ(*.jar) | *.jar | すべてのファイル(*.*) | *.*"
            pdd = FileDialog(SettingDialog, u"ファイルを選択してください")
            pdd.ShowModal()
            svp.SetValue(pdd.GetPath())

        #javaのファイルの参照
        def java_path(e):
            filter = "実行ファイル(*.exe) | *.exe | すべてのファイル(*.*) | *.*"
            pdd = FileDialog(SettingDialog, u"ファイルを選択してください")
            pdd.ShowModal()
            jvp.SetValue(pdd.GetPath())

        #バックアップのフォルダの参照
        def backup_path(e):
            pdd = DirDialog(SettingDialog, u"フォルダを選択してください")
            pdd.ShowModal()
            bkp.SetValue(pdd.GetPath())

        #設定のリセット
        def reset(e):
            ngp.SetValue("")
            svp.SetValue("")
            jvp.SetValue("")
            bkp.SetValue("")
            ncb.SetSelection(0)
            with open(self.config,mode='w') as yaml_file:
                data = {'option': {
                    'ngrokpath':'',
                    'serverpath':'',
                    'region':'us',
                    'runtime':'',
                    'backups':''
                }}
                safe_dump(data, yaml_file)

        def load():
            with open(self.config, 'r') as f:
                data = safe_load(f)
                #print(str(data['option']['ngrokpath']))

                ngp.SetValue(data['option']['ngrokpath'])
                svp.SetValue(data['option']['serverpath'])
                jvp.SetValue(data['option']['runtime'])
                bkp.SetValue(data['option']['backups'])
                ncb.SetStringSelection(data['option']['region'])


        #create gridbagsizer
        gbs = GridBagSizer()
        
        #create dialog
        SettingDialog = Dialog(self.master, ID_ANY, "サーバー作成", size=(360, 215))
        SettingDialog.Bind(EVT_CLOSE, save)
        
        #ngrok path
        lb1 = StaticText(SettingDialog, ID_ANY, "Ngrokのパス")
        ngp = TextCtrl(SettingDialog, ID_ANY)
        eb1 = EventBT(SettingDialog, ID_ANY, "参照", ngrok_path)

        #server.jar path
        lb2 = StaticText(SettingDialog, ID_ANY, "server.jarのパス")
        svp = TextCtrl(SettingDialog, ID_ANY)
        eb2 = EventBT(SettingDialog, ID_ANY, "参照", server_path)

        #ngrok server select
        varray = ('us','eu','ap','au','sa','jp','in')
        lb3 = StaticText(SettingDialog, ID_ANY, "ngrokのサーバー")
        ncb = ComboBox(SettingDialog, ID_ANY, "選択してください", choices=varray, style=CB_READONLY)
        
        #java path
        lb4 = StaticText(SettingDialog, ID_ANY, "Javaランタイム")
        jvp = TextCtrl(SettingDialog, ID_ANY)
        eb3 = EventBT(SettingDialog, ID_ANY, "参照", java_path)

        #backup path
        lb5 = StaticText(SettingDialog, ID_ANY, "バックアップの保存先")
        bkp = TextCtrl(SettingDialog, ID_ANY)
        eb5 = EventBT(SettingDialog, ID_ANY, "参照", backup_path)

        #ok reset
        eb6 = EventBT(SettingDialog, ID_ANY, "OK", save)
        eb7 = EventBT(SettingDialog, ID_ANY, "RESET", reset)

        #widget add for sizer
        gbs.Add(lb1, (0,0), (1,1), flag=EXPAND | ALL, border=3)
        gbs.Add(ngp, (0,1), (1,3), flag=EXPAND | ALL, border=3)
        gbs.Add(eb1, (0,4), (1,1), flag=EXPAND | ALL, border=3)

        gbs.Add(lb2, (1,0), (1,1), flag=EXPAND | ALL, border=3)
        gbs.Add(svp, (1,1), (1,3), flag=EXPAND | ALL, border=3)
        gbs.Add(eb2, (1,4), (1,1), flag=EXPAND | ALL, border=3)

        gbs.Add(lb3, (2,0), (1,1), flag=EXPAND | ALL, border=3)
        gbs.Add(ncb, (2,1), (1,3), flag=EXPAND | ALL, border=3)

        gbs.Add(lb4, (3,0), (1,1), flag=EXPAND | ALL, border=3)
        gbs.Add(jvp, (3,1), (1,3), flag=EXPAND | ALL, border=3)
        gbs.Add(eb3, (3,4), (1,1), flag=EXPAND | ALL, border=3)

        gbs.Add(lb5, (4,0), (1,1), flag=EXPAND | ALL, border=3)
        gbs.Add(bkp, (4,1), (1,3), flag=EXPAND | ALL, border=3)
        gbs.Add(eb5, (4,4), (1,1), flag=EXPAND | ALL, border=3)

        gbs.Add(eb6, (5,4), (1,1), flag=EXPAND | ALL, border=3)
        gbs.Add(eb7, (5,3), (1,1), flag=EXPAND | ALL, border=3)

        #設定ファイルをロードする
        load()

        #ダイアログにSizerをセット
        SettingDialog.SetSizer(gbs)

        #ダイアログをモーダルとして表示
        SettingDialog.ShowModal()
    
    def Create(self, e):
        
        #次の処理
        def next_run(e):
            
            #別スレッドでセットアップ
            def run_thread():

                #ダウンロードの割合の計算と更新
                def up(block_count,block_size,total_size):
                    parsent = int(100*block_count*block_size/total_size)
                    Dwndialog.Update(value=parsent, newmsg=f"現在{parsent}%ダウンロード完了しました")
                    return

                #サーバー作成
                path2 = path.GetValue()
                try:

                    #バージョンによる条件分岐
                    if drp.GetStringSelection() == '1.18.2':
                        urlretrieve('https://launcher.mojang.com/v1/objects/c8f83c5655308435b3dcf03c06d9fe8740a77469/server.jar',f'{path2}/server.jar',reporthook=up)
                        print("download")
                    elif drp.GetStringSelection() == '1.18.1':
                        urlretrieve('https://launcher.mojang.com/v1/objects/125e5adf40c659fd3bce3e66e67a16bb49ecc1b9/server.jar',f'{path2}/server.jar',reporthook=up)
                        print("download")
                    elif drp.GetStringSelection() == '1.17.1':
                        urlretrieve('https://launcher.mojang.com/v1/objects/a16d67e5807f57fc4e550299cf20226194497dc2/server.jar',f'{path2}/server.jar',reporthook=up)
                        print("download")                   
                    elif drp.GetStringSelection() == '1.16.5':
                        urlretrieve('https://launcher.mojang.com/v1/objects/1b557e7b033b583cd9f66746b7a9ab1ec1673ced/server.jar',f'{path2}/server.jar',reporthook=up)
                        print("download")
                    elif drp.GetStringSelection() == '1.15.2':
                        urlretrieve('https://launcher.mojang.com/v1/objects/bb2b6b1aefcd70dfd1892149ac3a215f6c636b07/server.jar',f'{path2}/server.jar',reporthook=up)
                        print("download")
                    elif drp.GetStringSelection() == '1.14.4':
                        urlretrieve('https://launcher.mojang.com/v1/objects/3dc3d84a581f14691199cf6831b71ed1296a9fdf/server.jar',f'{path2}/server.jar',reporthook=up)
                        print("download")
                    elif drp.GetStringSelection() == '1.13.2':
                        urlretrieve('https://launcher.mojang.com/v1/objects/3737db93722a9e39eeada7c27e7aca28b144ffa7/server.jar',f'{path2}/server.jar',reporthook=up)
                        print("download")
                    elif drp.GetStringSelection() == '1.12.2':
                        urlretrieve('https://launcher.mojang.com/v1/objects/886945bfb2b978778c3a0288fd7fab09d315b25f/server.jar',f'{path2}/server.jar',reporthook=up)
                        print("download")
                    
                    #プログレスバーのスタイルの変更
                    Dwndialog.Update(100, newmsg="サーバーの構築中")
                    Dwndialog.Pulse()
                    
                    #設定ファイルを読み込む
                    with open(self.config, 'r') as f:
                        data = safe_load(f)
                        data = data['option']['runtime']

                    #サーバーの実行
                    run(f'{data} -jar {path2}/server.jar',cwd=path2)
                    
                    Dwndialog.Update(100, newmsg="eulaファイルの変更")

                    #ユーザーライセンス条約の同意
                    with open(f'{path2}/eula.txt',mode='r') as f:
                        text = f.read()

                    with open(f'{path2}/eula.txt', 'w') as f:
                        f.write(text.replace('false','true'))

                    Dwndialog.Update(100, newmsg="設定ファイルの更新中")

                    with open(f'{path2}/server.properties',mode='r') as f:
                        text = f.read()

                    with open(f'{path2}/server.properties', 'w') as f:
                        text = text.replace('enable-rcon=false','enable-rcon=true')
                        if not 'rcon.password=sabatate' in text:
                            text = text.replace('rcon.password=','rcon.password=sabatate')
                        f.write(text)
                    
                    #設定ファイルにサーバーの場所を保存
                    with open(self.config, 'r') as f:
                        data = safe_load(f)
                    
                    with open(self.config, 'w') as f:
                        data["option"]["serverpath"] = path2+'\\server.jar'
                        safe_dump(data, f)

                    #メッセージダイアログ
                    MessageDialog(Dwndialog, 'サーバーの作成が正常に終了ました', '完了').ShowModal()

                    #終了
                    print("destory")
                    Dwndialog.Destroy()
                    self.Dcreate.Destroy()

                except:
                    print(traceback.format_exc())

            #値の検査
            if not path.GetValue() == "" and ckb.IsChecked() == True and not drp.GetStringSelection() == "":
                #プログレスダイアログの作成
                Dwndialog = ProgressDialog(title="サーバーの作成中", message="現在0%ダウンロードしました", maximum=102, style=PD_CAN_ABORT | PD_REMAINING_TIME)
                #別スレッドでダウンロードとセットアップ
                Thread(target=run_thread).start()

            #入力されていない項目に関するエラーの表示
            else:
                erdialog = MessageDialog(self.Dcreate, "入力されていない項目があります", "エラー", style=OK | ICON_ERROR)
                erdialog.ShowModal()

        #キャンセル
        def cancel(e):
            self.Dcreate.Destroy()

        #フォルダを参照
        def DirSelect(e):
            self.pdd = DirDialog(self.Dcreate, u"フォルダを選択してください")
            self.pdd.ShowModal()
            path.SetValue(self.pdd.GetPath())

        #OKボタンの有効か無効かの管理
        def update():
            try:
                if ckb.IsChecked() == True and not path.GetValue() == '':
                    btnOk.Enable()
                else:
                    btnOk.Disable()
                self.Dcreate.Refresh()
                CallLater(100*5, update)
            except:
                pass

        #Dialog Server Create
        self.Dcreate = Dialog(self.master, ID_ANY, "サーバー作成", size=(530,140))

        gsz = GridBagSizer()

        #Path Label
        lb1 = StaticText(self.Dcreate, ID_ANY, "サーバーを作成するパス")

        #Path TextCtrl
        path = TextCtrl(self.Dcreate, ID_ANY)

        #Path file dialog
        pbd = EventBT(self.Dcreate, ID_ANY, "参照", DirSelect)

        #Userlicence
        ckb = CheckBox(self.Dcreate, ID_ANY, "MOJANGの")
        lb2 = HyperlinkCtrl(self.Dcreate, ID_ANY, "エンドユーザーライセンス条項", "https://account.mojang.com/documents/minecraft_eula")
        lb3 = StaticText(self.Dcreate, ID_ANY, "を読み、ライセンス条約に同意しました。")

        #Server version
        varray = ("1.18.2", "1.18.1", "1.17.1", "1.16.5", "1.15.2", "1.14.4", "1.13.2", "1.12.2")
        lb4 = StaticText(self.Dcreate, ID_ANY, "サーバーバージョン: ")
        drp = ComboBox(self.Dcreate, ID_ANY, "選択してください", choices=varray, style=CB_READONLY)

        #EventButton
        btnOk = EventBT(self.Dcreate, ID_ANY, "次へ", next_run)
        btnCancel = EventBT(self.Dcreate, ID_ANY, "キャンセル", cancel)

        #wedget Add
        gsz.Add(lb1, (0,0), (1,1), flag=EXPAND | ALL, border=3)
        gsz.Add(path, (0,1), (1,2), flag=EXPAND | ALL, border=3)
        gsz.Add(pbd, (0,3), (1,1), flag=EXPAND | ALL, border=3)
        gsz.Add(ckb, (1,0), (1,1), flag=EXPAND | LEFT, border=35)
        gsz.Add(lb2, (1,1), (1,1), flag=EXPAND)
        gsz.Add(lb3, (1,2), (1,1), flag=EXPAND | RIGHT, border=3)
        gsz.Add(lb4, (2,0), (1,1), flag=EXPAND | ALL, border=3)
        gsz.Add(drp, (2,1), (1,2), flag=EXPAND | ALL, border=3)
        gsz.Add(btnOk, (3, 2), (1,1), flag=EXPAND | ALL, border=3)
        gsz.Add(btnCancel, (3,3), (1,1), flag=EXPAND | ALL, border=3)

        #ボタンの有効無効の管理用関数
        update()

        #ダイアログにSizerをセット
        self.Dcreate.SetSizer(gsz)

        #モーダルとしてダイアログを表示
        self.Dcreate.ShowModal()

    def NgrokSetup(self, e):

        def setup(e):
            #ダウンロードの割合の計算と更新
            def up(block_count,block_size,total_size):
                parsent = int(100*block_count*block_size/total_size)
                Dwndialog.Update(value=parsent, newmsg=f"現在{parsent}%ダウンロード完了しました")
                return
            
            def run_thread():
                pthc = self.pthc.GetValue()

                urlretrieve('https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-windows-amd64.zip',f'{pthc}/ngrok-stable-windows-amd64.zip',reporthook=up)
                
                Dwndialog.Update(100, newmsg="ファイルの解凍中")
                Dwndialog.Pulse()

                unpack_archive(f'{pthc}\\ngrok-stable-windows-amd64.zip', f'{pthc}\\ngrok')
                sleep(0.5)

                Dwndialog.Update(100, newmsg="ファイルの取り出し中")
                Dwndialog.Pulse()

                run(f'move ngrok\\ngrok.exe .\\', cwd=pthc, shell=True)
                run(f'rd ngrok', cwd=pthc, shell=True)
                run(f'del {pthc}\\ngrok-stable-windows-amd64.zip', shell=True)

                Dwndialog.Update(100, newmsg="ngrokの認証中")
                Dwndialog.Pulse()

                run(f'ngrok.exe authtoken {attc.GetValue()}', cwd=pthc)

                Dwndialog.Update(100, newmsg="設定ファイルの更新中")
                Dwndialog.Pulse()

                #設定ファイルにサーバーの場所を保存
                with open(self.config, 'r') as f:
                    data = safe_load(f)
                    
                with open(self.config, 'w') as f:
                    data["option"]["ngrokpath"] = pthc+'\\ngrok.exe'
                    safe_dump(data, f)

                #メッセージダイアログ
                MessageDialog(Dwndialog, 'サーバーの作成が正常に終了ました', '完了').ShowModal()

                Dwndialog.Destroy()

            #ProgressDialog
            Dwndialog = ProgressDialog(title="ngrokのセットアップ中", message="現在0%ダウンロードしました", maximum=102, style=PD_CAN_ABORT | PD_REMAINING_TIME)
            Thread(target=run_thread).start()

        #OKボタンの有効か無効かの管理
        def update():
            try:
                if not attc.GetValue() == '' and not self.pthc.GetValue() == '':
                    nxbt.Enable()
                else:
                    nxbt.Disable()
                Ngstp.Refresh()
                CallLater(100*5, update)
            except:
                pass
        
        def askdir(e):
            pdd = DirDialog(Ngstp, u"フォルダを選択してください")
            pdd.ShowModal()
            self.pthc.SetValue(pdd.GetPath())

        Ngstp = Dialog(self.master, ID_ANY, "ngrokのセットアップ", size=(210,170))
        
        grs = GridBagSizer()
        
        #Path Label
        pthl = StaticText(Ngstp, ID_ANY, "ngrokを保存するパス")

        #Path TextCtrl
        self.pthc = TextCtrl(Ngstp, ID_ANY)

        #Dir ask button
        dirbt = EventBT(Ngstp, ID_ANY, "参照", askdir)

        #AuthToken Label
        attl = StaticText(Ngstp, ID_ANY, "ngrokのトークン")

        #AuthToken TextCtrl
        attc = TextCtrl(Ngstp, ID_ANY)

        #Next Button
        nxbt = EventBT(Ngstp, ID_ANY, "次へ", setup)

        grs.Add(pthl, (0,0), (1,2), flag=EXPAND | ALL, border=3)
        grs.Add(self.pthc, (1,0), (1,1), flag=EXPAND | ALL, border=3)
        grs.Add(dirbt, (1,1), (1,1), flag=EXPAND | ALL, border=3)
        grs.Add(attl, (2,0), (1,2), flag=EXPAND | ALL, border=3)
        grs.Add(attc, (3,0), (1,2), flag=EXPAND | ALL, border=3)
        grs.Add(nxbt, (4,1), (1,1), flag=EXPAND | ALL, border=3)

        Ngstp.SetSizer(grs)

        update()

        Ngstp.ShowModal()

    def Backup(self):
        with open(self.config, "r") as f:
            data = safe_load(f)['option']
            if not data['backups'] == "" and not data['serverpath'] == "":
                run(f"cp {data['serverpath']} {data['backups']}")
                notification.notify(
                    title="サーバーバックアップ",
                    message="サーバーをバックアップしました。",
                    app_name="sabatate3! wx edition",
                    app_icon=".\\files\\icon.ico",
                    timeout=10
                )
            else:
                MessageDialog(self.master, "サーバーパスまたはバックアップパスが設定されていません", "エラー", style=ICON_ERROR).ShowModal()
