/***********************************************************************
* -Procedure appndc_c ( Append an item to a character cell )
*
* -Abstract
* 
* Append an item to a character cell.
* 
* void appndc_c (
*       ConstSpiceChar   * item,
*       SpiceCell        * cell  )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* item       I   The item to append.
* cell      I-O  The cell to which item will be appended.
***********************************************************************/


/***********************************************************************
* -Procedure appndd_c ( Append an item to a double precision cell )
*
* -Abstract
* 
* Append an item to a double precision cell.
* 
* void appndd_c (
*       SpiceDouble     item,
*       SpiceCell     * cell )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* item       I   The item to append.
* cell      I-O  The cell to which item will be appended.
***********************************************************************/


/***********************************************************************
* -Procedure appndi_c ( Append an item to an integer cell )
*
* -Abstract
* 
* Append an item to an integer cell.
* 
* void appndi_c (
*       SpiceInt        item,
*       SpiceCell     * cell )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* item       I   The item to append.
* cell      I-O  The cell to which `item' will be appended.
***********************************************************************/


/***********************************************************************
* -Procedure card_c ( Cardinality of a cell )
*
* -Abstract
* 
* Return the cardinality (current number of elements) in a
* cell of any data type.
* 
* SpiceInt card_c (
*       SpiceCell  * cell )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* cell       I   Input cell.
***********************************************************************/


/***********************************************************************
* -Procedure clearc_c ( Clear a two-dimensional character array )
*
* -Abstract
* 
* Fill a two-dimensional character array with blank strings.
* 
* void clearc_c (
*       SpiceInt            ndim,
*       SpiceInt            arrlen,
*       void              * array   )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* ndim       I   Number of rows of `array' to be set to blank.
* arrlen     I   Common length of the strings in `array'.
* array      O   Two-dimensional character array to be filled.
***********************************************************************/


/***********************************************************************
* -Procedure cleard_c ( Clear a double precision array )
*
* -Abstract
* 
* Fill a double precision array with zeros.
* 
* void cleard_c (
*       SpiceInt       ndim,
*       SpiceDouble  * array )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* ndim       I   The number of elements of `array' which are to be
* set to zero.
* array      O   Double precision array to be filled.
***********************************************************************/


/***********************************************************************
* -Procedure cleari_c ( Clear an integer array )
*
* -Abstract
* 
* Fill an integer array with zeros.
* 
* void cleari_c (
*       SpiceInt            ndim,
*       SpiceInt            array[] )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* ndim       I   The number of elements of `array' which are to be
* set to zero.
* array      O   Integer array to be filled.
***********************************************************************/


/***********************************************************************
* -Procedure copy_c ( Copy a SPICE cell )
*
* -Abstract
* 
* Copy the contents of a SpiceCell of any data type to another
* cell of the same type.
* 
* void copy_c (
*       SpiceCell   * cell,
*       SpiceCell   * copy  )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* cell       I   Cell to be copied.
* copy       O   New cell.
***********************************************************************/


/***********************************************************************
* -Procedure diff_c ( Difference of two sets )
*
* -Abstract
* 
* Take the difference of two sets of any data type to form a third
* set.
* 
* void diff_c (
*       SpiceCell   * a,
*       SpiceCell   * b,
*       SpiceCell   * c  )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* a          I   First input set.
* b          I   Second input set.
* c          O   Difference of `a' and `b'.
***********************************************************************/


/***********************************************************************
* -Procedure elemc_c ( Element of a character set )
*
* -Abstract
* 
* Determine whether an item is an element of a character set.
* 
* SpiceBoolean elemc_c (
*       ConstSpiceChar  * item,
*       SpiceCell       * a    )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* item       I   Item to be tested.
* a          I   Set to be tested.
***********************************************************************/


/***********************************************************************
* -Procedure elemd_c ( Element of a double precision set )
*
* -Abstract
* 
* Determine whether an item is an element of a double precision set.
* 
* SpiceBoolean elemd_c (
*       SpiceDouble     item,
*       SpiceCell     * a    )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* item       I   Item to be tested.
* a          I   Set to be tested.
***********************************************************************/


/***********************************************************************
* -Procedure elemi_c ( Element of an integer set )
*
* -Abstract
* 
* Determine whether an item is an element of an integer set.
* 
* SpiceBoolean elemi_c (
*       SpiceInt        item,
*       SpiceCell     * a    )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* item       I   Item to be tested.
* a          I   Set to be tested.
***********************************************************************/


/***********************************************************************
* -Procedure eqstr_c ( Equivalent strings )
*
* -Abstract
* 
* Determine whether two strings are equivalent.
* 
* SpiceBoolean eqstr_c (
*       ConstSpiceChar    * a,
*       ConstSpiceChar    * b )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* a,
* b          I   Arbitrary character strings.
***********************************************************************/


/***********************************************************************
* -Procedure exists_c ( Does the file exist? )
*
* -Abstract
* 
* Determine whether a file exists.
* 
* SpiceBoolean exists_c (
*       ConstSpiceChar  * fname )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* fname      I   Name of the file in question.
***********************************************************************/


/***********************************************************************
* -Procedure filld_c ( Fill a double precision array )
*
* -Abstract
* 
* Fill a double precision array with a specified value.
* 
* void filld_c (
*       SpiceDouble         value,
*       SpiceInt            ndim,
*       SpiceDouble         array[] )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* value      I   Double precision value to be placed in all the
* elements of `array'.
* ndim       I   The number of elements in `array'.
* array      O   Double precision array which is to be filled.
***********************************************************************/


/***********************************************************************
* -Procedure filli_c ( Fill an integer array )
*
* -Abstract
* 
* Fill an integer array with a specified value.
* 
* void filli_c (
*       SpiceInt            value,
*       SpiceInt            ndim,
*       SpiceInt            array[] )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* value      I   Integer value to be placed in all the elements of
* `array'.
* ndim       I   The number of elements in `array'.
* array      O   Integer array which is to be filled.
***********************************************************************/


/***********************************************************************
* -Procedure ftncls_c ( Close file designated by Fortran unit )
*
* -Abstract
* 
* Close a file designated by a Fortran-style integer logical unit.
* 
* void ftncls_c (
*       SpiceInt unit )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* unit       I   Fortran-style logical unit.
***********************************************************************/


/***********************************************************************
* -Procedure getcml_c ( Get the command line )
*
* -Abstract
* 
* Store the contents of argv and argc for later access..
* 
* void getcml_c (
*       SpiceInt     * argc,
*       SpiceChar  *** argv )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* argc       O   The number of command line arguments.
* argv       O   The vector of command line arguments.
***********************************************************************/


/***********************************************************************
* -Procedure gfbail_c ( GF, interrupt signal indicator )
*
* -Abstract
* 
* Indicate whether an interrupt signal (SIGINT) has been received.
* 
* SpiceBoolean gfbail_c (
*       )
*
* -Brief_I/O
*
***********************************************************************/


/***********************************************************************
* -Procedure gfclrh_c ( GF, clear interrupt signal handler status )
*
* -Abstract
* 
* Clear the interrupt signal handler status, so that future calls
* to gfbail_c will indicate no interrupt was received.
* 
* void gfclrh_c (
*       void )
*
* -Brief_I/O
*
* }
***********************************************************************/


/***********************************************************************
* -Procedure gfinth_c ( GF, interrupt signal handler )
*
* -Abstract
* 
* Respond to the interrupt signal SIGINT: save an indication
* that the signal has been received. This routine restores
* itself as the handler for SIGINT.
* 
* void gfinth_c (
*       int sigcode )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* sigcode    I   Interrupt signal ID code.
***********************************************************************/


/***********************************************************************
* -Procedure gfrefn_c ( GF, default refinement estimator )
*
* -Abstract
* 
* Estimate, using a bisection method, the next abscissa value at
* which a state change occurs. This is the default GF refinement
* method.
* 
* void gfrefn_c (
*       SpiceDouble     t1,
*       SpiceDouble     t2,
*       SpiceBoolean    s1,
*       SpiceBoolean    s2,
*       SpiceDouble   * t  )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* t1         I   One of two values bracketing a state change.
* t2         I   The other value that brackets a state change.
* s1         I   State at `t1'.
* s2         I   State at `t2'.
* t          O   New value at which to check for transition.
***********************************************************************/


/***********************************************************************
* -Procedure gfrepf_c ( GF, progress report finalization )
*
* -Abstract
* 
* Finish a GF progress report.
* 
* void gfrepf_c (
*       void )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* None.
***********************************************************************/


/***********************************************************************
* -Procedure gfrepi_c ( GF, progress report initialization )
*
* -Abstract
* 
* Initialize a search progress report.
* 
* void gfrepi_c (
*       SpiceCell        * window,
*       ConstSpiceChar   * begmss,
*       ConstSpiceChar   * endmss  )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* MXBEGM     P   Maximum progress report message prefix length.
* MXENDM     P   Maximum progress report message suffix length.
* window     I   A window over which a job is to be performed.
* begmss     I   Beginning of the text portion of output message.
* endmss     I   End of the text portion of output message.
***********************************************************************/


/***********************************************************************
* -Procedure gfrepu_c ( GF, progress report update )
*
* -Abstract
* 
* Tell the progress reporting system how far a search has
* progressed.
* 
* void gfrepu_c (
*       SpiceDouble ivbeg,
*       SpiceDouble ivend,
*       SpiceDouble time  )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* ivbeg      I   Start time of work interval.
* ivend      I   End time of work interval.
* time       I   Current time being examined in the search process.
***********************************************************************/


/***********************************************************************
* -Procedure gfsstp_c ( Geometry finder set step size )
*
* -Abstract
* 
* Set the step size to be returned by gfstep_c.
* 
* void gfsstp_c (
*       SpiceDouble  step )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* step       I   Time step to take.
***********************************************************************/


/***********************************************************************
* -Procedure gfstep_c ( Geometry finder step size )
*
* -Abstract
* 
* Return the time step set by the most recent call to gfsstp_c.
* 
* void gfstep_c (
*       SpiceDouble    time,
*       SpiceDouble  * step )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* time       I   Ignored ET value.
* step       O   Time step to take.
***********************************************************************/


/***********************************************************************
* -Procedure gfudb_c ( GF, user defined boolean )
*
* -Abstract
* 
* Perform a GF search on a user defined boolean quantity.
* 
* -Abstract
* 
* User defined geometric boolean function:
* 
* void gfudb_c (
*       void            ( * udfuns ) ( SpiceDouble       et,
*       SpiceDouble     * value ),
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* SPICE_GF_CNVTOL
* P   Convergence tolerance.
* udfuns     I   Name of the routine that computes a scalar
* quantity corresponding to an `et'.
* udfunb     I   Name of the routine returning the boolean value
* corresponding to an `et'.
* step       I   Constant step size in seconds for finding geometric
* events.
* cnfine    I-O  SPICE window to which the search is restricted.
* result     O   SPICE window containing results.
***********************************************************************/


/***********************************************************************
* -Procedure gfuds_c ( GF, user defined scalar )
*
* -Abstract
* 
* Perform a GF search on a user defined scalar quantity.
* 
* -Abstract
* 
* User defined geometric quantity function. In this case,
* the range rate from the sun to the Moon at TDB time `et'.
* 
* void gfuds_c (
*       void             ( * udfuns ) ( SpiceDouble       et,
*       SpiceDouble     * value ),
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* SPICE_GF_CNVTOL
* P   Convergence tolerance.
* udfuns     I   Name of the routine that computes a scalar
* quantity corresponding to an `et'.
* udqdec     I   Name of the routine that computes whether the
* scalar quantity is decreasing.
* relate     I   Operator that either looks for an extreme value
* (max, min, local, absolute) or compares the
* geometric quantity value and a number.
* refval     I   Value used as reference for scalar quantity
* condition.
* adjust     I   Allowed variation for absolute extremal
* geometric conditions.
* step       I   Step size used for locating extrema and roots.
* nintvls    I   Workspace window interval count.
* cnfine    I-O  SPICE window to which the search is confined.
* result     O   SPICE window containing results.
***********************************************************************/


/***********************************************************************
* -Procedure insrtc_c ( Insert an item into a character set )
*
* -Abstract
* 
* Insert an item into a character set.
* 
* void insrtc_c (
*       ConstSpiceChar  * item,
*       SpiceCell       * a    )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* item       I   Item to be inserted.
* a         I-O  Insertion set.
***********************************************************************/


/***********************************************************************
* -Procedure insrtd_c ( Insert an item into a double precision set )
*
* -Abstract
* 
* Insert an item into a double precision set.
* 
* void insrtd_c (
*       SpiceDouble     item,
*       SpiceCell     * a    )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* item       I   Item to be inserted.
* a         I-O  Insertion set.
***********************************************************************/


/***********************************************************************
* -Procedure insrti_c ( Insert an item into an integer set )
*
* -Abstract
* 
* Insert an item into an integer set.
* 
* void insrti_c (
*       SpiceInt        item,
*       SpiceCell     * a    )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* item       I   Item to be inserted.
* a         I-O  Insertion set.
***********************************************************************/


/***********************************************************************
* -Procedure inter_c ( Intersection of two sets )
*
* -Abstract
* 
* Intersect two sets of any data type to form a third set.
* 
* void inter_c (
*       SpiceCell   * a,
*       SpiceCell   * b,
*       SpiceCell   * c  )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* a          I   First input set.
* b          I   Second input set.
* c          O   Intersection of `a' and `b'.
***********************************************************************/


/***********************************************************************
* -Procedure lastnb_c ( Last non-blank character )
*
* -Abstract
* 
* Return the zero based index of the last non-blank character in
* a character string.
* 
* SpiceInt lastnb_c (
*       ConstSpiceChar * string )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* string     I   Input character string.
***********************************************************************/


/***********************************************************************
* -Procedure lcase_c ( Convert to lowercase )
*
* -Abstract
* 
* Convert the characters in a string to lowercase.
* 
* void lcase_c (
*       SpiceChar       * in,
*       SpiceInt          outlen,
*       SpiceChar       * out    )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* in         I   Input string.
* outlen     I   Maximum length of output string.
* out        O   Output string, all lowercase.
***********************************************************************/


/***********************************************************************
* -Procedure lparss_c (Parse a list of items; return a set)
*
* -Abstract
* 
* Parse a list of items separated by multiple delimiters, placing the
* resulting items into a set.
* 
* void lparss_c (
*       ConstSpiceChar   * list,
*       ConstSpiceChar   * delims,
*       SpiceCell        * set     )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* list       I    List of items delimited by delims.
* delims     I    Single characters which delimit items.
* set        O    Set containing items in the list, left justified.
***********************************************************************/


/***********************************************************************
* -Procedure maxd_c ( Maximum of a set of double precision values )
*
* -Abstract
* 
* Find the maximum of a set of double precision values.
* 
* SpiceDouble maxd_c (
*       SpiceInt  n,  ... )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* n          I   The number of double precision values to compare.
* ...        I   The numbers to be compared, separated by commas.
***********************************************************************/


/***********************************************************************
* -Procedure maxi_c ( Maximum of a set of integers )
*
* -Abstract
* 
* Find the maximum of a set of integers.
* 
* SpiceInt maxi_c (
*       SpiceInt n,  ... )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* n          I   The number of integer values to compare.
* ...        I   The numbers to be compared, separated by commas.
***********************************************************************/


/***********************************************************************
* -Procedure mind_c ( Minimum of a set of double precision values )
*
* -Abstract
* 
* Find the minimum of a set of double precision values.
* 
* SpiceDouble mind_c (
*       SpiceInt  n,  ... )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* n          I   The number of double precision values to compare.
* ...        I   The numbers to be compared, separated by commas.
***********************************************************************/


/***********************************************************************
* -Procedure mini_c ( minimum of a set of integers )
*
* -Abstract
* 
* Find the minimum of a set of integers.
* 
* SpiceInt mini_c (
*       SpiceInt n,  ... )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* n          I   The number of integer values to compare.
* ...        I   The numbers to be compared, separated by commas.
***********************************************************************/


/***********************************************************************
* -Procedure moved_c  ( Move a double precision array to another )
*
* -Abstract
* 
* Copy the elements of one double precision array into another
* array.
* 
* void moved_c (
*       ConstSpiceDouble    arrfrm[],
*       SpiceInt            ndim,
*       SpiceDouble         arrto[] )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* arrfrm     I   Double precision array to be moved.
* ndim       I   Number of elements to copy, i.e. the dimension
* of `arrfrm' and `arrto'.
* arrto      O   Destination array.
***********************************************************************/


/***********************************************************************
* -Procedure ordc_c ( The ordinal position of an element in a set )
*
* -Abstract
* 
* Return the ordinal position of a given item in a set. If the
* item does not appear in the set, return -1.
* 
* SpiceInt ordc_c (
*       ConstSpiceChar  * item,
*       SpiceCell       * set   )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* item       I   An item to locate within a set.
* set        I   A set to search for a given item.
***********************************************************************/


/***********************************************************************
* -Procedure ordd_c ( The ordinal position of an element in a set )
*
* -Abstract
* 
* Return the ordinal position of a given item in a set. If the
* item does not appear in the set, return -1.
* 
* SpiceInt ordd_c (
*       SpiceDouble     item,
*       SpiceCell     * set  )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* item       I   An item to locate within a set.
* set        I   A set to search for a given item.
***********************************************************************/


/***********************************************************************
* -Procedure ordi_c ( The ordinal position of an element in a set )
*
* -Abstract
* 
* Return the ordinal position of a given item in a set. If the
* item does not appear in the set, return -1.
* 
* SpiceInt ordi_c (
*       SpiceInt        item,
*       SpiceCell     * set   )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* item       I   An item to locate within a set.
* set        I   A set to search for a given item.
***********************************************************************/


/***********************************************************************
* -Procedure putcml_c ( Get the command line )
*
* -Abstract
* 
* Store the contents of argv and argc for later access..
* 
* void putcml_c (
*       SpiceInt      argc,
*       SpiceChar  ** argv )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* argc       I   The number of command line arguments.
* argv       I   The vector of command line arguments.
***********************************************************************/


/***********************************************************************
* -Procedure rdtext_c ( Read a line from a text file )
*
* -Abstract
* 
* Read the next line of text from a text file.
* 
* void rdtext_c (
*       ConstSpiceChar * file,
*       SpiceInt         lineln,
*       SpiceChar      * line,
*       SpiceBoolean   * eof    )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* file       I   Name of text file.
* lineln     I   Available room in output line.
* line       O   Next line from the text file.
* eof        O   End-of-file indicator.
***********************************************************************/


/***********************************************************************
* -Procedure removc_c ( Remove an item from a character set )
*
* -Abstract
* 
* Remove an item from a character set.
* 
* void removc_c (
*       ConstSpiceChar  * item,
*       SpiceCell       * a    )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* item       I   Item to be removed.
* a         I-O  Removal set.
***********************************************************************/


/***********************************************************************
* -Procedure removd_c ( Remove an item from a double precision set )
*
* -Abstract
* 
* Remove an item from a double precision set.
* 
* void removd_c (
*       SpiceDouble     item,
*       SpiceCell     * a    )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* item       I   Item to be removed.
* a         I-O  Removal set.
***********************************************************************/


/***********************************************************************
* -Procedure removi_c ( Remove an item from an integer set )
*
* -Abstract
* 
* Remove an item from an integer set.
* 
* void removi_c (
*       SpiceInt        item,
*       SpiceCell     * a    )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* item       I   Item to be removed.
* a         I-O  Removal set.
***********************************************************************/


/***********************************************************************
* -Procedure scard_c ( Set the cardinality of a cell )
*
* -Abstract
* 
* Set the cardinality of a SPICE cell of any data type.
* 
* void scard_c (
*       SpiceInt      card,
*       SpiceCell   * cell  )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* card       I   Cardinality of (number of elements in) the cell.
* cell       O   The cell.
***********************************************************************/


/***********************************************************************
* -Procedure sdiff_c ( Symmetric difference of two sets )
*
* -Abstract
* 
* Take the symmetric difference of two sets of any data type to form a
* third set.
* 
* void sdiff_c (
*       SpiceCell   * a,
*       SpiceCell   * b,
*       SpiceCell   * c  )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* a          I   First input set.
* b          I   Second input set.
* c          O   Symmetric difference of `a' and `b'.
***********************************************************************/


/***********************************************************************
* -Procedure set_c ( Compare sets )
*
* -Abstract
* 
* Compare two sets of any data type, as indicated by a relational operator.
* 
* SpiceBoolean set_c (
*       SpiceCell        * a,
*       ConstSpiceChar   * op,
*       SpiceCell        * b   )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* a          I   First set.
* op         I   Comparison operator.
* b          I   Second set.
***********************************************************************/


/***********************************************************************
* -Procedure size_c ( Size of a cell )
*
* -Abstract
* 
* Return the size (maximum cardinality) of a SPICE cell of any
* data type.
* 
* SpiceInt size_c (
*       SpiceCell  * cell )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* cell       I   Input cell.
***********************************************************************/


/***********************************************************************
* -Procedure ssize_c ( Set the size of a cell )
*
* -Abstract
* 
* Set the size (maximum cardinality) of a SPICE cell of any data
* type.
* 
* void ssize_c (
*       SpiceInt      size,
*       SpiceCell   * cell  )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* size       I   Size (maximum cardinality) of the cell.
* cell       O   The cell.
***********************************************************************/


/***********************************************************************
* -Procedure ucase_c ( Convert to uppercase )
*
* -Abstract
* 
* Convert the characters in a string to uppercase.
* 
* void ucase_c (
*       SpiceChar   * in,
*       SpiceInt      outlen,
*       SpiceChar   * out    )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* in         I   Input string.
* outlen     I   Maximum length of output string.
* out        O   Output string, all uppercase.
***********************************************************************/


/***********************************************************************
* -Procedure uddc_c ( Derivative of function less than zero, df(x)/dx < 0 )
*
* -Abstract
* 
* Return SPICETRUE if the derivative of the callback function `udfunc'
* at a given abscissa value is negative.
* 
* void uddc_c (
*       void            ( * udfunc ) ( SpiceDouble    x,
*       SpiceDouble  * value ),
*       SpiceDouble         x,
*       SpiceDouble         dx,
*       SpiceBoolean      * isdecr )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* udfunc     I   The routine that computes the scalar value
* of interest.
* x          I   Independent variable of 'udfunc'.
* dx         I   Interval from 'x' for derivative calculation.
* isdecr     O   Boolean indicating if the derivative is negative.
***********************************************************************/


/***********************************************************************
* -Procedure uddf_c ( First derivative of a function, df(x)/dx )
*
* -Abstract
* 
* Calculate the first derivative of a caller-specified scalar
* function using a three-point estimation.
* 
* void uddf_c (
*       void             ( * udfunc ) ( SpiceDouble    et,
*       SpiceDouble  * value ),
*       SpiceDouble          x,
*       SpiceDouble          dx,
*       SpiceDouble        * deriv )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* udfunc     I   The routine that computes the scalar value
* of interest.
* x          I   Independent variable of `udfunc'.
* dx         I   Interval from `x' for derivative calculation.
* deriv      O   Approximate derivative of `udfunc' at `x'.
***********************************************************************/


/***********************************************************************
* -Procedure udf_c ( GF, dummy function )
*
* -Abstract
* 
* Serve as a dummy function for GF routines expecting an `udfuns'
* argument. It is a no-op routine with an argument signature
* matching `udfuns'.
* 
* void udf_c (
*       SpiceDouble   x,
*       SpiceDouble * value )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* x          I   Double precision value, unused.
* value      I   Double precision value, unused.
***********************************************************************/


/***********************************************************************
* -Procedure union_c ( Union of two sets )
*
* -Abstract
* 
* Compute the union of two sets of any data type to form a third set.
* 
* void union_c (
*       SpiceCell   * a,
*       SpiceCell   * b,
*       SpiceCell   * c  )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* a          I   First input set.
* b          I   Second input set.
* c          O   Union of `a' and `b'.
***********************************************************************/


/***********************************************************************
* -Procedure valid_c ( Validate a set )
*
* -Abstract
* 
* Create a valid SPICE set from a SPICE Cell of any data type.
* 
* void valid_c (
*       SpiceInt      size,
*       SpiceInt      n,
*       SpiceCell   * a    )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* size       I   Size (maximum cardinality) of the set.
* n          I   Initial no. of (possibly non-distinct) elements.
* a         I-O  Set to be validated.
***********************************************************************/


/***********************************************************************
* -Procedure wncard_c ( Cardinality of a double precision window )
*
* -Abstract
* 
* Return the cardinality (number of intervals) of a double
* precision window.
* 
* SpiceInt wncard_c (
*       SpiceCell  * window )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* window     I   Input window
***********************************************************************/


/***********************************************************************
* -Procedure wnfetd_c ( Fetch an interval from a DP window )
*
* -Abstract
* 
* Fetch a particular interval from a double precision window.
* 
* void wnfetd_c (
*       SpiceCell    * window,
*       SpiceInt       n,
*       SpiceDouble  * left,
*       SpiceDouble  * right   )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* window     I   Input window.
* n          I   Index of interval to be fetched.
* left,
* right      O   Left, right endpoints of the nth interval.
***********************************************************************/



/***********************************************************************
* -Procedure wnvald_c ( Validate a DP window )
*
* -Abstract
* 
* Form a valid double precision window from the contents
* of a window array.
* 
* void wnvald_c (
*       SpiceInt       size,
*       SpiceInt       n,
*       SpiceCell    * window )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* size       I   Size of window.
* n          I   Original number of endpoints.
* window    I-O  Input, output window.
***********************************************************************/


/**********************************************************************/
