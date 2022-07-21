from typing import Type, Union, Dict


class IO:
    _ios: Dict[str, int]

    def __init__(self, **kwargs):
        self._ios = kwargs


class Add:
    io = IO(
        in1=3,
        in2=4,
        out=5
    )


import re


# 解析FIRRTL代码, 返回输入端口名列表 和 输出端口名列表
def firrtl_parse(firrtl_path):
    circuit_begin_match = r"circuit\s*([a-zA-Z0-9_]+)"
    module_begin_match = r"module\s*([a-zA-Z0-9_]+)"
    input_port_match = r"input\s*([a-zA-Z0-9_]+)"
    output_port_match = r"output\s*([a-zA-Z0-9_]+)"
    input_ports_name = []
    output_ports_name = []
    top_module_name = '0'
    current_module_name = '1'
    with open(firrtl_path, "r") as firrtl_file:
        while firrtl_file:
            firrtl_line = firrtl_file.readline().strip(' ')  # 读取一行
            # print(firrtl_line)
            if firrtl_line == "":           # 注：如果是空行，为'\n'
                break

            circuit_begin = re.search(circuit_begin_match, firrtl_line)
            module_begin = re.search(module_begin_match, firrtl_line)

            if circuit_begin:
                top_module_name = circuit_begin.group(1)
                # print(top_module_name)

            if module_begin:
                current_module_name = module_begin.group(1)
                # print(current_module_name)

            if current_module_name == top_module_name:
                input_port = re.search(input_port_match, firrtl_line)
                output_port = re.search(output_port_match, firrtl_line)
                if input_port:
                    input_ports_name.append(input_port.group(1))
                if output_port:
                    output_ports_name.append(output_port.group(1))
    print(top_module_name)
    print(input_ports_name)
    print(output_ports_name)
    return top_module_name, input_ports_name, output_ports_name


# 解析verilog代码, 返回输入端口名列表 和 输出端口名列表
def verilog_parse(dut_path, top_module_name):
    dut_name = top_module_name.split('.')[0]         # 模块名
    top_module_path = dut_path + top_module_name
    # print(top_module_path)
    module_begin_match = r"module\s*([a-zA-Z0-9_]+)"

    input_port_match = r"input\s*(reg|wire)*\s*(\[[0-9]+\:[0-9]+\]*)*\s*([a-zA-Z0-9_]+)"
    output_port_match = r"output\s*(reg|wire)*\s*(\[[0-9]+\:[0-9]+\]*)*\s*([a-zA-Z0-9_]+)"

    input_ports_name = []
    output_ports_name = []
    with open(top_module_path, "r") as verilog_file:
        while verilog_file:
            verilog_line = verilog_file.readline().strip(' ')  # 读取一行
            # print(verilog_line)
            if verilog_line == "":  # 注：如果是空行，为'\n'
                break

            module_begin = re.search(module_begin_match, verilog_line)

            if module_begin:
                current_module_name = module_begin.group(1)
                # print(current_module_name)

            if current_module_name == dut_name:
                input_port = re.search(input_port_match, verilog_line)
                output_port = re.search(output_port_match, verilog_line)
                if input_port:
                    input_ports_name.append(input_port.group(3))
                if output_port:
                    output_ports_name.append(output_port.group(3))
    print(dut_name)
    print(input_ports_name)
    print(output_ports_name)
    return input_ports_name, output_ports_name


def handle_inputs(inputs):
    res = ""
    i = 0
    # 对输入端口进行赋值
    for n in inputs:
        str = f"""
    if(inputs_s[{i}]!="z"){{
        s2l(inputs_s[{i}], inputs[{i}]);
        top->io_{n} = inputs[{i}];          
    }}\n
        """
        res += str

        i += 1
    return res


def generateInput():

    str_0 = '''#include "Vtinyalu.h"
#include "verilated.h"
#include "verilated_vcd_c.h"
#include <vector>
#include <iostream>
#include <cstdio>
#include <string>
#include <sstream>
#include <ctime>
using namespace std;


void s2l(string &s, unsigned long long &l){
    stringstream ss;
    ss<<s;
    ss>>l;    
}

int main(int argc, char** argv, char** env) {
    Verilated::commandArgs(argc, argv);
    
    Vtinyalu* top = new Vtinyalu;

    Verilated::internalsDump();  // See scopes to help debug
    Verilated::traceEverOn(true);

    VerilatedVcdC* tfp = new VerilatedVcdC;
    top->trace(tfp, 99);
    tfp->open("wave.vcd");

    //long t1 = GetTickCount();
    time_t beginTime = time(NULL);



    top->clk = 0;          
    top->A = 0;          
    top->B = 0;          
    top->op = 0;          
    top->reset_n = 1;          

    top->eval();
            
    top->clk = 1;          
    top->A = 0;          
    top->B = 0;          
    top->op = 0;          
    top->reset_n = 1;          
    top->start = 0;
    
    top->eval();
'''
    str_1 = '''
    top->clk = 0;          
    top->A = 170;          
    top->B = 85;          
    top->op = 1;          
    top->reset_n = 1;          
    top->start = 1;
    
    top->eval();
    std::cout<<top->result<<endl;
        '''
    str_2 = '''
    top->clk = 1;          
    top->A = 170;          
    top->B = 85;          
    top->op = 1;          
    top->reset_n = 1;          
    top->start = 1;
    
    top->eval();
    std::cout<<top->result<<endl;
    '''
    str_3 = '''
    top->clk = 0;          
    top->A = 170;          
    top->B = 85;          
    top->op = 1;          
    top->reset_n = 1;          
    top->start = 0;

    top->eval();
    std::cout<<top->result<<endl;
        '''
    str_4 = '''
    top->clk = 1;          
    top->A = 170;          
    top->B = 85;          
    top->op = 1;          
    top->reset_n = 1;          
    top->start = 0;

    top->eval();
    std::cout<<top->result<<endl;
        '''
    str_i = str_1 + str_2 + (str_3 + str_4) * 4

    str_end = '''
    
    std::cout<<top->result<<endl;
    time_t endTime = time(NULL);
    int32_t diff = endTime - beginTime;
    std::cout<<difftime(endTime, beginTime)<<endl;
    std::cout<<diff;
    
    top->final();
    tfp->close();
    delete top;
    return 0;
}
    '''
    str = str_0 + str_i * 5000 + str_end
    ifn = f"./tmp/tinyalu_harness.cpp"
    fd = open(ifn, "w")
    fd.write(str)


if __name__ == '__main__':
    li = ['mcdt.ch0_data_i',
     'mcdt.ch0_valid_i',

     'mcdt.ch1_data_i',
     'mcdt.ch1_valid_i',

     'mcdt.ch2_data_i',
     'mcdt.ch2_valid_i',

     'mcdt.clk_i',
     'mcdt.rstn_i',

     'mcdt.mcdt_val_o',
     'mcdt.mcdt_id_o',
     'mcdt.mcdt_data_o',

     'mcdt.ch2_ready_o',
     'mcdt.ch2_margin_o',

     'mcdt.ch1_ready_o',
     'mcdt.ch1_margin_o',

     'mcdt.ch0_ready_o',
     'mcdt.ch0_margin_o']
    print(li)
    # with open('../injector/reader.py', 'r') as f:
    #     file = f.readlines()
    # for i in range(len(file)):
    #     print(file[i])
    # print('xx')
    # verilog_parse('./tmp/dut/', 'tinyalu.sv')
    # verilog_parse('../simulation/', 'M.v')
    # firrtl_parse('./tmp/firrtl/M.fir')
    # res = handle_inputs(['A', 'B', 'C'])
    # print(res)
    # pass

    # generateInput()



