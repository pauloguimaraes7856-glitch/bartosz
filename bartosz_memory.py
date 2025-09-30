# This file contributes to the implementation of the Bartosz Virtual Machine
# https://www.bartoszsypytkowski.com/simple-virtual-machine/


def instr_locals(vm: 'VM', local_count):
    # push 0 or more 0's on the stack.
    # these effectively reserve space for local_count-many local variables.
    for i in range(local_count):
        vm.push(0)


#                ('LOAD', instr_load),  # load from local


def instr_load(vm: 'VM', offset):
    # load (push onto the stack) local value of the given offset
    # value is the next value from code to identify local variables offset start on the stack
    # CHALLENGE: student must complete the implementation.
    # HINT: goal <= 2 lines
    vm.push(vm.stack[vm.fp + offset + 1])

#                ('GLOAD', instr_gload),  # load from global


def instr_gload(vm: 'VM', addr):
    # Load value of global variable
    v = vm.globals[addr]  # ... load value from memory of the provided addres ...
    vm.push(v)  # ... and put that value on top of the stack


#                ('STORE', instr_store),  # store in local


def instr_store(vm: 'VM', offset):
    # store local value.  I.e., set local variable at given offset to the value atop the stack.
    # CHALLENGE: student must complete the implementation.
    # HINT: goal <= 2 lines
    vm.stack[vm.fp + offset + 1] = vm.pop()

#                ('GSTORE', instr_gstore),  # store in global memory


def instr_gstore(vm: 'VM', addr):
    # Set value of global variable
    v = vm.pop()  # get value from top of the stack ...
    vm.globals[addr] = v  # ... and store value at address received


#                ('PRINT', instr_print),  # print value on top of the stack


def instr_print(vm: 'VM'):
    # pop value from top of the stack and print it
    # CHALLENGE: student must complete the implementation.
    # HINT: goal = 1 line
    print(vm.pop())
