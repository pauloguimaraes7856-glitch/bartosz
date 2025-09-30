# This file contributes to the implementation of the Bartosz Virtual Machine
# https://www.bartoszsypytkowski.com/simple-virtual-machine/

from typing import List, Union, Tuple, Dict
from homework.bartosz_memory import *
from homework.bartosz_flow import *
from homework.bartosz_arith import *
from homework.bartosz_stack import *

# each triple indicates a human-readable mnemonic, function object, and arity
instructions = [('NOP', instr_nop, 0),  # Empty Operation
                ('LABEL', None, 1),
                ('SYMBOL', None, 2),  # associate a symbol with value
                ('ADD_I32', instr_add_i32, 0),  # int add
                ('SUB_I32', instr_sub_i32, 0),  # int sub
                ('MUL_I32', instr_mul_i32, 0),  # int mul
                ('DIV_I32', instr_div_i32, 0),  # int divide, discarding remainder, keeping quotient
                ('MOD_I32', instr_mod_i32, 0),  # divide, discarding quotient, keeping remainder
                ('BAND', instr_band, 0),  # bitwise AND
                ('BOR', instr_bor, 0),  # bitwise OR
                ('BXOR', instr_bxor, 0),  # bitwise XOR
                ('BNOT', instr_bnot, 0),  # bitwise NOT
                ('LAND', instr_land, 0),  # logical AND
                ('LOR', instr_lor, 0),  # logical OR
                ('LXOR', instr_lxor, 0),  # logical XOR
                ('LNOT', instr_lnot, 0),  # logical NOT
                ('LT_I32', instr_lt_i32, 0),  # int less than
                ('EQ_I32', instr_eq_i32, 0),  # int equal
                ('JMP', instr_jmp, 1),  # branch
                ('JMPT', instr_jmpt, 1),  # branch if true
                ('JMPF', instr_jmpf, 1),  # branch if false
                ('CONST_I32', instr_const_i32, 1),  # push constant integer
                ('LOCALS', instr_locals, 1),  # allocate given number of local vars on the stack
                ('LOAD', instr_load, 1),  # load from local
                ('GLOAD', instr_gload, 1),  # load from global
                ('STORE', instr_store, 1),  # store in local
                ('GSTORE', instr_gstore, 1),  # store in global memory
                ('PRINT', instr_print, 0),  # print value on top of the stack
                ('PRINTSTACK', instr_print_stack, 0),  # print stack
                ('POP', instr_pop, 0),  # throw away top of the stack
                ('DUP', instr_dup, 0),
                ('HALT', None, 0),  # stop program
                ('CALL', instr_call, 2),  # call procedure
                ('LDARG', instr_ldarg, 1),
                ('RET', instr_ret, 0)  # return from procedure
                ]

# this dictionary is the inverse mapping of instructions[]
# e.g.,  instructions[3] = ('SUB_I32', instr_sub_i32, 0)
# and instructions_as_dict['SUB_I32'] = (3, instr_sub_i32, 0)
instructions_as_dict = dict((mnemonic, (index, f, arity))
                            for index, (mnemonic, f, arity) in enumerate(instructions))

max_int = 2 ** 32 - 1
min_int = -2 ** 32


def justify(n: int) -> int:
    """Integers represent 32-bit integers.
    Therefore,  we mod with 2^32, but if the result is
    larger than 2^31 - 1, then we consider it negative, i.e. subtract 2^32"""
    assert isinstance(n, int)

    n = n % (2 ** 32)
    if n >= 2 ** 31:
        n -= 2 ** 32
    assert min_int <= n <= max_int
    return n


def context(raw: List[Union[int, str]], cursor: int) -> List[Union[int, str]]:
    """Help generate useful assembler error message."""
    return raw[cursor:max(len(raw), cursor + 5)]


def tuplify(raw: List[Union[int, str]]) -> List[tuple]:
    """partition input into tuples like [('LABEL', 'xyz'), ('GLOAD', 1) ...]"""
    cursor = 0
    tuples = []
    while cursor < len(raw):
        mnemonic = raw[cursor]
        if mnemonic in instructions_as_dict:
            index, f, arity = instructions_as_dict[mnemonic]
        else:
            raise RuntimeError(f'invalid instruction: {mnemonic=} at {context(raw, cursor)}')
        if cursor + arity + 1 > len(raw):
            raise RuntimeError(f'premature end of assembly code: {mnemonic=} has {arity=}')
        tup = tuple(raw[cursor:cursor + arity + 1])
        cursor += arity + 1
        tuples.append(tup)
    return tuples


def extract_labels(in_tuples) -> Tuple[Dict[str, int], List[tuple]]:
    """iterate over `in_tuples`; when we find (LABEL, XXX) we add an entry
    to the labels[] dictionary, and remove the tuple (non-destructively).
    Returns 2 values, the labels dictionary, and the filtered list of tuples."""
    addr = 0
    out_tuples = []
    labels = dict()

    def validate_label(label):
        if not isinstance(label, str):
            raise RuntimeError(f'invalid label: {label=}, should be a string')
        if label in instructions_as_dict:
            raise RuntimeError(f'cannot use reserved word {label} as label')
        if label in labels:
            raise RuntimeError(f'duplicate label {label}')

    for cursor, tup in enumerate(in_tuples):
        mnemonic = tup[0]
        if mnemonic == 'LABEL':
            label = tup[1]
            validate_label(label)
            labels[label] = addr
        elif mnemonic == 'SYMBOL':
            # e.g  ('SYMBOL', 'X', 42)
            # e.g. ('SYMBOL', 'Y', 'X')
            label = tup[1]
            validate_label(label)
            value = tup[2]
            if value in labels:
                value = labels[value]
            if isinstance(value, int):
                labels[label] = value
        else:
            out_tuples.append(tup)
            addr += len(tup)

    return labels, out_tuples


def substitute_labels(labels, in_tuples) -> List[tuple]:
    """Generate a new list of tuples, if a label appears in the
    operands of mnemonic, then substitute the corresponding integer address
    in place."""

    def subst(tup):
        return [tup[0]] + [labels.get(a, a) for a in tup[1:]]

    return [tuple(subst(in_tuple)) for in_tuple in in_tuples]


def substitute_opcodes(in_tuples) -> List[tuple]:
    """Generate a new list of tuples, substituting integer opcodes
    for mnemonics."""

    def subst(tup):
        opcode, _f, _arity = instructions_as_dict[tup[0]]
        return [opcode] + list(tup[1:])

    return [tuple(subst(in_tuple)) for in_tuple in in_tuples]


def assemble(raw: List[Union[int, str]]) -> Tuple[Dict[str, int], List[int]]:
    """Assemble the code returning a label dictionary and a list of integers.
    The label dictionary is useful so the caller can get the address of the
    entrypoint, whatever its name is.
    If an integer in the `raw` input is greater than 2**31 - 1 or less than -2*31,
    an exception is raised."""

    # pass 1: partition into tuples
    tuples0 = tuplify(raw)

    # pass 2: create label dictionary and remove ('LABEL', ...) and ('SYMBOL', ...)
    labels, tuples1 = extract_labels(tuples0)

    # pass 3: replace label references with addresses (ie integers)
    tuples2 = substitute_labels(labels, tuples1)

    # pass 4: replace mnemonics with opcodes (ie integers)
    tuples3 = substitute_opcodes(tuples2)

    # pass 5: check for integers that require more than 32 bits.
    max_int = 2 ** 31 - 1  # 2147483647
    min_int = -(2 ** 31)  # -2147483648
    for tup in tuples3:
        for i in tup:
            if i > max_int:
                raise RuntimeError(f'integer {i=} beyond upper bound {max_int}')
            if i < min_int:
                raise RuntimeError(f'integer {i=} beyond lower bound {min_int}')

    # pass 6: flatten list of tuples to list of 32-bit integers
    code_array = [justify(a) for tup in tuples3
                  for a in tup]

    return labels, code_array


if __name__ == '__main__':
    print(2**31 - 1)
    data = ['CONST_I32', -1,
            'CONST_I32', -2147483648,
            'CONST_I32', 2147483647
            ]
    print(assemble(data))
