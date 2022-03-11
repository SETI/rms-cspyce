import unittest

import numpy as  np
import cspyce.typemap_samples as ts


def flatten(array):
    return tuple(tuple(array.ravel()))

# noinspection PyTypeChecker
class test_array1_1(unittest.TestCase):
    # %apply (int IN_ARRAY1[ANY]) {int arg[3]}
    # cs.in_array1_1 just returns whatever 3 integers it was passed as a numpy array
    def test_basic_test_tuple(self):
        self.assertEqual((1, 2, 3), ts.in_array1_1((1, 2, 3)))

    def test_basic_test_array(self):
        array = np.arange(10, 13, dtype="int32")
        self.assertEqual(tuple(array), ts.in_array1_1(array))

    def test_non_contiguous_array(self):
        array = np.arange(9, dtype='int32').reshape((3, 3))
        self.assertEqual((0, 3, 6), ts.in_array1_1(array[:, 0]))

    def test_requires_three_elements(self):
        with self.assertRaises(ValueError):
            ts.in_array1_1((1, 2, 3, 4))

    def test_requires_integer_array(self):
        with self.assertRaises(ValueError):
            ts.in_array1_1(np.arange(3.0))

    def test_requires_one_dimensional_array(self):
        array = np.zeros((3, 3), dtype="int32")
        with self.assertRaises(ValueError):
            ts.in_array1_1(array)

    def test_requires_non_null(self):
        with self.assertRaises(TypeError):
            ts.in_array1_1(None)


class test_array1_2(unittest.TestCase):
    # %apply (int* IN_ARRAY1, int DIM1) {(int* arg, int dim)};
    # This function returns them as a list.
    def test_basic_test_tuple(self):
        self.assertEqual((1, 2, 3, 4, 5), ts.in_array1_2([1, 2, 3, 4, 5]))

    def test_basic_test_array(self):
        arg = np.arange(1, 10, dtype='int32')
        self.assertEqual(flatten(arg), ts.in_array1_2(arg))

    def test_okay_to_pass_empty_list(self):
        self.assertEqual((), ts.in_array1_2(()))

    def test_non_contiguous_array(self):
        array = np.arange(12, dtype='int32').reshape((4, 3))[:, 1]
        self.assertEqual(flatten(array), ts.in_array1_2(array))

    def test_requires_integer_array(self):
        with self.assertRaises(ValueError):
            ts.in_array1_2(np.arange(10.0))

    def test_requires_one_dimensional_array(self):
        array = np.zeros((3, 3), dtype="int32")
        with self.assertRaises(ValueError):
            ts.in_array1_2(array)

    def test_requires_one_dimensional_int_array(self):
        array = np.zeros((3, 3), dtype="double")
        with self.assertRaises(ValueError):
            ts.in_array1_2(array)

    def test_requires_non_null(self):
        with self.assertRaises(TypeError):
            ts.in_array1_2(None)

class test_array1_3(unittest.TestCase):
    # %apply (int* IN_ARRAY1, int DIM1) {(int* arg)};
    # This function is exactly like test_array_1_2, except the length is passed separately
    def test_basic_test_tuple(self):
        self.assertEqual((1, 2, 3, 4, 5), ts.in_array1_3([1, 2, 3, 4, 5], 5))

    def test_basic_test_array(self):
        arg = np.arange(1, 10, dtype='int32')
        self.assertEqual(flatten(arg), ts.in_array1_3(arg, len(arg)))

    def test_okay_to_pass_empty_list(self):
        self.assertEqual((), ts.in_array1_3((), 0))

    def test_non_contiguous_array(self):
        array = np.arange(12, dtype='int32').reshape((4, 3))[:, 1]
        self.assertEqual(flatten(array), ts.in_array1_3(array, len(array)))

    def test_requires_integer_array(self):
        with self.assertRaises(ValueError):
            ts.in_array1_3(np.arange(10.0), 1)

    def test_requires_one_dimensional_array(self):
        array = np.zeros((3, 3), dtype="int32")
        with self.assertRaises(ValueError):
            ts.in_array1_3(array, 9)

    def test_requires_one_dimensional_int_array(self):
        array = np.zeros((3, 3), dtype="double")
        with self.assertRaises(ValueError):
            ts.in_array1_3(array, 9)

    def test_requires_non_null(self):
        with self.assertRaises(TypeError):
            ts.in_array1_3(None, 0)


class test_array1_01_1(unittest.TestCase):
    # %apply (int *IN_ARRAY01, int DIM1) {(int *arg, int dim)};
    # cs.in_array01_1 received either an int scalar or sequence of integer, and
    SMALL_INT_ARRAY = np.array((4, 5, 6), dtype="int32")
    SMALL_FLOAT_ARRAY = np.array((4.0, 5.0, 6.0), dtype="double")

    def f(self, x):
        return ts.in_array01_1(x)

    def test_basic_test_scalar(self):
        self.assertEqual(1, ts.in_array01_1(1))

    def test_basic_test_tuple(self):
        self.assertEqual((1, 2, 3), ts.in_array01_1([1, 2, 3]))

    def test_basic_test_int_array(self):
        arg = np.arange(1, 10, dtype='int32')
        self.assertEqual(flatten(arg), ts.in_array01_1(arg))

    def test_non_contiguous_array(self):
        array = np.arange(12, dtype='int32').reshape((4, 3))[:, 0]
        self.assertEqual(flatten(array), ts.in_array01_1(array))

    def test_requires_integer_array(self):
        with self.assertRaises(ValueError):
            ts.in_array01_1(np.arange(20.))

    def test_requires_one_dimensional_array(self):
        array = np.zeros((3, 3), dtype="int32")
        with self.assertRaises(ValueError):
            ts.in_array01_1(array)

    def test_requires_one_dimensional_int_array(self):
        array = np.zeros((3, 3), dtype="double")
        with self.assertRaises(ValueError):
            ts.in_array01_1(array)

    def test_requires_non_null(self):
        with self.assertRaises(TypeError):
            ts.in_array01_1(None)


class test_array2_1(unittest.TestCase):
    # %apply (int IN_ARRAY2[ANY][ANY]) {int arg[3][5]};
    # This function specifically requires a 3x5 int array.
    # It returns the first element, and the dimensions as a tuple.
    def test_basic_run(self):
        array = np.arange(1000, 1015, dtype='int32').reshape(3, 5)
        self.assertEqual((flatten(array), 3, 5), ts.in_array2_1(array))

    def test_non_contiguous_array(self):
        array = np.arange(150, dtype='int32').reshape((3, 5, 10))[..., 2]
        self.assertEqual((flatten(array), 3, 5), ts.in_array2_1(array))

    def test_no_other_size(self):
        array = np.array(range(100, 115), dtype='int32').reshape(5, 3)
        with self.assertRaises(ValueError):
            ts.in_array2_1(array)

    def test_no_other_data_type(self):
        array = np.array(range(100, 115), dtype='int64').reshape(3, 5)
        with self.assertRaises(ValueError):
            ts.in_array2_1(array)

    def test_no_other_dimension(self):
        array = np.array(range(100, 115), dtype='int64').reshape(3, 5, 1)
        with self.assertRaises(ValueError):
            ts.in_array2_1(array)

    def test_requires_non_null(self):
        with self.assertRaises(TypeError):
            ts.in_array2_1(None)


class test_array2_2(unittest.TestCase):
    # %apply (int *IN_ARRAY2, int DIM1, int DIM2) {(int *arg, int dim1, int dim2)};
    # This function takes any sized integer array.
    # It returns the elements of the array as a tuple, and the dimensions
    def test_basic_run(self):
        array = np.arange(100, 200, dtype='int32').reshape(5, 20)
        self.assertEqual((flatten(array), 5, 20), ts.in_array2_2(array))
        self.assertEqual((flatten(array[1:]), 4, 20), ts.in_array2_2(array[1:]))

    def test_non_contiguous_array(self):
        array = np.arange(150, dtype='int32').reshape((3, 5, 10))[..., 2]
        self.assertEqual((flatten(array), 3, 5), ts.in_array2_2(array))

    def test_no_other_data_type(self):
        array = np.arange(100., 200.).reshape(5, 20)
        with self.assertRaises(ValueError):
            ts.in_array2_2(array)

    def test_no_bigger_dimension(self):
        array = np.arange(100, 200, dtype='int32').reshape(5, 20, 1)
        with self.assertRaises(ValueError):
            ts.in_array2_2(array)

    def test_no_smaller_dimension(self):
        array = np.arange(100, 200, dtype='int32')
        with self.assertRaises(ValueError):
            ts.in_array2_2(array)

    def test_requires_non_null(self):
        with self.assertRaises(TypeError):
            ts.in_array2_2(None)


class test_array2_3(unittest.TestCase):
    # %apply (int IN_ARRAY2[][ANY], int DIM1) {(int arg[][5], int dim1)};
    # This function takes any 2-dimensional array whose second dimension is 5.
    # It returns the elements, and the dimensions.
    def test_basic_run(self):
        array = np.arange(100, 150, dtype='int32').reshape(10, 5)
        self.assertEqual((flatten(array), 10, 5), ts.in_array2_3(array))
        self.assertEqual((flatten(array[1:]), 9, 5), ts.in_array2_3(array[1:]))

    def test_non_contiguous_array(self):
        array = np.arange(150, dtype='int32').reshape((3, 5, 10))[..., 2]
        self.assertEqual((flatten(array), 3, 5), ts.in_array2_3(array))

    def test_no_other_width(self):
        array = np.arange(100, 150, dtype='int32').reshape(5, 10)
        with self.assertRaises(ValueError):
            ts.in_array2_3(array)

    def test_no_other_data_type(self):
        array = np.arange(100, 150, dtype='float').reshape(10, 5)
        with self.assertRaises(ValueError):
            ts.in_array2_3(array)

    def test_no_bigger_dimension(self):
        array = np.arange(100, 150, dtype='int32').reshape(1, 10, 5)
        with self.assertRaises(ValueError):
            ts.in_array2_3(array)

    def test_no_smaller_dimension(self):
        array = np.arange(100, 150, dtype='int32')
        with self.assertRaises(ValueError):
            ts.in_array2_3(array)

    def test_requires_non_null(self):
        with self.assertRaises(TypeError):
            ts.in_array2_3(None)

class test_array2_3(unittest.TestCase):
    # %apply (int IN_ARRAY2[][ANY], int DIM1) {(int arg[][5], int dim1)};
    # This function takes any 2-dimensional array whose second dimension is 5.
    # It returns the elements, and the dimensions.
    def test_basic_run(self):
        array = np.arange(100, 150, dtype='int32').reshape(10, 5)
        self.assertEqual((flatten(array), 10, 5), ts.in_array2_3(array))
        self.assertEqual((flatten(array[1:]), 9, 5), ts.in_array2_3(array[1:]))

    def test_non_contiguous_array(self):
        array = np.arange(150, dtype='int32').reshape((3, 5, 10))[..., 2]
        self.assertEqual((flatten(array), 3, 5), ts.in_array2_3(array))

    def test_no_other_width(self):
        array = np.arange(100, 150, dtype='int32').reshape(5, 10)
        with self.assertRaises(ValueError):
            ts.in_array2_3(array)

    def test_no_other_data_type(self):
        array = np.arange(100, 150, dtype='float').reshape(10, 5)
        with self.assertRaises(ValueError):
            ts.in_array2_3(array)

    def test_no_bigger_dimension(self):
        array = np.arange(100, 150, dtype='int32').reshape(1, 10, 5)
        with self.assertRaises(ValueError):
            ts.in_array2_3(array)

    def test_no_smaller_dimension(self):
        array = np.arange(100, 150, dtype='int32')
        with self.assertRaises(ValueError):
            ts.in_array2_3(array)

    def test_requires_non_null(self):
        with self.assertRaises(TypeError):
            ts.in_array2_3(None)


class test_array12(unittest.TestCase):
    # %apply (int *IN_ARRAY12, int DIM1, int DIM2)  {(int *arg, int dim1, int dim2)};
    # This function can take one or two dimensional arrays.  If only one dimension,
    # then dim1 == 0.  As usual, this returns the array elements, and the dimension
    def test_run_1d(self):
        array = np.arange(100, 150, dtype='int32')
        self.assertEqual((flatten(array), 0, array.size), ts.in_array12(array))

    def test_run_2d(self):
        array = np.arange(100, 150, dtype='int32').reshape(10, 5)
        expected_result = (flatten(array),) + tuple(array.shape)
        self.assertEqual(expected_result, ts.in_array12(array))

    def test_run_on_tuple(self):
        value = (2, 3, 5, 7, 11)
        self.assertEqual((value, 0, len(value)), ts.in_array12(value))

    def test_non_contiguous_array_2d(self):
        array = np.arange(150, dtype='int32').reshape((3, 5, 10))[..., 1]
        expected_result = (flatten(array),) + tuple(array.shape)
        self.assertEqual(expected_result, ts.in_array12(array))

    def test_non_contiguous_array_1d(self):
        array = np.arange(150, dtype='int32').reshape((3, 5, 10))[1, :, 2]
        self.assertEqual((flatten(array), 0, array.size), ts.in_array12(array))

    def test_no_other_data_type(self):
        array = np.arange(100, 150, dtype='double')
        with self.assertRaises(ValueError):
            ts.in_array12(array)

    def test_no_bigger_dimensions(self):
        array = np.arange(100, 150, dtype='int32').reshape(2, 5, 5)
        with self.assertRaises(ValueError):
            ts.in_array12(array)

    def test_requires_non_null(self):
        with self.assertRaises(TypeError):
            ts.in_array12(None)

class test_array23(unittest.TestCase):
    # %apply (int *IN_ARRAY23, int DIM2, int DIM3)  {(int *arg, int dim1, int dim2, int dim3)};
    # This function can take one or two dimensional arrays.  If only one dimension,
    # then dim1 == 0.  As usual, this returns the array elements, and the dimension
    def test_run_2d(self):
        array = np.arange(100, 150, dtype='int32').reshape(10, 5)
        expected_result = (flatten(array), 0) + tuple(array.shape)
        self.assertEqual(expected_result, ts.in_array23(array))

    def test_run_3d(self):
        array = np.arange(100, 150, dtype='int32').reshape(10, 1, 5)
        expected_result = (flatten(array),) + tuple(array.shape)
        self.assertEqual(expected_result, ts.in_array23(array))

    def test_non_contiguous_array_2d(self):
        array = np.arange(150, dtype='int32').reshape((3, 5, 10))[..., 1]
        self.assertEqual((flatten(array), 0, 3, 5), ts.in_array23(array))

    def test_non_contiguous_array_3d(self):
        array = np.empty((3, 4, 5, 8), dtype='int32')[...,2]
        self.assertEqual((flatten(array), 3, 4, 5), ts.in_array23(array))

    def test_no_other_data_type(self):
        array = np.arange(100, 150, dtype='double').reshape(10, 5)
        with self.assertRaises(ValueError):
            ts.in_array23(array)

    def test_no_bigger_dimensions(self):
        array = np.arange(100, 200, dtype='int32').reshape(2, 5, 5, 2)
        with self.assertRaises(ValueError):
            ts.in_array23(array)

    def test_requires_non_null(self):
        with self.assertRaises(TypeError):
            ts.in_array23(None)


class test_out_array1(unittest.TestCase):
    # %apply (int OUT_ARRAY1[ANY]) {(int array[100])};
    # This function fills up a 100-element int array starting at the passed argument
    def test_fixed_size_array(self):
        value = ts.out_array1_1(200)
        self.assertEqual(list(range(200, 300)), list(value))

    # %apply (int OUT_ARRAY1[ANY], int *SIZE1) {(int array[100], int *size)};
    # This function can fill an array up to size 100.  The arguments are start and length
    def test_variable_size_array(self):
        value = ts.out_array1_2(200, 5)
        self.assertEqual(len(value), 5)
        self.assertEqual(value[0], 200)
        self.assertEqual(value[-1], 204)

class test_out_array1_malloced_array(unittest.TestCase):
    # %apply (int **OUT_ARRAY1, int *SIZE1) {(int **arrayP, int *size)};
    # The function mallocs an array of whatever side it needs uses the arguments as
    # start and length
    def test_malloced_array(self):
        value = ts.out_array1_malloc(1000, 5000)
        self.assertEqual(len(value), 5000)
        self.assertEqual(value[0], 1000)
        self.assertEqual(value[-1], 6000 - 1)

    def test_malloced_array_memory_failure(self):
        with self.assertRaises(MemoryError):
            ts.out_array1_malloc(-1, 5000)


class test_out_array01_malloced_array(unittest.TestCase):
    # %apply (double **OUT_ARRAY01, int *SIZE1) {(double **arrayP, int *size)};
    # Again, a malloced array, but if the function indicates size 0, then we want a scalar
    # Again, start and length, but this time we use floats
    def test_return_scalar(self):
        result = ts.out_array01_malloc(5.0, 0)
        self.assertEqual(float, type(result))
        self.assertEqual(5.0, result)

    def test_return_1d(self):
        result = ts.out_array01_malloc(5.0, 2)
        self.assertEqual((5.0, 6.0), flatten(result))

    def test_memory_error(self):
        with self.assertRaises(MemoryError):
            result = ts.out_array01_malloc(-1.0, 10)


class test_out_array2(unittest.TestCase):
    # %apply (int OUT_ARRAY2[ANY][ANY]) {(int array[2][3])};
    # returns a fixed size array filled with the indicated starting number
    def test_fixed_size_array(self):
        # Returns a fixed sized 2x3 array filled with integers starting from 100
        value = ts.out_array2_1(100)
        self.assertEqual((2, 3), value.shape)
        self.assertEqual(value[0,0], 100)

    # %apply (int OUT_ARRAY2[ANY][ANY], int *SIZE1) {(int array[1000][2], int *size)};
    # returns an Nx2 array.  Arguments are start value and length
    def test_variable_size_array(self):
        value = ts.out_array2_2(30, 10)
        self.assertEqual((10, 2), value.shape)
        self.assertEqual(30, value[0, 0])

    # %apply (int **OUT_ARRAY12, int *SIZE1, int *SIZE2) {(int **result, int *size1, int *size2)};
    # Malloced array.  Our function has arguments start value, and dim1, dim2
    # If the start value is < 0, instead, it simulates a malloc failure
    def test_malloced_array(self):
        value = ts.out_array2_3(25, 40, 41)
        self.assertEqual((40, 41), value.shape)
        self.assertEqual(25, value[0, 0])

    def test_memory_error(self):
        with self.assertRaises(MemoryError):
            value = ts.out_array2_3(-1, 40, 41)

    # %apply (int DIM1, int *SIZE1, double OUT_ARRAY2[ANY][ANY]) {(int dim1, int *size1, double result[4][5])};
    def test_2dim_fixed_size_array(self):
        array_length, result = ts.out_array2_4(10, 3)
        self.assertEqual(4, array_length);  # Why does the function need this?
        self.assertEqual((3, 5), result.shape)
        self.assertEqual(flatten(np.arange(10.0, 25.0)), flatten(result))

    # %apply (int *SIZE1, double OUT_ARRAY2[ANY][ANY]) {(int *size1, double result[4][5])};
    def test_2dim_fixed_size_array(self):
        result = ts.out_array2_5(2)
        self.assertEqual((2, 5), result.shape)
        # This generates a boolean array in which the elemnts whose index is a multiple of 3
        # is true.  Just not worth dealing with this

class test_out_array12(unittest.TestCase):
    # %apply (int **OUT_ARRAY12, int *SIZE1, int *SIZE2) {(int **result, int *size1, int *size2)};
    # Same as before, but a dim1=0 indicates to return a 1-dimensional array
    def test_2d_array(self):
        value1 = ts.out_array12_1(25, 40, 41)
        self.assertEqual((40, 41), value1.shape)
        self.assertEqual(25, value1[0, 0])

    def test_generating_1d_array(self):
        value2 = ts.out_array12_1(25, 0, 41)
        self.assertEqual((41,), value2.shape)
        self.assertEqual(25, value2[0])

    def test_memory_error(self):
        with self.assertRaises(MemoryError):
            ts.out_array2_3(-1, 40, 41)


class test_out_array23(unittest.TestCase):
    # %apply (double **OUT_ARRAY23, int *SIZE1, int *SIZE2, int *SIZE3) {(double **result, int *size1, int *size2, int *size3)};
    # Same as before, but 2 or 3 dimensions
    def test_yields_3d(self):
        value1 = ts.out_array23_1(25, 3, 4, 5)
        self.assertEqual((3, 4, 5), value1.shape)
        self.assertEqual(25, value1[0, 0, 0])

    def test_yields_2d(self):
        value2 = ts.out_array23_1(25, 0, 4, 5)
        self.assertEqual((4, 5), value2.shape)
        self.assertEqual(25, value2[0, 0])

    def test_memory_error(self):
        with self.assertRaises(MemoryError):
            ts.out_array23_1(-1, 0, 4, 5)

class test_inout_array_1d(unittest.TestCase):
    # double_in_out_array doubles each element in the array.
    # cs.in_array1_1 just returns whatever 3 integers it was passed as a numpy array
    def test_basic_test_tuple(self):
        self.assertEqual((2, 4, 6), flatten(ts.double_in_out_array((1, 2, 3))))

    def test_basic_test_array(self):
        array = np.arange(10, 13, dtype="int32")
        self.assertEqual((20, 22, 24), flatten(ts.double_in_out_array(array)))
        # verify that array itself hasn't been touched
        self.assertEqual((10, 11, 12), flatten(array))

    def test_non_contiguous_array(self):
        array = np.arange(9, dtype='int32').reshape((3, 3))
        self.assertEqual((0, 6, 12), flatten(ts.double_in_out_array(array[:, 0])))

    def test_requires_integer_array(self):
        with self.assertRaises(ValueError):
            ts.double_in_out_array(np.arange(3.0))

    def test_requires_one_dimensional_array(self):
        array = np.zeros((3, 3), dtype="int32")
        with self.assertRaises(ValueError):
            ts.double_in_out_array(array)

    def test_requires_non_null(self):
        with self.assertRaises(TypeError):
            ts.double_in_out_array(None)



class test_single_strings_input(unittest.TestCase):
    # %apply (char *CONST_STRING) {(const char *string)};
    # our function just returns the length
    def test_const_string(self):
        self.assertEqual(5, ts.const_string_0("abcde"))

    def test_const_string_bad_input(self):
        with self.assertRaises(ValueError):
            ts.const_string_0(23)

    def test_const_string_null_input(self):
        with self.assertRaises(ValueError):
            ts.const_string_0(None)

    # %apply (char IN_STRING) {(char value)};
    # our function accepts a character, and returns it as its integer value
    def test_const_char_0(self):
        self.assertEqual(ord('a'), ts.const_char_0('a'))

    def test_const_char_0_must_be_char(self):
        with self.assertRaises(ValueError):
            ts.const_char_0(3.14)

    def test_const_char_0_cant_be_string(self):
        with self.assertRaises(ValueError):
            ts.const_char_0("abcd")

    def test_const_char_0_cant_be_NULL(self):
        with self.assertRaises(ValueError):
            ts.const_char_0(None)


class test_single_strings_output(unittest.TestCase):

    def test_inout_string(self):
        # %apply (int DIM1, char INOUT_STRING[ANY]) {(int dim, char result[10])};
        # Has a buffer that's a minimum size of 10, but we grow it if necessary for the
        # argument.  We return the size of the buffer
        self.assertEqual("10", ts.inout_string("abcd"))
        self.assertEqual("101", ts.inout_string("a" * 100))

    def test_inout_string_bad_argument(self):
        with self.assertRaises(ValueError):
            ts.inout_string(5.8)

    def test_out_string(self):
        # %apply (char OUT_STRING[ANY]) {(char result[10])};
        # A fixed size buffer.  We return a string representing the value passed
        self.assertEqual("23", ts.out_string(23))


class test_multiple_strings_input(unittest.TestCase):
    # %apply (char *IN_STRINGS, int DIM1, int DIM2) {(const char *strings, int dim1, int dim2)};
    # The string arguments are packed into an N (count) by M (longest length + 1) buffer.
    # This program recreats the original strings and also returns the value of M.
    def test_in_strings(self):
        args = ("abcdefg", "a * 100", "", "xyz" * 35)
        result = ts.in_strings(args)
        self.assertEqual(args, result[:-1])
        self.assertEqual((len(args), 1 + max(len(x) for x in args)), result[-1])

    def test_in_strings_bad_must_strings(self):
        with self.assertRaises(ValueError):
            ts.in_strings(("abc", 27))

    def test_in_strings_bad_must_be_strings_2(self):
        with self.assertRaises(ValueError):
            ts.in_strings(np.array((1, 2, 3)))

    def test_in_strings_cant_be_None(self):
        with self.assertRaises(TypeError):
            ts.in_strings(None)

    def test_in_strings_cant_contain_None(self):
        with self.assertRaises(ValueError):
            ts.in_strings(("abc", None, "DEF"))


class test_multiple_strings_output(unittest.TestCase):
    # %apply (int DIM1, int DIM2, int *NSTRINGS, SpiceChar OUT_STRINGS[ANY][ANY])
    #          {(int dim1, int dim2, int *size, char buffer[50][256])};
    # We are given a 50x256 buffer.  This program returns "count" strings as
    #   "a", "bb", "ccc", "dddd", et.
    def test_out_strings(self):
        result = ts.out_strings(10)
        (dim1, dim2), [strings] = result
        self.assertEqual((50, 256), (dim1, dim2))  # This is part of the declaration
        self.assertEqual(10, len(strings))
        self.assertEqual("a", strings[0])
        self.assertEqual("j" * 10, strings[9])


class test_multiple_strings_inout(unittest.TestCase):
    # %apply(int DIM1, int DIM2, Type *INOUT_STRINGS)
    # because we could, we wrote a simple sorting program
    def test_basic_test_tuple(self):
        argument = "Four score and thirty years ago".split(' ')
        result, = ts.sort_strings(argument)
        self.assertEqual(sorted(argument), result)

    def test_okay_to_pass_empty_list(self):
        result, = ts.sort_strings(())
        self.assertEqual([], result)

    def test_requires_one_dimensional_array(self):
        argument = np.array([["a", "b", "c", "d"], ["w", "x", "y", "z"]])
        with self.assertRaises(ValueError):
            ts.sort_strings(argument)

    def test_requires_non_null(self):
        with self.assertRaises(TypeError):
            ts.sort_strings(None)


class test_primitive_return_types(unittest.TestCase):
    def test_return_string(self):
        self.assertEqual("hello", ts.return_string())

    def test_return_boolean(self):
        self.assertTrue(ts.return_boolean(100))
        self.assertFalse(ts.return_boolean(0))

    def test_sigerror(self):
        with self.assertRaises(RuntimeError):
            ts.return_sigerr()

if __name__ == '__main__':
    unittest.main()
