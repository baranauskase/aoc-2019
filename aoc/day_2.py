from intcode import Intcode



def find_nound_and_verb_for(target, program):
    for noun in range(100):
        for verb in range(100):
            program.reset()
            program.noun = noun
            program.verb = verb
            program.exec_program() 
            if program.exit_code == target:
                return noun, verb
    return None, None

if __name__ == '__main__':

    '''
    Restore the gravity assist program (your puzzle input) to the "1202 program alarm" state 
    it had just before the last computer caught fire. To do this, before running the program,
    replace position 1 with the value 12 and replace position 2 with the value 2.
    What value is left at position 0 after the program halts?
    '''
    program = Intcode()
    program.load_from_file('incode_input.txt')
    program.noun = 12
    program.verb = 2
    program.exec_program()

    print(f'Program state is: {program.exit_code}')

    '''
    Now that we know the program is working lets determine what pair of inputs produces the output 19690720.
    The inputs should still be provided to the program by replacing the values at addresses 1 and 2, just like before.
    In this program, the value placed in address 1 is called the noun, and the value placed in address 2 is called the verb.
    Each of the two input values will be between 0 and 99, inclusive.
    '''
    noun, verb = find_nound_and_verb_for(19690720, program)
    compound = 100 * noun + verb

    print(f'Verb and noun compount for 19690720 is: {compound}')
    