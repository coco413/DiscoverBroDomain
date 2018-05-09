### 0x00 简介
尽可能花更少的时间,使用All in one工具收集更多的信息-旁站关联域名采集。


### 0x01 说明
参考[BroDomain@code-scan](https://github.com/code-scan/BroDomain)的思路,修改如下:
```
|---输入域名或者IP(如果是IP就反查获取域名)
|    |---通过域名查询whois的邮箱，注册人,手机号。
|    |---通过whois邮箱进行反查获取更多注册的相关域名。
|    |---通过whois注册人进行反查获取更多注册的相关域名和邮箱和邮箱。
|    |---通过whois手机号进行反查获取更多注册的相关域名和邮箱和邮箱。
|    |---把通过手机号和注册人反查得到的邮箱再进行邮箱反查获取相关域名。
|    |---通过查询备案号获取更多相关域名。
|---最后再通过DiscoverSpdier和DiscoverSubdomain继续扩宽关联目标。
```
备注:忽略存在cdn、注册信息随意写的比如手机号110反查出很多无关域名情况。


### 0x02 使用
___
- 1.下载
```
git git@github.com:coco413/DiscoverBroDomain.git
cd DiscoverBroDomain
pip install tldextract bs4 lxml
```
- 2.运行
```
运行环境：python 2.7 Mac
python DiscoverBroDomain.py dota2.com.cn
python DiscoverBroDomain.py 121.207.226.230
```
- 3.截图
![test](https://s1.ax1x.com/2018/05/09/CwUDld.jpg)
![test](https://s1.ax1x.com/2018/05/09/CwaSXR.png)
![test](https://s1.ax1x.com/2018/05/09/CwUr6A.png)


### 0x03 其他
- 1.遇到tldextract的warning信息忽视或者对应目录文件添加权限。
- 2.避免遇到一些域名cdn、或者注册信息随意写可以边跑边whois看下自判断关联情况。
- 3.Tools目录中存放win下C段/旁站收集工具,辅助目标收集。
- 4.接口如果页面更新换下解析规则就可以了,自己用的过程遇到也会持续更新。
