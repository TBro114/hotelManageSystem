import json
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
from publicModels.models import CentralAirCondition, AirCondition, AirServiceLog, Room, Customer,AirBill
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Max
from global_count import cou
from supervise.views import News,new_s
change=0

# 登录视图
def login(request):
    if request.method == 'POST':
        # 获取用户输入的用户名（顾客姓名）和房间号
        username = request.POST.get('username')
        room_id = request.POST.get('room_number')  # 获取房间号

        try:
            # 查找房间信息
            room = Room.objects.get(id=room_id)

            # 检查该房间是否有分配给顾客
            if room.customer:
                customer = room.customer

                # 检查输入的用户名（顾客姓名）是否与房间内的顾客匹配
                if customer.name == username:
                    # 如果用户名和房间号匹配，登录成功
                    request.session['room_id'] = room.id  # 将房间 ID 存储到 session 中
                    return redirect('control')  # 登录成功后跳转到控制面板
                else:
                    messages.error(request, '用户名与房间号不匹配！')
            else:
                messages.error(request, '该房间没有分配给任何顾客！')

        except Room.DoesNotExist:
            messages.error(request, '房间号不存在！')

    return render(request, 'customerlogin.html')  # 如果是 GET 请求，显示登录页面

# 控制面板视图
def controlPanel(request):


    # 检查 session 中是否存储了登录用户的房间 ID
    if 'room_id' not in request.session:
        return redirect('customerloginlogin')  # 如果没有登录，则跳转到登录页面

    room_id = request.session['room_id']

    try:
        # 根据 room_id 获取当前的 Room 对象
        room = Room.objects.get(id=room_id)
        #检查房间是否分配了顾客，没有则清除session
        if room.customer is None:
            del request.session['room_id']
            return redirect('customerloginlogin')
        air_record = AirCondition.objects.get(pk=request.session['room_id'])
    except Room.DoesNotExist:
        # 如果房间不存在，重定向到登录页面或其他错误页面
        return redirect('customerloginlogin')



    if request.method == "GET":
        # 获取中央空调数据表
        centralaircondition = CentralAirCondition.objects.all().first()
        # 使用 filter() 获取所有符合条件的记录，并用 last() 获取最后一条记录
        airbill = AirBill.objects.filter(room=room).last()
        rangedict = {
            'max_temperature_cold:': centralaircondition.max_temperature_cold,
            'min_temperature_cold:': centralaircondition.min_temperature_cold,
            'max_temperature_hot:': centralaircondition.max_temperature_hot,
            'min_temperature_hot:': centralaircondition.min_temperature_hot,
        }
        speeddict={
            1:'低风速',
            2:'中风速',
            3:'高风速'
        }
        air_record.speed=speeddict[air_record.speed]
        airbill.one_time_price = f"{airbill.one_time_price:06.2f}"
        air_record.total_price=f"{ air_record.total_price:06.2f}"
        # air_record.target_temperature=f"{ air_record.target_temperature:04.1f}"

        return render(request, 'control.html', {'room': room, 'air_record': air_record, 'rangedict': rangedict,'airbill':airbill})

def get_air_condition(request):
    if request.method == 'GET':  # 确保处理 GET 请求
        try:
            # 获取房间 ID
            room_id = request.session.get('room_id')

            if not room_id:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Room ID not found in session.'
                }, status=400)  # 返回 400 错误，表示请求无效

            # 获取该房间对象
            room = Room.objects.get(id=room_id)
            centralaircondition = CentralAirCondition.objects.all().first()

            # 获取对应的空调记录，如果没有则创建
            
            air_record,created = AirCondition.objects.get_or_create(room=room)
            airbill = AirBill.objects.filter(room=room).last()
            air_record.current_temperature=f"{air_record.current_temperature:04.1f}"
            air_record.target_temperature=f"{air_record.target_temperature:04.1f}"
            print(air_record.target_temperature)
            air_record.total_price=f"{air_record.total_price:06.2f}"
            if(airbill):
                airbill.one_time_price = f"{airbill.one_time_price:06.2f}"
            else:
                airbill={
                    'one_time_price':"000.00"
                } 
        
        
                
            # print(airbill.one_time_price)

            # 返回空调状态信息
            if air_record.airCondition_mode!='sun':
                return JsonResponse({
                    'status': 'success',
                    'air_record': {
                        'central_aircondition': centralaircondition.central_aircondition_status,
                        'airCondition_status': air_record.airCondition_status,
                        'airCondition_mode': centralaircondition.mode,
                        'airCondition_current_temp':air_record.current_temperature,
                        'airCondition_target_temp':air_record.target_temperature,
                        'airCondition_speed':air_record.speed,
                        'airCondition_bill':air_record.total_price,
                        'airCondition_current_bill':airbill.one_time_price,
                        'max_temp':centralaircondition.max_temperature_cold,
                        'min_temp':centralaircondition.min_temperature_cold,
                    }
                })
            else:
                return JsonResponse({
                    'status': 'success',
                    'air_record': {
                        'central_aircondition': centralaircondition.central_aircondition_status,
                        'airCondition_status': air_record.airCondition_status,
                        'airCondition_mode': air_record.airCondition_mode,
                        'airCondition_current_temp':air_record.current_temperature,
                        'airCondition_target_temp':air_record.target_temperature,
                        'airCondition_speed':air_record.speed,
                        'airCondition_bill':air_record.total_price,
                        'airCondition_current_bill':airbill.one_time_price,
                        'max_temp':centralaircondition.max_temperature_hot,
                        'min_temp':centralaircondition.min_temperature_hot,
                        'mode':centralaircondition.mode,
                    }
                })
        except ObjectDoesNotExist:
            # 如果找不到 Room 对象或其他相关对象，返回错误
            return JsonResponse({
                'status': 'error',
                'message': 'Room or AirCondition not found.'
            }, status=404)
        except Exception as e:
            # 捕获所有其他异常并返回 500 错误
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=500)






@csrf_exempt
def update_air_condition(request):
    global change,cou
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            # print("接收到的数据:", data)

            # 获取房间 ID，从 session 中获取
            room_id = request.session.get('room_id')
            if not room_id:
                return JsonResponse({'status': 'error', 'message': '未找到房间信息'}, status=400)

            # 获取房间对象
            room = Room.objects.get(id=room_id)

            # 获取该房间对应的空调对象，若没有则创建
            air_record, created = AirCondition.objects.get_or_create(room=room)

            # 打印获取到的空调记录和数据
            # print(f"当前空调记录：{air_record}, 数据：{data}")
            change = data.get('service_type',change)
            # print(change)

            # 更新空调记录
            air_record.current_temperature = data.get('current_temperature', air_record.current_temperature)
            air_record.target_temperature = data.get('target_temperature', air_record.target_temperature)
            air_record.speed = data.get('current_speed', air_record.speed)
            air_record.airCondition_status = data.get('airCondition_status', air_record.airCondition_status)
            air_record.save()  # 保存空调记录
            # air_record.target_temperature=f"{air_record.target_temperature:04.1f}"
            time=cou.counter
           

            if change ==1:
                # print(air_record.airCondition_status)
                temp=News(time,room_id,1,air_record.airCondition_status)
                new_s.append(temp)

            elif change ==2:
                # print(air_record.target_temperature)
                temp=News(time,room_id,2,air_record.target_temperature)
                new_s.append(temp)
            elif change ==3:
                # print(air_record.speed)
                temp=News(time,room_id,3,air_record.speed)
                new_s.append(temp)
            else:
                print(0)
            for new in new_s:
                print('-----------------------------------------')
                print("房间号",new.r)
                print("value",new.value)

            # air_record.save()  # 保存到数据库
            # air_service_log = AirServiceLog.objects.create(airCondition=air_record,service_type=data.get('service_type'),
            #                                    current_speed=data.get('current_speed'),room=room)
            # air_service_log.save()  # 保存到数据库

            # 返回成功响应，并附带更新的空调记录
            return JsonResponse({
                'status': 'success',
                'message': '空调设置已更新',
                'air_record': {
                    'current_temperature': air_record.current_temperature,
                    'target_temperature': air_record.target_temperature,
                    'current_speed': air_record.speed,
                    'airCondition_status': air_record.airCondition_status,
                    'airCondition_mode': air_record.airCondition_mode,
                }
            })

        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)




def logout_view(request):
    # 清除 session 中的 room_id，退出登录
    if 'room_id' in request.session:
        del request.session['room_id']
        messages.info(request, '成功退出登录')

    # 重定向到登录页面
    return redirect('customerloginlogin')  # 假设你有一个名为 'customerloginlogin' 的 URL 来显示登录页面
