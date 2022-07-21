# from pyhcl import *
# from example import half_adder
# from example import simlite
# from example import simlite_2
# from example import Simlite_task
# from injector import simlite_v3

# from injector import simlite_v2
# from injector import simlite_v4
# from injector import simlite_verilog_v1

# from myTests import test_simlite
# from myTests import test_simlite_pysv
# from myTests import test_simlite_fork

from myTests import test_verilog
# from myTests import test_verilog_pysv
# from myTests import test_verilog_fork

# from myTests import test_firrtl
# from myTests import test_firrtl_2

# from myTests import test_tinyalu


def main():
    # f = Emitter.dump(Emitter.emit(MOD()), "mod.v")
    # Emitter.dumpVerilog(f)
    # half_adder.main()

    # simlite_v2.main()
    # simlite_v4.main()
    # simlite_verilog_v1.main()

    # simlite_2.main()
    # Simlite_task.test()

    # test_simlite.main()
    # test_simlite_pysv.main()
    # test_simlite_fork.main()

    test_verilog.main()
    # test_verilog_pysv.main()
    # test_verilog_fork.main()

    # test_firrtl.main()
    # test_firrtl_2.main()

    # test_tinyalu.main()
    pass


if __name__ == '__main__':
    main()


