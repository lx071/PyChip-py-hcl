
# 读波形
from injector.vcd_reader import VcdReader


def read_wave(wavefile, replay_block, inputs_only, excluded_sigs):
    # get file postfix check if supported   # 得到文件后缀查看是否支持
    
    wave_type = wavefile.split('.')[-1]     # 得到文件后缀（fsdb/vcd）

    supported_wave_formats = ['vcd', 'fsdb']

    if wave_type not in supported_wave_formats:     # 不属于fsdb和vcd文件，报错
        raise ValueError("Wavefile type: ", wave_type, " is currently not supported. Supported formats are: ", supported_wave_formats)

    data = None

    if wave_type == 'vcd':      # vcd文件
        # from waveRead.vcd_reader import VcdReader
        data = VcdReader(replay_block, wavefile, excluded_sigs, inputs_only)
    elif wave_type == 'fsdb':   # fsdb文件
        pass
        # from waveRead.fsdb_reader import FsdbReader
        # data = FsdbReader(replay_block, wavefile, excluded_sigs, inputs_only)

    return data     


'''
input [7:0] A,
input [7:0] B,
input [2:0] op,
input reset_n,
input start,
'''


def generateInput(data):
    ports_name = ['tinyalu.clk', 'tinyalu.A', 'tinyalu.B', 'tinyalu.op', 'tinyalu.reset_n', 'tinyalu.start']
    sim_time = 0
    ifn = f"./tmp/tinyalu_inputs"
    fd = open(ifn, "w")
    while True:
        # values为字典{'信号':'值',...}--存放仿真时刻sim_time时各信号量的值
        values = data.get_values_at(sim_time)
        values_list = []
        for port_name in ports_name:
            value = values[port_name]
            if value != 'z' and value != 'x':
                values_list.append(str(int(value, 2)))
            else:
                values_list.append('z')

        values_str = ' '.join(values_list)
        fd.write('0 ' + values_str + '\n')

        previous_time = sim_time
        # 得到仿真时刻sim_time后的一个变化时刻，若无则返回None
        sim_time = data.get_next_event(sim_time)

        if sim_time is None:
            break

        cnt = sim_time - previous_time - 1
        num = len(values)
        value_str = ('z ' * num + '\n') * cnt
        fd.write(value_str)
    fd.write('-1\n')
    fd.close()
    pass


def main():
    print("begin")
    replay_block = []
    # wavefile = "../simulation/wave.vcd"
    # wavefile = "./mcdt.vcd"
    wavefile = "./tinyalu.vcd"
    excluded_sigs = []
    inputs_only = False
    data = read_wave(wavefile, replay_block, inputs_only, excluded_sigs)  # VcdReader对象
    # print(data.sig_name_2_vcd_name)
    # print(data.vcd_name_2_sig_name)
    # print(data.signal_values)
    print("XXX")
    generateInput(data)
    print("YYY")


if __name__ == '__main__':
    main()

