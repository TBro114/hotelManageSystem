from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    ROLE_CHOICES = [
        ('front_desk', '前台'),
        ('ac_manager', '空调管理员'),
        ('hotel_manager', '酒店经理'),
    ]

    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    secret_key = models.CharField(max_length=255, blank=True, null=True)
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=255)

    class Meta:
        db_table = 'user'


class Customer(models.Model):
    name = models.CharField(max_length=100)
    identity_card = models.CharField(max_length=100)


    class Meta:
        db_table = 'customer'


class Room(models.Model):
    room_price = models.IntegerField(null=True, blank=True)
    room_status = models.IntegerField(default=0, null=True, blank=True)
    airConditioner = models.ForeignKey('AirCondition', on_delete=models.CASCADE)
    customer = models.ForeignKey('Customer', on_delete=models.DO_NOTHING, null=True, blank=True,default=None)

    class Meta:
        db_table = 'room'

    def __str__(self):
        # 返回房间号和价格，您可以根据需求定制显示的内容
        return f"Room {self.id} - ￥{self.room_price}"


class AirCondition(models.Model):
    SPEED_CHOICES = [
        ('1', '低风速'),
        ('2', '中风速'),
        ('3', '高风速'),
        ]
    airCondition_status = models.IntegerField(default=0)
    target_temperature = models.IntegerField(null=True, blank=True)
    current_temperature = models.FloatField(null=True, blank=True)
    speed = models.IntegerField(null=True, blank=True, default=1, choices=SPEED_CHOICES)
    airCondition_mode = models.CharField(max_length=100, default='cold')
    total_price = models.DecimalField(
        max_digits=5,  # 包括整数和小数的总位数
        decimal_places=2,  # 小数点后位数
        null=True,
        blank=True,
        default=000.00,
    )

    class Meta:
        db_table = 'aircondition'


class CentralAirCondition(models.Model):
    MODE_CHOICES = [
        ('cold', '制冷'),
        ('sun', '制热'),
        ('dry', '除湿'),
        ('wind', '送风'),
        ]

    max_temperature_cold = models.IntegerField(null=True, blank=True)
    min_temperature_cold = models.IntegerField(null=True, blank=True)
    max_temperature_hot = models.IntegerField(null=True, blank=True)
    min_temperature_hot = models.IntegerField(null=True, blank=True)
    price_rate = models.IntegerField(null=True, blank=True)
    mode = models.CharField(max_length=100, default='cold',choices=MODE_CHOICES)
    central_aircondition_status = models.IntegerField(default=0)

    class Meta:
        db_table = 'central_air_condition'


class AirServiceLog(models.Model):
    request_time = models.IntegerField(null=True, blank=True)
    airCondition = models.ForeignKey('AirCondition', on_delete=models.CASCADE)
    room = models.ForeignKey('Room', on_delete=models.CASCADE,null=True, blank=True)
    start_time = models.IntegerField(null=True, blank=True)
    end_time = models.IntegerField(null=True, blank=True)
    service_price = models.FloatField(null=True, blank=True)
    service_type = models.CharField(max_length=20, null=True, blank=True)
    current_speed = models.IntegerField(default=1, null=True, blank=True)

    class Meta:
        db_table = 'air_service_log'

    # def save(self, *args, **kwargs):
    #     if self.start_time and self.end_time:  # 检查时间字段是否非空
    #         time_difference = (self.end_time - self.start_time).total_seconds() / 3600  # 转为小时
    #         price_rate = CentralAirCondition.objects.first().price_rate if CentralAirCondition.objects.exists() else 1  # 获取 price_rate，默认值为 1
    #         self.service_price = int(time_difference * self.current_speed * price_rate)  # 计算服务价格
    #     else:
    #         self.service_price = 0  # 如果时间字段为空，设置默认值为 0
    #     super().save(*args, **kwargs)  # 调用父类的 save 方法


class Detail(models.Model):
    room = models.ForeignKey('Room', on_delete=models.CASCADE, default=1)
    check_in_time = models.DateTimeField(null=True, blank=True)
    stay_days = models.IntegerField(default=1,null=True, blank=True)
    status = models.IntegerField(null=True, blank=True, default=1)

    class Meta:
        db_table = 'detail'

class AirBill(models.Model):
    room = models.ForeignKey('Room', on_delete=models.CASCADE)
    one_time_price = models.FloatField(null=True, blank=True,default=0)
    flag = models.IntegerField()
    class Meta:
        db_table = 'airbill'