from intcode import Intcode


if __name__ == '__main__':

    program = Intcode()
    program.load_from_file('day_5.txt')
    program.exec_program()

    