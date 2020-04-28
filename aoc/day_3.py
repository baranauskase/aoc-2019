
import csv

def load_wires(file):
    wires = []
    with open(file) as f:
        csv_reader = csv.reader(f)
        for line in csv_reader:
            wires.append(line)
    return wires


def gen_steps(move):
    steps = int(move[1:])

    if move[0] == 'U':
        for i in range(1, steps+1):
            yield (0, i)
    elif move[0] == 'D':
         for i in range(1, steps+1):
            yield (0, -i)    
    elif move[0] == 'L':
         for i in range(1, steps+1):
            yield (-i, 0)          
    elif move[0] == 'R':
         for i in range(1, steps+1):
            yield (i, 0)    
    else:
        raise IOError('Unknown direction encountered.')

def trace_wire(wire):
    trace = {}
    last_coord = (0, 0)
    steps_taken = 0
    for step_gen in map(gen_steps, wire):
        for inc in step_gen:
            coord = (last_coord[0] + inc[0], last_coord[1] + inc[1])
            steps_taken += 1
            if coord not in trace:
                trace[coord] = steps_taken
        last_coord = coord

    return trace

def calc_manhattan_dist(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

def find_intersections(trace_1, trace_2):
    s1 = set(trace_1.keys())
    s2 = set(trace_2.keys())

    intersections = s1.intersection(s2)
    return intersections

def find_closest_intersect(w1, w2):
    wire_one_trace = trace_wire(w1)
    wire_two_trace = trace_wire(w2)

    intersections = find_intersections(wire_one_trace, wire_two_trace)

    lowest_dist = None
    for i in intersections:
        dist = calc_manhattan_dist((0,0), i)
        if not lowest_dist:
            lowest_dist = dist
        elif dist < lowest_dist:
            lowest_dist = dist


    return lowest_dist


def find_earliest_intersect(w1, w2):
    wire_one_trace = trace_wire(w1)
    wire_two_trace = trace_wire(w2)

    s1 = set(wire_one_trace.keys())
    s2 = set(wire_two_trace.keys())
    
    intersections = s1.intersection(s2)

    lowest_steps = None
    for i in intersections:
        steps = wire_one_trace[i] + wire_two_trace[i]
        if not lowest_steps:
            lowest_steps = steps
        elif steps < lowest_steps:
            lowest_steps = steps


    return lowest_steps

if __name__ == '__main__':
    wires = load_wires('wire_input.txt')
    closest_int = find_closest_intersect(wires[0], wires[1])
    earliest_int = find_earliest_intersect(wires[0], wires[1])

    print(f'Distance to closest wire intersection is {closest_int}')
    print(f'Distance to earliest wire intersection is {earliest_int}')