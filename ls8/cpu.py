"""CPU functionality."""

import sys

# Machine Code Values shown in binary
LDI = 0b10000010
MUL = 0b10100010
PRN = 0b01000111
HLT = 0b00000001
PUSH = 0b01000101
POP = 0b01000110

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256    # memory
        self.reg = [0] * 8      # registers
        self.reg[7] = 0xf4      # Stack Pointer
        self.pc = 0             # Program Counter
        self.running = False    # Toggle Running State
        self.branchtable = {}   # initialize the branch table
        self.branchtable[LDI] = self.handle_LDI
        self.branchtable[MUL] = self.alu
        self.branchtable[PRN] = self.handle_PRN
        self.branchtable[HLT] = self.handle_HLT
        self.branchtable[PUSH] = self.handle_PUSH
        self.branchtable[POP] = self.handle_POP

    def ram_read(self, MAR):
        """
        Memory Address Register (the address being read/written at)
        - can think of MAR as the index of the RAM array
        """
        return self.ram[MAR]

    def ram_write(self, MAR, MDR):
        """
        Memory Data Register (the actual data being read/written)
        - can think of MDR as the value of the RAM array at index [MAR]
        """
        self.ram[MAR] = MDR

    def load(self):
        """Load a program into memory."""

        address = 0

        with open(sys.argv[1]) as f:
            for line in f:
                line = line.strip()
                temp = line.split()

                if len(temp) == 0:
                    continue

                if temp[0][0] == "#":
                    continue

                try:
                    self.ram[address] = int(temp[0], 2)

                except ValueError:
                    print(f"Invalid number: {temp[0]}")
                    sys.exit(1)

                address += 1

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
            self.pc += 3
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def handle_LDI(self):
        """Load Register Immediate: set the value of a register to an integer"""
        operand_a = self.ram_read(self.pc + 1)
        operand_b = self.ram_read(self.pc + 2)
        self.reg[operand_a] = operand_b
        self.pc += 3

    def handle_PRN(self):
        """Print Register: print the numeric value stored in a given register"""
        address = self.ram_read(self.pc + 1)
        print(self.reg[address])
        self.pc += 2
    
    def handle_HLT(self):
        """Halt: halt the CPU (& exit the emulator)"""
        self.running = False
        self.pc += 1

    def handle_PUSH(self):
        # decrement the stack pointer
        self.reg[7] -= 1
        # get value from next line of instruction
        operand_a = self.ram_read(self.pc + 1)
        # the actual value we want to push
        value = self.reg[operand_a]
        # get the address at the stack pointer
        top_stack_address = self.reg[7]
        # store it on the stack
        self.ram[top_stack_address] = value
        # increment the program counter
        self.pc += 2

    def handle_POP(self):
        # get the address at stack pointer
        top_stack_address = self.reg[7]
        # get value at address of stack pointer
        value = self.ram[top_stack_address]
        # get next line instruction to find where to update value
        operand_a = self.ram_read(self.pc + 1)
        # update the value
        self.reg[operand_a] = value
        # increment the stack pointer
        self.reg[7] += 1
        # increment the program counter
        self.pc += 2

    def run(self):
        """Run the CPU."""
        self.running = True

        while self.running:
            # initialize Instruction Register with value
            # of RAM array at index of [Program Count] (initially 0)
            ir = self.ram[self.pc]

            # check if program requires multiplication
            if ir == MUL:
                operand_a = self.ram_read(self.pc + 1)
                operand_b = self.ram_read(self.pc + 2)
                # provide parameters for multiplication operation
                self.branchtable[ir]("MUL", operand_a, operand_b)
            # otherwise, locate program in the branch table
            else:
                # execute the program
                self.branchtable[ir]()