# backup_scan
一个写来自己用的简单备份扫描脚本，大佬勿喷

1.需要自己在代码里改写api_key为hunter的key
	2.使用的方式是默认已经选择中国并排除中国香港，也就是province!="中国香港"&&country="中国"
	3.后续条件可以自己添加，详情参考hunter语法。查询条数也是根据hunter（只能是10,20,50,100）
	4.扫描会生成文件夹（命名为时间戳格式），文件夹中all.txt是扫描全部信息，vul.txt是所有站点存在文件泄露的url
	5.由于hunter的站点查询结果重复率很高，所以很多结果都是重复的，望见谅
	6.有少部分结果可能是因为waf掉关键信息才会出现，后续在改进过滤吧
![image](https://user-images.githubusercontent.com/73013511/147515349-0e25de95-ccbb-4bca-a8fd-3c12b1688ac7.png)
