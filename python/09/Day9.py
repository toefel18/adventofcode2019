class Memory:
    def __init__(self, mem):
        self.mem = mem
        self.relative_base = 0

    def __getitem__(self, item):
        return self.mem.get(item, 0)

    def __setitem__(self, key, value):
        self.mem[key] = value


class Instruction:
    def __init__(self, opcode):
        self.opcode = opcode
        self.raw = f"{opcode:05d}"
        self.code = int(self.raw[3:])
        self.param_modes = [int(self.raw[2]), int(self.raw[1]), int(self.raw[0])]

    def get_param(self, param, ipx, memory: Memory):
        if self.param_modes[param - 1] == 0:
            return memory[memory[ipx + param]]  # dereference at address
        elif self.param_modes[param - 1] == 1:
            return memory[ipx + param]  # interpret as value
        elif self.param_modes[param - 1] == 2:
            return memory[memory.relative_base + memory[ipx + param]]  # relative mode
        else:
            raise ValueError

    def get_write_address(self, param, ipx, memory: Memory):
        if self.param_modes[param - 1] == 0:
            return memory[ipx + param]
        elif self.param_modes[param - 1] == 2:
            return memory.relative_base + memory[ipx + param]
        else:
            raise ValueError



def run(inputs, outputs, memory: Memory):
    ipx = 0
    while True:
        instruction = Instruction(memory[ipx])
        if instruction.code == 1:
            param1 = instruction.get_param(1, ipx, memory)
            param2 = instruction.get_param(2, ipx, memory)
            memory[instruction.get_write_address(3, ipx, memory)] = param1 + param2
            ipx += 4
        elif instruction.code == 2:
            param1 = instruction.get_param(1, ipx, memory)
            param2 = instruction.get_param(2, ipx, memory)
            memory[instruction.get_write_address(3, ipx, memory)] = param1 * param2
            ipx += 4
        elif instruction.code == 3:
            memory[instruction.get_write_address(1, ipx, memory)] = int(inputs.pop(0))
            ipx += 2
        elif instruction.code == 4:
            outputs.append(f"{instruction.get_param(1, ipx, memory)}")
            ipx += 2
        elif instruction.code == 5:
            param1 = instruction.get_param(1, ipx, memory)
            param2 = instruction.get_param(2, ipx, memory)
            if param1 != 0:
                ipx = param2
            else:
                ipx += 3
        elif instruction.code == 6:
            param1 = instruction.get_param(1, ipx, memory)
            param2 = instruction.get_param(2, ipx, memory)
            if param1 == 0:
                ipx = param2
            else:
                ipx += 3
        elif instruction.code == 7:
            param1 = instruction.get_param(1, ipx, memory)
            param2 = instruction.get_param(2, ipx, memory)
            if param1 < param2:
                memory[instruction.get_write_address(3, ipx, memory)] = 1
            else:
                memory[instruction.get_write_address(3, ipx, memory)] = 0
            ipx += 4
        elif instruction.code == 8:
            param1 = instruction.get_param(1, ipx, memory)
            param2 = instruction.get_param(2, ipx, memory)
            if param1 == param2:
                memory[instruction.get_write_address(3, ipx, memory)] = 1
            else:
                memory[instruction.get_write_address(3, ipx, memory)] = 0
            ipx += 4
        elif instruction.code == 9:
            param1 = instruction.get_param(1, ipx, memory)
            memory.relative_base = memory.relative_base + param1
            ipx += 2
        elif instruction.code == 99:
            break
        else:
            print(f"op_counter index {ipx} has value {memory[ipx]} in program {memory}")
            raise ValueError(ipx)


boost_software = [1102, 34463338, 34463338, 63, 1007, 63, 34463338, 63, 1005, 63, 53, 1102, 1, 3, 1000, 109, 988, 209,
                  12, 9, 1000, 209, 6, 209, 3, 203, 0, 1008, 1000, 1, 63, 1005, 63, 65, 1008, 1000, 2, 63, 1005, 63,
                  904, 1008, 1000, 0, 63, 1005, 63, 58, 4, 25, 104, 0, 99, 4, 0, 104, 0, 99, 4, 17, 104, 0, 99, 0, 0,
                  1102, 521, 1, 1028, 1101, 0, 33, 1011, 1101, 0, 22, 1006, 1101, 28, 0, 1018, 1102, 37, 1, 1008, 1102,
                  1, 20, 1019, 1101, 0, 405, 1026, 1101, 25, 0, 1015, 1101, 330, 0, 1023, 1101, 0, 29, 1016, 1101, 0,
                  560, 1025, 1101, 24, 0, 1017, 1102, 516, 1, 1029, 1102, 333, 1, 1022, 1102, 1, 34, 1012, 1101, 0, 402,
                  1027, 1101, 0, 1, 1021, 1102, 36, 1, 1013, 1102, 30, 1, 1002, 1101, 21, 0, 1000, 1102, 1, 23, 1005,
                  1102, 39, 1, 1003, 1102, 1, 32, 1007, 1102, 26, 1, 1004, 1101, 565, 0, 1024, 1101, 0, 0, 1020, 1101,
                  0, 31, 1014, 1101, 27, 0, 1001, 1101, 0, 38, 1009, 1101, 0, 35, 1010, 109, -3, 2102, 1, 10, 63, 1008,
                  63, 32, 63, 1005, 63, 203, 4, 187, 1106, 0, 207, 1001, 64, 1, 64, 1002, 64, 2, 64, 109, 26, 21108, 40,
                  40, -4, 1005, 1019, 229, 4, 213, 1001, 64, 1, 64, 1105, 1, 229, 1002, 64, 2, 64, 109, -20, 2102, 1,
                  -3, 63, 1008, 63, 22, 63, 1005, 63, 253, 1001, 64, 1, 64, 1105, 1, 255, 4, 235, 1002, 64, 2, 64, 109,
                  -10, 1208, 10, 39, 63, 1005, 63, 277, 4, 261, 1001, 64, 1, 64, 1106, 0, 277, 1002, 64, 2, 64, 109, 15,
                  2107, 20, -8, 63, 1005, 63, 299, 4, 283, 1001, 64, 1, 64, 1106, 0, 299, 1002, 64, 2, 64, 109, -8,
                  1208, 3, 40, 63, 1005, 63, 315, 1106, 0, 321, 4, 305, 1001, 64, 1, 64, 1002, 64, 2, 64, 109, 29, 2105,
                  1, -6, 1106, 0, 339, 4, 327, 1001, 64, 1, 64, 1002, 64, 2, 64, 109, -18, 1205, 10, 353, 4, 345, 1106,
                  0, 357, 1001, 64, 1, 64, 1002, 64, 2, 64, 109, 11, 1206, -1, 373, 1001, 64, 1, 64, 1105, 1, 375, 4,
                  363, 1002, 64, 2, 64, 109, -2, 1205, 0, 391, 1001, 64, 1, 64, 1106, 0, 393, 4, 381, 1002, 64, 2, 64,
                  109, 10, 2106, 0, -3, 1106, 0, 411, 4, 399, 1001, 64, 1, 64, 1002, 64, 2, 64, 109, -18, 21108, 41, 39,
                  3, 1005, 1015, 427, 1105, 1, 433, 4, 417, 1001, 64, 1, 64, 1002, 64, 2, 64, 109, -7, 21101, 42, 0, 6,
                  1008, 1011, 45, 63, 1005, 63, 457, 1001, 64, 1, 64, 1106, 0, 459, 4, 439, 1002, 64, 2, 64, 109, -14,
                  2101, 0, 9, 63, 1008, 63, 21, 63, 1005, 63, 481, 4, 465, 1105, 1, 485, 1001, 64, 1, 64, 1002, 64, 2,
                  64, 109, 22, 1207, -7, 21, 63, 1005, 63, 505, 1001, 64, 1, 64, 1106, 0, 507, 4, 491, 1002, 64, 2, 64,
                  109, 15, 2106, 0, 0, 4, 513, 1106, 0, 525, 1001, 64, 1, 64, 1002, 64, 2, 64, 109, -14, 21101, 43, 0,
                  -1, 1008, 1013, 43, 63, 1005, 63, 551, 4, 531, 1001, 64, 1, 64, 1106, 0, 551, 1002, 64, 2, 64, 109,
                  10, 2105, 1, 0, 4, 557, 1106, 0, 569, 1001, 64, 1, 64, 1002, 64, 2, 64, 109, -12, 21102, 44, 1, 3,
                  1008, 1015, 44, 63, 1005, 63, 595, 4, 575, 1001, 64, 1, 64, 1105, 1, 595, 1002, 64, 2, 64, 109, -4,
                  1201, -8, 0, 63, 1008, 63, 21, 63, 1005, 63, 621, 4, 601, 1001, 64, 1, 64, 1106, 0, 621, 1002, 64, 2,
                  64, 109, 5, 2108, 37, -5, 63, 1005, 63, 639, 4, 627, 1105, 1, 643, 1001, 64, 1, 64, 1002, 64, 2, 64,
                  109, -14, 1202, 1, 1, 63, 1008, 63, 21, 63, 1005, 63, 669, 4, 649, 1001, 64, 1, 64, 1105, 1, 669,
                  1002, 64, 2, 64, 109, -2, 1207, 7, 27, 63, 1005, 63, 691, 4, 675, 1001, 64, 1, 64, 1106, 0, 691, 1002,
                  64, 2, 64, 109, 13, 2107, 33, -3, 63, 1005, 63, 711, 1001, 64, 1, 64, 1105, 1, 713, 4, 697, 1002, 64,
                  2, 64, 109, 19, 1206, -9, 727, 4, 719, 1105, 1, 731, 1001, 64, 1, 64, 1002, 64, 2, 64, 109, -24, 1202,
                  0, 1, 63, 1008, 63, 20, 63, 1005, 63, 755, 1001, 64, 1, 64, 1106, 0, 757, 4, 737, 1002, 64, 2, 64,
                  109, 8, 21102, 45, 1, -3, 1008, 1010, 46, 63, 1005, 63, 781, 1001, 64, 1, 64, 1106, 0, 783, 4, 763,
                  1002, 64, 2, 64, 109, -15, 2108, 40, 10, 63, 1005, 63, 799, 1105, 1, 805, 4, 789, 1001, 64, 1, 64,
                  1002, 64, 2, 64, 109, 20, 21107, 46, 45, -1, 1005, 1017, 821, 1106, 0, 827, 4, 811, 1001, 64, 1, 64,
                  1002, 64, 2, 64, 109, -23, 1201, 6, 0, 63, 1008, 63, 29, 63, 1005, 63, 847, 1106, 0, 853, 4, 833,
                  1001, 64, 1, 64, 1002, 64, 2, 64, 109, 17, 21107, 47, 48, 2, 1005, 1014, 875, 4, 859, 1001, 64, 1, 64,
                  1106, 0, 875, 1002, 64, 2, 64, 109, -10, 2101, 0, -2, 63, 1008, 63, 20, 63, 1005, 63, 895, 1105, 1,
                  901, 4, 881, 1001, 64, 1, 64, 4, 64, 99, 21102, 27, 1, 1, 21101, 0, 915, 0, 1105, 1, 922, 21201, 1,
                  37574, 1, 204, 1, 99, 109, 3, 1207, -2, 3, 63, 1005, 63, 964, 21201, -2, -1, 1, 21102, 942, 1, 0,
                  1105, 1, 922, 22102, 1, 1, -1, 21201, -2, -3, 1, 21101, 957, 0, 0, 1105, 1, 922, 22201, 1, -1, -2,
                  1105, 1, 968, 21201, -2, 0, -2, 109, -3, 2105, 1, 0
                  ]

# boost_software = [109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99]
# boost_software = [1102,34915192,34915192,7,4,7,99,0]
# boost_software = [104,1125899906842624,99]

program_as_dict = {i: boost_software[i] for i in range(len(boost_software))}
memory = Memory(program_as_dict)
inputs = [1]
output = []
run(inputs, output, memory)
print(f"part 1 = {output}")
