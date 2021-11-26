from NetworkManager import NetworkManager
import time


if __name__ == '__main__':
    my_addr = ("127.0.0.1", 4119)   # 绑定一个端口来操作
    nmsl = NetworkManager()         #
    # Never Mind the Scandal and Liber

    # json格式的数据
    # 数据的格式大概是 (l端口, r端口, (事件类型, 字典))
    # 字典中包括 idx：物体的id，type：类型，pos：位置，ang：角度，lv：线速度，av：角速度
    # 有 owner属性的一般是可以操作的物体（玩家）

    nmsl.connectPort(my_addr)
    my_idx = None   # 自己控制的玩家的id
    timer = 0       # 计时器
    direction = 1
    while True:
        try:
            timer += 1
            while my_idx is None:               # 寻找需要操作的角色
                for data in nmsl.dataRead():
                    d = data[2][1]
                    if 'owner' in d:                        # owner属性
                        if tuple(d['owner']) == my_addr:    # 自己可以操作的
                            my_idx = d['idx']               # 设置当前操作的角色

            for data in nmsl.dataRead(flush=True):
                typ = data[2][0]
                if typ == 'destroy':                        # 有物体销毁时
                    if data[2][1]['idx'] == my_idx:         # 如果是自己
                        my_idx = None                       # 不再操作它
                        break
                d = data[2][1]
                if 'owner' in d:
                    if tuple(d['owner']) != my_addr:            # 对不可操作的角色
                        enemy_pos_x, enemy_pos_y = d['pos']     # 记录位置
                        enemy_angle = d['ang']
                    if d['idx'] == my_idx:                      # 对当前操作的角色
                        my_pos_x, my_pos_y = d['pos']           # 记录位置
                        my_angle = d['ang']

            opr = dict()
            opr['idx'] = my_idx                                 # 操作当前的角色
            opr['accX'] = (enemy_pos_x - my_pos_x) * direction  # 直接向对方加速
            opr['accY'] = (enemy_pos_y - my_pos_y) * direction  #
            opr['accR'] = 1                                     # 并且逆时针旋转
            opr['fire'] = 1                                     # 并且随意射击
            direction = (timer % 100 > 20)*2-1                  # 定时后退并撞击

            print(my_pos_x, my_pos_y)

            nmsl.dataWrite(("update", opr))   # 写入操作
            nmsl.update()                     # 并发送给server

        except Exception as err:
            print(err)
        time.sleep(0.016)
