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
            print(f"requesting input value {inputs[0]}")
            memory[instruction.get_write_address(1, ipx, memory)] = int(inputs.pop(0))
            ipx += 2
        elif instruction.code == 4:
            print("yielding")
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


paint_software = [3, 8, 1005, 8, 301, 1106, 0, 11, 0, 0, 0, 104, 1, 104, 0, 3, 8, 102, -1, 8, 10, 1001, 10, 1, 10, 4,
                  10, 1008, 8, 0, 10, 4, 10, 1002, 8, 1, 29, 1, 1103, 7, 10, 3, 8, 102, -1, 8, 10, 101, 1, 10, 10, 4,
                  10, 108, 1, 8, 10, 4, 10, 1002, 8, 1, 54, 2, 103, 3, 10, 2, 1008, 6, 10, 1006, 0, 38, 2, 1108, 7, 10,
                  3, 8, 102, -1, 8, 10, 1001, 10, 1, 10, 4, 10, 108, 1, 8, 10, 4, 10, 1001, 8, 0, 91, 3, 8, 1002, 8, -1,
                  10, 1001, 10, 1, 10, 4, 10, 1008, 8, 0, 10, 4, 10, 101, 0, 8, 114, 3, 8, 1002, 8, -1, 10, 101, 1, 10,
                  10, 4, 10, 1008, 8, 1, 10, 4, 10, 1001, 8, 0, 136, 3, 8, 1002, 8, -1, 10, 1001, 10, 1, 10, 4, 10,
                  1008, 8, 1, 10, 4, 10, 1002, 8, 1, 158, 1, 1009, 0, 10, 2, 1002, 18, 10, 3, 8, 102, -1, 8, 10, 101, 1,
                  10, 10, 4, 10, 108, 0, 8, 10, 4, 10, 1002, 8, 1, 187, 2, 1108, 6, 10, 3, 8, 1002, 8, -1, 10, 1001, 10,
                  1, 10, 4, 10, 108, 0, 8, 10, 4, 10, 1002, 8, 1, 213, 3, 8, 1002, 8, -1, 10, 101, 1, 10, 10, 4, 10,
                  1008, 8, 1, 10, 4, 10, 1001, 8, 0, 236, 1, 104, 10, 10, 1, 1002, 20, 10, 2, 1008, 9, 10, 3, 8, 102,
                  -1, 8, 10, 101, 1, 10, 10, 4, 10, 108, 0, 8, 10, 4, 10, 101, 0, 8, 269, 1, 102, 15, 10, 1006, 0, 55,
                  2, 1107, 15, 10, 101, 1, 9, 9, 1007, 9, 979, 10, 1005, 10, 15, 99, 109, 623, 104, 0, 104, 1, 21102, 1,
                  932700598932, 1, 21102, 318, 1, 0, 1105, 1, 422, 21102, 1, 937150489384, 1, 21102, 329, 1, 0, 1105, 1,
                  422, 3, 10, 104, 0, 104, 1, 3, 10, 104, 0, 104, 0, 3, 10, 104, 0, 104, 1, 3, 10, 104, 0, 104, 1, 3,
                  10, 104, 0, 104, 0, 3, 10, 104, 0, 104, 1, 21101, 46325083227, 0, 1, 21102, 376, 1, 0, 1106, 0, 422,
                  21102, 3263269927, 1, 1, 21101, 387, 0, 0, 1105, 1, 422, 3, 10, 104, 0, 104, 0, 3, 10, 104, 0, 104, 0,
                  21102, 988225102184, 1, 1, 21101, 410, 0, 0, 1105, 1, 422, 21101, 868410356500, 0, 1, 21102, 1, 421,
                  0, 1106, 0, 422, 99, 109, 2, 21202, -1, 1, 1, 21102, 1, 40, 2, 21102, 1, 453, 3, 21102, 1, 443, 0,
                  1105, 1, 486, 109, -2, 2106, 0, 0, 0, 1, 0, 0, 1, 109, 2, 3, 10, 204, -1, 1001, 448, 449, 464, 4, 0,
                  1001, 448, 1, 448, 108, 4, 448, 10, 1006, 10, 480, 1102, 1, 0, 448, 109, -2, 2106, 0, 0, 0, 109, 4,
                  1201, -1, 0, 485, 1207, -3, 0, 10, 1006, 10, 503, 21101, 0, 0, -3, 22101, 0, -3, 1, 21201, -2, 0, 2,
                  21102, 1, 1, 3, 21101, 0, 522, 0, 1105, 1, 527, 109, -4, 2106, 0, 0, 109, 5, 1207, -3, 1, 10, 1006,
                  10, 550, 2207, -4, -2, 10, 1006, 10, 550, 22102, 1, -4, -4, 1105, 1, 618, 21201, -4, 0, 1, 21201, -3,
                  -1, 2, 21202, -2, 2, 3, 21102, 569, 1, 0, 1106, 0, 527, 22101, 0, 1, -4, 21101, 0, 1, -1, 2207, -4,
                  -2, 10, 1006, 10, 588, 21102, 1, 0, -1, 22202, -2, -1, -2, 2107, 0, -3, 10, 1006, 10, 610, 21201, -1,
                  0, 1, 21101, 610, 0, 0, 105, 1, 485, 21202, -2, -1, -2, 22201, -4, -2, -4, 109, -5, 2105, 1, 0]

def move(turnInstruction):
    global orientation, x, y
    if turnInstruction == 0 and orientation == "UP":
        orientation = "LEFT"
        x -= 1
    elif turnInstruction == 0 and orientation == "LEFT":
        orientation = "DOWN"
        y += 1
    elif turnInstruction == 0 and orientation == "DOWN":
        orientation = "RIGHT"
        x += 1
    elif turnInstruction == 0 and orientation == "RIGHT":
        orientation = "UP"
        y -= 1
    elif turnInstruction == 1 and orientation == "UP":
        orientation = "RIGHT"
        x += 1
    elif turnInstruction == 1 and orientation == "LEFT":
        orientation = "UP"
        y -= 1
    elif turnInstruction == 1 and orientation == "DOWN":
        orientation = "LEFT"
        x -= 1
    elif turnInstruction == 1 and orientation == "RIGHT":
        orientation = "DOWN"
        y += 1



# part 1
try:
    program_as_dict = {i: paint_software[i] for i in range(len(paint_software))}
    memory = Memory(program_as_dict)
    inputs = [0]
    output = []
    paint_robot = run(inputs, memory)

    surface = {}
    x = 0
    y = 0
    orientation = "UP"

    while True:
        color = next(paint_robot)
        turnInstruction = next(paint_robot)
        surface[(x, y)] = color
        move(turnInstruction)
        inputs.append(surface.get((x, y), 0))
except StopIteration:
    pass

print(f"part1 =  {len(surface)}")






# part 2
try:
    program_as_dict = {i: paint_software[i] for i in range(len(paint_software))}
    memory = Memory(program_as_dict)
    inputs = [1]
    output = []
    paint_robot = run(inputs, memory)

    surface = {}
    x = 0
    y = 0
    orientation = "UP"

    while True:
        color = next(paint_robot)
        turnInstruction = next(paint_robot)
        surface[(x, y)] = color
        move(turnInstruction)
        inputs.append(surface.get((x, y), 0))
except StopIteration:
    pass

maxX = max([coordinate[0] for coordinate in surface.keys()])
maxY = max([coordinate[1] for coordinate in surface.keys()])

print(f"part2 = ")

for line in range(maxY + 1):
    for col in range(maxX + 1):
        color = surface.get((col, line), 0)
        if color == 1:
            print("#", end="")
        else:
            print(" ", end="")

    print()
