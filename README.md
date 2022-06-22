1\点击右上角**Fork**到自己的仓库

2\该项目下依次点开**Setting-Environments-New Environments-输入NAME为Library_CONFIG确定-Add Secret**

分别输入四组数据：

```
Name：DD_BOT_SECRET
Value：xxxxxxxxxx   #(这里将x换成自己的钉钉SECRET，如，WDAWDAW3R3FADWUHA)

Name：DD_BOT_ACCESS_TOKEN
Value：xxxxxxxxxx   #(这里将x换成自己的钉钉TOKEN，如，WDAWDAW3R3FADWUHA)

Name：USERNAME
Value：xxxxxxxxxx   #(这里将x换成自己的学号，如，1902222334)

Name：PASSWORD
Value：xxxxxxxxxx   #(这里将x换成自己的图书馆账号密码，如，WFAWCWAdcaw1!)
```

3\想要运行本脚本时，直接到该项目下，找到action，选择左侧的**Library_seat_reservation**，再点右侧的**run workflow**即可

4\当刷到座位时，会在钉钉群里接收到消息的



##### PS：

**关于预约的房间，需要自己根据需求更改main.py**：

找到下面的代码

```python
AREA_ID=[8,10] 
```

****

这里的**AREA_ID**中的数字就是想要预约的房间编号，默认是8、10，越靠前越优先考虑



以下为**房间名字和编号对照表**：

```
id-3	雁塔图书馆-二楼-南自修区
id-6	雁塔图书馆-二楼-学术文库自修
id-7	雁塔图书馆-三楼-南自修区
id-8	雁塔图书馆-三楼-移动设备自修区
id-14	雁塔图书馆-三楼-东自修区
id-9	雁塔图书馆-四楼-南自修区 
id-10	雁塔图书馆-四楼-移动设备自修区
id-15	雁塔图书馆-四楼-东自修区
id-16	雁塔图书馆-四楼-西自修区
id-12	雁塔图书馆-一楼研讨间-会议室2(2-20人)
id-13	雁塔图书馆-一楼研讨间-会议室3(2-20人)
id-32	草堂图书馆-一楼-考研专区
id-21	草堂图书馆-二楼-A区
id-22	草堂图书馆-二楼-D区
id-23	草堂图书馆-三楼-A区
id-24	草堂图书馆-三楼-B区
id-25	草堂图书馆-三楼-C区
id-26	草堂图书馆-三楼-D区
id-27	草堂图书馆-四楼-A区
id-28	草堂图书馆-四楼-B区
id-29	草堂图书馆-四楼-C区
id-30	草堂图书馆-四楼-D区
```
