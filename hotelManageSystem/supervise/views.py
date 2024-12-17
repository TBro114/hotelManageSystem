import json
import time
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
from publicModels.models import CentralAirCondition, AirCondition, AirServiceLog, Room, Customer,AirBill,Room, CentralAirCondition
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Max
from global_count import cou


center_airconditional_id=1
isschedule = 0
class sch:
    def __init__(self):
        # 作为控制调度循环是否进行的参数
        self.key = 0


    def startSchedule(self):
        global p
        p = 0 # 消息队列指示
        i = cou.counter # 前端控制
        # i = 0 # 脚本控制
        m = CentralAirCondition.objects.get(id=1).mode # 获取中央空调模式
        ac = AirCondition.objects.all() # 获取客房空调队列



        if m == 'sun':  # 制冷模式（因为没有除湿和送风的具体规则也视为制冷
            # 初始化房间属性
            r[0]=scheduleRoom(1, 0, 0, 10, 22, 10, 2, float(ac[0].total_price), 0, 0, 0)
            r[1]=scheduleRoom(2, 0, 0, 15, 22, 15, 2, float(ac[1].total_price), 0, 0, 0)
            r[2]=scheduleRoom(3, 0, 0, 18, 22, 18, 2, float(ac[2].total_price), 0, 0, 0)
            r[3]=scheduleRoom(4, 0, 0, 12, 22, 12, 2, float(ac[3].total_price), 0, 0, 0)
            r[4]=scheduleRoom(5, 0, 0, 14, 22, 14, 2, float(ac[4].total_price), 0, 0, 0)
            # 调度循环
            while True:
                # 判断是否退出循环
                if(self.key):
                    self.key=0
                    return
                # 读取消息队列对房间属性进行设置
                Set_s(i)
                # 进行实质调度
                schedule_s(i)
                # 打印服务和等待队列
                show(i)
                # 根据服务情况修改温度和计费
                settle_s()
                # 下一时刻
                i += 1
                # 等待2秒，2秒视为一分钟
                time.sleep(2)
        else:  # 制暖模式
            # 初始化房间属性
            r[0]=scheduleRoom(1, 0, 0, 32, 25, 32, 2, float(ac[0].total_price), 0, 0, 0)
            r[1]=scheduleRoom(2, 0, 0, 28, 25, 28, 2, float(ac[1].total_price), 0, 0, 0)
            r[2]=scheduleRoom(3, 0, 0, 30, 25, 30, 2, float(ac[2].total_price), 0, 0, 0)
            r[3]=scheduleRoom(4, 0, 0, 29, 25, 29, 2, float(ac[3].total_price), 0, 0, 0)
            r[4]=scheduleRoom(5, 0, 0, 35, 25, 35, 2, float(ac[4].total_price), 0, 0, 0)
            # 调度循环
            while True:
                # 判断是否退出循环
                if(self.key):
                    self.key=0
                    return
                # 读取消息队列对房间属性进行设置
                Set_c(i)
                # 进行实质调度
                schedule_c(i)
                # 打印服务和等待队列
                show(i)
                # 根据服务情况修改温度和计费
                settle_c()
                # 下一时刻
                i += 1
                # 等待2秒，2秒视为一分钟
                time.sleep(2)
    # 调用使调度循环结束
    def setkey(self):
        self.key=1



s=sch()

# @login_required(login_url='/login/login')
def acmanage(request):
    # if request.user.role != 'ac_manager':
    #     messages.error(request, "您没有访问此页面的权限。")
    #     return redirect('index')  # 重定向到首页或其他页面
    airList = AirCondition.objects.order_by('id').values('id', 'airCondition_status', 'current_temperature', 'speed', 'airCondition_mode', 'total_price', 'target_temperature')
    airList = list(airList)

    subquery = AirBill.objects.values('room_id').annotate(max_flag=Max('flag'))
    airbillList = AirBill.objects.filter(
        room_id__in=subquery.values('room_id'),
        flag__in=subquery.values('max_flag')
    ).order_by('room_id').values('room_id', 'one_time_price')
    airbillList = list(airbillList)
    # print(airbillList)

    # Create a dictionary to map room IDs to their air conditioning data
    room_data = {i : air for i, air in enumerate(airList)}

    # Update the dictionary with billing data if available
    for i, air in room_data.items():
        room_id = i + 1
        air['room_id'] = room_id
        air['one_time_price'] = '暂无账单'
        for bill in airbillList:
            if bill['room_id'] == air['id']:
                air['one_time_price'] = bill['one_time_price']
                break

    # Convert the dictionary back to a list
    combined_list = list(room_data.values())
    for air in combined_list:
        air['total_price'] = f"{float(air['total_price']):06.2f}"
        air['current_temperature'] = f"{float(air['current_temperature']):04.1f}"
        if air['one_time_price'] != '暂无账单':
            air['one_time_price'] = f"{float(air['one_time_price']):06.2f}"

        # 获取中央空调数据表
        aircondition = AirCondition.objects.all().first()
        centralaircondition = CentralAirCondition.objects.all().first()
        if centralaircondition.mode !='sun':
            max_temp = centralaircondition.max_temperature_cold
            min_temp = centralaircondition.min_temperature_cold
        else:
            max_temp = centralaircondition.max_temperature_hot
            min_temp = centralaircondition.min_temperature_hot
    air_conditions = AirCondition.objects.all()
    

    # 准备一个列表来存储每个空调的开关状态
    air_condition_data = []
    for air_condition in air_conditions:
        air_condition_data.append({
            'air_condition_id': air_condition.id,  # 空调ID
            'air_condition_status': air_condition.airCondition_status  # 只返回开关状态
        })
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'airList': combined_list,'air_condition_data':air_condition_data},)
    
    if request.method == "GET":
        return render(request, 'supervise.html', {'centralaircondition':centralaircondition,'max_temp':max_temp,'min_temp':min_temp,'airconditional':aircondition,'airList':combined_list})
   
def get_center_aircondition(request):
    centralaircondition = CentralAirCondition.objects.all().first()

    air_conditions = AirCondition.objects.all()

    # 准备一个列表来存储每个空调的开关状态
    air_condition_data = []
    for air_condition in air_conditions:
        air_condition_data.append({
            'air_condition_id': air_condition.id,  # 空调ID
            'air_condition_status': air_condition.airCondition_status,  # 只返回开关状态
            'speed': air_condition.speed,  # 风速，使用choices显示文本
            'mode': air_condition.airCondition_mode  # 空调模式
        })
    if centralaircondition.mode != 'sun':
        return JsonResponse({
                'status': 'success',
                'message': '空调设置已更新',
                'centralaircondition': {
                    'Max_temperature': centralaircondition.max_temperature_cold,
                    'Min_temperature': centralaircondition.min_temperature_cold,
                    'airCondition_status': centralaircondition.central_aircondition_status,
                    'mode': centralaircondition.mode,
                },
                'air_conditions': air_condition_data  # 只返回开关状态
            })
    else:
        return JsonResponse({
                'status': 'success',
                'message': '空调设置已更新',
                'centralaircondition': {
                    'Max_temperature': centralaircondition.max_temperature_hot,
                    'Min_temperature': centralaircondition.min_temperature_hot,
                    'airCondition_status': centralaircondition.central_aircondition_status,
                    'mode': centralaircondition.mode,
                },
                'air_conditions': air_condition_data  # 只返回开关状态
            })
    



@csrf_exempt
def update_center_aircondition(request):
    global isschedule
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            # print("接收到的数据:", data)

            centralaircondition = CentralAirCondition.objects.all().first()

            # 更新空调记录
            centralaircondition.mode = data.get('mode', centralaircondition.mode)
            centralaircondition.central_aircondition_status = data.get('airCondition_status',centralaircondition.central_aircondition_status)
            centralaircondition.price_rate = data.get('cost_rate',centralaircondition.price_rate)
            air_conditions = AirCondition.objects.all()
            for air_condition in air_conditions:
                # 将每个空调的模式设置为中央空调的模式
                air_condition.airCondition_mode = centralaircondition.mode
                # 如果中央空调关闭，则所有空调的状态也要设置为关闭
                if (centralaircondition.central_aircondition_status == 0):
                    air_condition.airCondition_status = centralaircondition.central_aircondition_status
                air_condition.save()        
            
            if centralaircondition.mode != 'sun':
                centralaircondition.max_temperature_cold = data.get('Max_temperature', centralaircondition.max_temperature_cold)
                centralaircondition.min_temperature_cold = data.get('Min_temperature', centralaircondition.min_temperature_cold)
                centralaircondition.save()
                if(centralaircondition.central_aircondition_status==1 and isschedule==0):
                    isschedule=1
            
                    s.startSchedule()
                elif(centralaircondition.central_aircondition_status==0 and isschedule==1):
                    isschedule=0
                    s.setkey()  
                return JsonResponse({
                'status': 'success',
                'message': '空调设置已更新',
                'centralaircondition': {
                    'Max_temperature': centralaircondition.max_temperature_cold,
                    'Min_temperature': centralaircondition.min_temperature_cold,
                    'airCondition_status': centralaircondition.central_aircondition_status,
                    'airCondition_mode': centralaircondition.mode,
                    'cost_rate': centralaircondition.price_rate,
                }
            })
            else:
                centralaircondition.max_temperature_hot = data.get('Max_temperature', centralaircondition.max_temperature_hot)
                centralaircondition.min_temperature_hot = data.get('Min_temperature', centralaircondition.min_temperature_hot)
                centralaircondition.save()
                if(centralaircondition.central_aircondition_status==1 and isschedule==0):
                    isschedule=1
                    s.startSchedule()
                elif(centralaircondition.central_aircondition_status==0 and isschedule==1):
                    isschedule=0
                    s.setkey()
                return JsonResponse({
                'status': 'success',
                'message': '空调设置已更新',
                'centralaircondition': {
                    'Max_temperature': centralaircondition.max_temperature_hot,
                    'Min_temperature': centralaircondition.min_temperature_hot,
                    'airCondition_status': centralaircondition.central_aircondition_status,
                    'airCondition_mode': centralaircondition.mode,
                    'cost_rate': centralaircondition.price_rate,
                }
            })
            



        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)

def room(request):
    airList = AirCondition.objects.order_by('id').values('id', 'airCondition_status', 'current_temperature', 'speed', 'airCondition_mode', 'total_price', 'target_temperature')
    airList = list(airList)

    subquery = AirBill.objects.values('room_id').annotate(max_flag=Max('flag'))
    airbillList = AirBill.objects.filter(
        room_id__in=subquery.values('room_id'),
        flag__in=subquery.values('max_flag')
    ).order_by('room_id').values('room_id', 'one_time_price')
    airbillList = list(airbillList)
    # print(airbillList)

    # Create a dictionary to map room IDs to their air conditioning data
    room_data = {i : air for i, air in enumerate(airList)}

    # Update the dictionary with billing data if available
    for i, air in room_data.items():
        room_id = i + 1
        air['room_id'] = room_id
        air['one_time_price'] = '暂无账单'
        for bill in airbillList:
            if bill['room_id'] == air['id']:
                air['one_time_price'] = bill['one_time_price']
                break

    # Convert the dictionary back to a list
    combined_list = list(room_data.values())
    # print(combined_list)


    centralaircondition = CentralAirCondition.objects.all().first()
    centralaircondition_dict = {
        'max_temperature': centralaircondition.max_temperature_hot,
        'min_temperature': centralaircondition.min_temperature_hot,
        'price_rate': centralaircondition.price_rate
    }

   

    return render(request, 'supervise.html', {'airList': combined_list[0], 'centralaircondition': centralaircondition})

# def logout_view(request):
#     # 清除 session 中的 room_id，退出登录
#     if 'room_id' in request.session:
#         del request.session['room_id']
#         messages.info(request, '成功退出登录')

#     # 重定向到登录页面
#     return redirect('login')  # 假设你有一个名为 'customerloginlogin' 的 URL 来显示登录页面

# 房间类
class scheduleRoom:
    def __init__(self, num, status, ser, initial, set_temp, now, wind, money, time,req_time,ifChange):
        self.num = num # 房间号
        self.status = status # 开关状态
        self.ser = ser # 是否被服务
        self.initial = initial # 房间初始温度
        self.set = set_temp # 房间设置温度
        self.now = now # 房间当前温度
        self.wind = wind # 房间设置风速
        self.money = money # 房间总计空调费用
        self.time = time # 房间等待/服务时长
        self.req_time=req_time # 房间请求时间
        self.ifChange=ifChange # 标记房间是否在当前时刻发起申请，生成详单时使用

    # 打印房间属性，用于调试
    def __str__(self):
        return f"room:{str(self.num)}, state:{self.status}, now:{self.now}, set:{self.set}, wind:{self.wind}, money:{self.money}, time:{str(self.time)}, ser:{str(self.ser)}"

 # 消息类
class News:
    def __init__(self, time, r, type_, value):
        self.time = time # 请求时间
        self.r = r # 请求房间
        self.type = type_ # 请求类型
        self.value = value # 请求值


wait = [None] * 5 # 等待队列
service = [None] * 5 # 服务队列
wn = 0 # 等待队列房间数
level = ["", "L", "M", "H"] # 用于转化风速的列表

# 消息队列，用于脚本测试（制冷）
new_s = [
    # News(1, 1, 1, 1),
    # News(2, 1, 2, 18),
    # News(2, 2, 1, 1),
    # News(2, 5, 1, 1),
    # News(3, 3, 1, 1),
    # News(4, 2, 2, 19),
    # News(4, 4, 1, 1),
    # News(5, 5, 2, 22),
    # News(6, 1, 3, 3),
    # News(7, 2, 1, 0),
    # News(8, 2, 1, 1),
    # News(8, 5, 3, 3),
    # News(10, 1, 2, 22),
    # News(10, 4, 3, 3),
    # News(10, 4, 2, 18),
    # News(12, 2, 2, 22),
    # News(13, 5, 3, 1),
    # News(15, 1, 1, 0),
    # News(15, 3, 2, 24),
    # News(15, 3, 3, 1),
    # News(16, 5, 2, 20),
    # News(16, 5, 3, 3),
    # News(17, 2, 1, 0),
    # News(18, 3, 3, 3),
    # News(19, 1, 1, 1),
    # News(19, 4, 2, 20),
    # News(19, 4, 3, 2),
    # News(20, 2, 1, 1),
    # News(21, 5, 2, 25),
    # News(23, 3, 1, 0),
    # News(24, 5, 1, 0),
    # News(25, 1, 1, 0),
    # News(26, 2, 1, 0),
    # News(26, 4, 1, 0),
]

# 初始化房间列表
r = [
    scheduleRoom(1, 0, 0, 32, 25, 32, 2, 0, 0, 0, 0),
    scheduleRoom(2, 0, 0, 28, 25, 28, 2, 0, 0, 0, 0),
    scheduleRoom(3, 0, 0, 30, 25, 30, 2, 0, 0, 0, 0),
    scheduleRoom(4, 0, 0, 29, 25, 29, 2, 0, 0, 0, 0),
    scheduleRoom(5, 0, 0, 35, 25, 35, 2, 0, 0, 0, 0),
]

p = 0  # 指向下一个要处理的消息

# 读取消息队列对房间属性进行设置（制暖）
def Set_s(n):
    global p, wn
    h = 0
    for i in range (5): # 初始化为0表示该时刻房间均未发起申请
        r[i].ifChange=0
    while True:
        if p >= len(new_s): # 当已经指向消息队列末尾直接退出，进入下一时刻
            return h
        h = 1
        a = new_s[p] # 获取下一个消息
        if a.time > n: # 当消息发起时间比当前处理时刻晚时退出，进入下一时刻
            return h
        r[a.r - 1].req_time=a.time # 对申请房间申请时间赋值
        r[a.r - 1].ifChange=1 # 表示该房间该时刻发起了申请
        if a.type == 1: # 发起了开关请求
            r[a.r - 1].status = a.value
            if a.value: # 为开时
                air=AirCondition.objects.get(id=int(a.r)) # 保存开关值
                air.airCondition_status=1
                air.save()
                airbill=AirBill.objects.filter(room_id=a.r).last() # 获取该房间上一详单，目的是对flag赋值用于区分
                if(airbill): # 若有
                    AirBill.objects.create(room_id=a.r,one_time_price=0,flag=airbill.flag+1) # 产生新详单
                else: # 若无
                    AirBill.objects.create(room_id=a.r,one_time_price=0,flag=0) # 产生新详单
                wait[wn] = r[a.r - 1] # 加入到等待队列
                wn += 1 # 等待队列数量加一
            else: # 为关时
                r[a.r - 1].set = 22 # 恢复目标温度
                r[a.r - 1].wind = 2 # 恢复风速
                ac=AirCondition.objects.get(id=a.r) # 保存到数据库中
                ac.total_price=r[a.r - 1].money
                ac.airCondition_status=0
                ac.target_temperature=22
                ac.speed=2
                ac.save()
        elif a.type == 2: # 发起了调温申请
            air=AirCondition.objects.get(id=a.r) # 保存目标温度
            air.target_temperature=a.value
            air.save()
            r[a.r - 1].set = a.value # 设置目标温度
        else:
            air=AirCondition.objects.get(id=a.r) # 保存设置风速
            air.speed=a.value
            air.save()
            r[a.r - 1].wind = a.value # 设置风速

        p += 1 # 处理下一消息

# 读取消息队列对房间属性进行设置（制冷）
# 除了关机恢复的温度不同，其余与制暖基本一致不再做解释
def Set_c(n):
    global p, wn
    h = 0
    for i in range (5):
        r[i].ifChange=0
    while True:
        if p >= len(new_s):
            return h
        h = 1
        a = new_s[p]
        if a.time > n:
            return h
        r[a.r - 1].req_time=a.time
        r[a.r - 1].ifChange=1
        if a.type == 1:
            r[a.r - 1].status = a.value
            if a.value:
                air=AirCondition.objects.get(id=a.r)
                air.airCondition_status=1
                air.save()
                airbill=AirBill.objects.filter(room_id=a.r).last()
                if(airbill):
                    AirBill.objects.create(room_id=a.r,one_time_price=0,flag=airbill.flag+1)
                else:
                    AirBill.objects.create(room_id=a.r,one_time_price=0,flag=0)
                wait[wn] = r[a.r - 1]
                wn += 1
            else:
                r[a.r - 1].set = 25
                r[a.r - 1].wind = 2
                ac=AirCondition.objects.get(id=a.r)
                ac.total_price=r[a.r - 1].money
                ac.airCondition_status=0
                ac.target_temperature=25
                ac.speed=2
                ac.save()
        elif a.type == 2:
            air=AirCondition.objects.get(id=a.r)
            air.target_temperature=a.value
            air.save()
            r[a.r - 1].set = a.value
        else:
            air=AirCondition.objects.get(id=a.r)
            air.speed=a.value
            air.save()
            r[a.r - 1].wind = a.value

        p += 1



def SORT(): # 根据风速（降序）、时长（降序）、房间号（升序）的顺序对两队列排序，并获得服务队列房间数量
    global wn
    wait.sort(key=lambda x: (x.wind if x else 0, x.time if x else 0, -x.num if x else 0, x is None), reverse=True)
    service.sort(key=lambda x: (x.wind if x else 0, x.time if x else 0, -x.num if x else 0, x is None), reverse=True)
    wn = sum(1 for x in wait if x is not None)


# 进行实质调度（制暖）
def schedule_s(counter):
    global wn    
    SORT() # 进行依次排序
    free = 0 # 表示服务队列空闲数量
    for i in range(2, -1, -1): # 获取空闲数量
        if service[i] is not None:
            break
        free += 1
    # 主动退出：等待队列
    for i in range(wn):
        if wait[i] and not wait[i].status:
            wait[i].ser = False
            wait[i].time = 0
            wait[i] = None

    # 主动退出：服务队列
    for i in range(3):  
        # 主动关机   
        if service[i] and not service[i].status:
            service[i].ser = False
            service[i].time = 0

            # service[i]退出服务队列，修改服务结束时间并计算该段费用
            detail = AirServiceLog.objects.filter(room_id=service[i].num).order_by('-id').first()
            detail.end_time=counter
            detail.service_price=(detail.end_time-detail.start_time)*1.0/(4-detail.current_speed)
            detail.save()
            service[i] = None # 表示该位置空缺
            free += 1 # 服务空闲位置增加

        # 达到设定温度
        elif service[i] and float(service[i].set) <= service[i].now:
            service[i].ser = False
            service[i].time = 0
            
            # service[i]退出服务队列，修改服务结束时间并计算该段费用
            detail = AirServiceLog.objects.filter(room_id=service[i].num).order_by('-id').first()
            detail.end_time=counter
            detail.service_price=(detail.end_time-detail.start_time)*1.0/(4-detail.current_speed)
            detail.save()
            wait[i + wn] = service[i]
            service[i] = None # 表示该位置空缺
            free += 1 # 服务空闲位置增加


    # 填补空缺
    for i in range(wn): 
        if free > 0 and wait[i] and float(wait[i].set) > wait[i].now: # 有空闲位置且当前温度小于设置温度（需要服务）
            wait[i].ser = True
            wait[i].time = 0
            service[4 - i] = wait[i]
            wait[i] = None
            free -= 1

            room = Room.objects.get(id = service[4 - i].num)
            aircondaition = AirCondition.objects.get(id = service[4 - i].num)
            # 创建新详单
            detail=AirServiceLog.objects.create(room=room, airCondition=aircondaition, request_time=service[4 - i].req_time, start_time=counter, current_speed=service[4-i].wind)

    # 增大风速后可以服务的情况
    for i in range(wn):    
        if wait[i] and float(wait[i].set) > wait[i].now: # 当前温度小于设置温度（需要服务）
            for j in range(3):
                if service[j] and wait[i].wind > service[j].wind: # 匹配第一个风速小于等待队列的作为替换
                    service[j].time = 0
                    service[j].ser = False
                    wait[j + wn] = service[j]
                    service[j] = None
                    wait[i].time = 0
                    wait[i].ser = True
                    service[4 - i] = wait[i]
                    wait[i] = None

                     # wait[i]进入服务队列，创建详单记录
                    room = Room.objects.get(id = service[4 - i].num)
                    aircondaition = AirCondition.objects.get(id = service[4 - i].num)
                    detail=AirServiceLog.objects.create(room=room, airCondition=aircondaition, request_time=service[4 - i].req_time, start_time=counter, current_speed=service[4-i].wind)
                    
                    # service[i]退出服务队列，修改服务结束时间
                    detail = AirServiceLog.objects.filter(room_id=wait[j + wn].num).order_by('-id').first()
                    detail.end_time=counter
                    detail.service_price=(detail.end_time-detail.start_time)*1.0/(4-detail.current_speed)
                    detail.save()
                    
                    break

    # 等待足够时切换
    for i in range(wn):   
        if wait[i] and float(wait[i].set) > wait[i].now and wait[i].time >= 2: # 当前温度小于设置温度（需要服务）且等待时间大于等于两分钟
            for j in range(3):
                if service[j] and wait[i].wind == service[j].wind: # 匹配第一个风速等于等待队列的作为替换（服务时间最久的）
                    service[j].time = 0
                    service[j].ser = False
                    wait[j + wn] = service[j]
                    service[j] = None
                    wait[i].time = 0
                    wait[i].ser = True
                    service[4 - i] = wait[i]
                    wait[i] = None

                    # wait[i]进入服务队列，创建详单记录
                    room = Room.objects.get(id = service[4 - i].num)
                    aircondaition = AirCondition.objects.get(id = service[4 - i].num)
                    detail=AirServiceLog.objects.create(room=room, airCondition=aircondaition, request_time=service[4 - i].req_time, start_time=counter, current_speed=service[4-i].wind)
                    
                    # service[i]退出服务队列，修改服务结束时间
                    detail = AirServiceLog.objects.filter(room_id=wait[j + wn].num).order_by('-id').first()
                    detail.end_time=counter
                    detail.service_price=(detail.end_time-detail.start_time)*1.0/(4-detail.current_speed)
                    detail.save()
                    
                    break
    SORT()
    # 根据当前时刻是否发起申请判断是否开启一个新详单
    for i in range(5):
        if r[i].ifChange and r[i].ser and r[i].time:
            
            detail = AirServiceLog.objects.filter(room_id=i+1).order_by('-id').first()
            detail.end_time=counter
            detail.service_price=(detail.end_time-detail.start_time)*1.0/(4-detail.current_speed)
            detail.save()

            room = Room.objects.get(id = i+1)
            aircondaition = AirCondition.objects.get(id = i+1)
            detail=AirServiceLog.objects.create(room=room, airCondition=aircondaition, request_time=counter, start_time=counter, current_speed=r[i].wind)


# 进行实质调度（制冷）
# 逻辑与制暖一致，不再做解释
def schedule_c(counter):
    global wn
    for i in range(5):
        print(r[i])
    SORT()
    free = 0
    for i in range(2, -1, -1):
        if service[i] is not None:
            break
        free += 1
    # 主动退出：等待队列
    for i in range(wn):
        if wait[i] and not wait[i].status:
            wait[i].ser = False
            wait[i].time = 0
            wait[i] = None

    # 主动退出：服务队列
    for i in range(3):      #service[i]退出
        if service[i] and not service[i].status:
            service[i].ser = False
            service[i].time = 0

            # service[i]退出服务队列，修改服务结束时间
            detail = AirServiceLog.objects.filter(room_id=service[i].num).order_by('-id').first()
            detail.end_time=counter
            detail.service_price=(detail.end_time-detail.start_time)*1.0/(4-detail.current_speed)
            detail.save()

            service[i] = None
            free += 1


        elif service[i] and float(service[i].set) >= service[i].now:
            service[i].ser = False
            service[i].time = 0
            
            # service[i]退出服务队列，修改服务结束时间
            detail = AirServiceLog.objects.filter(room_id=service[i].num).order_by('-id').first()
            detail.end_time=counter
            detail.service_price=(detail.end_time-detail.start_time)*1.0/(4-detail.current_speed)
            detail.save()
            wait[i + wn] = service[i]
            service[i] = None
            free += 1



    # 填补空缺
    for i in range(wn):     #wait[i]进入
        if free > 0 and wait[i] and float(wait[i].set) < wait[i].now:
            wait[i].ser = True
            wait[i].time = 0
            service[4 - i] = wait[i]
            wait[i] = None
            free -= 1

            room = Room.objects.get(id = service[4 - i].num)
            aircondaition = AirCondition.objects.get(id = service[4 - i].num)
            detail=AirServiceLog.objects.create(room=room, airCondition=aircondaition, request_time=service[4 - i].req_time, start_time=counter, current_speed=service[4-i].wind)

    # 风速调整
    for i in range(wn):     #service[j]退出，wait[i]进入
        if wait[i] and float(wait[i].set) < wait[i].now:
            for j in range(3):
                if service[j] and wait[i].wind > service[j].wind:
                    service[j].time = 0
                    service[j].ser = False
                    wait[j + wn] = service[j]
                    service[j] = None
                    wait[i].time = 0
                    wait[i].ser = True
                    service[4 - i] = wait[i]
                    wait[i] = None

                     # wait[i]进入服务队列，创建详单记录
                    room = Room.objects.get(id = service[4 - i].num)
                    aircondaition = AirCondition.objects.get(id = service[4 - i].num)
                    detail=AirServiceLog.objects.create(room=room, airCondition=aircondaition, request_time=service[4 - i].req_time, start_time=counter, current_speed=service[4-i].wind)
                    
                    # service[i]退出服务队列，修改服务结束时间
                    detail = AirServiceLog.objects.filter(room_id=wait[j + wn].num).order_by('-id').first()
                    detail.end_time=counter
                    detail.service_price=(detail.end_time-detail.start_time)*1.0/(4-detail.current_speed)
                    detail.save()
                    
                    break

    # 等待足够时切换
    for i in range(wn):     ##service[j]退出，wait[i]进入
        if wait[i] and float(wait[i].set) < wait[i].now and wait[i].time >= 2:
            for j in range(3):
                if service[j] and wait[i].wind == service[j].wind:
                    service[j].time = 0
                    service[j].ser = False
                    wait[j + wn] = service[j]
                    service[j] = None
                    wait[i].time = 0
                    wait[i].ser = True
                    service[4 - i] = wait[i]
                    wait[i] = None

                    # wait[i]进入服务队列，创建详单记录
                    room = Room.objects.get(id = service[4 - i].num)
                    aircondaition = AirCondition.objects.get(id = service[4 - i].num)
                    detail=AirServiceLog.objects.create(room=room, airCondition=aircondaition, request_time=service[4 - i].req_time, start_time=counter, current_speed=service[4-i].wind)
                    
                    # service[i]退出服务队列，修改服务结束时间
                    detail = AirServiceLog.objects.filter(room_id=wait[j + wn].num).order_by('-id').first()
                    detail.end_time=counter
                    detail.service_price=(detail.end_time-detail.start_time)*1.0/(4-detail.current_speed)
                    detail.save()
                    
                    break
    SORT()

    for i in range(5):
        if r[i].ifChange and r[i].ser and r[i].time:
            
            detail = AirServiceLog.objects.filter(room_id=i+1).order_by('-id').first()
            detail.end_time=counter
            detail.service_price=(detail.end_time-detail.start_time)*1.0/(4-detail.current_speed)
            detail.save()

            room = Room.objects.get(id = i+1)
            aircondaition = AirCondition.objects.get(id = i+1)
            detail=AirServiceLog.objects.create(room=room, airCondition=aircondaition, request_time=counter, start_time=counter, current_speed=r[i].wind)
# 打印服务和等待队列
def show(e):
    print(f"第{e}分钟")
    print("服务队列：", end="")
    for srv in service:
        if srv:
            print(f"{srv.num}{level[srv.wind]} ", end="")
            srv.time += 1
    print("等待队列：", end="")
    for w in wait:
        if w:
            print(f"{w.num}{level[w.wind]} ", end="")
            w.time += 1
    print()

# 根据服务情况修改温度和计费（制暖）
def settle_s():
    # 遍历每个房间
    for i in range(5):
        if r[i].ser: # 在服务队列时
            r[i].now = min(float(r[i].set), r[i].now + 1.0 / (4 - r[i].wind)) # 根据风速修改温度
            r[i].money += 1.0 / (4 - r[i].wind) # 根据风速计费
        elif r[i].status: # 在等待队列
            if float(r[i].set) <= r[i].now: # 判断是否回温
                r[i].now = max(r[i].initial, r[i].now - 0.5) # 回温
        else: # 关机
            r[i].now = max(r[i].initial, r[i].now - 0.5) # 回温
        if(r[i].status): # 对开机空调的当前费用进行修改
            air=AirCondition.objects.get(id=i+1)
            airbill=AirBill.objects.filter(room_id=i+1).last()
            airbill.one_time_price=r[i].money-float(air.total_price)
            airbill.save()
    airconditions=AirCondition.objects.all()
    # 保存当前温度
    i=0
    for ac in airconditions:
        ac.current_temperature=r[i].now
        ac.save()
        i+=1

# 根据服务情况修改温度和计费（制冷）
# 逻辑与制暖一致，不再做解释
def settle_c():
    for i in range(5):

        if r[i].ser:
            r[i].now = max(float(r[i].set), r[i].now - 1.0 / (4 - r[i].wind))
            r[i].money += 1.0 / (4 - r[i].wind)
        elif r[i].status:
            if float(r[i].set) >= r[i].now:
                r[i].now = min(r[i].initial, r[i].now + 0.5)
        else:
            r[i].now = min(r[i].initial, r[i].now + 0.5)
        if(r[i].status):
            air=AirCondition.objects.get(id=i+1)

            airbill=AirBill.objects.filter(room_id=i+1).last()

            airbill.one_time_price=r[i].money-float(air.total_price)

            airbill.save()
    airconditions=AirCondition.objects.all()
    i=0
    for ac in airconditions:
        ac.current_temperature=r[i].now
        ac.save()
        i+=1





