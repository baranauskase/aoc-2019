def load_module_mass(file):
    with open(file) as f:
        return [int(l) for l in f]


def calc_fuel_req(mass):
    '''
    Fuel required to launch a given module is based on its mass. 
    Specifically, to find the fuel required for a module,
    take its mass, divide by three, round down, and subtract 2.

    Args:
        mass: module mass
    Returns: fuel requirements.
    '''

    return mass // 3 - 2


def calc_fuel_req_adjusted(mass):
    '''
    Fuel itself requires fuel just like a module - take its mass,
    divide by three, round down, and subtract 2. However, that fuel
    also requires fuel, and that fuel requires fuel, and so on. 
    Any mass that would require negative fuel should instead be treated
    as if it requires zero fuel; the remaining mass, if any, is instead
    handled by wishing really hard, which has no mass and is outside
    the scope of this calculation.

    Args:
        mass: module mass
    Returns: fuel requirements.
    '''

    fuel = calc_fuel_req(mass)

    if fuel <= 0:
        return 0
    else:
        return fuel + calc_fuel_req_adjusted(fuel)


if __name__ == '__main__':
    module_mass = load_module_mass('mass_input.txt')

    fuel_per_module = map(calc_fuel_req, module_mass)
    fuel_sum  = sum(fuel_per_module)
    print(f'Fuel requirement is {fuel_sum}')

    fuel_per_module_adj = map(calc_fuel_req_adjusted, module_mass)
    fuel_sum_adj  = sum(fuel_per_module_adj)
    print(f'Fuel requirement adjusted {fuel_sum_adj}')