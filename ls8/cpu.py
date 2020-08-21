"""CPU functionality."""

import sys

# Machine Code Values shown in binary
LDI = 0b10000010
AND = 0b10101000
OR = 0b10101010
XOR = 0b10101011
NOT = 0b01101001
SHL = 0b10101100
SHR = 0b10101101
MOD = 0b10100100
ADD = 0b10100000
MUL = 0b10100010
PRN = 0b01000111
HLT = 0b00000001
PUSH = 0b01000101
POP = 0b01000110
CALL = 0b01010000
RET = 0b00010001
CMP = 0b10100111
JMP = 0b01010100
JEQ = 0b01010101
JNE = 0b01010110

class CPU:
    """Main CPU class."""


    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256        # memory
        self.reg = [0] * 8          # registers
        self.SP = 7                 # set Stack Pointer to index [7]
        self.reg[self.SP] = 0xf4    # Stack Pointer
        self.pc = 0                 # Program Counter
        self.fl = 0b00000000        # Flags Register
        self.running = False        # Toggle Running State
        self.branchtable = {        # initialize the branch table
            LDI: self.handle_LDI,
            AND: self.handle_AND,
            OR: self.handle_OR,
            XOR: self.handle_XOR,
            NOT: self.handle_NOT,
            SHL: self.handle_SHL,
            SHR: self.handle_SHR,
            MOD: self.handle_MOD,
            ADD: self.handle_ADD,
            MUL: self.handle_MUL,
            PRN: self.handle_PRN,
            HLT: self.handle_HLT,
            PUSH: self.handle_PUSH,
            POP: self.handle_POP,
            CALL: self.handle_CALL,
            RET: self.handle_RET,
            CMP: self.handle_CMP,
            JMP: self.handle_JMP,
            JEQ: self.handle_JEQ,
            JNE: self.handle_JNE,
        }

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
        elif op == "AND":
            self.reg[reg_a] &= self.reg[reg_b]
        elif op == "OR":
            self.reg[reg_a] |= self.reg[reg_b]
        elif op == "XOR":
            self.reg[reg_a] ^= self.reg[reg_b]
        elif op == "NOT":
            self.reg[reg_a] = ~self.reg[reg_a]
        elif op == "SHL":
            self.reg[reg_a] <<= self.reg[reg_b]
        elif op == "SHR":
            self.reg[reg_a] >>= self.reg[reg_b]
        elif op == "CMP":
            if self.reg[reg_a] < self.reg[reg_b]:
                self.fl |= 0b00000100
            elif self.reg[reg_a] > self.reg[reg_b]:
                self.fl |= 0b00000010
            elif self.reg[reg_a] == self.reg[reg_b]:
                self.fl |= 0b00000001
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            self.fl,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def handle_CALL(self, operand_a):
        """Call a subroutine function at the address stored in the register"""
        # decrement the stack pointer
        self.reg[self.SP] -= 1
        # save value of program counter + 2 to ram address at register[SP] 
        self.ram_write(self.reg[self.SP], self.pc + 2)
        self.pc = self.reg[operand_a]

    def handle_RET(self):
        """Return from the subroutine"""
        # set program counter to the return address
        self.pc = self.ram_read(self.reg[self.SP])
        # increment the stack pointer
        self.reg[self.SP] += 1

    def handle_LDI(self, operand_a, operand_b):
        """Load Register Immediate: set the value of a register to an integer"""
        self.reg[operand_a] = operand_b

    def handle_PRN(self, address):
        """Print Register: print the numeric value stored in a given register"""
        print(self.reg[address])
        
    def handle_CMP(self, operand_a, operand_b):
        """handles Comparison ALU operations"""
        # provide parameters for comparison operations
        self.alu("CMP", operand_a, operand_b)

    def handle_AND(self, operand_a, operand_b):
        # provide parameters for bitwise AND operation
        self.alu("AND", operand_a, operand_b)

    def handle_OR(self, operand_a, operand_b):
        # provide parameters for bitwise OR operation
        self.alu("OR", operand_a, operand_b)

    def handle_XOR(self, operand_a, operand_b):
        # provide parameters for bitwise XOR operation
        self.alu("XOR", operand_a, operand_b)

    def handle_NOT(self, operand_a, operand_b = None):
        # provide parameters for alu NOT operation
        self.alu("NOT", operand_a, operand_b)

    def handle_SHL(self, operand_a, operand_b):
        # provide parameters for alu SHL operation
        self.alu("SHL", operand_a, operand_b)

    def handle_SHR(self, operand_a, operand_b):
        # provide parameters for alu SHR operation
        self.alu("SHR", operand_a, operand_b)

    def handle_MOD(self, operand_a, operand_b):
        # provide parameters for alu MOD operation
        self.alu("MOD", operand_a, operand_b)

    def handle_MUL(self, operand_a, operand_b):
        """handles Multiplication ALU operations"""
        # provide parameters for multiplication operation
        self.alu("MUL", operand_a, operand_b)

    def handle_ADD(self, operand_a, operand_b):
        """handles Addition ALU operations"""
        # provide parameters for addition operation
        self.alu("ADD", operand_a, operand_b)

    def handle_PUSH(self, operand_a):
        """Push from the stack"""
        # decrement the stack pointer
        self.reg[self.SP] -= 1
        # get address at stack pointer and the actual value
        self.ram_write(self.reg[self.SP], self.reg[operand_a])

    def handle_POP(self, operand_a):
        """Pop from the stack"""
        # get address at stack pointer and value at address
        self.reg[operand_a] = self.ram_read(self.reg[self.SP])
        # increment the stack pointer
        self.reg[self.SP] += 1

    def handle_JMP(self, operand_a):
        """Jump to the address stored in the given register """
        self.pc = self.reg[operand_a]

    def handle_JEQ(self, operand_a):
        """If EQUAL is TRUE, jump to the address at the given register"""
        # if EQUAL is TRUE:
        if self.fl & 0b00000001:
            # jump
            self.handle_JMP(operand_a)
        else:
            self.pc += 2

    def handle_JNE(self, operand_a):
        """if EQUAL is FALSE, jump to the address at the given register"""
        # if EQUAL is FALSE:
        if not self.fl & 0b00000001:
            # jump
            self.handle_JMP(operand_a)
        else:
            self.pc += 2

    def handle_HLT(self):
        """Halt: halt the CPU (& exit the emulator)"""
        self.running = False

    def run(self):
        """Run the CPU."""
        self.running = True

        while self.running:
            # initialize Instruction Register with value of RAM at index[pc]
            ir = self.ram_read(self.pc)
            # identify the number of operands for an instruction
            operands = (ir & 0b11000000) >> 6
            
            if operands == 0:
                self.branchtable[ir]()
            elif operands == 1:
                self.branchtable[ir](self.ram_read(self.pc + 1))
            elif operands == 2:
                self.branchtable[ir](self.ram_read(self.pc + 1), self.ram_read(self.pc + 2))

            # if the instruction does NOT set self.pc
            if ir & 0b00010000 == 0:
                # set self.pc to number of operands + 1
                self.pc += operands + 1