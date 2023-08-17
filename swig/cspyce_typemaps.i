/* -*- C -*-  (not really, but good for syntax highlighting) */


/*******************************************************************************
* This is a major rewrite of numpy.i to support the CSPICE library
* from JPL. Many bugs have been fixed and new typemaps added, supporting
* character strings, string arrays, and booleans.
*
* See the details in the clearly identified header sections below.
*
* PDS Rings Node, SETI Institute, July 2009.
*
* Modified 1/4/12 (MRS) to handle error messages more consistently.
* Modified 3/21/13 (MRS) to define IN_ARRAY3.
* Modified 12/15/17 (MRS) to define OUT_ARRAY3, IN_ARRAY01, IN_ARRAY12, and
*   IN_ARRAY23, OUT_ARRAY23, OUT_ARRAY12, OUT_ARRAY01. Typemaps now support
*   Spice types explicitly. Spice errors now raise appropriate exceptions, not
*   just RuntimeErrors.
* Modified 2/14/21 (FY) Major rewrite to handle Python3
*******************************************************************************/

%{
#ifndef SWIG_FILE_WITH_INIT
#  define NO_IMPORT_ARRAY
#endif
#include "stdio.h"
#include "stdlib.h"
#include <numpy/arrayobject.h>

#define max(a, b) ((a) > (b) ? (a) : (b))

/*******************************************************************************
*******************************************************************************/

// Global variables
int USE_RUNTIME_ERRORS = 0;  //0 for default exceptions; 1 for RuntimeError only
char SHORT_MESSAGE[ 100] = "";
char LONG_MESSAGE[10000] = "";
char EXPLANATION[ 10000] = "";
char EXCEPTION_MESSAGE[10000] = "";

// flag = 0 uses meaningful exception; flag = 1 uses RuntimeErrors under most
// circumstances.
void set_python_exception_flag(int flag) {
    USE_RUNTIME_ERRORS = flag;
}

int get_python_exception_flag(void) {
    return USE_RUNTIME_ERRORS;
}

char *get_message_after_reset(int option) {
    switch (option) {
        case 0: return SHORT_MESSAGE;
        case 1: return LONG_MESSAGE;
        case 2: return EXPLANATION;
        default: return "";
    }
}

void reset_messages(void) {
    SHORT_MESSAGE[0] = '\0';
    LONG_MESSAGE[0]  = '\0';
    EXPLANATION[0]   = '\0';
}

void flush_traceback(void) {
    // Not currently used, but it may be used in the future.
    // Empty the traceback list
    int depth;
    trcdep_c(&depth);
    for (int k = depth-1; k >= 0; k--) {
        char module[100];
        trcnam_c(k, 100, module);
        chkout_c(module);
    }
}

typedef enum {
    IOError = 0,
    MemoryError = 1,
    TypeError = 2,
    KeyError = 3,
    IndexError = 4,
    ZeroDivisionError = 5,
    RuntimeError = 6,
    ValueError = 7,
    Exception_COUNT = 8,
} Exception;

// A table to convert from error codes to the corresponding Python exception
// objects.  Unfortunately, this table has to be built at start.

PyObject* errcode_to_PyErrorType[Exception_COUNT];

struct ExceptionTableEntry{
    const char* message;
    Exception exception;
};

static struct ExceptionTableEntry all_exception_table_entries[] = {
     {"SPICE(ARRAYSHAPEMISMATCH)",   ValueError},
     {"SPICE(ARRAYTOOSMALL)",        MemoryError},
     {"SPICE(BADACTION)",            ValueError},
     {"SPICE(BADARCHTYPE)",          IOError},
     {"SPICE(BADARRAYSIZE)",         MemoryError},
     {"SPICE(BADATTRIBUTES)",        IOError},
     {"SPICE(BADAXISLENGTH)",        ValueError},
     {"SPICE(BADAXISNUMBERS)",       ValueError},
     {"SPICE(BADBORESIGHTSPEC)",     ValueError},
     {"SPICE(BADBOUNDARY)",          ValueError},
     {"SPICE(BADCOARSEVOXSCALE)",    ValueError},
     {"SPICE(BADCOMMENTAREA)",       IOError},
     {"SPICE(BADCOORDSYSTEM)",       IOError},
     {"SPICE(BADDASCOMMENTAREA)",    IOError},
     {"SPICE(BADDEFAULTVALUE)",      ValueError},
     {"SPICE(BADDESCRTIMES)",        ValueError},
     {"SPICE(BADDIRECTION)",         ValueError},
     {"SPICE(BADECCENTRICITY)",      ValueError},
     {"SPICE(BADENDPOINTS)",         ValueError},
     {"SPICE(BADFILETYPE)",          IOError},
     {"SPICE(BADFINEVOXELSCALE)",    ValueError},
     {"SPICE(BADFRAME)",             ValueError},
     {"SPICE(BADFRAMECLASS)",        ValueError},
     {"SPICE(BADGM)",                ValueError},
     {"SPICE(BADINDEX)",             ValueError},
     {"SPICE(BADINITSTATE)",         RuntimeError},
     {"SPICE(BADLATUSRECTUM)",       ValueError},
     {"SPICE(BADLIMBLOCUSMIX)",      ValueError},
     {"SPICE(BADPARTNUMBER)",        ValueError},
     {"SPICE(BADPERIAPSEVALUE)",     ValueError},
     {"SPICE(BADPLATECOUNT)",        ValueError},
     {"SPICE(BADRADIUS)",            ValueError},
     {"SPICE(BADRADIUSCOUNT)",       ValueError},
     {"SPICE(BADREFVECTORSPEC)",     ValueError},
     {"SPICE(BADSEMIAXIS)",          ValueError},
     {"SPICE(BADSTOPTIME)",          ValueError},
     {"SPICE(BADTIMEITEM)",          ValueError},
     {"SPICE(BADTIMESTRING)",        ValueError},
     {"SPICE(BADTIMETYPE)",          ValueError},
     {"SPICE(BADVARIABLESIZE)",      ValueError},
     {"SPICE(BADVARIABLETYPE)",      TypeError},
     {"SPICE(BADVARNAME)",           IOError},
     {"SPICE(BADVECTOR)",            ValueError},
     {"SPICE(BADVERTEXCOUNT)",       ValueError},
     {"SPICE(BADVERTEXINDEX)",       IndexError},
     {"SPICE(BARYCENTEREPHEM)",      ValueError},
     {"SPICE(BLANKFILENAME)",        IOError},
     {"SPICE(BLANKMODULENAME)",      ValueError},
     {"SPICE(BODIESNOTDISTINCT)",    ValueError},
     {"SPICE(BODYANDCENTERSAME)",    ValueError},
     {"SPICE(BODYIDNOTFOUND)",       KeyError},
     {"SPICE(BODYNAMENOTFOUND)",     KeyError},
     {"SPICE(BORESIGHTMISSING)",     ValueError},
     {"SPICE(BOUNDARYMISSING)",      ValueError},
     {"SPICE(BOUNDARYTOOBIG)",       MemoryError},
     {"SPICE(BOUNDSOUTOFORDER)",     ValueError},
     {"SPICE(BUFFEROVERFLOW)",       MemoryError},
     {"SPICE(BUG)",                  RuntimeError},
     {"SPICE(CANTFINDFRAME)",        KeyError},
     {"SPICE(CELLTOOSMALL)",         MemoryError},
     {"SPICE(CKINSUFFDATA)",         IOError},
     {"SPICE(CKTOOMANYFILES)",       MemoryError},
     {"SPICE(COLUMNTOOSMALL)",       MemoryError},
     {"SPICE(COMMENTTOOLONG)",       MemoryError},
     {"SPICE(COORDSYSNOTREC)",       ValueError},
     {"SPICE(COVERAGEGAP)",          IOError},
     {"SPICE(CROSSANGLEMISSING)",    ValueError},
     {"SPICE(DAFBEGGTEND)",          IOError},
     {"SPICE(DAFFRNOTFOUND)",        IOError},
     {"SPICE(DAFFTFULL)",            MemoryError},
     {"SPICE(DAFIMPROPOPEN)",        IOError},
     {"SPICE(DAFNEGADDR)",           IOError},
     {"SPICE(DAFNOSEARCH)",          IOError},
     {"SPICE(DAFOPENFAIL)",          IOError},
     {"SPICE(DAFRWCONFLICT)",        IOError},
     {"SPICE(DASFILEREADFAILED)",    IOError},
     {"SPICE(DASFTFULL)",            MemoryError},
     {"SPICE(DASIMPROPOPEN)",        IOError},
     {"SPICE(DASNOSUCHHANDLE)",      IOError},
     {"SPICE(DASOPENCONFLICT)",      IOError},
     {"SPICE(DASOPENFAIL)",          IOError},
     {"SPICE(DASRWCONFLICT)",        IOError},
     {"SPICE(DEGENERATECASE)",       ValueError},
     {"SPICE(DEGENERATEINTERVAL)",   ValueError},
     {"SPICE(DEGENERATESURFACE)",    ValueError},
     {"SPICE(DEPENDENTVECTORS)",     ValueError},
     {"SPICE(DEVICENAMETOOLONG)",    MemoryError},
     {"SPICE(DIVIDEBYZERO)",         ZeroDivisionError},
     {"SPICE(DSKTARGETMISMATCH)",    ValueError},
     {"SPICE(DTOUTOFRANGE)",         ValueError},
     {"SPICE(DUBIOUSMETHOD)",        ValueError},
     {"SPICE(ECCOUTOFRANGE)",        ValueError},
     {"SPICE(EKCOLATTRTABLEFULL)",   MemoryError},
     {"SPICE(EKCOLDESCTABLEFULL)",   MemoryError},
     {"SPICE(EKFILETABLEFULL)",      MemoryError},
     {"SPICE(EKIDTABLEFULL)",        MemoryError},
     {"SPICE(EKNOSEGMENTS)",         IOError},
     {"SPICE(EKSEGMENTTABLEFULL)",   MemoryError},
     {"SPICE(ELEMENTSTOOSHORT)",     ValueError},
     {"SPICE(EMPTYSEGMENT)",         ValueError},
     {"SPICE(EMPTYSTRING)",          ValueError},
     {"SPICE(FILECURRENTLYOPEN)",    IOError},
     {"SPICE(FILEDOESNOTEXIST)",     IOError},
     {"SPICE(FILEISNOTSPK)",         IOError},
     {"SPICE(FILENOTFOUND)",         IOError},
     {"SPICE(FILEOPENFAILED)",       IOError},
     {"SPICE(FILEREADFAILED)",       IOError},
     {"SPICE(FRAMEIDNOTFOUND)",      KeyError},
     {"SPICE(FRAMEMISSING)",         ValueError},
     {"SPICE(FRAMENAMENOTFOUND)",    KeyError},
     {"SPICE(GRIDTOOLARGE)",         MemoryError},
     {"SPICE(IDCODENOTFOUND)",       KeyError},
     {"SPICE(ILLEGALCHARACTER)",     ValueError},
     {"SPICE(IMMUTABLEVALUE)",       RuntimeError},
     {"SPICE(INCOMPATIBLESCALE)",    ValueError},
     {"SPICE(INCOMPATIBLEUNITS)",    ValueError},
     {"SPICE(INDEXOUTOFRANGE)",      IndexError},
     {"SPICE(INPUTOUTOFRANGE)",      ValueError},
     {"SPICE(INPUTSTOOLARGE)",       ValueError},
     {"SPICE(INQUIREERROR)",         IOError},
     {"SPICE(INQUIREFAILED)",        IOError},
     {"SPICE(INSUFFICIENTANGLES)",   ValueError},
     {"SPICE(INSUFFLEN)",            MemoryError},
     {"SPICE(INTINDEXTOOSMALL)",     ValueError},
     {"SPICE(INTLENNOTPOS)",         ValueError},
     {"SPICE(INTOUTOFRANGE)",        ValueError},
     {"SPICE(INVALDINDEX)",          IndexError},
     {"SPICE(INVALIDACTION)",        ValueError},
     {"SPICE(INVALIDARCHTYPE)",      IOError},
     {"SPICE(INVALIDARGUMENT)",      ValueError},
     {"SPICE(INVALIDARRAYRANK)",     ValueError},
     {"SPICE(INVALIDARRAYSHAPE)",    ValueError},
     {"SPICE(INVALIDARRAYTYPE)",     ValueError},
     {"SPICE(INVALIDAXISLENGTH)",    ValueError},
     {"SPICE(INVALIDCARDINALITY)",   ValueError},
     {"SPICE(INVALIDCOUNT)",         ValueError},
     {"SPICE(INVALIDDEGREE)",        ValueError},
     {"SPICE(INVALIDDESCRTIME)",     ValueError},
     {"SPICE(INVALIDDIMENSION)",     ValueError},
     {"SPICE(INVALIDELLIPSE)",       ValueError},
     {"SPICE(INVALIDENDPNTSPEC)",    ValueError},
     {"SPICE(INVALIDEPOCH)",         ValueError},
     {"SPICE(INVALIDFORMAT)",        ValueError},
     {"SPICE(INVALIDFRAME)",         ValueError},
     {"SPICE(INVALIDFRAMEDEF)",      ValueError},
     {"SPICE(INVALIDINDEX)",         IndexError},
     {"SPICE(INVALIDLIMBTYPE)",      ValueError},
     {"SPICE(INVALIDLISTITEM)",      ValueError},
     {"SPICE(INVALIDLOCUS)",         ValueError},
     {"SPICE(INVALIDLONEXTENT)",     ValueError},
     {"SPICE(INVALIDMETHOD)",        ValueError},
     {"SPICE(INVALIDMSGTYPE)",       ValueError},
     {"SPICE(INVALIDNUMINTS)",       ValueError},
     {"SPICE(INVALIDNUMRECS)",       ValueError},
     {"SPICE(INVALIDOCCTYPE)",       ValueError},
     {"SPICE(INVALIDOPERATION)",     ValueError},
     {"SPICE(INVALIDOPTION)",        ValueError},
     {"SPICE(INVALIDPLANE)",         ValueError},
     {"SPICE(INVALIDPOINT)",         ValueError},
     {"SPICE(INVALIDRADIUS)",        ValueError},
     {"SPICE(INVALIDREFFRAME)",      ValueError},
     {"SPICE(INVALIDROLLSTEP)",      ValueError},
     {"SPICE(INVALIDSCLKSTRING)",    ValueError},
     {"SPICE(INVALIDSCLKTIME)",      ValueError},
     {"SPICE(INVALIDSEARCHSTEP)",    ValueError},
     {"SPICE(INVALIDSIGNAL)",        RuntimeError},
     {"SPICE(INVALIDSIZE)",          ValueError},
     {"SPICE(INVALIDSTARTTIME)",     ValueError},
     {"SPICE(INVALIDSTATE)",         ValueError},
     {"SPICE(INVALIDSTEP)",          ValueError},
     {"SPICE(INVALIDSTEPSIZE)",      ValueError},
     {"SPICE(INVALIDSUBTYPE)",       ValueError},
     {"SPICE(INVALIDTARGET)",        ValueError},
     {"SPICE(INVALIDTERMTYPE)",      ValueError},
     {"SPICE(INVALIDTIMEFORMAT)",    ValueError},
     {"SPICE(INVALIDTIMESTRING)",    ValueError},
     {"SPICE(INVALIDTOL)",           ValueError},
     {"SPICE(INVALIDTOLERANCE)",     ValueError},
     {"SPICE(INVALIDTYPE)",          TypeError},
     {"SPICE(INVALIDVALUE)",         ValueError},
     {"SPICE(INVALIDVERTEX)",        ValueError},
     {"SPICE(KERNELPOOLFULL)",       MemoryError},
     {"SPICE(KERNELVARNOTFOUND)",    KeyError},
     {"SPICE(MALLOCFAILED)",         MemoryError},
     {"SPICE(MALLOCFAILURE)",        MemoryError},
     {"SPICE(MEMALLOCFAILED)",       MemoryError},
     {"SPICE(MESSAGETOOLONG)",       MemoryError},
     {"SPICE(MISSINGDATA)",          ValueError},
     {"SPICE(MISSINGTIMEINFO)",      ValueError},
     {"SPICE(MISSINGVALUE)",         ValueError},
     {"SPICE(NAMESDONOTMATCH)",      ValueError},
     {"SPICE(NOCLASS)",              ValueError},
     {"SPICE(NOCOLUMN)",             ValueError},
     {"SPICE(NOCURRENTARRAY)",       IOError},
     {"SPICE(NOFRAME)",              ValueError},
     {"SPICE(NOFRAMEINFO)",          ValueError},
     {"SPICE(NOINTERCEPT)",          ValueError},
     {"SPICE(NOINTERVAL)",           ValueError},
     {"SPICE(NOLOADEDFILES)",        IOError},
     {"SPICE(NOMOREROOM)",           MemoryError},
     {"SPICE(NONCONICMOTION)",       ValueError},
     {"SPICE(NONCONTIGUOUSARRAY)",   ValueError},
     {"SPICE(NONPOSITIVEMASS)",      ValueError},
     {"SPICE(NONPOSITIVESCALE)",     ValueError},
     {"SPICE(NONPRINTABLECHARS)",    ValueError},
     {"SPICE(NOPARTITION)",          ValueError},
     {"SPICE(NOPATHVALUE)",          ValueError},
     {"SPICE(NOPRIORITIZATION)",     ValueError},
     {"SPICE(NOSEGMENTSFOUND)",      IOError},
     {"SPICE(NOSEPARATION)",         ValueError},
     {"SPICE(NOSUCHFILE)",           IOError},
     {"SPICE(NOTADAFFILE)",          IOError},
     {"SPICE(NOTADASFILE)",          IOError},
     {"SPICE(NOTADPNUMBER)",         ValueError},
     {"SPICE(NOTANINTEGER)",         ValueError},
     {"SPICE(NOTAROTATION)",         ValueError},
     {"SPICE(NOTASET)",              TypeError},
     {"SPICE(NOTINITIALIZED)",       RuntimeError},
     {"SPICE(NOTINPART)",            ValueError},
     {"SPICE(NOTPRINTABLECHARS)",    ValueError},
     {"SPICE(NOTRANSLATION)",        KeyError},
     {"SPICE(NOTRECOGNIZED)",        ValueError},
     {"SPICE(NOTSUPPORTED)",         ValueError},
     {"SPICE(NULLPOINTER)",          ValueError},
     {"SPICE(NUMCOEFFSNOTPOS)",      ValueError},
     {"SPICE(NUMERICOVERFLOW)",      ValueError},
     {"SPICE(NUMPARTSUNEQUAL)",      ValueError},
     {"SPICE(NUMSTATESNOTPOS)",      ValueError},
     {"SPICE(OUTOFROOM)",            MemoryError},
     {"SPICE(PCKFILETABLEFULL)",     MemoryError},
     {"SPICE(PLATELISTTOOSMALL)",    ValueError},
     {"SPICE(POINTNOTONSURFACE)",    ValueError},
     {"SPICE(POINTONZAXIS)",         ValueError},
     {"SPICE(PTRARRAYTOOSMALL)",     ValueError},
     {"SPICE(RECURSIVELOADING)",     IOError},
     {"SPICE(REFANGLEMISSING)",      ValueError},
     {"SPICE(REFVECTORMISSING)",     ValueError},
     {"SPICE(SCLKTRUNCATED)",        ValueError},
     {"SPICE(SEGIDTOOLONG)",         ValueError},
     {"SPICE(SETEXCESS)",            MemoryError},
     {"SPICE(SHAPEMISSING)",         ValueError},
     {"SPICE(SHAPENOTSUPPORTED)",    ValueError},
     {"SPICE(SIGNALFAILED)",         RuntimeError},
     {"SPICE(SIGNALFAILURE)",        RuntimeError},
     {"SPICE(SINGULARMATRIX)",       ValueError},
     {"SPICE(SPKFILETABLEFULL)",     MemoryError},
     {"SPICE(SPKINSUFFDATA)",        IOError},
     {"SPICE(SPKINVALIDOPTION)",     IOError},
     {"SPICE(SPKNOTASUBSET)",        IOError},
     {"SPICE(SPKTYPENOTSUPP)",       IOError},
     {"SPICE(STRINGTOOLSHORT)",      ValueError},
     {"SPICE(STRINGTOOSHORT)",       ValueError},
     {"SPICE(SUBPOINTNOTFOUND)",     ValueError},
     {"SPICE(TABLENOTLOADED)",       IOError},
     {"SPICE(TARGETMISMATCH)",       ValueError},
     {"SPICE(TIMECONFLICT)",         ValueError},
     {"SPICE(TIMESDONTMATCH)",       ValueError},
     {"SPICE(TIMESOUTOFORDER)",      ValueError},
     {"SPICE(TOOFEWPACKETS)",        ValueError},
     {"SPICE(TOOFEWPLATES)",         ValueError},
     {"SPICE(TOOFEWSTATES)",         ValueError},
     {"SPICE(TOOFEWVERTICES)",       ValueError},
     {"SPICE(TOOMANYFILESOPEN)",     IOError},
     {"SPICE(TOOMANYPARTS)",         ValueError},
     {"SPICE(TRACEBACKOVERFLOW)",    MemoryError},
     {"SPICE(TRACESTACKEMPTY)",      RuntimeError},
     {"SPICE(TYPEMISMATCH)",         TypeError},
     {"SPICE(UNDEFINEDFRAME)",       ValueError},
     {"SPICE(UNITSMISSING)",         ValueError},
     {"SPICE(UNITSNOTREC)",          ValueError},
     {"SPICE(UNKNOWNCOMPARE)",       ValueError},
     {"SPICE(UNKNOWNFRAME)",         KeyError},
     {"SPICE(UNKNOWNSPKTYPE)",       IOError},
     {"SPICE(UNKNOWNSYSTEM)",        ValueError},
     {"SPICE(UNMATCHENDPTS)",        ValueError},
     {"SPICE(UNORDEREDTIMES)",       ValueError},
     {"SPICE(UNPARSEDTIME)",         ValueError},
     {"SPICE(UNSUPPORTEDBFF)",       IOError},
     {"SPICE(UNSUPPORTEDSPEC)",      IOError},
     {"SPICE(VALUEOUTOFRANGE)",      ValueError},
     {"SPICE(VARIABLENOTFOUND)",     KeyError},
     {"SPICE(VECTORTOOBIG)",         ValueError},
     {"SPICE(WINDOWEXCESS)",         MemoryError},
     {"SPICE(WINDOWTOOSMALL)",       ValueError},
     {"SPICE(WORKSPACETOOSMALL)",    MemoryError},
     {"SPICE(WRONGDATATYPE)",        TypeError},
     {"SPICE(YEAROUTOFRANGE)",       ValueError},
     {"SPICE(ZEROBOUNDSEXTENT)",     ValueError},
     {"SPICE(ZEROLENGTHCOLUMN)",     ValueError},
     {"SPICE(ZEROPOSITION)",         ValueError},
     {"SPICE(ZEROQUATERNION)",       ValueError},
     {"SPICE(ZEROVECTOR)",           ValueError},
     {"SPICE(ZEROVELOCITY)",         ValueError},
};

static int exception_compare_function(const void* pkey, const void* pelem) {
    const char* key = pkey;
    const struct ExceptionTableEntry *entry = pelem;
    return strcmp(key, entry->message);
}

Exception select_exception(char *shortmsg) {
    // RuntimeErrors only
    if (USE_RUNTIME_ERRORS) {
        return RuntimeError;
    }
    int element_size = sizeof(all_exception_table_entries[0]);
    int elements = sizeof(all_exception_table_entries) / element_size;
    struct ExceptionTableEntry *result =
        bsearch(shortmsg, all_exception_table_entries, elements, element_size,
        exception_compare_function);
    return result ? result->exception : RuntimeError;
}

char *get_exception_message(const char *name) {
    // Save the messages globally
    getmsg_c("SHORT",     100, SHORT_MESSAGE);
    getmsg_c("LONG",    10000, LONG_MESSAGE );
    getmsg_c("EXPLAIN", 10000, EXPLANATION  );

    // Create the exception message
    getmsg_c("SHORT", 100, EXCEPTION_MESSAGE);
    strcat(EXCEPTION_MESSAGE, " -- ");
    if (name[0]) {
        strcat(EXCEPTION_MESSAGE, name);
        strcat(EXCEPTION_MESSAGE, " -- ");
    }
    strcat(EXCEPTION_MESSAGE, LONG_MESSAGE);

    return EXCEPTION_MESSAGE;
}

void set_python_exception(const char *symname) {
    char *message = get_exception_message(symname);
    Exception errtype = select_exception(SHORT_MESSAGE);
    PyObject* exception = errcode_to_PyErrorType[errtype];
    PyErr_SetString(exception, message);
}

void initialize_typemap_globals(void) {
    errcode_to_PyErrorType[IOError] = PyExc_IOError;
    errcode_to_PyErrorType[MemoryError] = PyExc_MemoryError;
    errcode_to_PyErrorType[TypeError] = PyExc_TypeError;
    errcode_to_PyErrorType[KeyError] = PyExc_KeyError;
    errcode_to_PyErrorType[IndexError] = PyExc_IndexError;
    errcode_to_PyErrorType[ZeroDivisionError] = PyExc_ZeroDivisionError;
    errcode_to_PyErrorType[RuntimeError] = PyExc_RuntimeError;
    errcode_to_PyErrorType[ValueError] = PyExc_ValueError;
}

PyObject* SWIG_CALLBACK_CLASS  = NULL;

void initialize_swig_callback(void) {
    PyObject *record_support = PyImport_ImportModule("cspyce.swig_python_callback");
    SWIG_CALLBACK_CLASS  = PyObject_GetAttrString(record_support, "_SwigPythonCallback");
    Py_XDECREF(record_support);
}
%}

%define TEST_FOR_EXCEPTION
{
    if (failed_c()) {
        handle_swig_exception("$symname");
        SWIG_fail;
    }
}
%enddef

%{
void handle_swig_exception(const char *symname) {
    chkin_c(symname);
    set_python_exception(symname);
    chkout_c(symname);
    reset_c();
}
%}

%define TEST_MALLOC_FAILURE(arg)
{
    if (!(arg)) {
        handle_malloc_failure("$symname");
        SWIG_fail;
    }
}
%enddef

%{
void handle_malloc_failure(const char* symname) {
    chkin_c(symname);
    setmsg_c("Failed to allocate memory");
    sigerr_c("SPICE(MALLOCFAILURE)");
    chkout_c(symname);
    PyErr_SetString(USE_RUNTIME_ERRORS ? PyExc_RuntimeError : PyExc_MemoryError,
                    get_exception_message(symname));
    reset_c();
}
%}

%define TEST_IS_STRING(obj)
{
    if (!PyUnicode_Check(obj)) {
        handle_bad_type_error("$symname", "String");
        SWIG_fail;
    }
}
%enddef

%define RAISE_BAD_TYPE_ON_ERROR(error, typename)
{
    if (!SWIG_IsOK(error)) {
        handle_bad_type_error("$symname", typename);
        SWIG_fail;
    }
}
%enddef

%{
void handle_bad_type_error(const char* symname, const char* typename) {
    chkin_c(symname);
    setmsg_c("Expected #");
    errch_c( "#", typename);
    sigerr_c("SPICE(INVALIDARGUMENT)");
    chkout_c(symname);
    PyErr_SetString(
        USE_RUNTIME_ERRORS ? PyExc_RuntimeError : PyExc_ValueError,
        get_exception_message(symname));
    reset_c();
}
%}


%define TEST_INVALID_ARRAY_SHAPE_1D(pyarr, req0)
{
    if ((pyarr) && (PyArray_DIM(pyarr, 0) != (req0))) {
        handle_invalid_array_shape_1d("$symname", pyarr, req0);
        SWIG_fail;
    }
}
%enddef

%{
void handle_invalid_array_shape_1d(const char *symname, PyArrayObject *pyarr, int required) {
    chkin_c(symname);
    setmsg_c("Invalid array shape (#) in module #; (#) is required");
    errint_c("#", (int) PyArray_DIM(pyarr, 0));
    errch_c( "#", symname);
    errint_c("#", (int) (required));
    sigerr_c("SPICE(INVALIDARRAYSHAPE)");
    chkout_c(symname);

    PyErr_SetString(
        USE_RUNTIME_ERRORS ? PyExc_RuntimeError : PyExc_ValueError,
        get_exception_message(symname));
    reset_c();
}
%}

%define TEST_INVALID_ARRAY_SHAPE_2D(pyarr, req0, req1)
{
    if ((pyarr) && (PyArray_DIM(pyarr, 0) != (req0) || PyArray_DIM(pyarr, 1) != (req1))) {
        handle_invalid_array_shape_2d("$symname", pyarr, req0, req1);
        SWIG_fail;
    }
}
%enddef

%{
void handle_invalid_array_shape_2d(const char *symname, PyArrayObject *pyarr, int req0, int req1) {
    chkin_c(symname);
    setmsg_c("Invalid array shape (#,#) in module #; (#,#) is required");
    errint_c("#", (int) PyArray_DIM(pyarr, 0));
    errint_c("#", (int) PyArray_DIM(pyarr, 1));
    errch_c( "#", symname);
    errint_c("#", req0);
    errint_c("#", req1);
    sigerr_c("SPICE(INVALIDARRAYSHAPE)");
    chkout_c(symname);

    PyErr_SetString(
        USE_RUNTIME_ERRORS ? PyExc_RuntimeError : PyExc_ValueError,
        get_exception_message(symname));
    reset_c();
}
%}

%define TEST_INVALID_ARRAY_SHAPE_x2D(pyarr, req1)
{
    if ((pyarr) && (PyArray_DIM(pyarr, 1) != (req1))) {
        handle_invalid_array_shape_x2d("$symname", pyarr, req1);
        SWIG_fail;
    }
}
%enddef

%{
void handle_invalid_array_shape_x2d(const char *symname, PyArrayObject *pyarr, int req1) {
    chkin_c(symname);
    setmsg_c("Invalid array shape (#,#) in module #; (*,#) is required");
    errint_c("#", (int) PyArray_DIM(pyarr, 0));
    errint_c("#", (int) PyArray_DIM(pyarr, 1));
    errch_c( "#", symname);
    errint_c("#", req1);
    sigerr_c("SPICE(INVALIDARRAYSHAPE)");
    chkout_c(symname);

    PyErr_SetString(
        USE_RUNTIME_ERRORS ? PyExc_RuntimeError : PyExc_ValueError,
        get_exception_message(symname));
    reset_c();
}
%}

%{
PyArrayObject*
get_contiguous_array(int typecode, PyObject *input, int min, int max, int flags) {
    if (typecode == NPY_INT && PyArray_Check(input) && PyArray_ISINTEGER((PyArrayObject *)(input))) {
        // We allow the conversion of all integer types to integer arrays.
        flags |= NPY_ARRAY_FORCECAST;
    }
    return (PyArrayObject *) PyArray_FROMANY(input, typecode, min, max, flags);
}
%}

%define CONVERT_TO_CONTIGUOUS_ARRAY(typecode, input, min, max, result)
{
    result = get_contiguous_array(typecode, input, min, max, NPY_ARRAY_CARRAY_RO);
    if (!result) {
        handle_bad_array_conversion("$symname", typecode, input, min, max);
        SWIG_fail;
    }
}
%enddef
%define CONVERT_TO_CONTIGUOUS_ARRAY_WRITEABLE_COPY(typecode, input, min, max, result)
{
    result = get_contiguous_array(typecode, input, min, max,
    NPY_ARRAY_CARRAY | NPY_ARRAY_ENSURECOPY);
    if (!result) {
        handle_bad_array_conversion("$symname", typecode, input, min, max);
        SWIG_fail;
    }
}
%enddef

// result must be a variable which will be Py_DECREF-ed if an error occurs
%define CONVERT_BUFFER_TO_ARRAY_OF_STRINGS(buffer, rows, columns, result)
    result = PyTuple_New(rows);
    TEST_MALLOC_FAILURE(result);

    // Convert the results to Python strings and add them to the list
    for (int i = 0; i < rows; i++) {
        char *str = &buffer[i * columns];
        size_t length = strlen(str);
        while (length > 0 && str[length - 1] == ' ') {
            length--;
        }
        PyObject *value = PyUnicode_FromStringAndSize(str, length);
        TEST_MALLOC_FAILURE(value)
        PyTuple_SET_ITEM(result, i, value);
    }
%enddef

%{
extern const char* typecode_string(int typecode);

void handle_bad_array_conversion(const char* symname, int typecode, PyObject *input, int min, int max) {
    if (!input || !PyArray_Check(input)) {
        setmsg_c("Array of type \"#\" required in module #; "
                 "input argument could not be converted");
        errch_c("#", typecode_string(typecode));
        errch_c("#", symname);
        sigerr_c("SPICE(INVALIDTYPE)");
    } else if (PyArray_NDIM((PyArrayObject *) input) < min || PyArray_NDIM((PyArrayObject *) input) > max) {
        if (min == max) {
            setmsg_c("Invalid array rank # in module #; # is required");
        } else {
            setmsg_c("Invalid array rank # in module #; # or # is required");
        }
        errint_c("#", (int) PyArray_NDIM((PyArrayObject *) input));
        errch_c( "#", symname);
        errint_c("#", (int) (min));
        if (min != max) {
            errint_c("#", (int) (max));
        }
        sigerr_c("SPICE(INVALID_ARRAY_RANK)");
        PyErr_SetString(
            USE_RUNTIME_ERRORS ? PyExc_RuntimeError : PyExc_ValueError,
            get_exception_message(symname));
        reset_c();
        return;
    } else {
        setmsg_c("Array of type \"#\" required in module #; "
                 "array of type \"#\" could not be converted");
        errch_c("#", typecode_string(typecode));
        errch_c("#", symname);
        errch_c("#", typecode_string(PyArray_TYPE((PyArrayObject *)(input))));
        sigerr_c("SPICE(INVALIDARRAYTYPE)");
    }
    // We don't like the error that's already been set up by the array conversion code
    // so we modify it to be what we want.
    set_python_exception(symname);
    reset_c();
}
%}

// This macro takes $input
%define HANDLE_TYPEMAP_IN_STRINGS(ARG_buffer, ARG_buffer_etype, ARG_count, ARG_maxlen, buffer, list)
{
    ARG_buffer = NULL;
    ARG_count = 0;
    ARG_maxlen = 0;

    list = PySequence_List($input);
    if (!list) {
        handle_bad_sequence_to_list("$symname");
        SWIG_fail;
    }

    // list is guaranteed to be a PyList, and we own it.
    Py_ssize_t count = PyList_Size(list);
    Py_ssize_t maxlen = 2;
    for (int i = 0; i < count; i++) {
        PyObject *obj = PyList_GetItem(list, i);  // Note, we don't own this object
        TEST_IS_STRING(obj);
        obj = PyUnicode_AsUTF8String(obj);   // We own this item
        TEST_MALLOC_FAILURE(obj);
        PyList_SetItem(list, i, obj);        // And SetItem steals the ownership
        maxlen = max(maxlen, PyBytes_Size(obj));
    }
    // Allocate the buffer
    buffer = PyMem_Malloc(count * (maxlen + 1) * sizeof(ARG_buffer_etype));
    TEST_MALLOC_FAILURE(buffer);
    // Copy the strings
    for (int i = 0; i < count; i++) {
        PyObject *obj = PyList_GetItem(list, i);
        // PyBytes_AsString simply grabs a pointer out of the python object.
        strncpy((buffer + i * (maxlen+1)), PyBytes_AsString(obj), maxlen+1);
    }
    ARG_buffer = (ARG_buffer_etype *)buffer;
    ARG_count = (int) count;
    ARG_maxlen = (int)(maxlen + 1);
}
%enddef

%define HANDLE_RESIZE(array, dims)
{
    PyArray_Dims shape = {dims, sizeof(dims) / sizeof(dims[0])};
    PyObject* ok = PyArray_Resize(pyarr$argnum, &shape, 0, NPY_CORDER);
    TEST_MALLOC_FAILURE(ok);
    Py_XDECREF(ok);
}
%enddef

%{
void handle_bad_sequence_to_list(const char *symname) {
    chkin_c(symname);
    setmsg_c("Input argument must be a sequence in module #");
    errch_c( "#", symname);
    sigerr_c("SPICE(INVALIDTYPE)");
    chkout_c(symname);
    PyErr_SetString(
        USE_RUNTIME_ERRORS ? PyExc_RuntimeError : PyExc_TypeError,
        get_exception_message(symname));
    reset_c();
}

void capsule_cleanup(PyObject *capsule) {
    void *memory = PyCapsule_GetPointer(capsule, NULL);
    PyMem_Free(memory);
}

// A wrapper around PyArray_SimpleNewFromData that gives the PyArray ownership
// of the data. The buffer pointed to by *data will be freed when the array is freed.
//
// On success, this function returns the newly created array and set *data to NULL.
// On failure, this function returns False, and *data is unchanged.
//
PyArrayObject* create_array_with_owned_data(int nd, npy_intp const *dims, int typenum, void **data) {
    PyArrayObject* array = (PyArrayObject *) PyArray_SimpleNewFromData(nd, dims, typenum, *data);
    PyObject *capsule = array ? PyCapsule_New(*data, NULL, capsule_cleanup) : NULL;
    // If this is successful, it steals ownership of capsule.
    int result = capsule ? PyArray_SetBaseObject(array, capsule) : -1;
    if (result == 0) {
        // The array owns capsule, and capsule owns the data. The caller is no longer
        // responsible for freeing data.
        *data = NULL;
        return array;
    } else {
        // Something went wrong.  Clear both of these.
        Py_XDECREF(array);
        Py_XDECREF(capsule);
        return NULL;
    }
}

void *get_arraylike_object_data(PyObject *object) {
    // Special field holding information about array-like objects
    PyObject *capsule = PyObject_GetAttrString(object, "__array_struct__");
    // Interface is a malloc'ed structure owned by the capsule.
    PyArrayInterface* interface = PyCapsule_GetPointer(capsule, NULL);
    void *result = interface->data;
    Py_DECREF(capsule);
    return result;
}

#if 0
// The are useful functions for when we need to try and debug the generated code.
// Leaving them out of the build, but they can be added whenever necessary.
void debug_show_array(const char* name, PyArrayObject *array, FILE* file) {
     int typenum = PyArray_TYPE(array);
     int dimensions = PyArray_NDIM(array);
     npy_intp* shape = PyArray_SHAPE(array);
     void* data = PyArray_DATA(array);
     char *typename = typenum == NPY_INT ? "int" : typenum == NPY_DOUBLE ? "double" : "??";

     fprintf(file, "%6s: array=%p data=%p %s", name, array, data, typename);
     if (dimensions == 0) {
         fprintf(file, "[()]\n");
     } else {
         for (int i = 0; i < dimensions; ++i) {
             fprintf(file, "%s%ld", (i == 0 ? "[" : ", "), shape[i]);
         }
         fprintf(file, "]\n");
     }
}

void debug_print_object(PyObject *object, FILE* file) {
    PyObject_Print(object, file, 0);
    fprintf(file, "\n");

}
#endif
%}

// Copy standard typemaps for Spice types
%apply int {SpiceInt, SpiceBoolean, ConstSpiceInt, ConstSpiceBoolean};
%apply char {SpiceChar, ConstSpiceChar}
%apply double {SpiceDouble, ConstSpiceDouble};
%apply float {SpiceFloat, ConstSpiceFloat};

/*******************************************************************************
* 1-D numeric typemaps for input
*
* This family of typemaps allows Python sequences and Numpy 1-D arrays to be
* read as arrays in C functions.
*
* If the size of the array is fixed and can be specified in the SWIG interface:
*       (type IN_ARRAY1[ANY])
*       (type IN_ARRAY1[ANY], SpiceInt DIM1)
*       (SpiceInt DIM1, type IN_ARRAY1[ANY])
* In these cases, an error condition will be raised if the dimension of the
* structure passed from Python does not match that specified in braces within
* the C function call.
*
* If the size of the array is defined by the Python structure:
*       (type *IN_ARRAY1, SpiceInt DIM1)
*       (SpiceInt DIM1, type *IN_ARRAY1)
* In these cases, there is no limit on the number of elements that can be passed
* to the C function. Internal memory is allocated as needed based on the size of
* the array passed from Python.
*
* If a scalar should be shaped into an array of shape (1,):
*       (type *IN_ARRAY01, SpiceInt DIM1)
* If a scalar is given, then DIM1 = 0.
*******************************************************************************/


%define TYPEMAP_IN(Type, Typecode) // Use to fill in numeric types below

/*******************************************************
* (Type IN_ARRAY1[ANY])
*******************************************************/

%typemap(in)
    (Type IN_ARRAY1[ANY])                                       // PATTERN
            (PyArrayObject* pyarr=NULL)
{
//      $1_type $1_name
//      (Type IN_ARRAY1[ANY])
    CONVERT_TO_CONTIGUOUS_ARRAY(Typecode, $input, 1, 1, pyarr)
    TEST_INVALID_ARRAY_SHAPE_1D(pyarr, $1_dim0);

    $1 = ($1_ltype) PyArray_DATA(pyarr);                        // ARRAY
}

/*******************************************************
* (Type IN_ARRAY1[ANY], SpiceInt DIM1)
*******************************************************/

%typemap(in)
    (Type IN_ARRAY1[ANY], SpiceInt DIM1)                        // PATTERN
        (PyArrayObject* pyarr=NULL)
{
//       $1_type $1_name, $2_type $2_name
//       (Type IN_ARRAY1[ANY], SpiceInt DIM1)
//       NOT CURRENTLY USED BY CSPICE

    CONVERT_TO_CONTIGUOUS_ARRAY(Typecode, $input, 1, 1, pyarr)
    TEST_INVALID_ARRAY_SHAPE_1D(pyarr, $1_dim0);

    $1 = ($1_ltype) PyArray_DATA(pyarr);                        // ARRAY
    $2 = (SpiceInt) PyArray_DIM(pyarr, 0);                      // DIM1
}

/*******************************************************
* (SpiceInt DIM1, Type IN_ARRAY1[ANY])
*******************************************************/

%typemap(in)
    (SpiceInt DIM1, Type IN_ARRAY1[ANY])                        // PATTERN
        (PyArrayObject* pyarr=NULL)
{
//       $1_type $1_name, $2_type $2_name
//       (SpiceInt DIM1, Type IN_ARRAY1[ANY])
//       NOT CURRENTLY USED BY CSPICE

    CONVERT_TO_CONTIGUOUS_ARRAY(Typecode, $input, 1, 1, pyarr)
    TEST_INVALID_ARRAY_SHAPE_1D(pyarr, $2_dim0);

    $2 = ($2_ltype) PyArray_DATA(pyarr);                        // ARRAY
    $1 = (SpiceInt) PyArray_DIM(pyarr, 0);                      // DIM1
}

/*******************************************************
* (Type *IN_ARRAY1, SpiceInt DIM1)
*******************************************************/

%typemap(in)
    (Type *IN_ARRAY1, SpiceInt DIM1)                            // PATTERN
        (PyArrayObject* pyarr=NULL),
    (Type IN_ARRAY1[], SpiceInt DIM1)                           // PATTERN
        (PyArrayObject* pyarr=NULL)
{
//       $1_type $1_name, $2_type $2_name
//      (Type *IN_ARRAY1, SpiceInt DIM1)

    CONVERT_TO_CONTIGUOUS_ARRAY(Typecode, $input, 1, 1, pyarr)
    $1 = ($1_ltype) PyArray_DATA(pyarr);                        // ARRAY
    $2 = (SpiceInt) PyArray_DIM(pyarr, 0);                      // DIM1
}

/*******************************************************
* (SpiceInt DIM1, Type *IN_ARRAY1)
*******************************************************/

%typemap(in)
    (SpiceInt DIM1, Type *IN_ARRAY1)                            // PATTERN
        (PyArrayObject* pyarr=NULL),
    (SpiceInt DIM1, Type IN_ARRAY1[])                           // PATTERN
        (PyArrayObject* pyarr=NULL)
{
//       $1_type $1_name, $2_type $2_name
//      (SpiceInt DIM1, Type *IN_ARRAY1)

    CONVERT_TO_CONTIGUOUS_ARRAY(Typecode, $input, 1, 1, pyarr)
    $2 = ($2_ltype) PyArray_DATA(pyarr);                        // ARRAY
    $1 = (SpiceInt) PyArray_DIM(pyarr, 0);                      // DIM1
}

/*******************************************************
* (Type *IN_ARRAY1)
*******************************************************/

%typemap(in)
    (Type *IN_ARRAY1)                                           // PATTERN
        (PyArrayObject* pyarr=NULL),
    (Type IN_ARRAY1[])                                          // PATTERN
        (PyArrayObject* pyarr=NULL)
{
//       $1_type $1_name
//       (Type *IN_ARRAY1), (Type IN_ARRAY1[]

    CONVERT_TO_CONTIGUOUS_ARRAY(Typecode, $input, 1, 1, pyarr)
    $1 = ($1_ltype) PyArray_DATA(pyarr);                        // ARRAY
}

/*******************************************************
* (Type *IN_ARRAY01, SpiceInt DIM1)
*******************************************************/

%typemap(in)
    (Type *IN_ARRAY01, SpiceInt DIM1)                           // PATTERN
        (PyArrayObject* pyarr=NULL)
{
//       $1_type $1_name, $2_type $2_name
//      (Type *IN_ARRAY01, SpiceInt DIM1)

    CONVERT_TO_CONTIGUOUS_ARRAY(Typecode, $input, 0, 1, pyarr)
    $1 = ($1_ltype) PyArray_DATA(pyarr);                        // ARRAY
    if (PyArray_NDIM(pyarr) == 0) {
        $2 = 0;                                                 // DIM1
    } else {
        $2 = (SpiceInt) PyArray_DIM(pyarr, 0);                  // DIM1
    }
}

/*******************************************************
* %typemap(argout)
* %typemap(freearg)
*******************************************************/

%typemap(argout)
    (Type IN_ARRAY1[ANY]),
    (Type IN_ARRAY1[ANY], SpiceInt DIM1),
    (SpiceInt DIM1, Type IN_ARRAY1[ANY]),
    (Type *IN_ARRAY1, SpiceInt DIM1),
    (Type IN_ARRAY1[], SpiceInt DIM1),
    (SpiceInt DIM1, Type *IN_ARRAY1),
    (SpiceInt DIM1, Type IN_ARRAY1[]),
    (Type *IN_ARRAY1),
    (Type IN_ARRAY1[]),
    (Type *IN_ARRAY01, SpiceInt DIM1)
 ""

%typemap(freearg)
    (Type IN_ARRAY1[ANY]),
    (Type IN_ARRAY1[ANY], SpiceInt DIM1),
    (SpiceInt DIM1, Type IN_ARRAY1[ANY]),
    (Type *IN_ARRAY1, SpiceInt DIM1),
    (Type IN_ARRAY1[], SpiceInt DIM1),
    (SpiceInt DIM1, Type *IN_ARRAY1),
    (SpiceInt DIM1, Type IN_ARRAY1[]),
    (Type *IN_ARRAY1),
    (Type IN_ARRAY1[]),
    (Type *IN_ARRAY01, SpiceInt DIM1)
%{
    Py_XDECREF(pyarr$argnum);
%}

/*******************************************************
* Now apply to all data types
*******************************************************/

%enddef

// Define concrete examples of the TYPEMAP_IN1 macros
TYPEMAP_IN(ConstSpiceChar,   NPY_STRING )
TYPEMAP_IN(SpiceInt,         NPY_INT   )
TYPEMAP_IN(ConstSpiceInt,    NPY_INT   )
TYPEMAP_IN(SpiceBoolean,     NPY_INT   )
TYPEMAP_IN(ConstSpiceBoolean,NPY_INT   )
TYPEMAP_IN(SpiceDouble,      NPY_DOUBLE)
TYPEMAP_IN(ConstSpiceDouble, NPY_DOUBLE)

#undef TYPEMAP_IN

/*******************************************************************************
* 2-D numeric typemaps for input
*
* This family of typemaps allows Python 2-D sequences and Numpy 2-D arrays to be
* read as arrays in C functions.
*
* If the size of the array is fixed and can be specified in the SWIG interface:
*       (type IN_ARRAY2[ANY][ANY])
*       (type IN_ARRAY2[ANY][ANY], SpiceInt DIM1, SpiceInt DIM2)
*       (SpiceInt DIM1, SpiceInt DIM2, type IN_ARRAY2[ANY][ANY])
* In these cases, an error condition will be raised if the dimensions of the
* structure passed from Python do not match what was specified in braces within
* the C function call.
*
* If the size of the array is defined by the Python structure:
*       (type *IN_ARRAY2, SpiceInt DIM1, SpiceInt DIM2)
*       (SpiceInt DIM1, SpiceInt DIM2, type *IN_ARRAY2)
* In these cases, there is no limit on the number of elements that can be passed
* to the C function. Internal memory is allocated as needed based on the size of
* the array passed from Python.
*
* NEW variations...
*
* If the size of the last array axis is fixed and can be specified in the
* SWIG interface:
*       (type IN_ARRAY2[ANY][ANY], SpiceInt DIM1)
*       (SpiceInt DIM1, type IN_ARRAY2[ANY][ANY])
* In these cases, an error condition will be raised if the second dimension of
* the structure passed from Python does not match what was specified in braces
* within the C function call. The value of the first dimension is ignored and
* can be set to one.
*
* If the first dimension can be missing:
*       (type *IN_ARRAY12, SpiceInt DIM1, SpiceInt DIM2)
* If it is missing, DIM1 = 0.
*******************************************************************************/

%define TYPEMAP_IN(Type, Typecode) /* Use to fill in numeric types below!

/*******************************************************
* (Type IN_ARRAY2[ANY][ANY])
*******************************************************/

%typemap(in)
    (Type IN_ARRAY2[ANY][ANY])                                  // PATTERN
            (PyArrayObject* pyarr=NULL)
{
//       $1_type $1_name
//      (Type IN_ARRAY2[ANY][ANY])

    CONVERT_TO_CONTIGUOUS_ARRAY(Typecode, $input, 2, 2, pyarr)
    TEST_INVALID_ARRAY_SHAPE_2D(pyarr, $1_dim0, $1_dim1);

    $1 = ($1_ltype) PyArray_DATA(pyarr);                        // ARRAY
}

/*******************************************************
* (Type IN_ARRAY2[ANY][ANY], SpiceInt DIM1, SpiceInt DIM2)
*******************************************************/

%typemap(in)
    (Type IN_ARRAY2[ANY][ANY], SpiceInt DIM1, SpiceInt DIM2)    // PATTERN
        (PyArrayObject* pyarr=NULL)
{
//       $1_type $1_name, $2_type $2_name, $3_type $3_name
//       (Type IN_ARRAY2[ANY][ANY], SpiceInt DIM1, SpiceInt DIM2)
//       NOT CURRENTLY USED BY CSPICE

    CONVERT_TO_CONTIGUOUS_ARRAY(Typecode, $input, 2, 2, pyarr)
    TEST_INVALID_ARRAY_SHAPE_2D(pyarr, $1_dim0, $1_dim1);


    $1 = ($1_ltype) PyArray_DATA(pyarr);                        // ARRAY
    $2 = (SpiceInt) PyArray_DIM(pyarr, 0);                      // DIM1
    $3 = (SpiceInt) PyArray_DIM(pyarr, 1);                      // DIM2
}

/*******************************************************
* (SpiceInt DIM1, SpiceInt DIM2, Type IN_ARRAY2[ANY][ANY])
*******************************************************/

%typemap(in)
    (SpiceInt DIM1, SpiceInt DIM2, Type IN_ARRAY2[ANY][ANY])    // PATTERN
            (PyArrayObject* pyarr=NULL)
{
//       $1_type $1_name, $2_type $2_name, $3_type $3_name
//       (SpiceInt DIM1, SpiceInt DIM2, Type IN_ARRAY2[ANY][ANY])
//       NOT CURRENTLY USED

    CONVERT_TO_CONTIGUOUS_ARRAY(Typecode, $input, 2, 2, pyarr)
    TEST_INVALID_ARRAY_SHAPE_2D(pyarr, $3_dim0, $3_dim1);

    $3 = ($3_ltype) PyArray_DATA(pyarr);		      // ARRAY
    $1 = (SpiceInt) PyArray_DIM(pyarr, 0);		      // DIM1
    $2 = (SpiceInt) PyArray_DIM(pyarr, 1);		      // DIM2
}

/*******************************************************
* (Type *IN_ARRAY2, SpiceInt DIM1, SpiceInt DIM2)
*******************************************************/

%typemap(in)
    (Type *IN_ARRAY2, SpiceInt DIM1, SpiceInt DIM2)             // PATTERN
        (PyArrayObject* pyarr=NULL)
{
//       $1_type $1_name, $2_type $2_name, $3_type $3_name
//      (Type *IN_ARRAY2, SpiceInt DIM1, SpiceInt DIM2)

    CONVERT_TO_CONTIGUOUS_ARRAY(Typecode, $input, 2, 2, pyarr)

    $1 = ($1_ltype) PyArray_DATA(pyarr);		      // ARRAY
    $2 = (SpiceInt) PyArray_DIM(pyarr, 0);		      // DIM1
    $3 = (SpiceInt) PyArray_DIM(pyarr, 1);		      // DIM2
}

/*******************************************************
* (SpiceInt DIM1, SpiceInt DIM2, Type *IN_ARRAY2)
*******************************************************/

%typemap(in)
    (SpiceInt DIM1, SpiceInt DIM2, Type *IN_ARRAY2)             // PATTERN
        (PyArrayObject* pyarr=NULL)
{
//      $1_type $1_name, $2_type $2_name, $3_type $3_name
//      (SpiceInt DIM1, SpiceInt DIM2, Type *IN_ARRAY2)
//  NOT CURRENTLY USED BY CSPICE

    CONVERT_TO_CONTIGUOUS_ARRAY(Typecode, $input, 2, 2, pyarr)

    $3 = ($3_ltype) PyArray_DATA(pyarr);		         // ARRAY
    $1 = (SpiceInt) PyArray_DIM(pyarr, 0);		         // DIM1
    $2 = (SpiceInt) PyArray_DIM(pyarr, 1);		         // DIM2
}

/*******************************************************
* (SpiceInt DIM1, Type IN_ARRAY2[][ANY])
* (SpiceInt DIM1, Type IN_ARRAY2[ANY])
*******************************************************/

%typemap(in)
    (SpiceInt DIM1, Type IN_ARRAY2[][ANY])                       // PATTERN
        (PyArrayObject* pyarr=NULL)
{
//      (SpiceInt DIM1, Type IN_ARRAY2[][ANY])
//      $1_type $1_name, $2_type $2_name
    CONVERT_TO_CONTIGUOUS_ARRAY(Typecode, $input, 2, 2, pyarr)
    TEST_INVALID_ARRAY_SHAPE_x2D(pyarr, $2_dim1);

    $2 = ($2_ltype) PyArray_DATA(pyarr);		         // ARRAY
    $1 = (SpiceInt) PyArray_DIM(pyarr, 0);		         // DIM1
}

/*******************************************************
* (SpiceInt DIM1, Type IN_ARRAY2[][ANY])
* (SpiceInt DIM1, Type IN_ARRAY2[ANY])
*******************************************************/

%typemap(in)
    (Type IN_ARRAY2[][ANY], SpiceInt DIM1)              // PATTERN
        (PyArrayObject* pyarr=NULL)
{
//      $1_type $1_name, $2_type $2_name
//      (Type IN_ARRAY2[][ANY], SpiceInt DIM1)

    CONVERT_TO_CONTIGUOUS_ARRAY(Typecode, $input, 2, 2, pyarr)
    TEST_INVALID_ARRAY_SHAPE_x2D(pyarr, $1_dim1);

    $1 = ($1_ltype) PyArray_DATA(pyarr);                        // ARRAY
    $2 = (SpiceInt) PyArray_DIM(pyarr, 0);                      // DIM1
}

/*******************************************************
* (Type IN_ARRAY2[][ANY])
*******************************************************/

%typemap(in)
    (Type IN_ARRAY2[][ANY])                                     // PATTERN
            (PyArrayObject* pyarr=NULL)
{
//      $1_type $1_name
//      (Type IN_ARRAY2[][ANY])

    CONVERT_TO_CONTIGUOUS_ARRAY(Typecode, $input, 2, 2, pyarr)
    TEST_INVALID_ARRAY_SHAPE_x2D(pyarr, $1_dim1);

    $1 = ($1_ltype) PyArray_DATA(pyarr);                        // ARRAY
}


/*******************************************************
* (Type *IN_ARRAY2)
* (Type IN_ARRAY2[])
*******************************************************/

%typemap(in)
    (Type *IN_ARRAY2)           // PATTERN
        (PyArrayObject* pyarr=NULL),
    (Type IN_ARRAY2[])          // PATTERN
        (PyArrayObject* pyarr=NULL)
{
//      $1_type $1_name
//      (SpiceInt DIM1, SpiceInt DIM2, Type *IN_ARRAY2)

    CONVERT_TO_CONTIGUOUS_ARRAY(Typecode, $input, 2, 2, pyarr)
    $1 = ($1_ltype) PyArray_DATA(pyarr);                        // ARRAY
}


/*******************************************************
* (Type *IN_ARRAY12, SpiceInt DIM1, SpiceInt DIM2)
*******************************************************/

%typemap(in)
    (Type *IN_ARRAY12, SpiceInt DIM1, SpiceInt DIM2)            // PATTERN
        (PyArrayObject* pyarr=NULL)
{
//      $1_type $1_name, $2_type $2_name, $3_type $3_name
//      (Type *IN_ARRAY12, SpiceInt DIM1, SpiceInt DIM2)

    CONVERT_TO_CONTIGUOUS_ARRAY(Typecode, $input, 1, 2, pyarr)

    if (PyArray_NDIM(pyarr) == 1) {
        $1 = ($1_ltype) PyArray_DATA(pyarr);                    // ARRAY
        $2 = 0;                                                 // DIM1
        $3 = (SpiceInt) PyArray_DIM(pyarr, 0);                  // DIM2
    } else {
        $1 = ($1_ltype) PyArray_DATA(pyarr);                    // ARRAY
        $2 = (SpiceInt) PyArray_DIM(pyarr, 0);                  // DIM1
        $3 = (SpiceInt) PyArray_DIM(pyarr, 1);                  // DIM2
    }
}

/*******************************************************
* (Type *IN_ARRAY23, SpiceInt DIM1, SpiceInt DIM2, SpiceInt DIM3)
*******************************************************/

%typemap(in)
    (Type *IN_ARRAY23, SpiceInt DIM1, SpiceInt DIM2, SpiceInt DIM3) // PATTERN
        (PyArrayObject* pyarr=NULL)
{
//      $1_type $1_name, $2_type $2_name, $3_type $3_name, $4_type $4_name
//      (Type *IN_ARRAY23, SpiceInt DIM1, SpiceInt DIM2, SpiceInt DIM3)

    CONVERT_TO_CONTIGUOUS_ARRAY(Typecode, $input, 2, 3, pyarr)

    if (PyArray_NDIM(pyarr) == 2) {
        $1 = ($1_ltype) PyArray_DATA(pyarr);                    // ARRAY
        $2 = 0;                                                 // DIM1
        $3 = (SpiceInt) PyArray_DIM(pyarr, 0);                  // DIM2
        $4 = (SpiceInt) PyArray_DIM(pyarr, 1);                  // DIM3
    } else {
        $1 = ($1_ltype) PyArray_DATA(pyarr);                    // ARRAY
        $2 = (SpiceInt) PyArray_DIM(pyarr, 0);                  // DIM1
        $3 = (SpiceInt) PyArray_DIM(pyarr, 1);                  // DIM2
        $4 = (SpiceInt) PyArray_DIM(pyarr, 2);                  // DIM3
    }
}


/*******************************************************
* %typemap(argout)
* %typemap(freearg)
*******************************************************/

%typemap(argout)
    (Type IN_ARRAY2[ANY][ANY]),
    (Type IN_ARRAY2[ANY][ANY], SpiceInt DIM1, SpiceInt DIM2),
    (SpiceInt DIM1, SpiceInt DIM2, Type IN_ARRAY2[ANY][ANY]),
    (Type *IN_ARRAY2, SpiceInt DIM1, SpiceInt DIM2),
    (SpiceInt DIM1, SpiceInt DIM2, Type *IN_ARRAY2),
    (SpiceInt DIM1, Type IN_ARRAY2[][ANY]),
    (Type IN_ARRAY2[][ANY], SpiceInt DIM1),
    (Type IN_ARRAY2[][ANY]),
    (Type IN_ARRAY2[]),
    (Type *IN_ARRAY2),
    (Type *IN_ARRAY12, SpiceInt DIM1, SpiceInt DIM2),
    (Type *IN_ARRAY23, SpiceInt DIM1, SpiceInt DIM2, SpiceInt DIM3)
""

%typemap(freearg)
    (Type IN_ARRAY2[ANY][ANY]),
    (Type IN_ARRAY2[ANY][ANY], SpiceInt DIM1, SpiceInt DIM2),
    (SpiceInt DIM1, SpiceInt DIM2, Type IN_ARRAY2[ANY][ANY]),
    (Type *IN_ARRAY2, SpiceInt DIM1, SpiceInt DIM2),
    (SpiceInt DIM1, SpiceInt DIM2, Type *IN_ARRAY2),
    (SpiceInt DIM1, Type IN_ARRAY2[][ANY]),
    (Type IN_ARRAY2[][ANY], SpiceInt DIM1),
    (Type IN_ARRAY2[][ANY]),
    (Type IN_ARRAY2[]),
    (Type *IN_ARRAY2),
    (Type *IN_ARRAY12, SpiceInt DIM1, SpiceInt DIM2),
    (Type *IN_ARRAY23, SpiceInt DIM1, SpiceInt DIM2, SpiceInt DIM3)
{
    Py_XDECREF(pyarr$argnum);
}

/*******************************************************
* Now apply to all data types
*******************************************************/

%enddef

// Define concrete examples of the TYPEMAP_IN1 macros
TYPEMAP_IN(SpiceInt,         NPY_INT   )
TYPEMAP_IN(ConstSpiceInt,    NPY_INT   )
TYPEMAP_IN(SpiceBoolean,     NPY_INT   )
TYPEMAP_IN(ConstSpiceBoolean,NPY_INT   )
TYPEMAP_IN(SpiceDouble,      NPY_DOUBLE)
TYPEMAP_IN(ConstSpiceDouble, NPY_DOUBLE)

#undef TYPEMAP_IN


/*******************************************************************************
* 1-D numeric typemaps for output
*
* This family of typemaps allows arrays of numbers in a C to be hidden as inputs
* but to be returned as Numpy arrays inside Python. However, the size (or an
* upper limit) must be specified in advance so that adequate memory can be
* allocated.
*
* If the size of the array can be specified in the SWIG interface:
*       (type OUT_ARRAY1[ANY])
*       (type OUT_ARRAY1[ANY], SpiceInt DIM1)
*       (SpiceInt DIM1, type OUT_ARRAY1[ANY])
*
* If the upper limit on the size of the array can be specified in the SWIG
* interface, but the size returned by C is variable:
*       (type OUT_ARRAY1[ANY], SpiceInt DIM1, SpiceInt *SIZE1)
*       (type OUT_ARRAY1[ANY], SpiceInt *SIZE1, SpiceInt DIM1)
*       (SpiceInt DIM1, SpiceInt *SIZE1, type OUT_ARRAY1[ANY])
*       (SpiceInt *SIZE1, SpiceInt DIM1, type OUT_ARRAY1[ANY])
*
* If the total size of a temporary memory buffer can be specified in advance,
* and the shape of the array then returned afterward.
*       (type OUT_ARRAY1[ANY], SpiceInt *SIZE1)
*       (SpiceInt *SIZE1, type OUT_ARRAY1[ANY])
*
* If the C function will allocate the memory it needs and will return the size:
*       (type **OUT_ARRAY1, SpiceInt *DIM1)
*       (SpiceInt *DIM1, type **OUT_ARRAY1)
* This SWIG code is responsible for initializing the variable into which the C
* code will put the allocated memory to NULL. This SWIG code is also responsible in
* all cases for freeing the allocated memory.
*******************************************************************************/

%define TYPEMAP_ARGOUT(Type, Typecode) // Use to fill in numeric types below!

/*******************************************************
* (Type OUT_ARRAY1[ANY])
*******************************************************/

%typemap(in, numinputs=0)
    (Type OUT_ARRAY1[ANY])                                      // PATTERN
        (PyArrayObject* pyarr = NULL)
{
//      $1_type $1_name
//      (Type OUT_ARRAY1[ANY])

    npy_intp dims[1] = {$1_dim0};                               // DIMENSIONS
    pyarr = (PyArrayObject *) PyArray_SimpleNew(1, dims, Typecode);
    TEST_MALLOC_FAILURE(pyarr);

    $1 = ($1_ltype) PyArray_DATA(pyarr);                        // ARRAY
}

/*******************************************************
* (Type OUT_ARRAY1[ANY], SpiceInt DIM1)
*******************************************************/

%typemap(in, numinputs=0)
    (Type OUT_ARRAY1[ANY], SpiceInt DIM1)                       // PATTERN
        (PyArrayObject* pyarr = NULL)
{
//      $1_type $1_name, $2_type $2_name
//      (Type OUT_ARRAY1[ANY], SpiceInt DIM1)
//  NOT CURRENTLY USED BY CSPICE

    npy_intp dims[1] = {$1_dim0};                               // ARRAY
    pyarr = (PyArrayObject *) PyArray_SimpleNew(1, dims, Typecode);
    TEST_MALLOC_FAILURE(pyarr);

    $1 = ($1_ltype) PyArray_DATA(pyarr);                        // ARRAY
    $2 = (SpiceInt) PyArray_DIM(pyarr, 0);                      // DIM1
}

/*******************************************************
* (SpiceInt DIM1, Type OUT_ARRAY1[ANY])
*******************************************************/

%typemap(in, numinputs=0)
    (SpiceInt DIM1, Type OUT_ARRAY1[ANY])                       // PATTERN
        (PyArrayObject* pyarr = NULL)
{
//      $1_type $1_name, $2_type $2_name
//      (SpiceInt DIM1, Type OUT_ARRAY1[ANY])
//  NOT CURRENTLY USED BY CSPICE

    npy_intp dims[1] = {$2_dim0};                               // ARRAY
    pyarr = (PyArrayObject *) PyArray_SimpleNew(1, dims, Typecode);
    TEST_MALLOC_FAILURE(pyarr);

    $2 = ($2_ltype) PyArray_DATA(pyarr);                        // ARRAY
    $1 = (SpiceInt) PyArray_DIM(pyarr, 0);                      // DIM1
//  $3 = &size[0];                                              // SIZE1
}

/*******************************************************
* (Type OUT_ARRAY1[ANY], SpiceInt DIM1, SpiceInt *SIZE1)
*******************************************************/

%typemap(in, numinputs=0)
    (Type OUT_ARRAY1[ANY], SpiceInt DIM1, SpiceInt *SIZE1)      // PATTERN
        (PyArrayObject* pyarr = NULL, SpiceInt size[1])
{
//      $1_type $1_name, $2_type $2_name, $3_type $3_name
//      (Type OUT_ARRAY1[ANY], SpiceInt DIM1, SpiceInt *SIZE1)
//  NOT CURRENTLY USED BY CSPICE

    size[0] = 0;
    npy_intp dims[1] = {$1_dim0};                               // ARRAY
    pyarr = (PyArrayObject *) PyArray_SimpleNew(1, dims, Typecode);
    TEST_MALLOC_FAILURE(pyarr);

    $1 = ($1_ltype) PyArray_DATA(pyarr);                        // ARRAY
    $2 = (SpiceInt) PyArray_DIM(pyarr, 0);                      // DIM1
    $3 = &size[0];                                              // SIZE1
}

/*******************************************************
* (Type OUT_ARRAY1[ANY], SpiceInt *SIZE1, SpiceInt DIM1)
*******************************************************/

%typemap(in, numinputs=0)
    (Type OUT_ARRAY1[ANY], SpiceInt *SIZE1, SpiceInt DIM1)      // PATTERN
        (PyArrayObject* pyarr = NULL, SpiceInt size[1])
{
//      $1_type $1_name, $2_type $2_name, $3_type $3_name
//      (Type OUT_ARRAY1[ANY], SpiceInt *SIZE1, SpiceInt DIM1)
//  NOT CURRENTLY USED BY CSPICE

    size[0] = 0;
    npy_intp dims[1] = {$1_dim0};                               // ARRAY
    pyarr = (PyArrayObject *) PyArray_SimpleNew(1, dims, Typecode);
    TEST_MALLOC_FAILURE(pyarr);

    $1 = ($1_ltype) PyArray_DATA(pyarr);                        // ARRAY
    $3 = (SpiceInt) PyArray_DIM(pyarr, 0);                      // DIM1
    $2 = &size[0];                                              // SIZE1
}

/*******************************************************
* (SpiceInt DIM1, SpiceInt *SIZE1, Type OUT_ARRAY1[ANY])
*******************************************************/

%typemap(in, numinputs=0)
    (SpiceInt DIM1, SpiceInt *SIZE1, Type OUT_ARRAY1[ANY])      // PATTERN
        (PyArrayObject* pyarr = NULL, SpiceInt size[1])
{
//      $1_type $1_name, $2_type $2_name, $3_type $3_name
//      (SpiceInt DIM1, SpiceInt *SIZE1, Type OUT_ARRAY1[ANY])

    size[0] = 0;
    npy_intp dims[1] = {$3_dim0};                               // ARRAY
    pyarr = (PyArrayObject *) PyArray_SimpleNew(1, dims, Typecode);
    TEST_MALLOC_FAILURE(pyarr);

    $3 = ($3_ltype) PyArray_DATA(pyarr);                        // ARRAY
    $1 = (SpiceInt) PyArray_DIM(pyarr, 0);                      // DIM1
    $2 = &size[0];                                              // SIZE1
}

/*******************************************************
* (SpiceInt *SIZE1, SpiceInt DIM1, Type OUT_ARRAY1[ANY])
*******************************************************/

%typemap(in, numinputs=0)
    (SpiceInt *SIZE1, SpiceInt DIM1, Type OUT_ARRAY1[ANY])      // PATTERN
        (PyArrayObject* pyarr = NULL, SpiceInt size[1])
{
//      $1_type $1_name, $2_type $2_name, $3_type $3_name
//      (SpiceInt *SIZE1, SpiceInt DIM1, Type OUT_ARRAY1[ANY])
//  NOT CURRENTLY USED BY CSPICE

    size[0] = 0;
    npy_intp dims[1] = {$3_dim0};                               // ARRAY
    pyarr = (PyArrayObject *) PyArray_SimpleNew(1, dims, Typecode);
    TEST_MALLOC_FAILURE(pyarr);

    $3 = ($3_ltype) PyArray_DATA(pyarr);                        // ARRAY
    $2 = (SpiceInt) PyArray_DIM(pyarr, 0);                           // DIM1
    $1 = &size[0];                                              // SIZE1
}

/*******************************************************
* (Type OUT_ARRAY1[ANY], SpiceInt *SIZE1)
*******************************************************/

%typemap(in, numinputs=0)
    (Type OUT_ARRAY1[ANY], SpiceInt *SIZE1)                     // PATTERN
        (PyArrayObject* pyarr = NULL, SpiceInt size[1])
{
//      $1_type $1_name, $2_type $2_name
//      (Type OUT_ARRAY1[ANY], SpiceInt *SIZE1)

    size[0] = 0;
    npy_intp dims[1] = {$1_dim0};                               // ARRAY
    pyarr = (PyArrayObject *) PyArray_SimpleNew(1, dims, Typecode);
    TEST_MALLOC_FAILURE(pyarr);

    $1 = ($1_ltype) PyArray_DATA(pyarr);                        // ARRAY
    $2 = &size[0];                                              // SIZE1
}

/*******************************************************
* (SpiceInt *SIZE1, Type OUT_ARRAY1[ANY])
*******************************************************/

%typemap(in, numinputs=0)
    (SpiceInt *SIZE1, Type OUT_ARRAY1[ANY])                     // PATTERN
        (PyArrayObject* pyarr = NULL, SpiceInt size[1])
{
//      $1_type $1_name, $2_type $2_name
//      (SpiceInt *SIZE1, Type OUT_ARRAY1[ANY])

    size[0] = 0;
    npy_intp dims[1] = {$2_dim0};                               // ARRAY
    pyarr = (PyArrayObject *) PyArray_SimpleNew(1, dims, Typecode);
    TEST_MALLOC_FAILURE(pyarr);

    $2 = ($2_ltype) PyArray_DATA(pyarr);                        // ARRAY
    $1 = &size[0];                                              // SIZE1
}

/*******************************************************
* %typemap(argout)
* %typemap(freearg)
*******************************************************/

%typemap(argout)
    (Type OUT_ARRAY1[ANY]),
    (Type OUT_ARRAY1[ANY], SpiceInt DIM1),
    (SpiceInt DIM1, Type OUT_ARRAY1[ANY])
{
    $result = SWIG_Python_AppendOutput($result, (PyObject *) pyarr$argnum);
    // AppendOutput steals the reference to the argument.
    pyarr$argnum = NULL;
}

%typemap(argout)
    (Type OUT_ARRAY1[ANY], SpiceInt DIM1, SpiceInt *SIZE1),
    (Type OUT_ARRAY1[ANY], SpiceInt *SIZE1, SpiceInt DIM1),
    (SpiceInt DIM1, SpiceInt *SIZE1, Type OUT_ARRAY1[ANY]),
    (SpiceInt *SIZE1, SpiceInt DIM1, Type OUT_ARRAY1[ANY]),
    (Type OUT_ARRAY1[ANY], SpiceInt *SIZE1),
    (SpiceInt *SIZE1, Type OUT_ARRAY1[ANY])
{
    // Reshape to indicate the number of elements we actually created
    npy_intp new_dim[1] = {size$argnum[0]};
    HANDLE_RESIZE(pyarr$argnum, new_dim)

    $result = SWIG_Python_AppendOutput($result, (PyObject *) pyarr$argnum);
    // AppendOutput steals the reference to the argument.
    pyarr$argnum = NULL;
}

%typemap(freearg)
    (Type OUT_ARRAY1[ANY]),
    (Type OUT_ARRAY1[ANY], SpiceInt DIM1),
    (SpiceInt DIM1, Type OUT_ARRAY1[ANY]),
    (Type OUT_ARRAY1[ANY], SpiceInt DIM1, SpiceInt *SIZE1),
    (Type OUT_ARRAY1[ANY], SpiceInt *SIZE1, SpiceInt DIM1),
    (SpiceInt DIM1, SpiceInt *SIZE1, Type OUT_ARRAY1[ANY]),
    (SpiceInt *SIZE1, SpiceInt DIM1, Type OUT_ARRAY1[ANY]),
    (Type OUT_ARRAY1[ANY], SpiceInt *SIZE1),
    (SpiceInt *SIZE1, Type OUT_ARRAY1[ANY])
{
    Py_XDECREF(pyarr$argnum);
}

/***************************************************************
* (Type **OUT_ARRAY1, SpiceInt *SIZE1)
***************************************************************/

%typemap(in, numinputs=0)
    (Type **OUT_ARRAY1, SpiceInt *SIZE1)
        (PyArrayObject* pyarr=NULL, Type *buffer=NULL, SpiceInt dimsize[1])
{
//      $1_type $1_name, $2_type $2_name
//      (Type **OUT_ARRAY1, SpiceInt *SIZE1)

    dimsize[0] = 0;
    $1 = &buffer;                                               // ARRAY
    $2 = &dimsize[0];                                           // SIZE1
}

/***************************************************************
* (SpiceInt *SIZE1, Type **OUT_ARRAY1)
***************************************************************/

%typemap(in, numinputs=0)
    (SpiceInt *SIZE1, Type **OUT_ARRAY1)
        (PyArrayObject* pyarr=NULL, Type *buffer=NULL, SpiceInt dimsize[1])
{
//      $1_type $1_name, $2_type $2_name
//      (SpiceInt *SIZE1, Type **OUT_ARRAY1)

    dimsize[0] = 0;
    $2 = &buffer;                                               // ARRAY
    $1 = &dimsize[0];                                           // SIZE1
}

/*******************************************************
* %typemap(argout)
* %typemap(freearg)
*******************************************************/

%typemap(argout)
    (Type **OUT_ARRAY1, SpiceInt *SIZE1),
    (SpiceInt *SIZE1, Type **OUT_ARRAY1)
{
//      (Type **OUT_ARRAY1, SpiceInt *SIZE1)
//      (SpiceInt *SIZE1, Type **OUT_ARRAY1)

    TEST_MALLOC_FAILURE(buffer$argnum);
    npy_intp dims[1] = {dimsize$argnum[0]};
    pyarr$argnum = create_array_with_owned_data(1, dims, Typecode,  (void **)&buffer$argnum);
    TEST_MALLOC_FAILURE(pyarr$argnum);

    $result = SWIG_Python_AppendOutput($result, (PyObject *) pyarr$argnum);
    // AppendOutput steals the reference to the argument.
    pyarr$argnum = NULL;
}

%typemap(freearg)
    (Type **OUT_ARRAY1, SpiceInt *SIZE1),
    (SpiceInt *SIZE1, Type **OUT_ARRAY1)
{
    Py_XDECREF(pyarr$argnum);
    PyMem_Free((void *) buffer$argnum);
}

/*******************************************************
* Now define these typemaps for every numeric type
*******************************************************/

%enddef

TYPEMAP_ARGOUT(SpiceInt,      NPY_INT   )
TYPEMAP_ARGOUT(SpiceBoolean,  NPY_INT   )
TYPEMAP_ARGOUT(SpiceDouble,   NPY_DOUBLE)

#undef TYPEMAP_ARGOUT

/*******************************************************************************
* If the function should return a Python scalar on size = 0:
*       (type **OUT_ARRAY01, SpiceInt *DIM1)
*******************************************************************************/

%define TYPEMAP_ARGOUT(Type, Typecode) // To fill in types below!

/***************************************************************
* (Type **OUT_ARRAY01, SpiceInt *SIZE1)
***************************************************************/

%typemap(in, numinputs=0)
    (Type **OUT_ARRAY01, SpiceInt *SIZE1)
        (PyArrayObject* pyarr=NULL, Type *buffer=NULL, SpiceInt dimsize[1])
{
//      $1_type $1_name, $2_type $2_name
//      (Type **OUT_ARRAY01, SpiceInt *SIZE1)

    $1 = &buffer;                                               // ARRAY
    $2 = &dimsize[0];                                           // SIZE1
}

/*******************************************************
* %typemap(argout)
* %typemap(freearg)
*******************************************************/

%typemap(argout)
    (Type **OUT_ARRAY01, SpiceInt *SIZE1)
{
//      (Type **OUT_ARRAY01, SpiceInt *SIZE1)

    TEST_MALLOC_FAILURE(buffer$argnum);
    npy_intp dim = max(dimsize$argnum[0], 1);
    pyarr$argnum = (PyArrayObject *) create_array_with_owned_data(1, &dim, Typecode,  (void **)&buffer$argnum);
    TEST_MALLOC_FAILURE(pyarr$argnum);

    if (dimsize$argnum[0] == 0) {
        PyObject* value = PyArray_GETITEM(pyarr$argnum, PyArray_DATA(pyarr$argnum));
        TEST_MALLOC_FAILURE(value);
        // AppendOutput steals the reference to this object, so we don't need DECREF
        // pyarr$argnum is cleaned up by the freearg
        $result = SWIG_Python_AppendOutput($result, value);
    } else {
        $result = SWIG_Python_AppendOutput($result, (PyObject *)pyarr$argnum);
        // AppendOutput steals the reference to the argument.
        pyarr$argnum = NULL;
    }
}

%typemap(freearg)
    (Type **OUT_ARRAY01, SpiceInt *SIZE1)
{
    Py_XDECREF(pyarr$argnum);
    PyMem_Free((void *) buffer$argnum);
}

%enddef

/*******************************************************
* Now define these typemaps for every numeric type
*******************************************************/

TYPEMAP_ARGOUT(SpiceInt,      NPY_INT)
TYPEMAP_ARGOUT(SpiceInt,      NPY_INT)
TYPEMAP_ARGOUT(SpiceBoolean,  NPY_INT)
TYPEMAP_ARGOUT(long,          NPY_LONG)
TYPEMAP_ARGOUT(double,        NPY_DOUBLE)
TYPEMAP_ARGOUT(SpiceDouble,   NPY_DOUBLE)

#undef TYPEMAP_ARGOUT


/*******************************************************************************
* 2-D numeric typemaps for output
*
* This family of typemaps allows arrays of numbers returned by C to appear as
* Numpy arrays inside Python.
*
* If the size of the array can be specified in the SWIG interface:
*       (type OUT_ARRAY2[ANY][ANY])
*       (type OUT_ARRAY2[ANY][ANY], SpiceInt DIM1, SpiceInt DIM2)
*       (SpiceInt DIM1, SpiceInt DIM2, type OUT_ARRAY2[ANY][ANY])
*
* If the upper limit on the size of the array's first axis can be specified in
* the SWIG interface, but the size of the first axis returned by C is variable:
*       (type OUT_ARRAY2[ANY][ANY], SpiceInt DIM1, SpiceInt DIM2, SpiceInt *SIZE1)
*       (type OUT_ARRAY2[ANY][ANY], SpiceInt *SIZE1, SpiceInt DIM1, SpiceInt DIM2)
*       (SpiceInt DIM1, SpiceInt DIM2, SpiceInt *SIZE1, type OUT_ARRAY2[ANY][ANY])
*       (SpiceInt *SIZE1, SpiceInt DIM1, SpiceInt DIM2, type OUT_ARRAY2[ANY][ANY])
* Also...
*       (SpiceInt DIM1, SpiceInt *SIZE1, type OUT_ARRAY2[ANY][ANY])
*       (SpiceInt *SIZE1, type OUT_ARRAY2[ANY][ANY])
*
* If an upper limit on the total size of a temporary memory buffer can be
* specified in advance, and the shape of the array then returned afterward.
* Upon return, the large buffer is freed and only the required amount of memory
* is retained.
*       (type OUT_ARRAY2[ANY][ANY], SpiceInt *SIZE1, SpiceInt *SIZE2)
*       (SpiceInt *SIZE1, SpiceInt *SIZE2, type OUT_ARRAY2[ANY][ANY])
*
* If the C function will allocate the memory it needs and will return the
* dimensions:
*       (type **OUT_ARRAY2, SpiceInt *DIM1, SpiceInt *DIM2)
*       (SpiceInt *DIM1, SpiceInt *DIM2, type **OUT_ARRAY2)
*
* This version will return a 1-D array if the first dimension is 0; otherwise
* a 2-D array:
*       (type **OUT_ARRAY12, SpiceInt *DIM1, SpiceInt *DIM2)
* Note that ownership of the buffer for **OUT_ARRAY2 and **OUT_ARRAY12 is the same
* as with *OUT_ARRAY2:
*
* This SWIG code is responsible for initializing the variable into which the C
* code will put the allocated memory to NULL. This SWIG code is also responsible in
* all cases for freeing the allocated memory if that variable is non-NULL.
*******************************************************************************/

%define TYPEMAP_ARGOUT(Type, Typecode) // Use to fill in numeric types below!

/***************************************************************
* (Type OUT_ARRAY2[ANY][ANY])
***************************************************************/

%typemap(in, numinputs=0)
    (Type OUT_ARRAY2[ANY][ANY])                                 // PATTERN
        (PyArrayObject* pyarr = NULL)
{
//      $1_type $1_name
//      (Type OUT_ARRAY2[ANY][ANY])

    npy_intp dims[2] = {$1_dim0, $1_dim1};               // ARRAY
    pyarr = (PyArrayObject *) PyArray_SimpleNew(2, dims, Typecode);
    TEST_MALLOC_FAILURE(pyarr);

    $1 = ($1_ltype) PyArray_DATA(pyarr);                        // ARRAY
}

/***************************************************************
* (Type OUT_ARRAY2[ANY][ANY], SpiceInt DIM1, SpiceInt DIM2)
***************************************************************/

%typemap(in, numinputs=0)
    (Type OUT_ARRAY2[ANY][ANY], SpiceInt DIM1, SpiceInt DIM2)   // PATTERN
        (PyArrayObject* pyarr = NULL)
{
//      $1_type $1_name, $2_type $2_name, $3_type $3_name
//      (Type OUT_ARRAY2[ANY][ANY], SpiceInt DIM1, SpiceInt DIM2)
//  NOT CURRENTLY USED BY CSPICE

    npy_intp dims[2] = {$1_dim0, $1_dim1};                      // ARRAY
    pyarr = (PyArrayObject *) PyArray_SimpleNew(2, dims, Typecode);
    TEST_MALLOC_FAILURE(pyarr);

    $1 = ($1_ltype) PyArray_DATA(pyarr);                        // ARRAY
    $2 = (SpiceInt) PyArray_DIM(pyarr, 0);                      // DIM1
    $3 = (SpiceInt) PyArray_DIM(pyarr, 1);                      // DIM2
}

/***************************************************************
* (SpiceInt DIM1, SpiceInt DIM2, Type OUT_ARRAY2[ANY][ANY])
***************************************************************/

%typemap(in, numinputs=0)
    (SpiceInt DIM1, SpiceInt DIM2, Type OUT_ARRAY2[ANY][ANY])   // PATTERN
        (PyArrayObject* pyarr = NULL),
    (SpiceInt DIM1, SpiceInt DIM2, Type OUT_ARRAY2[ANY][ANY])   // PATTERN
        (PyArrayObject* pyarr = NULL)
{
//      $1_type $1_name, $2_type $2_name, $3_type $3_name
//      (SpiceInt DIM1, SpiceInt DIM2, Type OUT_ARRAY2[ANY][ANY])
//  NOT CURRENTLY USED BY CSPICE

    npy_intp dims[2] = {$3_dim0, $3_dim1};                      // ARRAY
    pyarr = (PyArrayObject *) PyArray_SimpleNew(2, dims, Typecode);
    TEST_MALLOC_FAILURE(pyarr);

    $3 = ($3_ltype) PyArray_DATA(pyarr);                        // ARRAY
    $1 = (SpiceInt) PyArray_DIM(pyarr, 0);                      // DIM1
    $2 = (SpiceInt) PyArray_DIM(pyarr, 1);                      // DIM2
}

/***************************************************************
* (Type OUT_ARRAY2[ANY][ANY], SpiceInt DIM1, SpiceInt DIM2, SpiceInt *SIZE1)
***************************************************************/

%typemap(in, numinputs=0)
    (Type OUT_ARRAY2[ANY][ANY], SpiceInt DIM1, SpiceInt DIM2, SpiceInt *SIZE1)
        (PyArrayObject* pyarr = NULL, SpiceInt dimsize[2], SpiceInt outsize)
{
//      $1_type $1_name, $2_type $2_name, $3_type $3_name, $4_type $4_name
//      (Type OUT_ARRAY2[ANY][ANY], SpiceInt DIM1, SpiceInt DIM2, SpiceInt *SIZE1)
//  NOT CURRENTLY USED BY CSPICE

    outsize = 0;
    npy_intp dims[2] = {$1_dim0, $1_dim1};               // ARRAY
    pyarr = (PyArrayObject *) PyArray_SimpleNew(2, dims, Typecode);
    TEST_MALLOC_FAILURE(pyarr);

    dimsize[0] = (SpiceInt) dims[0];
    dimsize[1] = (SpiceInt) dim$argnums[1];

    $1 = ($1_ltype) PyArray_DATA(pyarr);                        // ARRAY
    $2 = (SpiceInt) PyArray_DIM(pyarr, 0);                      // DIM1
    $3 = (SpiceInt) PyArray_DIM(pyarr, 1);                      // DIM2
    $4 = &outsize;                                              // SIZE1
}

/***************************************************************
* (Type OUT_ARRAY2[ANY][ANY], SpiceInt *SIZE1, SpiceInt DIM1, SpiceInt DIM2)
***************************************************************/

%typemap(in, numinputs=0)
    (Type OUT_ARRAY2[ANY][ANY], SpiceInt *SIZE1, SpiceInt DIM1, SpiceInt DIM2)
        (PyArrayObject* pyarr = NULL, SpiceInt dimsize[2], SpiceInt outsize)
{
//      $1_type $1_name, $2_type $2_name, $3_type $3_name
//      (Type OUT_ARRAY2[ANY][ANY], SpiceInt *SIZE1, SpiceInt DIM1, SpiceInt DIM2)
//  NOT CURRENTLY USED BY CSPICE

    outsize = 0;
    npy_intp dims[2] = {$1_dim0, $1_dim1};                      // ARRAY
    pyarr = (PyArrayObject *) PyArray_SimpleNew(2, dims, Typecode);
    TEST_MALLOC_FAILURE(pyarr);

    dimsize[0] = (SpiceInt) dims[0];
    dimsize[1] = (SpiceInt) dims[1];

    $1 = ($1_ltype) PyArray_DATA(pyarr);                        // ARRAY
    $3 = (SpiceInt) PyArray_DIM(pyarr, 0);                      // DIM1
    $4 = (SpiceInt) PyArray_DIM(pyarr, 1);                       // DIM2
    $2 = &outsize;                                              // SIZE1
}

/***************************************************************
* (SpiceInt DIM1, SpiceInt DIM2, SpiceInt *SIZE1, Type OUT_ARRAY2[ANY][ANY])
***************************************************************/

%typemap(in, numinputs=0)
    (SpiceInt DIM1, SpiceInt DIM2, SpiceInt *SIZE1, Type OUT_ARRAY2[ANY][ANY])
        (PyArrayObject* pyarr = NULL, SpiceInt dimsize[2], SpiceInt outsize)
{
//      $1_type $1_name, $2_type $2_name, $3_type $3_name, $4_type $4_name
//      (SpiceInt DIM1, SpiceInt DIM2, SpiceInt *SIZE1, Type OUT_ARRAY2[ANY][ANY])
//  NOT CURRENTLY USED BY CSPICE

    outsize = 0;
    npy_intp dims[2] = {$4_dim0, $4_dim1};                      // ARRAY
    pyarr = (PyArrayObject *) PyArray_SimpleNew(2, dims, Typecode);
    TEST_MALLOC_FAILURE(pyarr);

    dimsize[0] = (SpiceInt) dims[0];
    dimsize[1] = (SpiceInt) dims[1];

    $4 = ($4_ltype) PyArray_DATA(pyarr);                        // ARRAY
    $1 = (SpiceInt) PyArray_DIM(pyarr, 0);                           // DIM1
    $2 = (SpiceInt) PyArray_DIM(pyarr, 1);                           // DIM2
    $3 = &outsize;                                              // SIZE1
}

/***************************************************************
* (SpiceInt DIM1, SpiceInt *SIZE1, Type OUT_ARRAY2[ANY][ANY])
***************************************************************/

%typemap(in, numinputs=0)
    (SpiceInt DIM1, SpiceInt *SIZE1, Type OUT_ARRAY2[ANY][ANY])
        (PyArrayObject* pyarr = NULL, SpiceInt dimsize[2], SpiceInt outsize)
{
//      $1_type $1_name, $2_type $2_name, $3_type $3_name
//      (SpiceInt DIM1, SpiceInt *SIZE1, Type OUT_ARRAY2[ANY][ANY])
//  NOT CURRENTLY USED BY CSPICE

    outsize = 0;
    npy_intp dims[2] = {$3_dim0, $3_dim1};                      // ARRAY
    pyarr = (PyArrayObject *) PyArray_SimpleNew(2, dims, Typecode);
    TEST_MALLOC_FAILURE(pyarr);

    dimsize[0] = (SpiceInt) dims[0];
    dimsize[1] = (SpiceInt) $3_dim1;

    $3 = ($3_ltype) PyArray_DATA(pyarr);                        // ARRAY
    $1 = (SpiceInt) PyArray_DIM(pyarr, 0);                           // DIM1
    $2 = &outsize;                                              // SIZE1
}

/***************************************************************
* (SpiceInt *SIZE1, SpiceInt DIM1, SpiceInt DIM2, Type OUT_ARRAY2[ANY][ANY])
***************************************************************/

%typemap(in, numinputs=0)
    (SpiceInt *SIZE1, SpiceInt DIM1, SpiceInt DIM2, Type OUT_ARRAY2[ANY][ANY])
        (PyArrayObject* pyarr = NULL, SpiceInt dimsize[2], SpiceInt outsize)
{
//      $1_type $1_name, $2_type $2_name, $3_type $3_name, $4_name $4_type
//      (SpiceInt *SIZE1, SpiceInt DIM1, SpiceInt DIM2, Type OUT_ARRAY2[ANY][ANY])
//  NOT CURRENTLY USED BY CSPICE

    outsize = 0;
    npy_intp dims[2] = {$4_dim0, $4_dim1};                      // ARRAY
    pyarr = (PyArrayObject *) PyArray_SimpleNew(2, dims, Typecode);
    TEST_MALLOC_FAILURE(pyarr);

    dimsize[0] = (SpiceInt) dims[0];
    dimsize[1] = (SpiceInt) dims[1];

    $4 = ($4_ltype) PyArray_DATA(pyarr);                        // ARRAY
    $2 = (SpiceInt) PyArray_DIM(pyarr, 0);                      // DIM1
    $3 = (SpiceInt) PyArray_DIM(pyarr, 1);                      // DIM2
    $1 = &outsize;                                              // SIZE1
}

/***************************************************************
* (Type OUT_ARRAY2[ANY][ANY], SpiceInt *SIZE1)
***************************************************************/

%typemap(in, numinputs=0)
    (Type OUT_ARRAY2[ANY][ANY], SpiceInt *SIZE1)
        (PyArrayObject* pyarr = NULL, SpiceInt dimsize[2], SpiceInt outsize)
{
//      $1_type $1_name, $2_type $2_name
//      (Type OUT_ARRAY2[ANY][ANY], SpiceInt *SIZE1)

    outsize = 0;
    npy_intp dims[2] = {$1_dim0, $1_dim1};                      // ARRAY
    pyarr = (PyArrayObject *) PyArray_SimpleNew(2, dims, Typecode);
    TEST_MALLOC_FAILURE(pyarr);

    dimsize[0] = (SpiceInt) dims[0];
    dimsize[1] = (SpiceInt) dims[1];

    $1 = ($1_ltype) PyArray_DATA(pyarr);                        // ARRAY
    $2 = &outsize;                                              // SIZE1
}

/***************************************************************
* (SpiceInt *SIZE1, Type OUT_ARRAY2[ANY][ANY])
***************************************************************/

%typemap(in, numinputs=0)
    (SpiceInt *SIZE1, Type OUT_ARRAY2[ANY][ANY])
        (PyArrayObject* pyarr = NULL, SpiceInt dimsize[2], SpiceInt outsize)
{
//      $1_type $1_name, $2_type $2_name
//      (SpiceInt *SIZE1, Type OUT_ARRAY2[ANY][ANY])

    outsize = 0;
    npy_intp dims[2] = {$2_dim0, $2_dim1};                      // ARRAY
    pyarr = (PyArrayObject *) PyArray_SimpleNew(2, dims, Typecode);
    TEST_MALLOC_FAILURE(pyarr);

    dimsize[0] = (SpiceInt) dims[0];
    dimsize[1] = (SpiceInt) dims[1];

    $2 = ($2_ltype) PyArray_DATA(pyarr);                        // ARRAY
    $1 = &outsize;                                              // SIZE1
}

/***************************************************************
* (Type OUT_ARRAY2[ANY][ANY], SpiceInt *SIZE1, SpiceInt *SIZE2)
***************************************************************/

%typemap(in, numinputs=0)
    (Type OUT_ARRAY2[ANY][ANY], SpiceInt *SIZE1, SpiceInt *SIZE2)
        (PyArrayObject* pyarr = NULL, SpiceInt dimsize[2], SpiceInt outsize)
{
//      $1_type $1_name, $2_type $2_name, $3_type $3_name
//      (Type OUT_ARRAY2[ANY][ANY], SpiceInt *SIZE1, SpiceInt *SIZE2)
//  NOT CURRENTLY USED BY CSPICE

    outsize = 0;
    npy_intp dims[2] = {$1_dim0, $1_dim1};                      // ARRAY
    pyarr = (PyArrayObject *) PyArray_SimpleNew(2, dims, Typecode);
    TEST_MALLOC_FAILURE(pyarr);

    dimsize[0] = (SpiceInt) dims[0];
    dimsize[1] = (SpiceInt) dims[1];

    $1 = ($1_ltype) PyArray_DATA(pyarr);                        // ARRAY
    $2 = &outsize;                                              // SIZE1
}

/***************************************************************
* (SpiceInt *SIZE1, SpiceInt *SIZE2, Type OUT_ARRAY2[ANY][ANY])
***************************************************************/

%typemap(in, numinputs=0)
    (SpiceInt *SIZE1, SpiceInt *SIZE2, Type OUT_ARRAY2[ANY][ANY])
        (PyArrayObject* pyarr = NULL, SpiceInt outsize[2])
{
//      $1_type $1_name, $2_type $2_name, $3_type $3_name
//      (SpiceInt *SIZE1, SpiceInt *SIZE2, Type OUT_ARRAY2[ANY][ANY])

    outsize[0] = 0;
    outsize[1] = 0;
    npy_intp dims[2] = {$3_dim0, $3_dim1};                      // ARRAY
    pyarr = (PyArrayObject *) PyArray_SimpleNew(2, dims, Typecode);
    TEST_MALLOC_FAILURE(pyarr);

    $3 = ($3_ltype) PyArray_DATA(pyarr);                        // ARRAY
    $1 = &outsize[0];                                           // SIZE1
    $2 = &outsize[1];                                           // SIZE2
}

/*******************************************************
* %typemap(argout)
* %typemap(freearg)
*******************************************************/

%typemap(argout)
    (Type OUT_ARRAY2[ANY][ANY]),
    (Type OUT_ARRAY2[ANY][ANY], SpiceInt DIM1, SpiceInt DIM2),
    (SpiceInt DIM1, SpiceInt DIM2, Type OUT_ARRAY2[ANY][ANY])
{
    $result = SWIG_Python_AppendOutput($result, (PyObject *) pyarr$argnum);
    // AppendOutput steals the reference to the argument.
    pyarr$argnum = NULL;
}

%typemap(argout)
    (Type OUT_ARRAY2[ANY][ANY], SpiceInt DIM1, SpiceInt DIM2, SpiceInt *SIZE1),
    (Type OUT_ARRAY2[ANY][ANY], SpiceInt *SIZE1, SpiceInt DIM1, SpiceInt DIM2),
    (SpiceInt DIM1, SpiceInt DIM2, SpiceInt *SIZE1, Type OUT_ARRAY2[ANY][ANY]),
    (SpiceInt DIM1, SpiceInt *SIZE1, Type OUT_ARRAY2[ANY][ANY]),
    (SpiceInt *SIZE1, SpiceInt DIM1, SpiceInt DIM2, Type OUT_ARRAY2[ANY][ANY]),
    (Type OUT_ARRAY2[ANY][ANY], SpiceInt *SIZE1),
    (SpiceInt *SIZE1, Type OUT_ARRAY2[ANY][ANY])
{
    npy_intp dims[2] = {outsize$argnum, dimsize$argnum[1]};
    HANDLE_RESIZE(pyarr$argnum, dims)
    $result = SWIG_Python_AppendOutput($result, (PyObject *)pyarr$argnum);
    // AppendOutput steals the reference to the argument.
    pyarr$argnum = NULL;
}

%typemap(argout)
    (Type OUT_ARRAY2[ANY][ANY], SpiceInt *SIZE1, SpiceInt *SIZE2),
    (SpiceInt *SIZE1, SpiceInt *SIZE2, Type OUT_ARRAY2[ANY][ANY])
{
    npy_intp dims[2] = {outsize$argnum[0], outsize$argnum[1]};
    HANDLE_RESIZE(pyarr$argnum, dims)
    $result = SWIG_Python_AppendOutput($result, (PyObject *)pyarr$argnum);
    // AppendOutput steals the reference to the argument.
    pyarr$argnum = NULL;
}

%typemap(freearg)
    (Type OUT_ARRAY2[ANY][ANY]),
    (Type OUT_ARRAY2[ANY][ANY], SpiceInt DIM1, SpiceInt DIM2),
    (SpiceInt DIM1, SpiceInt DIM2, Type OUT_ARRAY2[ANY][ANY]),

    (Type OUT_ARRAY2[ANY][ANY], SpiceInt DIM1, SpiceInt DIM2, SpiceInt *SIZE1),
    (Type OUT_ARRAY2[ANY][ANY], SpiceInt *SIZE1, SpiceInt DIM1, SpiceInt DIM2),
    (SpiceInt DIM1, SpiceInt DIM2, SpiceInt *SIZE1, Type OUT_ARRAY2[ANY][ANY]),
    (SpiceInt DIM1, SpiceInt *SIZE1, Type OUT_ARRAY2[ANY][ANY]),
    (SpiceInt *SIZE1, SpiceInt DIM1, SpiceInt DIM2, Type OUT_ARRAY2[ANY][ANY]),
    (Type OUT_ARRAY2[ANY][ANY], SpiceInt *SIZE1),
    (SpiceInt *SIZE1, Type OUT_ARRAY2[ANY][ANY]),

    (Type OUT_ARRAY2[ANY][ANY], SpiceInt *SIZE1, SpiceInt *SIZE2),
    (SpiceInt *SIZE1, SpiceInt *SIZE2, Type OUT_ARRAY2[ANY][ANY])
{
    Py_XDECREF(pyarr$argnum);
}

/***************************************************************
* (Type **OUT_ARRAY2, SpiceInt *SIZE1, SpiceInt *SIZE2)
***************************************************************/

%typemap(in, numinputs=0)
    (Type **OUT_ARRAY2, SpiceInt *SIZE1, SpiceInt *SIZE2)
        (PyArrayObject* pyarr=NULL, Type *buffer=NULL, SpiceInt dimsize[2]),
    (Type **OUT_ARRAY12, SpiceInt *SIZE1, SpiceInt *SIZE2)
        (PyArrayObject* pyarr=NULL, Type *buffer=NULL, SpiceInt dimsize[2])
{
//      $1_type $1_name, $2_type $2_name, $3_type $3_name
//      (Type **OUT_ARRAY2, SpiceInt *SIZE1, SpiceInt *SIZE2)

    $1 = &buffer;                                               // ARRAY
    $2 = &dimsize[0];                                           // SIZE1
    $3 = &dimsize[1];                                           // SIZE2
}

/***************************************************************
* (SpiceInt *SIZE1, SpiceInt *SIZE2, Type **OUT_ARRAY2)
***************************************************************/

%typemap(in, numinputs=0)
    (SpiceInt *SIZE1, SpiceInt *SIZE2, Type **OUT_ARRAY2)
        (PyArrayObject* pyarr=NULL, Type *buffer=NULL, SpiceInt dimsize[2])
{
//      $1_type $1_name, $2_type $2_name, $3_type $3_name
//      (SpiceInt *SIZE1, SpiceInt *SIZE2, Type **OUT_ARRAY2)
//  NOT CURRENTLY USED BY CSPICE

    $3 = &buffer;                                               // ARRAY
    $1 = &dimsize[0];                                           // SIZE1
    $2 = &dimsize[1];                                           // SIZE2
}

/*******************************************************
* %typemap(argout)
* %typemap(freearg)
*******************************************************/

%typemap(argout)
    (Type **OUT_ARRAY2, SpiceInt *SIZE1, SpiceInt *SIZE2),
    (SpiceInt *SIZE1, SpiceInt *SIZE2, Type **OUT_ARRAY2)
{
//      $1_type $1_name, $2_type $2_name, $3_type $3_name
//      (Type **OUT_ARRAY2, SpiceInt *SIZE1, SpiceInt *SIZE2)
//      (SpiceInt *SIZE1, SpiceInt *SIZE2, Type **OUT_ARRAY2)

    TEST_MALLOC_FAILURE(buffer$argnum);
    npy_intp dims[2] = {dimsize$argnum[0], dimsize$argnum[1]};
    pyarr$argnum = (PyArrayObject *) create_array_with_owned_data(2, dims, Typecode,  (void **)&buffer$argnum);
    TEST_MALLOC_FAILURE(pyarr$argnum);

    $result = SWIG_Python_AppendOutput($result, (PyObject *) pyarr$argnum);
    // AppendOutput steals the reference to the argument.
    pyarr$argnum = NULL;
}

%typemap(argout)
    (Type **OUT_ARRAY12, SpiceInt *SIZE1, SpiceInt *SIZE2)
{
//      (Type **OUT_ARRAY12, SpiceInt *SIZE1, SpiceInt *SIZE2)

    TEST_MALLOC_FAILURE(buffer$argnum);
    npy_intp dims[2] = {dimsize$argnum[0], dimsize$argnum[1]};
    int nd = (dims[0] == 0) ? 1 : 2;
    pyarr$argnum = create_array_with_owned_data(nd, &dims[2 - nd], Typecode,  (void **)&buffer$argnum);
    TEST_MALLOC_FAILURE(pyarr$argnum);

    $result = SWIG_Python_AppendOutput($result, (PyObject *) pyarr$argnum);
    // AppendOutput steals the reference to the argument.
    pyarr$argnum = NULL;
}

%typemap(freearg)
        (Type **OUT_ARRAY2, SpiceInt *SIZE1, SpiceInt *SIZE2),
        (Type **OUT_ARRAY12, SpiceInt *SIZE1, SpiceInt *SIZE2),
        (SpiceInt *SIZE1, SpiceInt *SIZE2, Type **OUT_ARRAY2)
{
    Py_XDECREF(pyarr$argnum);
    PyMem_Free((void *) buffer$argnum);
}

/*******************************************************
* Now define these typemaps for every numeric type
*******************************************************/

%enddef

TYPEMAP_ARGOUT(SpiceInt,      NPY_INT   )
TYPEMAP_ARGOUT(SpiceBoolean,  NPY_INT   )
TYPEMAP_ARGOUT(SpiceDouble,   NPY_DOUBLE)

#undef TYPEMAP_ARGOUT

/*******************************************************************************
* Basic 3-D numeric typemaps for output
*       (type **OUT_ARRAY23, SpiceInt *SIZE1, SpiceInt *SIZE2, SpiceInt *SIZE3)
* We only have a few left over from vectors.
*******************************************************************************/

%define TYPEMAP_ARGOUT(Type, Typecode) // Use to fill in numeric types below!

/***************************************************************
* (Type **OUT_ARRAY23, SpiceInt *SIZE1, SpiceInt *SIZE2, SpiceInt *SIZE3)
***************************************************************/

%typemap(in, numinputs=0)
    (Type **OUT_ARRAY23, SpiceInt *SIZE1, SpiceInt *SIZE2, SpiceInt *SIZE3)
        (PyArrayObject* pyarr=NULL, Type *buffer=NULL, SpiceInt dimsize[3]),
    (Type **OUT_ARRAY23, SpiceInt *SIZE1, SpiceInt *SIZE2, SpiceInt *SIZE3)
        (PyArrayObject* pyarr=NULL, Type *buffer=NULL, SpiceInt dimsize[3])
{
//      $1_type $1_name, $2_type $2_name, $3_type $3_name, $4_type $4_name
//      (Type **OUT_ARRAY23, SpiceInt *SIZE1, SpiceInt *SIZE2, SpiceInt *SIZE3)

    $1 = &buffer;                                               // ARRAY
    $2 = &dimsize[0];                                           // SIZE1
    $3 = &dimsize[1];                                           // SIZE2
    $4 = &dimsize[2];                                           // SIZE3
}

/*******************************************************
* %typemap(argout)
* %typemap(freearg)
*******************************************************/

%typemap(argout)
    (Type **OUT_ARRAY23, SpiceInt *SIZE1, SpiceInt *SIZE2, SpiceInt *SIZE3)
{
//      (Type **OUT_ARRAY23, SpiceInt *SIZE1, SpiceInt *SIZE2, SpiceInt *SIZE3)

    TEST_MALLOC_FAILURE(buffer$argnum);
    npy_intp dims[3] = {dimsize$argnum[0], dimsize$argnum[1], dimsize$argnum[2]};
    int nd = dims[0] == 0 ? 2 : 3;
    pyarr$argnum = create_array_with_owned_data(nd, &dims[3 - nd], Typecode,  (void **)&buffer$argnum);
    TEST_MALLOC_FAILURE(pyarr$argnum);

    $result = SWIG_Python_AppendOutput($result, (PyObject *)pyarr$argnum);
    // AppendOutput steals the reference to the argument.
    pyarr$argnum = NULL;
}

%typemap(freearg)
    (Type **OUT_ARRAY23, SpiceInt *SIZE1, SpiceInt *SIZE2, SpiceInt *SIZE3),
    (Type **OUT_ARRAY23, SpiceInt *SIZE1, SpiceInt *SIZE2, SpiceInt *SIZE3)
{
    Py_XDECREF(pyarr$argnum);
    PyMem_Free((void *) buffer$argnum);
}

/*******************************************************
* Now define these typemaps for every numeric type
*******************************************************/

%enddef

TYPEMAP_ARGOUT(SpiceDouble, NPY_DOUBLE)

#undef TYPEMAP_ARGOUT

/*******************************************************************************
* Basic INOUT typemaps for 1- and 2-dimensional arrays:
*    (SpiceInt DIM1, Type *INOUT_ARRAY1)
*    (SpiceInt DIM1, Type INOUT_ARRAY2[][ANY])
*
* We make a new Numpy array out of the contents passed to us (which may or may not
* be a Numpy array) and pass it to the function.  The new array is returned to the user.
*******************************************************************************/

%define TYPEMAP_INOUT(Type, Typecode)
/*******************************************************
* (Type *INOUT_ARRAY1)
*******************************************************/

%typemap(in)
    (Type *INOUT_ARRAY1)
        (PyArrayObject* pyarr=NULL)
{
//      $1_type $1_name
//      (Type *INOUT_ARRAY1)
    CONVERT_TO_CONTIGUOUS_ARRAY_WRITEABLE_COPY(Typecode, $input, 1, 1, pyarr)
    $1 = ($1_ltype) PyArray_DATA(pyarr);                        // ARRAY
}

%typemap(in)
    (SpiceInt DIM1, Type *INOUT_ARRAY1)
        (PyArrayObject* pyarr=NULL),
    (SpiceInt DIM1, Type INOUT_ARRAY1[])
        (PyArrayObject* pyarr=NULL)
{
//      $1_type $1_name, $2_type $2_name
//      (SpiceInt DIM1, Type *INOUT_ARRAY1)
//  NOT CURRENTLY USED BY CSPICE

    CONVERT_TO_CONTIGUOUS_ARRAY_WRITEABLE_COPY(Typecode, $input, 1, 1, pyarr)
    $2 = ($2_ltype) PyArray_DATA(pyarr);                        // ARRAY
    $1 = (SpiceInt) PyArray_DIM(pyarr, 0);                      // DIM1
}

%typemap(argout)
    (Type *INOUT_ARRAY1),
    (SpiceInt DIM1, Type *INOUT_ARRAY1),
    (SpiceInt DIM1, Type INOUT_ARRAY1[])
    (SpiceInt DIM1, Type INOUT_ARRAY2[][ANY])
{
    $result = SWIG_Python_AppendOutput($result, (PyObject *)pyarr$argnum);
    pyarr$argnum = NULL;
}

%typemap(freearg)
    (Type *INOUT_ARRAY1),
    (SpiceInt DIM1, Type *INOUT_ARRAY1),
    (SpiceInt DIM1, Type INOUT_ARRAY1[])
{
    Py_XDECREF(pyarr$argnum);
}

%enddef

// Define concrete examples of the TYPEMAP_INOUT macros
TYPEMAP_INOUT(SpiceChar,     NPY_STRING)
TYPEMAP_INOUT(SpiceInt,      NPY_INT   )
TYPEMAP_INOUT(SpiceBoolean,  NPY_INT   )
TYPEMAP_INOUT(SpiceDouble,   NPY_DOUBLE)

#undef TYPEMAP_INOUT


/*******************************************************************************
* Typemap for string input
*
* These typemaps handle string input.
*
*       (SpiceChar *IN_STRING)
*       (SpiceChar *CONST_STRING)
*       (SpiceChar IN_STRING)
*
* The differences between the options are:
*
*       (SpiceChar *IN_STRING): The string is taken as input. It is copied to ensure
*               that the Python string remains immutable.
*
*       (SpiceChar *CONST_STRING): The string is taken as input. It is not copied so
*               one must ensure that it does not get changed by the C function.
*
*       (SpiceChar IN_STRING): If the C function accepts a single SpiceChar, not a
*               pointer to a string, any you wish to provide the Python input
*               as a string.
*******************************************************************************/

%define TYPEMAP_IN(Type) // Use to fill in types below

/***********************************************
* (SpiceChar *CONST_STRING)
***********************************************/

%typemap(in) (Type *CONST_STRING) (PyObject* byte_string = NULL) {
//      $1_type $1_name
//      (Type *CONST_STRING)

    TEST_IS_STRING($input);
    byte_string = PyUnicode_AsUTF8String($input);
    TEST_MALLOC_FAILURE(byte_string);

    $1 = PyBytes_AS_STRING(byte_string);
}

%typemap(argout) (Type *CONST_STRING) ""

%typemap(freearg) (Type *CONST_STRING) {
    Py_XDECREF(byte_string$argnum);
}

/***********************************************
* (SpiceChar IN_STRING)
***********************************************/

%typemap(in) (Type IN_STRING) {
//      $1_type $1_name
//      (Type IN_STRING)
    TEST_IS_STRING($input);
    SpiceInt error  = SWIG_AsVal_char($input, &$1);
    RAISE_BAD_TYPE_ON_ERROR(error, "Character");
 }

%typemap(argout)
    (Type IN_STRING) ""

%typemap(freearg)
    (Type IN_STRING) ""

/*******************************************************
* Now apply to all data types
*******************************************************/

%enddef

// Define concrete examples of the TYPEMAP_IN macros

TYPEMAP_IN(SpiceChar)
TYPEMAP_IN(ConstSpiceChar)

#undef TYPEMAP_IN

/*******************************************************************************
* String typemaps for input and output
*
* These typemaps allow C-format strings to be passed to the C function and for
* a string value to be returned.
*
*       (SpiceChar INOUT_STRING[ANY])
*       (SpiceChar *INOUT_STRING)
*
*       (SpiceInt DIM1, SpiceChar INOUT_STRING[ANY])
*       (SpiceInt DIM1, SpiceChar *INOUT_STRING)
*
*       (SpiceChar INOUT_STRING[ANY], SpiceInt DIM1)
*       (SpiceChar *INOUT_STRING, SpiceInt DIM1)
*
* The differences between the options are:
*
*       (SpiceChar *INOUT_STRING): The string is taken as input. A buffer of the
*               size is used to construct the returned string.
*
*       (SpiceChar INOUT_STRING[ANY]): The string is taken as input. A buffer of the
*               size specified in braces is used to construct the output.
*
* The integer DIM1 parameter carries the dimensioned length of the string.
*******************************************************************************/

/*******************************************************************************
* String typemaps for output
*
* These typemaps allow C-format strings to be returned by the C program as
* Python string values. They are part of the Python return value and do not
* appear as arguments when the function is called from Python.
*
*       (SpiceChar OUT_STRING[ANY])
*       (SpiceChar OUT_STRING[ANY], SpiceInt DIM1)
*       (SpiceInt DIM1, SpiceChar OUT_STRING[ANY])
*
* In each case, the dimensioned length of the string is defined in the SWIG
* interface by a number inside the brackets. The differences between the three
* options are:
*
*       (SpiceChar OUT_STRING[ANY]): one argument to the C function of type SpiceChar*
*               is consumed; no information about the string's dimensioned
*               length is passed to the function.
*
*       ((SpiceChar OUT_STRING[ANY], SpiceInt DIM1): two arguments to the C function are
*               consumed; the dimensioned length of the the SpiceChar string
*               (which is one greater than the maximum allowed string length)
*               is passed as the next argument after the SpiceChar* pointer.
*
*       ((SpiceInt DIM1, SpiceChar OUT_STRING[ANY]): two arguments to the C function are
*               consumed; the dimensioned length of the the character string is
*               passed as the argument before the char* pointer.
*
* Example:
*
* The C source code:
*
*       void yesno(SpiceInt status, SpiceChar *str, SpiceInt lstr) {
*           if (status) {
*               strncpy(str, "yes", lstr);
*           } else {
*               strncpy(str, "no", lstr);
*           }
*       }
*
* In the interface file:
*
*       %apply (SpiceChar OUT_STRING[ANY], SpiceInt LEN) {(SpiceChar str[4], SpiceInt lstr)};
*       extern void yesno(SpiceInt status, SpiceChar str[4], SpiceInt lstr);
*
* In Python:
*
*       >>> yesno(3)
*       'yes'
*       >>> yesno(0)
*       'no'
*******************************************************************************/

%{

char *byte_string_to_buffer_minimum_size(
    PyObject* byte_string, size_t needed_size, size_t *out_size) {

    size_t actual_size = PyBytes_GET_SIZE(byte_string);
    needed_size = max(needed_size, actual_size + 1);

    char *buffer = PyMem_Malloc(needed_size + 1);
    memcpy(buffer, PyBytes_AS_STRING(byte_string), actual_size);
    buffer[actual_size] = 0;
    *out_size = needed_size;
    return buffer;
}

%}


%define TYPEMAP_INOUT_OUT(Type) // Use to fill in types below

/***********************************************
* (SpiceChar INOUT_STRING[ANY])
***********************************************/

%typemap(in)
    (Type INOUT_STRING[ANY])                                    // PATTERN
        (char *buffer = NULL, size_t dim1 = 0, PyObject *byte_string = NULL)
{
//      $1_type $1_name
//      (Type INOUT_STRING[ANY])
//  NOT CURRENTLY USED BY CSPICE

    TEST_IS_STRING($input);
    byte_string = PyUnicode_AsUTF8String($input);
    TEST_MALLOC_FAILURE(byte_string);

    buffer = byte_string_to_buffer_minimum_size(byte_string, $1_dim0, &dim1);
    TEST_MALLOC_FAILURE(buffer);

    $1 = ($1_ltype)buffer;                                      // STRING
}

/***********************************************
* (SpiceChar INOUT_STRING[ANY], SpiceInt DIM1)
***********************************************/

%typemap(in)
    (Type INOUT_STRING[ANY], SpiceInt DIM1)                     // PATTERN
        (char *buffer = NULL, size_t dim1 = 0, PyObject *byte_string = NULL)
{
//      $1_type $1_name, $2_type $2_name
//      (SpiceChar INOUT_STRING[ANY], SpiceInt DIM1)
//  NOT CURRENTLY USED BY CSPICE

    TEST_IS_STRING($input);
    byte_string = PyUnicode_AsUTF8String($input);
    TEST_MALLOC_FAILURE(byte_string);

    buffer = byte_string_to_buffer_minimum_size(byte_string, $1_dim0, &dim1);
    TEST_MALLOC_FAILURE(buffer);

    $1 = buffer;                                                // STRING
    $2 = ($2_type)dim1;                                         // DIM1
}

/***********************************************
* (SpiceInt DIM1, SpiceChar INOUT_STRING[ANY])
***********************************************/

%typemap(in)
    (SpiceInt DIM1, Type INOUT_STRING[ANY])                     // PATTERN
        (char *buffer = NULL, size_t dim1 = 0, PyObject *byte_string = NULL)
{
//      $1_type $1_name, $2_type $2_name
//      (SpiceInt DIM1, SpiceChar INOUT_STRING[ANY])

    TEST_IS_STRING($input);
    byte_string = PyUnicode_AsUTF8String($input);
    TEST_MALLOC_FAILURE(byte_string);

    buffer = byte_string_to_buffer_minimum_size(byte_string, $2_dim0, &dim1);
    TEST_MALLOC_FAILURE(buffer);

    $1 = ($1_type)dim1;                                         // DIM1
    $2 = buffer;                                                // STRING
}

/***********************************************
* (SpiceInt DIM1, SpiceChar *INOUT_STRING)
***********************************************/

%typemap(in)
    (SpiceInt DIM1, Type *INOUT_STRING)                         // PATTERN
        (char *buffer = NULL, size_t dim1 = 0, PyObject *byte_string = NULL)
{
//      $1_type $1_name, $2_type $2_name
//      (SpiceInt DIM1, SpiceChar *INOUT_STRING)

    TEST_IS_STRING($input);
    byte_string = PyUnicode_AsUTF8String($input);
    TEST_MALLOC_FAILURE(byte_string);

    buffer = byte_string_to_buffer_minimum_size(byte_string, 0, &dim1);
    TEST_MALLOC_FAILURE(buffer);

    $2 = buffer;                                                // STRING
    $1 = ($1_type) dim1;                                        // DIM1
}

/*******************************************************
* %typemap(argout)
* %typemap(freearg)
*******************************************************/

%typemap(argout)
    (Type INOUT_STRING[ANY]),
    (Type INOUT_STRING[ANY], SpiceInt DIM1),
    (SpiceInt DIM1, Type INOUT_STRING[ANY]),
    (Type *INOUT_STRING),
    (Type *INOUT_STRING, SpiceInt DIM1),
    (SpiceInt DIM1, Type *INOUT_STRING)
{
    buffer$argnum[dim1$argnum-1] = '\0';  // Make sure string is terminated
    PyObject *obj = PyUnicode_FromString((Type *) buffer$argnum);
    $result = SWIG_Python_AppendOutput($result, obj);
}

%typemap(freearg)
    (Type INOUT_STRING[ANY]),
    (Type INOUT_STRING[ANY], SpiceInt DIM1),
    (SpiceInt DIM1, Type INOUT_STRING[ANY]),
    (Type *INOUT_STRING),
    (Type *INOUT_STRING, SpiceInt DIM1),
    (SpiceInt DIM1, Type *INOUT_STRING)
{
    PyMem_Free(buffer$argnum);
    Py_XDECREF(byte_string$argnum);
}

/***********************************************
* (SpiceChar OUT_STRING[ANY])
***********************************************/

%typemap(in, numinputs=0)
    (Type OUT_STRING[ANY])                                      // PATTERN
        (Type *buffer = NULL, size_t dim1)
{
//      $1_type $1_name
//      (SpiceChar OUT_STRING[ANY])

    dim1 = max(1, $1_dim0);
    buffer = (char *) PyMem_Malloc((dim1 + 1) * sizeof(Type));
    TEST_MALLOC_FAILURE(buffer);

    buffer[0] = '\0';   // String begins empty
    $1 = buffer;                                                // STRING
}

/***********************************************
* (SpiceInt DIM1, SpiceChar OUT_STRING[ANY])
***********************************************/

%typemap(in, numinputs=0)
    (SpiceInt DIM1, Type OUT_STRING[ANY])                       // PATTERN
        (Type *buffer = NULL, size_t dim1)
{
//      $1_type $1_name, $2_type $2_name
//      (SpiceInt DIM1, SpiceChar OUT_STRING[ANY])

    dim1 = max(1, $2_dim0);
    buffer = (Type *) PyMem_Malloc((dim1 + 1) * sizeof(Type));
    TEST_MALLOC_FAILURE(buffer);

    buffer[0] = '\0';   // String begins empty
    $2 = buffer;                                                // STRING
    $1 = ($1_type)dim1;                                         // DIM1
}

%typemap(in, numinputs=0)
    (Type OUT_STRING[ANY], SpiceInt *SIZE1)                      // PATTERN
        (Type *buffer = NULL, SpiceInt size1),
    (Type OUT_STRING[ANY], SpiceInt *SIZE1)                      // PATTERN
        (Type *buffer = NULL, SpiceInt size1)
{
//      $1_type $1_name, $2_type $2_name
//    (Type OUT_STRING[ANY], SpiceInt *SIZE1)                    // PATTERN

    size_t dim1 = max(1, $1_dim0);
    buffer = ($1_ltype) PyMem_Malloc((dim1 + 1) * sizeof(Type));
    TEST_MALLOC_FAILURE(buffer);

    buffer[0] = '\0';   // String begins empty
    $1 = buffer;                                                // STRING
    $2 = &size1;                                                 // DIM1
}

/*******************************************************
* %typemap(argout)
* %typemap(freearg)
*******************************************************/

%typemap(argout)
    (Type OUT_STRING[ANY]),
    (Type OUT_STRING[ANY], SpiceInt DIM1),
    (SpiceInt DIM1, Type OUT_STRING[ANY])
{
    buffer$argnum[dim1$argnum-1] = '\0';  // Make sure string is terminated
    PyObject *obj = PyUnicode_FromString((Type *) buffer$argnum);
    $result = SWIG_Python_AppendOutput($result, obj);
}

%typemap(argout)
    (Type OUT_STRING[ANY], SpiceInt *SIZE1)
{
    PyObject *obj = PyUnicode_FromStringAndSize((Type *) buffer$argnum, size1$argnum);
    $result = SWIG_Python_AppendOutput($result, obj);
}

%typemap(freearg)
    (Type OUT_STRING[ANY]),
    (Type OUT_STRING[ANY], SpiceInt DIM1),
    (SpiceInt DIM1, Type OUT_STRING[ANY]),
    (Type OUT_STRING[ANY], SpiceInt *SIZE1)
{
    PyMem_Free(buffer$argnum);
}



/*******************************************************
* Now apply to all data types
*******************************************************/

%enddef

// Define concrete examples of the  MAP_IN macros
TYPEMAP_INOUT_OUT(SpiceChar)

#undef TYPEMAP_INOUT_OUT

/*******************************************************************************
* String array typemaps for input
*
* These typemaps allow C-format string arrays to be passed into the C function.
*
*       (SpiceChar *IN_STRINGS, SpiceInt DIM1, SpiceInt DIM2)
*       (SpiceInt DIM1, SpiceInt DIM2, SpiceChar *IN_STRINGS)
*       (SpiceInt DIM1, SpiceInt DIM2, Type *INOUT_STRINGS)
*
* In all cases, the Strings are copied to an n x m array where n is the number
* of strings and m is longer than the longest string.
* For INOUT_STRINGS, the resulting buffer is converted back into an array of strings
* and returned to the user as a result.
*******************************************************************************/


%define TYPEMAP_IN(Type) // Use to fill in types below

/***********************************************************************
* (Type *IN_STRINGS, SpiceInt DIM1, SpiceInt DIM2)
***********************************************************************/

%typemap(in)
    (Type *IN_STRINGS, SpiceInt DIM1, SpiceInt DIM2)
        (PyObject *list = NULL, char *buffer = NULL)
{
//      $1_type $1_name, $2_type $2_name, $3_type $3_name
//      (Type *IN_STRINGS, SpiceInt DIM1, SpiceInt DIM2)

    HANDLE_TYPEMAP_IN_STRINGS($1, $*1_type, $2, $3, buffer, list)
}

/***********************************************************************
* (SpiceInt DIM1, SpiceInt DIM2, Type *IN_STRINGS)
***********************************************************************/

%typemap(in)
    (SpiceInt DIM1, SpiceInt DIM2, Type *IN_STRINGS)
        (PyObject *list = NULL, char *buffer = NULL),
    (SpiceInt DIM1, SpiceInt DIM2, Type *INOUT_STRINGS)
        (PyObject *list = NULL, char *buffer = NULL)
{
//      $1_type $1_name, $2_type $2_name, $3_type $3_name
//      (SpiceInt DIM1, SpiceInt DIM2, Type *IN[OUT]_STRINGS)

    HANDLE_TYPEMAP_IN_STRINGS($3, $*3_type, $1, $2, buffer, list)
}

/***********************************************************************
* %typemap(argout)
* %typemap(freearg)
***********************************************************************/
%typemap(argout)
    (Type *IN_STRINGS, SpiceInt DIM1, SpiceInt DIM2),
    (SpiceInt DIM1, SpiceInt DIM2, Type *IN_STRINGS)
""

%typemap(argout)
    (SpiceInt DIM1, SpiceInt DIM2, Type *INOUT_STRINGS)
{
//      (SpiceInt DIM1, SpiceInt DIM2, Type *INOUT_STRINGS)
    // We can reuse list$argnum, but first we need to free whatever is there.
    Py_XDECREF(list$argnum);
    list$argnum = NULL;
    CONVERT_BUFFER_TO_ARRAY_OF_STRINGS(buffer$argnum, $1, $2, list$argnum);
    $result = SWIG_Python_AppendOutput($result, list$argnum);
    list$argnum = NULL;
}

%typemap(freearg)
    (Type *IN_STRINGS, SpiceInt DIM1, SpiceInt DIM2),
    (SpiceInt DIM1, SpiceInt DIM2, Type *IN_STRINGS),
    (SpiceInt DIM1, SpiceInt DIM2, Type *INOUT_STRINGS)
{
    Py_XDECREF(list$argnum);
    PyMem_Free((void *) buffer$argnum);
}

/*******************************************************
* Now apply to all data types
*******************************************************/

%enddef

// Define concrete examples of the TYPEMAP_IN macros
TYPEMAP_IN(SpiceChar)
TYPEMAP_IN(ConstSpiceChar)

#undef TYPEMAP_IN

/*******************************************************************************
* String array typemaps for output
*
* These typemaps allow C-format string arrays to be returned by the program as
* a list of Python string values. They are part of the return value and do not
* appear as arguments to the Python function.
*
*       (SpiceChar OUT_STRINGS[ANY][ANY], SpiceInt DIM1, SpiceInt DIM1, SpiceInt *NSTRINGS)
*       (SpiceInt DIM1, SpiceInt DIM2, SpiceInt *NSTRINGS, SpiceChar OUT_STRINGS[ANY][ANY])
*
* As above, the maximum size and number of strings must be defined in the SWIG
* interface file (to ensure adequate memory is allocated). The typemaps could
* easily be written for alternative orderings of the arguments or for cases
* where one or more arguments are missing.
*
* There are so many possibilities here that we are just going to create them on
* demand as needed.
*******************************************************************************/

%define HANDLE_OUT_STRINGS_ANY_ANY(Type, dim0, dim1)
    nstrings = 0;
    dimsize[0] = dim0;                                       // ARRAY_dim0
    dimsize[1] = dim1;                                       // ARRAY_dim1
    if (dimsize[1] < 2) {
        dimsize[1] = 2;
    }
    buffer = (Type *) PyMem_Malloc(dimsize[0] * dimsize[1] * sizeof(Type));
    TEST_MALLOC_FAILURE(buffer);
%enddef

%define TYPEMAP_OUT(Type) // Use to fill in types below

/***********************************************************************
* (SpiceInt DIM1, SpiceInt DIM2, SpiceInt *NSTRINGS, SpiceChar OUT_STRINGS[ANY][ANY])
***********************************************************************/

%typemap(in,numinputs=0)
    (Type OUT_STRINGS[ANY][ANY], SpiceInt *NSTRINGS)
        (Type *buffer = NULL, SpiceInt dimsize[2], SpiceInt nstrings, PyObject* list = NULL)
{
//      $1_type $1_name, $2_type $2_name

    HANDLE_OUT_STRINGS_ANY_ANY(Type, $1_dim0, $1_dim1)
    $1 = ($1_ltype) buffer;                                     // ARRAY
    $2 = &nstrings;                                             // NSTRINGS
}

%typemap(in,numinputs=0)
    (SpiceInt DIM1, SpiceInt DIM2, SpiceInt *NSTRINGS, Type OUT_STRINGS[ANY][ANY])
        (Type *buffer = NULL, SpiceInt dimsize[2], SpiceInt nstrings, PyObject* list = NULL)
{
//      $1_type $1_name, $2_type $2_name, $3_type $3_name, $4_type $4_name
//      (SpiceInt DIM1, SpiceInt DIM2, SpiceInt *NSTRINGS, Type OUT_STRINGS[ANY][ANY])

    HANDLE_OUT_STRINGS_ANY_ANY(Type, $4_dim0, $4_dim1)
    $4 = ($4_ltype) buffer;                                     // ARRAY
    $1 = dimsize[0];                                            // DIM1
    $2 = dimsize[1];                                            // DIM2
    $3 = &nstrings;                                             // NSTRINGS
}

%typemap(in,numinputs=0)
    (SpiceInt DIM2, SpiceInt *NSTRINGS, Type OUT_STRINGS[ANY][ANY])
        (Type *buffer = NULL, SpiceInt dimsize[2], SpiceInt nstrings, PyObject* list = NULL)
{
//      $1_type $1_name, $2_type $2_name, $3_type $3_name
//      (SpiceInt DIM2, SpiceInt *NSTRINGS, Type OUT_STRINGS[ANY][ANY])

    HANDLE_OUT_STRINGS_ANY_ANY(Type, $3_dim0, $3_dim1)
    $3 = ($3_ltype) buffer;                                     // ARRAY
    $1 = dimsize[1];                                            // DIM2
    $2 = &nstrings;                                             // NSTRINGS
}

%typemap(argout)
    (Type OUT_STRINGS[ANY][ANY], SpiceInt *NSTRINGS),
    (SpiceInt DIM1, SpiceInt DIM2, SpiceInt *NSTRINGS, Type OUT_STRINGS[ANY][ANY]),
    (SpiceInt DIM2, SpiceInt *NSTRINGS, Type OUT_STRINGS[ANY][ANY])
{
    CONVERT_BUFFER_TO_ARRAY_OF_STRINGS(buffer$argnum, nstrings$argnum, dimsize$argnum[1], list$argnum)
    $result = SWIG_Python_AppendOutput($result, list$argnum);
    list$argnum = NULL;
}

%typemap(freearg)
    (Type OUT_STRINGS[ANY][ANY], SpiceInt *NSTRINGS),
    (SpiceInt DIM1, SpiceInt DIM2, SpiceInt *NSTRINGS, Type OUT_STRINGS[ANY][ANY]),
    (SpiceInt DIM2, SpiceInt *NSTRINGS, Type OUT_STRINGS[ANY][ANY])
{
    PyMem_Free((void *) buffer$argnum);
    Py_XDECREF(list$argnum);
}

/*******************************************************
* Now apply to all data types
*******************************************************/

%enddef

// Define concrete examples of the TYPEMAP_IN macros
TYPEMAP_OUT(SpiceChar)

#undef TYPEMAP_OUT

/*******************************************************************************
* Typemaps for records.
*
* These typemaps are for data-structures in which the user wants to see a record
* with named fields.  The only forms that exist are:
*
*     (ConstType *INPUT)
*     (Type *INPUT)      // Not currently used, but just in case
*     (Type *OUTPUT)
*
* Any type used here must have a descriptor added in record_support.py
*******************************************************************************/

%define TYPEMAP_RECORDS(ConstType, Type)

%typemap(in)
    (ConstType *INPUT)
        (PyObject *record = NULL),
    (Type *INPUT)
        (PyObject *record = NULL)
{
//      $1_type $1_name
//      $1_type *INPUT
    record = PyObject_CallMethod(SWIG_CALLBACK_CLASS , "as_record", "sO", "Type", $input);
    if (!record || record == Py_None) {
        handle_bad_type_error("$symname", "Type");
        SWIG_fail;
    }
    $1 = get_arraylike_object_data(record);
}

%typemap(in, numinputs=0)
    (Type *OUTPUT)
        (PyObject *record = NULL)
{
//      $1_type $1_name
//      Type *OUTPUT
    record = PyObject_CallMethod(SWIG_CALLBACK_CLASS , "create_record", "s", "Type");
    TEST_MALLOC_FAILURE(record);
    $1 = get_arraylike_object_data(record);
}

%typemap(argout)
    (Type *OUTPUT)
%{
    $result = SWIG_Python_AppendOutput($result, record$argnum);
    record$argnum = NULL;
%}

%typemap(freearg)
    (ConstType *INPUT),
    (Type *INPUT),
    (Type *OUTPUT)
%{
    Py_XDECREF(record$argnum);
%}


%enddef

// If you add a new type here, then also add it to record_support.py
TYPEMAP_RECORDS(ConstSpiceDLADescr, SpiceDLADescr)
TYPEMAP_RECORDS(ConstSpiceDSKDescr, SpiceDSKDescr)

#undef TYPEMAP_RECORDS


/******************************
* Typemaps for records that we prefer to implement as Numpy arrays.
*
* These typemaps are for data-structures in which the interface with the user is just
* a plane numpy array.  However we can do better typechecking in the .i files by using
* the actual type name.
*
*     (ConstType *INPUT)
*     (Type *INPUT)      // Not currently used, but just in case
*     (Type *OUTPUT)
*
*/

%define TYPEMAP_RECORDS_ALIAS(ConstType, Type, Typecode, size)

%typemap(in)
    (ConstType *INPUT)
        (PyArrayObject *pyarr=NULL),
    (Type *INPUT)
        (PyArrayObject *pyarr=NULL)
{
//      $1_type $1_name
//      $1_type *INPUT

    CONVERT_TO_CONTIGUOUS_ARRAY(Typecode, $input, 1, 1, pyarr)
    TEST_INVALID_ARRAY_SHAPE_1D(pyarr, size);
    $1 = ($1_ltype) PyArray_DATA(pyarr);                        // ARRAY
}

%typemap(in, numinputs=0)
    (Type *OUTPUT)                                              // PATTERN
        (PyArrayObject *pyarr = NULL)
{
//      $1_type $1_name
//      Type *OUTPUT

    npy_intp dims = size;                                       // DIMENSIONS
    pyarr = (PyArrayObject *) PyArray_SimpleNew(1, &dims, Typecode);
    TEST_MALLOC_FAILURE(pyarr);

    $1 = ($1_ltype) PyArray_DATA(pyarr);                        // ARRAY
}

%typemap(argout)
    (Type *OUTPUT)
%{
    $result = SWIG_Python_AppendOutput($result, (PyObject *) pyarr$argnum);
    pyarr$argnum = NULL;
%}

%typemap(freearg)
   (ConstType *INPUT),
   (Type *INPUT),
   (Type *OUTPUT)
%{
    Py_XDECREF(pyarr$argnum);
%}

%enddef

TYPEMAP_RECORDS_ALIAS(ConstSpiceEllipse, SpiceEllipse, NPY_DOUBLE, 9)
TYPEMAP_RECORDS_ALIAS(ConstSpicePlane, SpicePlane, NPY_DOUBLE, 4)

#undef TYPEMAP_RECORDS_ALIAS

%{
typedef SpiceCell SpiceCellInt;
typedef SpiceCell SpiceCellDouble;
%}

/******************************
* Typemaps for records that we prefer to implement as Numpy arrays.
*
* These typemaps are for data-structures in which the interface with the user is just
* a plane numpy array.  However we can do better typechecking in the .i files by using
* the actual type name.
*
*     (ConstType *INPUT)
*     (Type *INPUT)      // Not currently used, but just in case
*     (Type *OUTPUT)
*
*/

%define TYPEMAP_SPICE_CELL(Type, TypeCode)
%typemap(in)
    (Type *INPUT)
        (PyObject *record = NULL),
    (Type *INOUT)
        (PyObject *record = NULL)
{
//      $1_type $1_name
//      $1_type *INPUT
    record = PyObject_CallMethod(SWIG_CALLBACK_CLASS , "as_spice_cell", "iO", TypeCode, $input);
    if (!record || record == Py_None) {
        handle_bad_type_error("$symname", "Type");
        SWIG_fail;
    }
    PyObject *header_address = PyObject_GetAttrString(record, "_header_address");
    $1 = PyLong_AsVoidPtr(header_address);
    Py_XDECREF(header_address);
}

%typemap(in, numinputs=0)
    (Type *OUTPUT)
        (PyObject *record = NULL)
{
//      $1_type $1_name
//      Type *OUTPUT
    record = PyObject_CallMethod(SWIG_CALLBACK_CLASS , "create_spice_cell", "i", TypeCode);
    TEST_MALLOC_FAILURE(record);

    PyObject *header_address = PyObject_GetAttrString(record, "_header_address");
    $1 = PyLong_AsVoidPtr(header_address);
    Py_XDECREF(header_address);
}

%typemap(argout)
    (Type *OUTPUT),
    (Type *INOUT)
%{
    $result = SWIG_Python_AppendOutput($result, record$argnum);
    record$argnum = NULL;
%}

%typemap(freearg)
    (Type *INPUT),
    (Type *INOUT),
    (Type *OUTPUT)
%{
    Py_XDECREF(record$argnum);
%}

%enddef

TYPEMAP_SPICE_CELL(SpiceCellInt,     SPICE_INT)
TYPEMAP_SPICE_CELL(SpiceCellDouble,  SPICE_DP)
TYPEMAP_SPICE_CELL(SpiceCellChar,    SPICE_CHR)

#undef TYPEMAP_SPICE_CELL


/*******************************************************************************
* Typemap for boolean output
*
*       (Type *OUTPUT)
*
* This typemap allows ints to be returned by the program as Python booleans.
* They are part of the return value and do not appear as arguments to the
* Python function. A zero value is False; anything else is True.
*******************************************************************************/

%define TYPEMAP_ARGOUT(Type, converter)

%typemap(in, numinputs=0)
    (Type *OUTPUT)
        (Type value = 0)
{
//      $1_type $1_name
//      (Type *OUTPUT)
    $1 = &value;
}

%typemap(argout)
    (Type *OUTPUT)
{
//      $1_type $1_name
//      (Type *OUTPUT)

    $result = SWIG_Python_AppendOutput($result, converter);
}

%typemap(freearg) (Type *OUTPUT) ""

%enddef

TYPEMAP_ARGOUT(SpiceBoolean, PyBool_FromLong(value$argnum))
TYPEMAP_ARGOUT(SpiceInt,     PyInt_FromLong(value$argnum))
TYPEMAP_ARGOUT(SpiceDouble,  PyFloat_FromDouble(value$argnum))
TYPEMAP_ARGOUT(SpiceChar,    PyUnicode_FromStringAndSize(&value$argnum, 1))
TYPEMAP_ARGOUT(PyObject*,    (value$argnum))

%typemap(freearg) (PyObject *OUTPUT)
%{
    Py_INCREF(value$argnum);
%}

#undef TYPEMAP_ARGOUT

/*******************************************************************************
* Typemap for return values. They also check for error status and raise a
* runtime exception if necessary.
*
*       (void   RETURN_VOID   )
*       (SpiceInt    RETURN_BOOLEAN)
*       (SpiceInt    RETURN_INT    )
*       (double RETURN_DOUBLE )
*       (SpiceChar  *RETURN_STRING )
*******************************************************************************/

%typemap(out) (void RETURN_VOID) {

    TEST_FOR_EXCEPTION;
    if (!$result) {
       Py_INCREF(Py_None);
       $result = Py_None;
    }
}

%typemap(out) (PyPointer* RETURN_OBJECT) {
    TEST_FOR_EXCEPTION;
    $result = SWIG_Python_AppendOutput($1);
}


%typemap(out)
    (SpiceInt RETURN_BOOLEAN),
    (SpiceBoolean RETURN_BOOLEAN) {

    TEST_FOR_EXCEPTION;
    $result = SWIG_Python_AppendOutput($result, PyBool_FromLong((long) $1));
}

%typemap(out)
    (SpiceInt RETURN_INT) {

    TEST_FOR_EXCEPTION;
    $result = SWIG_Python_AppendOutput($result, PyInt_FromLong((long) $1));
}

%typemap(out)
    (double RETURN_DOUBLE),
    (SpiceDouble RETURN_DOUBLE) {

    TEST_FOR_EXCEPTION;
    $result = SWIG_Python_AppendOutput($result, PyFloat_FromDouble((double) $1));
}

%typemap(out)
    (char *RETURN_STRING),
    (SpiceChar *RETURN_STRING) {

    TEST_FOR_EXCEPTION;
    $result = SWIG_Python_AppendOutput($result, PyUnicode_FromString((char *) $1));
}

%typemap(in)
    (ConstSpiceChar* CONST_FILENAME)
        (PyObject *byte_string = NULL)
{
//      $1_type $1_name
//      $1_type *CONST_FILENAME

    // Badly named function converts string/bytes/os.FilePath to bytes.
    int status = PyUnicode_FSConverter($input, &byte_string);
    if (status == 0) {
        handle_bad_type_error("$symname", "String, Byte String, or Path");
        SWIG_fail;
    }
    $1 = PyBytes_AsString(byte_string);
}

%typemap(freearg)
    (ConstSpiceChar* CONST_FILENAME)
{
    Py_XDECREF(byte_string$argnum);
}




/*******************************************************************************
*******************************************************************************/
#if 0
%typemap(in, numinputs=0)
    (SWIGTYPE*)
{
//      $1_type $1_name, $2_type $2_name, $3_type $3_name
     ERROR The argument "$1_type $1_name" in "$symname" didnt match any template!!
}
#endif
