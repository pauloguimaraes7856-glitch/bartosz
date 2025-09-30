# This file contributes to the implementation of the Bartosz Virtual Machine
# https://www.bartoszsypytkowski.com/simple-virtual-machine/
# This file contains implementation for opcodes dealing with arithmetic


#                ('ADD_I32', instr_add_i32),  # int add
def instr_add_i32(vm: 'VM'):
    # Assume the stack ends in [ ..... a, b],
    # pop off a and b, and push back a+b as 32-bit signed integer.
    # The result must be an integer -2**31 <= n < 2*31.
    # CHALLENGE: student must complete the implementation.
    # HINT: goal <= 3 lines
    from homework.bartosz_assembler import justify
    b, a = vm.pop(), vm.pop()  # right hand side: order of execution starts with b's vm.pop(), then a's vm.pop()
    vm.push(justify(a + b))
#                ('SUB_I32', instr_sub_i32),  # int sub


def instr_sub_i32(vm: 'VM'):
    # Assume the stack ends in [ ..... a, b],
    # pop off a and b, and push back a-b as 32-bit signed integer.
    # The result must be an integer -2**31 <= n < 2*31.
    # CHALLENGE: student must complete the implementation.
    # HINT: goal <= 3 lines
    from homework.bartosz_assembler import justify
    b, a = vm.pop(), vm.pop()  # right hand side: order of execution starts with b's vm.pop(), then a's vm.pop()
    vm.push(justify(a - b))

#                ('MUL_I32', instr_mul_i32),  # int mul


def instr_mul_i32(vm: 'VM'):
    # Assume the stack ends in [ ..... a, b],
    # pop off a and b, and push back a*b as 32-bit signed integer.
    # The result must be an integer -2**31 <= n < 2*31.
    # CHALLENGE: student must complete the implementation.
    # HINT: goal <= 3 lines
    from homework.bartosz_assembler import justify
    b, a = vm.pop(), vm.pop()
    vm.push(justify(a * b))


def instr_div_i32(vm: 'VM'):
    # int divide, discarding remainder, keeping quotient
    # if denominator is 0, push -1; do not raise exception
    # CHALLENGE: student must complete the implementation.
    # HINT: goal <= 6 lines
    b, a = vm.pop(), vm.pop()
    vm.push(a // b if b else -1)


def instr_mod_i32(vm: 'VM'):
    # divide, discarding quotient, keeping remainder
    # if denominator is 0, push -1; do not raise exception
    # CHALLENGE: student must complete the implementation.
    # HINT: goal <= 6 lines
    b, a = vm.pop(), vm.pop()
    vm.push(a % b if b else -1)

#                ('LT_I32', instr_lt_i32),  # int less than


def instr_lt_i32(vm: 'VM'):
    # Assume the stack ends in [ ..... a, b],
    #  pop off a and b, and push back 0 (false) or 1 (true)
    #  depending on whether a < b.
    #  E.g.,
    #     CONST_I32 4
    #     CONST_I32 12
    #     LT_I32 # 4 < 12 ?
    # CHALLENGE: student must complete the implementation.
    # HINT: goal <= 6 lines
    b, a = vm.pop(), vm.pop()
    vm.push(1 if a < b else 0)

#                ('EQ_I32', instr_eq_i32),  # int equal


def instr_eq_i32(vm: 'VM'):
    # Assume the stack ends in [ ..... a, b],
    # pop off a and b, and push back 0 (false) or 1 (true)
    # depending on whether a < b.
    # CHALLENGE: student must complete the implementation.
    # HINT: goal <= 6 lines
    b, a = vm.pop(), vm.pop()
    vm.push(1 if a == b else 0)


def instr_lnot(vm: 'VM', ):
    # logical Not.  pop a from stack, if it is False (=0) push
    # True(=1) elase push False(=0)
    # CHALLENGE: student must complete the implementation.
    # HINT: goal <= 5 lines
    a = vm.pop()
    vm.push(0 if a else 1)


def instr_bnot(vm: 'VM', ):
    # Bitwise NOT, pop 32-bit int from stack, push
    # 32-bit integer which toggles all the bits.
    # The result must be an integer -2**31 <= n < 2*31.
    # CHALLENGE: student must complete the implementation.
    # HINT: goal <= 3 lines
    a = vm.pop()
    vm.push(-(a + 1))  # twos complement of a is -(a+1)


def instr_land(vm: 'VM'):
    # Logical AND, pop a and b from stack,
    # if both a and b are logical True (i.e, different than zero)
    #   then the result is 1, otherwise the result is 0
    # CHALLENGE: student must complete the implementation.
    # HINT: goal <= 6 lines
    b, a = vm.pop(), vm.pop()
    vm.push(1 if a and b else 0)


def instr_lor(vm: 'VM'):
    # Logical O, pop a and b from stack,
    # if either a or b is logical True (i.e, different than zero)
    #   then the result is 1, otherwise the result is 0
    # CHALLENGE: student must complete the implementation.
    # CHALLENGE: student must complete the implementation.
    # HINT: goal <= 6 lines
    b, a = vm.pop(), vm.pop()
    vm.push(1 if a or b else 0)


def instr_lxor(vm: 'VM'):
    # Logical XOR, if a is True(!=0) and b is False(=0), or
    # if a is False(=0) and B is True(!=0), then True (=0) else
    # False (=0)
    # CHALLENGE: student must complete the implementation.
    # HINT: goal <= 6 lines
    b, a = vm.pop(), vm.pop()
    vm.push(1 if (a and not b) or (not a and b) else 0)


def instr_band(vm: 'VM'):
    # Bitwise AND, pop two 32-bit ints from stack,
    # push back the bitwise 32-bit AND of the two.
    # The result must be an integer -2**31 <= n < 2*31.
    # CHALLENGE: student must complete the implementation.
    # HINT: goal <= 3 lines
    b, a = vm.pop(), vm.pop()
    vm.push(a & b)


def instr_bor(vm: 'VM'):
    # Bitwise AND, pop two 32-bit ints from stack,
    # push back the bitwise 32-bit OR of the two.
    # The result must be an integer -2**31 <= n < 2*31.
    # CHALLENGE: student must complete the implementation.
    # HINT: goal <= 3 lines
    b, a = vm.pop(), vm.pop()
    vm.push(a | b)


def instr_bxor(vm: 'VM'):
    # Bitwise AND, pop two 32-bit ints from stack,
    # push back the bitwise 32-bit XOR of the two.
    # The result must be an integer -2**31 <= n < 2*31.
    # CHALLENGE: student must complete the implementation.
    # HINT: goal <= 3 lines
    b, a = vm.pop(), vm.pop()
    vm.push(a ^ b)
