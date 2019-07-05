# YiWa

项目同步自[码云yiwa](https://gitee.com/bobo2cj/yiwa)，码云相当于开发环境，github相当于生产环境，周末会持续更新。

#### 介绍
- 伊瓦（树莓派runing），基于百度AI开放平台，语音识别指令，NLP匹配指令，支持自定义“插件”式指令。
无需鼠标，只要说出指令，页面跳转到对应功能。
- 最近看到另外一个pi项目，[悟空机器人（叮当猫）](https://github.com/wzpan/wukong-robot)，主打控制和聊天，
    感兴趣的去看，so，就不用在我这提他的优势项了，ths。

#### 注意
- ！！！请申请你的百度AI应用key，方法在下面（安装教程）！！！
- 项目难度不大，你也可以。
- 本地部署运行文档见[项目Wiki](https://gitee.com/bobo2cj/yiwa/wikis)。

#### 项目灵感
想做的项目 家庭 语音设备 显示屏 统计 展示 提醒 告警
树莓派，麦克风，扬声器，显示屏，

想像中具备的功能：

- 不是控制类设备，只是想家庭统计和展示类助手
- 可以在设定好的时间段内去预判设定好的上班路线是否堵车，并语音告诉我，显示屏显示拥堵路段和路况
- 可以用作闹钟，提现我该送小孩上学了，并且可以自动关闭闹钟，避免一直发出噪音，也可交互关闭闹钟
- 启动语音交互，hi 伊瓦，亮灯+咚咚回应，或者可定制回应
- 结束语音交互：克罗瓦，bey，good luck，随时待命等 待定制回应
- 中间可不中断交流，发出指令
- 语音可选择自带麦克风，或者无线局域网内的智能手机
- 初期指令需要指定，例如：查看指令列表，新增指令，查看内容，下一页等
- 统计儿子是否哭了，哭了几次，什么时候哭的，每天都有记录，展示连续没有哭的次数，可以设定次数对应的奖励，以及惩罚
- 犯错误记录，年度和月度展示
- 声音记录器，起到备忘作用
- 做菜计时提现，还可以记录烧了什么菜，以后回过头来看看自己的成就，哈哈
- 出门需要关哪些设备，门窗等项，给予提现
- 倒计时用
- 游戏比分展示
- 考试历史成绩展示
- 算术学习和测试
- 所有以上都以插件形式可扩展
- 编程语言 python
- 每个包需要包括：语音交互、音频反馈、界面显示（不同指令对应的内容展示，和反馈结果）
- 基础结构平台包括：语音识别为文字指令，指令匹配；文字（指令结果）转语音，渲染界面结果
- 包英文name不可重复
- NLP

#### 软件架构
1. macOS系统环境，Python3.6，其他库在requirements.txt文件中
2. 大概流程：接收麦克风语音，本地离线匹配唤醒词；唤醒后继续接收麦克风指令，指令接入百度语音识别平台，转换成文字；
    接着继续使用百度AI平台的NLP功能，将指令短文本和本地预设好的指令短文本，做语义比较；匹配成功后，通过selenium
    打开本地预设指令对应的url地址，就此实现无鼠标语音控制页面内容展示功能。


#### 安装教程，[看Wiki](https://gitee.com/bobo2cj/yiwa/wikis)

1. pip install -r requirements.txt -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com
2. selenium使用的谷歌驱动文件需要替换为你本地chrome对应的版本，
    下载地址：[这里选择不同版本](https://chromedriver.storage.googleapis.com/index.html)
3. 下载好chromedriver文件后不要更改文件名，就保持chromedriver或chromedriver.exe等
4. 最好替换自己的百度AI的key（[申请指南](https://ai.baidu.com/docs#/Begin/top)），
    配置分别在asr/configs.py和nlp/configs.py文件修改

#### 使用说明（程序启动），[看Wiki](https://gitee.com/bobo2cj/yiwa/wikis)

1. python3.6 web.py
2. python3.6 yiwa.py
3. 启动无误后，即可对着你的麦克风说话，目前支持指令：返回首页，刷新指令，显示所有指令，重启，退出（去掉了）


#### 本地开发，[看Wiki](https://gitee.com/bobo2cj/yiwa/wikis)

1. 可开发基于Flask的插件页面，插件以独包形式，放入apps文件夹下，
    插件必需包含configs.py文件，并指定必需的参数:APPID :str, APPNAME :str, COMMANDS :dict
2. 插件的__init__.py文件必需导入其他flask页面文件，参考已存在的插件包。
3. 插件包的静态文件放入各自包里
4. 约定：
    - 插件必需以单独文件夹形式放入apps文件夹中
    - 插件文件夹根目录，必需包含自我介绍的配置文件，configs.py文件，至少有：appid，appname，


#### 截图

- 等待唤醒、录音中

![等待唤醒、录音中](https://images.gitee.com/uploads/images/2019/0705/115600_5539545b_25066.png "WX20190705-113652-录音中.png")

- 等待唤醒、录音中

![等待唤醒、录音结束](https://images.gitee.com/uploads/images/2019/0705/115649_3e77334c_25066.png "WX20190705-113724-录音结束.png")

- 已唤醒

![已唤醒](https://images.gitee.com/uploads/images/2019/0705/115823_b62dc348_25066.png "WX20190705-113821-已唤醒.png")

- 执行日志

![执行日志](https://images.gitee.com/uploads/images/2019/0705/115720_ff8e5e41_25066.png "WX20190705-115130@2x-指令.png")

- 指令目录

![指令目录](https://images.gitee.com/uploads/images/2019/0705/115759_f9f4be9f_25066.png "WX20190705-114647-指令目录.png")

- 二维码

![二维码](https://images.gitee.com/uploads/images/2019/0706/075010_a70cf626_25066.png "WX20190706-074009@2x-二维码.png")

#### 运行时的样子
    ![树莓派+17'二手显示器，图以后补](#)
    
#### 告诉自己
- 休息一下
-  :white_check_mark: 做几个页面（至少包含欢迎和指令目录）
-  :white_check_mark: 使用websocket刷新yiwa的唤醒状态和语音指令，下一步加入是否“正在录音”的界面标识，
    方便用户知道什么时候该说出指令，而不是去“碰”。
-  :white_check_mark: 提升下语音指令匹配的速度，先采用本地词库来预匹配，找到对应插件，再接百度，
    缩小遍历范围（本地词库需要去生产词库文件，如果采用自动化去生成，对于速度没有保障，
    故而采用[jieba分词](https://github.com/fxsjy/jieba)处理）
-  :white_check_mark: 做下tts文本转语音基础功能，供插件需要发出语音响应时调用（缺少对不同平台的处理，
    例如mac用mei-jia，linux用xxx，windows用xxx）
-  :white_check_mark: 做个二维码生成基础功能，供插件调用，有的插件可能需要借助手机来配置，例如闹钟，通勤地点等
    (渲染时需要使用自定义的render方法，看home页面的实现)
- 接着再休息一下，失业找工作中:(
- 做几个插件，算术题目、汉字笔顺动图展示、英语单词、惩罚记录、闹钟、上学提醒，下学期上学能用上的几个优先做
- 再休息休息
- 停下来优化调整（部分代码替换为python的特性写法）
- 做个在线升级和安装apps的功能，备份本地apps，从gitee拉取代码，替换apps，重启服务。
- 做几个自己相关的插件，高德地图通勤（跨省/市）、做菜倒计时、出门检查项等
- 后面的后面想到再加，土比亢踢牛的。。。