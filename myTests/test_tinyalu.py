import time

from pyhcl.simulator.simlite_verilog import Simlite
import random


# 每次给输入端口赋值, 跑一个时间单位
def test_step(s):
    s.start()
    with open('../injector/tmp/tinyalu_inputs', 'r') as f:
        file = f.readlines()
    begin = time.time()
    for i in range(len(file)):
        s.stepp(file[i])

    end = time.time()
    print('time:', end - begin)


def test_task(s):
    tasks = []
    tasks.append([0, 0, 20, 20])
    tasks.append([1, 0, 15, 10])
    tasks.append([0, 0, 1000, 1])
    tasks.append([1, 0, 999, 201])

    s.start_task('Top', tasks)


def randomInput(ifn):
    fd = open(ifn, "w")
    instr = ""
    for i in range(100):
        instr += "0 0 0 " + str(random.randint(1, 2000)) + ' ' + str(random.randint(1, 2000)) + "\n"
    instr = instr + "-1\n"
    fd.write(instr)
    fd.close()


def test_file(s):
    ifn = f"../injector/tmp/tinyalu_inputs"
    ofn = f"../myTests/tmp/outputs"
    begin = time.time()
    s.start(mode="task", ofn=ofn, ifn=ifn)
    end = time.time()
    print('time: ', end-begin)
    pass


def main():
    # Emitter.dumpVerilog(Emitter.dump(Emitter.emit(Top()), "Add.fir"))
    top_module_name = 'tinyalu.sv'
    dut_path = 'myTests/tmp/dut/'
    s = Simlite(top_module_name, dut_path)

    # with open('myTests/tmp/tinyalu_harness.cpp', 'r') as f:
    #     code = ''.join(f.readlines())
    #
    # s = Simlite(top_module_name, dut_path, debug=True, harness_code=code)

    test_step(s)
    # test_task(s)
    # test_file(s)

    s.close()


if __name__ == '__main__':
    main()

