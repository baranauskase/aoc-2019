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
    elif instruction == 3:
        return ReadInput(modes)
    elif instruction == 4:
        return PrintOutput(modes)
    elif instruction == 5:
        return JumpIfTrue(modes)
    elif instruction == 6:
        return JumpIfFalse(modes)
    elif instruction == 7:
        return LessThan(modes)
    elif instruction == 8:
        return Equals(modes)
    else:
        raise IOError('Unknown instruction.')

class Operator:
    def __init__(self, num_inputs, modes):
        self._num_inputs = num_inputs
        self._modes = modes
        self._advance_steps = 1 + self._num_inputs
        self._current_program = None

    def exec(self, program):
        self._current_program = program

        inputs = self._read_inputs()
        output = self._do_operation(inputs)

        has_output = 0
        if output is not None:
            self._write_output(output)
            has_output = 1
        
        self._advance_program(has_output)
        self._current_program = None

    def _read_inputs(self):
        inputs = []
        for offset in range(1, self._num_inputs + 1):
            mode = self._modes[offset-1]
            position_mode = mode == 0
            immediate_mode = mode == 1
            unknown_mode = not(position_mode or immediate_mode)

            if position_mode:
                operand_addr = self._current_program.state[self._current_program.curr_adr + offset]
                inputs.append(self._current_program.state[operand_addr])
            elif immediate_mode:
                operand = self._current_program.state[self._current_program.curr_adr + offset]
                inputs.append(operand)
            elif unknown_mode:
                raise IOError('Unknown instruction mode.')

        return inputs
    
    @abstractmethod
    def _do_operation(self, inputs):
        raise IOError('Not implemented')

    def _write_output(self, output):
        write_addr = self._current_program.state[self._current_program.curr_adr + self._num_inputs + 1]
        self._current_program.state[write_addr] = output

    def _advance_program(self, has_output):
        self._current_program.curr_adr += (self._advance_steps + has_output)

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

class ReadInput(Operator):
    def __init__(self, modes):
        super().__init__(0, modes)

    def _do_operation(self, inputs):
        return int(input('Enter an int:'))

class PrintOutput(Operator):
    def __init__(self, modes):
        super().__init__(1, modes)

    def _do_operation(self, inputs):
        print(inputs[0])
        return None

class JumpIfTrue(Operator):
    def __init__(self, modes):
        super().__init__(2, modes)
        self._jump_to = None

    def _do_operation(self, inputs):
        if inputs[0] != 0:
            self._jump_to = inputs[1]
        return None

    def _advance_program(self, has_output):
        if self._jump_to:
            self._current_program.curr_adr = self._jump_to
        else:
            super()._advance_program(has_output)


class JumpIfFalse(Operator):
    def __init__(self, modes):
        super().__init__(2, modes)
        self._jump_to = None

    def _do_operation(self, inputs):
        if inputs[0] == 0:
            self._jump_to = inputs[1]
        return None

    def _advance_program(self, has_output):
        if self._jump_to:
            self._current_program.curr_adr = self._jump_to
        else:
            super()._advance_program(has_output)

class LessThan(Operator):
    def __init__(self, modes):
        super().__init__(2, modes)

    def _do_operation(self, inputs):
        if inputs[0] < inputs[1]:
            return 1
        return 0    

class Equals(Operator):
    def __init__(self, modes):
        super().__init__(2, modes)

    def _do_operation(self, inputs):
        if inputs[0] == inputs[1]:
            return 1
        return 0    


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
            op.exec(self)
