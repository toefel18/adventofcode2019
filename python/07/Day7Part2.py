# Main difference with part 1 is that run() now is a generator function

class Instruction:
    def __init__(self, opcode):
        self.opcode = opcode
        self.raw = f"{opcode:05d}"
        self.code = int(self.raw[3:])
        self.param_modes = [int(self.raw[2]), int(self.raw[1]), int(self.raw[0])]

    def get_param(self, param, ipx, program):
        if self.param_modes[param - 1] == 0:
            return program[program[ipx + param]]  # dereference at address
        elif self.param_modes[param - 1] == 1:
            return program[ipx + param]  # interpret as value
        else:
            raise ValueError


# implemented as a generator function
def run(inputs, program):
    ipx = 0
    while True:
        instruction = Instruction(program[ipx])
        if instruction.code == 1:
            param1 = instruction.get_param(1, ipx, program)
            param2 = instruction.get_param(2, ipx, program)
            program[program[ipx + 3]] = param1 + param2
            ipx += 4
        elif instruction.code == 2:
            param1 = instruction.get_param(1, ipx, program)
            param2 = instruction.get_param(2, ipx, program)
            program[program[ipx + 3]] = param1 * param2
            ipx += 4
        elif instruction.code == 3:
            program[program[ipx + 1]] = int(inputs.pop(0))
            ipx += 2
        elif instruction.code == 4:
            yield f"{instruction.get_param(1, ipx, program)}"
            ipx += 2
        elif instruction.code == 5:
            param1 = instruction.get_param(1, ipx, program)
            param2 = instruction.get_param(2, ipx, program)
            if param1 != 0:
                ipx = param2
            else:
                ipx += 3
        elif instruction.code == 6:
            param1 = instruction.get_param(1, ipx, program)
            param2 = instruction.get_param(2, ipx, program)
            if param1 == 0:
                ipx = param2
            else:
                ipx += 3
        elif instruction.code == 7:
            param1 = instruction.get_param(1, ipx, program)
            param2 = instruction.get_param(2, ipx, program)
            if param1 < param2:
                program[program[ipx + 3]] = 1
            else:
                program[program[ipx + 3]] = 0
            ipx += 4
        elif instruction.code == 8:
            param1 = instruction.get_param(1, ipx, program)
            param2 = instruction.get_param(2, ipx, program)
            if param1 == param2:
                program[program[ipx + 3]] = 1
            else:
                program[program[ipx + 3]] = 0
            ipx += 4
        elif instruction.code == 99:
            raise StopIteration
        else:
            print(f"op_counter index {ipx} has value {program[ipx]} in program {program}")
            raise ValueError(ipx)

#
amplifier_software = [3, 8, 1001, 8, 10, 8, 105, 1, 0, 0, 21, 30, 51, 72, 81, 94, 175, 256, 337, 418, 99999, 3, 9, 101,
                      5, 9, 9, 4, 9, 99, 3, 9, 1001, 9, 3, 9, 1002, 9, 2, 9, 1001, 9, 2, 9, 1002, 9, 5, 9, 4, 9, 99, 3,
                      9, 1002, 9, 4, 9, 101, 4, 9, 9, 102, 5, 9, 9, 101, 3, 9, 9, 4, 9, 99, 3, 9, 1002, 9, 4, 9, 4, 9,
                      99, 3, 9, 102, 3, 9, 9, 1001, 9, 4, 9, 4, 9, 99, 3, 9, 1001, 9, 2, 9, 4, 9, 3, 9, 101, 2, 9, 9, 4,
                      9, 3, 9, 101, 2, 9, 9, 4, 9, 3, 9, 1001, 9, 1, 9, 4, 9, 3, 9, 101, 1, 9, 9, 4, 9, 3, 9, 101, 1, 9,
                      9, 4, 9, 3, 9, 101, 1, 9, 9, 4, 9, 3, 9, 1002, 9, 2, 9, 4, 9, 3, 9, 101, 1, 9, 9, 4, 9, 3, 9,
                      1002, 9, 2, 9, 4, 9, 99, 3, 9, 102, 2, 9, 9, 4, 9, 3, 9, 1002, 9, 2, 9, 4, 9, 3, 9, 1001, 9, 1, 9,
                      4, 9, 3, 9, 102, 2, 9, 9, 4, 9, 3, 9, 1001, 9, 2, 9, 4, 9, 3, 9, 1002, 9, 2, 9, 4, 9, 3, 9, 101,
                      1, 9, 9, 4, 9, 3, 9, 101, 1, 9, 9, 4, 9, 3, 9, 101, 2, 9, 9, 4, 9, 3, 9, 102, 2, 9, 9, 4, 9, 99,
                      3, 9, 102, 2, 9, 9, 4, 9, 3, 9, 102, 2, 9, 9, 4, 9, 3, 9, 1002, 9, 2, 9, 4, 9, 3, 9, 1001, 9, 1,
                      9, 4, 9, 3, 9, 1002, 9, 2, 9, 4, 9, 3, 9, 102, 2, 9, 9, 4, 9, 3, 9, 102, 2, 9, 9, 4, 9, 3, 9, 102,
                      2, 9, 9, 4, 9, 3, 9, 102, 2, 9, 9, 4, 9, 3, 9, 102, 2, 9, 9, 4, 9, 99, 3, 9, 1001, 9, 2, 9, 4, 9,
                      3, 9, 101, 1, 9, 9, 4, 9, 3, 9, 1001, 9, 1, 9, 4, 9, 3, 9, 1001, 9, 1, 9, 4, 9, 3, 9, 102, 2, 9,
                      9, 4, 9, 3, 9, 101, 1, 9, 9, 4, 9, 3, 9, 1001, 9, 2, 9, 4, 9, 3, 9, 1002, 9, 2, 9, 4, 9, 3, 9,
                      1001, 9, 1, 9, 4, 9, 3, 9, 101, 2, 9, 9, 4, 9, 99, 3, 9, 101, 2, 9, 9, 4, 9, 3, 9, 101, 2, 9, 9,
                      4, 9, 3, 9, 101, 1, 9, 9, 4, 9, 3, 9, 1001, 9, 1, 9, 4, 9, 3, 9, 1002, 9, 2, 9, 4, 9, 3, 9, 1001,
                      9, 1, 9, 4, 9, 3, 9, 1001, 9, 1, 9, 4, 9, 3, 9, 1001, 9, 2, 9, 4, 9, 3, 9, 1001, 9, 1, 9, 4, 9, 3,
                      9, 101, 1, 9, 9, 4, 9, 99
                      ]


def valid_setting_part_2(setting_num):
    options = set(str("{:05d}".format(setting_num)))
    return len(options) == 5 and len(options.intersection(["0", "1", "2", "3", "4"])) == 0


possible_phase_settings = [list("{:05d}".format(n)) for n in range(99999) if valid_setting_part_2(n)]
highest_output = 0


for phase_setting in possible_phase_settings:
    inputs = [[phase_setting[0]], [phase_setting[1]], [phase_setting[2]], [phase_setting[3]], [phase_setting[4]]]
    amplifiers = [
        run(inputs[0], amplifier_software.copy()),
        run(inputs[1], amplifier_software.copy()),
        run(inputs[2], amplifier_software.copy()),
        run(inputs[3], amplifier_software.copy()),
        run(inputs[4], amplifier_software.copy()),
    ]

    # feed first generator 0
    input_signal = 0

    while True:
        try:
            for amp in range(5):
                inputs[amp].append(input_signal)
                input_signal = next(amplifiers[amp])
        except StopIteration:
            break

    print(f"{phase_setting} output = {input_signal}")
    highest_output = max(int(input_signal), highest_output)

print(f"part 2 = {highest_output}")
