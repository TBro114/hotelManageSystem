from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from publicModels.models import Customer,Detail,AirBill,Room,AirServiceLog,AirCondition
from django.utils.dateparse import parse_datetime


# Create your views here.

def customerInfor(request):
    if request.method == 'POST':
        # 获取用户输入的数据
        name = request.POST.get('name')
        id_number = request.POST.get('id_number')
        checkin_time = request.POST.get('checkin_time')

        # 解析入住时间
        parsed_checkin_time = parse_datetime(checkin_time)
        if not parsed_checkin_time:
            return render(request, 'error.html', {'error': '时间格式错误'})

        # 重定向到成功页面或其他页面
        return HttpResponseRedirect(f'/checkIn/roomInquiry?name={name}&identity_card={id_number}&check_in_time={checkin_time}')

    # 如果是 GET 请求，返回表单页面
    return render(request, 'customerInfor.html')

def roomInquiry(request):
    rooms = Room.objects.all()
    identity_card = request.GET.get('identity_card')
    check_in_time = request.GET.get('check_in_time')
    name = request.GET.get('name')
    print(rooms)

    # 如果是 POST 请求，表示用户提交了表单
    if request.method == 'POST':
        selected_room_id = request.POST.get('selected_room_id')
        name = request.GET.get('name')
        identity_card = request.GET.get('identity_card')
        check_in_time = request.GET.get('check_in_time')
        room = Room.objects.get(id = selected_room_id)
        AirServiceLog.objects.filter(room = room).delete()
        AirBill.objects.filter(room = room).delete()
        aircondition=AirCondition.objects.get(id=selected_room_id)
        aircondition.total_price=0
        aircondition.save()
        room.room_status = 1
        cus=Customer.objects.create(name = name,identity_card = identity_card)
        room.customer=cus
        room.save()
        last_airbill = AirBill.objects.filter(room=room).last()
        # 计算新 AirBill 的 flag 值
        new_flag = (last_airbill.flag + 1) if last_airbill else 1
        airbill= AirBill.objects.create(room = room,flag=new_flag)
        Detail.objects.create(check_in_time=check_in_time,room = room)

        return render(request,'roomInquiry.html',{'room':rooms})
    
    return render(request, 'roomInquiry.html',{'room':rooms,'identity_card':identity_card,'check_in_time':check_in_time,'name':name})