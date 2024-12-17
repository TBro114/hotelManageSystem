class Room:
    def __init__(self, num, status, ser, initial, set_temp, now, wind, money, time):
        self.num = num
        self.status = status
        self.ser = ser
        self.initial = initial
        self.set = set_temp
        self.now = now
        self.wind = wind
        self.money = money
        self.time = time

    def __str__(self):
        return f"room:{str(self.num)}, state:{self.status}, now:{self.now}, set:{self.set}, wind:{self.wind}, money:{self.money}, time:{str(self.time)}, ser:{str(self.ser)}"


class News:
    def __init__(self, time, r, type_, value):
        self.time = time
        self.r = r
        self.type = type_
        self.value = value


wait = [None] * 5
service = [None] * 5
wn = 0
level = ["", "L", "M", "H"]

new_s = [
News(1, 1, 1, 1),
News(2, 1, 2, 24),
News(2, 2, 1, 1),
News(3, 3, 1, 1),
News(4, 2, 2, 25),
News(4, 4, 1, 1),
News(4, 5, 1, 1),
News(5, 3, 2, 27),
News(5, 5, 3, 3),
News(6, 1, 3, 3),
News(8, 5, 2, 24),
News(10, 1, 2, 28),
News(10, 4, 2, 28),
News(10, 4, 3, 3),
News(12, 5, 3, 2),
News(13, 2, 3, 3),
News(15, 1, 1, 0),
News(15, 3, 3, 1),
News(17, 5, 1, 0),
News(18, 3, 3, 3),
News(19, 1, 1, 1),
News(19, 4, 2, 25),
News(19, 4, 3, 2),
News(21, 2, 2, 27),
News(21, 2, 3, 2),
News(21, 5, 1, 1),
News(25, 1, 1, 0),
News(25, 3, 1, 0),
News(25, 5, 1, 0),
News(26, 2, 1, 0),
News(26, 4, 1, 0),
]

r = [
    Room(1, 0, 0, 10, 22, 10, 2, 0, 0),
    Room(2, 0, 0, 15, 22, 15, 2, 0, 0),
    Room(3, 0, 0, 18, 22, 18, 2, 0, 0),
    Room(4, 0, 0, 12, 22, 12, 2, 0, 0),
    Room(5, 0, 0, 14, 22, 14, 2, 0, 0),
]

p = 0  # 指向下一个要处理的消息


def Set(n):
    global p, wn
    h = 0
    while True:
        if p >= len(new_s):
            return h
        h = 1
        a = new_s[p]
        if a.time > n:
            return h
        if a.type == 1:
            r[a.r - 1].status = a.value
            if a.value:
                wait[wn] = r[a.r - 1]
                wn += 1
            else:
                r[a.r - 1].set = 22
                r[a.r - 1].wind = 2
        elif a.type == 2:
            r[a.r - 1].set = a.value
        else:
            r[a.r - 1].wind = a.value
        p += 1


def SORT():
    global wn
    wait.sort(key=lambda x: (x.wind if x else 0, x.time if x else 0, -x.num if x else 0, x is None), reverse=True)
    service.sort(key=lambda x: (x.wind if x else 0, x.time if x else 0, -x.num if x else 0, x is None), reverse=True)
    wn = sum(1 for x in wait if x is not None)


def schedule():
    global wn
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
    for i in range(3):
        if service[i] and not service[i].status:
            service[i].ser = False
            service[i].time = 0
            service[i] = None
            free += 1

        elif service[i] and service[i].set <= service[i].now:
            service[i].ser = False
            service[i].time = 0
            wait[i + wn] = service[i]
            service[i] = None
            free += 1

    # 填补空缺
    for i in range(wn):
        if free > 0 and wait[i] and wait[i].set > wait[i].now:
            wait[i].ser = True
            wait[i].time = 0
            service[4 - i] = wait[i]
            wait[i] = None
            free -= 1

    # 风速调整
    for i in range(wn):
        if wait[i] and wait[i].set > wait[i].now:
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
                    break

    # 等待足够时切换
    for i in range(wn):
        if wait[i] and wait[i].set > wait[i].now and wait[i].time >= 2:
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
                    break
    SORT()


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


def settle():
    for i in range(5):
        if r[i].ser:
            r[i].now = min(r[i].set, 1.0 / (4.0 - r[i].wind) + r[i].now)
            r[i].money += 1.0 / r[i].wind
        elif r[i].status:
            if r[i].set <= r[i].now:
                r[i].now = max(r[i].initial, r[i].now - 0.5)
        else:
            r[i].now = max(r[i].initial, r[i].now - 0.5)


if __name__ == "__main__":
    i = 1
    while True:
        while True:
            if Set(i):
                break
        schedule()
        show(i)
        settle()
        i += 1