from abc import abstractmethod


def make_instruction(code):
    instruction = code % 100
    code = code // 100
    modes = []
    for _ in range(3):
        modes.append(code % 10)
        code = code // 10

    if instruction == 1:
        return Add(modes)
    elif instruction == 2:
        return Multiply(modes)
    else:
        raise IOError('Unknown instruction.')

class Operator:
    def __init__(self, num_inputs, modes):
        self._num_inputs = num_inputs
        self._modes = modes

    def exec(self, program):
        advance_steps = 1 + self._num_inputs
        inputs = self._read_inputs(program)
        output = self._do_operation(inputs)
        if output is not None:
            self._write_output(program, output)
            advance_steps += 1
        
        program.curr_adr += advance_steps

    def _read_inputs(self, program):
        inputs = []
        for offset in range(1, self._num_inputs + 1):
            mode = self._modes[offset-1]
            position_mode = mode == 0
            immediate_mode = mode == 1
            unknown_mode = not(position_mode or immediate_mode)

            if position_mode:
                operand_addr = program.state[program.curr_adr + offset]
                inputs.append(program.sate[operand_addr])
            elif immediate_mode:
                operand = program.state[program.curr_adr + offset]
                inputs.append(operand)
            elif unknown_mode:
                raise IOError('Unknown instruction mode.')

        return inputs
    
    @abstractmethod
    def _do_operation(self, inputs):
        raise IOError('Not implemented')

    def _write_output(self, program, output):
        write_addr = program.state[program.curr_adr + self._num_inputs + 1]
        program.state[write_addr] = output


class Add(Operator):
    def __init__(self, modes):
        super().__init__(2, modes)
    
    def _do_operation(self, inputs):
        return sum(inputs)

class Multiply(Operator):
    def __init__(self, modes):
        super().__init__(2, modes)
    
    def _do_operation(self, inputs):
        return inputs[0] * inputs[1]

class Intcode:
    
    def __init__(self):
        self._source = None
        self.state = None
        self.curr_adr = 0

    def load_from_file(self, file):
        with open(file) as f:
            line = f.readline()
            program = map(int, line.split(','))

        self._source = list(program)       
        self.reset()

    def load_directly(self, program):
        self._source = program
        self.reset() 

    def reset(self):
        self.state = list(self._source)
        self.curr_adr = 0

    @property
    def current_op(self):
        if not self.state:
            raise IOError('Program not loaded.')
        return self.state[self.curr_adr]

    @property
    def exit_code(self):
        if self.current_op != 99:
            raise IOError('Program not executed yet.')

        return self.state[0]

    @property
    def noun(self):
        if not self.state:
            raise IOError('Program not loaded.')

        return self.state[1]

    @noun.setter
    def noun(self, noun):
        if not self.state:
            raise IOError('Program not loaded.')   
        self.state[1] = noun

    @property
    def verb(self):
        if not self.state:
            raise IOError('Program not loaded.')

        return self.state[2]

    @verb.setter
    def verb(self, verb):
        if not self.state:
            raise IOError('Program not loaded.')        
        self.state[2] = verb

    def exec_program(self):
        '''
        An Intcode program is a list of integers separated by commas (like 1,0,0,3,99).
        To run one, start by looking at the first integer (called position 0).
        Here, you will find an opcode - either 1, 2, or 99. The opcode indicates what to do;
        for example, 99 means that the program is finished and should immediately halt.
        Encountering an unknown opcode means something went wrong.
        
        Opcode 1 adds together numbers read from two positions and stores the result in a third position.
        The three integers immediately after the opcode tell you these three positions - the
        first two indicate the positions from which you should read the input values,
        and the third indicates the position at which the output should be stored.

        For example, if your Intcode computer encounters 1,10,20,30, it should read the values at
        positions 10 and 20, add those values, and then overwrite the value at position 30 with their sum.

        Opcode 2 works exactly like opcode 1, except it multiplies the two inputs instead of
        adding them. Again, the three integers after the opcode indicate where the inputs and outputs are, not their values.

        Once you're done processing an opcode, move to the next one by stepping forward 4 positions.

        Args:
            program: list of ints
        Return: list of ints that represent program state
        '''
        while self.current_op != 99:
            op = make_instruction(self.current_op)
            op.exec


            if self.current_op in [1, 2]:
                operand_1 = self.state[self.state[self.curr_adr + 1]]
                operand_2 = self.state[self.state[self.curr_adr + 2]]
                write_idx = self.state[self.curr_adr + 3]
            else:
                raise IOError('Unknown operation.')
                

            if self.current_op == 1:
                self.state[write_idx] = operand_1 + operand_2
            elif self.current_op == 2:
                self.state[write_idx] = operand_1 * operand_2

            self.curr_adr += 4
        
# def exec_intcode_program(noun, verb):
#     program = Intcode()
#     program.load_directly
#     intcode_program = load_incode_program('incode_input.txt')
#     intcode_program[1] = noun
#     intcode_program[2] = verb
#     run_intcode_program(intcode_program)

#     return intcode_program[0]