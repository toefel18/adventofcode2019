def required_fuel(mass):
    return int(mass / 3) - 2


def required_fuel_for_fuel(fuel):
    x = required_fuel(fuel)
    if x <= 0:
        return 0
    return x + required_fuel_for_fuel(x)


masses = [int(line) for line in open('Day1-input.txt')]
fuel_required_for_module_mass = [required_fuel(mass) for mass in masses]
print(f"part 1: {sum(fuel_required_for_module_mass)}")

total_required_fuel_per_module = [required_fuel_for_fuel(fuel) + fuel for fuel in fuel_required_for_module_mass]
print(f"part 2: {sum(total_required_fuel_per_module)}")
