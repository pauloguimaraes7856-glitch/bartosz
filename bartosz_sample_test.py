import unittest
import os
import sys

test_directory = os.path.dirname(__file__)
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from tests.ads import AdsTestCase

import_exception = None
try:
    from homework.bartosz_vm import emulate
except Exception as e:
    print(e)
    import_exception = e

num_repetitions = 100
test_size = 10


class BartoszTestCase(AdsTestCase):

    def test_basic(self):
        test = [
            'LABEL', 'test',
            # 'PRINTSTACK',
            'LOCALS', 3,
            # 'PRINTSTACK',
            'CONST_I32', 100,
            'STORE', 0,
            'CONST_I32', 200,
            'STORE', 1,
            'CONST_I32', 300,
            'STORE', 2,
            # 'PRINTSTACK',

            # arg 0 + local 0 = 43 + 0 = 43
            'LOAD', 0,  # 100
            'LDARG', 0,  # 43
            'ADD_I32',  # 143
            'STORE', 0,  # local 0 <- 143

            # arg 0 + local 1 = 43 +
            'LOAD', 1,  # 200
            'LDARG', 0,  # 43
            'ADD_I32',  # 243
            'STORE', 1,  # local 1 <- 243

            # increment 75 -> 76
            'LOAD', 2,  # 300
            'LDARG', 0,  # 43
            'ADD_I32',  # 343
            'STORE', 2,  # local 2 <- 343

            'LDARG', 1,  # 42
            # 'PRINTSTACK',
            'RET',  # returning 4

            'LABEL', 'entry',
            # 'PRINTSTACK',
            'CONST_I32', 42,
            # 'PRINTSTACK',
            'CONST_I32', 43,
            # 'PRINTSTACK',
            'CALL', 'test', 2,
            # 'PRINTSTACK',
            'DUP',
            'PRINT',
            # 'PRINTSTACK',
            'HALT'
        ]
        self.assertEqual(emulate(test, entry='entry', trace=False),
                         [42])

    def test_add_1(self):
        # ('ADD_I32', instr_add_i32, 0),  # int add
        self.assertEqual(emulate(['CONST_I32', 42,
                                  'CONST_I32', 43,
                                  'ADD_I32']),
                         [85])
        self.assertEqual(emulate(['CONST_I32', 2 ** 31 - 1,
                                  'CONST_I32', 1,
                                  'ADD_I32']),
                         [-2 ** 31])

    def test_add_2(self):
        for a in range(-num_repetitions, num_repetitions):
            for b in range(-num_repetitions, num_repetitions):
                self.assertEqual(emulate(['CONST_I32', a,
                                          'CONST_I32', b,
                                          'ADD_I32']),
                                 [a + b])

    def test_LT_I32(self):
        # ('LT_I32', instr_lt_i32, 0),  # int less than
        self.assertEqual(emulate(['CONST_I32', 2,
                                  'CONST_I32', 3,
                                  'LT_I32',
                                  'HALT']),
                         [1])

        self.assertEqual(emulate(['CONST_I32', 4,
                                  'CONST_I32', 3,
                                  'LT_I32',
                                  'HALT']),
                         [0])

        self.assertEqual(emulate(['CONST_I32', 2 ** 31 - 1,
                                  'CONST_I32', 1,
                                  'ADD_I32',
                                  'CONST_I32', 0,
                                  'LT_I32',  # 32 bit integer overflow
                                  'HALT']),
                         [1])

    # This test case tests that LDARG references the correct value
    #   passed to a function.
    def test_LDARG_1(self):
        # ('LDARG', instr_ldarg, 1),
        self.assertEqual(emulate(['CONST_I32', 41,
                                  'CONST_I32', 42,  # arg 1
                                  'CONST_I32', 43,  # arg 0
                                  'CALL', 'test-3-arg', 3,
                                  'HALT',
                                  'LABEL', 'test-3-arg',
                                  # now return arg 0, v=43
                                  'LDARG', 0,
                                  'RET']),
                         # when test-3-arg returns, the stack contains 43
                         [43])
        self.assertEqual(emulate(['CONST_I32', 41,
                                  'CONST_I32', 42,  # arg 1
                                  'CONST_I32', 43,  # arg 0
                                  'CALL', 'test-3-arg', 3,
                                  'HALT',
                                  'LABEL', 'test-3-arg',
                                  # now return arg 1, v=42
                                  'LDARG', 1,
                                  'RET']),
                         [42])
        self.assertEqual(emulate(['CONST_I32', 41,
                                  'CONST_I32', 42,  # arg 1
                                  'CONST_I32', 43,  # arg 0
                                  'CALL', 'test-3-arg', 3,
                                  'HALT',
                                  'LABEL', 'test-3-arg',
                                  # now return arg 2, v=41
                                  'LDARG', 2,
                                  'RET']),
                         [41])

    def test_fibonacci_emulate(self):
        from homework.bartosz_fibonacci import fibonacci
        self.assertEqual(emulate(fibonacci, 'ffi', stack=[6]),
                         [8])
        self.assertEqual(emulate(fibonacci, 'ffi', stack=[5]),
                         [5])

    def test_fibonacci_call(self):
        from homework.bartosz_fibonacci import fibonacci
        from homework.bartosz_vm import VM

        vm = VM(fibonacci)
        self.assertEqual(vm(6),
                         8)
        self.assertEqual(vm(7),
                         13)

    def test_factorial_emulate(self):
        from homework.bartosz_fibonacci import factorial
        self.assertEqual(emulate(factorial, 'ffi', stack=[0]),
                         [1])
        self.assertEqual(emulate(factorial, 'ffi', stack=[1]),
                         [1])
        self.assertEqual(emulate(factorial, 'ffi', stack=[2]),
                         [2])
        self.assertEqual(emulate(factorial, 'ffi', stack=[6]),
                         [2 * 3 * 4 * 5 * 6])

    def test_factorial_call(self):
        from homework.bartosz_vm import VM
        from homework.bartosz_fibonacci import factorial

        vm = VM(factorial)
        self.assertEqual(vm(6),
                         2 * 3 * 4 * 5 * 6)
        self.assertEqual(vm(7),
                         2 * 3 * 4 * 5 * 6 * 7)

    def test_absval(self):
        # here we test the user's implementation of absval against python's abs
        from homework.bartosz_absval import absval
        from homework.bartosz_vm import VM

        vm = VM(absval)
        for a in range(-test_size, test_size):
            self.assertEqual(abs(a), vm(a))

    def test_PRINT_0(self):
        # PRINT should output to stdout and leave stack empty
        result = emulate(['CONST_I32', 42, 'PRINT', 'HALT'])
        self.assertEqual(result, [])

    def test_PRINTSTACK_0(self):
        # PRINTSTACK should output debug info but not modify stack
        result = emulate(['CONST_I32', 1, 'CONST_I32', 2, 'PRINTSTACK', 'HALT'])
        self.assertEqual(result, [1, 2])

    def test_NOP_0(self):
        # NOP should do nothing
        result = emulate(['CONST_I32', 42, 'NOP', 'HALT'])
        self.assertEqual(result, [42])

    def test_LABEL_0(self):
        # LABEL should work with jumps
        result = emulate(['LABEL', 'test 0',
                          'JMP', 'test 1',
                          'HALT',
                          'LABEL', 'test 1',
                          'CONST_I32', 42,
                          'HALT'])
        self.assertEqual(result, [42])

    def test_MUL_I32(self):
        # Basic multiplication
        self.assertEqual(emulate(['CONST_I32', 6, 'CONST_I32', 7, 'MUL_I32', 'HALT']), [42])
        # Test overflow
        from homework.bartosz_assembler import justify
        big_num = 2 ** 16
        expected = justify(big_num * big_num)
        self.assertEqual(emulate(['CONST_I32', big_num, 'CONST_I32', big_num, 'MUL_I32', 'HALT']),
                         [expected])

    def test_DIV_I32(self):
        # Basic division
        self.assertEqual(emulate(['CONST_I32', 42, 'CONST_I32', 6, 'DIV_I32', 'HALT']), [7])
        # Division by zero should return -1
        self.assertEqual(emulate(['CONST_I32', 42, 'CONST_I32', 0, 'DIV_I32', 'HALT']), [-1])

    def test_MOD_I32(self):
        # Basic modulo
        self.assertEqual(emulate(['CONST_I32', 43, 'CONST_I32', 6, 'MOD_I32', 'HALT']), [1])
        # Modulo by zero should return -1
        self.assertEqual(emulate(['CONST_I32', 43, 'CONST_I32', 0, 'MOD_I32', 'HALT']), [-1])

    def test_EQ_I32_0(self):
        # Equal values
        self.assertEqual(emulate(['CONST_I32', 42, 'CONST_I32', 42, 'EQ_I32', 'HALT']), [1])
        # Unequal values
        self.assertEqual(emulate(['CONST_I32', 42, 'CONST_I32', 43, 'EQ_I32', 'HALT']), [0])

    def test_JMP_0(self):
        # Unconditional jump should skip over instructions
        result = emulate(['JMP', 'test 0',
                          'CONST_I32', 13,
                          'HALT',
                          'LABEL', 'test 0',
                          'CONST_I32', 42,
                          'HALT'])
        self.assertEqual(result, [42])

    def test_JMPT_0(self):
        # Jump when condition is true (non-zero)
        result = emulate(['CONST_I32', 7,  # True condition
                          'JMPT', 'test 0',
                          'CONST_I32', 13,
                          'HALT',
                          'LABEL', 'test 0',
                          'CONST_I32', 42,
                          'HALT'])
        self.assertEqual(result, [42])

    def test_JMPF_0(self):
        # Jump when condition is false (zero)
        result = emulate(['CONST_I32', 0,  # False condition
                          'JMPF', 'test 0',
                          'CONST_I32', 13,
                          'HALT',
                          'LABEL', 'test 0',
                          'CONST_I32', 42,
                          'HALT'])
        self.assertEqual(result, [42])

    def test_CONST_I32_0(self):
        # Push various constants
        self.assertEqual(emulate(['CONST_I32', 42, 'HALT']), [42])
        self.assertEqual(emulate(['CONST_I32', 0, 'HALT']), [0])
        self.assertEqual(emulate(['CONST_I32', -13, 'HALT']), [-13])

    def test_LOCALS_I32_0(self):
        # LOCALS should reserve space on stack
        result = emulate(['LOCALS', 3, 'HALT'])
        self.assertEqual(result, [0, 0, 0])  # 3 zeros pushed

    def test_LDARG_0(self):
        # Test loading arguments in function calls
        result = emulate(['CONST_I32', 100,
                          'CONST_I32', 101,
                          'CALL', 'test 0', 2,
                          'HALT',
                          'LABEL', 'test 0',
                          'LDARG', 0,  # Should return 101 (most recent arg)
                          'RET'])
        self.assertEqual(result, [101])

    def test_LDARG_1(self):
        # Test loading second argument
        result = emulate(['CONST_I32', 100,
                          'CONST_I32', 101,
                          'CALL', 'test 0', 2,
                          'HALT',
                          'LABEL', 'test 0',
                          'LDARG', 1,  # Should return 100 (second arg)
                          'RET'])
        self.assertEqual(result, [100])

    def test_GLOAD_0(self):
        # Test global load/store
        result = emulate(['CONST_I32', 100,
                          'GSTORE', 0,
                          'CONST_I32', 101,
                          'GSTORE', 1,
                          'GLOAD', 1,
                          'HALT'],
                         num_globals=2)
        self.assertEqual(result, [101])

    def test_POP_0(self):
        # POP should remove top element
        self.assertEqual(emulate(['CONST_I32', 42, 'CONST_I32', 43, 'POP', 'HALT']), [42])

    def test_DUP_0(self):
        # DUP should duplicate top element
        self.assertEqual(emulate(['CONST_I32', 100, 'DUP', 'HALT']), [100, 100])

    def test_HALT_0(self):
        # HALT should stop execution
        self.assertEqual(emulate(['CONST_I32', 100, 'HALT']), [100])

    def test_CALL_0(self):
        # Test basic function call
        result = emulate(['CONST_I32', 100,
                          'CONST_I32', 101,
                          'CALL', 'test 0', 2,
                          'HALT',
                          'LABEL', 'test 0',
                          'CONST_I32', 0,  # Return value
                          'RET'])  # Proper return
        self.assertEqual(result, [0])

    def test_RET_0(self):
        # Test function return with value
        result = emulate(['CONST_I32', 100,
                          'CALL', 'test 0', 1,
                          'HALT',
                          'LABEL', 'test 0',
                          'CONST_I32', 42,  # Return value
                          'RET'])
        self.assertEqual(result, [42])

    def test_SYMBOL_0(self):
        # Test symbol definition
        result = emulate(['SYMBOL', 'X', 42,
                          'CONST_I32', 'X',
                          'HALT'])
        self.assertEqual(result, [42])

    def test_LAND_0(self):
        # Logical AND tests
        self.assertEqual(emulate(['CONST_I32', 1, 'CONST_I32', 1, 'LAND', 'HALT']), [1])  # True AND True
        self.assertEqual(emulate(['CONST_I32', 1, 'CONST_I32', 0, 'LAND', 'HALT']), [0])  # True AND False
        self.assertEqual(emulate(['CONST_I32', 0, 'CONST_I32', 1, 'LAND', 'HALT']), [0])  # False AND True
        self.assertEqual(emulate(['CONST_I32', 0, 'CONST_I32', 0, 'LAND', 'HALT']), [0])  # False AND False

    def test_LOR_0(self):
        # Logical OR tests
        self.assertEqual(emulate(['CONST_I32', 1, 'CONST_I32', 1, 'LOR', 'HALT']), [1])  # True OR True
        self.assertEqual(emulate(['CONST_I32', 1, 'CONST_I32', 0, 'LOR', 'HALT']), [1])  # True OR False
        self.assertEqual(emulate(['CONST_I32', 0, 'CONST_I32', 1, 'LOR', 'HALT']), [1])  # False OR True
        self.assertEqual(emulate(['CONST_I32', 0, 'CONST_I32', 0, 'LOR', 'HALT']), [0])  # False OR False

    def test_LXOR_0(self):
        # Logical XOR tests
        self.assertEqual(emulate(['CONST_I32', 1, 'CONST_I32', 1, 'LXOR', 'HALT']), [0])  # True XOR True
        self.assertEqual(emulate(['CONST_I32', 1, 'CONST_I32', 0, 'LXOR', 'HALT']), [1])  # True XOR False
        self.assertEqual(emulate(['CONST_I32', 0, 'CONST_I32', 1, 'LXOR', 'HALT']), [1])  # False XOR True
        self.assertEqual(emulate(['CONST_I32', 0, 'CONST_I32', 0, 'LXOR', 'HALT']), [0])  # False XOR False

    def test_LNOT_0(self):
        # Logical NOT tests
        self.assertEqual(emulate(['CONST_I32', 0, 'LNOT', 'HALT']), [1])  # NOT False = True
        self.assertEqual(emulate(['CONST_I32', 1, 'LNOT', 'HALT']), [0])  # NOT True = False
        self.assertEqual(emulate(['CONST_I32', 42, 'LNOT', 'HALT']), [0])  # NOT non-zero = False

    def test_BAND_0(self):
        # Bitwise AND tests
        for a in range(-num_repetitions, num_repetitions):
            for b in range(-num_repetitions, num_repetitions):
                from homework.bartosz_assembler import justify
                expected = justify(a & b)
                result = emulate(['CONST_I32', a, 'CONST_I32', b, 'BAND', 'HALT'])
                self.assertEqual(result, [expected])

    def test_BOR_0(self):
        # Bitwise OR tests
        for a in range(-num_repetitions, num_repetitions):
            for b in range(-num_repetitions, num_repetitions):
                from homework.bartosz_assembler import justify
                expected = justify(a | b)
                result = emulate(['CONST_I32', a, 'CONST_I32', b, 'BOR', 'HALT'])
                self.assertEqual(result, [expected])

    def test_BXOR_0(self):
        # Bitwise XOR tests
        for a in range(-num_repetitions, num_repetitions):
            for b in range(-num_repetitions, num_repetitions):
                from homework.bartosz_assembler import justify
                expected = justify(a ^ b)
                result = emulate(['CONST_I32', a, 'CONST_I32', b, 'BXOR', 'HALT'])
                self.assertEqual(result, [expected])

    def test_BNOT_0(self):
        # Bitwise NOT tests
        for a in range(-num_repetitions, num_repetitions):
            from homework.bartosz_assembler import justify
            expected = justify(~a)
            result = emulate(['CONST_I32', a, 'BNOT', 'HALT'])
            self.assertEqual(result, [expected])

    def test_BAND_1(self):
        # Additional bitwise AND test with specific patterns
        # Test with specific bit patterns
        result = emulate(['CONST_I32', 0b1010, 'CONST_I32', 0b1100, 'BAND', 'HALT'])
        self.assertEqual(result, [0b1000])  # 1010 & 1100 = 1000

    def test_BOR_1(self):
        # Additional bitwise OR test with specific patterns
        result = emulate(['CONST_I32', 0b1010, 'CONST_I32', 0b1100, 'BOR', 'HALT'])
        self.assertEqual(result, [0b1110])  # 1010 | 1100 = 1110

if __name__ == '__main__':
    unittest.main()