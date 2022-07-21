from pyhcl import *
from pyhcl.simulator.simlite import Simlite
import random


class Top(Module):
    io = IO(
        a=Input(U.w(32)),
        b=Input(U.w(32)),
        c=Output(U.w(32))
    )

    io.c <<= io.a + io.b


# 每次给输入端口赋值, 跑一个时间单位
def test_step(s):
    # 开启仿真
    s.start()
    # 每次跑一个时间单位，传入每个input端口的值
    s.step([20, 20])
    # s.cnt得到step次数，s.getRes()得到输出端口的值
    print("cnt: %d\t\tresult:%s" % (s.cnt, s.getRes()))
    s.step([15, 10])
    print("cnt: %d\t\tresult:%s" % (s.cnt, s.getRes()))
    s.step([1000, 1])
    print("cnt: %d\t\tresult:%s" % (s.cnt, s.getRes()))
    s.step([999, 201])
    print("cnt: %d\t\tresult:%s" % (s.cnt, s.getRes()))
    # 结束仿真（只有单步仿真时需要）
    s.stop()


def test_task(s):
    # 将输入端口值列表存放成task二维列表
    tasks = []
    tasks.append([20, 20])
    tasks.append([15, 10])
    tasks.append([1000, 1])
    tasks.append([999, 201])
    # 仿真
    s.start_task('Top', tasks)


def randomInput(ifn):
    fd = open(ifn, "w")
    instr = ""
    # instr += "0 " + 'x' + ' ' + str(random.randint(1, 2000)) + "\n"
    for i in range(100):
        instr += "0 " + str(random.randint(1, 2000)) + ' ' + str(random.randint(1, 2000)) + "\n"
    instr = instr + "-1\n"
    fd.write(instr)
    fd.close()


def test_file(s):
    # 输入和输出端口文件路径
    ifn = f"../myTests/tmp/Top_inputs"
    ofn = f"../myTests/tmp/Top_outputs"
    # 随机化生成input文件
    randomInput(ifn)
    # 仿真
    s.start(mode="task", ofn=ofn, ifn=ifn)
    pass


def main():
    # 创建Simlite对象
    s = Simlite(Top(), debug=True)
    # 仿真测试
    # test_step(s)
    # test_task(s)
    test_file(s)
    s.close()


if __name__ == '__main__':
    main()
