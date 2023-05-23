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
    // Empty the traceback list
    int depth;
    trcdep_c(&depth);
    for (int k = depth-1; k >= 0; k--) {
        char module[100];
        trcnam_c(k, 100, module);
        chkout_c(module);
    }
}

void flush_traceback_to(char *name) {
    int depth;
    trcdep_c(&depth);
    for (int k = depth-1; k >= 0; k--) {
        char module[100];
        trcnam_c(k, 100, module);
        chkout_c(module);
        if (strcmp(module, name) == 0) return;
    }
}

void pop_traceback(void) {
    int depth;
    trcdep_c(&depth);
    if (depth) {
        char module[100];
        trcnam_c(depth-1, 100, module);
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

%define RAISE_SIGERR_EXCEPTION
{
    handle_sigerr_exception();
    SWIG_fail;
}
%enddef

%{
void handle_sigerr_exception(void) {
    // TODO(fy): Ask Mark why we can't use $symname
    int depth;
    char symname[100];

    trcdep_c(&depth);
    if (depth > 0) {
        trcnam_c(depth-1, 100, symname);
    } else {
        symname[0] = 0;
    }

    set_python_exception(symname);
    pop_traceback();
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
        handle_bad_string_error("$symname");
        SWIG_fail;
    }
}
%enddef

%define RAISE_BAD_STRING_ON_ERROR(error)
{
    if (!SWIG_IsOK(error)) {
        handle_bad_string_error("$symname");
        SWIG_fail;
    }
}
%enddef

%{
void handle_bad_string_error(const char* symname) {
    chkin_c(symname);
    setmsg_c("Expected String");
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
    if (typecode == NPY_INT && PyArray_Check(input) && PyArray_ISINTEGER(input)) {
        // We allow the conversion of all integer types to integer arrays.
        flags |= NPY_ARRAY_FORCECAST;
    }
    return PyArray_FROMANY(input, typecode, min, max, flags);
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
    result = PyList_New(rows);
    TEST_MALLOC_FAILURE(result);

    // Convert the results to Python strings and add them to the list
    for (int i = 0; i < rows; i++) {
        char *str = &buffer[i * columns];
        PyObject *value = PyString_FromString(str);
        TEST_MALLOC_FAILURE(value)
        PyList_SetItem(result, i, value);
    }
    result = Py_BuildValue("[N]", result);  // N steals the reference
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
    } else if (PyArray_NDIM(input) < min || PyArray_NDIM(input) > max) {
        if (min == max) {
            setmsg_c("Invalid array rank # in module #; # is required");
        } else {
            setmsg_c("Invalid array rank # in module #; # or # is required");
        }
        errint_c("#", (int) PyArray_NDIM(input));
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
        errch_c("#", typecode_string(PyArray_TYPE(input)));
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
    PyArrayObject* array = PyArray_SimpleNewFromData(nd, dims, typenum, *data);
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
%}

// Copy standard typemaps for Spice types
%apply int {SpiceInt, SpiceBoolean, ConstSpiceInt, ConstSpiceBoolean};
%apply char {SpiceChar, ConstSpiceChar}
%apply double {SpiceDouble, ConstSpiceDouble};
%apply float {SpiceFloat, ConstSpiceFloat};

%apply int *OUTPUT {SpiceInt *OUTPUT};
%apply char *OUTPUT {SpiceChar *OUTPUT}
%apply double *OUTPUT {SpiceDouble *OUTPUT};
%apply float *OUTPUT {SpiceFloat *OUTPUT};

/*******************************************************************************
* 1-D numeric typemaps for input
*
* This family of typemaps allows Python sequences and Numpy 1-D arrays to be
* read as arrays in C functions.
*
* If the size of the array is fixed and can be specified in the SWIG interface:
*       (type IN_ARRAY1[ANY])
*       (type IN_ARRAY1[ANY], int DIM1)
*       (int DIM1, type IN_ARRAY1[ANY])
* In these cases, an error condition will be raised if the dimension of the
* structure passed from Python does not match that specified in braces within
* the C function call.
*
* If the size of the array is defined by the Python structure:
*       (type *IN_ARRAY1, int DIM1)
*       (int DIM1, type *IN_ARRAY1)
* In these cases, there is no limit on the number of elements that can be passed
* to the C function. Internal memory is allocated as needed based on the size of
* the array passed from Python.
*
* If a scalar should be shaped into an array of shape (1,):
*       (type *IN_ARRAY01, int DIM1)
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
//      (Type IN_ARRAY1[ANY])
    CONVERT_TO_CONTIGUOUS_ARRAY(Typecode, $input, 1, 1, pyarr)
    TEST_INVALID_ARRAY_SHAPE_1D(pyarr, $1_dim0);

    $1 = ($1_ltype) PyArray_DATA(pyarr);                        // ARRAY
//  $2 = (int) PyArray_DIM(pyarr, 0);                           // DIM1
}

/*******************************************************
* (Type IN_ARRAY1[ANY], int DIM1)
*******************************************************/

%typemap(in)
    (Type IN_ARRAY1[ANY], int DIM1)                             // PATTERN
        (PyArrayObject* pyarr=NULL),
    (Type IN_ARRAY1[ANY], SpiceInt DIM1)                        // PATTERN
        (PyArrayObject* pyarr=NULL)
{
//      (Type IN_ARRAY1[ANY], int DIM1)
//  NOT CURRENTLY USED BY CSPICE

    CONVERT_TO_CONTIGUOUS_ARRAY(Typecode, $input, 1, 1, pyarr)
    TEST_INVALID_ARRAY_SHAPE_1D(pyarr, $1_dim0);

    $1 = ($1_ltype) PyArray_DATA(pyarr);                        // ARRAY
    $2 = (int) PyArray_DIM(pyarr, 0);                           // DIM1
}

/*******************************************************
* (int DIM1, Type IN_ARRAY1[ANY])
*******************************************************/

%typemap(in)
    (int DIM1, Type IN_ARRAY1[ANY])                             // PATTERN
        (PyArrayObject* pyarr=NULL),
    (SpiceInt DIM1, Type IN_ARRAY1[ANY])                        // PATTERN
        (PyArrayObject* pyarr=NULL)
{
//      (int DIM1, Type IN_ARRAY1[ANY])
//  NOT CURRENTLY USED BY CSPICE

    CONVERT_TO_CONTIGUOUS_ARRAY(Typecode, $input, 1, 1, pyarr)
    TEST_INVALID_ARRAY_SHAPE_1D(pyarr, $2_dim0);

    $2 = ($2_ltype) PyArray_DATA(pyarr);                        // ARRAY
    $1 = (int) PyArray_DIM(pyarr, 0);                           // DIM1
}

/*******************************************************
* (Type *IN_ARRAY1, int DIM1)
*******************************************************/

%typemap(in)
    (Type *IN_ARRAY1, int DIM1)                                 // PATTERN
        (PyArrayObject* pyarr=NULL),
    (Type *IN_ARRAY1, SpiceInt DIM1)                            // PATTERN
        (PyArrayObject* pyarr=NULL)
{
//      (Type *IN_ARRAY1, int DIM1)

    CONVERT_TO_CONTIGUOUS_ARRAY(Typecode, $input, 1, 1, pyarr)

    $1 = ($1_ltype) PyArray_DATA(pyarr);                        // ARRAY
    $2 = (int) PyArray_DIM(pyarr, 0);                           // DIM1
}

/*******************************************************
* (int DIM1, Type *IN_ARRAY1)
*******************************************************/

%typemap(in)
    (int DIM1, Type *IN_ARRAY1)                                 // PATTERN
        (PyArrayObject* pyarr=NULL),
    (SpiceInt DIM1, Type *IN_ARRAY1)                            // PATTERN
        (PyArrayObject* pyarr=NULL)
{
//      (int DIM1, Type *IN_ARRAY1)

    CONVERT_TO_CONTIGUOUS_ARRAY(Typecode, $input, 1, 1, pyarr)

    $2 = ($2_ltype) PyArray_DATA(pyarr);                        // ARRAY
    $1 = (int) PyArray_DIM(pyarr, 0);                           // DIM1
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
//      (Type *IN_ARRAY1)
//      (Type IN_ARRAY1[]

    CONVERT_TO_CONTIGUOUS_ARRAY(Typecode, $input, 1, 1, pyarr)

    $1 = ($1_ltype) PyArray_DATA(pyarr);                        // ARRAY
}

/*******************************************************
* (Type *IN_ARRAY01, int DIM1)
*******************************************************/

%typemap(in)
    (Type *IN_ARRAY01, int DIM1)                                // PATTERN
        (PyArrayObject* pyarr=NULL),
    (Type *IN_ARRAY01, SpiceInt DIM1)                           // PATTERN
        (PyArrayObject* pyarr=NULL)
{
//      (Type *IN_ARRAY01, int DIM1)


    CONVERT_TO_CONTIGUOUS_ARRAY(Typecode, $input, 0, 1, pyarr)

    $1 = ($1_ltype) PyArray_DATA(pyarr);                        // ARRAY
    if (PyArray_NDIM(pyarr) == 0) {
        $2 = 0;                                                 // DIM1
    } else {
        $2 = (int) PyArray_DIM(pyarr, 0);                       // DIM1
    }
}

/*******************************************************
* %typemap(argout)
* %typemap(freearg)
*******************************************************/

%typemap(argout)
    (Type IN_ARRAY1[ANY]),
    (Type IN_ARRAY1[ANY], int DIM1),
    (Type IN_ARRAY1[ANY], SpiceInt DIM1),
    (int DIM1, Type IN_ARRAY1[ANY]),
    (SpiceInt DIM1, Type IN_ARRAY1[ANY]),
    (Type *IN_ARRAY1, int DIM1),
    (Type *IN_ARRAY1, SpiceInt DIM1),
    (int DIM1, Type *IN_ARRAY1),
    (SpiceInt DIM1, Type *IN_ARRAY1),
    (Type *IN_ARRAY1),
    (Type IN_ARRAY1[]),
    (Type *IN_ARRAY01, int DIM1),
    (Type *IN_ARRAY01, SpiceInt DIM1)
 ""

%typemap(freearg)
    (Type IN_ARRAY1[ANY]),
    (Type IN_ARRAY1[ANY], int DIM1),
    (Type IN_ARRAY1[ANY], SpiceInt DIM1),
    (int DIM1, Type IN_ARRAY1[ANY]),
    (SpiceInt DIM1, Type IN_ARRAY1[ANY]),
    (Type *IN_ARRAY1, int DIM1),
    (Type *IN_ARRAY1, SpiceInt DIM1),
    (int DIM1, Type *IN_ARRAY1),
    (SpiceInt DIM1, Type *IN_ARRAY1),
    (Type *IN_ARRAY1),
    (Type IN_ARRAY1[]),
    (Type *IN_ARRAY01, int DIM1),
    (Type *IN_ARRAY01, SpiceInt DIM1)
{
//      (Type ...IN_ARRAY1[ANY]...)
    Py_XDECREF(pyarr$argnum);
}

/*******************************************************
* Now apply to all data types
*******************************************************/

%enddef

// Define concrete examples of the TYPEMAP_IN1 macros
TYPEMAP_IN(ConstSpiceChar,   NPY_STRING )
TYPEMAP_IN(int,              NPY_INT   )
TYPEMAP_IN(SpiceInt,         NPY_INT   )
TYPEMAP_IN(ConstSpiceInt,    NPY_INT   )
TYPEMAP_IN(SpiceBoolean,     NPY_INT   )
TYPEMAP_IN(ConstSpiceBoolean,NPY_INT   )
TYPEMAP_IN(long,             NPY_LONG  )
TYPEMAP_IN(double,           NPY_DOUBLE)
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
*       (type IN_ARRAY2[ANY][ANY], int DIM1, int DIM2)
*       (int DIM1, int DIM2, type IN_ARRAY2[ANY][ANY])
* In these cases, an error condition will be raised if the dimensions of the
* structure passed from Python do not match what was specified in braces within
* the C function call.
*
* If the size of the array is defined by the Python structure:
*       (type *IN_ARRAY2, int DIM1, int DIM2)
*       (int DIM1, int DIM2, type *IN_ARRAY2)
* In these cases, there is no limit on the number of elements that can be passed
* to the C function. Internal memory is allocated as needed based on the size of
* the array passed from Python.
*
* NEW variations...
*
* If the size of the last array axis is fixed and can be specified in the
* SWIG interface:
*       (type IN_ARRAY2[ANY][ANY], int DIM1)
*       (int DIM1, type IN_ARRAY2[ANY][ANY])
* In these cases, an error condition will be raised if the second dimension of
* the structure passed from Python does not match what was specified in braces
* within the C function call. The value of the first dimension is ignored and
* can be set to one.
*
* If the first dimension can be missing:
*       (type *IN_ARRAY12, int DIM1, int DIM2)
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
//      (Type IN_ARRAY2[ANY][ANY])

    CONVERT_TO_CONTIGUOUS_ARRAY(Typecode, $input, 2, 2, pyarr)
    TEST_INVALID_ARRAY_SHAPE_2D(pyarr, $1_dim0, $1_dim1);

    $1 = ($1_ltype) PyArray_DATA(pyarr);                        // ARRAY
//  $2 = (int) PyArray_DIM(pyarr, 0);                           // DIM1
//  $3 = (int) PyArray_DIM(pyarr, 1);                           // DIM2
}

/*******************************************************
* (Type IN_ARRAY2[ANY][ANY], int DIM1, int DIM2)
*******************************************************/

%typemap(in)
    (Type IN_ARRAY2[ANY][ANY], int DIM1, int DIM2)              // PATTERN
        (PyArrayObject* pyarr=NULL),
    (Type IN_ARRAY2[ANY][ANY], SpiceInt DIM1, SpiceInt DIM2)    // PATTERN
        (PyArrayObject* pyarr=NULL)
{
//      (Type IN_ARRAY2[ANY][ANY], int DIM1, int DIM2)
//  NOT CURRENTLY USED BY CSPICE

    CONVERT_TO_CONTIGUOUS_ARRAY(Typecode, $input, 2, 2, pyarr)
    TEST_INVALID_ARRAY_SHAPE_2D(pyarr, $1_dim0, $1_dim1);

    $1 = ($1_ltype) PyArray_DATA(pyarr);                        // ARRAY
    $2 = (int) PyArray_DIM(pyarr, 0);                           // DIM1
    $3 = (int) PyArray_DIM(pyarr, 1);                           // DIM2
}

/*******************************************************
* (int DIM1, int DIM2, Type IN_ARRAY2[ANY][ANY])
*******************************************************/

%typemap(in)
    (int DIM1, int DIM2, Type IN_ARRAY2[ANY][ANY])              // PATTERN
            (PyArrayObject* pyarr=NULL),
    (SpiceInt DIM1, SpiceInt DIM2, Type IN_ARRAY2[ANY][ANY])    // PATTERN
            (PyArrayObject* pyarr=NULL)
{
//      (int DIM1, int DIM2, Type IN_ARRAY2[ANY][ANY])
//   NOT CURRENTLY USED

    CONVERT_TO_CONTIGUOUS_ARRAY(Typecode, $input, 2, 2, pyarr)
    TEST_INVALID_ARRAY_SHAPE_2D(pyarr, $3_dim0, $3_dim1);

    $3 = ($3_ltype) PyArray_DATA(pyarr);                        // ARRAY
    $1 = (int) PyArray_DIM(pyarr, 0);                           // DIM1
    $2 = (int) PyArray_DIM(pyarr, 1);                           // DIM2
}

/*******************************************************
* (Type *IN_ARRAY2, int DIM1, int DIM2)
*******************************************************/

%typemap(in)
    (Type *IN_ARRAY2, int DIM1, int DIM2)                       // PATTERN
        (PyArrayObject* pyarr=NULL),
    (Type *IN_ARRAY2, SpiceInt DIM1, SpiceInt DIM2)             // PATTERN
        (PyArrayObject* pyarr=NULL)
{
//      (Type *IN_ARRAY2, int DIM1, int DIM2)

    CONVERT_TO_CONTIGUOUS_ARRAY(Typecode, $input, 2, 2, pyarr)

    $1 = ($1_ltype) PyArray_DATA(pyarr);                        // ARRAY
    $2 = (int) PyArray_DIM(pyarr, 0);                           // DIM1
    $3 = (int) PyArray_DIM(pyarr, 1);                           // DIM2
}

/*******************************************************
* (int DIM1, int DIM2, Type *IN_ARRAY2)
*******************************************************/

%typemap(in)
    (int DIM1, int DIM2, Type *IN_ARRAY2)                       // PATTERN
        (PyArrayObject* pyarr=NULL),
    (SpiceInt DIM1, SpiceInt DIM2, Type *IN_ARRAY2)             // PATTERN
        (PyArrayObject* pyarr=NULL)
{
//      (int DIM1, int DIM2, Type *IN_ARRAY2)
//  NOT CURRENTLY USED BY CSPICE

    CONVERT_TO_CONTIGUOUS_ARRAY(Typecode, $input, 2, 2, pyarr)

    $3 = ($3_ltype) PyArray_DATA(pyarr);                        // ARRAY
    $1 = (int) PyArray_DIM(pyarr, 0);                           // DIM1
    $2 = (int) PyArray_DIM(pyarr, 1);                           // DIM2
}

/*******************************************************
* (int DIM1, Type IN_ARRAY2[][ANY])
* (SpiceInt DIM1, Type IN_ARRAY2[ANY])
*******************************************************/

%typemap(in)
    (int DIM1, Type IN_ARRAY2[][ANY])                           // PATTERN
        (PyArrayObject* pyarr=NULL),
    (SpiceInt DIM1, Type IN_ARRAY2[][ANY])                      // PATTERN
        (PyArrayObject* pyarr=NULL)
{
//      (int DIM1, Type IN_ARRAY2[][ANY])
//      (SpiceInt DIM1, Type IN_ARRAY2[][ANY])

    CONVERT_TO_CONTIGUOUS_ARRAY(Typecode, $input, 2, 2, pyarr)
    TEST_INVALID_ARRAY_SHAPE_x2D(pyarr, $2_dim1);

    $2 = ($2_ltype) PyArray_DATA(pyarr);                        // ARRAY
    $1 = (int) PyArray_DIM(pyarr, 0);                           // DIM1
}

/*******************************************************
* (int DIM1, Type IN_ARRAY2[][ANY])
* (SpiceInt DIM1, Type IN_ARRAY2[ANY])
*******************************************************/

%typemap(in)
    (Type IN_ARRAY2[][ANY], int DIM1)                           // PATTERN
        (PyArrayObject* pyarr=NULL),
    (Type IN_ARRAY2[][ANY], SpiceInt DIM1)                      // PATTERN
        (PyArrayObject* pyarr=NULL)
{
//      (Type IN_ARRAY2[][ANY], int DIM1)
//      (Type IN_ARRAY2[][ANY], SpiceInt DIM1)

    CONVERT_TO_CONTIGUOUS_ARRAY(Typecode, $input, 2, 2, pyarr)
    TEST_INVALID_ARRAY_SHAPE_x2D(pyarr, $1_dim1);

    $1 = ($1_ltype) PyArray_DATA(pyarr);                        // ARRAY
    $2 = (int) PyArray_DIM(pyarr, 0);                           // DIM1
}

/*******************************************************
* (Type IN_ARRAY2[][ANY])
*******************************************************/

%typemap(in)
    (Type IN_ARRAY2[][ANY])                                     // PATTERN
            (PyArrayObject* pyarr=NULL)
{
//      (Type IN_ARRAY2[][ANY])

    CONVERT_TO_CONTIGUOUS_ARRAY(Typecode, $input, 2, 2, pyarr)
    TEST_INVALID_ARRAY_SHAPE_x2D(pyarr, $1_dim1);

    $1 = ($1_ltype) PyArray_DATA(pyarr);                        // ARRAY
//  $2 = (int) PyArray_DIM(pyarr, 0);                           // DIM1
//  $3 = (int) PyArray_DIM(pyarr, 1);                           // DIM2
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
//      (int DIM1, int DIM2, Type *IN_ARRAY2)

    CONVERT_TO_CONTIGUOUS_ARRAY(Typecode, $input, 2, 2, pyarr)

    $1 = ($1_ltype) PyArray_DATA(pyarr);                        // ARRAY
}


/*******************************************************
* (Type *IN_ARRAY12, int DIM1, int DIM2)
*******************************************************/

%typemap(in)
    (Type *IN_ARRAY12, int DIM1, int DIM2)                      // PATTERN
        (PyArrayObject* pyarr=NULL),
    (Type *IN_ARRAY12, SpiceInt DIM1, SpiceInt DIM2)            // PATTERN
        (PyArrayObject* pyarr=NULL)
{
//      (Type *IN_ARRAY12, int DIM1, int DIM2)

    CONVERT_TO_CONTIGUOUS_ARRAY(Typecode, $input, 1, 2, pyarr)

    if (PyArray_NDIM(pyarr) == 1) {
        $1 = ($1_ltype) PyArray_DATA(pyarr);                    // ARRAY
        $2 = 0;                                                 // DIM1
        $3 = (int) PyArray_DIM(pyarr, 0);                       // DIM2
    } else {
        $1 = ($1_ltype) PyArray_DATA(pyarr);                    // ARRAY
        $2 = (int) PyArray_DIM(pyarr, 0);                       // DIM1
        $3 = (int) PyArray_DIM(pyarr, 1);                       // DIM2
    }
}

/*******************************************************
* (Type *IN_ARRAY23, int DIM1, int DIM2, int DIM3)
*******************************************************/

%typemap(in)
    (Type *IN_ARRAY23, int DIM1, int DIM2, int DIM3)            // PATTERN
        (PyArrayObject* pyarr=NULL),
    (Type *IN_ARRAY23, SpiceInt DIM1, SpiceInt DIM2, SpiceInt DIM3) // PATTERN
        (PyArrayObject* pyarr=NULL)
{
//      (Type *IN_ARRAY23, int DIM1, int DIM2, int DIM3)

    CONVERT_TO_CONTIGUOUS_ARRAY(Typecode, $input, 2, 3, pyarr)

    if (PyArray_NDIM(pyarr) == 2) {
        $1 = ($1_ltype) PyArray_DATA(pyarr);                    // ARRAY
        $2 = 0;                                                 // DIM1
        $3 = (int) PyArray_DIM(pyarr, 0);                       // DIM2
        $4 = (int) PyArray_DIM(pyarr, 1);                       // DIM3
    } else {
        $1 = ($1_ltype) PyArray_DATA(pyarr);                    // ARRAY
        $2 = (int) PyArray_DIM(pyarr, 0);                       // DIM1
        $3 = (int) PyArray_DIM(pyarr, 1);                       // DIM2
        $4 = (int) PyArray_DIM(pyarr, 2);                       // DIM3
    }
}


/*******************************************************
* %typemap(argout)
* %typemap(freearg)
*******************************************************/

%typemap(argout)
    (Type IN_ARRAY2[ANY][ANY]),
    (Type IN_ARRAY2[ANY][ANY], int DIM1, int DIM2),
    (Type IN_ARRAY2[ANY][ANY], SpiceInt DIM1, SpiceInt DIM2),
    (int DIM1, int DIM2, Type IN_ARRAY2[ANY][ANY]),
    (SpiceInt DIM1, SpiceInt DIM2, Type IN_ARRAY2[ANY][ANY]),
    (Type *IN_ARRAY2, int DIM1, int DIM2),
    (Type *IN_ARRAY2, SpiceInt DIM1, SpiceInt DIM2),
    (int DIM1, int DIM2, Type *IN_ARRAY2),
    (SpiceInt DIM1, SpiceInt DIM2, Type *IN_ARRAY2),
    (int DIM1, Type IN_ARRAY2[][ANY]),
    (SpiceInt DIM1, Type IN_ARRAY2[][ANY]),
    (Type IN_ARRAY2[][ANY], int DIM1),
    (Type IN_ARRAY2[][ANY], SpiceInt DIM1),
    (Type IN_ARRAY2[][ANY]),
    (Type IN_ARRAY2[]),
    (Type *IN_ARRAY2),
    (Type *IN_ARRAY12, int DIM1, int DIM2),
    (Type *IN_ARRAY12, SpiceInt DIM1, SpiceInt DIM2),
    (Type *IN_ARRAY23, int DIM1, int DIM2, INT DIM3),
    (Type *IN_ARRAY23, SpiceInt DIM1, SpiceInt DIM2, SpiceInt DIM3)
""

%typemap(freearg)
    (Type IN_ARRAY2[ANY][ANY]),
    (Type IN_ARRAY2[ANY][ANY], int DIM1, int DIM2),
    (Type IN_ARRAY2[ANY][ANY], SpiceInt DIM1, SpiceInt DIM2),
    (int DIM1, int DIM2, Type IN_ARRAY2[ANY][ANY]),
    (SpiceInt DIM1, SpiceInt DIM2, Type IN_ARRAY2[ANY][ANY]),
    (Type *IN_ARRAY2, int DIM1, int DIM2),
    (Type *IN_ARRAY2, SpiceInt DIM1, SpiceInt DIM2),
    (int DIM1, int DIM2, Type *IN_ARRAY2),
    (SpiceInt DIM1, SpiceInt DIM2, Type *IN_ARRAY2),
    (int DIM1, Type IN_ARRAY2[][ANY]),
    (SpiceInt DIM1, Type IN_ARRAY2[][ANY]),
    (Type IN_ARRAY2[][ANY], int DIM1),
    (Type IN_ARRAY2[][ANY], SpiceInt DIM1),
    (Type IN_ARRAY2[][ANY]),
    (Type IN_ARRAY2[]),
    (Type *IN_ARRAY2),
    (Type *IN_ARRAY12, int DIM1, int DIM2),
    (Type *IN_ARRAY12, SpiceInt DIM1, SpiceInt DIM2),
    (Type *IN_ARRAY23, int DIM1, int DIM2, INT DIM3),
    (Type *IN_ARRAY23, SpiceInt DIM1, SpiceInt DIM2, SpiceInt DIM3)

{
//      (Type ...IN_ARRAY2...)
    Py_XDECREF(pyarr$argnum);
}

/*******************************************************
* Now apply to all data types
*******************************************************/

%enddef

// Define concrete examples of the TYPEMAP_IN1 macros
TYPEMAP_IN(int,              NPY_INT   )
TYPEMAP_IN(SpiceInt,         NPY_INT   )
TYPEMAP_IN(ConstSpiceInt,    NPY_INT   )
TYPEMAP_IN(SpiceBoolean,     NPY_INT   )
TYPEMAP_IN(ConstSpiceBoolean,NPY_INT   )
TYPEMAP_IN(long,             NPY_LONG  )
TYPEMAP_IN(double,           NPY_DOUBLE)
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
*       (type OUT_ARRAY1[ANY], int DIM1)
*       (int DIM1, type OUT_ARRAY1[ANY])
*
* If the upper limit on the size of the array can be specified in the SWIG
* interface, but the size returned by C is variable:
*       (type OUT_ARRAY1[ANY], int DIM1, int *SIZE1)
*       (type OUT_ARRAY1[ANY], int *SIZE1, int DIM1)
*       (int DIM1, int *SIZE1, type OUT_ARRAY1[ANY])
*       (int *SIZE1, int DIM1, type OUT_ARRAY1[ANY])
*
* If the total size of a temporary memory buffer can be specified in advance,
* and the shape of the array then returned afterward.
*       (type OUT_ARRAY1[ANY], int *SIZE1)
*       (int *SIZE1, type OUT_ARRAY1[ANY])
*
* If the C function will allocate the memory it needs and will return the size:
*       (type **OUT_ARRAY1, int *DIM1)
*       (int *DIM1, type **OUT_ARRAY1)
*******************************************************************************/

%define TYPEMAP_ARGOUT(Type, Typecode) // Use to fill in numeric types below!

/*******************************************************
* (Type OUT_ARRAY1[ANY])
*******************************************************/

%typemap(in, numinputs=0)
    (Type OUT_ARRAY1[ANY])                                      // PATTERN
        (PyArrayObject* pyarr = NULL)
{
//      (Type OUT_ARRAY1[ANY])

    npy_intp dims[1] = {$1_dim0};                               // DIMENSIONS
    pyarr = (PyArrayObject *) PyArray_SimpleNew(1, dims, Typecode);
    TEST_MALLOC_FAILURE(pyarr);

    $1 = ($1_ltype) PyArray_DATA(pyarr);                        // ARRAY
//  $2 = (int) PyArray_DIM(pyarr, 0);                           // DIM1
//  $3 = &size[0];                                              // SIZE1
}

/*******************************************************
* (Type OUT_ARRAY1[ANY], int DIM1)
*******************************************************/

%typemap(in, numinputs=0)
    (Type OUT_ARRAY1[ANY], int DIM1)                            // PATTERN
        (PyArrayObject* pyarr = NULL),
    (Type OUT_ARRAY1[ANY], SpiceInt DIM1)                       // PATTERN
        (PyArrayObject* pyarr = NULL)
{
//      (Type OUT_ARRAY1[ANY], int DIM1)
//  NOT CURRENTLY USED BY CSPICE

    npy_intp dims[1] = {$1_dim0};                               // ARRAY
    pyarr = (PyArrayObject *) PyArray_SimpleNew(1, dims, Typecode);
    TEST_MALLOC_FAILURE(pyarr);

    $1 = ($1_ltype) PyArray_DATA(pyarr);                        // ARRAY
    $2 = (int) PyArray_DIM(pyarr, 0);                           // DIM1
//  $3 = &size[0];                                              // SIZE1
}

/*******************************************************
* (int DIM1, Type OUT_ARRAY1[ANY])
*******************************************************/

%typemap(in, numinputs=0)
    (int DIM1, Type OUT_ARRAY1[ANY])                            // PATTERN
        (PyArrayObject* pyarr = NULL),
    (SpiceInt DIM1, Type OUT_ARRAY1[ANY])                       // PATTERN
        (PyArrayObject* pyarr = NULL)
{
//      (int DIM1, Type OUT_ARRAY1[ANY])
//  NOT CURRENTLY USED BY CSPICE

    npy_intp dims[1] = {$2_dim0};                               // ARRAY
    pyarr = (PyArrayObject *) PyArray_SimpleNew(1, dims, Typecode);
    TEST_MALLOC_FAILURE(pyarr);

    $2 = ($2_ltype) PyArray_DATA(pyarr);                        // ARRAY
    $1 = (int) PyArray_DIM(pyarr, 0);                           // DIM1
//  $3 = &size[0];                                              // SIZE1
}

/*******************************************************
* (Type OUT_ARRAY1[ANY], int DIM1, int *SIZE1)
*******************************************************/

%typemap(in, numinputs=0)
    (Type OUT_ARRAY1[ANY], int DIM1, int *SIZE1)                // PATTERN
        (PyArrayObject* pyarr = NULL, int size[1]),
    (Type OUT_ARRAY1[ANY], SpiceInt DIM1, SpiceInt *SIZE1)      // PATTERN
        (PyArrayObject* pyarr = NULL, int size[1])
{
//      (Type OUT_ARRAY1[ANY], int DIM1, int *SIZE1)
//  NOT CURRENTLY USED BY CSPICE

    size[0] = 0;
    npy_intp dims[1] = {$1_dim0};                               // ARRAY
    pyarr = (PyArrayObject *) PyArray_SimpleNew(1, dims, Typecode);
    TEST_MALLOC_FAILURE(pyarr);

    $1 = ($1_ltype) PyArray_DATA(pyarr);                        // ARRAY
    $2 = (int) PyArray_DIM(pyarr, 0);                           // DIM1
    $3 = &size[0];                                              // SIZE1
}

/*******************************************************
* (Type OUT_ARRAY1[ANY], int *SIZE1, int DIM1)
*******************************************************/

%typemap(in, numinputs=0)
    (Type OUT_ARRAY1[ANY], int *SIZE1, int DIM1)                // PATTERN
        (PyArrayObject* pyarr = NULL, int size[1]),
    (Type OUT_ARRAY1[ANY], SpiceInt *SIZE1, SpiceInt DIM1)      // PATTERN
        (PyArrayObject* pyarr = NULL, int size[1])
{
//      (Type OUT_ARRAY1[ANY], int *SIZE1, int DIM1)
//  NOT CURRENTLY USED BY CSPICE

    size[0] = 0;
    npy_intp dims[1] = {$1_dim0};                               // ARRAY
    pyarr = (PyArrayObject *) PyArray_SimpleNew(1, dims, Typecode);
    TEST_MALLOC_FAILURE(pyarr);

    $1 = ($1_ltype) PyArray_DATA(pyarr);                        // ARRAY
    $3 = (int) PyArray_DIM(pyarr, 0);                           // DIM1
    $2 = &size[0];                                              // SIZE1
}

/*******************************************************
* (int DIM1, int *SIZE1, Type OUT_ARRAY1[ANY])
*******************************************************/

%typemap(in, numinputs=0)
    (int DIM1, int *SIZE1, Type OUT_ARRAY1[ANY])                // PATTERN
        (PyArrayObject* pyarr = NULL, int size[1]),
    (SpiceInt DIM1, SpiceInt *SIZE1, Type OUT_ARRAY1[ANY])      // PATTERN
        (PyArrayObject* pyarr = NULL, int size[1])
{
//      (int DIM1, int *SIZE1, Type OUT_ARRAY1[ANY])

    size[0] = 0;
    npy_intp dims[1] = {$3_dim0};                               // ARRAY
    pyarr = (PyArrayObject *) PyArray_SimpleNew(1, dims, Typecode);
    TEST_MALLOC_FAILURE(pyarr);

    $3 = ($3_ltype) PyArray_DATA(pyarr);                        // ARRAY
    $1 = (int) PyArray_DIM(pyarr, 0);                           // DIM1
    $2 = &size[0];                                              // SIZE1
}

/*******************************************************
* (int *SIZE1, int DIM1, Type OUT_ARRAY1[ANY])
*******************************************************/

%typemap(in, numinputs=0)
    (int *SIZE1, int DIM1, Type OUT_ARRAY1[ANY])                // PATTERN
        (PyArrayObject* pyarr = NULL, int size[1]),
    (SpiceInt *SIZE1, SpiceInt DIM1, Type OUT_ARRAY1[ANY])      // PATTERN
        (PyArrayObject* pyarr = NULL, int size[1])
{
//      (int *SIZE1, int DIM1, Type OUT_ARRAY1[ANY])
//  NOT CURRENTLY USED BY CSPICE

    size[0] = 0;
    npy_intp dims[1] = {$3_dim0};                               // ARRAY
    pyarr = (PyArrayObject *) PyArray_SimpleNew(1, dims, Typecode);
    TEST_MALLOC_FAILURE(pyarr);

    $3 = ($3_ltype) PyArray_DATA(pyarr);                        // ARRAY
    $2 = (int) PyArray_DIM(pyarr, 0);                           // DIM1
    $1 = &size[0];                                              // SIZE1
}

/*******************************************************
* (Type OUT_ARRAY1[ANY], int *SIZE1)
*******************************************************/

%typemap(in, numinputs=0)
    (Type OUT_ARRAY1[ANY], int *SIZE1)                          // PATTERN
        (PyArrayObject* pyarr = NULL, int size[1]),
    (Type OUT_ARRAY1[ANY], SpiceInt *SIZE1)                     // PATTERN
        (PyArrayObject* pyarr = NULL, int size[1])
{
//      (Type OUT_ARRAY1[ANY], int *SIZE1)

    size[0] = 0;
    npy_intp dims[1] = {$1_dim0};                               // ARRAY
    pyarr = (PyArrayObject *) PyArray_SimpleNew(1, dims, Typecode);
    TEST_MALLOC_FAILURE(pyarr);

    $1 = ($1_ltype) PyArray_DATA(pyarr);                        // ARRAY
//  $3 = (int) PyArray_DIM(pyarr, 0);                           // DIM1
    $2 = &size[0];                                              // SIZE1
}

/*******************************************************
* (int *SIZE1, Type OUT_ARRAY1[ANY])
*******************************************************/

%typemap(in, numinputs=0)
    (int *SIZE1, Type OUT_ARRAY1[ANY])                          // PATTERN
        (PyArrayObject* pyarr = NULL, int size[1]),
    (SpiceInt *SIZE1, Type OUT_ARRAY1[ANY])                     // PATTERN
        (PyArrayObject* pyarr = NULL, int size[1])
{
//      (int *SIZE1, Type OUT_ARRAY1[ANY])

    size[0] = 0;
    npy_intp dims[1] = {$2_dim0};                               // ARRAY
    pyarr = (PyArrayObject *) PyArray_SimpleNew(1, dims, Typecode);
    TEST_MALLOC_FAILURE(pyarr);

    $2 = ($2_ltype) PyArray_DATA(pyarr);                        // ARRAY
//  $3 = (int) PyArray_DIM(pyarr, 0);                           // DIM1
    $1 = &size[0];                                              // SIZE1
}

/*******************************************************
* %typemap(argout)
* %typemap(freearg)
*******************************************************/

%typemap(argout)
    (Type OUT_ARRAY1[ANY]),
    (Type OUT_ARRAY1[ANY], int DIM1),
    (Type OUT_ARRAY1[ANY], Spiceint DIM1),
    (int DIM1, Type OUT_ARRAY1[ANY]),
    (Spiceint DIM1, Type OUT_ARRAY1[ANY])
{
    $result = SWIG_Python_AppendOutput($result, (PyObject *) pyarr$argnum);
    // AppendOutput steals the reference to the argument.
    pyarr$argnum = NULL;
}

%typemap(argout)
    (Type OUT_ARRAY1[ANY], int DIM1, int *SIZE1),
    (Type OUT_ARRAY1[ANY], SpiceInt DIM1, SpiceInt *SIZE1),
    (Type OUT_ARRAY1[ANY], int  *SIZE1, int DIM1),
    (Type OUT_ARRAY1[ANY], SpiceInt *SIZE1, SpiceInt DIM1),
    (int DIM1, int *SIZE1, Type OUT_ARRAY1[ANY]),
    (SpiceInt DIM1, SpiceInt *SIZE1, Type OUT_ARRAY1[ANY]),
    (int *SIZE1, int DIM1, Type OUT_ARRAY1[ANY]),
    (SpiceInt *SIZE1, SpiceInt DIM1, Type OUT_ARRAY1[ANY]),
    (Type OUT_ARRAY1[ANY], int *SIZE1),
    (Type OUT_ARRAY1[ANY], SpiceInt *SIZE1),
    (int *SIZE1, Type OUT_ARRAY1[ANY]),
    (SpiceInt *SIZE1, Type OUT_ARRAY1[ANY])
{
    // Reshape to indicate the number of elements we actually created
    npy_intp dims[1] = {size$argnum[0]};
    PyArray_Dims shape = {dims, 1};
    PyArray_Resize(pyarr$argnum, &shape, 0, NPY_CORDER);

    $result = SWIG_Python_AppendOutput($result, (PyObject *) pyarr$argnum);
    // AppendOutput steals the reference to the argument.
    pyarr$argnum = NULL;
}

%typemap(freearg)
    (Type OUT_ARRAY1[ANY]),
    (Type OUT_ARRAY1[ANY], int DIM1),
    (Type OUT_ARRAY1[ANY], SpiceInt DIM1),
    (int DIM1, Type OUT_ARRAY1[ANY]),
    (SpiceInt DIM1, Type OUT_ARRAY1[ANY]),
    (Type OUT_ARRAY1[ANY], int DIM1, int  *SIZE1),
    (Type OUT_ARRAY1[ANY], SpiceInt DIM1, SpiceInt *SIZE1),
    (Type OUT_ARRAY1[ANY], int  *SIZE1, int DIM1),
    (Type OUT_ARRAY1[ANY], SpiceInt *SIZE1, SpiceInt DIM1),
    (int DIM1, int *SIZE1, Type OUT_ARRAY1[ANY]),
    (SpiceInt DIM1, SpiceInt *SIZE1, Type OUT_ARRAY1[ANY]),
    (int *SIZE1, int DIM1, Type OUT_ARRAY1[ANY]),
    (SpiceInt *SIZE1, SpiceInt DIM1, Type OUT_ARRAY1[ANY]),
    (Type OUT_ARRAY1[ANY], int  *SIZE1),
    (Type OUT_ARRAY1[ANY], SpiceInt *SIZE1),
    (int *SIZE1, Type OUT_ARRAY1[ANY]),
    (SpiceInt *SIZE1, Type OUT_ARRAY1[ANY])
{
    Py_XDECREF(pyarr$argnum);
}

/***************************************************************
* (Type **OUT_ARRAY1, int *SIZE1)
***************************************************************/

%typemap(in, numinputs=0)
    (Type **OUT_ARRAY1, int *SIZE1)
        (PyArrayObject* pyarr=NULL, Type *buffer=NULL, int dimsize[1]),
    (Type **OUT_ARRAY1, SpiceInt *SIZE1)
        (PyArrayObject* pyarr=NULL, Type *buffer=NULL, int dimsize[1])
{
//      (Type **OUT_ARRAY1, int *SIZE1)

    $1 = &buffer;                                               // ARRAY
    $2 = &dimsize[0];                                           // SIZE1
}

/***************************************************************
* (int *SIZE1, Type **OUT_ARRAY1)
***************************************************************/

%typemap(in, numinputs=0)
    (int *SIZE1, Type **OUT_ARRAY1)
        (PyArrayObject* pyarr=NULL, Type *buffer=NULL, int dimsize[1]),
    (SpiceInt *SIZE1, Type **OUT_ARRAY1)
        (PyArrayObject* pyarr=NULL, Type *buffer=NULL, int dimsize[1])
{
//      (int *SIZE1, Type **OUT_ARRAY1)
//  NOT CURRENTLY USED BY CSPICE

    $2 = &buffer;                                               // ARRAY
    $1 = &dimsize[0];                                           // SIZE1
}

/*******************************************************
* %typemap(argout)
* %typemap(freearg)
*******************************************************/

%typemap(argout)
    (Type **OUT_ARRAY1, int *SIZE1),
    (Type **OUT_ARRAY1, SpiceInt *SIZE1),
    (int *SIZE1, Type **OUT_ARRAY1),
    (SpiceInt *SIZE1, Type **OUT_ARRAY1)
{
//      (Type **OUT_ARRAY1, int *SIZE1)
//      (int *SIZE1, Type **OUT_ARRAY1)

    TEST_MALLOC_FAILURE(buffer$argnum);
    npy_intp dims[1] = {dimsize$argnum[0]};
    pyarr$argnum = create_array_with_owned_data(1, dims, Typecode, &buffer$argnum);
    TEST_MALLOC_FAILURE(pyarr$argnum);

    $result = SWIG_Python_AppendOutput($result, (PyObject *) pyarr$argnum);
    // AppendOutput steals the reference to the argument.
    pyarr$argnum = NULL;
}

%typemap(freearg)
    (Type **OUT_ARRAY1, int *SIZE1),
    (Type **OUT_ARRAY1, SpiceInt *SIZE1),
    (int *SIZE1, Type **OUT_ARRAY1),
    (SpiceInt *SIZE1, Type **OUT_ARRAY1)
{
    Py_XDECREF(pyarr$argnum);
    PyMem_Free((void *) buffer$argnum);
}

/*******************************************************
* Now define these typemaps for every numeric type
*******************************************************/

%enddef

TYPEMAP_ARGOUT(int,           NPY_INT   )
TYPEMAP_ARGOUT(SpiceInt,      NPY_INT   )
TYPEMAP_ARGOUT(SpiceBoolean,  NPY_INT   )
TYPEMAP_ARGOUT(long,          NPY_LONG  )
TYPEMAP_ARGOUT(double,        NPY_DOUBLE)
TYPEMAP_ARGOUT(SpiceDouble,   NPY_DOUBLE)

#undef TYPEMAP_ARGOUT

/*******************************************************************************
* If the function should return a Python scalar on size = 0:
*       (type **OUT_ARRAY01, int *DIM1)
*******************************************************************************/

%define TYPEMAP_ARGOUT(Type, Typecode) // To fill in types below!

/***************************************************************
* (Type **OUT_ARRAY01, int *SIZE1)
***************************************************************/

%typemap(in, numinputs=0)
    (Type **OUT_ARRAY01, int *SIZE1)
        (PyArrayObject* pyarr=NULL, Type *buffer=NULL,
                                                           int dimsize[1]),
    (Type **OUT_ARRAY01, SpiceInt *SIZE1)
        (PyArrayObject* pyarr=NULL, Type *buffer=NULL,
                                                           int dimsize[1])
{
//      (Type **OUT_ARRAY01, int *SIZE1)

    $1 = &buffer;                                               // ARRAY
    $2 = &dimsize[0];                                           // SIZE1
}

/*******************************************************
* %typemap(argout)
* %typemap(freearg)
*******************************************************/

%typemap(argout)
    (Type **OUT_ARRAY01, int *SIZE1),
    (Type **OUT_ARRAY01, SpiceInt *SIZE1)
{
//      (Type **OUT_ARRAY01, int *SIZE1)

    TEST_MALLOC_FAILURE(buffer$argnum);
    npy_intp dim = max(dimsize$argnum[0], 1);
    pyarr$argnum = (PyArrayObject *) create_array_with_owned_data(1, &dim, Typecode, &buffer$argnum);
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
    (Type **OUT_ARRAY01, int *SIZE1),
    (Type **OUT_ARRAY01, SpiceInt *SIZE1)
{
    Py_XDECREF(pyarr$argnum);
    PyMem_Free((void *) buffer$argnum);
}

%enddef

/*******************************************************
* Now define these typemaps for every numeric type
*******************************************************/

TYPEMAP_ARGOUT(int,           NPY_INT)
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
*       (type OUT_ARRAY2[ANY][ANY], int DIM1, int DIM2)
*       (int DIM1, int DIM2, type OUT_ARRAY2[ANY][ANY])
*
* If the upper limit on the size of the array's first axis can be specified in
* the SWIG interface, but the size of the first axis returned by C is variable:
*       (type OUT_ARRAY2[ANY][ANY], int DIM1, int DIM2, int *SIZE1)
*       (type OUT_ARRAY2[ANY][ANY], int *SIZE1, int DIM1, int DIM2)
*       (int DIM1, int DIM2, int *SIZE1, type OUT_ARRAY2[ANY][ANY])
*       (int *SIZE1, int DIM1, int DIM2, type OUT_ARRAY2[ANY][ANY])
* Also...
*       (int DIM1, int *SIZE1, type OUT_ARRAY2[ANY][ANY])
*       (int *SIZE1, type OUT_ARRAY2[ANY][ANY])
*
* If an upper limit on the total size of a temporary memory buffer can be
* specified in advance, and the shape of the array then returned afterward.
* Upon return, the large buffer is freed and only the required amount of memory
* is retained.
*       (type OUT_ARRAY2[ANY][ANY], int *SIZE1, int *SIZE2)
*       (int *SIZE1, int *SIZE2, type OUT_ARRAY2[ANY][ANY])
*
* If the C function will allocate the memory it needs and will return the
* dimensions:
*       (type **OUT_ARRAY2, int *DIM1, int *DIM2)
*       (int *DIM1, int *DIM2, type **OUT_ARRAY2)
*
* This version will return a 1-D array if the first dimension is 0; otherwise
* a 2-D array:
*       (type **OUT_ARRAY12, int *DIM1, int *DIM2)
*******************************************************************************/

%define TYPEMAP_ARGOUT(Type, Typecode) // Use to fill in numeric types below!

/***************************************************************
* (Type OUT_ARRAY2[ANY][ANY])
***************************************************************/

%typemap(in, numinputs=0)
    (Type OUT_ARRAY2[ANY][ANY])                                 // PATTERN
        (PyArrayObject* pyarr = NULL)
{
//      (Type OUT_ARRAY2[ANY][ANY])

    npy_intp dims[2] = {$1_dim0, $1_dim1};               // ARRAY
    pyarr = (PyArrayObject *) PyArray_SimpleNew(2, dims, Typecode);
    TEST_MALLOC_FAILURE(pyarr);

//  dimsize[0] = (int) dims[0];
//  dimsize[1] = (int) dims[1];

    $1 = ($1_ltype) PyArray_DATA(pyarr);                        // ARRAY
//  $2 = (int) PyArray_DIM(pyarr, 0);                           // DIM1
//  $3 = (int) PyArray_DIM(pyarr, 1);                           // DIM2
//  $4 = &dimsize[0];                                           // SIZE1
//  $5 = &dimsize[1];                                           // SIZE2
}

/***************************************************************
* (Type OUT_ARRAY2[ANY][ANY], int DIM1, int DIM2)
***************************************************************/

%typemap(in, numinputs=0)
    (Type OUT_ARRAY2[ANY][ANY], int DIM1, int DIM2)             // PATTERN
        (PyArrayObject* pyarr = NULL),
    (Type OUT_ARRAY2[ANY][ANY], SpiceInt DIM1, SpiceInt DIM2)   // PATTERN
        (PyArrayObject* pyarr = NULL)
{
//      (Type OUT_ARRAY2[ANY][ANY], int DIM1, int DIM2)
//  NOT CURRENTLY USED BY CSPICE

    npy_intp dims[2] = {$1_dim0, $1_dim1};                      // ARRAY
    pyarr = (PyArrayObject *) PyArray_SimpleNew(2, dims, Typecode);
    TEST_MALLOC_FAILURE(pyarr);

//  dimsize[0] = (int) dims[0];
//  dimsize[1] = (int) dims[1];

    $1 = ($1_ltype) PyArray_DATA(pyarr);                        // ARRAY
    $2 = (int) PyArray_DIM(pyarr, 0);                           // DIM1
    $3 = (int) PyArray_DIM(pyarr, 1);                           // DIM2
//  $4 = &dimsize[0];                                           // SIZE1
//  $5 = &dimsize[1];                                           // SIZE2
}

/***************************************************************
* (int DIM1, int DIM2, Type OUT_ARRAY2[ANY][ANY])
***************************************************************/

%typemap(in, numinputs=0)
    (int DIM1, int DIM2, Type OUT_ARRAY2[ANY][ANY])             // PATTERN
        (PyArrayObject* pyarr = NULL),
    (SpiceInt DIM1, SpiceInt DIM2, Type OUT_ARRAY2[ANY][ANY])   // PATTERN
        (PyArrayObject* pyarr = NULL)
{
//      (int DIM1, int DIM2, Type OUT_ARRAY2[ANY][ANY])
//  NOT CURRENTLY USED BY CSPICE

    npy_intp dims[2] = {$3_dim0, $3_dim1};                      // ARRAY
    pyarr = (PyArrayObject *) PyArray_SimpleNew(2, dims, Typecode);
    TEST_MALLOC_FAILURE(pyarr);

//  dimsize[0] = (int) dims[0];
//  dimsize[1] = (int) dims[1];

    $3 = ($3_ltype) PyArray_DATA(pyarr);                        // ARRAY
    $1 = (int) PyArray_DIM(pyarr, 0);                           // DIM1
    $2 = (int) PyArray_DIM(pyarr, 1);                           // DIM2
//  $4 = &dimsize[0];                                           // SIZE1
//  $5 = &dimsize[1];                                           // SIZE2
}

/***************************************************************
* (Type OUT_ARRAY2[ANY][ANY], int DIM1, int DIM2, int *SIZE1)
***************************************************************/

%typemap(in, numinputs=0)
    (Type OUT_ARRAY2[ANY][ANY], int DIM1, int DIM2, int *SIZE1)
        (PyArrayObject* pyarr = NULL, int dimsize[2], int outsize),
    (Type OUT_ARRAY2[ANY][ANY], SpiceInt DIM1, SpiceInt DIM2, SpiceInt *SIZE1)
        (PyArrayObject* pyarr = NULL, int dimsize[2], int outsize)
{
//      (Type OUT_ARRAY2[ANY][ANY], int DIM1, int DIM2, int *SIZE1)
//  NOT CURRENTLY USED BY CSPICE

    outsize = 0;
    npy_intp dims[2] = {$1_dim0, $1_dim1};               // ARRAY
    pyarr = (PyArrayObject *) PyArray_SimpleNew(2, dims, Typecode);
    TEST_MALLOC_FAILURE(pyarr);

    dimsize[0] = (int) dims[0];
    dimsize[1] = (int) dim$argnums[1];

    $1 = ($1_ltype) PyArray_DATA(pyarr);                        // ARRAY
    $2 = (int) PyArray_DIM(pyarr, 0);                           // DIM1
    $3 = (int) PyArray_DIM(pyarr, 1);                           // DIM2
    $4 = &outsize;                                              // SIZE1
//  $5 = &dimsize[1];                                           // SIZE2

}

/***************************************************************
* (Type OUT_ARRAY2[ANY][ANY], int *SIZE1, int DIM1, int DIM2)
***************************************************************/

%typemap(in, numinputs=0)
    (Type OUT_ARRAY2[ANY][ANY], int *SIZE1, int DIM1, int DIM2)
        (PyArrayObject* pyarr = NULL, int dimsize[2], int outsize),
    (Type OUT_ARRAY2[ANY][ANY], SpiceInt *SIZE1, SpiceInt DIM1, SpiceInt DIM2)
        (PyArrayObject* pyarr = NULL, int dimsize[2], int outsize)
{
//      (Type OUT_ARRAY2[ANY][ANY], int *SIZE1, int DIM1, int DIM2)
//  NOT CURRENTLY USED BY CSPICE

    outsize = 0;
    npy_intp dims[2] = {$1_dim0, $1_dim1};                      // ARRAY
    pyarr = (PyArrayObject *) PyArray_SimpleNew(2, dims, Typecode);
    TEST_MALLOC_FAILURE(pyarr);

    dimsize[0] = (int) dims[0];
    dimsize[1] = (int) dims[1];

    $1 = ($1_ltype) PyArray_DATA(pyarr);                        // ARRAY
    $3 = (int) PyArray_DIM(pyarr, 0);                           // DIM1
    $4 = (int) PyArray_DIM(pyarr, 1);                           // DIM2
    $2 = &outsize;                                              // SIZE1
//  $5 = &dimsize[1];                                           // SIZE2
}

/***************************************************************
* (int DIM1, int DIM2, int *SIZE1, Type OUT_ARRAY2[ANY][ANY])
***************************************************************/

%typemap(in, numinputs=0)
    (int DIM1, int DIM2, int *SIZE1, Type OUT_ARRAY2[ANY][ANY])
        (PyArrayObject* pyarr = NULL, int dimsize[2], int outsize),
    (SpiceInt DIM1, SpiceInt DIM2, SpiceInt *SIZE1, Type OUT_ARRAY2[ANY][ANY])
        (PyArrayObject* pyarr = NULL, int dimsize[2], int outsize)
{
//      (int DIM1, int DIM2, int *SIZE1, Type OUT_ARRAY2[ANY][ANY])
//  NOT CURRENTLY USED BY CSPICE

    outsize = 0;
    npy_intp dims[2] = {$4_dim0, $4_dim1};                      // ARRAY
    pyarr = (PyArrayObject *) PyArray_SimpleNew(2, dims, Typecode);
    TEST_MALLOC_FAILURE(pyarr);

    dimsize[0] = (int) dims[0];
    dimsize[1] = (int) dims[1];

    $4 = ($4_ltype) PyArray_DATA(pyarr);                        // ARRAY
    $1 = (int) PyArray_DIM(pyarr, 0);                           // DIM1
    $2 = (int) PyArray_DIM(pyarr, 1);                           // DIM2
    $3 = &outsize;                                              // SIZE1
//  $5 = &dimsize[1];                                           // SIZE2
}

/***************************************************************
* (int DIM1, int *SIZE1, Type OUT_ARRAY2[ANY][ANY])
***************************************************************/

%typemap(in, numinputs=0)
    (int DIM1, int *SIZE1, Type OUT_ARRAY2[ANY][ANY])
        (PyArrayObject* pyarr = NULL, int dimsize[2], int outsize)
{
//      (int DIM1, int *SIZE1, Type OUT_ARRAY2[ANY][ANY])
//  NOT CURRENTLY USED BY CSPICE

    outsize = 0;
    npy_intp dims[2] = {$3_dim0, $3_dim1};                      // ARRAY
    pyarr = (PyArrayObject *) PyArray_SimpleNew(2, dims, Typecode);
    TEST_MALLOC_FAILURE(pyarr);

    dimsize[0] = (int) dims[0];
    dimsize[1] = (int) $3_dim1;

    $3 = ($3_ltype) PyArray_DATA(pyarr);                        // ARRAY
    $1 = (int) PyArray_DIM(pyarr, 0);                           // DIM1
//  $4 = (int) PyArray_DIM(pyarr, 1);                           // DIM2
    $2 = &outsize;                                              // SIZE1
//  $5 = &dimsize[1];                                           // SIZE2
}

/***************************************************************
* (int *SIZE1, int DIM1, int DIM2, Type OUT_ARRAY2[ANY][ANY])
***************************************************************/

%typemap(in, numinputs=0)
    (int *SIZE1, int DIM1, int DIM2, Type OUT_ARRAY2[ANY][ANY]),
        (PyArrayObject* pyarr = NULL, int dimsize[2], int outsize),
    (SpiceInt *SIZE1, SpiceInt DIM1, SpiceInt DIM2, Type OUT_ARRAY2[ANY][ANY])
        (PyArrayObject* pyarr = NULL, int dimsize[2], int outsize)
{
//      (int *SIZE1, int DIM1, int DIM2, Type OUT_ARRAY2[ANY][ANY])
//  NOT CURRENTLY USED BY CSPICE

    outsize = 0;
    npy_intp dims[2] = {$4_dim0, $4_dim1};                      // ARRAY
    pyarr = (PyArrayObject *) PyArray_SimpleNew(2, dims, Typecode);
    TEST_MALLOC_FAILURE(pyarr);

    dimsize[0] = (int) dims[0];
    dimsize[1] = (int) dims[1];

    $4 = ($4_ltype) PyArray_DATA(pyarr);                        // ARRAY
    $2 = (int) PyArray_DIM(pyarr, 0);                           // DIM1
    $3 = (int) PyArray_DIM(pyarr, 1);                           // DIM2
    $1 = &outsize;                                              // SIZE1
//  $5 = &dimsize[1];                                           // SIZE2
}

/***************************************************************
* (Type OUT_ARRAY2[ANY][ANY], int *SIZE1)
***************************************************************/

%typemap(in, numinputs=0)
    (Type OUT_ARRAY2[ANY][ANY], int *SIZE1)
        (PyArrayObject* pyarr = NULL, int dimsize[2], int outsize),
    (Type OUT_ARRAY2[ANY][ANY], SpiceInt *SIZE1)
        (PyArrayObject* pyarr = NULL, int dimsize[2], int outsize)
{
//      (Type OUT_ARRAY2[ANY][ANY], int *SIZE1)

    outsize = 0;
    npy_intp dims[2] = {$1_dim0, $1_dim1};                      // ARRAY
    pyarr = (PyArrayObject *) PyArray_SimpleNew(2, dims, Typecode);
    TEST_MALLOC_FAILURE(pyarr);

    dimsize[0] = (int) dims[0];
    dimsize[1] = (int) dims[1];

    $1 = ($1_ltype) PyArray_DATA(pyarr);                        // ARRAY
//  $3 = (int) PyArray_DIM(pyarr, 0);                           // DIM1
//  $4 = (int) PyArray_DIM(pyarr, 1);                           // DIM2
    $2 = &outsize;                                              // SIZE1
//  $5 = &dimsize[1];                                           // SIZE2
}

/***************************************************************
* (int *SIZE1, Type OUT_ARRAY2[ANY][ANY])
***************************************************************/

%typemap(in, numinputs=0)
    (int *SIZE1, Type OUT_ARRAY2[ANY][ANY])
        (PyArrayObject* pyarr = NULL, int dimsize[2], int outsize),
    (SpiceInt *SIZE1, Type OUT_ARRAY2[ANY][ANY])
        (PyArrayObject* pyarr = NULL, int dimsize[2], int outsize)
{
//      (int *SIZE1, Type OUT_ARRAY2[ANY][ANY])

    outsize = 0;
    npy_intp dims[2] = {$2_dim0, $2_dim1};                      // ARRAY
    pyarr = (PyArrayObject *) PyArray_SimpleNew(2, dims, Typecode);
    TEST_MALLOC_FAILURE(pyarr);

    dimsize[0] = (int) dims[0];
    dimsize[1] = (int) dims[1];

    $2 = ($2_ltype) PyArray_DATA(pyarr);                        // ARRAY
//  $3 = (int) PyArray_DIM(pyarr, 0);                           // DIM1
//  $4 = (int) PyArray_DIM(pyarr, 1);                           // DIM2
    $1 = &outsize;                                              // SIZE1
//  $5 = &dimsize[1];                                           // SIZE2
}

/***************************************************************
* (Type OUT_ARRAY2[ANY][ANY], int *SIZE1, int *SIZE2)
***************************************************************/

%typemap(in, numinputs=0)
    (Type OUT_ARRAY2[ANY][ANY], int *SIZE1, int *SIZE2)
        (PyArrayObject* pyarr = NULL, int dimsize[2], int outsize),
    (Type OUT_ARRAY2[ANY][ANY], SpiceInt *SIZE1, SpiceInt *SIZE2)
        (PyArrayObject* pyarr = NULL, int dimsize[2], int outsize)
{
//      (Type OUT_ARRAY2[ANY][ANY], int *SIZE1, int *SIZE2)
//  NOT CURRENTLY USED BY CSPICE

    outsize = 0;
    npy_intp dims[2] = {$1_dim0, $1_dim1};                      // ARRAY
    pyarr = (PyArrayObject *) PyArray_SimpleNew(2, dims, Typecode);
    TEST_MALLOC_FAILURE(pyarr);

    dimsize[0] = (int) dims[0];
    dimsize[1] = (int) dims[1];

    $1 = ($1_ltype) PyArray_DATA(pyarr);                        // ARRAY
//  $4 = (int) PyArray_DIM(pyarr, 0);                           // DIM1
//  $5 = (int) PyArray_DIM(pyarr, 1);                           // DIM2
    $2 = &outsize;                                              // SIZE1
//  $3 = &dimsize[1];                                           // SIZE2
}

/***************************************************************
* (int *SIZE1, int *SIZE2, Type OUT_ARRAY2[ANY][ANY])
***************************************************************/

%typemap(in, numinputs=0)
    (int *SIZE1, int *SIZE2, Type OUT_ARRAY2[ANY][ANY])
        (PyArrayObject* pyarr = NULL, int dimsize[2], int outsize[2]),
    (SpiceInt *SIZE1, SpiceInt *SIZE2, Type OUT_ARRAY2[ANY][ANY])
        (PyArrayObject* pyarr = NULL, int dimsize[2], int outsize[2])
{
//      (int *SIZE1, int *SIZE2, Type OUT_ARRAY2[ANY][ANY])

    outsize[0] = 0;
    outsize[1] = 0;
    npy_intp dims[2] = {$3_dim0, $3_dim1};                      // ARRAY
    pyarr = (PyArrayObject *) PyArray_SimpleNew(2, dims, Typecode);
    TEST_MALLOC_FAILURE(pyarr);

    dimsize[0] = (int) dims[0];
    dimsize[1] = (int) dims[1];

    $3 = ($3_ltype) PyArray_DATA(pyarr);                        // ARRAY
//  $4 = (int) PyArray_DIM(pyarr, 0);                           // DIM1
//  $5 = (int) PyArray_DIM(pyarr, 1);                           // DIM2
    $1 = &outsize[0];                                           // SIZE1
    $2 = &outsize[1];                                           // SIZE2
}

/*******************************************************
* %typemap(argout)
* %typemap(freearg)
*******************************************************/

%typemap(argout)
    (Type OUT_ARRAY2[ANY][ANY]),
    (Type OUT_ARRAY2[ANY][ANY], int DIM1, int DIM2),
    (Type OUT_ARRAY2[ANY][ANY], SpiceInt DIM1, SpiceInt DIM2),
    (int DIM1, int DIM2, Type OUT_ARRAY2[ANY][ANY]),
    (SpiceInt DIM1, SpiceInt DIM2, Type OUT_ARRAY2[ANY][ANY])
{
    $result = SWIG_Python_AppendOutput($result, (PyObject *) pyarr$argnum);
    // AppendOutput steals the reference to the argument.
    pyarr$argnum = NULL;
}

%typemap(argout)
    (Type OUT_ARRAY2[ANY][ANY], int DIM1, int DIM2, int *SIZE1),
    (Type OUT_ARRAY2[ANY][ANY], SpiceInt DIM1, SpiceInt DIM2, SpiceInt *SIZE1),
    (Type OUT_ARRAY2[ANY][ANY], int *SIZE1, int DIM1, int DIM2),
    (Type OUT_ARRAY2[ANY][ANY], SpiceInt *SIZE1, SpiceInt DIM1, SpiceInt DIM2),
    (int DIM1, int DIM2, int *SIZE1, Type OUT_ARRAY2[ANY][ANY]),
    (SpiceInt DIM1, SpiceInt DIM2, SpiceInt *SIZE1, Type OUT_ARRAY2[ANY][ANY]),
    (int DIM1, int *SIZE1, Type OUT_ARRAY2[ANY][ANY]),
    (int *SIZE1, int DIM1, int DIM2, Type OUT_ARRAY2[ANY][ANY]),
    (SpiceInt *SIZE1, SpiceInt DIM1, SpiceInt DIM2, Type OUT_ARRAY2[ANY][ANY]),
    (Type OUT_ARRAY2[ANY][ANY], int *SIZE1),
    (Type OUT_ARRAY2[ANY][ANY], SpiceInt *SIZE1),
    (int *SIZE1, Type OUT_ARRAY2[ANY][ANY]),
    (SpiceInt *SIZE1, Type OUT_ARRAY2[ANY][ANY])
{
    npy_intp dims[2] = {outsize$argnum, dimsize$argnum[1]};
    PyArray_Dims shape = {dims, 2};

    PyArray_Resize(pyarr$argnum, &shape, 0, NPY_CORDER);
    $result = SWIG_Python_AppendOutput($result, (PyObject *)pyarr$argnum);
    // AppendOutput steals the reference to the argument.
    pyarr$argnum = NULL;
}

%typemap(argout)
    (Type OUT_ARRAY2[ANY][ANY], int *SIZE1, int *SIZE2),
    (Type OUT_ARRAY2[ANY][ANY], SpiceInt *SIZE1, SpiceInt *SIZE2),
    (int *SIZE1, int *SIZE2, Type OUT_ARRAY2[ANY][ANY]),
    (SpiceInt *SIZE1, SpiceInt *SIZE2, Type OUT_ARRAY2[ANY][ANY])
{
    npy_intp dims[2] = {outsize$argnum[0], outsize$argnum[1]};
    PyArray_Dims shape = {dims, 2};

    PyArray_Resize(pyarr$argnum, &shape, 0, NPY_CORDER);
    $result = SWIG_Python_AppendOutput($result, (PyObject *)pyarr$argnum);
    // AppendOutput steals the reference to the argument.
    pyarr$argnum = NULL;
}

%typemap(freearg)
    (Type OUT_ARRAY2[ANY][ANY]),
    (Type OUT_ARRAY2[ANY][ANY], int DIM1, int DIM2),
    (Type OUT_ARRAY2[ANY][ANY], SpiceInt DIM1, SpiceInt DIM2),
    (int DIM1, int DIM2, Type OUT_ARRAY2[ANY][ANY]),
    (SpiceInt DIM1, SpiceInt DIM2, Type OUT_ARRAY2[ANY][ANY]),

    (Type OUT_ARRAY2[ANY][ANY], int DIM1, int DIM2, int *SIZE1),
    (Type OUT_ARRAY2[ANY][ANY], SpiceInt DIM1, SpiceInt DIM2, SpiceInt *SIZE1),
    (Type OUT_ARRAY2[ANY][ANY], int *SIZE1, int DIM1, int DIM2),
    (Type OUT_ARRAY2[ANY][ANY], SpiceInt *SIZE1, SpiceInt DIM1, SpiceInt DIM2),
    (int DIM1, int DIM2, int *SIZE1, Type OUT_ARRAY2[ANY][ANY]),
    (SpiceInt DIM1, SpiceInt DIM2, SpiceInt *SIZE1, Type OUT_ARRAY2[ANY][ANY]),
    (int DIM1, int *SIZE1, Type OUT_ARRAY2[ANY][ANY]),
    (int *SIZE1, int DIM1, int DIM2, Type OUT_ARRAY2[ANY][ANY]),
    (SpiceInt *SIZE1, SpiceInt DIM1, SpiceInt DIM2, Type OUT_ARRAY2[ANY][ANY]),
    (Type OUT_ARRAY2[ANY][ANY], int *SIZE1),
    (Type OUT_ARRAY2[ANY][ANY], SpiceInt *SIZE1),
    (int *SIZE1, Type OUT_ARRAY2[ANY][ANY]),
    (SpiceInt *SIZE1, Type OUT_ARRAY2[ANY][ANY]),

    (Type OUT_ARRAY2[ANY][ANY], int *SIZE1, int *SIZE2),
    (Type OUT_ARRAY2[ANY][ANY], SpiceInt *SIZE1, SpiceInt *SIZE2),
    (int *SIZE1, int *SIZE2, Type OUT_ARRAY2[ANY][ANY]),
    (SpiceInt *SIZE1, SpiceInt *SIZE2, Type OUT_ARRAY2[ANY][ANY])
{
    Py_XDECREF(pyarr$argnum);
}

/***************************************************************
* (Type **OUT_ARRAY2, int *SIZE1, int *SIZE2)
***************************************************************/

%typemap(in, numinputs=0)
    (Type **OUT_ARRAY2, int *SIZE1, int *SIZE2)
        (PyArrayObject* pyarr=NULL, Type *buffer=NULL, int dimsize[2]),
    (Type **OUT_ARRAY2, SpiceInt *SIZE1, SpiceInt *SIZE2)
        (PyArrayObject* pyarr=NULL, Type *buffer=NULL, int dimsize[2]),
    (Type **OUT_ARRAY12, int *SIZE1, int *SIZE2)
        (PyArrayObject* pyarr=NULL, Type *buffer=NULL, int dimsize[2]),
    (Type **OUT_ARRAY12, SpiceInt *SIZE1, SpiceInt *SIZE2)
        (PyArrayObject* pyarr=NULL, Type *buffer=NULL, int dimsize[2])
{
//      (Type **OUT_ARRAY2, int *SIZE1, int *SIZE2)

    $1 = &buffer;                                               // ARRAY
    $2 = &dimsize[0];                                           // SIZE1
    $3 = &dimsize[1];                                           // SIZE2
}

/***************************************************************
* (int *SIZE1, int *SIZE2, Type **OUT_ARRAY2)
***************************************************************/

%typemap(in, numinputs=0)
    (int *SIZE1, int *SIZE2, Type **OUT_ARRAY2)
        (PyArrayObject* pyarr=NULL, Type *buffer=NULL, int dimsize[2]),
    (SpiceInt *SIZE1, SpiceInt *SIZE2, Type **OUT_ARRAY2)
        (PyArrayObject* pyarr=NULL, Type *buffer=NULL, int dimsize[2])
{
//      (int *SIZE1, int *SIZE2, Type **OUT_ARRAY2)
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
    (Type **OUT_ARRAY2, int *SIZE1, int *SIZE2),
    (Type **OUT_ARRAY2, SpiceInt *SIZE1, SpiceInt *SIZE2),
    (int *SIZE1, int *SIZE2, Type **OUT_ARRAY2),
    (SpiceInt *SIZE1, SpiceInt *SIZE2, Type **OUT_ARRAY2)
{
//      (Type **OUT_ARRAY2, int *SIZE1, int *SIZE2)
//      (int *SIZE1, int *SIZE2, Type **OUT_ARRAY2)

    TEST_MALLOC_FAILURE(buffer$argnum);
    npy_intp dims[2] = {dimsize$argnum[0], dimsize$argnum[1]};
    pyarr$argnum = (PyArrayObject *) create_array_with_owned_data(2, dims, Typecode, &buffer$argnum);
    TEST_MALLOC_FAILURE(pyarr$argnum);

    $result = SWIG_Python_AppendOutput($result, (PyObject *) pyarr$argnum);
    // AppendOutput steals the reference to the argument.
    pyarr$argnum = NULL;
}

%typemap(argout)
    (Type **OUT_ARRAY12, int *SIZE1, int *SIZE2),
    (Type **OUT_ARRAY12, SpiceInt *SIZE1, SpiceInt *SIZE2)
{
//      (Type **OUT_ARRAY12, int *SIZE1, int *SIZE2)

    TEST_MALLOC_FAILURE(buffer$argnum);
    npy_intp dims[2] = {dimsize$argnum[0], dimsize$argnum[1]};
    int nd = dims[0] == 0 ? 1 : 2;
    pyarr$argnum = create_array_with_owned_data(nd, &dims[2 - nd], Typecode, &buffer$argnum);
    TEST_MALLOC_FAILURE(pyarr$argnum);

    $result = SWIG_Python_AppendOutput($result, (PyObject *) pyarr$argnum);
    // AppendOutput steals the reference to the argument.
    pyarr$argnum = NULL;
}

%typemap(freearg)
        (Type **OUT_ARRAY2, int *SIZE1, int *SIZE2),
        (Type **OUT_ARRAY2, SpiceInt *SIZE1, SpiceInt *SIZE2),
        (Type **OUT_ARRAY12, int *SIZE1, int *SIZE2),
        (Type **OUT_ARRAY12, SpiceInt *SIZE1, SpiceInt *SIZE2),
        (int *SIZE1, int *SIZE2, Type **OUT_ARRAY2),
        (SpiceInt *SIZE1, SpiceInt *SIZE2, Type **OUT_ARRAY2)
{
    Py_XDECREF(pyarr$argnum);
    PyMem_Free((void *) buffer$argnum);
}

/*******************************************************
* Now define these typemaps for every numeric type
*******************************************************/

%enddef

TYPEMAP_ARGOUT(int,           NPY_INT   )
TYPEMAP_ARGOUT(SpiceInt,      NPY_INT   )
TYPEMAP_ARGOUT(SpiceBoolean,  NPY_INT   )
TYPEMAP_ARGOUT(long,          NPY_LONG  )
TYPEMAP_ARGOUT(double,        NPY_DOUBLE)
TYPEMAP_ARGOUT(SpiceDouble,   NPY_DOUBLE)

#undef TYPEMAP_ARGOUT

/*******************************************************************************
* Basic 3-D numeric typemaps for output
*       (type **OUT_ARRAY23, int *SIZE1, int *SIZE2, int *SIZE3)
* We only have a few left over from vectors.
*******************************************************************************/

%define TYPEMAP_ARGOUT(Type, Typecode) // Use to fill in numeric types below!

/***************************************************************
* (Type **OUT_ARRAY23, int *SIZE1, int *SIZE2, int *SIZE3)
***************************************************************/

%typemap(in, numinputs=0)
    (Type **OUT_ARRAY23, int *SIZE1, int *SIZE2, int *SIZE3)
        (PyArrayObject* pyarr=NULL, Type *buffer=NULL, int dimsize[3]),
    (Type **OUT_ARRAY23, SpiceInt *SIZE1, SpiceInt *SIZE2, SpiceInt *SIZE3)
        (PyArrayObject* pyarr=NULL, Type *buffer=NULL, int dimsize[3])
{
//      (Type **OUT_ARRAY23, int *SIZE1, int *SIZE2, int *SIZE3)

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
    (Type **OUT_ARRAY23, int *SIZE1, int *SIZE2, int *SIZE3),
    (Type **OUT_ARRAY23, SpiceInt *SIZE1, SpiceInt *SIZE2, SpiceInt *SIZE3)
{
//      (Type **OUT_ARRAY23, int *SIZE1, int *SIZE2, int *SIZE3)

    TEST_MALLOC_FAILURE(buffer$argnum);
    npy_intp dims[3] = {dimsize$argnum[0], dimsize$argnum[1], dimsize$argnum[2]};
    int nd = dims[0] == 0 ? 2 : 3;
    pyarr$argnum = create_array_with_owned_data(nd, &dims[3 - nd], Typecode, &buffer$argnum);
    TEST_MALLOC_FAILURE(pyarr$argnum);

    $result = SWIG_Python_AppendOutput($result, (PyObject *)pyarr$argnum);
    // AppendOutput steals the reference to the argument.
    pyarr$argnum = NULL;
}

%typemap(freearg)
    (Type **OUT_ARRAY23, int *SIZE1, int *SIZE2, int *SIZE3),
    (Type **OUT_ARRAY23, SpiceInt *SIZE1, SpiceInt *SIZE2, SpiceInt *SIZE3)
{
    Py_XDECREF(pyarr$argnum);
    PyMem_Free((void *) buffer$argnum);
}

/*******************************************************
* Now define these typemaps for every numeric type
*******************************************************/

%enddef

TYPEMAP_ARGOUT(double,      NPY_DOUBLE)
TYPEMAP_ARGOUT(SpiceDouble, NPY_DOUBLE)

#undef TYPEMAP_ARGOUT

/*******************************************************************************
* Basic INOUT typemaps for 1- and 2-dimensional arrays:
*    (int DIM1, Type *INOUT_ARRAY1)
*    (int DIM1, Type INOUT_ARRAY2[][ANY])
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
//      (Type *INOUT_ARRAY1)
    CONVERT_TO_CONTIGUOUS_ARRAY_WRITEABLE_COPY(Typecode, $input, 1, 1, pyarr)
    $1 = ($1_ltype) PyArray_DATA(pyarr);                        // ARRAY
}

%typemap(in)
    (int DIM1, Type *INOUT_ARRAY1)
        (PyArrayObject* pyarr=NULL),
    (int DIM1, Type INOUT_ARRAY1[])
        (PyArrayObject* pyarr=NULL)
{
//      (int DIM1, Type *INOUT_ARRAY1)
//  NOT CURRENTLY USED BY CSPICE

    CONVERT_TO_CONTIGUOUS_ARRAY_WRITEABLE_COPY(Typecode, $input, 1, 1, pyarr)
    $2 = ($2_ltype) PyArray_DATA(pyarr);                        // ARRAY
    $1 = (int) PyArray_DIM(pyarr, 0);                           // DIM1
}

%typemap(in)
    (int DIM1, Type INOUT_ARRAY2[][ANY])
        (PyArrayObject* pyarr=NULL)
{
//      (int DIM1, type INOUT_ARRAY2[][ANY])
//  NOT CURRENTLY USED BY CSPICE

    // NOT CURRENTLY USED
    CONVERT_TO_CONTIGUOUS_ARRAY_WRITABLE_COPY(Typecode, $input, 2, 2, pyarr)
    TEST_INVALID_ARRAY_SHAPE_x2D(pyarr, $2_dim1)
    $1 = (int) PyArray_DIM(pyarr, 0);                           // DIM1
    $2 = ($2_ltype) PyArray_DATA(pyarr);                        // ARRAY
}

%typemap(in)
    (int DIM2, Type *INOUT_ARRAY2)
        (PyArrayObject* pyarr=NULL)
{
//      (int DIM1, type INOUT_ARRAY2)
//  NOT CURRENTLY USED BY CSPICE

    CONVERT_TO_CONTIGUOUS_ARRAY_WRITABLE_COPY(Typecode, $input, 2, 2, pyarr)
    $1 = (int) PyArray_DIM(pyarr, 1);                           // DIM1
    $2 = ($2_ltype) PyArray_DATA(pyarr);                        // ARRAY
}

%typemap(argout)
    (Type *INOUT_ARRAY1),
    (int DIM1, Type *INOUT_ARRAY1),
    (int DIM1, Type INOUT_ARRAY1[]),
    (int DIM1, Type INOUT_ARRAY2[][ANY]),
    (int DIM2, Type *INOUT_ARRAY2)
{
    $result = SWIG_Python_AppendOutput($result, (PyObject *)pyarr$argnum);
    pyarr$argnum = NULL;
}

%typemap(freearg)
    (Type *INOUT_ARRAY1),
    (int DIM1, Type *INOUT_ARRAY1),
    (int DIM1, Type INOUT_ARRAY1[]),
    (int DIM1, Type INOUT_ARRAY2[][ANY]),
    (int DIM2, Type *INOUT_ARRAY2)
{
    Py_XDECREF(pyarr$argnum);
}

%enddef

// Define concrete examples of the TYPEMAP_INOUT macros
TYPEMAP_INOUT(char,          NPY_STRING)
TYPEMAP_INOUT(int,           NPY_INT   )
TYPEMAP_INOUT(SpiceInt,      NPY_INT   )
TYPEMAP_INOUT(SpiceBoolean,  NPY_INT   )
TYPEMAP_INOUT(long,          NPY_LONG  )
TYPEMAP_INOUT(double,        NPY_DOUBLE)
TYPEMAP_INOUT(SpiceDouble,   NPY_DOUBLE)

#undef TYPEMAP_INOUT


/*******************************************************************************
* Typemap for string input
*
* These typemaps handle string input.
*
*       (char *IN_STRING)
*       (char *CONST_STRING)
*       (char IN_STRING)
*
* The differences between the options are:
*
*       (char *IN_STRING): The string is taken as input. It is copied to ensure
*               that the Python string remains immutable.
*
*       (char *CONST_STRING): The string is taken as input. It is not copied so
*               one must ensure that it does not get changed by the C function.
*
*       (char IN_STRING): If the C function accepts a single character, not a
*               pointer to a string, any you wish to provide the Python input
*               as a string.
*******************************************************************************/

%define TYPEMAP_IN(Type) // Use to fill in types below

/***********************************************
* (char *CONST_STRING)
***********************************************/

%typemap(in) (Type *CONST_STRING) (PyObject* byte_string = NULL) {
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
* (char IN_STRING)
***********************************************/

%typemap(in) (Type IN_STRING) {
//      (Type IN_STRING)
    TEST_IS_STRING($input);
    int error  = SWIG_AsVal_char($input, &$1);
    RAISE_BAD_STRING_ON_ERROR(error);
 }

%typemap(argout) (Type IN_STRING) ""

%typemap(freearg) (Type IN_STRING) ""

/*******************************************************
* Now apply to all data types
*******************************************************/

%enddef

// Define concrete examples of the TYPEMAP_IN macros

TYPEMAP_IN(char)
TYPEMAP_IN(SpiceChar)
TYPEMAP_IN(ConstSpiceChar)

#undef TYPEMAP_IN

/*******************************************************************************
* String typemaps for input and output
*
* These typemaps allow C-format strings to be passed to the C function and for
* a string value to be returned.
*
*       (char INOUT_STRING[ANY])
*       (char *INOUT_STRING)
*
*       (int DIM1, char INOUT_STRING[ANY])
*       (int DIM1, char *INOUT_STRING)
*
*       (char INOUT_STRING[ANY], int DIM1)
*       (char *INOUT_STRING, int DIM1)
*
* The differences between the options are:
*
*       (char *INOUT_STRING): The string is taken as input. A buffer of the
*               size is used to construct the returned string.
*
*       (char INOUT_STRING[ANY]): The string is taken as input. A buffer of the
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
*       (char OUT_STRING[ANY])
*       (char OUT_STRING[ANY], int DIM1)
*       (int DIM1, char OUT_STRING[ANY])
*
* In each case, the dimensioned length of the string is defined in the SWIG
* interface by a number inside the brackets. The differences between the three
* options are:
*
*       (char OUT_STRING[ANY]): one argument to the C function of type char*
*               is consumed; no information about the string's dimensioned
*               length is passed to the function.
*
*       ((char OUT_STRING[ANY], int DIM1): two arguments to the C function are
*               consumed; the dimensioned length of the the character string
*               (which is one greater than the maximum allowed string length)
*               is passed as the next argument after the char* pointer.
*
*       ((int DIM1, char OUT_STRING[ANY]): two arguments to the C function are
*               consumed; the dimensioned length of the the character string is
*               passed as the argument before the char* pointer.
*
* Example:
*
* The C source code:
*
*       void yesno(int status, char *str, int lstr) {
*           if (status) {
*               strncpy(str, "yes", lstr);
*           } else {
*               strncpy(str, "no", lstr);
*           }
*       }
*
* In the interface file:
*
*       %apply (char OUT_STRING[ANY], int LEN) {(char str[4], int lstr)};
*       extern void yesno(int status, char str[4], int lstr);
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
* (char INOUT_STRING[ANY])
***********************************************/

%typemap(in)
    (Type INOUT_STRING[ANY])                                    // PATTERN
        (char *buffer = NULL, size_t dim1 = 0, PyObject *byte_string = NULL)
{
//      (char INOUT_STRING[ANY])
//  NOT CURRENTLY USED BY CSPICE

    TEST_IS_STRING($input);
    byte_string = PyUnicode_AsUTF8String($input);
    TEST_MALLOC_FAILURE(byte_string);

    buffer = byte_string_to_buffer_minimum_size(byte_string, $1_dim0, &dim1);
    TEST_MALLOC_FAILURE(buffer);

    $1 = ($1_ltype)buffer;                                      // STRING
}

/***********************************************
* (char INOUT_STRING[ANY], int DIM1)
***********************************************/

%typemap(in)
    (Type INOUT_STRING[ANY], int DIM1)                          // PATTERN
        (char *buffer = NULL, size_t dim1 = 0, PyObject *byte_string = NULL),
    (Type INOUT_STRING[ANY], SpiceInt DIM1)                     // PATTERN
        (char *buffer = NULL, size_t dim1 = 0, PyObject *byte_string = NULL)
{
//      (char INOUT_STRING[ANY], int DIM1)
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
* (int DIM1, char INOUT_STRING[ANY])
***********************************************/

%typemap(in)
    (int DIM1, Type INOUT_STRING[ANY])                          // PATTERN
        (char *buffer = NULL, size_t dim1 = 0, PyObject *byte_string = NULL),
    (SpiceInt DIM1, Type INOUT_STRING[ANY])                     // PATTERN
        (char *buffer = NULL, size_t dim1 = 0, PyObject *byte_string = NULL)
{
//      (int DIM1, char INOUT_STRING[ANY])

    TEST_IS_STRING($input);
    byte_string = PyUnicode_AsUTF8String($input);
    TEST_MALLOC_FAILURE(byte_string);

    buffer = byte_string_to_buffer_minimum_size(byte_string, $2_dim0, &dim1);
    TEST_MALLOC_FAILURE(buffer);

    $1 = ($1_type)dim1;                                         // DIM1
    $2 = buffer;                                                // STRING
}

/***********************************************
* (int DIM1, char *INOUT_STRING)
***********************************************/

%typemap(in)
    (int DIM1, Type *INOUT_STRING)                              // PATTERN
        (char *buffer = NULL, size_t dim1 = 0, PyObject *byte_string = NULL),
    (SpiceInt DIM1, Type *INOUT_STRING)                         // PATTERN
        (char *buffer = NULL, size_t dim1 = 0, PyObject *byte_string = NULL)
{
//      (int DIM1, char *INOUT_STRING)

    TEST_IS_STRING($input);
    byte_string = PyUnicode_AsUTF8String($input);
    TEST_MALLOC_FAILURE(byte_string);

    buffer = byte_string_to_buffer_minimum_size(byte_string, 0, &dim1);
    TEST_MALLOC_FAILURE(buffer);

    $2 = buffer;                                                // STRING
    $1 = ($1_type) dim1;                                        // DIM1
}

/***********************************************
* (char OUT_STRING[ANY])
***********************************************/

%typemap(in, numinputs=0)
    (Type OUT_STRING[ANY])                                      // PATTERN
        (Type *buffer = NULL, size_t dim1 = 0)
{
//      (char OUT_STRING[ANY])

    dim1 = max(1, $1_dim0);
    buffer = (char *) PyMem_Malloc((dim1 + 1) * sizeof(Type));
    TEST_MALLOC_FAILURE(buffer);

    buffer[0] = '\0';   // String begins empty
    $1 = buffer;                                                // STRING
}

/***********************************************
* (char OUT_STRING[ANY], int DIM1)
***********************************************/

%typemap(in, numinputs=0)
    (Type OUT_STRING[ANY], int DIM1)                            // PATTERN
        (Type *buffer = NULL, size_t dim1 = 0),
    (Type OUT_STRING[ANY], SpiceInt DIM1)                       // PATTERN
        (Type *buffer = NULL, size_t dim1 = 0)
{
//      (char OUT_STRING[ANY], int DIM1)
//  NOT CURRENTLY USED BY CSPICE

    dim1 = max(1, $2_dim0);
    buffer = ($1_ltype) PyMem_Malloc((dim1 + 1) * sizeof(Type));
    TEST_MALLOC_FAILURE(buffer);

    buffer[0] = '\0';   // String begins empty
    $1 = buffer;                                                // STRING
    $2 = ($2type)dim1;                                         // DIM1
}

/***********************************************
* (int DIM1, char OUT_STRING[ANY])
***********************************************/

%typemap(in, numinputs=0)
    (int DIM1, Type OUT_STRING[ANY])                            // PATTERN
        (Type *buffer = NULL, size_t dim1),
    (SpiceInt DIM1, Type OUT_STRING[ANY])                       // PATTERN
        (Type *buffer = NULL, size_t dim1)
{
//      (int DIM1, char OUT_STRING[ANY])

    dim1 = max(1, $2_dim0);
    buffer = (Type *) PyMem_Malloc((dim1 + 1) * sizeof(Type));
    TEST_MALLOC_FAILURE(buffer);

    buffer[0] = '\0';   // String begins empty
    $2 = buffer;                                                // STRING
    $1 = ($1_type)dim1;                                         // DIM1
}


/*******************************************************
* %typemap(argout)
* %typemap(freearg)
*******************************************************/

%typemap(argout)
    (Type INOUT_STRING[ANY]),
    (Type INOUT_STRING[ANY], int DIM1),
    (Type INOUT_STRING[ANY], SpiceInt DIM1),
    (int DIM1, Type INOUT_STRING[ANY]),
    (SpiceInt DIM1, Type INOUT_STRING[ANY]),
    (Type *INOUT_STRING),
    (Type *INOUT_STRING, int DIM1),
    (Type *INOUT_STRING, SpiceInt DIM1),
    (int DIM1, Type *INOUT_STRING),
    (SpiceInt DIM1, Type *INOUT_STRING),
    (Type OUT_STRING[ANY]),
    (Type OUT_STRING[ANY], int DIM1),
    (Type OUT_STRING[ANY], SpiceInt DIM1),
    (int DIM1, Type OUT_STRING[ANY]),
    (SpiceInt DIM1, Type OUT_STRING[ANY])
{
//      (... Type INOUT_STRING[ANY] ...)
//      (... Type *INOUT_STRING ...)
//      (... Type OUT_STRING[ANY] ...)

    buffer$argnum[dim1$argnum-1] = '\0';  // Make sure string is terminated
    PyObject *obj = PyUnicode_FromString((Type *) buffer$argnum);
    $result = SWIG_Python_AppendOutput($result, obj);
}

%typemap(freearg)
    (Type INOUT_STRING[ANY]),
    (Type INOUT_STRING[ANY], int DIM1),
    (Type INOUT_STRING[ANY], SpiceInt DIM1),
    (int DIM1, Type INOUT_STRING[ANY]),
    (SpiceInt DIM1, Type INOUT_STRING[ANY]),
    (Type *INOUT_STRING),
    (Type *INOUT_STRING, int DIM1),
    (Type *INOUT_STRING, SpiceInt DIM1),
    (int DIM1, Type *INOUT_STRING),
    (SpiceInt DIM1, Type *INOUT_STRING)
{
    PyMem_Free(buffer$argnum);
    Py_XDECREF(byte_string$argnum);
}

%typemap(freearg)
    (Type OUT_STRING[ANY]),
    (Type OUT_STRING[ANY], int DIM1),
    (Type OUT_STRING[ANY], SpiceInt DIM1),
    (INT DIM1, Type OUT_STRING[ANY]),
    (SpiceInt DIM1, Type OUT_STRING[ANY])
{
    PyMem_Free(buffer$argnum);
}



/*******************************************************
* Now apply to all data types
*******************************************************/

%enddef

// Define concrete examples of the  MAP_IN macros
TYPEMAP_INOUT_OUT(char)
TYPEMAP_INOUT_OUT(SpiceChar)

#undef TYPEMAP_INOUT_OUT

/*******************************************************************************
* String array typemaps for input
*
* These typemaps allow C-format string arrays to be passed into the C function.
*
*       (char *IN_STRINGS, int DIM1, int DIM2)
*       (int DIM1, int DIM2, char *IN_STRINGS)
*       (int DIM1, int DIM2, Type *INOUT_STRINGS)
*
* In all cases, the Strings are copied to an n x m array where n is the number
* of strings and m is longer than the longest string.
* For INOUT_STRINGS, the resulting buffer is converted back into an array of strings
* and returned to the user as a result.
*******************************************************************************/


%define TYPEMAP_IN(Type) // Use to fill in types below

/***********************************************************************
* (Type *IN_STRINGS, int DIM1, int DIM2)
***********************************************************************/

%typemap(in)
    (Type *IN_STRINGS, int DIM1, int DIM2)
        (PyObject *list = NULL, char *buffer = NULL),
    (Type *IN_STRINGS, SpiceInt DIM1, SpiceInt DIM2)
        (PyObject *list = NULL, char *buffer = NULL)
{
//      (Type *IN_STRINGS, int DIM1, int DIM2)

    HANDLE_TYPEMAP_IN_STRINGS($1, $*1_type, $2, $3, buffer, list)
}

/***********************************************************************
* (int DIM1, int DIM2, Type *IN_STRINGS)
***********************************************************************/

%typemap(in)
    (int DIM1, int DIM2, Type *IN_STRINGS)
        (PyObject *list = NULL, char *buffer = NULL),
    (SpiceInt DIM1, SpiceInt DIM2, Type *IN_STRINGS)
        (PyObject *list = NULL, char *buffer = NULL),
    (int DIM1, int DIM2, Type *INOUT_STRINGS)
        (PyObject *list = NULL, char *buffer = NULL),
    (SpiceInt DIM1, SpiceInt DIM2, Type *INOUT_STRINGS)
        (PyObject *list = NULL, char *buffer = NULL)
{
//      (int DIM1, int DIM2, Type *IN[OUT]_STRINGS)

    HANDLE_TYPEMAP_IN_STRINGS($3, $*3_type, $1, $2, buffer, list)
}

/***********************************************************************
* %typemap(argout)
* %typemap(freearg)
***********************************************************************/
%typemap(argout)
    (Type *IN_STRINGS, int DIM1, int DIM2),
    (Type *IN_STRINGS, SpiceInt DIM1, SpiceInt DIM2),
    (int DIM1, int DIM2, Type *IN_STRINGS),
    (SpiceInt DIM1, SpiceInt DIM2, Type *IN_STRINGS)
""

%typemap(argout)
    (int DIM1, int DIM2, Type *INOUT_STRINGS),
    (SpiceInt DIM1, SpiceInt DIM2, Type *INOUT_STRINGS)
{
//      (int DIM1, int DIM2, Type *INOUT_STRINGS)
    // We can reuse list$argnum, but first we need to free whatever is already there.
    Py_XDECREF(list$argnum);
    list$argnum = NULL;
    CONVERT_BUFFER_TO_ARRAY_OF_STRINGS(buffer$argnum, $1, $2, list$argnum);
    $result = SWIG_Python_AppendOutput($result, list$argnum);
    list$argnum = NULL;
}

%typemap(freearg)
    (Type *IN_STRINGS, int DIM1, int DIM2),
    (Type *IN_STRINGS, SpiceInt DIM1, SpiceInt DIM2),
    (int DIM1, int DIM2, Type *IN_STRINGS),
    (SpiceInt DIM1, SpiceInt DIM2, Type *IN_STRINGS),
    (int DIM1, int DIM2, Type *INOUT_STRINGS),
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
TYPEMAP_IN(char)
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
*       (char OUT_STRINGS[ANY][ANY], int DIM1, int DIM1, int *NSTRINGS)
*       (int DIM1, int DIM2, int *NSTRINGS, char OUT_STRINGS[ANY][ANY])
*
* As above, the maximum size and number of strings must be defined in the SWIG
* interface file (to ensure adequate memory is allocated). The typemaps could
* easily be written for alternative orderings of the arguments or for cases
* where one or more arguments are missing.
*******************************************************************************/

%define TYPEMAP_OUT(Type) // Use to fill in types below

/***********************************************************************
* (char OUT_STRINGS[ANY][ANY], int DIM1, int DIM2, int *NSTRINGS)
***********************************************************************/

%typemap(in,numinputs=0)
    (Type OUT_STRINGS[ANY][ANY], int DIM1, int DIM2, int *NSTRINGS)
        (Type *buffer, int dimsize[2], int nstrings),
    (Type OUT_STRINGS[ANY][ANY], SpiceInt DIM1, SpiceInt DIM2, SpiceInt *NSTRINGS)
        (Type *buffer, int dimsize[2], int nstrings)
{
//      (char OUT_STRINGS[ANY][ANY], int DIM1, int DIM2, int *NSTRINGS)
//  NOT CURRENTLY USED BY CSPICE

    nstrings = 0;
    dimsize[0] = $1_dim0;                                       // ARRAY_dim0
    dimsize[1] = $1_dim1;                                       // ARRAY_dim1
    if (dimsize[1] < 2) {
        dimsize[1] = 2;
    }

    buffer = (Type *) PyMem_Malloc(dimsize[0] * dimsize[1] * sizeof(Type));
    TEST_MALLOC_FAILURE(buffer);

    $1 = buffer;                                                // ARRAY
    $2 = dimsize[0];                                            // DIM1
    $3 = dimsize[1];                                            // DIM2
    $4 = &nstrings;                                             // NSTRINGS
}

/***********************************************************************
* (int DIM1, int DIM2, int *NSTRINGS, char OUT_STRINGS[ANY][ANY])
***********************************************************************/

%typemap(in,numinputs=0)
    (int DIM1, int DIM2, int *NSTRINGS, Type OUT_STRINGS[ANY][ANY])
        (Type *buffer, int dimsize[2], int nstrings, PyObject* list = NULL),
    (SpiceInt DIM1, SpiceInt DIM2, SpiceInt *NSTRINGS, Type OUT_STRINGS[ANY][ANY])
        (Type *buffer, int dimsize[2], int nstrings, PyObject* list = NULL)
{
//      (int DIM1, int DIM2, int *NSTRINGS, char OUT_STRINGS[ANY][ANY])

    nstrings = 0;
    dimsize[0] = $4_dim0;                                       // ARRAY_dim0
    dimsize[1] = $4_dim1;                                       // NARRAY_dim1
    if (dimsize[1] < 2) {
        dimsize[1] = 2;
    }

    buffer = (Type *) PyMem_Malloc(dimsize[0] * dimsize[1] * sizeof(Type));
    TEST_MALLOC_FAILURE(buffer);

    $4 = buffer;                                                // ARRAY
    $1 = dimsize[0];                                            // DIM1
    $2 = dimsize[1];                                            // DIM2
    $3 = &nstrings;                                             // NSTRINGS
}

/***********************************************************************
* %typemap(argout)
* %typemap(freearg)
***********************************************************************/

%typemap(argout)
    (Type OUT_STRINGS[ANY][ANY], int DIM1, int DIM2, int *NSTRINGS),
    (Type OUT_STRINGS[ANY][ANY], SpiceInt DIM1, SpiceInt DIM2, SpiceInt *NSTRINGS),
    (int DIM1, int DIM2, int *NSTRINGS, Type OUT_STRINGS[ANY][ANY]),
    (SpiceInt DIM1, SpiceInt DIM2, SpiceInt *NSTRINGS, Type OUT_STRINGS[ANY][ANY])
{
//      (char OUT_STRINGS[ANY][ANY], int DIM1, int DIM2, int *NSTRINGS)

    CONVERT_BUFFER_TO_ARRAY_OF_STRINGS(buffer$argnum, nstrings$argnum, dimsize$argnum[1], list$argnum)
    $result = SWIG_Python_AppendOutput($result, list$argnum);
    list$argnum = NULL;
}

%typemap(freearg)
    (Type OUT_STRINGS[ANY][ANY], int DIM1, int DIM2, int *NSTRINGS),
    (Type OUT_STRINGS[ANY][ANY], SpiceInt DIM1, SpiceInt DIM2, SpiceInt *NSTRINGS),
    (int DIM1, int DIM2, int *NSTRINGS, Type OUT_STRINGS[ANY][ANY]),
    (SpiceInt DIM1, SpiceInt DIM2, SpiceInt *NSTRINGS, Type OUT_STRINGS[ANY][ANY])
{
//      (char OUT_STRINGS[ANY][ANY], int DIM1, int DIM2, int *NSTRINGS)
    PyMem_Free((void *) buffer$argnum);
    Py_XDECREF(list$argnum);
}

/*******************************************************
* Now apply to all data types
*******************************************************/

%enddef

// Define concrete examples of the TYPEMAP_IN macros
TYPEMAP_OUT(char)
TYPEMAP_OUT(SpiceChar)

#undef TYPEMAP_OUT

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
        (Type value)
{
//      (Type *OUTPUT)
    $1 = &value;
}

%typemap(argout)
    (Type *OUTPUT)
{
//      (Type *OUTPUT)

    $result = SWIG_Python_AppendOutput($result, converter);
}

%typemap(freearg) (Type *OUTPUT) ""

%enddef

TYPEMAP_ARGOUT(SpiceBoolean, PyBool_FromLong(value$argnum))
TYPEMAP_ARGOUT(PyObject*, (value$argnum))

#undef TYPEMAP_ARGOUT

/*******************************************************************************
* Typemap for return values. They also check for error status and raise a
* runtime exception if necessary.
*
*       (void   RETURN_VOID   )
*       (int    RETURN_BOOLEAN)
*       (int    RETURN_INT    )
*       (double RETURN_DOUBLE )
*       (char  *RETURN_STRING )
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
    (int RETURN_BOOLEAN),
    (SpiceBoolean RETURN_BOOLEAN) {

    TEST_FOR_EXCEPTION;
    $result = SWIG_Python_AppendOutput($result, PyBool_FromLong((long) $1));
}

%typemap(out)
    (int RETURN_INT),
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

// Special handler just for direct calls to sigerr()
%typemap(out) (void RETURN_VOID_SIGERR) {
    RAISE_SIGERR_EXCEPTION;
    Py_XDECREF($result);
    Py_INCREF(Py_None);
    $result = Py_None;
}

/*******************************************************************************
*******************************************************************************/
#if 0
%typemap(in, numinputs=0)
    (SWIGTYPE*)
{
     ERROR The argument "$1_type $1_name" in "$symname" didnt match any template!!
}
#endif
