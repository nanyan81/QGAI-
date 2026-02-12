# 传统方法
old_methon = []
for i in range(1,11):
    old_methon.append(i*i)

print(old_methon)

# 列表推导式
new_methon = [i*i for i in range(1,11)]

print(new_methon)

# 加QG前缀(不采用map)
add_QG = lambda name : "QG_" + name
new_name_list = []
old_name_list = ["张三","李四"]
for i in range(len(old_name_list)):
    new_name_list.append(add_QG(old_name_list[i]))
print("new_name_list",new_name_list)
print("old_name_list",old_name_list)

# 加QG前缀(采用map)
old_Name = ["王五","赵六"]
new_Name = map(add_QG, old_Name)
print("new_Name",list(new_Name))
print("old_Name",old_Name)

# 数据清洗
raw_data = ["85", "92", "ERROR", "105", "78", "WARNING", "99", "120"]

new_data = []
for i in range(len(raw_data)):
    try:
        float(raw_data[i])
    except ValueError:
        raw_data[i] = raw_data[i]
    else:
        new_data.append(float(raw_data[i])/100.0)

print("raw_data",raw_data)
print("new_data",new_data)

verify = lambda x : "核心过载 "+str(x) if x > 1 else "运转正常 " + str(x)

final_data =list(map(verify, new_data))
print("final_data",final_data)
