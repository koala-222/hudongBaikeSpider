# 互动百科爬虫

利用Scrapy1.6爬取全部互动百科页面

将爬取到的页面写入磁盘文件，将文件记录写入MySQL数据库

**运行环境：**

- Python3.7
- Scrapy1.6
- MySQL8.0

**运行命令：**

```powershell
scrapy crawl hudongBaike -s JOBDIR=./status
```

