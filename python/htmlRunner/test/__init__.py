# 数据引用计数
data = {}
l = []
s = [1,2,3]
data["l"] = l
data["d"] = l
for i in s:
    data["d"].append(i)
print(id(data["l"]), id(l))

print(data)