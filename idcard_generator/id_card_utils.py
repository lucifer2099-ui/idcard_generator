import datetime
import random
import calendar


# 计算最后一位校验码
class IdentityCard:
    __Wi = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]
    __Ti = ['1', '0', 'x', '9', '8', '7', '6', '5', '4', '3', '2']

    @staticmethod
    def check(code):
        return len(code) == 17

    @staticmethod
    def calculate(code):
        sum_value = 0
        for i in range(17):
            sum_value += int(code[i]) * IdentityCard.__Wi[i]
        return IdentityCard.__Ti[sum_value % 11]


# 徐州市区县代码列表
XUZHOU_AREA_CODES = [
    '320302',  # 鼓楼区
    '320303',  # 云龙区
    '320305',  # 贾汪区
    '320311',  # 泉山区
    '320312',  # 铜山区
    '320321',  # 丰县
    '320322',  # 沛县
    '320324',  # 睢宁县
    '320381',  # 新沂市
    '320382'   # 邳州市
]

# 随机生成身份证号
def random_card_no(prefix='', year='', month='', day='', sex=None):
    if len(prefix) < 6:
        # 默认使用徐州市随机区县的编码
        prefix = random.choice(XUZHOU_AREA_CODES)
    else:
        prefix = prefix[0:6]

    if len(year) > 0:
        year = str(year).zfill(4)
        # 确保指定的年份不早于1980年
        if int(year) < 1980:
            year = str(1980)
    else:
        year = str(random.randint(1980, 2020))

    if len(month) > 0:
        month = str(month[0:2]).zfill(2)
    else:
        month = str(random.randint(1, 12)).zfill(2)

    if len(day) > 0:
        day = str(day).zfill(2)
    else:
        day = str(random.randint(1, 28)).zfill(2)

    # 生成顺序码（15-17位），其中第17位表示性别
    # 第15-16位：随机生成
    seq_first = str(random.randint(0, 99)).zfill(2)
    
    # 第17位：根据性别生成，奇数为男，偶数为女
    if sex is None:
        # 如果没有指定性别，随机生成
        seq_last = str(random.randint(0, 9))
    elif sex == 1:  # 男性
        # 生成奇数
        seq_last = str(random.choice([1, 3, 5, 7, 9]))
    elif sex == 0:  # 女性
        # 生成偶数
        seq_last = str(random.choice([0, 2, 4, 6, 8]))
    else:
        # 默认随机生成
        seq_last = str(random.randint(0, 9))
    
    rand_value = seq_first + seq_last

    card_17 = prefix + year + month + day + rand_value
    vi_code = IdentityCard.calculate(card_17)
    return card_17 + vi_code


# 随机生成身份证号
def random_day(year=2020, month=2):
    monthRange = calendar.monthrange(year, month)
    return random.randint(1, monthRange[1])


# 生成身份证有效期限（严格的20年，结束日期在2030年之后）
def generate_validity_period():
    # 随机生成起始年份，从当前年份往前推5-15年
    current_year = datetime.datetime.now().year
    start_year = random.randint(current_year - 15, current_year - 5)
    
    # 确保起始年份不会导致20年后仍在2030年前
    min_start_year = 2030 - 20
    if start_year < min_start_year:
        start_year = min_start_year
    
    start_month = random.randint(1, 12)
    start_day = random.randint(1, 28)
    start_time = datetime.datetime(start_year, start_month, start_day)
    
    # 计算结束时间（严格的20年后，保持相同的月日）
    expire_time = datetime.datetime(start_time.year + 20, start_time.month, start_time.day)
    
    return start_time.strftime("%Y.%m.%d"), expire_time.strftime("%Y.%m.%d")


# 身份证起始日（保留原函数名以保持兼容性）
def get_start_time():
    start_time, _ = generate_validity_period()
    return start_time


# 身份证到期日（保留原函数名以保持兼容性）
def get_expire_time():
    _, expire_time = generate_validity_period()
    return expire_time


def test():
    code = random_card_no()  # 17位身份证
    print(code)
    if IdentityCard.check(code):
        print("你的校验位为:%s" % IdentityCard.calculate(code))


if __name__ == '__main__':
    test()
