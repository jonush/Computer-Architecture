"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256    # memory
        self.reg = [0] * 8      # registers
        self.pc = 0             # Program Counter
        self.running = False    # Toggle Running State

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

        # For now, we've just hardcoded a program:
        program = [
            # From print8.ls8
            0b10000010, # LDI R0,8
            0b00000000,
            0b00001000,
            0b01000111, # PRN R0
            0b00000000,
            0b00000001, # HLT
        ]

        for instruction in program:
            self.ram[address] = instruction
            address += 1

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
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

    def LDI(self):
        """Load Register Immediate: set the value of a register to an integer"""
        operand_a = self.ram_read(self.pc + 1)
        operand_b = self.ram_read(self.pc + 2)
        self.reg[operand_a] = operand_b

    def PRN(self):
        """Print Register: print the numeric value stored in a given register"""
        address = self.ram_read(self.pc + 1)
        print(self.reg[address])
    
    def HLT(self):
        """Halt: halt the CPU (& exit the emulator)"""
        self.running = False

    def run(self):
        """Run the CPU."""
        self.running = True

        # Machine Code Values shown in binary
        LDI = 0b10000010
        PRN = 0b01000111
        HLT = 0b00000001

        while self.running:
            # initialize Instruction Register with
            # value of RAM array at index of [Program Count] (initially 0)
            ir = self.ram_read(self.pc)

            # if program is to load register immediate
            if ir == LDI:                   
                self.LDI()
                self.pc += 3
            # if program is to print register
            elif ir == PRN:                 
                self.PRN()
                self.pc += 2
            # if program is to halt programs and exit CPU emulator
            elif ir == HLT:                 
                self.HLT()
                self.pc += 1