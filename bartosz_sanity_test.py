# This file contributes to the implementation of the Bartosz Virtual Machine
# https://www.bartoszsypytkowski.com/simple-virtual-machine/


from bartosz_vm import emulate

test = [

    'LABEL', 'test',
    'LOCALS', 3,

    # increment 13 -> 14
    'LOAD', 0,
    'LDARG', 0,
    'ADD_I32',
    'STORE', 0,

    # increment 99 -> 100
    'LOAD', 1,
    'LDARG', 0,
    'ADD_I32',
    'STORE', 1,

    # increment 75 -> 76
    'LOAD', 2,
    'LDARG', 0,
    'ADD_I32',
    'STORE', 2,

    'LDARG', 1,
    'PRINTSTACK',
    'RET',

    'LABEL', 'entry',
    'CONST_I32', 42,
    'CONST_I32', 43,
    'CALL', 'test', 2,
    'HALT'

]

if __name__ == '__main__':
    emulate(test, 'entry', single_step=True)
