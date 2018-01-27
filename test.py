# coding: utf-8
## coding by Synsis [https://github.com/synsis]
## 27/01/2008
import time
import json
import requests
import sys
from PIL import Image
from urllib.parse import quote
import pyscreenshot as ImageGrab
from aip import AipOcr
##import webbrowser

##baidu ocr 自己注册填写
APP_ID = ''
API_KEY = ''
SECRET_KEY = ''

picPath=r"snap.jpg"
picPath2=r"sample.png"
chrome_path = r"tools\chromedriver.exe"


def snap_pic(tmp):
    ##截图像素坐标自己定义，以在全屏幕的像素位置为基准
    pic=ImageGrab.grab(bbox=(1406,75,1896,940))
    pic.save('snap.jpg')
    print("......................截图成功......................\n")
    if(tmp==2):
        analyse_pic(picPath)
    elif(tmp==1):
        rr=0
        gg=0
        bb=0
        r,g,b = pic.getpixel((50,95)) #要识别像素的坐标
        rr=rr+r
        gg=gg+g
        bb=bb+b
        r,g,b = pic.getpixel((160,95)) #要识别像素的坐标
        rr=rr+r
        gg=gg+g
        bb=bb+b
        r,g,b = pic.getpixel((335,95)) #要识别像素的坐标
        rr=rr+r
        gg=gg+g
        bb=bb+b
        r,g,b = pic.getpixel((420,95)) #要识别像素的坐标
        rr=rr+r
        gg=gg+g
        bb=bb+b
        sum=(rr+gg+bb)/12
        if (sum>=245):
            analyse_pic(picPath)


def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()

def search_keyword(question, answers):
    header = {
        "User-Agent":
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",
        "Host":
        "www.baidu.com",
        "Cache-Control":
        "no-cache"
    }
    counts = []

    if '不' in question:
        copy_question = question
        question = question.replace('不','')
        url = 'https://www.baidu.com/s?wd=' + quote(question)

        req = requests.get(url=url, headers=header).text
        for i in range(len(answers)):
            counts.append(req.count(answers[i]))
        index = counts.index(min(counts))
        print(str(index) +":"+answers[index] + " --------- " + str(counts[index]))
        sumx=sum(counts)
        print(str(counts[0]/sumx)+'  '+str(counts[1]/sumx)+'  '+str(counts[2]/sumx))
        print('******************************************')

    else:
        url = 'https://www.baidu.com/s?wd=' + quote(question)
        #webbrowser.open(url)
        req = requests.get(url=url, headers=header).text
        for i in range(len(answers)):
            counts.append(req.count(answers[i]))
        index = counts.index(max(counts))

        if (counts[index] == 0):
            print('无结果')
        else:
            print(str(index+1) +":" +answers[index] + " --------- " + str(counts[index]))
            sumx=sum(counts)
            print(str(counts[0]/sumx)+'  '+str(counts[1]/sumx)+'  '+str(counts[2]/sumx))
            print('******************************************')
    time.sleep(5)

def analyse_result(result):
    print("......................题目解析中......................\n")
    question=".......................no quiz......................."
    answers=[]
    flag = 1
    str1=""
    for dic in result["words_result"]:
        str1=str(dic["words"]).replace(' ', '')
        if(str1.find(".")!=-1 and str1.find("?")!=-1 and flag == 1):
            question = str1[str1.find(".") + 1:str1.find("?")]
            flag=3
        elif(str1.find(".")!=-1 and flag == 1):
            question = str1[str1.find(".") + 1:]
            flag=2
        elif (str1.find("?")==-1 and flag == 2):
            question= question+str1
        elif (str1.find("?")!=-1 and flag == 2):
            question= question+str1[:str1.find("?")]
            flag=3
        elif (flag==3):
            answers.append(str1)
            flag=4
        elif (flag==4):
            answers.append(str1)
            flag=5
        elif (flag==5):
            answers.append(str1)
            flag=6
    if(question==".......................no quiz......................."):
        print(question)
    else:
        print("********************问题是：********************")
        print(question)
        print("问题是选项是：")
        for ans in answers:
           print(ans)
        print("************************************************")
        search_keyword(question, answers)

def analyse_pic(myfilePath):
    print("...................百度识图进行中...................\n")
    client = AipOcr(APP_ID, API_KEY, SECRET_KEY)
    client.setConnectionTimeoutInMillis(2000)
    client.setSocketTimeoutInMillis(2000)
    ##读取文件
    image = get_file_content(myfilePath)
    ##调用文中子识别
    result = client.basicGeneral(image)
    analyse_result(result)
    time.sleep(0)

if __name__ == '__main__':
    while(1):
        key = input("\n点击1运行截图以及计算功能，点击2进行百度云功能测试，点击3进行题目提取以及搜索功能测试:")
        if(key.find('1')!=-1):
            key = input("\n你参与的是冲顶大会或百万英雄（按1），其他(按2)，选择其他后需要点击s进行手动截图:")
            if(key.find('1')!=-1):
                while(1):                
                    snap_pic(1)
            elif(key.find('2')!=-1):
                while(1):   
                    key = input()
                    if(key.find('s')!=-1 or key.find('S')!=-1):
                        snap_pic(2)
        elif (key.find('2')!=-1):                                    
            analyse_pic(picPath2)
        elif (key.find('3')!=-1):
            result={'log_id': 1216615976726532686, 'words_result_num': 18, 'words_result': [{'words': '2'}, {'words': '11.《基尔条约》于1814年的今天签订,其中丹麦将哪部分领'}, {'words': '土割让了给了瑞典?'}, {'words': '冰岛'}, {'words': '挪威'}, {'words': '芬 兰'}, {'words': '咕砝子xKO苟利'}, {'words': '切随心XmK2587434'}, {'words': '← Wenwooooa210893210893210893'}, {'words': '已冷风吹不醒的-一我2088785'}, {'words': 'Lim酱5258049'}, {'words': '哎吆珊珊1851525复活复活复活哈哈哈'}, {'words': '法 兰首席摄影师刘亚复活13399935'}, {'words': '林6bV13362636'}, {'words': 'od312'}, {'words': '手机用户99080dLR411339411339411339411339'}, {'words': '2山有木兮木有枝。0Ug鹿晗老婆复制7937712,可以复活'}, {'words': '北悲1128361'}]};
            analyse_result(result)
