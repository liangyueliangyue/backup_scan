# backup_scan
一个写来自己用的简单备份扫描脚本，大佬勿喷  

1.需要自己在代码里改写api_key为hunter的key  
2.使用的方式是默认已经选择中国并排除中国香港，也就是province!="中国香港"&&country="中国"  
3.后续条件可以自己添加，详情参考hunter语法。查询条数也是根据hunter（只能是10,20,50,100）  
4.扫描会生成文件夹（命名为时间戳格式），文件夹中info.txt是扫描信息，vul.txt是所有站点存在文件泄露的url  
5.由于hunter的站点查询结果重复率很高，所以很多结果都是重复的，望见谅  
![image](https://user-images.githubusercontent.com/73013511/147515669-7fd44c29-db5a-472e-aac6-c196b7a1d8a5.png)
