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
    initialize_swig_callback();
%}

%typemap(in, numinputs=0)
    (SWIGTYPE*)
{
     ERROR The argument "$1_type $1_name" in "$symname" didnt match any template!!
}

%{
    PyObject* int_array_to_tuple(SpiceInt *buffer, SpiceInt count) {
        PyObject* result = PyTuple_New(count);
        for (SpiceInt i = 0; i < count;i++) {
            PyTuple_SetItem(result, i, Py_BuildValue("i", buffer[i]));
        }
        return result;
    }

    PyObject* double_array_to_tuple(SpiceDouble *buffer, SpiceInt count) {
        PyObject *result = PyTuple_New(count);
        for (SpiceInt i = 0; i < count;i++) {
            PyTuple_SetItem(result, i, Py_BuildValue("d", buffer[i]));
        }
        return result;
    }
%}


%{
    PyObject* in_array1_1(SpiceInt arg[3]) {
        return int_array_to_tuple(arg, 3);
    }

    PyObject* in_array1_2(SpiceInt *arg, SpiceInt dim) {
        return int_array_to_tuple(arg, dim);
    }

    PyObject* in_array1_3(SpiceInt *arg, SpiceInt dim) {
        return int_array_to_tuple(arg, dim);
    }

    PyObject* in_array01_1(SpiceInt *arg, SpiceInt dim) {
        if (dim == 0) {
            return Py_BuildValue("i", arg[0]);
        }
        return int_array_to_tuple(arg, dim);
    }
%}

%apply (SpiceInt IN_ARRAY1[ANY]) {SpiceInt arg[3]};
PyObject* in_array1_1(SpiceInt arg[3]);

%apply (SpiceInt* IN_ARRAY1, SpiceInt DIM1) {(SpiceInt* arg, SpiceInt dim)};
PyObject* in_array1_2(SpiceInt *arg, SpiceInt dim);

%apply (SpiceInt* IN_ARRAY1) {(SpiceInt arg[])};
PyObject* in_array1_3(SpiceInt arg[], SpiceInt dim);

%apply (SpiceInt *IN_ARRAY01, SpiceInt DIM1) {(SpiceInt *arg, SpiceInt dim)};
PyObject* in_array01_1(SpiceInt *arg, SpiceInt dim);

%{
   PyObject* in_array2_1(SpiceInt arg[3][5]) {
       PyObject* info = int_array_to_tuple((int *)arg, 15);
       return Py_BuildValue("Nii", info, 3, 5);
   }

   PyObject *in_array2_2(SpiceInt *arg, SpiceInt dim1, SpiceInt dim2) {
       PyObject* info = int_array_to_tuple(arg, dim1 * dim2);
       return Py_BuildValue("Nii", info, dim1, dim2);
   }

   PyObject *in_array2_3(SpiceInt arg[][5], SpiceInt dim1) {
       PyObject* info = int_array_to_tuple((int *)arg, dim1 * 5);
       return Py_BuildValue("Nii", info, dim1, 5);
   }

   PyObject *in_array2_4(SpiceInt arg[][5]) {
       /* Nothing we can return, since array might be size 0 */
       Py_RETURN_TRUE;
   }

   PyObject *in_array12(SpiceInt *arg, SpiceInt dim1, SpiceInt dim2) {
       PyObject* info = int_array_to_tuple(arg, max(dim1, 1) * dim2);
       return Py_BuildValue("Nii", info, dim1, dim2);
   }

   PyObject *in_array23(SpiceInt *arg, SpiceInt dim1, SpiceInt dim2, SpiceInt dim3) {
       PyObject* info = int_array_to_tuple(arg, max(dim1, 1) * dim2 * dim3);
       return Py_BuildValue("Niii", info, dim1, dim2, dim3);
   }
%}

%apply (SpiceInt IN_ARRAY2[ANY][ANY]) {SpiceInt arg[3][5]};
PyObject* in_array2_1(SpiceInt arg[3][5]);

%apply (SpiceInt *IN_ARRAY2, SpiceInt DIM1, SpiceInt DIM2) {(SpiceInt *arg, SpiceInt dim1, SpiceInt dim2)};
PyObject *in_array2_2(SpiceInt *arg, SpiceInt dim1, SpiceInt dim2);

%apply (SpiceInt IN_ARRAY2[][ANY], SpiceInt DIM1) {(SpiceInt arg[][5], SpiceInt dim1)};
PyObject *in_array2_3(SpiceInt arg[][5], SpiceInt dim1);

%apply (SpiceInt IN_ARRAY2[][ANY]) {SpiceInt arg[][5]};
PyObject *in_array2_4(SpiceInt arg[][5]);

%apply (SpiceInt *IN_ARRAY12, SpiceInt DIM1, SpiceInt DIM2)  {(SpiceInt *arg, SpiceInt dim1, SpiceInt dim2)};
PyObject *in_array12(SpiceInt *arg, SpiceInt dim1, SpiceInt dim2);

%apply (SpiceInt *IN_ARRAY23, SpiceInt DIM1, SpiceInt DIM2, SpiceInt DIM3)  {(SpiceInt *arg, SpiceInt dim1, SpiceInt dim2, SpiceInt dim3)};
PyObject *in_array23(SpiceInt *arg, SpiceInt dim1, SpiceInt dim2, SpiceInt dim3);

%{
    void out_array1_1(SpiceInt start, SpiceInt array[100]) {
        for (SpiceInt i = 0; i < 100; i++) {
            array[i] = start + i;
        }
    }

    void out_array1_2(SpiceInt start, SpiceInt length, SpiceInt array[100], SpiceInt *size) {
        for (SpiceInt i = 0; i < length; i++) {
            array[i] = start + i;
        }
        *size = length;
    }

    void out_array1_malloc(SpiceInt start, SpiceInt length, SpiceInt **arrayP, SpiceInt *size) {
        if (start >= 0) {
            *arrayP = PyMem_Malloc(length * sizeof(SpiceInt));
            SpiceInt *array = *arrayP;
            for (SpiceInt i = 0; i < length; i++) {
                array[i] = start + i;
            }
        } else {
            *arrayP = NULL;
        }
        *size = length;
    }

    void out_array01_malloc(SpiceDouble start, SpiceInt length, SpiceDouble **arrayP, SpiceInt *size) {
        SpiceInt real_length = max(length, 1);
        *size = length;
        if (start >= 0) {
            *arrayP = PyMem_Malloc(real_length * sizeof(SpiceDouble));
            SpiceDouble *array = *arrayP;
            for (SpiceInt i = 0; i < real_length; i++) {
                array[i] = start + i;
            }
        } else {
            *arrayP = NULL;
        }
    }
%}

%apply (SpiceInt OUT_ARRAY1[ANY]) {(SpiceInt array[100])};
void out_array1_1(SpiceInt start, SpiceInt array[100]);

%apply (SpiceInt OUT_ARRAY1[ANY], SpiceInt *SIZE1) {(SpiceInt array[100], SpiceInt *size)};
void out_array1_2(SpiceInt start, SpiceInt length, SpiceInt array[100], SpiceInt *size);

%apply (SpiceInt **OUT_ARRAY1, SpiceInt *SIZE1) {(SpiceInt **arrayP, SpiceInt *size)};
void out_array1_malloc(SpiceInt start, SpiceInt length, SpiceInt **arrayP, SpiceInt *size);

%apply (SpiceDouble **OUT_ARRAY01, SpiceInt *SIZE1) {(SpiceDouble **arrayP, SpiceInt *size)};
void out_array01_malloc(SpiceDouble start, SpiceInt length, SpiceDouble **arrayP, SpiceInt *size);


%{
    void out_array2_1(SpiceInt start, SpiceInt array[2][3]) {
        SpiceInt* ptr = (SpiceInt *)array;
        for (SpiceInt i = 0; i < 6; i++) {
           ptr[i] = start + i;
        }
    }

    void out_array2_2(SpiceInt start, SpiceInt length, SpiceInt array[1000][2], SpiceInt *size) {
        SpiceInt *ptr = (SpiceInt *)array;
        for (SpiceInt i = 0; i < 2000; i++) {
           ptr[i] = start + i;
        }
        *size = length;
    }

    void out_array2_3(SpiceInt start, SpiceInt length1, SpiceInt length2, SpiceInt **result, SpiceInt *size1, SpiceInt *size2) {
        SpiceInt *ptr = NULL;
        if (start >= 0) {
            ptr = PyMem_Malloc(length1 * length2 * sizeof(SpiceInt));
            for (SpiceInt i = 0; i < length1 * length2; i++) {
                ptr[i] = start + i;
            }
        }
        *result = ptr;
        *size1 = length1;
        *size2 = length2;
    }

    SpiceInt out_array2_4(SpiceInt start, SpiceInt length, SpiceInt dim1, SpiceInt *size1, SpiceDouble result[4][5]) {
        SpiceDouble *ptr = (SpiceDouble *)result;
        for (SpiceInt i = 0; i < 20; i++) {
            ptr[i] = start + i;
        }
        *size1 = length;
        return dim1;
    }

    void out_array2_5(SpiceInt length, SpiceInt *size1, SpiceBoolean result[4][5]) {
        *size1 = length;
        SpiceBoolean *ptr = (SpiceBoolean *)result;
        for (SpiceInt i = 0; i < 20; i++) {
            ptr[i] = (i % 3) == 0;
        }
    }


    void out_array12_1(SpiceInt start, SpiceInt length1, SpiceInt length2, SpiceInt **result, SpiceInt *size1, SpiceInt *size2) {
        SpiceInt *ptr = NULL;
        if (start >= 0) {
            SpiceInt xlength1 = max(length1, 1);
            ptr = PyMem_Malloc(xlength1 * length2 * sizeof(SpiceInt));
            for (SpiceInt i = 0; i < xlength1 * length2; i++) {
                ptr[i] = start + i;
            }
        }
        *result = ptr;
        *size1 = length1;
        *size2 = length2;
    }

    void out_array23_1(SpiceInt start, SpiceInt length1, SpiceInt length2, SpiceInt length3,
                       SpiceDouble **result, SpiceInt *size1, SpiceInt *size2, SpiceInt *size3) {
        SpiceDouble *ptr = NULL;
        if (start >= 0) {
            SpiceInt xlength1 = max(length1, 1);
            ptr = PyMem_Malloc(xlength1 * length2 * length3 * sizeof(SpiceDouble));
            for (SpiceInt i = 0; i < xlength1 * length2; i++) {
                ptr[i] = start + i;
            }
        }
        *result = ptr;
        *size1 = length1;
        *size2 = length2;
        *size3 = length3;
    }
%}

%apply (SpiceInt OUT_ARRAY2[ANY][ANY]) {(SpiceInt array[2][3])};
void out_array2_1(SpiceInt start, SpiceInt array[2][3]);

%apply (SpiceInt OUT_ARRAY2[ANY][ANY], SpiceInt *SIZE1) {(SpiceInt array[1000][2], SpiceInt *size)};
void out_array2_2(SpiceInt start, SpiceInt length, SpiceInt array[1000][2], SpiceInt *size);

%apply (SpiceInt **OUT_ARRAY2, SpiceInt *SIZE1, SpiceInt *SIZE2) {(SpiceInt **result, SpiceInt *size1, SpiceInt *size2)};
void out_array2_3(SpiceInt start, SpiceInt length1, SpiceInt length2, SpiceInt **result, SpiceInt *size1, SpiceInt *size2);

%apply (SpiceInt DIM1, SpiceInt *SIZE1, SpiceDouble OUT_ARRAY2[ANY][ANY]) {(SpiceInt dim1, SpiceInt *size1, SpiceDouble result[4][5])};
SpiceInt out_array2_4(SpiceInt start, SpiceInt length, SpiceInt dim1, SpiceInt *size1, SpiceDouble result[4][5]);

%apply (SpiceInt *SIZE1, SpiceBoolean OUT_ARRAY2[ANY][ANY]) {(SpiceInt *size1, SpiceBoolean result[4][5])}
void out_array2_5(SpiceInt length, SpiceInt *size1, SpiceBoolean result[4][5]);

%apply (SpiceInt **OUT_ARRAY12, SpiceInt *SIZE1, SpiceInt *SIZE2) {(SpiceInt **result, SpiceInt *size1, SpiceInt *size2)};
void out_array12_1(SpiceInt start, SpiceInt length1, SpiceInt length2, SpiceInt **result, SpiceInt *size1, SpiceInt *size2);

%apply (SpiceDouble **OUT_ARRAY23, SpiceInt *SIZE1, SpiceInt *SIZE2, SpiceInt *SIZE3) {(SpiceDouble **result, SpiceInt *size1, SpiceInt *size2, SpiceInt *size3)};
void out_array23_1(SpiceInt start, SpiceInt length1, SpiceInt length2, SpiceInt length3, SpiceDouble **result, SpiceInt *size1, SpiceInt *size2, SpiceInt *size3);



%{
    SpiceInt const_string_0(const SpiceChar *string) {
        return (SpiceInt) strlen(string);
    }

    SpiceInt const_char_0(SpiceChar value) {
        return (SpiceInt)value;
    }

    void inout_string_10(SpiceInt dim, SpiceChar* result) {
        sprintf(result, "%d", dim);
    }

    void inout_string_ptr(SpiceInt dim, SpiceChar* result) {
        sprintf(result, "%d", dim);
    }

    void out_string(SpiceInt value, SpiceChar* result) {
        sprintf(result, "%d", value);
    }
%}

%apply (SpiceChar *CONST_STRING) {(const SpiceChar *string)};
SpiceInt const_string_0(const SpiceChar *string);

%apply (SpiceChar IN_STRING) {(SpiceChar value)};
SpiceInt const_char_0(SpiceChar value);

%apply (SpiceInt DIM1, SpiceChar INOUT_STRING[ANY]) {(SpiceInt dim, SpiceChar result[10])};
void inout_string_10(SpiceInt dim, SpiceChar result[10]);

%apply (SpiceInt DIM1, SpiceChar *INOUT_STRING) {(SpiceInt dim, SpiceChar* result)};
void inout_string_ptr(SpiceInt dim, SpiceChar *result);

%apply (SpiceChar OUT_STRING[ANY]) {(SpiceChar result[10])};
void out_string(SpiceInt value, SpiceChar result[10]);

%{
    PyObject* in_strings(ConstSpiceChar *strings, SpiceInt dim1, SpiceInt dim2) {
        PyObject* result = PyTuple_New(dim1 + 1);
        for (SpiceInt i = 0; i < dim1; i++) {
            PyTuple_SetItem(result, i, Py_BuildValue("s", strings + i * dim2));
        }
        PyTuple_SetItem(result, dim1, Py_BuildValue("ii", dim1, dim2));
        return result;
    }

    PyObject* out_strings(SpiceInt length, SpiceInt dim1, SpiceInt dim2, SpiceInt *size, SpiceChar buffer[][256]) {
        if (dim2 != 256) {
            chkin_c("out_strings");
            setmsg_c("Expected dimension to be 256");
            sigerr_c("SPICE(ARRAYSHAPEMISMATCH)");
            chkout_c("out_strings");
            return 0;
        }
        memset(buffer, 0, dim1 * dim2);
        for (SpiceInt i = 0; i < length; i++) {
            memset(buffer[i], 'a' + i, i + 1);
        }
        *size = length;
        return Py_BuildValue("ii", dim1, dim2);
    }
%}

%apply (ConstSpiceChar *IN_STRINGS, SpiceInt DIM1, SpiceInt DIM2) {(ConstSpiceChar *strings, SpiceInt dim1, SpiceInt dim2)};
PyObject* in_strings(ConstSpiceChar *strings, SpiceInt dim1, SpiceInt dim2);

%apply (SpiceInt DIM1, SpiceInt DIM2, SpiceInt *NSTRINGS, SpiceChar OUT_STRINGS[ANY][ANY]) {(SpiceInt dim1, SpiceInt dim2, SpiceInt *size, SpiceChar buffer[50][256])};
PyObject* out_strings(SpiceInt length, SpiceInt dim1, SpiceInt dim2, SpiceInt *size, SpiceChar buffer[50][256]);

%{
    void double_in_out_array(SpiceInt dim1, SpiceInt *array) {
        for (SpiceInt i = 0; i < dim1; i++) {
            array[i] *= 2;
        }
    }

%}

%apply (SpiceInt DIM1, SpiceInt *INOUT_ARRAY1) {(SpiceInt dim1, SpiceInt *array)}
void double_in_out_array(SpiceInt dim1, SpiceInt *array);

%{
    void sort_strings(SpiceInt rows, SpiceInt columns, SpiceChar* array) {
        int (*comparator)(const void* p, const void* q) = (int (*)(const void *, const void *))strcmp;
        qsort(array, rows, columns, comparator);
    }
%}

%apply (SpiceInt DIM1, SpiceInt DIM2, SpiceChar *INOUT_STRINGS) {(SpiceInt rows, SpiceInt columns, SpiceChar* array)};
void sort_strings(SpiceInt rows, SpiceInt columns, SpiceChar* array);

%{
    const SpiceChar* return_string(void) {
       return "hello";
    }

    SpiceInt return_boolean(SpiceInt value) {
        return value;
    }

    void return_sigerr(void) {
    }

%}

%apply (SpiceChar *RETURN_STRING) {const SpiceChar* return_string};
const SpiceChar* return_string();

%apply (SpiceInt RETURN_BOOLEAN) {SpiceInt return_boolean};
SpiceInt return_boolean(SpiceInt value);

%apply (void RETURN_VOID_SIGERR) {void return_sigerr};
void return_sigerr(void);

%{
    void outvar_set_from_var_int(SpiceInt in, SpiceInt* out) { *out = in; }
    void outvar_set_from_var_double(SpiceDouble in, SpiceDouble* out) { *out = in; }
    void outvar_set_from_var_char(SpiceChar in, SpiceChar *out) { *out = in; }
    void outvar_set_from_var_bool(SpiceInt in, SpiceBoolean *out) { *out = in; }
%}

void outvar_set_from_var_int(SpiceInt INPUT, SpiceInt* OUTPUT);
void outvar_set_from_var_double(SpiceDouble INPUT, SpiceDouble* OUTPUT);
void outvar_set_from_var_char(SpiceChar INPUT, SpiceChar *OUTPUT);
void outvar_set_from_var_bool(SpiceInt INPUT, SpiceBoolean *OUTPUT);

//SpiceDLADescr
%{
    int DLADescr_in(ConstSpiceDLADescr *arg) {
        return arg->isize + arg->dsize + arg->csize;
    }

    void DLADescr_out(SpiceDLADescr *arg) {
        arg->isize = 1;
    }

    int ellipse_in(ConstSpiceEllipse *arg) {
        return arg->center[0];
    }

    void ellipse_out(SpiceEllipse *arg) {
        arg->center[0] = 1;
    }

%}

%apply (ConstSpiceDLADescr* INPUT) {ConstSpiceDLADescr *arg};
int DLADescr_in(ConstSpiceDLADescr *arg);

%apply (SpiceDLADescr* OUTPUT) {SpiceDLADescr *arg};
void DLADescr_out(SpiceDLADescr *arg);

%apply (ConstSpiceEllipse* INPUT) {ConstSpiceEllipse *arg};
int ellipse_in(ConstSpiceEllipse *arg);

%apply (SpiceEllipse* OUTPUT) {SpiceEllipse *arg};
void ellipse_out(SpiceEllipse *arg);

// SpiceCell
%{
    int SpiceCell_in(SpiceCell *arg) {
        int total = 0;
        for (int i = 0; i < size_c(arg); ++i) {
            total += SPICE_CELL_ELEM_I(arg, i);
        }
        return total;
    }

    void SpiceCell_append(SpiceCell *arg, SpiceInt value) {
        appndi_c(value, arg);
    }

    void SpiceCell_out(SpiceCell *arg, SpiceDouble value) {
        appndd_c(value, arg);
    }
%}

%apply (SpiceCellInt* INPUT) {SpiceCell *arg};
int SpiceCell_in(SpiceCell *arg);

%apply (SpiceCellInt* INOUT) {SpiceCell *arg};
void SpiceCell_append(SpiceCell *arg, SpiceInt value);

%apply (SpiceCellDouble* OUTPUT) {SpiceCell *arg};
void SpiceCell_out(SpiceCell *arg, SpiceDouble value);

%{
    const SpiceChar* decode_filename(const char* filename) {
       return filename;
    }
%}

%apply (ConstSpiceChar *CONST_FILENAME) {const char *filename};
%apply (SpiceChar *RETURN_STRING) {const SpiceChar* decode_filename};

const SpiceChar* decode_filename(const char *filename);


