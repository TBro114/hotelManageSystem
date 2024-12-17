from django.shortcuts import render,get_object_or_404
from publicModels.models import Room,AirCondition,AirBill,Detail,AirServiceLog
from django.http import JsonResponse,FileResponse,HttpResponse
from django.db.models import Sum
from django.core.paginator import Paginator, EmptyPage
import json
import openpyxl
from openpyxl import Workbook
from django.views.decorators.csrf import csrf_exempt
from io import BytesIO
import pandas as pd
import json

def charge(request):
    if request.method == 'POST':
        room_id = request.POST.get('roomId')
        room = Room.objects.get(id=room_id)
        airCondition = AirCondition.objects.get(id=room_id)
        # detail = Detail.objects.get(room_id = room_id)
        air_bills = AirBill.objects.filter(room = room)
        total_ac_price = air_bills.aggregate(total=Sum('one_time_price'))


        if room:
            days_stayed = AirBill.objects.filter(room = room).count()
            room_rate = room.room_price
            accommodation_cost = days_stayed * room_rate
            air_conditioning_cost = total_ac_price['total']
            total_cost = accommodation_cost + air_conditioning_cost

            
            airCondition.airCondition_status = 0
            # detail.stay_days = days_stayed
            room.save()
            airCondition.save()
            # detail.save()

            context = {
                'room_id':room_id,
                'days_stayed': days_stayed,
                'room_rate': room_rate,
                'accommodation_cost': accommodation_cost,
                'air_conditioning_cost': air_conditioning_cost,
                'total_cost': total_cost,
            }
            return render(request, 'charge.html', context)
        else:
            return render(request, 'charge.html', {'error': 'Room not found'})
    else:
        return render(request, 'charge.html')
   
def acDetailRecord(request):
    room_id = request.GET.get('room_id')  # 通过GET请求参数获取
    air_service_logs = None

    # 如果有room_id参数，获取对应的Room记录，否则获取所有的Room记录
    if room_id and room_id!="None":
        print(type(room_id),"************************************************************")
        room = get_object_or_404(Room, id=room_id)  # 获取对应的Room对象
        air_service_logs = AirServiceLog.objects.filter(room=room)  # 过滤该Room的空调服务记录
    else:
        air_service_logs = AirServiceLog.objects.all()  # 获取所有空调服务记录

    # 如果请求是DELETE方法，删除指定的记录
    if request.method == 'DELETE':
        room_id = request.GET.get('room_id')  # 获取要删除的记录ID
        if room_id:
            try:
                room = get_object_or_404(Room, id=room_id)  # 获取对应的Room对象
                customer=room.customer
                customer.delete()
                room.customer=None
                room.room_status = 0
                room.save()
                return JsonResponse({'success': True})  # 返回删除成功的JSON响应
            except AirServiceLog.DoesNotExist:
                return JsonResponse({'success': False, 'message': '记录未找到'}, status=404)
        else:
            return JsonResponse({'success': False, 'message': '没有提供room_id'}, status=400)

    # 分页：根据每页记录数动态设置
    paginator = Paginator(air_service_logs, 3)  # 在这里传入已经筛选后的记录

    # 获取当前页码，如果没有传递页码，则默认为第 1 页
    page_number = request.GET.get('page', 1)

    # 防止非法页码（页码小于1）
    try:
        page_number = int(page_number)
        if page_number < 1:
            page_number = 1  # 强制将页码设为 1
    except ValueError:
        page_number = 1  # 默认设置页码为 1

    # 获取当前页的数据
    try:
        page_obj = paginator.get_page(page_number)
    except EmptyPage:
        # 如果页码不合法（例如小于 1 或大于总页数），则跳转到第一页
        page_obj = paginator.get_page(1)

    # 将分页后的记录传递给模板
    return render(request, "acDetailRecord.html", {"page_obj": page_obj, "per_page":3,"room_id":room_id,"air_service_logs":air_service_logs})

@csrf_exempt
def export_to_excel(request):
    if request.method == 'POST':
        # 解析JSON数据
        data_json = json.loads(request.body)
        room_id = data_json['room_id']
        days_stayed = data_json['days_stayed']
        room_rate = data_json['room_rate']
        accommodation_cost = data_json['accommodation_cost']
        air_conditioning_cost = data_json['air_conditioning_cost']
        total_cost = data_json['total_cost']

        # 创建数据字典
        data = {
            '房间号': [room_id],
            '住宿天数': [days_stayed],
            '客房单价': [room_rate],
            '住宿费用': [accommodation_cost],
            '空调费用': [air_conditioning_cost],
            '总费用': [total_cost]
        }
        
        # 创建DataFrame
        df = pd.DataFrame(data)
        
        # 将DataFrame转换为Excel文件内容
        excel_file = 'bills.xlsx'
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False)
        
        # 移动到流的开始
        output.seek(0)
        
        # 设置响应头，告诉浏览器这是一个文件下载
        response = HttpResponse(output, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = f'attachment; filename="{excel_file}"'
        
        return response
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)