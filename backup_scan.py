import requests
import json
import time
import os
import base64
import re


#命令行颜色
red = "\033[31m"
green = "\033[32m"
white = "\033[37m"

#配置信息
api_key = ""  #自己hunter的apikey


#代理
proxies = {
    "http":None,
    "https":None
}

#异常请求处理
def request_error(type,url):
    try:
        r = requests.get(url,proxies=proxies)
        return r
    except Exception as e:
        if type==1:
            print("{}站点：{} is error!".format(red,url))
        elif type==2:
            print("\t{}{} is error!".format(red,url))
        return False


#筛选
def file_delete(file_name,urls):
    for url in urls:
        with open(file_name,"r",encoding="utf-8") as f:
            lines = f.readlines()
        with open(file_name,"w",encoding="utf-8") as f_w:
            for line in lines:
                if url in line:
                    continue
                f_w.write(line)


def main():
    #输入信息
    yufa = input("请输出你的查询条件(默认已经中国并排除中国香港)：")
    page_size = input("请输入查询条数：")
    page = input("请输入查询页数：")

    #hunter-api调用
    search = 'province!="中国香港"&&country="中国"&&{}'.format(yufa)
    search_b64 = base64.b64encode(search.encode("utf-8"))
    search_re = search_b64.decode().replace("/","_").replace("+","-")
    end_time = time.strftime('%Y-%m-%d+%H:%M:%S',time.localtime(time.time()))
    url = "https://hunter.qianxin.com/openApi/search?api-key={}&search={}&page={}&page_size={}&is_web=1&status_code=200&start_time=2020-12-08+00%3A00%3A00&end_time={}".format(api_key,search_re,page,page_size,end_time)
    path = time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime())
    os.makedirs(path) 

    #开始
    r = requests.get(url,proxies=proxies)
    with open("{}/info.txt".format(path), 'a', encoding='UTF-8') as w:
        w.write("查询语句为: {}  查询条数为{} 查询页数为{}\n".format(search,page_size,page)+r.json()['data']['consume_quota']+r.json()['data']['rest_quota'])
        error_urls = []
        for i in r.json()['data']['arr']:
            url = i['url']     
            if (request_error(1,url)==False):
                continue
            with open("web.txt", 'r', encoding='UTF-8') as web:
                    webs = web.readlines()
            with open('{}/vul.txt'.format(path),'a',encoding='UTF-8') as vul:
                print("{}站点: {}".format(white,url))
                vul.write("\n站点: {}\n".format(url))
                index = 0
                for web in webs:
                    u = url + web.strip()
                    r2 = request_error(2,u)
                    if(r2==False):
                        continue
                    if r2.status_code==200:
                        index += 1
                        if(index > 5):
                            error_urls.append(url)
                            print("\t{}{} I can't Scan!!!!".format(red,url))
                            break
                        else:
                            print("\t{}url为: {} 状态为: {}".format(green,u,r2.status_code))
                            vul.write("\turl为: {} 状态为: {}\n".format(u,r2.status_code))
        file_delete('{}/vul.txt'.format(path),error_urls)

if __name__ == '__main__':  
    main()
