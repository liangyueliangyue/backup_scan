import requests
import json
import time
import os
import base64
import re

api_key = ""  #需要填写自己hunter的api_key，注意：hunter是定期需要更换key的

#颜色渲染
red = "\033[31m"
green = "\033[32m"
white = "\033[37m"

#代理
proxies = {
    "http":None,
    "https":None
}

#异常处理
def request_error(url):
    try:
        r = requests.get(url,proxies=proxies)
        return False
    except Exception as e:
        print("{}{} is error!".format(red,url))
        return True

#文件结果筛选
def checkfile(url_list,file_path):
    print("{}进入筛选模式--------------------------------------------".format(green))
    file_name = "{}/vul.txt".format(file_path)
    with open(file_name,"r",encoding="utf-8") as f:
        body = f.read()
        for i in url_list:
            url = i["url"]
            if body.count(url) > 5:
                file_delete(file_name,url)

#文件结果筛选
def file_delete(file_name,url):
    with open(file_name,"r",encoding="utf-8") as f:
        lines = f.readlines()
    with open(file_name,"w",encoding="utf-8") as f_w:
        for line in lines:
            if url in line:
                continue
            f_w.write(line)


def main():
    yufa = input("请输出你的查询条件(默认已经中国并排除中国香港)：")
    page_size = input("请输入查询条数：")
    page = input("请输入查询页数：")
    search = 'province!="中国香港"&&country="中国"&&{}'.format(yufa)
    search_b64 = base64.b64encode(search.encode("utf-8"))
    search_re = search_b64.decode().replace("/","_").replace("+","-")
    end_time = time.strftime('%Y-%m-%d+%H:%M:%S',time.localtime(time.time()))
    url = "https://hunter.qianxin.com/openApi/search?api-key={}&search={}&page={}&page_size={}&is_web=1&status_code=200&start_time=2020-12-08+00%3A00%3A00&end_time={}".format(api_key,search_re,page,page_size,end_time)
    r = requests.get(url,proxies=proxies)
    path = time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime())
    os.makedirs(path) 
    with open("{}/all.txt".format(path), 'a', encoding='UTF-8') as w:
        w.write("查询语句为: {}  查询条数为{} 查询页数为{}".format(search,page_size,page))
        for i in r.json()['data']['arr']:
            url = i['url']     
            if request_error(url):
                continue
            with open("web.txt", 'r', encoding='UTF-8') as web:
                    webs = web.readlines()
            with open('{}/vul.txt'.format(path),'a',encoding='UTF-8') as vul:
                w.write("\n\n站点: {}\n\n".format(url))
                vul.write("\n\n站点: {}\n\n".format(url))
                for web in webs:
                    web = web.strip()
                    u = url + web
                    try:
                        r2 = requests.get(u,proxies=proxies)
                    except Exception as e:
                        print("{}{} is error!".format(red,u))
                        continue
                    if r2.status_code==200:
                        print("{}url为: {} 状态为: {}".format(green,u,r2.status_code))
                        vul.write("url为: {} 状态为: {}\n".format(u,r2.status_code))
                    else:
                        print("{}url为: {} 状态为: {}".format(white,u,r2.status_code))
                    w.write("url为: {} 状态为: {}\n".format(u,r2.status_code))
    print(r.json()['data']['consume_quota'],r.json()['data']['rest_quota'])
    checkfile(r.json()['data']['arr'],path)

if __name__ == '__main__':  
    main()