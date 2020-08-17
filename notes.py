# The index into the memory array, AKA the location, address, pointer

# 1 - PRINT_HELLO
# 2 - HALT
# 3 - SAVE_REG store value in a register
# 4 - PRINT_REG  print the register value in decimal

# a big array of bytes, 8-bits per byte
memory = [
    1, # PRINT_HELLO
    3, # SAVE_REG R4 37
    4, # 4 and 37 are arguments to SAVE_REG, AKA "operands"
    37,
    4,
    4,
    2 # HALT
]

registers = [0] * 8

"""
registers[4] = 37
"""

def computer():

    running = True

    # Program Counter, index into memory of currently-executing instruction
    pc = 0

    while running:
        ir = memory[pc] # Instruction Register
        
        if ir == 1:
            print("Hello!")
            pc += 1
        elif ir == 2:
            running = False
            pc += 1
        elif ir == 3:
            reg_num = memory[pc + 1]
            value = memory[pc + 2]
            registers[reg_num] = value
            pc += 3
        elif ir == 4:
            reg_num = memory[pc + 1]
            print(registers[reg_num])
            pc += 2

# computer()

"""
WHITEBOARD CHALLENGE
---------------------------------------------

Given an object/dictionary with keys and values that consist of both strings and integers, design an algorithm to calculate and return the sum of all of the numeric values.

For example, given the following object/dictionary as input:

{
  "cat": "bob",
  "dog": 23,
  19: 18,
  90: "fish"
}

Your algorithm should return 41, the sum of the values 23 and 18.

You may use whatever programming language you'd like.
Verbalize your thought process as much as possible before writing any code. Run through the UPER problem solving framework while going through your thought process.
"""

# look through dictionary and note any key/value that is a number
# find the total sum of those numbers

def sum_of_values(d):
    nums = []

    # look through the dictionary's key and values
    for n in d.values():
        if isinstance(n, int):
            nums.append(n)

    # sum those numbers
    return sum(nums)

test = {
  "cat": "bob",
  "dog": 23,
  19: 18,
  90: "fish"
}

print(sum_of_values(test))