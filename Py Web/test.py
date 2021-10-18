from random import shuffle,seed
import time
seed(time.time())
a = [1,1,1,1,1,1,2,2,2,2,2,2,6,6,6,6,10,10,10,10,1,1,1,1,2,2,2,2,3,3,3,3]
ct = {2:0,4:0,6:0,20:0}
for i in range(1000):
    ts = sum(a[:len(a)//2])-sum(a[len(a)//2:])

    if(abs(ts)<=2): ct[2]+=1
    elif(abs(ts)<=4): ct[4]+=1
    elif(abs(ts)<=6): ct[6]+=1
    else: ct[20]+=1

    shuffle(a)

for i in ct.values():
    print(i)

# 吴晗 韩柏林 刘思佳
# 赵范佑 张喜瑞 刘力源
# 老段 * 3
# 猎马人 * 3
# 孙文彬 *3
# 张鋆枻 江克威 张一帆