#coding:UTF-8
import time
import requests
from  datetime import datetime
from tkinter import messagebox
import webbrowser
from os import system
import threading

def timeupdate():
    while True:
        current_time = time.strftime("%H:%M:%S", time.localtime())
        system("title PlayerLib-build：082323" + "     " + current_time)
thread = threading.Thread(target=timeupdate)
thread.start()

#欢迎语
print("欢迎使用PlayerLib！")

#公告
messagebox.showinfo("公告", """        欢迎使用PlayerLib!
        Made By AlexBlock
        初次使用请在【https://developer.hypixel.net/】申请Apikey
        
        更新日志：
        082123 发布
        082223 加入FKDR/在线状态等 
        082323 优化key保存系统的沟矢逻辑 修复无rank导致的诡异报错""")

#key保存系统
try:
    with open('key.txt', 'r') as file:
        file_api = file.read()
    if file_api:
        print("检测到历史key,自动填入:", file_api)
    else:
        yes_or_no = messagebox.askquestion("Nope!", """没有找到储存的ApiKey!
是否打开developer.hypixel.net获取key？""")
        if yes_or_no == "yes":
            print("正在开启浏览器页面")
            webbrowser.open('https://developer.hypixel.net/')
        write = input('未找到储存的key，请输入：')
        with open('key.txt', 'w') as file:
            file.write(write)
            print('已保存newkey')
            file_api = file.read()
except FileNotFoundError:
    print("未找到key.txt,以为您自动创建！")
    file = open("key.txt", "w")
    write = input('请输入ApiKey：')
    with open('key.txt', 'w') as file:
        file.write(write)
        print('已保存newkey，请重启程序！')


while True:

#输入玩家名&key
    game_name = input("输入要查询的玩家名：")
    api_key = file_api

#转换uuid
    back_uuid_data = requests.get(f"https://api.mojang.com/users/profiles/minecraft/{game_name}")
    back_uuid = back_uuid_data.json()
    player_uuid = back_uuid["id"]
    print("BackPlayerUUID：" + player_uuid)

# 设置要请求的API接口
    api_url = "https://api.hypixel.net/player"
    api_url2 = "https://api.hypixel.net/status"
    api_url3 = "https://api.hypixel.net/recentgames"

#构建请求参数
    request = {
        "key": api_key,
        "uuid": player_uuid
    }

#发送请求，获取API响应
    response = requests.get(api_url,  params=request)
    response2 = requests.get(api_url2,  params=request)

#解析API的响应
    back_data = response.json()
    back_data2 = response2.json()

    print('收到服务器响应')

    if back_data["success"] == True:
        if "newPackageRank" in back_data["player"]:
            a = back_data["player"]["newPackageRank"]
        else:
            a = "Normal"
        print("PlayerNmae|游戏昵称：", back_data["player"]["displayname"])
        print("Rank|会员等级：", a)
        print("BadWarsLevel|起床等级：", back_data["player"]["achievements"]["bedwars_level"])
        print("Wins|胜场：", back_data["player"]["achievements"]["bedwars_wins"])
        print("Loser|变成膀胱者次数：", back_data["player"]["stats"]["Bedwars"]["losses_bedwars"])
        print("WLR|输赢比：", back_data["player"]["stats"]["Bedwars"]["wins_bedwars"] / back_data["player"]["stats"]["Bedwars"]["losses_bedwars"])
        print("LostBeds|被偷家次数：", back_data["player"]["stats"]["Bedwars"]["beds_lost_bedwars"])
        print("BadWarsKills|起床击杀：", back_data["player"]["stats"]["Bedwars"]["kills_bedwars"])
        print("BedWarsDeaths|起床死亡：", back_data["player"]["stats"]["Bedwars"]["deaths_bedwars"])
        print("Kill/Death|死亡击杀比：：", back_data["player"]["stats"]["Bedwars"]["kills_bedwars"] / back_data["player"]["stats"]["Bedwars"]["deaths_bedwars"])
        print("LostBeds|被偷家次数：", back_data["player"]["stats"]["Bedwars"]["beds_lost_bedwars"])
        print("LostBeds|被偷家次数：", back_data["player"]["stats"]["Bedwars"]["beds_lost_bedwars"])
        print("FinalKill|最终击杀：", back_data["player"]["stats"]["Bedwars"]["final_kills_bedwars"])
        print("FinalDeath|最终死亡：", back_data["player"]["stats"]["Bedwars"]["final_deaths_bedwars"])
        print("FKDR|技术玩家排行榜：", back_data["player"]["stats"]["Bedwars"]["final_kills_bedwars"] / back_data["player"]["stats"]["Bedwars"]["final_deaths_bedwars"])

        print("OnlineStatus|当前在线：", back_data2["session"]["online"])

        print("[" + datetime.now().strftime("%H:%M:%S") + "]" + "查询成功!")
    else:
        print("查询失败")