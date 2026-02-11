sen ="Agent:007_Bond; Coords:(40,74); Items:gun,money,gun;Mission:2025-RESCUE-X"
sen_no_space = sen.replace(" ","")
print("去除空格后的情报：",sen_no_space)
items = set()

unit = sen_no_space.split(";")
print("unit: ",unit)
temp_items = unit[2].split(":")
print("temp_items: ",temp_items)
temp_dou_items = temp_items[1].split(",")
n = len(temp_dou_items)
print("n: ",n)
for i in range(n):
    items.add(temp_dou_items[i])
print("items: ",items)
mission = unit[3].split(":")
mission = mission[1]
print("mission: ",mission)
temp_coord = unit[1].split(":")
print("temp_coord: ",temp_coord)
temp_dou_coord = temp_coord[1][1:-1]
print("temp_dou_coord: ",temp_dou_coord)
temp_thr_coord = temp_dou_coord.split(",")
print("tem_thr_coord: ",temp_thr_coord)
coord = (int(temp_thr_coord[0]),int(temp_thr_coord[1]))
print("coord: ",coord)
temp_agent = unit[0]
start_leagal = temp_agent.find(":")
agent = temp_agent[start_leagal+1:]
print("agent: ",agent)
result = {
    "agent": agent,
    "coord": coord,
    "items": items,
    "mission": mission,
}
print("result: ",result)