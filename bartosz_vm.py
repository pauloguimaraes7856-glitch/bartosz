# This file contributes to the implementation of the Bartosz Virtual Machine
# https://www.bartoszsypytkowski.com/simple-virtual-machine/
# This file contains the definition of the `VM` class and the `emulate` function.


from typing import List, Union, Optional

from homework.bartosz_stack import *
from homework.bartosz_assembler import assemble, instructions, instructions_as_dict, justify

# stack will have fixed size
STACK_SIZE = 100
NUM_GLOBALS = 0


class VM:
    # code,      # pointer to table containing a bytecode to be executed
    # pc,        # address of instruction to be invoked as first one - entrypoint/main func
    # datasize   # total globals size required to perform a program operations
    # labels     # dict mapping labels (str) to addresses (int)
    def __init__(self,
                 code: List[int],
                 pc: int = 0,
                 datasize: int = NUM_GLOBALS,
                 stack_size: int = STACK_SIZE,
                 trace: bool = False,
                 single_step: bool = False,
                 ffi: str = 'ffi'):
        self.globals = [0] * datasize  # local scoped data
        self.labels, self.code = assemble(code)  # label dictionary and array of byte codes to be executed
        self.stack = [0] * stack_size  # virtual stack
        self.stack_size = stack_size
        self.pc = pc  # program counter (aka. IP - instruction pointer)
        # sp is the index of the top element of the stack.
        # Special case, if sp=-1, then the stack is empty
        # I.e. the size of the stack is sp + 1.
        # the elements on the stack are stack[0], ... stack[sp]
        self.sp = -1  # stack pointer
        # the first local variable (if any) is stored at fp + 1
        # i.e., LOAD 0 and STORE 0 refer to fp + 1
        #       LOAD 3 and store 3 refer to fp + 1 + 3
        self.fp = -1  # frame pointer (for local scope)
        self.trace = trace
        self.single_step = single_step
        self.ffi = ffi  # string, symbol of entry point for python function interface

    def __call__(self, *args):
        """This method allows us to call from Python.
        The given `args` are pushed onto the stack so that
        when the VM runs args[0] is LDARG 0,
        args[1] is LDARG 1, etc...
        Notice that this means __call__ mush push the args in reverse order.
        """
        if self.ffi not in self.labels:
            raise RuntimeError(f'entry point {self.ffi} not in known labels')

        self.pc = self.labels[self.ffi]
        for s in reversed(args):
            self.push(s)

        self.run(trace=self.trace)
        return self.pop()

    def push(self, v: int) -> None:
        """push value on top of the stack.
        First sp is incremented, and THAT new index
        is used to reference into the stack.
        E.g., if sp=3,  then stack[4] will be returned,
        after sp becomes 4."""
        assert self.sp < self.stack_size - 1, "stack overflow"
        assert isinstance(v, int)
        # CHALLENGE: student must complete the implementation.
        # HINT: goal <= 2 lines
        self.sp += 1
        self.stack[self.sp] = v

    def pop(self) -> int:
        """pop value from top of the stack.
        The value of the stack at index sp is returned.
        and sp is decremented.   E.g., if sp=4,
        then sp becomes 3, but stack[4] is returned.
        If sp is 0, then stack[0] is returned and sp becomes -1.
        If sp is already negative, an exception is thrown."""
        assert self.sp >= 0, "Cannot pop from empty stack"
        # CHALLENGE: student must complete the implementation.
        # HINT: goal <= 2 lines
        val, self.sp = self.stack[self.sp], self.sp - 1
        return val

    def ncode(self) -> int:
        """get next bytecode.
        Return the value at code[pc],
        and increment pc.  E.g., if pc=4,
        then code[4] is returned, and pc is incremented to 5.
        Note: pc is an index into code[].  If pc points outside
        code[] then no error is thrown, rather the opcode
        of HALT is returned.
        This means users do not have to end their program with
        an explicit HALT.
        """
        if self.pc >= len(self.code):
            opcode, _f, _arity = instructions_as_dict['HALT']
            return opcode
        else:
            # CHALLENGE: student must complete the implementation.
            # HINT: goal <= 2 lines
            bytecode, self.pc = self.code[self.pc], self.pc + 1
            return bytecode

    def run(self, trace=False) -> None:
        """Start executing the VM at the current value of self.pc
        and continue until HALT is reached.
        If `trace` is true, then print stack and print a disassembled
        rendition of the instruction at self.pc
        """
        def addr_to_label(target):
            for label, addr in self.labels.items():
                if addr == target:
                    return f"[{label}]"
            return ''

        if self.single_step:
            trace = True
        while True:
            opcode = self.ncode()  # fetch
            # the code array has been converted to all int,
            assert isinstance(opcode, int)
            if opcode >= len(instructions) or opcode < 0:
                raise RuntimeError(f'invalid instruction: {opcode=}')

            mnemonic, instr, arity = instructions[opcode]
            if trace:
                instr_print_stack(self)
                print(f"   {self.pc - 1}", end='')
                print(addr_to_label(self.pc - 1), end='')
                print(f":{mnemonic}", end=' ')
                for i in range(arity):
                    print(self.code[self.pc + i], end='')
                    print(addr_to_label(self.code[self.pc + i]), end=' ')

                print('')

            if self.single_step:
                input('step > ')

            # handle HALT as special case
            if mnemonic == 'HALT':
                return

            # call ncode arity-many times, and build a list of return values of ncode.
            # then call the correct instruction function with collected return values of ncode
            # as the function arguments.
            # CHALLENGE: student must complete the implementation.
            # HINT: goal <= 2 lines
            arg_opcodes = [self.ncode() for _ in range(arity)]  # no justify(). code[] array had it in assemble()
            instr(self, *arg_opcodes)


def emulate(program: List[Union[str, int]],
            entry: Optional[str] = None,
            num_globals: int = NUM_GLOBALS,
            stack: List[int] = list(),
            trace=False,
            single_step=False) -> List[int]:
    """Compile, and execute a program on the Bartosz VM,
    return the stack remaining after the program finishes.
    If `stack` is given, it will be the initial value of vm.stack
    when the program executes.   E.g., if stack of length three
    is given then stack[0] will be LOAD 0
                  stack[1] will be LOAD 1
                  stack[2] will be LOAD 2
    """
    vm = VM(program,
            datasize=num_globals,
            single_step=single_step)
    vm.pc = 0 if entry is None else vm.labels[entry]
    for s in stack:
        vm.push(s)
    print(f"code array={vm.code}")
    print(f"labels    ={vm.labels}")
    vm.run(trace=trace)
    return vm.stack[:vm.sp + 1]


if __name__ == '__main__':
    data = ['LABEL', 'begin',
            'SYMBOL', 'val', 42,
            'CONST_I32', 'val',
            'CALL', 'sample-fun', 1,
            'HALT',
            'LABEL', 'sample-fun',
            'LDARG', 0,
            'DUP',
            'MUL_I32',
            'CONST_I32', 2,
            'MUL_I32',
            'RET'
            ]
    print(assemble(data))
