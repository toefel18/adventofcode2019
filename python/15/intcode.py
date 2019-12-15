class Memory:
    def __init__(self, mem):
        if isinstance(mem, list):
            self.mem = {i: mem for i in range(len(mem))}
        elif isinstance(mem, dict):
            self.mem = mem.copy()
        else:
            raise ValueError(f"memory should be a list or map but was {type(mem)}")
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


def run(inputs, memory: Memory):
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
            yield instruction.get_param(1, ipx, memory)
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
            raise StopIteration
        else:
            print(f"op_counter index {ipx} has value {memory[ipx]} in program {memory}")
            raise ValueError(ipx)
