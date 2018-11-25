# SpiderDemo 01

第一个小案例，爬取 douyu 颜值区主播的图片并重命名

新建项目：scrapy startproject douyu

初始化项目：scrapy genspider douyu "douyucdn.cn"

执行并打印 item 内容：scrapy crawl douyu -o 主播.json

