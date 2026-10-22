from idcard_generator.id_card_gui import IDGen
from idcard_generator.time_check import check_time_limit

# 检查程序时间限制
check_time_limit()

id_gen = IDGen()
id_gen.run()
