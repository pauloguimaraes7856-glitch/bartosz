# This file contributes to the implementation of the Bartosz Virtual Machine
# https://www.bartoszsypytkowski.com/simple-virtual-machine/



def instr_print_stack(vm: 'VM'):
    # For debugging, print stack without popping
    # stack is printed in two groups, the values before fp (and including) and the values after.
    print(f"stack[sp={vm.sp} fp={vm.fp}]: ", end='')
    if vm.sp < 0:
        print("[]+[]")
    else:
        # we ignore everything passed the end of the stack.
        clipped = vm.stack[:vm.sp + 1]
        # print stack up to and including fp
        print(clipped[:vm.fp + 1], end='+')  # part handled by fp

        # print stack starting at fp + 1 up to and including sp
        print(clipped[vm.fp + 1:])  # stack frame; part handled by sp


def instr_pop(vm: 'VM'):
    # throw away value at top of the stack.
    # CHALLENGE: student must complete the implementation.
    # HINT: goal = 1 line
    vm.sp -= 1


def instr_dup(vm: 'VM'):
    # Duplicate the top of the stack
    # CHALLENGE: student must complete the implementation.
    # HINT: goal <= 3 lines
    top = vm.pop()
    vm.push(top)
    vm.push(top)

#                ('CONST_I32', instr_const_i32),  # push constant integer


def instr_const_i32(vm: 'VM', value):
    # push the given value onto the stack
    # CHALLENGE: student must complete the implementation.
    # HINT: goal = 1 line
    vm.push(value)
