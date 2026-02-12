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
