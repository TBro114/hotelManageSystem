# hotelManageSystem
BUPT软件工程小组作业——波普特酒店空调管理系统

该项目的源仓库在https://gitee.com/TBro136/hotelManageSystem

此github仓库为搬运

# 酒店空调管理系统

#### 介绍
AI院AI专业2022级软件工程小组作业——波普特酒店空调管理系统
小组成员：郭鑫焱、董光硕、逯晓暾、陈国玉、童伟杰

### 前言

本项目采用css渲染HTML+后端django的体系结构进行开发，DBMS采用MySQL，并使用navicat来便于数据库的管理。

为了隔离项目依赖且便于管理和迁移项目，在工作目录下创建 .venv 文件夹来设置一个 Python 虚拟环境，VS Code 可以通过 .venv 文件夹自动识别虚拟环境，并配置虚拟Python解释器。
使用  pip install -r requirements.txt  来下载项目所需要的依赖。
在每一次开发结束后调用pip freeze > requirements.txt来把项目中新增的依赖更新在requirements.txt中

### 结构设计

checkIn:用户办理入住以及选择房间

checkOut：用户办理退房、导出账单以及空调详单

control：房间空调的控制面板

login：空调管理系统的登录（不包含用户）

publicModels：只用来定义数据库的模型，无其他作用

supervise：空调管理员设置空调的页面，同时包含了调度的完全实现

cold.py:当模式为制冷时的调度机制（只是逻辑上的实现，不包含与数据库和前端的交互）

warm.py:同上，只不过模式为制热

testScipt.py:用于从测试用例的excel表中读取测试用例

### 注意
该项目仍有一些小bug没有解决，且每一届的任务要求都会有不同之处，本开源只供借鉴，提供思路，请勿直接copy







 :yum:  :yum:  :yum: 

此外，该课程作业“年事已高”，从一开始有这个作业后，每年课程组都会往任务要求中加些新鲜玩意儿，并且严重怀疑他们并没有验证过这个作业的合理性。
因此，写这个课程作业是一件痛苦又自相矛盾的事情，且该课程作业成绩占比不高，属于是性价比“拉满” :imp: 

总之，希望本开源能减轻一些开发过程中的痛苦。若对你有帮助，请 :star: 本项目。


