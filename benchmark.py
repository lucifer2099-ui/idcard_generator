import timeit

setup = """
name_body_ming = ['壮', '昱杰', '开虎', '凯信', '永斌', '方洲', '长发', '可人', '天弘', '炫锐', '富明', '俊枫']
name_body_ming2 = '伟刚勇毅俊峰强军平保东文辉力明永健世广志义兴良海山仁波宁贵福生龙元全国胜学祥才发武新利清飞彬富顺信子杰涛昌成康星光天达安岩中茂进林有坚和彪博诚先敬震振壮会思群豪心邦承乐绍功松善厚庆磊民友裕河哲江超浩亮政谦亨奇固之轮翰朗伯宏言若鸣朋斌梁栋维启克伦翔旭鹏泽晨辰士以建家致树炎德行时泰盛雄琛钧冠策腾楠榕风航弘'
"""

loop_test = """
result = list(name_body_ming)
for everyChar in name_body_ming2:
    result.append(everyChar)
"""

extend_test = """
result = list(name_body_ming)
result.extend(name_body_ming2)
"""

n = 100000

loop_time = timeit.timeit(loop_test, setup=setup, number=n)
extend_time = timeit.timeit(extend_test, setup=setup, number=n)

print(f"Loop time: {loop_time:.4f} s")
print(f"Extend time: {extend_time:.4f} s")
print(f"Improvement: {(loop_time - extend_time) / loop_time * 100:.2f}%")
