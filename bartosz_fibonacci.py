# This file contributes to the implementation of the Bartosz Virtual Machine
# https://www.bartoszsypytkowski.com/simple-virtual-machine/

from homework.bartosz_vm import emulate

fibonacci = [

    # int fib(n) {
    #     if(n == 0) return 0;
    'LABEL', 'fib',  # address of the fibonacci procedure
    'LDARG', 0,  # 0 - load last function argument N
    'CONST_I32', 0,  # 2 - put 0
    'EQ_I32',  # 4 - check equality: N == 0
    'JMPF', 'if(n < 3)',  # 5 - if they are NOT equal, goto 10
    'CONST_I32', 0,  # 7 - otherwise put 0
    'RET',  # 9 - and return it

    #     if(n < 3) return 1;
    'LABEL', 'if(n < 3)',
    'LDARG', 0,  # 10 - load last function argument N
    'CONST_I32', 3,  # 12 - put 3
    'LT_I32',  # 14 - check if 3 is <= N, actually check N < 3, and jump if false
    'JMPF', 'N >= 3',  # 15 - if 3 is NOT less than N, goto 20
    'CONST_I32', 1,  # 17 - otherwise put 1
    'RET',  # 19 - and return it

    #     else return fib(n-1) + fib(n-2);
    'LABEL', 'N >= 3',
    'LDARG', 0,  # 20 - load last function argument N
    'CONST_I32', 1,  # 22 - put 1
    'SUB_I32',  # 24 - calculate: N-1, result is on the stack
    'CALL', 'fib', 1,  # 25 - call fib function with 1 arg. from the stack
    'LDARG', 0,  # 28 - load N again
    'CONST_I32', 2,  # 30 - put 2
    'SUB_I32',  # 32 - calculate: N-2, result is on the stack
    'CALL', 'fib', 1,  # 33 - call fib function with 1 arg. from the stack
    'ADD_I32',  # 36 - since 2 fibs pushed their ret values on the stack, just add them
    'RET',  # 37 - return from procedure

    # entry point from external ffi,
    # to use this entry point, create a VM, and push the argument
    # of fib onto the stack,
    # when emulate will return the nth fibonacci number where n was
    # what was pushed on the stack.
    'LABEL', 'ffi',
    'CALL', 'fib', 1,
    'HALT',

    'LABEL', 'entrypoint',  # - main function
    'CONST_I32', 3,  # 38 - put 6
    'CALL', 'fib', 1,  # 40 - call function: fib(arg) where arg = 6;
    'PRINT',  # 43 - print result
    'HALT',  # 44 - stop program

    'LABEL', 'loop',
    'CONST_I32', 10,
    'LABEL', 'next n',
    'DUP',
    'CALL', 'fib', 1,  # call fib with N at top of stack
    'PRINT',
    'CONST_I32', 1,
    'SUB_I32',  # decrement N
    'DUP',
    'CONST_I32', 0,
    'EQ_I32',  # is N == 0
    'JMPF', 'next n',
    'HALT'
]

factorial = ['LABEL', 'fac',
             'LDARG', 0,
             'CONST_I32', 2,
             'LT_I32',
             'JMPF', 'n >= 2',
             'CONST_I32', 1,  # 0! = 1 and 1! = 1
             'RET',

             'LABEL', 'n >= 2',
             'LDARG', 0,
             'CONST_I32', 1,
             'SUB_I32',
             'CALL', 'fac', 1,  # compute (n-1)!
             'LDARG', 0,
             'MUL_I32',  # n * (n-1)!
             'RET',

             'LABEL', 'entry',
             'CONST_I32', 6,
             'CALL', 'fac', 1,
             'PRINT',  # print 6! for testing
             'HALT',

             # entry point from external ffi,
             # to use this entry point, create a VM, and push the argument
             # of fib onto the stack,
             # when emulate will return the nth fibonacci number where n was
             # what was pushed on the stack.
             'LABEL', 'ffi',
             'CALL', 'fac', 1,
             'HALT',
             ]

factorial2 = ['LABEL', 'start',
              'CONST_I32', 6,
              'CALL', 'fac', 1,
              'PRINT',
              'HALT',

              'LABEL', 'ffi',
              'CALL', 'fac', 1,
              'HALT',

              'LABEL', 'fac',
              'LOCALS', 2,
              'CONST_I32', 1,
              'STORE', 0,  # f = 0
              'LDARG', 0,
              'STORE', 1,  # g = n

              'LABEL', 'loop',
              'LOAD', 1,
              'CONST_I32', 2,
              'LT_I32',  # g < 2 ?
              'JMPT', 'g < 2',
              'LOAD', 0,
              'LOAD', 1,
              'MUL_I32',
              'STORE', 0,
              'LOAD', 1,
              'CONST_I32', 1,
              'SUB_I32',
              'STORE', 1,
              'JMP', 'loop',

              'LABEL', 'g < 2',
              'LOAD', 0,
              'RET'
              ]

sample = ['CONST_I32', 6,  # a
          'CONST_I32', 7,  # b
          'DUP',
          'MUL_I32',
          'ADD_I32',
          'PRINT',
          'HALT']

sumsqr = ['CONST_I32', 0,  # acc
          'CONST_I32', 0,  # n
          'CALL', 'addsqr', 2,
          'CONST_I32', 6,  # n
          'CALL', 'addsqr', 2,
          'PRINT',
          'HALT',
          # stack = [acc, n]
          # return acc + n^2
          'LABEL', 'addsqr',
          'LDARG', 1,
          'LDARG', 0,
          'CONST_I32', 0,
          'EQ_I32',
          'JMPF', 'n != 0',
          'RET',
          'LABEL', 'n != 0',

          'LDARG', 0,
          'DUP',
          'MUL_I32',
          'ADD_I32',
          'RET'
          ]

if __name__ == '__main__':
    from bartosz_vm import VM

    # vm = VM(sumsqr, trace=False, single_step=False)
    # print(vm(0))

    # emulate(sumsqr, single_step=True)
    emulate(factorial2, 'ffi', num_globals=0, stack=[3], single_step=True)
