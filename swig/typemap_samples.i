%module typemap_samples

%{
#define SWIG_FILE_WITH_INIT
#include <math.h>
#include <stdio.h>
#include "SpiceUsr.h"
#include "SpiceCel.h"
#include "SpiceOsc.h"
%}

%include "typemaps.i"
%include "numpy.i"
%include "cspyce_typemaps.i"

%fragment("NumPy_Fragments");

%init %{
    import_array(); /* For numpy interface */
    erract_c("SET", 256, "RETURN");
    errdev_c("SET", 256, "NULL");   /* Suppresses default error messages */
    initialize_typemap_globals();
%}

%typemap(in, numinputs=0)
    (SWIGTYPE*)
{
     ERROR The argument "$1_type $1_name" in "$symname" didnt match any template!!
}

%{
    PyObject* int_array_to_tuple(int *buffer, int count) {
        PyObject* result = PyTuple_New(count);
        for (int i = 0; i < count;i++) {
            PyTuple_SetItem(result, i, Py_BuildValue("i", buffer[i]));
        }
        return result;
    }

    PyObject* double_array_to_tuple(double *buffer, int count) {
        PyObject *result = PyTuple_New(count);
        for (int i = 0; i < count;i++) {
            PyTuple_SetItem(result, i, Py_BuildValue("d", buffer[i]));
        }
        return result;
    }
%}


%{
    PyObject* in_array1_1(int arg[3]) {
        return int_array_to_tuple(arg, 3);
    }

    PyObject* in_array1_2(int *arg, int dim) {
        return int_array_to_tuple(arg, dim);
    }

    PyObject* in_array1_3(int *arg, int dim) {
        return int_array_to_tuple(arg, dim);
    }

    PyObject* in_array01_1(int *arg, int dim) {
        if (dim == 0) {
            return Py_BuildValue("i", arg[0]);
        }
        return int_array_to_tuple(arg, dim);
    }
%}

%apply (int IN_ARRAY1[ANY]) {int arg[3]};
PyObject* in_array1_1(int arg[3]);

%apply (int* IN_ARRAY1, int DIM1) {(int* arg, int dim)};
PyObject* in_array1_2(int *arg, int dim);

%apply (int* IN_ARRAY1) {(int arg[])};
PyObject* in_array1_3(int arg[], int dim);

%apply (int *IN_ARRAY01, int DIM1) {(int *arg, int dim)};
PyObject* in_array01_1(int *arg, int dim);

%{
   PyObject* in_array2_1(int arg[3][5]) {
       PyObject* info = int_array_to_tuple(arg, 15);
       return Py_BuildValue("Nii", info, 3, 5);
   }

   PyObject *in_array2_2(int *arg, int dim1, int dim2) {
       PyObject* info = int_array_to_tuple(arg, dim1 * dim2);
       return Py_BuildValue("Nii", info, dim1, dim2);
   }

   PyObject *in_array2_3(int arg[][5], int dim1) {
       PyObject* info = int_array_to_tuple(arg, dim1 * 5);
       return Py_BuildValue("Nii", info, dim1, 5);
   }

   PyObject *in_array2_4(int arg[][5]) {
       /* Nothing we can return, since array might be size 0 */
       Py_RETURN_TRUE;
   }

   PyObject *in_array12(int *arg, int dim1, int dim2) {
       PyObject* info = int_array_to_tuple(arg, max(dim1, 1) * dim2);
       return Py_BuildValue("Nii", info, dim1, dim2);
   }

   PyObject *in_array23(int *arg, int dim1, int dim2, int dim3) {
       PyObject* info = int_array_to_tuple(arg, max(dim1, 1) * dim2 * dim3);
       return Py_BuildValue("Niii", info, dim1, dim2, dim3);
   }
%}

%apply (int IN_ARRAY2[ANY][ANY]) {int arg[3][5]};
PyObject* in_array2_1(int arg[3][5]);

%apply (int *IN_ARRAY2, int DIM1, int DIM2) {(int *arg, int dim1, int dim2)};
PyObject *in_array2_2(int *arg, int dim1, int dim2);

%apply (int IN_ARRAY2[][ANY], int DIM1) {(int arg[][5], int dim1)};
PyObject *in_array2_3(int arg[][5], int dim1);

%apply (int IN_ARRAY2[][ANY]) {int arg[][5]};
PyObject *in_array2_4(int arg[][5]);

%apply (int *IN_ARRAY12, int DIM1, int DIM2)  {(int *arg, int dim1, int dim2)};
PyObject *in_array12(int *arg, int dim1, int dim2);

%apply (int *IN_ARRAY23, int DIM1, int DIM2, int DIM3)  {(int *arg, int dim1, int dim2, int dim3)};
PyObject *in_array23(int *arg, int dim1, int dim2, int dim3);

%{
    void out_array1_1(int start, int array[100]) {
        for (int i = 0; i < 100; i++) {
            array[i] = start + i;
        }
    }

    void out_array1_2(int start, int length, int array[100], int *size) {
        for (int i = 0; i < length; i++) {
            array[i] = start + i;
        }
        *size = length;
    }

    void out_array1_malloc(int start, int length, int **arrayP, int *size) {
        if (start >= 0) {
            *arrayP = PyMem_Malloc(length * sizeof(int));
            int *array = *arrayP;
            for (int i = 0; i < length; i++) {
                array[i] = start + i;
            }
        } else {
            *arrayP = NULL;
        }
        *size = length;
    }

    void out_array01_malloc(double start, int length, double **arrayP, int *size) {
        int real_length = max(length, 1);
        *size = length;
        if (start >= 0) {
            *arrayP = PyMem_Malloc(real_length * sizeof(double));
            double *array = *arrayP;
            for (int i = 0; i < real_length; i++) {
                array[i] = start + i;
            }
        } else {
            *arrayP = NULL;
        }
    }
%}

%apply (int OUT_ARRAY1[ANY]) {(int array[100])};
void out_array1_1(int start, int array[100]);

%apply (int OUT_ARRAY1[ANY], int *SIZE1) {(int array[100], int *size)};
void out_array1_2(int start, int length, int array[100], int *size);

%apply (int **OUT_ARRAY1, int *SIZE1) {(int **arrayP, int *size)};
void out_array1_malloc(int start, int length, int **arrayP, int *size);

%apply (double **OUT_ARRAY01, int *SIZE1) {(double **arrayP, int *size)};
void out_array01_malloc(double start, int length, double **arrayP, int *size);


%{
    void out_array2_1(int start, int array[2][3]) {
        int* ptr = array;
        for (int i = 0; i < 6; i++) {
           ptr[i] = start + i;
        }
    }

    void out_array2_2(int start, int length, int array[1000][2], int *size) {
        int *ptr = array;
        for (int i = 0; i < 2000; i++) {
           ptr[i] = start + i;
        }
        *size = length;
    }

    void out_array2_3(int start, int length1, int length2, int **result, int *size1, int *size2) {
        int *ptr = NULL;
        if (start >= 0) {
            ptr = PyMem_Malloc(length1 * length2 * sizeof(int));
            for (int i = 0; i < length1 * length2; i++) {
                ptr[i] = start + i;
            }
        }
        *result = ptr;
        *size1 = length1;
        *size2 = length2;
    }

    int out_array2_4(int start, int length, int dim1, int *size1, double result[4][5]) {
        double *ptr = result;
        for (int i = 0; i < 20; i++) {
            ptr[i] = start + i;
        }
        *size1 = length;
        return dim1;
    }

    void out_array2_5(int length, int *size1, SpiceBoolean result[4][5]) {
        *size1 = length;
        SpiceBoolean *ptr = result;
        for (int i = 0; i < 20; i++) {
            ptr[i] = (i % 3) == 0;
        }
    }


    void out_array12_1(int start, int length1, int length2, int **result, int *size1, int *size2) {
        int *ptr = NULL;
        if (start >= 0) {
            int xlength1 = max(length1, 1);
            ptr = PyMem_Malloc(xlength1 * length2 * sizeof(int));
            for (int i = 0; i < xlength1 * length2; i++) {
                ptr[i] = start + i;
            }
        }
        *result = ptr;
        *size1 = length1;
        *size2 = length2;
    }

    void out_array23_1(int start, int length1, int length2, int length3,
                       double **result, int *size1, int *size2, int *size3) {
        double *ptr = NULL;
        if (start >= 0) {
            int xlength1 = max(length1, 1);
            ptr = PyMem_Malloc(xlength1 * length2 * length3 * sizeof(double));
            for (int i = 0; i < xlength1 * length2; i++) {
                ptr[i] = start + i;
            }
        }
        *result = ptr;
        *size1 = length1;
        *size2 = length2;
        *size3 = length3;
    }
%}

%apply (int OUT_ARRAY2[ANY][ANY]) {(int array[2][3])};
void out_array2_1(int start, int array[2][3]);

%apply (int OUT_ARRAY2[ANY][ANY], int *SIZE1) {(int array[1000][2], int *size)};
void out_array2_2(int start, int length, int array[1000][2], int *size);

%apply (int **OUT_ARRAY2, int *SIZE1, int *SIZE2) {(int **result, int *size1, int *size2)};
void out_array2_3(int start, int length1, int length2, int **result, int *size1, int *size2);

%apply (int DIM1, int *SIZE1, double OUT_ARRAY2[ANY][ANY]) {(int dim1, int *size1, double result[4][5])};
int out_array2_4(int start, int length, int dim1, int *size1, double result[4][5]);

%apply (int *SIZE1, SpiceBoolean OUT_ARRAY2[ANY][ANY]) {(int *size1, SpiceBoolean result[4][5])}
void out_array2_5(int length, int *size1, SpiceBoolean result[4][5]);

%apply (int **OUT_ARRAY12, int *SIZE1, int *SIZE2) {(int **result, int *size1, int *size2)};
void out_array12_1(int start, int length1, int length2, int **result, int *size1, int *size2);

%apply (double **OUT_ARRAY23, int *SIZE1, int *SIZE2, int *SIZE3) {(double **result, int *size1, int *size2, int *size3)};
void out_array23_1(int start, int length1, int length2, int length3, double **result, int *size1, int *size2, int *size3);



%{
    int const_string_0(const char *string) {
        return (int) strlen(string);
    }

    int const_char_0(char value) {
        return (int)value;
    }

    void inout_string_10(int dim, char* result) {
        sprintf(result, "%d", dim);
    }

    void inout_string_ptr(int dim, char* result) {
        sprintf(result, "%d", dim);
    }

    void out_string(int value, char* result) {
        sprintf(result, "%d", value);
    }
%}

%apply (char *CONST_STRING) {(const char *string)};
int const_string_0(const char *string);

%apply (char IN_STRING) {(char value)};
int const_char_0(char value);

%apply (int DIM1, char INOUT_STRING[ANY]) {(int dim, char result[10])};
void inout_string_10(int dim, char result[10]);

%apply (int DIM1, char *INOUT_STRING) {(int dim, char* result)};
void inout_string_ptr(int dim, char *result);

%apply (char OUT_STRING[ANY]) {(char result[10])};
void out_string(int value, char result[10]);

%{
    PyObject* in_strings(const char *strings, int dim1, int dim2) {
        PyObject* result = PyTuple_New(dim1 + 1);
        for (int i = 0; i < dim1; i++) {
            PyTuple_SetItem(result, i, Py_BuildValue("s", strings + i * dim2));
        }
        PyTuple_SetItem(result, dim1, Py_BuildValue("ii", dim1, dim2));
        return result;
    }

    PyObject* out_strings(int length, int dim1, int dim2, int *size, char* buffer) {
        for (int i = 0; i < length; i++) {
            char* ptr = buffer + i * dim2;
            memset(ptr, 0, dim1);
            memset(ptr, 'a' + i, i + 1);
        }
        *size = length;
        return Py_BuildValue("ii", dim1, dim2);
    }
%}

%apply (char *IN_STRINGS, int DIM1, int DIM2) {(const char *strings, int dim1, int dim2)};
PyObject* in_strings(const char *strings, int dim1, int dim2);

%apply (int DIM1, int DIM2, int *NSTRINGS, SpiceChar OUT_STRINGS[ANY][ANY]) {(int dim1, int dim2, int *size, char buffer[50][256])};
PyObject* out_strings(int length, int dim1, int dim2, int *size, char buffer[50][256]);

%{
    void double_in_out_array(int dim1, int *array) {
        for (int i = 0; i < dim1; i++) {
            array[i] *= 2;
        }
    }

%}

%apply (int DIM1, int *INOUT_ARRAY1) {(int dim1, int *array)}
void double_in_out_array(int dim1, int *array);

%{
    void sort_strings(int rows, int columns, char* array) {
        qsort(array, rows, columns, strcmp);
    }
%}

%apply (int DIM1, int DIM2, char *INOUT_STRINGS) {(int rows, int columns, char* array)};
void sort_strings(int rows, int columns, char* array);

%{
    const char* return_string(void) {
       return "hello";
    }

    int return_boolean(int value) {
        return value;
    }

    void return_sigerr(void) {
    }

%}

%apply (char *RETURN_STRING) {const char* return_string};
const char* return_string();

%apply (int RETURN_BOOLEAN) {int return_boolean};
int return_boolean(int value);

%apply (void RETURN_VOID_SIGERR) {void return_sigerr};
void return_sigerr(void);

%{
    void outvar_set_from_var_int(int in, SpiceInt* out) { *out = in; }
    void outvar_set_from_var_float(float in, SpiceFloat* out) { *out = in; }
    void outvar_set_from_var_double(double in, SpiceDouble* out) { *out = in; }
    void outvar_set_from_var_char(char in, SpiceChar *out) { *out = in; }
    void outvar_set_from_var_bool(int in, SpiceBoolean *out) { *out = in; }
%}

void outvar_set_from_var_int(int INPUT, SpiceInt* OUTPUT);
void outvar_set_from_var_float(float INPUT, SpiceFloat* OUTPUT);
void outvar_set_from_var_double(double INPUT, SpiceDouble* OUTPUT);
void outvar_set_from_var_char(char INPUT, SpiceChar *OUTPUT);
void outvar_set_from_var_bool(int INPUT, SpiceBoolean *OUTPUT);

