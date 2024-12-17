import pandas as pd

class News:
    def __init__(self, time: int=0, r: int=0, type: int=0, value: int=0):
        self.time = time  # 申请的时间
        self.r = r        # 房间号
        self.type = type  # 申请类型
        self.value = value  # 申请的值


def testScriptFunction():
    # 指定文件路径
    file_path = "./系统测试用例冷.xlsx"

    # 指定表名
    sheet_name = "测试用例"

    # 读取指定表
    data = pd.read_excel(file_path, sheet_name=sheet_name)

    # 选取某部分内容（假设选取第1-3行，第1-2列）
    subset = data.iloc[2:28, 0:6]  # 行列从0开始计数

    list = []

    # 遍历 subset 中的每一行
    for i in range(len(subset)):

        row = subset.iloc[i]  # 提取第 i 行

        for j in range(1, len(row)):
            if pd.notna(row.iloc[j]):
                if row.iloc[j]=='开机' or row.iloc[j]=='关机':
                    new=News(time=row.iloc[0]+1)
                    new.r=j
                    new.type=1
                    if row.iloc[j]=='开机':
                        new.value=1
                    else:
                        new.value=0
                    list.append(new)
                elif row.iloc[j]=='高' or row.iloc[j]=='中' or row.iloc[j]=='低':
                    new=News(time=row.iloc[0]+1)
                    new.r=j
                    new.type=3
                    if row.iloc[j]=="高":
                        new.value=3
                    elif row.iloc[j]=="中":
                        new.value=2
                    else:
                        new.value=1
                    list.append(new)
                else:
                    value_str = str(row.iloc[j])
                    if '，' in value_str:  # 检查是否包含逗号
                        # 分割值并创建新的News对象
                        parts = value_str.split('，')
                        for part in parts:
                            new = News(time=row.iloc[0]+1)
                            new.r = j
                            if part=='高' or part=='中' or part=='低':
                                new.type=3
                                if part=='高':
                                    new.value=3
                                elif part=="中":
                                    new.value=2
                                else:
                                    new.value=1
                            else:
                                new.type=2
                                new.value=part
                            list.append(new)
                    else:
                        new = News(time=row.iloc[0]+1)
                        new.r = j
                        new.type = 2
                        new.value = row.iloc[j]
                        list.append(new)

    return list
    
                
