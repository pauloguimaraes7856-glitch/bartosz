# This file contributes to the implementation of the Bartosz Virtual Machine
# https://www.bartoszsypytkowski.com/simple-virtual-machine/


# Empty Operation


def instr_nop(vm: 'VM'):
    # do nothing and let the program continue as normal
    # CHALLENGE: student must complete the implementation.
    # HINT: goal = 1 line
    pass

# branch


def instr_jmp(vm: 'VM', addr):
    # set the program counter to the specified address
    # i.e.,  # unconditionally jump with program counter
    # CHALLENGE: student must complete the implementation.
    # HINT: goal = 1 line
    vm.pc = addr

# branch if true


def instr_jmpt(vm: 'VM', addr):
    # assume stack ends with a Boolean, if true
    # then set the program counter to the specified address
    # Pop a Boolean from the stack, if it is true
    # (i.e. any value other than 0) then update the
    # program counter to the next value read from the code.
    # CHALLENGE: student must complete the implementation.
    # HINT: goal <= 2 lines
    if vm.pop():
        vm.pc = addr

# branch if false


def instr_jmpf(vm: 'VM', addr):
    # assume stack ends with a Boolean, if false
    # then set the program counter to the specified address
    # Pop a Boolean from the stack, if it is false
    # (i.e. exactly 0) then update the
    # program counter to the next value read from the code.
    # CHALLENGE: student must complete the implementation.
    # HINT: goal <= 2 lines
    if not vm.pop():
        vm.pc = addr

#  ('CALL', address, arg_count),
# call procedure


def instr_call(vm: 'VM', addr, argc):
    # Function call protocol
    # We expect that stack has argc-many values having been pushed by the caller.
    # We expect all args to be on the stack.
    # Save the three values, argc, fp, and pc on the stack.
    # update fp to sp
    # update pc to the address of the function being called.
    #
    # CHALLENGE: student must complete the implementation.
    # HINT: goal <= 5 lines
    for _ in [argc, vm.fp, vm.pc]:  # for the fp to know how to reach the proc args (fp - (1 + 1 + argc))
        vm.push(_)  # save old fp; save program state
    vm.fp = vm.sp
    vm.pc = addr


def instr_ldarg(vm: 'VM', arg):
    # The function has been code with 0 or more arguments.
    # Get the indicated argument and push it on the stack.
    # arg 0, i.e., the first argument passed to the function is
    #      at LDARG 0
    # arg 1, i.e., 2nd argument is at LDARG 1, etc.
    # arg 0 is the argument most recently pushed
    # arg 1 is the argument pushed prior to that.
    # The index of the specified argument is relative to fp,
    #   skipping the 3 values which CALL pushed, i.e. argc, fp, and pc.
    # CHALLENGE: student must complete the implementation.
    # HINT: goal = 1 line
    vm.push(vm.stack[vm.fp - 3 - arg])  # fp - 1 - 1 - arg - 1

#                ('RET', instr_ret)  # return from procedure


def instr_ret(vm: 'VM'):
    # The RET part of the function call protocol.
    # Restore the stack to `almost` its state before the function
    # was called.  I.e., the top of the stack is the value
    # to be returned.  So save that value, then it and the
    # three values which CALL pushed, restoring sp, pc, and fp
    # to their values before CALL.  finally subtract argc from sp.
    #
    # CHALLENGE: student must complete the implementation.
    # HINT: goal <= 7 lines
    res, vm.sp = vm.pop(), vm.fp
    vm.pc, vm.fp, argc = vm.pop(), vm.pop(), vm.pop()  # Right Hand Side: in order: left to right
    vm.sp -= argc
    vm.push(res)
