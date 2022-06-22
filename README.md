1\安装python（注意要将python添加到环境变量，同时安装pip）

2\因为是通过bark的app进行通知结果，所以要在手机上安装bark，打开app后，将其中类似"https://api.day.app/vLSvc5LgZSwS4jrHcy7VC/"的链接复制

2\cmd中键入以下代码并回车

```
pip install requests
```

3\main.py中修改如下几行

```python
USERNAME=2222222222 #账号-->学号
PASSWORD="dawdf2222" #密码
AREA_ID=[10,8] #想要预约的房间编号，默认是8、10，若想添加其他的，可以先运行脚本，会显示出其他房间的编号，自行添加或者更改，同时越靠前越优先考虑
BARK_URL="https://api.day.app/vLSvc5LgZSwS4jrHcy7VC/" #bark链接，将自己的粘贴过来，注意保留最外边的引号

#脚本有两项功能，请自己选择，必须是二选一（每个功能块都已用 上双行#下双行# 表示出）
#功能一：预约座位
#功能二：取消预约
#将不需要的功能的代码做成注释，即在代码前加上#
```

4\在main.py所在文件夹内，按住shift不放，同时右击鼠标，选择“在此处打开powershell窗口”，在弹出的cmd窗口中键入以下代码并回车

```python
python main.py
```

即可运行





