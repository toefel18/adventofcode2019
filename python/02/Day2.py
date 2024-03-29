def op(ipx, op_function):
    x = program[program[ipx + 1]]
    y = program[program[ipx + 2]]
    program[program[ipx + 3]] = op_function(x, y)


def run():
    for ipx in range(0, len(program), 4):
        if program[ipx] == 1:
            op(ipx, lambda x, y: x + y)
        elif program[ipx] == 2:
            op(ipx, lambda x, y: x * y)
        elif program[ipx] == 99:
            break
        else:
            print(f"op_counter index {ipx} has value {program[ipx]} in program {program}")
            raise ValueError(ipx)


program = [1, 9, 10, 3, 2, 3, 11, 0, 99, 30, 40, 50]
run()
print(program)

program = [1, 0, 0, 0, 99]
run()
print(program)

program = [2, 3, 0, 3, 99]
run()
print(program)

program = [2, 4, 4, 5, 99, 0]
run()
print(program)

program = [1, 1, 1, 4, 99, 5, 6, 0, 99]
run()
print(program)

# part 1
input = [1, 0, 0, 3, 1, 1, 2, 3, 1, 3, 4, 3, 1, 5, 0, 3, 2, 13, 1, 19, 1, 6, 19, 23, 2, 23, 6, 27, 1, 5, 27, 31, 1,
           10, 31, 35, 2, 6, 35, 39, 1, 39, 13, 43, 1, 43, 9, 47, 2, 47, 10, 51, 1, 5, 51, 55, 1, 55, 10, 59, 2, 59, 6,
           63, 2, 6, 63, 67, 1, 5, 67, 71, 2, 9, 71, 75, 1, 75, 6, 79, 1, 6, 79, 83, 2, 83, 9, 87, 2, 87, 13, 91, 1, 10,
           91, 95, 1, 95, 13, 99, 2, 13, 99, 103, 1, 103, 10, 107, 2, 107, 10, 111, 1, 111, 9, 115, 1, 115, 2, 119, 1,
           9, 119, 0, 99, 2, 0, 14, 0]

program = list(input)
program[1] = 12
program[2] = 2
run()
print(program)

for noun in range(100):
    for verb in range(100):
        program = input.copy()
        program[1] = noun
        program[2] = verb
        run()
        if program[0] == 19690720:
            print(f"part 2: result={program[0]} verb={verb} noun={noun}  100*noun +verb = {(100*noun)+verb}")

