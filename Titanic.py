import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams['font.sans-serif']=['SimHei']
plt.rcParams['axes.unicode_minus']=False

train = pd.read_csv('train.csv')

# 任务一：查看数据集
print(train)
# 倘若要查看完整代码，则取消下一行代码的注释
# print(train.to_string())

# 任务二：统计存活率，绘制饼状图
survived_count = train[train['Survived'].isin([1])].shape[0]
print("survived:",survived_count)
dead_count = train[train['Survived'].isin([0])].shape[0]
print("dead:",dead_count)

pie_x = [survived_count,dead_count]
pie_label = ['存活率', '死亡率']

fig,pie_ax = plt.subplots(num=1,figsize = (6,6))
pie_ax.pie(x=pie_x,explode = [0,0.1],labels = pie_label,
           autopct='%1.2f%%',pctdistance = 0.4,shadow=True,
           labeldistance = 0.55,textprops={'fontsize':15})
plt.figure(num = 1)
plt.show()

# 任务二：统计不同性别的生还率

temp1 = train[train['Survived'].isin([1])]
male_survived_count = temp1[temp1["Sex"].isin(["male"])].shape[0]
print("male_survived:",male_survived_count)
female_survived_count = len(temp1) - male_survived_count
print("female_survived:",female_survived_count)

temp2 = train[train["Survived"].isin([0])]
male_dead_count = temp2[temp2["Sex"].isin(["male"])].shape[0]
print("male_dead_count:",male_dead_count)
female_dead_count = len(temp2) - male_dead_count
print("female_dead_count:",female_dead_count)

fig,pie_ax2 = plt.subplots(1,3,num=2,figsize = (14,8))
pie_ax2[0].pie(x = [male_survived_count,female_survived_count],autopct = '%1.2f%%',
               labels = ["男性生还率","女性生还率"],textprops={'fontsize':11},
               shadow = True,explode = [0.1,0],pctdistance = 0.4,
               labeldistance = 0.55)

pie_ax2[1].pie(x = [male_dead_count,male_survived_count],labels = ["死亡率","存活率"],
               autopct = '%1.2f%%',pctdistance = 0.35,
               labeldistance = 0.55)
pie_ax2[1].set_title("男性存活率",fontsize = 12,pad = 20)

pie_ax2[2].pie(x = [female_dead_count,female_survived_count],labels = ["死亡率","存活率"],
               autopct = '%1.2f%%',pctdistance = 0.35,
               labeldistance = 0.55)
pie_ax2[2].set_title("女性存活率",fontsize = 12,pad = 20)
plt.figure(num = 2)
plt.show()

# 任务三：绘制不同年龄段的存活率（条形图）
age_range = train["Age"]
print("age_range",age_range)
period_num,_ = np.histogram(age_range,bins=16,range = [0,80])
print("period_num",period_num)
period_survived_num = []
for age in range(5,81,5):
    survived_num = train.loc[(age_range>=age-5)&(age_range<=age),"Survived"].sum()
    period_survived_num.append(survived_num)
print("period_survived_num",period_survived_num)

fig,ax3 = plt.subplots(num = 3,figsize = (8,8))
ax3.bar(x=np.arange(2.5,78.5,5),height=period_survived_num,
        width = 5,label = "存活数")
ax3.bar(x=np.arange(2.5,78.5,5),height=period_num,
        width = 5,alpha = 0.6,label = "总人数")
ax3.set_xticks(np.arange(0,81,5))
ax3.set_yticks(np.arange(0,120,10))
ax3.set_title("不同年龄段的存活率",fontsize = 15)
ax3.grid(alpha = 0.3,linestyle=':')
ax3.legend()
plt.figure(num = 3)
plt.show()