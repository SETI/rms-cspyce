/***********************************************************************
* -Procedure azlcpo_c ( AZ/EL, constant position observer state )
*
* -Abstract
*
* Return the azimuth/elevation coordinates of a specified target
* relative to an "observer," where the observer has constant
* position in a specified reference frame. The observer's position
* is provided by the calling program rather than by loaded SPK
* files.
*
* void azlcpo_c (
*       ConstSpiceChar    * method,
*       ConstSpiceChar    * target,
*       SpiceDouble         et,
*       ConstSpiceChar    * abcorr,
*       SpiceBoolean        azccw,
*       SpiceBoolean        elplsz,
*       ConstSpiceDouble    obspos[3],
*       ConstSpiceChar    * obsctr,
*       ConstSpiceChar    * obsref,
*       SpiceDouble         azlsta[6],
*       SpiceDouble       * lt         )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* method     I   Method to obtain the surface normal vector; "ELLIPSOID" is the one and only option.
* target     I   Name of target ephemeris object.
* et         I   Observation epoch.
* abcorr     I   Aberration correction, "NONE", "LT", "LT+S", "CN", "CN+S", "XLT", "XLT+S", "XCN", or "XCN+S".
* azccw      I   Flag indicating how azimuth is measured, True for counterclockwise, False for clockwise.
* elplsz     I   Flag indicating how elevation is measured, True for increasing toward +Z, False for -Z.
* obspos     I   Observer position relative to center of motion.
* obsctr     I   Center of motion of observer.
* obsref     I   Body-fixed, body-centered frame of observer's center.
* azlsta     O   State of target with respect to observer,
*                in azimuth/elevation coordinates.
* lt         O   One way light time between target and observer.
***********************************************************************/

%rename (azlcpo) azlcpo_c;
%apply (void RETURN_VOID) {void azlcpo_c};
%apply (ConstSpiceDouble IN_ARRAY1[ANY]) {ConstSpiceDouble obspos[3]};
%apply (SpiceDouble OUT_ARRAY1[ANY]) {SpiceDouble azlsta[6]};

extern void azlcpo_c(
        ConstSpiceChar   *CONST_STRING,
        ConstSpiceChar   *CONST_STRING,
        SpiceDouble      et,
        ConstSpiceChar   *CONST_STRING,
        SpiceBoolean     azccw,
        SpiceBoolean     elplsz,
        ConstSpiceDouble obspos[3],
        ConstSpiceChar   *CONST_STRING,
        ConstSpiceChar   *CONST_STRING,
        SpiceDouble      azlsta[6],
        SpiceDouble      *OUTPUT
);

//Vector version
VECTORIZE_2s_d_s_2b_dX_2s__dN_d(azlcpo, azlcpo_c, 6)

//CSPYCE_TYPE:obsctr:body_name

/***********************************************************************
* -Procedure azlrec_c ( AZ/EL to rectangular coordinates )
*
* -Abstract
*
* Convert from range, azimuth and elevation of a point to
* rectangular coordinates.
*
* void azlrec_c (
*       SpiceDouble         range,
*       SpiceDouble         az,
*       SpiceDouble         el,
*       SpiceBoolean        azccw,
*       SpiceBoolean        elplsz,
*       SpiceDouble         rectan[3] )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* range      I   Distance of the point from the origin.
* az         I   Azimuth in radians.
* el         I   Elevation in radians.
* azccw      I   Flag indicating how azimuth is measured, True for counterclockwise, False for clockwise.
* elplsz     I   Flag indicating how elevation is measured, True for increasing toward +Z, False for -Z.
* rectan     O   Rectangular coordinates of a point.
***********************************************************************/

%rename (azlrec) azlrec_c;
%apply (void RETURN_VOID) {void azlrec_c};
%apply (SpiceDouble OUT_ARRAY1[ANY]) {SpiceDouble rectan[3]};

extern void azlrec_c(
        SpiceDouble  range,
        SpiceDouble  az,
        SpiceDouble  el,
        SpiceBoolean azccw,
        SpiceBoolean elplsz,
        SpiceDouble  rectan[3]
);

//Vector version
VECTORIZE_3d_2b__dN(azlrec, azlrec_c, 3)

/***********************************************************************
* -Procedure badkpv_c ( Bad Kernel Pool Variable )
*
* -Abstract
*
* Determine if a kernel pool variable is present and if so
* that it has the correct size and type.
*
* SpiceBoolean badkpv_c (
*       ConstSpiceChar    *caller,
*       ConstSpiceChar    *name,
*       ConstSpiceChar    *comp,
*       SpiceInt           size,
*       SpiceInt           divby,
*       SpiceChar          type   )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* caller     I   Name of the routine calling this routine.
* name       I   Name of a kernel pool variable.
* comp       I   Comparison operator, one of  "=", "<", ">", "=>", "<=".
* size       I   Expected size of the kernel pool variable.
* divby      I   A divisor of the size of the kernel pool variable.
* type       I   Expected type of the kernel pool variable, "C" for string, "N" for numeric.
***********************************************************************/

%rename (badkpv) badkpv_c;
%apply (SpiceBoolean RETURN_BOOLEAN) {SpiceBoolean badkpv_c};

extern void badkpv_c(
        ConstSpiceChar *CONST_STRING,
        ConstSpiceChar *CONST_STRING,
        ConstSpiceChar *CONST_STRING,
        SpiceInt       size,
        SpiceInt       divby,
        SpiceChar      IN_STRING
);

/***********************************************************************
* -Procedure brcktd_c ( Bracket a d.p. value within an interval )
*
* -Abstract
*
* Bracket a floating-point number. That is, given a number and an
* acceptable interval, make sure that the number is contained in the
* interval. (If the number is already in the interval, leave it
* alone. If not, set it to the nearest endpoint of the interval.)
*
* SpiceDouble brcktd_c (
*       SpiceDouble  number,
*       SpiceDouble  end1,
*       SpiceDouble  end2   )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* number     I   Number to be bracketed.
* end1       I   One of the bracketing endpoints for `number'.
* end2       I   The other bracketing endpoint for `number'.
***********************************************************************/

%rename (brcktd) brcktd_c;
%apply (SpiceDouble RETURN_DOUBLE) {SpiceDouble brcktd_c};

extern SpiceDouble brcktd_c(
        SpiceDouble number,
        SpiceDouble end1,
        SpiceDouble end2
);

//Vector version
VECTORIZE_3d__RETURN_d(brcktd, brcktd_c)

/***********************************************************************
* -Procedure brckti_c ( Bracket an integer value within an interval )
*
* -Abstract
*
* Bracket an integer number. That is, given a number and an
* acceptable interval, make sure that the number is contained in the
* interval. (If the number is already in the interval, leave it
* alone. If not, set it to the nearest endpoint of the interval.)
*
* SpiceInt brckti_c (
*       SpiceInt  number,
*       SpiceInt  end1,
*       SpiceInt  end2   )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* number     I   Number to be bracketed.
* end1       I   One of the bracketing endpoints for `number'.
* end2       I   The other bracketing endpoint for `number'.
* result     R   Bracketed value.
***********************************************************************/

%rename (brckti) brckti_c;
%apply (SpiceInt RETURN_INT) {SpiceInt brckti_c};

extern SpiceInt brckti_c(
        SpiceInt number,
        SpiceInt end1,
        SpiceInt end2
);

/***********************************************************************
* -Procedure bschoc_c ( Binary search with order vector, character )
*
* -Abstract
*
* Do a binary search for a given value within an array of character
* strings, accompanied by an order vector. Return the index of the
* matching array entry, or -1 if the key value is not found.
*
* SpiceInt bschoc_c (
*       ConstSpiceChar  * value,
*       SpiceInt          ndim,
*       SpiceInt          arrlen,
*       const void        array[][],
*       ConstSpiceInt   * order    )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* value      I   Key value to be found in `array'.
* ndim       I   Dimension of `array'.
* arrlen     I   Declared length of the strings in `array'.
* array      I   Character string array to search.
* order      I   Order vector.
* index      R   Index of value in array.
***********************************************************************/

%rename (bschoc) bschoc_c;
%apply (SpiceInt RETURN_INT) {SpiceInt bschoc_c};
%apply (SpiceInt DIM1, SpiceInt DIM2, ConstSpiceChar *IN_STRINGS)
                {(SpiceInt ndim, SpiceInt arrlen, ConstSpiceChar *array)};
%apply (ConstSpiceInt *IN_ARRAY1) {ConstSpiceInt *order};

extern SpiceInt bschoc_c(
        ConstSpiceChar *CONST_STRING,
        SpiceInt       ndim, SpiceInt arrlen, ConstSpiceChar *array,
        ConstSpiceInt  *order
);

/***********************************************************************
* -Procedure bschoi_c ( Binary search with order vector, integer )
*
* -Abstract
*
* Do a binary search for a given value within an integer array,
* accompanied by an order vector. Return the index of the
* matching array entry, or -1 if the key value is not found.
*
* SpiceInt bschoi_c (
*       SpiceInt          value,
*       SpiceInt          ndim,
*       ConstSpiceInt   * array,
*       ConstSpiceInt   * order  )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* value      I   Value to find in `array'.
* ndim       I   Dimension of `array'.
* array      I   Array to be searched.
* order      I   Order vector.
* index      R   Index of value in array.
***********************************************************************/

%rename (bschoi) bschoi_c;
%apply (SpiceInt RETURN_INT) {SpiceInt bschoi_c};
%apply (SpiceInt DIM1, ConstSpiceInt *IN_ARRAY1) {(SpiceInt ndim, ConstSpiceInt *array)};
%apply (ConstSpiceInt *IN_ARRAY1) {ConstSpiceInt *order};

extern SpiceInt bschoi_c(
        SpiceInt       value,
        SpiceInt       ndim,
        ConstSpiceInt  *array,
        ConstSpiceInt  *order
);

/***********************************************************************
* -Procedure bsrchc_c ( Binary search for a character string )
*
* -Abstract
*
* Do a binary search for a given value within a character string array,
* assumed to be in nondecreasing order. Return the index of the
* matching array entry, or -1 if the key value is not found.
*
* SpiceInt bsrchc_c (
*       ConstSpiceChar  * value,
*       SpiceInt          ndim,
*       SpiceInt          arrlen,
*       const void        array[][]   )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* value      I   Key value to be found in `array'.
* ndim       I   Dimension of `array'.
* arrlen     I   Declared length of the strings in `array'.
* array      I   Character string array to search.
* index      R   Index of value in array.
***********************************************************************/

%rename (bsrchc) bsrchc_c;
%apply (SpiceInt RETURN_INT) {SpiceInt bsrchc_c};
%apply (SpiceInt DIM1, SpiceInt DIM2, ConstSpiceChar *IN_STRINGS)
                    {(SpiceInt ndim, SpiceInt arrlen, ConstSpiceChar *array)};

extern SpiceInt bsrchc_c(
        ConstSpiceChar *CONST_STRING,
        SpiceInt       ndim, SpiceInt arrlen, ConstSpiceChar *array
);

/***********************************************************************
* -Procedure bsrchd_c ( Binary search for a double precision value )
*
* -Abstract
*
* Do a binary search for a given value within a floating-point
* array, assumed to be in nondecreasing order. Return the index of
* the matching array entry, or -1 if the key value is not found.
*
* SpiceInt bsrchd_c (
*       SpiceDouble          value,
*       SpiceInt             ndim,
*       ConstSpiceDouble   * array )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* value      I   Value to find in `array'.
* ndim       I   Dimension of `array'.
* array      I   Array to be searched.
* index      R   Index of value in array.
***********************************************************************/

%rename (bsrchd) bsrchd_c;
%apply (SpiceInt RETURN_INT) {SpiceInt bsrchd_c};
%apply (SpiceInt DIM1, ConstSpiceDouble *IN_ARRAY1) {(SpiceInt ndim, ConstSpiceDouble *array)};

extern SpiceInt bsrchd_c(
        SpiceDouble value,
        SpiceInt    ndim, ConstSpiceDouble *array
);

%{
    SpiceInt my_bsrchd_vector(
        SpiceDouble value,
        ConstSpiceDouble *array, SpiceInt ndim)
    {
        return bsrchd_c(value, ndim, array);
    }
%}

//Vector version
VECTORIZE_d_di__RETURN_i(bsrchd, my_bsrchd_vector)

/***********************************************************************
* -Procedure bsrchi_c ( Binary search for an integer value )
*
* -Abstract
*
* Do a binary search for a given value within an integer array,
* assumed to be in nondecreasing order. Return the index of the
* matching array entry, or -1 if the key value is not found.
*
* SpiceInt bsrchi_c (
*       SpiceInt          value,
*       SpiceInt          ndim,
*       ConstSpiceInt   * array )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* value      I   Value to find in `array'.
* ndim       I   Dimension of `array'.
* array      I   Array to be searched.
* index      R   Index of value in array.
***********************************************************************/

%rename (bsrchi) bsrchi_c;
%apply (SpiceInt RETURN_INT) {SpiceInt bsrchi_c};
%apply (SpiceInt DIM1, ConstSpiceInt *IN_ARRAY1) {(SpiceInt ndim, ConstSpiceInt *array)};

extern SpiceInt bsrchi_c(
        SpiceInt value,
        SpiceInt ndim, ConstSpiceInt *array
);

/***********************************************************************
* -Procedure chbder_c ( Derivatives of a Chebyshev expansion )
*
* -Abstract
*
* Return the value of a polynomial and its first `nderiv'
* derivatives, evaluated at the input `x', using the coefficients of
* the Chebyshev expansion of the polynomial.
*
* void chbder_c (
*       ConstSpiceDouble * cp,
*       SpiceInt           degp,
*       SpiceDouble        x2s[2],
*       SpiceDouble        x,
*       SpiceInt           nderiv,
*       SpiceDouble      * partdp,
*       SpiceDouble      * dpdxs )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* cp         I   degp+1 Chebyshev polynomial coefficients.
* degp       I   Degree of polynomial.
* x2s        I   Transformation parameters of polynomial.
* x          I   Value for which the polynomial is to be evaluated.
* nderiv     I   The number of derivatives to compute.
* partdp    I-O  Workspace provided for computing derivatives.
* dpdxs      O   Array of the derivatives of the polynomial.
***********************************************************************/

%rename (chbder) my_chbder_c;
%apply (void RETURN_VOID) {void my_chbder_c};
%apply (ConstSpiceDouble *IN_ARRAY1, SpiceInt DIM1) {(ConstSpiceDouble *cp, SpiceInt deg_plus_1)};
%apply (SpiceDouble IN_ARRAY1[ANY]) {SpiceDouble x2s[2]};
%apply (SpiceDouble **OUT_ARRAY1, SpiceInt *SIZE1) {(SpiceDouble **dpdxs, SpiceInt *n)};

// Copied from vectorize.i
%apply (ConstSpiceDouble *IN_ARRAY12, SpiceInt DIM1, SpiceInt DIM2)
                    {(ConstSpiceDouble *in21, SpiceInt in21_dim1, SpiceInt in21_dim2)};
%apply (ConstSpiceDouble *IN_ARRAY01, SpiceInt DIM1)
                    {(ConstSpiceDouble *in12, SpiceInt in12_dim1)};
%apply (SpiceDouble **OUT_ARRAY12, SpiceInt *SIZE1, SpiceInt *SIZE2)
                    {(SpiceDouble **out21, SpiceInt *out21_dim1, SpiceInt *out21_dim2)};

%inline %{
    void my_chbder_c(
        ConstSpiceDouble *cp, SpiceInt deg_plus_1,
        SpiceDouble      x2s[2],
        SpiceDouble      x,
        SpiceInt         nderiv,
        SpiceDouble      **dpdxs, SpiceInt *n)
    {
        int nderiv_plus_1 = nderiv + 1;

        *n = nderiv_plus_1;
        *dpdxs = my_malloc(nderiv_plus_1, "chbder");
        SpiceDouble *partdp = my_malloc(3 * nderiv_plus_1, "chbder");
        if (*dpdxs && partdp) {
            chbder_c(cp, deg_plus_1 - 1, x2s, x, nderiv, partdp, *dpdxs);
        }
        PyMem_Free(partdp);
    }

    // This function doesn't fit any of our vectorization templates, because
    // the rightmost dimension of the returned axis is variable.

    void chbder_vector(
        ConstSpiceDouble *in21, SpiceInt in21_dim1, SpiceInt in21_dim2,
        SpiceDouble x2s[2],
        ConstSpiceDouble *in12, SpiceInt in12_dim1,
        SpiceInt nderiv,
        SpiceDouble **out21, SpiceInt *out21_dim1, SpiceInt *out21_dim2)
    {
        char *my_name = "chbder_vector";

        // in21 is cp
        // in12 is x
        // out21 is dpdxs

        int nderiv_plus_1 = nderiv + 1;
        int degp = in21_dim1 - 1;

        *out21 = NULL;
        *out21_dim1 = 0;
        *out21_dim2 = nderiv_plus_1;

        int maxdim = in21_dim1;
        if (maxdim < in12_dim1) maxdim = in12_dim1;

        int size = (maxdim == 0 ? 1 : maxdim);
        in21_dim1 = (in21_dim1 == 0 ? 1 : in21_dim1);
        in12_dim1 = (in12_dim1 == 0 ? 1 : in12_dim1);

        *out21_dim1 = maxdim;
        *out21_dim2 = nderiv_plus_1;
        *out21 = my_malloc(size * nderiv_plus_1, my_name);

        SpiceDouble *partdp = my_malloc(3 * nderiv_plus_1, my_name);

        if (*out21 && partdp) {
            for (int i = 0; i < size; i++) {
                chbder_c(
                    in21 + (i % in21_dim1) * in21_dim2, degp,
                    x2s,
                    in12[i % in12_dim1],
                    nderiv,
                    partdp,
                    *out21 + i * nderiv_plus_1
                );
            }
        }
        PyMem_Free(partdp);
    }
%}

/***********************************************************************
* -Procedure chbigr_c ( Chebyshev expansion integral )
*
* -Abstract
*
* Evaluate an indefinite integral of a Chebyshev expansion at a
* specified point `x' and return the value of the input expansion at
* `x' as well. The constant of integration is selected to make the
* integral zero when `x' equals the abscissa value x2s[0].
*
* void chbigr_c (
*       SpiceInt            degp,
*       ConstSpiceDouble    cp[],
*       ConstSpiceDouble    x2s[2],
*       SpiceDouble         x,
*       SpiceDouble       * p,
*       SpiceDouble       * itgrlp     )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* degp       I   Degree of input Chebyshev expansion.
* cp         I   Chebyshev coefficients of input expansion.
* x2s        I   Transformation parameters.
* x          I   Abscissa value of evaluation.
* p          O   Input expansion evaluated at `x'.
* itgrlp     O   Integral evaluated at `x'.
***********************************************************************/

%rename (chbigr) my_chbigr_c;
%apply (void RETURN_VOID) {void my_chbigr_c};
%apply (ConstSpiceDouble *IN_ARRAY1, SpiceInt DIM1) {(ConstSpiceDouble *cp, SpiceInt ncp)};
%apply (ConstSpiceDouble IN_ARRAY1[ANY]) {ConstSpiceDouble x2s[2]};
%apply (SpiceDouble *OUTPUT) {SpiceDouble *p};
%apply (SpiceDouble *OUTPUT) {SpiceDouble *itgrlp};

%inline %{
    void my_chbigr_c(
        ConstSpiceDouble *cp, SpiceInt ncp,
        ConstSpiceDouble x2s[2],
        SpiceDouble      x,
        SpiceDouble      *p,
        SpiceDouble      *itgrlp)
    {
        chbigr_c(ncp - 1, cp, x2s, x, p, itgrlp);
    }
%}

//Vector version
VECTORIZE_di_dX_d__2d(chbigr, my_chbigr_c)

/***********************************************************************
* -Procedure chbint_c ( Interpolate a Chebyshev expansion )
*
* -Abstract
*
* Return the value of a polynomial and its derivative, evaluated at
* the input `x', using the coefficients of the Chebyshev expansion of
* the polynomial.
*
* void chbint_c (
*       ConstSpiceDouble    cp[],
*       SpiceInt            degp,
*       ConstSpiceDouble    x2s[2],
*       SpiceDouble         x,
*       SpiceDouble       * p,
*       SpiceDouble       * dpdx       )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* cp         I   degp+1 Chebyshev polynomial coefficients.
* degp       I   Degree of polynomial.
* x2s        I   Transformation parameters of polynomial.
* x          I   Value for which the polynomial is to be evaluated
* p          O   Value of the polynomial at `x'
* dpdx       O   Value of the derivative of the polynomial at X
***********************************************************************/

%rename (chbint) my_chbint_c;
%apply (void RETURN_VOID) {void my_chbint_c};
%apply (ConstSpiceDouble *IN_ARRAY1, SpiceInt DIM1) {(ConstSpiceDouble *cp, SpiceInt ncp)};
%apply (ConstSpiceDouble IN_ARRAY1[ANY]) {ConstSpiceDouble x2s[2]};
%apply (SpiceDouble *OUTPUT) {SpiceDouble *p};
%apply (SpiceDouble *OUTPUT) {SpiceDouble *dpdx};

%inline %{
    void my_chbint_c(
        ConstSpiceDouble *cp, SpiceInt ncp,
        ConstSpiceDouble x2s[2],
        SpiceDouble      x,
        SpiceDouble      *p,
        SpiceDouble      *dpdx)
    {
        chbint_c(cp, ncp - 1, x2s, x, p, dpdx);
    }
%}

//Vector version
VECTORIZE_di_dX_d__2d(chbint, my_chbint_c)

/***********************************************************************
* -Procedure chbval_c ( Value of a Chebyshev polynomial expansion )
*
* -Abstract
*
* Return the value of a polynomial evaluated at the input `x' using
* the coefficients for the Chebyshev expansion of the polynomial.
*
* void chbval_c (
*       ConstSpiceDouble    cp[],
*       SpiceInt            degp,
*       ConstSpiceDouble    x2s[2],
*       SpiceDouble         x,
*       SpiceDouble       * p          )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* cp         I   degp+1 Chebyshev polynomial coefficients.
* degp       I   Degree of polynomial.
* x2s        I   Transformation parameters of polynomial.
* x          I   Value for which the polynomial is to be evaluated.
* p          O   Value of the polynomial at `x'.
***********************************************************************/

%rename (chbval) my_chbval_c;
%apply (void RETURN_VOID) {void my_chbval_c};
%apply (ConstSpiceDouble *IN_ARRAY1, SpiceInt DIM1) {(ConstSpiceDouble *cp, SpiceInt ncp)};
%apply (ConstSpiceDouble IN_ARRAY1[ANY]) {ConstSpiceDouble x2s[2]};
%apply (SpiceDouble *OUTPUT) {SpiceDouble *p};

%inline %{
    void my_chbval_c(
        ConstSpiceDouble *cp, SpiceInt ncp,
        ConstSpiceDouble x2s[2],
        SpiceDouble      x,
        SpiceDouble      *p)
    {
        chbval_c(cp, ncp - 1, x2s, x, p);
    }
%}

//Vector version
VECTORIZE_di_dX_d__d(chbval, my_chbval_c)

/***********************************************************************
* -Procedure ckcls_c ( CK, Close file )
*
* -Abstract
*
* Close an open CK file.
*
* void ckcls_c (
*       SpiceInt handle )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* handle     I   Handle of the CK file to be closed.
***********************************************************************/

%rename (ckcls) ckcls_c;
%apply (void RETURN_VOID) {void ckcls_c};

extern void ckcls_c(
        SpiceInt handle
);

/***********************************************************************
* -Procedure ckfrot_c ( CK frame, find position rotation )
*
* -Abstract
*
* Find the position rotation matrix from a C-kernel (CK) frame with
* the specified frame class ID (CK ID) to the base frame of the
* highest priority CK segment containing orientation data for this
* CK frame at the time requested.
*
* void ckfrot_c (
*       SpiceInt            inst,
*       SpiceDouble         et,
*       SpiceDouble         rotate[3][3],
*       SpiceInt          * ref,
*       SpiceBoolean      * found         )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* inst       I   Frame class ID (CK ID) of a CK frame.
* et         I   Epoch measured in seconds past J2000 TDB.
* rotate     O   Rotation matrix from CK frame to frame `ref'.
* ref        O   Frame ID of the base reference.
* found      O   True if the requested pointing is available.
***********************************************************************/

%rename (ckfrot) ckfrot_c;
%apply (void RETURN_VOID) {void ckfrot_c};
%apply (SpiceDouble OUT_ARRAY2[ANY][ANY]) {SpiceDouble rotate[3][3]};

extern void ckfrot_c(
        SpiceInt     inst,
        SpiceDouble  et,
        SpiceDouble  rotate[3][3],
        SpiceInt     *OUTPUT,
        SpiceBoolean *OUTPUT
);

//Vector version
VECTORIZE_i_d__dMN_i_b(ckfrot, ckfrot_c, 3, 3)

/***********************************************************************
* -Procedure ckfxfm_c ( CK frame, find state transformation )
*
* -Abstract
*
* Find the state transformation matrix from a C-kernel (CK) frame
* with the specified frame class ID (CK ID) to the base frame of
* the highest priority CK segment containing orientation and
* angular velocity data for this CK frame at the time requested.
*
* void ckfxfm_c (
*       SpiceInt            inst,
*       SpiceDouble         et,
*       SpiceDouble         xform[6][6],
*       SpiceInt          * ref,
*       SpiceBoolean      * found         )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* inst       I   Frame class ID (CK ID) of a CK frame.
* et         I   Epoch measured in seconds past J2000 TDB.
* xform      O   Transformation from CK frame to frame `ref'.
* ref        O   Frame ID of the base reference.
* found      O   True if the requested pointing is available.
***********************************************************************/

%rename (ckfxfm) ckfxfm_c;
%apply (void RETURN_VOID) {void ckfxfm_c};
%apply (SpiceDouble OUT_ARRAY2[ANY][ANY]) {SpiceDouble xform[6][6]};

extern void ckfxfm_c(
        SpiceInt     inst,
        SpiceDouble  et,
        SpiceDouble  xform[6][6],
        SpiceInt     *OUTPUT,
        SpiceBoolean *OUTPUT
);

//Vector version
VECTORIZE_i_d__dMN_i_b(ckfxfm, ckfxfm_c, 6, 6)

/***********************************************************************
* -Procedure ckgr02_c ( C-kernel, get record, type 02 )
*
* -Abstract
*
* Return a specified pointing instance from a CK type 02 segment.
* The segment is identified by a CK file handle and segment
* descriptor.
*
* void ckgr02_c (
*       SpiceInt            handle,
*       ConstSpiceDouble    descr[5],
*       SpiceInt            recno,
*       SpiceDouble         record[] )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* handle     I   The handle of the CK file containing the segment.
* descr      I   The segment descriptor.
* recno      I   The number of the pointing record to be returned.
* record     O   The pointing record.
***********************************************************************/

%rename (ckgr02) ckgr02_c;
%apply (void RETURN_VOID) {void ckgr02_c};
%apply (ConstSpiceDouble IN_ARRAY1[ANY]) {ConstSpiceDouble descr[5]};
%apply (SpiceDouble OUT_ARRAY1[ANY]) {SpiceDouble record[10]};

extern void ckgr02_c(
        SpiceInt         handle,
        ConstSpiceDouble descr[5],
        SpiceInt         recno,
        SpiceDouble      record[10]
);

/***********************************************************************
* -Procedure ckgr03_c ( C-kernel, get record, type 03 )
*
* -Abstract
*
* Return a specified pointing instance from a CK type 03 segment.
* The segment is identified by a CK file handle and segment
* descriptor.
*
* void ckgr03_c (
*       SpiceInt            handle,
*       ConstSpiceDouble    descr[5],
*       SpiceInt            recno,
*       SpiceDouble         record[] )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* handle     I   The handle of the CK file containing the segment.
* descr      I   The segment descriptor.
* recno      I   The number of the pointing instance to be returned.
* record     O   The pointing record.
***********************************************************************/

%rename (ckgr03) my_ckgr03_c;
%apply (void RETURN_VOID) {void my_ckgr03_c};
%apply (ConstSpiceDouble IN_ARRAY1[ANY]) {ConstSpiceDouble descr[5]};
%apply (SpiceDouble **OUT_ARRAY1, SpiceInt *SIZE1) {(SpiceDouble **record, SpiceInt *size)};

%inline %{
    void my_ckgr03_c(
        SpiceInt         handle,
        ConstSpiceDouble descr[5],
        SpiceInt         recno,
        SpiceDouble      **record, SpiceInt *size)
    {
        SpiceDouble dcd[2];
        SpiceInt    icd[6];
        dafus_c(descr, 2, 6, dcd, icd);

        *size = (icd[3] == 1) ? 8 : 5;
        *record = my_malloc(*size, "ckgr03");
        if (*record) {
            ckgr03_c(handle, descr, recno, *record);
        }
    }
%}

/***********************************************************************
* -Procedure cklpf_c ( CK, load pointing file )
*
* -Abstract
*
* Load a CK pointing file for use by the CK readers. Return that
* file's handle, to be used by other CK routines to refer to the
* file.
*
* void cklpf_c (
*       ConstSpiceChar * fname,
*       SpiceInt       * handle )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* fname      I   Name of the CK file to be loaded.
* handle     O   Loaded file's handle.
***********************************************************************/

%rename (cklpf) cklpf_c;
%apply (void RETURN_VOID) {void cklpf_c};

extern void cklpf_c(
        ConstSpiceChar *CONST_STRING,
        SpiceInt       *OUTPUT
);

/***********************************************************************
* -Procedure ckmeta_c ( CK ID to associated SCLK )
*
* -Abstract
*
* Return (depending upon the user's request) the ID code of either
* the spacecraft or spacecraft clock associated with a C-Kernel ID
* code.
*
* void ckmeta_c (
*       SpiceInt            ckid,
*       ConstSpiceChar    * meta,
*       SpiceInt          * idcode )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* ckid       I   The ID code for some C kernel object.
* meta       I   The kind of meta data requested "SPK" or "SCLK"
* idcode     O   The requested SCLK or spacecraft ID code.
***********************************************************************/

%rename (ckmeta) ckmeta_c;
%apply (void RETURN_VOID) {void ckmeta_c};

extern void ckmeta_c(
        SpiceInt       ckid,
        ConstSpiceChar *CONST_STRING,
        SpiceInt       *OUTPUT
);

/***********************************************************************
* -Procedure cknr02_c ( C-kernel, number of records, type 02 )
*
* -Abstract
*
* Return the number of pointing records in a CK type 02 segment.
* The segment is identified by a CK file handle and segment
* descriptor.
*
* void cknr02_c (
*       SpiceInt            handle,
*       ConstSpiceDouble    descr[5],
*       SpiceInt          * nrec      )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* handle     I   The handle of the CK file containing the segment.
* descr      I   The descriptor of the type 2 segment.
* nrec       O   The number of records in the segment.
***********************************************************************/

%rename (cknr02) cknr02_c;
%apply (void RETURN_VOID) {void cknr02_c};
%apply (ConstSpiceDouble IN_ARRAY1[ANY]) {ConstSpiceDouble descr[5]};

extern void cknr02_c(
        SpiceInt         handle,
        ConstSpiceDouble descr[5],
        SpiceInt         *OUTPUT
);

/***********************************************************************
* -Procedure cknr03_c ( C-kernel, number of records, type 03 )
*
* -Abstract
*
* Return the number of pointing instances in a CK type 03 segment.
* The segment is identified by a CK file handle and segment
* descriptor.
*
* void cknr03_c (
*       SpiceInt            handle,
*       ConstSpiceDouble    descr[5],
*       SpiceInt          * nrec      )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* handle     I   The handle of the CK file containing the segment.
* descr      I   The descriptor of the type 3 segment.
* nrec       O   The number of pointing instances in the segment.
***********************************************************************/

%rename (cknr03) cknr03_c;
%apply (void RETURN_VOID) {void cknr03_c};
%apply (ConstSpiceDouble IN_ARRAY1[ANY]) {ConstSpiceDouble descr[5]};

extern void cknr03_c(
        SpiceInt         handle,
        ConstSpiceDouble descr[5],
        SpiceInt         *OUTPUT
);

/***********************************************************************
* -Procedure ckopn_c ( CK, open new file. )
*
* -Abstract
*
* Open a new CK file, returning the handle of the opened file.
*
* void ckopn_c (
*       ConstSpiceChar   * fname,
*       ConstSpiceChar   * ifname,
*       SpiceInt           ncomch,
*       SpiceInt         * handle  )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* fname      I   The name of the CK file to be opened.
* ifname     I   The internal filename for the CK.
* ncomch     I   The number of characters to reserve for comments.
* handle     O   The handle of the opened CK file.
***********************************************************************/

%rename (ckopn) ckopn_c;
%apply (void RETURN_VOID) {void ckopn_c};

extern void ckopn_c(
        ConstSpiceChar *CONST_STRING,
        ConstSpiceChar *CONST_STRING,
        SpiceInt       ncomch,
        SpiceInt       *OUTPUT
);

/***********************************************************************
* -Procedure ckupf_c ( CK, Unload pointing file )
*
* -Abstract
*
* Unload a CK pointing file so that it will no longer be searched
* by the readers.
*
* void ckupf_c (
*       SpiceInt handle )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* handle     I   Handle of CK file to be unloaded
***********************************************************************/

%rename (ckupf) ckupf_c;
%apply (void RETURN_VOID) {void ckupf_c};

extern void ckupf_c(
        SpiceInt handle
);

/***********************************************************************
* -Procedure ckw01_c ( C-Kernel, write segment to C-kernel, data type 1 )
*
* -Abstract
*
* Add a type 1 segment to a C-kernel.
*
* void ckw01_c (
*       SpiceInt            handle,
*       SpiceDouble         begtim,
*       SpiceDouble         endtim,
*       SpiceInt            inst,
*       ConstSpiceChar    * ref,
*       SpiceBoolean        avflag,
*       ConstSpiceChar    * segid,
*       SpiceInt            nrec,
*       ConstSpiceDouble    sclkdp[],
*       ConstSpiceDouble    quats[][4],
*       ConstSpiceDouble    avvs[][3]  )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* handle     I   Handle of an open CK file.
* begtim     I   The beginning encoded SCLK of the segment.
* endtim     I   The ending encoded SCLK of the segment.
* inst       I   The NAIF instrument ID code.
* ref        I   The reference frame of the segment.
* avflag     I   True if the segment will contain angular velocity.
* segid      I   Segment identifier.
* nrec       I   Number of pointing records.
* sclkdp     I   Encoded SCLK times.
* quats      I   Quaternions representing instrument pointing.
* avvs       I   Angular velocity vectors.
***********************************************************************/

%rename (ckw01) ckw01_c;
%apply (void RETURN_VOID) {void ckw01_c};
%apply (SpiceInt DIM1, ConstSpiceDouble *IN_ARRAY1) {(SpiceInt nrec, ConstSpiceDouble *sclkdp)};
%apply (ConstSpiceDouble IN_ARRAY2[][ANY]) {ConstSpiceDouble quats[][4]};
%apply (ConstSpiceDouble IN_ARRAY2[][ANY]) {ConstSpiceDouble avvs[][3]};

extern void ckw01_c(
        SpiceInt         handle,
        SpiceDouble      begtim,
        SpiceDouble      endtim,
        SpiceInt         inst,
        ConstSpiceChar   *CONST_STRING,
        SpiceBoolean     avflag,
        ConstSpiceChar   *CONST_STRING,
        SpiceInt         nrec, ConstSpiceDouble *sclkdp,
        ConstSpiceDouble quats[][4],
        ConstSpiceDouble avvs[][3]
);

/***********************************************************************
* -Procedure ckw02_c ( C-Kernel, write segment to C-kernel, data type 2 )
*
* -Abstract
*
* Write a type 2 segment to a C-kernel.
*
* void ckw02_c (
*       SpiceInt            handle,
*       SpiceDouble         begtim,
*       SpiceDouble         endtim,
*       SpiceInt            inst,
*       ConstSpiceChar    * ref,
*       ConstSpiceChar    * segid,
*       SpiceInt            nrec,
*       ConstSpiceDouble    start[],
*       ConstSpiceDouble    stop[],
*       ConstSpiceDouble    quats[][4],
*       ConstSpiceDouble    avvs[][3],
*       ConstSpiceDouble    rates[]    )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* handle     I   Handle of an open CK file.
* begtim     I   The beginning encoded SCLK of the segment.
* endtim     I   The ending encoded SCLK of the segment.
* inst       I   The NAIF instrument ID code.
* ref        I   The reference frame of the segment.
* segid      I   Segment identifier.
* nrec       I   Number of pointing records.
* start      I   Encoded SCLK interval start times.
* stop       I   Encoded SCLK interval stop times.
* quats      I   Quaternions representing instrument pointing.
* avvs       I   Angular velocity vectors.
* rates      I   Number of seconds per tick for each interval.
***********************************************************************/

%rename (ckw02) ckw02_c;
%apply (void RETURN_VOID) {void ckw02_c};
%apply (SpiceInt DIM1, ConstSpiceDouble *IN_ARRAY1) {(SpiceInt nrec, ConstSpiceDouble *start)};
%apply (ConstSpiceDouble IN_ARRAY2[][ANY]) {ConstSpiceDouble quats[][4]};
%apply (ConstSpiceDouble IN_ARRAY2[][ANY]) {ConstSpiceDouble avvs[][3]};

extern void ckw02_c(
        SpiceInt         handle,
        SpiceDouble      begtim,
        SpiceDouble      endtim,
        SpiceInt         inst,
        ConstSpiceChar   *CONST_STRING,
        ConstSpiceChar   *CONST_STRING,
        SpiceInt         nrec, ConstSpiceDouble *start,
        ConstSpiceDouble *IN_ARRAY1,
        ConstSpiceDouble quats[][4],
        ConstSpiceDouble avvs[][3],
        ConstSpiceDouble *IN_ARRAY1
);

/***********************************************************************
* -Procedure ckw03_c ( C-Kernel, write segment to C-kernel, data type 3 )
*
* -Abstract
*
* Add a type 3 segment to a C-kernel.
*
* void ckw03_c (
*       SpiceInt            handle,
*       SpiceDouble         begtim,
*       SpiceDouble         endtim,
*       SpiceInt            inst,
*       ConstSpiceChar    * ref,
*       SpiceBoolean        avflag,
*       ConstSpiceChar    * segid,
*       SpiceInt            nrec,
*       ConstSpiceDouble    sclkdp[],
*       ConstSpiceDouble    quats[][4],
*       ConstSpiceDouble    avvs[][3],
*       SpiceInt            nints,
*       ConstSpiceDouble    starts[]    )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* handle     I   Handle of an open CK file.
* begtim     I   The beginning encoded SCLK of the segment.
* endtim     I   The ending encoded SCLK of the segment.
* inst       I   The NAIF instrument ID code.
* ref        I   The reference frame of the segment.
* avflag     I   True if the segment will contain angular velocity.
* segid      I   Segment identifier.
* nrec       I   Number of pointing records.
* sclkdp     I   Encoded SCLK times.
* quats      I   Quaternions representing instrument pointing.
* avvs       I   Angular velocity vectors.
* nints      I   Number of intervals.
* starts     I   Encoded SCLK interval start times.
***********************************************************************/

%rename (ckw03) ckw03_c;
%apply (void RETURN_VOID) {void ckw03_c};
%apply (SpiceInt DIM1, ConstSpiceDouble *IN_ARRAY1) {(SpiceInt nrec, ConstSpiceDouble *sclkdp)};
%apply (ConstSpiceDouble IN_ARRAY2[][ANY]) {ConstSpiceDouble quats[][4]};
%apply (ConstSpiceDouble IN_ARRAY2[][ANY]) {ConstSpiceDouble avvs[][3]};

extern void ckw03_c(
        SpiceInt         handle,
        SpiceDouble      begtim,
        SpiceDouble      endtim,
        SpiceInt         inst,
        ConstSpiceChar   *CONST_STRING,
        SpiceBoolean     avflag,
        ConstSpiceChar   *CONST_STRING,
        SpiceInt         nrec, ConstSpiceDouble *sclkdp,
        ConstSpiceDouble quats[][4],
        ConstSpiceDouble avvs[][3],
        SpiceInt         nints,
        ConstSpiceDouble *IN_ARRAY1
);

/***********************************************************************
* -Procedure ckw05_c ( Write CK segment, type 5 )
*
* -Abstract
*
* Write a type 5 segment to a CK file.
*
* void ckw05_c (
*       SpiceInt            handle,
*       SpiceCK05Subtype    subtyp,
*       SpiceInt            degree,
*       SpiceDouble         begtim,
*       SpiceDouble         endtim,
*       SpiceInt            inst,
*       ConstSpiceChar    * ref,
*       SpiceBoolean        avflag,
*       ConstSpiceChar    * segid,
*       SpiceInt            n,
*       ConstSpiceDouble    sclkdp[],
*       const void        * packts,
*       SpiceDouble         rate,
*       SpiceInt            nints,
*       ConstSpiceDouble    starts[]    )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* handle     I   Handle of an open CK file.
* subtyp     I   CK type 5 subtype code.
* degree     I   Degree of interpolating polynomials.
* begtim     I   The beginning encoded SCLK of the segment.
* endtim     I   The ending encoded SCLK of the segment.
* inst       I   The NAIF instrument ID code.
* ref        I   The reference frame of the segment.
* avflag     I   True if the segment will contain angular velocity.
* segid      I   Segment identifier.
* n          I   Number of packets.
* sclkdp     I   Encoded SCLK times.
* packts     I   Array of packets.
* rate       I   Nominal SCLK rate in seconds per tick.
* nints      I   Number of intervals.
* starts     I   Encoded SCLK interval start times.
* MAXDEG     P   Maximum allowed degree of interpolating polynomial.
***********************************************************************/

%rename (ckw05) my_ckw05_c;
%apply (void RETURN_VOID) {void my_ckw05_c};
%apply (ConstSpiceChar *CONST_STRING) {ConstSpiceChar *subtyp};
%apply (SpiceInt DIM1, ConstSpiceDouble *IN_ARRAY1)
                                     {(SpiceInt n, ConstSpiceDouble *sclkdp)};
%apply (ConstSpiceDouble *IN_ARRAY2) {ConstSpiceDouble *packts};
%apply (ConstSpiceDouble *IN_ARRAY1) {ConstSpiceDouble *starts};
%apply (ConstSpiceChar *CONST_STRING) {ConstSpiceChar *ref};
%apply (ConstSpiceChar *CONST_STRING) {ConstSpiceChar *segid};

%inline %{
    void my_ckw05_c(
        SpiceInt         handle,
        ConstSpiceChar   *subtyp,
        SpiceInt         degree,
        SpiceDouble      begtim,
        SpiceDouble      endtim,
        SpiceInt         inst,
        ConstSpiceChar   *ref,
        SpiceBoolean     avflag,
        ConstSpiceChar   *segid,
        SpiceInt         n, ConstSpiceDouble *sclkdp,
        ConstSpiceDouble *packts,
        SpiceDouble      rate,
        SpiceInt         nints,
        ConstSpiceDouble *starts)
    {
        SpiceCK05Subtype subtyp_;
        if (strcmp(subtyp, "C05TP0") == 0) {
            subtyp_ = C05TP0;
        } else if (strcmp(subtyp, "C05TP1") == 0) {
            subtyp_ = C05TP1;
        } else if (strcmp(subtyp, "C05TP2") == 0) {
            subtyp_ = C05TP2;
        } else if (strcmp(subtyp, "C05TP3") == 0) {
            subtyp_ = C05TP3;
        } else {
            chkin_c("ckw05");
            setmsg_c("subtyp value must be one of {\"C05TP0\", \"C05TP1\", \"C05TP2\", \"C05TP3\"}");
            sigerr_c("SPICE(SPICE(INVALIDARGUMENT)");
            chkout_c("ckw05");
            return;
        }

        ckw05_c(handle, subtyp_, degree, begtim, endtim, inst, ref, avflag, segid,
                n, sclkdp, packts, rate, nints, starts);
    }
%}

/***********************************************************************
* -Procedure cmprss_c ( Compress a character string )
*
* -Abstract
*
* Compress a character string by removing occurrences of
* more than N consecutive occurrences of a specified
* character.
*
* void cmprss_c (
*       SpiceChar          delim,
*       SpiceInt           n,
*       ConstSpiceChar   * input,
*       SpiceInt           outlen,
*       SpiceChar        * output  )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* delim      I   Delimiter to be compressed.
* n          I   Maximum consecutive occurrences of delim.
* input      I   Input string.
* outlen     I   Available space in output string.
* output     O   Compressed string.
***********************************************************************/

%rename (cmprss) cmprss_c;
%apply (void RETURN_VOID) {void cmprss_c};
%apply (ConstSpiceChar *CONST_STRING) {ConstSpiceChar *input};
%apply (SpiceInt DIM1, SpiceChar OUT_STRING[ANY])
                    {(SpiceInt outlen, SpiceChar output[LONGMSGLEN])};

extern void cmprss_c(
        SpiceChar      delim,
        SpiceInt       n,
        ConstSpiceChar *input,
        SpiceInt       outlen, SpiceChar output[LONGMSGLEN]
);

/***********************************************************************
* -Procedure cpos_c ( Character position )
*
* -Abstract
*
* Find the first occurrence in a string of a character belonging
* to a collection of characters, starting at a specified location,
* searching forward.
*
* SpiceInt cpos_c (
*       ConstSpiceChar    * str,
*       ConstSpiceChar    * chars,
*       SpiceInt            start  )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* str        I   Any character string.
* chars      I   A collection of characters.
* start      I   Position to begin looking for one of chars.
* pos        R   Position of character.
***********************************************************************/

%rename (cpos) cpos_c;
%apply (SpiceInt RETURN_INT) {SpiceInt cpos_c};

extern SpiceInt cpos_c(
        ConstSpiceChar *CONST_STRING,
        ConstSpiceChar *CONST_STRING,
        SpiceInt       start
);

/***********************************************************************
* -Procedure cposr_c ( Character position, reverse )
*
* -Abstract
*
* Find the first occurrence in a string of a character belonging
* to a collection of characters, starting at a specified location,
* searching in reverse.
*
* SpiceInt cposr_c (
*       ConstSpiceChar    * str,
*       ConstSpiceChar    * chars,
*       SpiceInt            start  )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* str        I   Any character string.
* chars      I   A collection of characters.
* start      I   Position to begin looking for one of chars.
* pos        R   Position of character.
***********************************************************************/

%rename (cposr) cposr_c;
%apply (SpiceInt RETURN_INT) {SpiceInt cposr_c};

extern SpiceInt cposr_c(
        ConstSpiceChar *CONST_STRING,
        ConstSpiceChar *CONST_STRING,
        SpiceInt       start
);

/***********************************************************************
* -Procedure cvpool_c ( Check variable in the pool for update)
*
* -Abstract
*
* Indicate whether or not any watched kernel variables that have a
* specified agent on their notification list have been updated.
*
* void cvpool_c (
*       ConstSpiceChar  * agent,
*       SpiceBoolean    * update )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* agent      I   Name of the agent to check for notices.
* update     O   True if variables for `agent' have been updated.
***********************************************************************/

%rename (cvpool) cvpool_c;
%apply (void RETURN_VOID) {void cvpool_c};

extern void cvpool_c(
        ConstSpiceChar *CONST_STRING,
        SpiceBoolean   *OUTPUT
);

/***********************************************************************
* -Procedure dafac_c ( DAF add comments )
*
* -Abstract
*
* Add comments from a buffer of character strings to the comment
* area of a binary DAF file, appending them to any comments which
* are already present in the file's comment area.
*
* void dafac_c (
*       SpiceInt      handle,
*       SpiceInt      n,
*       SpiceInt      buflen,
*       const void    buffer[][]  )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* handle     I    handle of a DAF opened with write access.
* n          I    Number of comments to put into the comment area.
* buflen     I    Length of elements
* buffer     I    Buffer of comments to put into the comment area.
***********************************************************************/

%rename (dafac) dafac_c;
%apply (void RETURN_VOID) {void dafac_c};
%apply (SpiceInt DIM1, SpiceInt DIM2, ConstSpiceChar *IN_STRINGS)
                    {(SpiceInt n, SpiceInt buflen, ConstSpiceChar *buffer)};

extern void dafac_c(
        SpiceInt handle,
        SpiceInt n, SpiceInt buflen, ConstSpiceChar *buffer
);

/***********************************************************************
* -Procedure dafbbs_c ( DAF, begin backward search )
*
* -Abstract
*
* Begin a backward search for arrays in a DAF.
*
* void dafbbs_c (
*       SpiceInt handle )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* handle     I   Handle of DAF to be searched.
***********************************************************************/

%rename (dafbbs) dafbbs_c;
%apply (void RETURN_VOID) {void dafbbs_c};

extern void dafbbs_c(
        SpiceInt handle
);

/***********************************************************************
* -Procedure dafcs_c ( DAF, continue search )
*
* -Abstract
*
* Select a DAF that already has a search in progress as the
* one to continue searching.
*
* void dafcs_c (
*       SpiceInt handle )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* handle     I   Handle of DAF to continue searching.
***********************************************************************/

%rename (dafcs) dafcs_c;
%apply (void RETURN_VOID) {void dafcs_c};

extern void dafcs_c(
        SpiceInt handle
);

/***********************************************************************
* -Procedure dafdc_c ( DAF delete comments )
*
* -Abstract
*
* Delete the entire comment area of a specified DAF file.
*
* void dafdc_c (
*       SpiceInt handle )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* handle     I   The handle of a binary DAF opened for writing.
***********************************************************************/

%rename (dafdc) dafdc_c;
%apply (void RETURN_VOID) {void dafdc_c};

extern void dafdc_c(
        SpiceInt handle
);

/***********************************************************************
* -Procedure dafec_c ( DAF extract comments )
*
* -Abstract
*
* Extract comments from the comment area of a binary DAF.
*
* void dafec_c (
*       SpiceInt          handle,
*       SpiceInt          bufsiz,
*       SpiceInt          buffln,
*       SpiceInt        * n,
*       void            * buffer,
*       SpiceBoolean    * done    )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* handle    I   Handle of binary DAF opened with read access.
* bufsiz    I   Maximum size, in lines, of buffer.
* buffln    I   Length of strings in output buffer.
* n         O   Number of extracted comment lines.
* buffer    O   Buffer where extracted comment lines are placed.
* done      O   Indicates whether all comments have been extracted.
***********************************************************************/

%rename (dafec) dafec_c;
%apply (void RETURN_VOID) {void dafec_c};
%apply (SpiceInt DIM1, SpiceInt DIM2, SpiceInt *NSTRINGS, SpiceChar OUT_STRINGS[ANY][ANY])
        {(SpiceInt bufsiz, SpiceInt buffln, SpiceInt *n, SpiceChar buffer[COMMENTS][COMMENTLEN])};

extern void dafec_c(
        SpiceInt     handle,
        SpiceInt     bufsiz, SpiceInt buffln, SpiceInt *n, SpiceChar buffer[COMMENTS][COMMENTLEN],
        SpiceBoolean *OUTPUT
);

/***********************************************************************
* -Procedure daffpa_c ( DAF, find previous array )
*
* -Abstract
*
* Find the previous (backward) array in the current DAF.
*
* void daffpa_c (
*       SpiceBoolean  * found )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* found      O   True if an array was found.
***********************************************************************/

%rename (daffpa) daffpa_c;
%apply (void RETURN_VOID) {void daffpa_c};

extern void daffpa_c(
        SpiceBoolean *OUTPUT
);

/***********************************************************************
* -Procedure dafgh_c ( DAF, get handle )
*
* -Abstract
*
* Return (get) the handle of the DAF currently being searched.
*
* void dafgh_c (
*       SpiceInt  * handle )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* handle     O   Handle for current DAF.
***********************************************************************/

%rename (dafgh) dafgh_c;
%apply (void RETURN_VOID) {void dafgh_c};

extern void dafgh_c(
        SpiceInt *OUTPUT
);

/***********************************************************************
* -Procedure dafgsr_c ( DAF, get summary/descriptor record )
*
* -Abstract
*
* Read a portion of the contents of a summary record in a DAF file.
*
* void dafgsr_c (
*       SpiceInt        handle,
*       SpiceInt        recno,
*       SpiceInt        begin,
*       SpiceInt        end,
*       SpiceDouble   * data,
*       SpiceBoolean  * found  )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* handle     I   Handle of DAF.
* recno      I   Record number.
* begin      I   First word to read from record.
* end        I   Last word to read from record.
* data       O   Contents of record.
* found      O   True if record is found.
***********************************************************************/

%rename (dafgsr) my_dafgsr_c;
%apply (void RETURN_VOID) {void my_dafgsr_c};
%apply (SpiceDouble OUT_ARRAY1[ANY], SpiceInt *SIZE1)
                    {(SpiceDouble data[DAFSIZE], SpiceInt *size)};

%inline %{
    void my_dafgsr_c(
        SpiceInt     handle,
        SpiceInt     recno,
        SpiceInt     begin,
        SpiceInt     end,
        SpiceDouble  data[DAFSIZE], SpiceInt *size,
        SpiceBoolean *found)
    {
        dafgsr_c(handle, recno, begin, end, data, found);
        if (*found) {
            *size = end - begin + 1;
        } else {
           *size = 0;
        }
    }
%}

/***********************************************************************
* -Procedure dafhsf_c ( DAF, handle to summary format )
*
* -Abstract
*
* Return the summary format associated with a handle.
*
* void dafhsf_c (
*       SpiceInt            handle,
*       SpiceInt          * nd,
*       SpiceInt          * ni      )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* handle     I   Handle of a DAF file.
* nd         O   Number of floating-point components in summaries.
* ni         O   Number of integer components in summaries.
***********************************************************************/

%rename (dafhsf) dafhsf_c;
%apply (void RETURN_VOID) {void dafhsf_c};

extern void dafhsf_c(
        SpiceInt handle,
        SpiceInt *OUTPUT,
        SpiceInt *OUTPUT
);

/***********************************************************************
* -Procedure dafopw_c ( DAF, open for write )
*
* -Abstract
*
* Open a DAF for subsequent write requests.
*
* void dafopw_c (
*       ConstSpiceChar  * fname,
*       SpiceInt        * handle )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* fname      I   Name of DAF to be opened.
* handle     O   Handle assigned to DAF.
***********************************************************************/

%rename (dafopw) dafopw_c;
%apply (void RETURN_VOID) {void dafopw_c};

extern void dafopw_c(
        ConstSpiceChar *CONST_STRING,
        SpiceInt       *OUTPUT
);

/***********************************************************************
* -Procedure dafps_c ( DAF, pack summary )
*
* -Abstract
*
* Pack (assemble) an array summary from its floating-point and
* integer components.
*
* void dafps_c (
*       SpiceInt             nd,
*       SpiceInt             ni,
*       ConstSpiceDouble   * dc,
*       ConstSpiceInt      * ic,
*       SpiceDouble        * sum )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* nd         I   Number of floating-point components.
* ni         I   Number of integer components.
* dc         I   Double precision components.
* ic         I   Integer components.
* sum        O   Array summary.
***********************************************************************/

%rename (dafps) my_dafps_c;
%apply (void RETURN_VOID) {void my_dafps_c};
%apply (SpiceInt DIM1, ConstSpiceDouble *IN_ARRAY1) {(SpiceInt nd, ConstSpiceDouble *dc)};
%apply (SpiceInt DIM1, ConstSpiceInt *IN_ARRAY1) {(SpiceInt ni, ConstSpiceInt *ic)};
%apply (SpiceDouble OUT_ARRAY1[ANY], SpiceInt *SIZE1) {(SpiceDouble sum[DAFSIZE], SpiceInt *nsum)};

%inline %{
    void my_dafps_c(
        SpiceInt nd, ConstSpiceDouble *dc,
        SpiceInt ni, ConstSpiceInt *ic,
        SpiceDouble sum[DAFSIZE], SpiceInt *nsum)
    {
        dafps_c(nd, ni, dc, ic, sum);
        *nsum = nd + (ni + 1)/2 + 1;
    }
%}

/***********************************************************************
* -Procedure dafrfr_c ( DAF, read file record )
*
* -Abstract
*
* Read the contents of the file record of a DAF.
*
* void dafrfr_c (
*       SpiceInt     handle,
*       SpiceInt     ifnlen,
*       SpiceInt   * nd,
*       SpiceInt   * ni,
*       SpiceChar  * ifname,
*       SpiceInt   * fward,
*       SpiceInt   * bward,
*       SpiceInt   * free    )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* handle     I   Handle of an open DAF file.
* ifnlen     I   Available room in the output string `ifname'.
* nd         O   Number of floating-point components in summaries.
* ni         O   Number of integer components in summaries.
* ifname     O   Internal file name.
* fward      O   Forward list pointer.
* bward      O   Backward list pointer.
* free       O   Free address pointer.
***********************************************************************/

%rename (dafrfr) my_dafrfr_c;
%apply (void RETURN_VOID) {void my_dafrfr_c};
%apply (SpiceInt *OUTPUT) {SpiceInt *nd};
%apply (SpiceInt *OUTPUT) {SpiceInt *ni};
%apply (SpiceInt DIM1, SpiceChar OUT_STRING[ANY])
                    {(SpiceInt ifnlen, SpiceChar ifname[FILELEN])};
%apply (SpiceInt *OUTPUT) {SpiceInt *fward};
%apply (SpiceInt *OUTPUT) {SpiceInt *bward};
%apply (SpiceInt *OUTPUT) {SpiceInt *free};

%inline %{
    void my_dafrfr_c(
        SpiceInt handle,
        SpiceInt *nd,
        SpiceInt *ni,
        SpiceInt ifnlen,  SpiceChar ifname[FILELEN],
        SpiceInt *fward,
        SpiceInt *bward,
        SpiceInt *free)
    {
        dafrfr_c(handle, ifnlen, nd, ni, ifname, fward, bward, free);
    }
%}

/***********************************************************************
* -Procedure dafrs_c ( DAF, replace summary )
*
* -Abstract
*
* Change the summary for the current array in the current DAF.
*
* void dafrs_c (
*       ConstSpiceDouble  * sum )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* sum        I   New summary for current array.
***********************************************************************/

%rename (dafrs) dafrs_c;
%apply (void RETURN_VOID) {void dafrs_c};
%apply (ConstSpiceDouble *IN_ARRAY1) {ConstSpiceDouble *sum};

extern void dafrs_c(
        ConstSpiceDouble *sum
);

/***********************************************************************
* -Procedure dasac_c ( DAS add comments )
*
* -Abstract
*
* Add comments from a buffer of character strings to the comment
* area of a binary DAS file, appending them to any comments which
* are already present in the file's comment area.
*
* void dasac_c (
*       SpiceInt       handle,
*       SpiceInt       n,
*       SpiceInt       buflen,
*       const void     buffer[][]  )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* handle     I   DAS handle of a file opened with write access.
* n          I   Number of comments to put into the comment area.
* buflen     I   Line length associated with buffer.
* buffer     I   Buffer of lines to be put into the comment area.
***********************************************************************/

%rename (dasac) dasac_c;
%apply (void RETURN_VOID) {void dasac_c};
%apply (SpiceInt DIM1, SpiceInt DIM2, ConstSpiceChar *IN_STRINGS)
                    {(SpiceInt n, SpiceInt buflen, ConstSpiceChar *buffer)};

extern void dasac_c(
        SpiceInt handle,
        SpiceInt n, SpiceInt buflen, ConstSpiceChar *buffer
);

/***********************************************************************
* -Procedure dasadc_c ( DAS, add data, character )
*
* -Abstract
*
* Add character data to a DAS file.
*
* void dasadc_c (
*       SpiceInt            handle,
*       SpiceInt            n,
*       SpiceInt            bpos,
*       SpiceInt            epos,
*       SpiceInt            datlen,
*       const void        * data   )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* handle     I   DAS file handle.
* n          I   Number of characters to add to file.
* bpos       I   Begin position of substrings in byte array.
* epos       I   End position of substrings in byte array.
* datlen     I   Common length of the character arrays in `data'.
* data       I   Sequence of strings providing the set of substrings to be added
*                to the character data in the DAS file.
***********************************************************************/

%rename (dasadc) dasadc_c;
%apply (void RETURN_VOID) {void dasadc_c};
%apply (ConstSpiceChar *IN_ARRAY1) {ConstSpiceChar *data};

extern void dasadc_c(
        SpiceInt handle,
        SpiceInt n,
        SpiceInt bpos,
        SpiceInt epos,
        SpiceInt datlen,
        ConstSpiceChar *data
);

//CSPYCE_TYPE:data:byte_array[][]

/***********************************************************************
* -Procedure dasadd_c ( DAS, add data, double precision )
*
* -Abstract
*
* Add an array of floating-point numbers to a DAS file.
*
* void dasadd_c (
*       SpiceInt            handle,
*       SpiceInt            n,
*       ConstSpiceDouble    data[] )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* handle     I   DAS file handle.
* n          I   Number of d.p. numbers to add to DAS file.
* data       I   Array of d.p. numbers to add.
***********************************************************************/

%rename (dasadd) dasadd_c;
%apply (void RETURN_VOID) {void dasadd_c};
%apply (SpiceInt DIM1, ConstSpiceDouble *IN_ARRAY1) {(SpiceInt n, ConstSpiceDouble *data)};

extern void dasadd_c(
        SpiceInt handle,
        SpiceInt n, ConstSpiceDouble *data
);

/***********************************************************************
* -Procedure dasadi_c ( DAS, add data, integer )
*
* -Abstract
*
* Add an array of integers to a DAS file.
*
* void dasadi_c (
*       SpiceInt            handle,
*       SpiceInt            n,
*       ConstSpiceInt       data[] )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* handle     I   DAS file handle.
* n          I   Number of integers to add to DAS file.
* data       I   Array of integers to add.
***********************************************************************/

%rename (dasadi) dasadi_c;
%apply (void RETURN_VOID) {void dasadi_c};
%apply (SpiceInt DIM1, ConstSpiceInt *IN_ARRAY1) {(SpiceInt n, ConstSpiceInt *data)};

extern void dasadi_c(
        SpiceInt handle,
        SpiceInt n, ConstSpiceInt *data
);

/***********************************************************************
* -Procedure dascls_c ( DAS, close file )
*
* -Abstract
*
* Close a DAS file.
*
* void dascls_c (
*       SpiceInt handle )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* handle     I   Handle of an open DAS file.
* FTSIZE     P   Maximum number of simultaneously open DAS files.
***********************************************************************/

%rename (dascls) dascls_c;
%apply (void RETURN_VOID) {void dascls_c};

extern void dascls_c(
        SpiceInt handle
);

/***********************************************************************
* -Procedure dasdc_c    ( DAS, delete comments )
*
* -Abstract
*
* Delete the entire comment area of a previously opened binary
* DAS file.
*
* void dasdc_c (
*       SpiceInt handle )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* handle     I   The handle of a binary DAS file opened for writing.
***********************************************************************/

%rename (dasdc) dasdc_c;
%apply (void RETURN_VOID) {void dasdc_c};

extern void dasdc_c(
        SpiceInt handle
);

/***********************************************************************
* -Procedure dasec_c  ( DAS extract comments )
*
* -Abstract
*
* Extract comments from the comment area of a binary DAS file.
*
* void dasec_c (
*       SpiceInt         handle,
*       SpiceInt         bufsiz,
*       SpiceInt         buffln,
*       SpiceInt       * n,
*       void           * buffer,
*       SpiceBoolean   * done   )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* handle     I   Handle of binary DAS file open with read access.
* bufsiz     I   Maximum size, in lines, of `buffer'.
* buffln     I   Line length associated with `buffer'.
* n          O   Number of comments extracted from the DAS file.
* buffer     O   Buffer in which extracted comments are placed.
* done       O   Indicates whether all comments have been extracted.
***********************************************************************/

%rename (dasec) dasec_c;
%apply (void RETURN_VOID) {void dasec_c};
%apply (SpiceInt DIM1, SpiceInt DIM2, SpiceInt *NSTRINGS, SpiceChar OUT_STRINGS[ANY][ANY])
            {(SpiceInt bufsiz, SpiceInt buffln, SpiceInt *n, SpiceChar buffer[COMMENTS][COMMENTLEN])};

extern void dasec_c(
        SpiceInt     handle,
        SpiceInt     bufsiz, SpiceInt buffln, SpiceInt *n, SpiceChar buffer[COMMENTS][COMMENTLEN],
        SpiceBoolean *OUTPUT
);

/***********************************************************************
* -Procedure dashfn_c ( DAS, handle to file name )
*
* -Abstract
*
* Return the name of the DAS file associated with a handle.
*
* void dashfn_c (
*       SpiceInt     handle,
*       SpiceInt     namlen,
*       SpiceChar  * fname  )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* handle     I   Handle of a DAS file.
* namlen     I   Length of output file name string.
* fname      O   Corresponding file name.
***********************************************************************/

%rename (dashfn) dashfn_c;
%apply (void RETURN_VOID) {void dashfn_c};
%apply (SpiceInt DIM1, SpiceChar OUT_STRING[ANY])
                    {(SpiceInt namlen, SpiceChar fname[FILELEN])};

extern void dashfn_c(
        SpiceInt handle,
        SpiceInt namlen, SpiceChar fname[FILELEN]
);

/***********************************************************************
* -Procedure dashfs_c ( DAS, handle to file summary )
*
* -Abstract
*
* Return a file summary for a specified DAS file.
*
* void dashfs_c (
*       SpiceInt            handle,
*       SpiceInt          * nresvr,
*       SpiceInt          * nresvc,
*       SpiceInt          * ncomr,
*       SpiceInt          * ncomc,
*       SpiceInt          * free,
*       SpiceInt            lastla[3],
*       SpiceInt            lastrc[3],
*       SpiceInt            lastwd[3] )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* handle     I   Handle of a DAS file.
* nresvr     O   Number of reserved records in file.
* nresvc     O   Number of characters in use in reserved rec. area.
* ncomr      O   Number of comment records in file.
* ncomc      O   Number of characters in use in comment area.
* free       O   Number of first free record.
* lastla     O   Array of last logical addresses for each data type.
* lastrc     O   Record number of last descriptor of each data type.
* lastwd     O   Word number of last descriptor of each data type.
***********************************************************************/

%rename (dashfs) dashfs_c;
%apply (void RETURN_VOID) {void dashfs_c};
%apply (SpiceInt OUT_ARRAY1[ANY]) {SpiceInt lastla[3]};
%apply (SpiceInt OUT_ARRAY1[ANY]) {SpiceInt lastrc[3]};
%apply (SpiceInt OUT_ARRAY1[ANY]) {SpiceInt lastwd[3]};

extern void dashfs_c(
        SpiceInt handle,
        SpiceInt *OUTPUT,
        SpiceInt *OUTPUT,
        SpiceInt *OUTPUT,
        SpiceInt *OUTPUT,
        SpiceInt *OUTPUT,
        SpiceInt lastla[3],
        SpiceInt lastrc[3],
        SpiceInt lastwd[3]
);

/***********************************************************************
* -Procedure daslla_c ( DAS, last logical addresses )
*
* -Abstract
*
* Return last DAS logical addresses of character, floating-point
* and integer type that are currently in use in a specified DAS
* file.
*
* void daslla_c (
*       SpiceInt            handle,
*       SpiceInt          * lastc,
*       SpiceInt          * lastd,
*       SpiceInt          * lasti  )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* handle     I   DAS file handle.
* lastc      O   Last character address in use.
* lastd      O   Last floating-point address in use.
* lasti      O   Last integer address in use.
***********************************************************************/

%rename (daslla) daslla_c;
%apply (void RETURN_VOID) {void daslla_c};

extern void daslla_c(
        SpiceInt handle,
        SpiceInt *OUTPUT,
        SpiceInt *OUTPUT,
        SpiceInt *OUTPUT
);

/***********************************************************************
* -Procedure dasllc_c ( DAS, low-level close )
*
* -Abstract
*
* Close the DAS file associated with a given handle, without
* flushing buffered data or segregating the file.
*
* void dasllc_c (
*       SpiceInt            handle )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* handle     I   Handle of a DAS file to be closed.
***********************************************************************/

%rename (dasllc) dasllc_c;
%apply (void RETURN_VOID) {void dasllc_c};

extern void dasllc_c(
        SpiceInt handle
);

/***********************************************************************
* -Procedure dasonw_c ( DAS, open new file )
*
* -Abstract
*
* Open a new DAS file and set the file type.
*
* void dasonw_c (
*       ConstSpiceChar    * fname,
*       ConstSpiceChar    * ftype,
*       ConstSpiceChar    * ifname,
*       SpiceInt            ncomr,
*       SpiceInt          * handle )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* fname      I   Name of a DAS file to be opened.
* ftype      I   Mnemonic code for type of data in the DAS file.
* ifname     I   Internal file name.
* ncomr      I   Number of comment records to allocate.
* handle     O   Handle assigned to the opened DAS file.
***********************************************************************/

%rename (dasonw) dasonw_c;
%apply (void RETURN_VOID) {void dasonw_c};

extern void dasonw_c(
        ConstSpiceChar *CONST_STRING,
        ConstSpiceChar *CONST_STRING,
        ConstSpiceChar *CONST_STRING,
        SpiceInt       ncomr,
        SpiceInt       *OUTPUT
);

/***********************************************************************
* -Procedure dasopr_c ( DAS, open for read )
*
* -Abstract
*
* Open a DAS file for reading.
*
* void dasopr_c (
*       ConstSpiceChar  * fname,
*       SpiceInt        * handle )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* fname      I   Name of a DAS file to be opened.
* handle     O   Handle assigned to the opened DAS file.
***********************************************************************/

%rename (dasopr) dasopr_c;
%apply (void RETURN_VOID) {void dasopr_c};

extern void dasopr_c(
        ConstSpiceChar *CONST_STRING,
        SpiceInt       *OUTPUT
);

/***********************************************************************
* -Procedure dasops_c ( DAS, open scratch )
*
* -Abstract
*
* Open a scratch DAS file for writing.
*
* void dasops_c (
*       SpiceInt          * handle )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* handle     O   Handle assigned to a scratch DAS file.
***********************************************************************/

%rename (dasops) dasops_c;
%apply (void RETURN_VOID) {void dasops_c};

extern void dasops_c(
        SpiceInt *OUTPUT
);

/***********************************************************************
* -Procedure dasopw_c ( DAS, open for write )
*
* -Abstract
*
* Open a DAS file for writing.
*
* void dasopw_c (
*       ConstSpiceChar    * fname,
*       SpiceInt          * handle )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* fname      I   Name of a DAS file to be opened.
* handle     O   Handle assigned to the opened DAS file.
***********************************************************************/

%rename (dasopw) dasopw_c;
%apply (void RETURN_VOID) {void dasopw_c};

extern void dasopw_c(
        ConstSpiceChar *CONST_STRING,
        SpiceInt       *OUTPUT
);

/***********************************************************************
* -Procedure dasrdc_c ( DAS, read data, character )
*
* -Abstract
*
* Read character data from a range of DAS logical addresses.
*
* void dasrdc_c (
*       SpiceInt            handle,
*       SpiceInt            first,
*       SpiceInt            last,
*       SpiceInt            bpos,
*       SpiceInt            epos,
*       SpiceInt            datlen,
*       void              * data   )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* handle     I   DAS file handle.
* first      I   Beginning of range of DAS character logical addresses.
* last       I   End of range of DAS character logical addresses.
* bpos       I   Beginning position of substrings.
* epos       I   End position of substrings.
* datlen     I   Common length of the character arrays in `data'.
* data      I-O  Sequence of strings to be updated by the character data in the DAS file.
***********************************************************************/

%rename (dasrdc) dasrdc_c;
%apply (void RETURN_VOID) {void dasrdc_c};
%apply (SpiceChar *INOUT_ARRAY1) {SpiceChar *data};

extern void dasrdc_c(
        SpiceInt handle,
        SpiceInt first,
        SpiceInt last,
        SpiceInt bpos,
        SpiceInt epos,
        SpiceInt datlen,
        SpiceChar *data
);

//CSPYCE_TYPE:data:byte_array[][]

/***********************************************************************
* -Procedure dasrdd_c ( DAS, read data, double precision )
*
* -Abstract
*
* Read floating-point data from a range of DAS logical addresses.
*
* void dasrdd_c (
*       SpiceInt            handle,
*       SpiceInt            first,
*       SpiceInt            last,
*       SpiceDouble         data[] )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* handle     I   DAS file handle.
* first      I   Beginning of range of DAS floating-point logical addresses.
* last       I   End of range of DAS floating-point logical addresses.
* data       O   Data having addresses `first' through `last'.
***********************************************************************/

%rename (dasrdd) my_dasrdd_c;
%apply (void RETURN_VOID) {void my_dasrdd_c};
%apply (SpiceDouble **OUT_ARRAY1, SpiceInt *SIZE1){(SpiceDouble **data, SpiceInt *size)};

%inline %{
    void my_dasrdd_c (
        SpiceInt            handle,
        SpiceInt            first,
        SpiceInt            last,
        SpiceDouble         **data,
        SpiceInt            *size)
    {
        my_assert_ge(first, 1, "dasrdd", "first (#) must be at least 1");
        my_assert_ge(last, first, "dasrdd", "last (#) must be as large as first (#)");
        *size = last - first + 1;
        *data = my_malloc(*size, "dasrdd");
        if (*data) {
           dasrdd_c(handle, first, last,  *data);
        }
    }
%}

/***********************************************************************
* -Procedure dasrdi_c ( DAS, read data, integer )
*
* -Abstract
*
* Read integer data from a range of DAS logical addresses.
*
* void dasrdi_c (
*       SpiceInt            handle,
*       SpiceInt            first,
*       SpiceInt            last,
*       SpiceInt            data[] )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* handle     I   DAS file handle.
* first      I   Beginning of range of DAS integer logical addresses.
* last       I   End of range of DAS integer logical addresses.
* data       O   Data having addresses `first' through `last'.
***********************************************************************/

%rename (dasrdi) my_dasrdi_c;
%apply (void RETURN_VOID) {void my_dasrdi_c};
%apply (SpiceInt **OUT_ARRAY1, SpiceInt *SIZE1){(SpiceInt **data, SpiceInt *size)};

%inline %{
   void my_dasrdi_c (
        SpiceInt            handle,
        SpiceInt            first,
        SpiceInt            last,
        SpiceInt            **data,
        SpiceInt            *size)
    {
        my_assert_ge(first, 1, "dasrdi", "first (#) must be at least 1");
        my_assert_ge(last, first, "dasrdi", "last (#) must be as large as first (#)");
        *size = last - first + 1;
        *data = my_int_malloc(*size, "dasrdi");
        if (*data) {
           dasrdi_c(handle, first, last,  *data);
        }
    }
%}

/***********************************************************************
* -Procedure dasrfr_c ( DAS, read file record )
*
* -Abstract
*
* Return the contents of the file record of a specified DAS
* file.
*
* void dasrfr_c (
*       SpiceInt            handle,
*       SpiceInt            idwlen,
*       SpiceInt            ifnlen,
*       SpiceChar         * idword,
*       SpiceChar         * ifname,
*       SpiceInt          * nresvr,
*       SpiceInt          * nresvc,
*       SpiceInt          * ncomr,
*       SpiceInt          * ncomc  )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* handle     I   DAS file handle.
* idwlen     I   Length of ID word string.
* ifnlen     I   Length of internal file name string.
* idword     O   ID word.
* ifname     O   DAS internal file name.
* nresvr     O   Number of reserved records in file.
* nresvc     O   Number of characters in use in reserved rec. area.
* ncomr      O   Number of comment records in file.
* ncomc      O   Number of characters in use in comment area.
***********************************************************************/

%rename (dasrfr) my_dasrfr_c;
%apply (void RETURN_VOID) {void my_dasrfr_c};
%apply (SpiceInt DIM1, SpiceChar OUT_STRING[ANY]) {(SpiceInt idwlen, SpiceChar idword[10])};
%apply (SpiceInt DIM1, SpiceChar OUT_STRING[ANY]) {(SpiceInt ifnlen, SpiceChar ifname[61])};
%apply (SpiceInt *OUTPUT) {SpiceInt *nresvr};
%apply (SpiceInt *OUTPUT) {SpiceInt *nresvc};
%apply (SpiceInt *OUTPUT) {SpiceInt *ncomr};
%apply (SpiceInt *OUTPUT) {SpiceInt *ncomc};
// Fixed lengths above are defined in the documentation

%inline %{
    void my_dasrfr_c(
        SpiceInt  handle,
        SpiceInt  idwlen, SpiceChar idword[10],
        SpiceInt  ifnlen, SpiceChar ifname[61],
        SpiceInt  *nresvr,
        SpiceInt  *nresvc,
        SpiceInt  *ncomr,
        SpiceInt  *ncomc)
    {
        dasrfr_c(handle, idwlen, ifnlen, idword, ifname,
                 nresvr, nresvc, ncomr, ncomc);
    }
%}

/***********************************************************************
* -Procedure dasudc_c ( DAS, update data, character )
*
* -Abstract
*
* Update character data in a specified range of DAS logical
* addresses with substrings of a character array.
*
* void dasudc_c (
*       SpiceInt            handle,
*       SpiceInt            first,
*       SpiceInt            last,
*       SpiceInt            bpos,
*       SpiceInt            epos,
*       SpiceInt            datlen,
*       const void        * data   )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* handle     I   DAS file handle.
* first      I   Beginning of range of DAS character logical addresses.
* last       I   End of range of DAS character logical addresses.
* bpos       I   Begin position of substrings in byte array.
* epos       I   End position of substrings in byte array.
* datlen     I   Common length of the character arrays in `data'.
* data       I   Sequence of strings providing the set of substrings to be updated
*                in the character data in the DAS file.
***********************************************************************/

%rename (dasudc) dasudc_c;
%apply (void RETURN_VOID) {void dasudc_c};
%apply (ConstSpiceChar *IN_ARRAY1) {ConstSpiceChar *data};

extern void dasudc_c(
        SpiceInt handle,
        SpiceInt first,
        SpiceInt last,
        SpiceInt bpos,
        SpiceInt epos,
        SpiceInt datlen, ConstSpiceChar *data
);

//CSPYCE_TYPE:data:byte_array[][]

/***********************************************************************
* -Procedure dasudd_c ( DAS, update data, double precision )
*
* -Abstract
*
* Update data in a specified range of floating-point addresses
* in a DAS file.
*
* void dasudd_c (
*       SpiceInt            handle,
*       SpiceInt            first,
*       SpiceInt            last,
*       ConstSpiceDouble    data[] )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* handle     I   DAS file handle.
* first      I   Beginning of range of floating-point addresses to write to.
* last       I   End of range of floating-point addresses to write to.
* data       I   An array of d.p. numbers.
***********************************************************************/

%rename (dasudd) my_dasudd_c;
%apply (void RETURN_VOID) {void my_dasudd_c};
%apply (SpiceInt DIM1, ConstSpiceDouble *IN_ARRAY1) {(SpiceInt n, ConstSpiceDouble *data)};

%inline %{
    void my_dasudd_c(
        SpiceInt         handle,
        SpiceInt         first,
        SpiceInt         last,
        SpiceInt n, ConstSpiceDouble *data)
    {
        if (!my_assert_ge(n, last - first + 1, "dasudd",
                          "Array is not long enough for update")) return;
        dasudd_c(handle, first, last, data);
    }

%}

/***********************************************************************
* -Procedure dasudi_c ( DAS, update data, integer )
*
* -Abstract
*
* Update data in a specified range of integer addresses in a DAS
* file.
*
* void dasudi_c (
*       SpiceInt            handle,
*       SpiceInt            first,
*       SpiceInt            last,
*       ConstSpiceInt       data[] )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* handle     I   DAS file handle.
* first      I   Beginning of range of integer addresses to write to.
* last       I   End of range of integer addresses to write to.
* data       I   An array of integers.
***********************************************************************/

%rename (dasudi) my_dasudi_c;
%apply (void RETURN_VOID) {void my_dasudi_c};
%apply (SpiceInt DIM1, ConstSpiceInt *IN_ARRAY1) {(SpiceInt n, ConstSpiceInt *data)};

%inline %{
    void my_dasudi_c(
        SpiceInt      handle,
        SpiceInt      first,
        SpiceInt      last,
        SpiceInt n, ConstSpiceInt *data)
    {
        if (!my_assert_ge(n, last - first + 1, "dasudi",
                          "Array is not long enough for update")) return;
        dasudi_c(handle, first, last, data);
    }
%}

/***********************************************************************
* -Procedure daswbr_c ( DAS, write buffered records )
*
* -Abstract
*
* Write out all buffered records of a specified DAS file.
*
* void daswbr_c (
*       SpiceInt            handle )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* handle     I   Handle of DAS file.
***********************************************************************/

%rename (daswbr) daswbr_c;
%apply (void RETURN_VOID) {void daswbr_c};

extern void daswbr_c(
        SpiceInt handle
);

/***********************************************************************
* -Procedure dazldr_c ( Derivative of AZ/EL w.r.t. rectangular )
*
* -Abstract
*
* Compute the Jacobian matrix of the transformation from
* rectangular to azimuth/elevation coordinates.
*
* void dazldr_c (
*       SpiceDouble         x,
*       SpiceDouble         y,
*       SpiceDouble         z,
*       SpiceBoolean        azccw,
*       SpiceBoolean        elplsz,
*       SpiceDouble         jacobi[3][3] )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* x          I   x-coordinate of point.
* y          I   y-coordinate of point.
* z          I   z-coordinate of point.
* azccw      I   Flag indicating how azimuth is measured, True for counterclockwise, False for clockwise.
* elplsz     I   Flag indicating how elevation is measured, True for increasing toward +Z, False for -Z.
* jacobi     O   Matrix of partial derivatives.
***********************************************************************/

%rename (dazldr) dazldr_c;
%apply (void RETURN_VOID) {void dazldr_c};
%apply (SpiceDouble OUT_ARRAY2[ANY][ANY]) {SpiceDouble jacobi[3][3]};

extern void dazldr_c(
        SpiceDouble  x,
        SpiceDouble  y,
        SpiceDouble  z,
        SpiceBoolean azccw,
        SpiceBoolean elplsz,
        SpiceDouble  jacobi[3][3]
);

//Vector version
VECTORIZE_3d_2b__dMN(dazldr, dazldr_c, 3, 3)

/***********************************************************************
* -Procedure dlabbs_c ( DLA, begin backward search )
*
* -Abstract
*
* Begin a backward segment search in a DLA file.
*
* void dlabbs_c (
*       SpiceInt         handle,
*       SpiceDLADescr  * dladsc,
*       SpiceBoolean   * found  )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* handle     I   Handle of open DLA file.
* dladsc     O   Descriptor of last segment in DLA file.
* found      O   Flag indicating whether a segment was found.
***********************************************************************/

%rename (dlabbs) dlabbs_c;
%apply (void RETURN_VOID) {void dlabbs_c};
%apply (SpiceDLADescr *OUTPUT) {SpiceDLADescr *dladsc};

extern void dlabbs_c(
        SpiceInt      handle,
        SpiceDLADescr *dladsc,
        SpiceBoolean  *OUTPUT
);

/***********************************************************************
* -Procedure dlabfs_c ( DLA, begin forward search )
*
* -Abstract
*
* Begin a forward segment search in a DLA file.
*
* void dlabfs_c (
*       SpiceInt          handle,
*       SpiceDLADescr   * dladsc,
*       SpiceBoolean    * found  )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* handle     I   Handle of open DLA file.
* dladsc     O   Descriptor of first segment in DLA file.
* found      O   Flag indicating whether a segment was found.
***********************************************************************/

%rename (dlabfs) dlabfs_c;
%apply (void RETURN_VOID) {void dlabfs_c};
%apply (SpiceDLADescr *OUTPUT) {SpiceDLADescr *dladsc};

extern void dlabfs_c(
        SpiceInt      handle,
        SpiceDLADescr *dladsc,
        SpiceBoolean  *OUTPUT
);

/***********************************************************************
* -Procedure dlabns_c ( DLA, begin new segment )
*
* -Abstract
*
* Begin a new segment in a DLA file.
*
* void dlabns_c (
*       SpiceInt            handle )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* handle     I   Handle of open DLA file.
***********************************************************************/

%rename (dlabns) dlabns_c;
%apply (void RETURN_VOID) {void dlabns_c};

extern void dlabns_c(
        SpiceInt handle
);

/***********************************************************************
* -Procedure dlaens_c ( DLA, end new segment )
*
* -Abstract
*
* End a new segment in a DLA file.
*
* void dlaens_c (
*       SpiceInt            handle )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* handle     I   Handle of open DLA file.
***********************************************************************/

%rename (dlaens) dlaens_c;
%apply (void RETURN_VOID) {void dlaens_c};

extern void dlaens_c(
        SpiceInt handle
);

/***********************************************************************
* -Procedure dlafns_c ( DLA, find next segment )
*
* -Abstract
*
* Find the segment following a specified segment in a DLA file.
*
* void dlafns_c (
*       SpiceInt               handle,
*       ConstSpiceDLADescr   * dladsc,
*       SpiceDLADescr        * nxtdsc,
*       SpiceBoolean         * found    )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* handle     I   Handle of open DLA file.
* dladsc     I   Descriptor of a DLA segment.
* nxtdsc     O   Descriptor of next segment in DLA file.
* found      O   Flag indicating whether a segment was found.
***********************************************************************/

%rename (dlafns) dlafns_c;
%apply (void RETURN_VOID) {void dlafns_c};
%apply (ConstSpiceDLADescr *INPUT) {ConstSpiceDLADescr *dladsc};
%apply (SpiceDLADescr *OUTPUT)     {SpiceDLADescr *nxtdsc};

extern void dlafns_c(
        SpiceInt      handle,
        ConstSpiceDLADescr *dladsc,
        SpiceDLADescr      *nxtdsc,
        SpiceBoolean       *OUTPUT
);

/***********************************************************************
* -Procedure dlafps_c ( DLA, find previous segment )
*
* -Abstract
*
* Find the segment preceding a specified segment in a DLA file.
*
* void dlafps_c (
*       SpiceInt               handle,
*       ConstSpiceDLADescr   * dladsc,
*       SpiceDLADescr        * prvdsc,
*       SpiceBoolean         * found   )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* handle     I   Handle of open DLA file.
* dladsc     I   Descriptor of a segment in DLA file.
* prvdsc     O   Descriptor of previous segment in DLA file.
* found      O   Flag indicating whether a segment was found.
***********************************************************************/

%rename (dlafps) dlafps_c;
%apply (void RETURN_VOID) {void dlafps_c};
%apply (ConstSpiceDLADescr *INPUT) {ConstSpiceDLADescr *dladsc};
%apply (SpiceDLADescr *OUTPUT) {SpiceDLADescr *prvdsc};

extern void dlafps_c(
        SpiceInt      handle,
        ConstSpiceDLADescr *dladsc,
        SpiceDLADescr      *prvdsc,
        SpiceBoolean       *OUTPUT
);

/***********************************************************************
* -Procedure dlaopn_c ( DLA, open new file )
*
* -Abstract
*
* Open a new DLA file and set the file type.
*
* void dlaopn_c (
*       ConstSpiceChar    * fname,
*       ConstSpiceChar    * ftype,
*       ConstSpiceChar    * ifname,
*       SpiceInt            ncomch,
*       SpiceInt          * handle )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* fname      I   Name of a DLA file to be opened.
* ftype      I   Mnemonic code for type of data in the DLA file.
* ifname     I   Internal file name.
* ncomch     I   Number of comment characters to allocate.
* handle     O   Handle assigned to the opened DLA file.
***********************************************************************/

%rename (dlaopn) dlaopn_c;
%apply (void RETURN_VOID) {void dlaopn_c};

extern void dlaopn_c(
        ConstSpiceChar *CONST_STRING,
        ConstSpiceChar *CONST_STRING,
        ConstSpiceChar *CONST_STRING,
        SpiceInt       ncomch,
        SpiceInt       *OUTPUT
);

/***********************************************************************
* -Procedure dnearp_c ( Derivative of near point )
*
* -Abstract
*
* Compute the state (position and velocity) of an ellipsoid surface
* point nearest to the position component of a specified state.
*
* void dnearp_c (
*       ConstSpiceDouble    state[6],
*       SpiceDouble         a,
*       SpiceDouble         b,
*       SpiceDouble         c,
*       SpiceDouble         dnear[6],
*       SpiceDouble         dalt[2],
*       SpiceBoolean      * found      )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* state      I   State of an object in body-fixed coordinates.
* a          I   Length of semi-axis parallel to X-axis.
* b          I   Length of semi-axis parallel to Y-axis.
* c          I   Length on semi-axis parallel to Z-axis.
* dnear      O   State of the nearest point on the ellipsoid.
* dalt       O   Altitude and derivative of altitude.
* found      O   Flag that indicates whether `dnear' is degenerate.
***********************************************************************/

%rename (dnearp) dnearp_c;
%apply (void RETURN_VOID) {void dnearp_c};
%apply (ConstSpiceDouble IN_ARRAY1[ANY]) {ConstSpiceDouble state[6]};
%apply (SpiceDouble OUT_ARRAY1[ANY]) {SpiceDouble dnear[6]};
%apply (SpiceDouble OUT_ARRAY1[ANY]) {SpiceDouble dalt[2]};

extern void dnearp_c(
        ConstSpiceDouble state[6],
        SpiceDouble  a,
        SpiceDouble  b,
        SpiceDouble  c,
        SpiceDouble  dnear[6],
        SpiceDouble  dalt[2],
        SpiceBoolean *OUTPUT
);

//Vector version
VECTORIZE_dX_3d__dM_dN_b(dnearp, dnearp_c, 6, 2)

/***********************************************************************
* -Procedure dp2hx_c ( D.p. number to hexadecimal string )
*
* -Abstract
*
* Convert a floating-point number to an equivalent character
* string using a base 16 "scientific notation."
*
* void dp2hx_c (
*       SpiceDouble         number,
*       SpiceInt            hxslen,
*       SpiceChar           hxstr[],
*       SpiceInt          * hxssiz    )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* STRLEN     P   Max number of characters allowed in output string.
* number     I   D.p. number to be converted.
* hxslen     I   Available space for output string `hxstr'.
* hxstr      O   Equivalent character string, left justified.
* hxssiz     O   Length of the character string produced.
***********************************************************************/

%rename (dp2hx) my_dp2hx_c;
%apply (void RETURN_VOID) {void my_dp2hx_c};
%apply (SpiceChar OUT_STRING[ANY]) {SpiceChar hxstr[256]};

%inline %{
    void my_dp2hx_c(
        SpiceDouble number,
        SpiceChar   hxstr[256])
    {
        SpiceInt hxssiz;

        dp2hx_c(number, 256, hxstr, &hxssiz);
        hxstr[hxssiz] = 0;
    }
%}

/***********************************************************************
* -Procedure drdazl_c ( Derivative of rectangular w.r.t. AZ/EL )
*
* -Abstract
*
* Compute the Jacobian matrix of the transformation from
* azimuth/elevation to rectangular coordinates.
*
* void drdazl_c (
*       SpiceDouble         range,
*       SpiceDouble         az,
*       SpiceDouble         el,
*       SpiceBoolean        azccw,
*       SpiceBoolean        elplsz,
*       SpiceDouble         jacobi[3][3] )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* range      I   Distance of a point from the origin.
* az         I   Azimuth of input point in radians.
* el         I   Elevation of input point in radians.
* azccw      I   Flag indicating how azimuth is measured, True for counterclockwise, False for clockwise.
* elplsz     I   Flag indicating how elevation is measured, True for increasing toward +Z, False for -Z.
* jacobi     O   Matrix of partial derivatives.
***********************************************************************/

%rename (drdazl) drdazl_c;
%apply (void RETURN_VOID) {void drdazl_c};
%apply (SpiceDouble OUT_ARRAY2[ANY][ANY]) {SpiceDouble jacobi[3][3]};

extern void drdazl_c(
        SpiceDouble  range,
        SpiceDouble  az,
        SpiceDouble  el,
        SpiceBoolean azccw,
        SpiceBoolean elplsz,
        SpiceDouble  jacobi[3][3]
);

//Vector version
VECTORIZE_3d_2b__dMN(drdazl, drdazl_c, 3, 3)

/***********************************************************************
* -Procedure dskb02_c ( DSK, fetch type 2 bookkeeping data )
*
* -Abstract
*
* Return bookkeeping data from a DSK type 2 segment.
*
* void dskb02_c (
*       SpiceInt               handle,
*       ConstSpiceDLADescr   * dladsc,
*       SpiceInt             * nv,
*       SpiceInt             * np,
*       SpiceInt             * nvxtot,
*       SpiceDouble            vtxbds[3][2],
*       SpiceDouble          * voxsiz,
*       SpiceDouble            voxori[3],
*       SpiceInt               vgrext[3],
*       SpiceInt             * cgscal,
*       SpiceInt             * vtxnpl,
*       SpiceInt             * voxnpt,
*       SpiceInt             * voxnpl          )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* handle     I   DSK file handle.
* dladsc     I   DLA descriptor.
* nv         O   Number of vertices in model.
* np         O   Number of plates in model.
* nvxtot     O   Number of voxels in fine grid.
* vtxbds     O   Vertex bounds.
* voxsiz     O   Fine voxel edge length.
* voxori     O   Fine voxel grid origin.
* vgrext     O   Fine voxel grid extent.
* cgscal     O   Coarse voxel grid scale.
* vtxnpl     O   Size of vertex-plate correspondence list.
* voxnpt     O   Size of voxel-plate pointer list.
* voxnpl     O   Size of voxel-plate correspondence list.
***********************************************************************/

%rename (dskb02) dskb02_c;
%apply (void RETURN_VOID) {void dskb02_c};
%apply (ConstSpiceDLADescr *INPUT) {ConstSpiceDLADescr *dladsc};
%apply (SpiceDouble OUT_ARRAY2[ANY][ANY]) {SpiceDouble vtxbds[3][2]};
%apply (SpiceDouble OUT_ARRAY1[ANY]) {SpiceDouble voxori[3]};
%apply (SpiceInt OUT_ARRAY1[ANY]) {SpiceInt vgrext[3]};

extern void dskb02_c(
        SpiceInt      handle,
        ConstSpiceDLADescr *dladsc,
        SpiceInt      *OUTPUT,
        SpiceInt      *OUTPUT,
        SpiceInt      *OUTPUT,
        SpiceDouble   vtxbds[3][2],
        SpiceDouble   *OUTPUT,
        SpiceDouble   voxori[3],
        SpiceInt      vgrext[3],
        SpiceInt      *OUTPUT,
        SpiceInt      *OUTPUT,
        SpiceInt      *OUTPUT,
        SpiceInt      *OUTPUT
);

/***********************************************************************
* -Procedure dskcls_c ( DSK, close file )
*
* -Abstract
*
* Close a DSK file.
*
* void dskcls_c (
*       SpiceInt      handle,
*       SpiceBoolean  optmiz )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* handle     I   Handle assigned to the opened DSK file.
* optmiz     I   Flag indicating whether to segregate the DSK.
***********************************************************************/

%rename (dskcls) dskcls_c;
%apply (void RETURN_VOID) {void dskcls_c};

extern void dskcls_c(
        SpiceInt     handle,
        SpiceBoolean optmiz
);

/***********************************************************************
* -Procedure dskd02_c ( DSK, fetch d.p. type 2 data )
*
* -Abstract
*
* Fetch floating-point data from a type 2 DSK segment.
*
* void dskd02_c (
*       SpiceInt               handle,
*       ConstSpiceDLADescr   * dladsc,
*       SpiceInt               item,
*       SpiceInt               start,
*       SpiceInt               room,
*       SpiceInt             * n,
*       SpiceDouble          * values )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* handle     I   DSK file handle.
* dladsc     I   DLA descriptor.
* item       I   Keyword identifying item to fetch.
* start      I   Start index.
* room       I   Amount of room in output array.
* n          O   Number of values returned.
* values     O   Array containing requested item.
***********************************************************************/

%rename (dskd02) dskd02_c;
%apply (void RETURN_VOID) {void dskd02_c};
%apply (ConstSpiceDLADescr *INPUT) {ConstSpiceDLADescr *dladsc};
%apply (SpiceInt DIM1, SpiceInt *SIZE1, SpiceDouble OUT_ARRAY1[ANY])
                    {(SpiceInt room, SpiceInt *n, SpiceDouble values[MAXVALS])};

extern void dskd02_c(
        SpiceInt      handle,
        ConstSpiceDLADescr *dladsc,
        SpiceInt      item,
        SpiceInt      start,
        SpiceInt      room, SpiceInt *n, SpiceDouble values[MAXVALS]
);

/***********************************************************************
* -Procedure dskgd_c ( DSK, return DSK segment descriptor  )
*
* -Abstract
*
* Return the DSK descriptor from a DSK segment identified
* by a DAS handle and DLA descriptor.
*
* void dskgd_c (
*       SpiceInt               handle,
*       ConstSpiceDLADescr   * dladsc,
*       SpiceDSKDescr        * dskdsc )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* handle     I   Handle of a DSK file.
* dladsc     I   DLA segment descriptor.
* dskdsc     O   DSK segment descriptor.
***********************************************************************/

%rename (dskgd) dskgd_c;
%apply (void RETURN_VOID) {void dskgd_c};
%apply (ConstSpiceDLADescr *INPUT) {ConstSpiceDLADescr *dladsc};
%apply (SpiceDSKDescr *OUTPUT) {SpiceDSKDescr *dskdsc};

extern void dskgd_c(
        SpiceInt      handle,
        ConstSpiceDLADescr *dladsc,
        SpiceDSKDescr *dskdsc
);

/***********************************************************************
* -Procedure dskgtl_c ( DSK, get tolerance )
*
* -Abstract
*
* Retrieve the value of a specified DSK tolerance or margin parameter.
*
* void dskgtl_c (
*       SpiceInt        keywrd,
*       SpiceDouble   * dpval  )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* keywrd     I   Code specifying parameter to retrieve.
* dpval      O   Value of parameter.
***********************************************************************/

%rename (dskgtl) dskgtl_c;
%apply (void RETURN_VOID) {void dskgtl_c};

extern void dskgtl_c(
        SpiceInt    keywrd,
        SpiceDouble *OUTPUT
);

/***********************************************************************
* -Procedure dski02_c ( DSK, fetch integer type 2 data )
*
* -Abstract
*
* Fetch integer data from a type 2 DSK segment.
*
* void dski02_c (
*       SpiceInt              handle,
*       ConstSpiceDLADescr  * dladsc,
*       SpiceInt              item,
*       SpiceInt              start,
*       SpiceInt              room,
*       SpiceInt            * n,
*       SpiceInt            * values   )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* handle     I   DSK file handle.
* dladsc     I   DLA descriptor.
* item       I   Keyword identifying item to fetch.
* start      I   Start index.
* room       I   Amount of room in output array.
* n          O   Number of values returned.
* values     O   Array containing requested item.
***********************************************************************/

%rename (dski02) dski02_c;
%apply (void RETURN_VOID) {void dski02_c};
%apply (ConstSpiceDLADescr *INPUT) {ConstSpiceDLADescr *dladsc};

extern void dski02_c(
        SpiceInt      handle,
        ConstSpiceDLADescr *dladsc,
        SpiceInt      item,
        SpiceInt      start,
        SpiceInt      room,
        SpiceInt      *OUTPUT,
        SpiceInt      *OUTPUT
);

/***********************************************************************
* -Procedure dskmi2_c ( DSK, make spatial index for type 2 segment )
*
* -Abstract
*
* Make spatial index for a DSK type 2 segment. The index is returned
* as a pair of arrays, one of type int and one of type
* float. These arrays are suitable for use with the DSK type 2
* writer dskw02.
*
* void dskmi2_c (
*       SpiceInt            nv,
*       ConstSpiceDouble    vrtces[][3],
*       SpiceInt            np,
*       ConstSpiceInt       plates[][3],
*       SpiceDouble         finscl,
*       SpiceInt            corscl,
*       SpiceInt            worksz,
*       SpiceInt            voxpsz,
*       SpiceInt            voxlsz,
*       SpiceBoolean        makvtl,
*       SpiceInt            spxisz,
*       SpiceInt            work[][2],
*       SpiceDouble         spaixd[],
*       SpiceInt            spaixi[]    )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* nv         I   Number of vertices.
* vrtces     I   Vertices.
* np         I   Number of plates.
* plates     I   Plates.
* finscl     I   Fine voxel scale.
* corscl     I   Coarse voxel scale.
* worksz     I   Workspace size.
* voxpsz     I   Voxel-plate pointer array size.
* voxlsz     I   Voxel-plate list array size.
* makvtl     I   Vertex-plate list flag.
* spxisz     I   Spatial index integer component size.
* work      I-O  Workspace.
* spaixd     O   Double precision component of spatial index.
* spaixi     O   Integer component of spatial index.
***********************************************************************/

%rename (dskmi2) my_dskmi2_c;
%apply (void RETURN_VOID) {void my_dskmi2_c};
%apply (SpiceInt DIM1, ConstSpiceDouble IN_ARRAY2[][ANY])
                    {(SpiceInt nv, ConstSpiceDouble vrtces[][3])};
%apply (SpiceInt DIM1, ConstSpiceInt IN_ARRAY2[][ANY])
                    {(SpiceInt np, ConstSpiceInt plates[][3])};
%apply (SpiceDouble **OUT_ARRAY1, SpiceInt *SIZE1) {(SpiceDouble **spaixd, SpiceInt *n1)};
%apply (SpiceInt    **OUT_ARRAY1, SpiceInt *SIZE1) {(SpiceInt **spaixi,    SpiceInt *n2)};

%inline %{
    void my_dskmi2_c(
        SpiceInt         nv, ConstSpiceDouble vrtces[][3],
        SpiceInt         np, ConstSpiceInt    plates[][3],
        SpiceDouble      finscl,
        SpiceInt         corscl,
        SpiceInt         worksz,
        SpiceInt         voxpsz,
        SpiceInt         voxlsz,
        SpiceBoolean     makvtl,
        SpiceInt         spxisz,
        SpiceDouble**    spaixd, SpiceInt *n1,
        SpiceInt**       spaixi, SpiceInt *n2)
    {
        SpiceInt *work   = my_int_malloc(2 * worksz, "dskmi2");
        *spaixd = my_malloc(SPICE_DSK02_SPADSZ, "dskmi2");
        *n1 = SPICE_DSK02_SPADSZ;
        *spaixi = my_int_malloc(spxisz, "dskmi2");
        *n2 = spxisz;

        if (work && *spaixi) {
            dskmi2_c(nv, vrtces, np, plates, finscl, corscl, worksz, voxpsz, voxlsz,
                     makvtl, spxisz, work, *spaixd, *spaixi);
        }
        PyMem_Free(work);
    }
%}

/***********************************************************************
* -Procedure dskn02_c ( DSK, type 2, compute normal vector for plate )
*
* -Abstract
*
* Compute the unit normal vector for a specified plate from a type
* 2 DSK segment.
*
* void dskn02_c (
*       SpiceInt               handle,
*       ConstSpiceDLADescr   * dladsc,
*       SpiceInt               plid,
*       SpiceDouble            normal[3] )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* handle     I   DSK file handle.
* dladsc     I   DLA descriptor.
* plid       I   Plate ID.
* normal     O   Plate's unit normal vector.
***********************************************************************/

%rename (dskn02) dskn02_c;
%apply (void RETURN_VOID) {void dskn02_c};
%apply (ConstSpiceDLADescr *INPUT) {ConstSpiceDLADescr *dladsc};
%apply (SpiceDouble OUT_ARRAY1[ANY]) {SpiceDouble normal[3]};

extern void dskn02_c(
        SpiceInt      handle,
        ConstSpiceDLADescr *dladsc,
        SpiceInt      plid,
        SpiceDouble   normal[3]
);

/***********************************************************************
* -Procedure dskobj_c ( DSK, get object IDs )
*
* -Abstract
*
* Find the set of body ID codes of all objects for which
* topographic data are provided in a specified DSK file.
*
* void dskobj_c (
*       ConstSpiceChar   * dskfnm,
*       SpiceCell        * bodids )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* dskfnm     I   Name of DSK file.
* bodids    I-O  Set of ID codes of objects in DSK file.
***********************************************************************/

%rename (dskobj) dskobj_c;
%apply (void RETURN_VOID) {void dskobj_c};
%apply (ConstSpiceChar *CONST_STRING) {ConstSpiceChar *dskfnm};
%apply (SpiceCellInt *INOUT) {SpiceCell* bodids};

extern void dskobj_c(
        ConstSpiceChar *dskfnm,
        SpiceCell *bodids
);

//CSPYCE_DEFAULT:bodids:()

/***********************************************************************
* -Procedure dskopn_c ( DSK, open new file )
*
* -Abstract
*
* Open a new DSK file for subsequent write operations.
*
* void dskopn_c (
*       ConstSpiceChar  * fname,
*       ConstSpiceChar  * ifname,
*       SpiceInt          ncomch,
*       SpiceInt       *  handle )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* fname      I   Name of a DSK file to be opened.
* ifname     I   Internal file name.
* ncomch     I   Number of comment characters to allocate.
* handle     O   Handle assigned to the opened DSK file.
***********************************************************************/

%rename (dskopn) dskopn_c;
%apply (void RETURN_VOID) {void dskopn_c};

extern void dskopn_c(
        ConstSpiceChar *CONST_STRING,
        ConstSpiceChar *CONST_STRING,
        SpiceInt       ncomch,
        SpiceInt       *OUTPUT
);

/***********************************************************************
* -Procedure dskp02_c ( DSK, fetch type 2 plate data )
*
* -Abstract
*
* Fetch triangular plates from a type 2 DSK segment.
*
* void dskp02_c (
*       SpiceInt              handle,
*       ConstSpiceDLADescr  * dladsc,
*       SpiceInt              start,
*       SpiceInt              room,
*       SpiceInt            * n,
*       SpiceInt              plates[][3] )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* handle     I   DSK file handle.
* dladsc     I   DLA descriptor.
* start      I   Start index.
* room       I   Amount of room in output array.
* n          O   Number of plates returned.
* plates     O   Array containing plates.
***********************************************************************/

%rename (dskp02) my_dskp02_c;
%apply (void RETURN_VOID) {void my_dskp02_c};
%apply (ConstSpiceDLADescr *INPUT) {ConstSpiceDLADescr *dladsc};
%apply (SpiceInt **OUT_ARRAY2, SpiceInt *SIZE1, SpiceInt *SIZE2)
                {(SpiceInt **plates, SpiceInt *dim1, SpiceInt *dim2)};

%inline %{
    void my_dskp02_c(
        SpiceInt      handle,
        ConstSpiceDLADescr *dladsc,
        SpiceInt      start,
        SpiceInt      room,
        SpiceInt      **plates, SpiceInt *dim1, SpiceInt *dim2)
    {
        *dim2 = 3;
        *plates = my_int_malloc(3 * room, "dskp02");
        if (*plates) {
            dskp02_c(handle, dladsc, start, room, dim1, *plates);
        }
    }
%}

//CSPYCE_DEFAULT:room:100

/***********************************************************************
* -Procedure dskrb2_c ( DSK, determine range bounds for plate set )
*
* -Abstract
*
* Determine range bounds for a set of triangular plates to
* be stored in a type 2 DSK segment.
*
* void dskrb2_c (
*       SpiceInt           nv,
*       ConstSpiceDouble   vrtces[][3],
*       SpiceInt           np,
*       ConstSpiceInt      plates[][3],
*       SpiceInt           corsys,
*       ConstSpiceDouble   corpar[],
*       SpiceDouble      * mncor3,
*       SpiceDouble      * mxcor3       )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* nv         I   Number of vertices.
* vrtces     I   Vertices.
* np         I   Number of plates.
* plates     I   Plates.
* corsys     I   DSK coordinate system code.
* corpar     I   DSK coordinate system parameters.
* mncor3     O   Lower bound on range of third coordinate.
* mxcor3     O   Upper bound on range of third coordinate.
***********************************************************************/

%rename (dskrb2) dskrb2_c;
%apply (void RETURN_VOID) {void dskrb2_c};
%apply (SpiceInt DIM1, ConstSpiceDouble IN_ARRAY2[][ANY]) {(SpiceInt nv, ConstSpiceDouble vrtces[][3])};
%apply (SpiceInt DIM1, ConstSpiceInt IN_ARRAY2[][ANY]) {(SpiceInt np, ConstSpiceInt plates[][3])};

extern void dskrb2_c(
        SpiceInt         nv, ConstSpiceDouble vrtces[][3],
        SpiceInt         np, ConstSpiceInt    plates[][3],
        SpiceInt         corsys,
        ConstSpiceDouble *IN_ARRAY1,
        SpiceDouble      *OUTPUT,
        SpiceDouble      *OUTPUT
);

/***********************************************************************
* -Procedure dsksrf_c ( DSK, get surface IDs for body )
*
* -Abstract
*
* Find the set of surface ID codes for all surfaces associated with
* a given body in a specified DSK file.
*
* void dsksrf_c (
*       ConstSpiceChar  * dskfnm,
*       SpiceInt          bodyid,
*       SpiceCell       * srfids )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* dskfnm     I   Name of DSK file.
* bodyid     I   Integer body ID code.
* srfids    I-O  Set of ID codes of surfaces in DSK file.
***********************************************************************/

%rename (dsksrf) dsksrf_c;
%apply (void RETURN_VOID) {void dsksrf_c};
%apply (ConstSpiceChar *CONST_STRING) {ConstSpiceChar *dskfnm};
%apply (SpiceCellInt *INOUT) {SpiceCell *srfids};

extern void dsksrf_c(
        ConstSpiceChar *dskfnm,
        SpiceInt       bodyid,
        SpiceCell      *srfids
);

//CSPYCE_DEFAULT:srfids:()


/***********************************************************************
* -Procedure dskstl_c ( DSK, set tolerance )
*
* -Abstract
*
* Set the value of a specified DSK tolerance or margin parameter.
*
* void dskstl_c (
*       SpiceInt        keywrd,
*       SpiceDouble     dpval  )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* keywrd     I   Code specifying parameter to set.
* dpval      I   Value of parameter.
***********************************************************************/

%rename (dskstl) dskstl_c;
%apply (void RETURN_VOID) {void dskstl_c};

extern void dskstl_c(
        SpiceInt    keywrd,
        SpiceDouble dpval
);

/***********************************************************************
* -Procedure dskv02_c ( DSK, fetch type 2 vertex data )
*
* -Abstract
*
* Fetch vertices from a type 2 DSK segment.
*
* void dskv02_c (
*       SpiceInt               handle,
*       ConstSpiceDLADescr   * dladsc,
*       SpiceInt               start,
*       SpiceInt               room,
*       SpiceInt             * n,
*       SpiceDouble            vrtces[][3] )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* handle     I   DSK file handle.
* dladsc     I   DLA descriptor.
* start      I   Start index.
* room       I   Amount of room in output array.
* n          O   Number of vertices returned.
* vrtces     O   Array containing vertices.
***********************************************************************/

%rename (dskv02) my_dskv02_c;
%apply (void RETURN_VOID) {void my_dskv02_c};
%apply (ConstSpiceDLADescr *INPUT) {ConstSpiceDLADescr *dladsc};
%apply (SpiceDouble **OUT_ARRAY2, SpiceInt *SIZE1, SpiceInt *SIZE2)
                    {(SpiceDouble **vrtces, SpiceInt *dim1, SpiceInt *dim2)};

%inline %{
    void my_dskv02_c(
        SpiceInt      handle,
        ConstSpiceDLADescr *dladsc,
        SpiceInt      start,
        SpiceInt      room,
        SpiceDouble **vrtces, SpiceInt *dim1, SpiceInt *dim2)
    {
        *dim1 = 0;
        *dim2 = 3;
        *vrtces = my_malloc(3 * room, "dskv02_c");
        if (*vrtces) {
            dskv02_c(handle, dladsc, start, room, dim1, *vrtces);
        }
    }
%}

//CSPYCE_DEFAULT:room:100

/***********************************************************************
* -Procedure dskw02_c ( DSK, write type 2 segment )
*
* -Abstract
*
* Write a type 2 segment to a DSK file.
*
* void dskw02_c (
*       SpiceInt             handle,
*       SpiceInt             center,
*       SpiceInt             surfid,
*       SpiceInt             dclass,
*       ConstSpiceChar     * frame,
*       SpiceInt             corsys,
*       ConstSpiceDouble     corpar[],
*       SpiceDouble          mncor1,
*       SpiceDouble          mxcor1,
*       SpiceDouble          mncor2,
*       SpiceDouble          mxcor2,
*       SpiceDouble          mncor3,
*       SpiceDouble          mxcor3,
*       SpiceDouble          first,
*       SpiceDouble          last,
*       SpiceInt             nv,
*       ConstSpiceDouble     vrtces[][3],
*       SpiceInt             np,
*       ConstSpiceInt        plates[][3],
*       ConstSpiceDouble     spaixd[],
*       ConstSpiceInt        spaixi[]      )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* handle     I   Handle assigned to the opened DSK file.
* center     I   Central body ID code.
* surfid     I   Surface ID code.
* dclass     I   Data class.
* frame      I   Reference frame.
* corsys     I   Coordinate system code.
* corpar     I   Coordinate system parameters.
* mncor1     I   Minimum value of first coordinate.
* mxcor1     I   Maximum value of first coordinate.
* mncor2     I   Minimum value of second coordinate.
* mxcor2     I   Maximum value of second coordinate.
* mncor3     I   Minimum value of third coordinate.
* mxcor3     I   Maximum value of third coordinate.
* first      I   Coverage start time.
* last       I   Coverage stop time.
* nv         I   Number of vertices.
* vrtces     I   Vertices.
* np         I   Number of plates.
* plates     I   Plates.
* spaixd     I   Double precision component of spatial index.
* spaixi     I   Integer component of spatial index.
* SPICE_DSK_ANGMRG
*            P   Angular round-off margin.
* SPICE_DSK_GENCLS
*            P   General surface DSK class.
* SPICE_DSK_SVFCLS
*            P   Single-valued function DSK class.
* SPICE_DSK_NSYPAR
*            P   Maximum number of coordinate system parameters in
*                a DSK descriptor.
* SPICE_DSK02_MAXCGR
*            P   Maximum DSK type 2 coarse voxel count.
* SPICE_DSK02_MAXPLT
*            P   Maximum DSK type 2 plate count.
* SPICE_DSK02_MAXVOX
*            P   Maximum DSK type 2 voxel count.
* SPICE_DSK02_MAXVRT
*            P   Maximum DSK type 2 vertex count.
***********************************************************************/

%rename (dskw02) dskw02_c;
%apply (void RETURN_VOID) {void dskw02_c};
%apply (ConstSpiceDouble IN_ARRAY1[]) {ConstSpiceDouble corpar[]};
%apply (SpiceInt DIM1, ConstSpiceDouble IN_ARRAY2[][ANY]) {(SpiceInt nv, ConstSpiceDouble vrtces[][3])};
%apply (SpiceInt DIM1, ConstSpiceInt IN_ARRAY2[][ANY]) {(SpiceInt np, ConstSpiceInt plates[][3])};
%apply (ConstSpiceDouble IN_ARRAY1[]) {ConstSpiceDouble spaixd[]};
%apply (ConstSpiceInt IN_ARRAY1[]) {ConstSpiceInt spaixi[]};

extern void dskw02_c(
        SpiceInt         handle,
        SpiceInt         center,
        SpiceInt         surfid,
        SpiceInt         dclass,
        ConstSpiceChar   *CONST_STRING,
        SpiceInt         corsys,
        ConstSpiceDouble corpar[],
        SpiceDouble      mncor1,
        SpiceDouble      mxcor1,
        SpiceDouble      mncor2,
        SpiceDouble      mxcor2,
        SpiceDouble      mncor3,
        SpiceDouble      mxcor3,
        SpiceDouble      first,
        SpiceDouble      last,
        SpiceInt         nv, ConstSpiceDouble vrtces[][3],
        SpiceInt         np, ConstSpiceInt    plates[][3],
        ConstSpiceDouble spaixd[],
        ConstSpiceInt    spaixi[]
);

/***********************************************************************
* -Procedure dskx02_c ( DSK, ray-surface intercept, type 2 )
*
* -Abstract
*
* Determine the plate ID and body-fixed coordinates of the
* intersection of a specified ray with the surface defined by a
* type 2 DSK plate model.
*
* void dskx02_c (
*       SpiceInt               handle,
*       ConstSpiceDLADescr   * dladsc,
*       ConstSpiceDouble       vertex[3],
*       ConstSpiceDouble       raydir[3],
*       SpiceInt             * plid,
*       SpiceDouble            xpt[3],
*       SpiceBoolean         * found        )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* handle     I   Handle of DSK kernel containing plate model.
* dladsc     I   DLA descriptor of plate model segment.
* vertex     I   Ray's vertex in the  body fixed frame.
* raydir     I   Ray direction in the body fixed frame.
* plid       O   ID code of the plate intersected by the ray.
* xpt        O   Intercept.
* found      O   Flag indicating whether intercept exists.
***********************************************************************/

%rename (dskx02) dskx02_c;
%apply (void RETURN_VOID) {void dskx02_c};
%apply (ConstSpiceDLADescr *INPUT) {ConstSpiceDLADescr *dladsc};
%apply (ConstSpiceDouble IN_ARRAY1[ANY]) {ConstSpiceDouble vertex[3]};
%apply (ConstSpiceDouble IN_ARRAY1[ANY]) {ConstSpiceDouble raydir[3]};
%apply (SpiceDouble OUT_ARRAY1[ANY]) {SpiceDouble xpt[3]};

extern void dskx02_c(
        SpiceInt         handle,
        ConstSpiceDLADescr *dladsc,
        ConstSpiceDouble vertex[3],
        ConstSpiceDouble raydir[3],
        SpiceInt         *OUTPUT,
        SpiceDouble      xpt[3],
        SpiceBoolean     *OUTPUT
);

/***********************************************************************
* -Procedure dskxsi_c (DSK, ray-surface intercept with source information)
*
* -Abstract
*
* Compute a ray-surface intercept using data provided by
* multiple loaded DSK segments. Return information about
* the source of the data defining the surface on which the
* intercept was found: DSK handle, DLA and DSK descriptors,
* and DSK data type-dependent parameters.
*
* void dskxsi_c (
*       SpiceBoolean         pri,
*       ConstSpiceChar     * target,
*       SpiceInt             nsurf,
*       ConstSpiceInt        srflst[],
*       SpiceDouble          et,
*       ConstSpiceChar     * fixref,
*       ConstSpiceDouble     vertex[3],
*       ConstSpiceDouble     raydir[3],
*       SpiceInt             maxd,
*       SpiceInt             maxi,
*       SpiceDouble          xpt[3],
*       SpiceInt           * handle,
*       SpiceDLADescr      * dladsc,
*       SpiceDSKDescr      * dskdsc,
*       SpiceDouble          dc[],
*       SpiceInt             ic[],
*       SpiceBoolean       * found      )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* pri        I   Data prioritization flag.
* target     I   Target body name.
* nsurf      I   Number of surface IDs in list.
* srflst     I   Surface ID list.
* et         I   Epoch, expressed as seconds past J2000 TDB.
* fixref     I   Name of target body-fixed reference frame.
* vertex     I   Vertex of ray.
* raydir     I   Direction vector of ray.
* maxd       I   Size of DC array.
* maxi       I   Size of IC array.
* xpt        O   Intercept point.
* handle     O   Handle of segment contributing surface data.
* dladsc     O   DLA descriptor of segment.
* dskdsc     O   DSK descriptor of segment.
* dc         O   Double precision component of source info.
* ic         O   Integer component of source info.
* found      O   Found flag.
* SPICE_DSKXSI_DCSIZE
*            P    Required size of DC array.
* SPICE_DSKXSI_ICSIZE
*            P    Required size of IC array.
***********************************************************************/

%rename (dskxsi) my_dskxsi_c;
%apply (void RETURN_VOID) {void my_dskxsi_c};
%apply (ConstSpiceChar *CONST_STRING) {ConstSpiceChar *target};
%apply (SpiceInt DIM1, ConstSpiceInt IN_ARRAY1[]) {(SpiceInt nsurf, ConstSpiceInt srflst[])};
%apply (ConstSpiceChar *CONST_STRING) {ConstSpiceChar *fixref};
%apply (ConstSpiceDouble IN_ARRAY1[ANY]) {ConstSpiceDouble vertex[3]};
%apply (ConstSpiceDouble IN_ARRAY1[ANY]) {ConstSpiceDouble raydir[3]};
%apply (SpiceDouble OUT_ARRAY1[ANY]) {SpiceDouble xpt[3]};
%apply (SpiceInt *OUTPUT) {SpiceInt *handle};
%apply (SpiceDLADescr *OUTPUT) {SpiceDLADescr *dladsc};
%apply (SpiceDSKDescr *OUTPUT) {SpiceDSKDescr *dskdsc};
%apply (SpiceDouble OUT_ARRAY1[ANY]) {SpiceDouble dc[SPICE_DSKXSI_DCSIZE]};
%apply (SpiceInt OUT_ARRAY1[ANY]) {SpiceInt ic[SPICE_DSKXSI_ICSIZE]};
%apply (SpiceBoolean *OUTPUT) {SpiceBoolean *found};

%inline %{
    void my_dskxsi_c(
        SpiceBoolean     pri,
        ConstSpiceChar   *target,
        SpiceInt         nsurf, ConstSpiceInt srflst[],
        SpiceDouble      et,
        ConstSpiceChar   *fixref,
        ConstSpiceDouble vertex[3],
        ConstSpiceDouble raydir[3],
        SpiceDouble      xpt[3],
        SpiceInt         *handle,
        SpiceDLADescr    *dladsc,
        SpiceDSKDescr    *dskdsc,
        SpiceDouble      dc[SPICE_DSKXSI_DCSIZE],
        SpiceInt         ic[SPICE_DSKXSI_ICSIZE],
        SpiceBoolean     *found)
    {
        dskxsi_c(pri, target, nsurf, srflst, et, fixref, vertex, raydir,
                 SPICE_DSKXSI_DCSIZE, SPICE_DSKXSI_ICSIZE,
                 xpt, handle, dladsc, dskdsc, dc, ic, found);
    }
%}

/***********************************************************************
* -Procedure dskxv_c ( DSK, ray-surface intercept, vectorized )
*
* -Abstract
*
* Compute ray-surface intercepts for a set of rays, using data
* provided by multiple loaded DSK segments.
*
* void dskxv_c (
*       SpiceBoolean         pri,
*       ConstSpiceChar     * target,
*       SpiceInt             nsurf,
*       ConstSpiceInt        srflst[],
*       SpiceDouble          et,
*       ConstSpiceChar     * fixref,
*       SpiceInt             nrays,
*       ConstSpiceDouble     vtxarr[][3],
*       ConstSpiceDouble     dirarr[][3],
*       SpiceDouble          xptarr[][3],
*       SpiceBoolean         fndarr[]     )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* pri        I   Data prioritization flag.
* target     I   Target body name.
* nsurf      I   Number of surface IDs in list.
* srflst     I   Surface ID list.
* et         I   Epoch, expressed as seconds past J2000 TDB.
* fixref     I   Name of target body-fixed reference frame.
* nrays      I   Number of rays.
* vtxarr     I   Array of vertices of rays.
* dirarr     I   Array of direction vectors of rays.
* xptarr     O   Intercept point array.
* fndarr     O   Found flag array.
***********************************************************************/

%rename (dskxv) my_dskxv_c;
%apply (void RETURN_VOID) {void my_dskxv_c};
%apply (ConstSpiceChar *CONST_STRING)
                            {ConstSpiceChar *target};
%apply (SpiceInt DIM1, ConstSpiceInt *IN_ARRAY1)
                            {(SpiceInt nsurf, ConstSpiceInt srflst[])};
%apply (ConstSpiceChar *CONST_STRING)
                            {ConstSpiceChar *fixref};
%apply (SpiceInt DIM1, ConstSpiceDouble IN_ARRAY2[][ANY])
                            {(SpiceInt nrays, ConstSpiceDouble vtxarr[][3])};
%apply (SpiceInt DIM1, ConstSpiceDouble IN_ARRAY2[][ANY])
                            {(SpiceInt n2, ConstSpiceDouble dirarr[][3])};
%apply (SpiceInt *SIZE1, SpiceInt *SIZE2, SpiceDouble **OUT_ARRAY2)
                            {(SpiceInt *n3, SpiceInt *nv, SpiceDouble **xptarr)};
%apply (SpiceInt *SIZE1, SpiceBoolean **OUT_ARRAY1)
                            {(SpiceInt *n4, SpiceBoolean **fndarr)};

%inline %{
    void my_dskxv_c(
        SpiceBoolean   pri,
        ConstSpiceChar *target,
        SpiceInt       nsurf, ConstSpiceInt srflst[],
        SpiceDouble    et,
        ConstSpiceChar *fixref,
        SpiceInt       nrays, ConstSpiceDouble vtxarr[][3],
        SpiceInt       n2,    ConstSpiceDouble dirarr[][3],
        SpiceInt       *n3,   SpiceInt *nv, SpiceDouble **xptarr,
        SpiceInt       *n4,   SpiceBoolean **fndarr)
    {
        if (!my_assert_eq(nrays, n2, "dskxv",
            "Array dimension mismatch in dskxv: "
            "vtxarr dimension = #; dirarr dimension = #")) return;

        *n3 = nrays;
        *nv = 3;
        *n4 = nrays;
        *fndarr = my_malloc(nrays, "dskxv");
        *xptarr =  my_malloc(nrays * 3, "dskxv");
        if (*fndarr && *xptarr) {
            dskxv_c(pri, target, nsurf, srflst, et, fixref, nrays,
                    vtxarr, dirarr, *xptarr, *fndarr);
        }
    }
%}

/***********************************************************************
* -Procedure dskz02_c ( DSK, fetch type 2 model size parameters )
*
* -Abstract
*
* Return plate model size parameters---plate count and
* vertex count---for a type 2 DSK segment.
*
* void dskz02_c (
*       SpiceInt               handle,
*       ConstSpiceDLADescr   * dladsc,
*       SpiceInt             * nv,
*       SpiceInt             * np     )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* handle     I   DSK file handle.
* dladsc     I   DLA descriptor.
* nv         O   Number of vertices.
* np         O   Number of plates.
***********************************************************************/

%rename (dskz02) dskz02_c;
%apply (void RETURN_VOID) {void dskz02_c};
%apply (ConstSpiceDLADescr *INPUT) {ConstSpiceDLADescr *dladsc};

extern void dskz02_c(
        SpiceInt      handle,
        ConstSpiceDLADescr *dladsc,
        SpiceInt      *OUTPUT,
        SpiceInt      *OUTPUT
);

/***********************************************************************
* -Procedure ednmpt_c ( Ellipsoid normal vector to surface point )
*
* -Abstract
*
* Return the unique point on an ellipsoid's surface where the
* outward normal direction is a given vector.
*
* void ednmpt_c (
*       SpiceDouble         a,
*       SpiceDouble         b,
*       SpiceDouble         c,
*       ConstSpiceDouble    normal[3],
*       SpiceDouble         point[3] )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* a          I   Length of the ellipsoid semi-axis along the X-axis.
* b          I   Length of the ellipsoid semi-axis along the Y-axis.
* c          I   Length of the ellipsoid semi-axis along the Z-axis.
* normal     I   Outward normal direction.
* point      O   Point where outward normal is parallel to `normal'.
***********************************************************************/

%rename (ednmpt) ednmpt_c;
%apply (void RETURN_VOID) {void ednmpt_c};
%apply (ConstSpiceDouble IN_ARRAY1[ANY]) {ConstSpiceDouble normal[3]};
%apply (SpiceDouble OUT_ARRAY1[ANY]) {SpiceDouble point[3]};

extern void ednmpt_c(
        SpiceDouble      a,
        SpiceDouble      b,
        SpiceDouble      c,
        ConstSpiceDouble normal[3],
        SpiceDouble      point[3]
);

//Vector version
VECTORIZE_3d_dX__dN(ednmpt, ednmpt_c, 3)

/***********************************************************************
* -Procedure edpnt_c ( Ellipsoid point  )
*
* -Abstract
*
* Scale a point so that it lies on the surface of a specified
* triaxial ellipsoid that is centered at the origin and aligned
* with the Cartesian coordinate axes.
*
* void edpnt_c (
*       ConstSpiceDouble    p[3],
*       SpiceDouble         a,
*       SpiceDouble         b,
*       SpiceDouble         c,
*       SpiceDouble         ep[3] )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* p          I   A point in three-dimensional space.
* a          I   Semi-axis length in the X direction.
* b          I   Semi-axis length in the Y direction.
* c          I   Semi-axis length in the Z direction.
* ep         O   Point on ellipsoid.
***********************************************************************/

%rename (edpnt) edpnt_c;
%apply (void RETURN_VOID) {void edpnt_c};
%apply (ConstSpiceDouble IN_ARRAY1[ANY]) {ConstSpiceDouble p[3]};
%apply (SpiceDouble OUT_ARRAY1[ANY]) {SpiceDouble ep[3]};

extern void edpnt_c(
        ConstSpiceDouble p[3],
        SpiceDouble      a,
        SpiceDouble      b,
        SpiceDouble      c,
        SpiceDouble      ep[3]
);

//Vector version
VECTORIZE_dX_3d__dN(edpnt, edpnt_c, 3)

/***********************************************************************
* -Procedure ekacec_c ( EK, add character data to column )
*
* -Abstract
*
* Add data to a character column in a specified EK record.
*
* void ekacec_c (
*       SpiceInt          handle,
*       SpiceInt          segno,
*       SpiceInt          recno,
*       ConstSpiceChar  * column,
*       SpiceInt          nvals,
*       SpiceInt          cvalen,
*       const void        cvals[][],
*       SpiceBoolean      isnull )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* handle     I   EK file handle.
* segno      I   Index of segment containing record.
* recno      I   Record to which data is to be added.
* column     I   Column name.
* nvals      I   Number of values to add to column.
* cvalen     I   Declared length of character values.
* cvals      I   Character values to add to column.
* isnull     I   Flag indicating whether column entry is null.
***********************************************************************/

%rename (ekacec) ekacec_c;
%apply (void RETURN_VOID) {void ekacec_c};
%apply (SpiceInt DIM1, SpiceInt DIM2, ConstSpiceChar *IN_STRINGS)
                {(SpiceInt nvals, SpiceInt cvalen, ConstSpiceChar *cvals)};

extern void ekacec_c(
        SpiceInt       handle,
        SpiceInt       segno,
        SpiceInt       recno,
        ConstSpiceChar *CONST_STRING,
        SpiceInt       nvals, SpiceInt cvalen, ConstSpiceChar *cvals,
        SpiceBoolean   isnull
);

/***********************************************************************
* -Procedure ekaced_c ( EK, add d.p. data to column )
*
* -Abstract
*
* Add data to an floating-point column in a specified EK record.
*
* void ekaced_c (
*       SpiceInt            handle,
*       SpiceInt            segno,
*       SpiceInt            recno,
*       ConstSpiceChar    * column,
*       SpiceInt            nvals,
*       ConstSpiceDouble  * dvals,
*       SpiceBoolean        isnull )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* handle     I   EK file handle.
* segno      I   Index of segment containing record.
* recno      I   Record to which data is to be added.
* column     I   Column name.
* nvals      I   Number of values to add to column.
* dvals      I   Double precision values to add to column.
* isnull     I   Flag indicating whether column entry is null.
***********************************************************************/

%rename (ekaced) ekaced_c;
%apply (void RETURN_VOID) {void ekaced_c};
%apply (SpiceInt DIM1, ConstSpiceDouble IN_ARRAY1[])
                {(SpiceInt nvals, ConstSpiceDouble dvals[])};

extern void ekaced_c(
        SpiceInt         handle,
        SpiceInt         segno,
        SpiceInt         recno,
        ConstSpiceChar   *CONST_STRING,
        SpiceInt         nvals, ConstSpiceDouble dvals[],
        SpiceBoolean     isnull
);

/***********************************************************************
* -Procedure ekacei_c ( EK, add integer data to column )
*
* -Abstract
*
* Add data to an integer column in a specified EK record.
*
* void ekacei_c (
*       SpiceInt          handle,
*       SpiceInt          segno,
*       SpiceInt          recno,
*       ConstSpiceChar  * column,
*       SpiceInt          nvals,
*       ConstSpiceInt   * ivals,
*       SpiceBoolean      isnull )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* handle     I   EK file handle.
* segno      I   Index of segment containing record.
* recno      I   Record to which data is to be added.
* column     I   Column name.
* nvals      I   Number of values to add to column.
* ivals      I   Integer values to add to column.
* isnull     I   Flag indicating whether column entry is null.
***********************************************************************/

%rename (ekacei) ekacei_c;
%apply (void RETURN_VOID) {void ekacei_c};
%apply (ConstSpiceChar *CONST_STRING) {ConstSpiceChar *column};
%apply (SpiceInt DIM1, ConstSpiceInt IN_ARRAY1[])
                    {(SpiceInt nvals, ConstSpiceInt ivals[])};

extern void ekacei_c(
        SpiceInt       handle,
        SpiceInt       segno,
        SpiceInt       recno,
        ConstSpiceChar *CONST_STRING,
        SpiceInt       nvals, ConstSpiceInt ivals[],
        SpiceBoolean   isnull
);

/***********************************************************************
* -Procedure ekaclc_c ( EK, add character column to segment )
*
* -Abstract
*
* Add an entire character column to an EK segment.
*
* void ekaclc_c (
*       SpiceInt                handle,
*       SpiceInt                segno,
*       ConstSpiceChar        * column,
*       SpiceInt                vallen,
*       const void              cvals[][],
*       ConstSpiceInt         * entszs,
*       ConstSpiceBoolean     * nlflgs,
*       ConstSpiceInt         * rcptrs,
*       SpiceInt              * wkindx  )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* handle     I   EK file handle.
* segno      I   Number of segment to add column to.
* column     I   Column name.
* vallen     I   Length of character values.
* cvals      I   Character values to add to column.
* entszs     I   Array of sizes of column entries.
* nlflgs     I   Array of null flags for column entries.
* rcptrs     I   Record pointers for segment.
* wkindx    I-O  Work space for column index.
***********************************************************************/

// TODO(FY): Create the right typemap for cvals, or use an existing one and throw away unused value?
%rename (ekaclc) my_ekaclc_c;
%apply (void RETURN_VOID) {void my_ekaclc_c};
%apply (ConstSpiceChar *CONST_STRING) {ConstSpiceChar *column};
%apply (SpiceInt DIM1, SpiceInt DIM2, ConstSpiceChar *IN_STRINGS)
                    {(SpiceInt ignore, SpiceInt vallen, ConstSpiceChar *cvals)};
%apply (ConstSpiceInt     IN_ARRAY1[]) {ConstSpiceInt     entszs[]};
%apply (ConstSpiceBoolean IN_ARRAY1[]) {ConstSpiceBoolean nlflgs[]};
%apply (ConstSpiceInt     IN_ARRAY1[]) {ConstSpiceInt     rcptrs[]};

%inline %{
    void my_ekaclc_c(
        SpiceInt          handle,
        SpiceInt          segno,
        ConstSpiceChar    *column,
        SpiceInt          ignore, SpiceInt vallen, ConstSpiceChar *cvals,
        ConstSpiceInt     entszs[],
        ConstSpiceBoolean nlflgs[],
        ConstSpiceInt     rcptrs[])
    {
        SpiceInt wkindx[MAXROWS];

        ekaclc_c(handle, segno, column, vallen, cvals, entszs, nlflgs, rcptrs,
                 wkindx);
    }
%}

/***********************************************************************
* -Procedure ekacld_c ( EK, add double precision column to segment )
*
* -Abstract
*
* Add an entire floating-point column to an EK segment.
*
* void ekacld_c (
*       SpiceInt                handle,
*       SpiceInt                segno,
*       ConstSpiceChar        * column,
*       ConstSpiceDouble      * dvals,
*       ConstSpiceInt         * entszs,
*       ConstSpiceBoolean     * nlflgs,
*       ConstSpiceInt         * rcptrs,
*       SpiceInt              * wkindx  )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* handle     I   EK file handle.
* segno      I   Number of segment to add column to.
* column     I   Column name.
* dvals      I   Double precision values to add to column.
* entszs     I   Array of sizes of column entries.
* nlflgs     I   Array of null flags for column entries.
* rcptrs     I   Record pointers for segment.
* wkindx    I-O  Work space for column index.
***********************************************************************/

%rename (ekacld) my_ekacld_c;
%apply (void RETURN_VOID) {void my_ekacld_c};
%apply (ConstSpiceChar *CONST_STRING) {ConstSpiceChar *column};
%apply (ConstSpiceDouble  IN_ARRAY1[]) {ConstSpiceDouble  dvals[]};
%apply (ConstSpiceInt     IN_ARRAY1[]) {ConstSpiceInt     entszs[]};
%apply (ConstSpiceBoolean IN_ARRAY1[]) {ConstSpiceBoolean nlflgs[]};
%apply (ConstSpiceInt     IN_ARRAY1[]) {ConstSpiceInt     rcptrs[]};

%inline %{
    void my_ekacld_c(
        SpiceInt          handle,
        SpiceInt          segno,
        ConstSpiceChar    *column,
        ConstSpiceDouble  dvals[],
        ConstSpiceInt     entszs[],
        ConstSpiceBoolean nlflgs[],
        ConstSpiceInt     rcptrs[])
    {
        SpiceInt wkindx[MAXROWS];

        ekacld_c(handle, segno, column, dvals, entszs, nlflgs, rcptrs,
                 wkindx);
    }
%}

/***********************************************************************
* -Procedure ekacli_c ( EK, add integer column to segment )
*
* -Abstract
*
* Add an entire integer column to an EK segment.
*
* void ekacli_c (
*       SpiceInt                handle,
*       SpiceInt                segno,
*       ConstSpiceChar        * column,
*       ConstSpiceInt         * ivals,
*       ConstSpiceInt         * entszs,
*       ConstSpiceBoolean     * nlflgs,
*       ConstSpiceInt         * rcptrs,
*       SpiceInt              * wkindx  )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* handle     I   EK file handle.
* segno      I   Number of segment to add column to.
* column     I   Column name.
* ivals      I   Integer values to add to column.
* entszs     I   Array of sizes of column entries.
* nlflgs     I   Array of null flags for column entries.
* rcptrs     I   Record pointers for segment.
* wkindx    I-O  Work space for column index.
***********************************************************************/

%rename (ekacli) my_ekacli_c;
%apply (void RETURN_VOID) {void my_ekacli_c};
%apply (ConstSpiceChar *CONST_STRING) {ConstSpiceChar *column};
%apply (ConstSpiceInt     IN_ARRAY1[]) {ConstSpiceInt     ivals[]};
%apply (ConstSpiceInt     IN_ARRAY1[]) {ConstSpiceInt     entszs[]};
%apply (ConstSpiceBoolean IN_ARRAY1[]) {ConstSpiceBoolean nlflgs[]};
%apply (ConstSpiceInt     IN_ARRAY1[]) {ConstSpiceInt     rcptrs[]};

%inline %{
    void my_ekacli_c(
        SpiceInt          handle,
        SpiceInt          segno,
        ConstSpiceChar    *column,
        ConstSpiceInt     ivals[],
        ConstSpiceInt     entszs[],
        ConstSpiceBoolean nlflgs[],
        ConstSpiceInt     rcptrs[])
    {
        SpiceInt wkindx[MAXROWS];

        ekacli_c(handle, segno, column, ivals, entszs, nlflgs, rcptrs,
                 wkindx);
    }
%}

/***********************************************************************
* -Procedure ekappr_c ( EK, append record onto segment )
*
* -Abstract
*
* Append a new, empty record at the end of a specified E-kernel
* segment.
*
* void ekappr_c (
*       SpiceInt     handle,
*       SpiceInt     segno,
*       SpiceInt   * recno  )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* handle     I   File handle.
* segno      I   Segment number.
* recno      O   Number of appended record.
***********************************************************************/

%rename (ekappr) ekappr_c;
%apply (void RETURN_VOID) {void ekappr_c};

extern void ekappr_c(
        SpiceInt handle,
        SpiceInt segno,
        SpiceInt *OUTPUT
);

/***********************************************************************
* -Procedure ekbseg_c ( EK, start new segment )
*
* -Abstract
*
* Start a new segment in an E-kernel.
*
* void ekbseg_c (
*       SpiceInt           handle,
*       ConstSpiceChar   * tabnam,
*       SpiceInt           ncols,
*       SpiceInt           cnamln,
*       const void         cnames[][],
*       SpiceInt           declen,
*       const void         decls[][],
*       SpiceInt         * segno  )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* handle     I   File handle.
* tabnam     I   Table name.
* ncols      I   Number of columns in the segment.
* cnamln     I   Length of names in column name array.
* cnames     I   Names of columns.
* declen     I   Length of declaration strings in declaration array.
* decls      I   Declarations of columns.
* segno      O   Segment number.
***********************************************************************/

%rename (ekbseg) my_ekbseg_c;
%apply (void RETURN_VOID) {void ekbseg_c};
%apply (ConstSpiceChar *CONST_STRING) {ConstSpiceChar *tabnam};
%apply (SpiceInt DIM1, SpiceInt DIM2, ConstSpiceChar *IN_STRINGS)
            {(SpiceInt ncols, SpiceInt cnamln, ConstSpiceChar *cnames)};
%apply (SpiceInt DIM1, SpiceInt DIM2, ConstSpiceChar *IN_STRINGS)
                {(SpiceInt ignore, SpiceInt declen, ConstSpiceChar *decls)};
%apply (SpiceInt *OUTPUT) {SpiceInt *segno};

%inline %{
    void my_ekbseg_c(
        SpiceInt       handle,
        ConstSpiceChar *tabnam,
        SpiceInt       ncols,  SpiceInt cnamln, ConstSpiceChar *cnames,
        SpiceInt       ignore, SpiceInt  declen,  ConstSpiceChar *decls,
        SpiceInt       *segno)
    {
        ekbseg_c(handle, tabnam, ncols, cnamln, cnames, declen, decls, segno);
    }
%}

/***********************************************************************
* -Procedure ekccnt_c ( EK, column count )
*
* -Abstract
*
* Return the number of distinct columns in a specified, currently
* loaded table.
*
* void ekccnt_c (
*       ConstSpiceChar  * table,
*       SpiceInt        * ccount )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* table      I   Name of table.
* ccount     O   Count of distinct, currently loaded columns.
***********************************************************************/

%rename (ekccnt) ekccnt_c;
%apply (void RETURN_VOID) {void ekccnt_c};
%apply (ConstSpiceChar *CONST_STRING) {ConstSpiceChar *table};

extern void ekccnt_c(
        ConstSpiceChar *CONST_STRING,
        SpiceInt       *OUTPUT
);

/***********************************************************************
* -Procedure ekcii_c  ( EK, column info by index )
*
* -Abstract
*
* Return attribute information about a column belonging to a loaded
* EK table, specifying the column by table and index.
*
* void ekcii_c (
*       ConstSpiceChar   * table,
*       SpiceInt           cindex,
*       SpiceInt           collen,
*       SpiceChar        * column,
*       SpiceEKAttDsc    * attdsc  )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* table      I   Name of table containing column.
* cindex     I   Index of column whose attributes are to be found.
* collen     I   Maximum allowed length of column name.
* column     O   Name of column.
* attdsc     O   Column attribute descriptor.
* cclass     O   Column class code.
* dtype      O   Data type code: 0 for character; 1 for floating-point; 2 for integer; 3 for time.
* strlen     O   String length.
* size       O   Column entry size; this is the number of array elements in a column entry.
* indexd     O   True if the column is indexed; False otherwise.
* nullok     O   True if the column may contain null values; False otherwise.
***********************************************************************/

%rename (ekcii) my_ekcii_c;
%apply (void RETURN_VOID) {void my_ekcii_c};
%apply (ConstSpiceChar *CONST_STRING) {ConstSpiceChar *table};
%apply (SpiceInt DIM1, SpiceChar OUT_STRING[ANY])
                    {(SpiceInt collen, SpiceChar column[NAMELEN])};
%apply (SpiceInt     *OUTPUT) {SpiceInt     *cclass};
%apply (SpiceInt     *OUTPUT) {SpiceInt     *dtype};
%apply (SpiceInt     *OUTPUT) {SpiceInt     *strlen};
%apply (SpiceInt     *OUTPUT) {SpiceInt     *size};
%apply (SpiceBoolean *OUTPUT) {SpiceBoolean *indexd};
%apply (SpiceBoolean *OUTPUT) {SpiceBoolean *nullok};

%inline %{
    void my_ekcii_c(
        ConstSpiceChar *table,
        SpiceInt       cindex,
        SpiceInt       collen, SpiceChar column[NAMELEN],
        SpiceInt       *cclass,
        SpiceInt       *dtype,
        SpiceInt       *strlen,
        SpiceInt       *size,
        SpiceBoolean   *indexd,
        SpiceBoolean   *nullok)
    {
        SpiceEKAttDsc attdsc;

        ekcii_c(table, cindex, collen, column, &attdsc);

        *cclass = attdsc.cclass;
        *dtype  = (int) attdsc.dtype;
        *strlen = attdsc.strlen;
        *size   = attdsc.size;
        *indexd = attdsc.indexd;
        *nullok = attdsc.nullok;
    }
%}

/***********************************************************************
* -Procedure ekcls_c ( EK, close file )
*
* -Abstract
*
* Close an E-kernel.
*
* void ekcls_c (
*       SpiceInt handle )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* handle     I   EK file handle.
***********************************************************************/

%rename (ekcls) ekcls_c;
%apply (void RETURN_VOID) {void ekcls_c};

extern void ekcls_c(
        SpiceInt handle
);

/***********************************************************************
* -Procedure ekdelr_c ( EK, delete record from segment )
*
* -Abstract
*
* Delete a specified record from a specified E-kernel segment.
*
* void ekdelr_c (
*       SpiceInt   handle,
*       SpiceInt   segno,
*       SpiceInt   recno )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* handle     I   File handle.
* segno      I   Segment number.
* recno      I   Record number.
***********************************************************************/

%rename (ekdelr) ekdelr_c;
%apply (void RETURN_VOID) {void ekdelr_c};

extern void ekdelr_c(
        SpiceInt handle,
        SpiceInt segno,
        SpiceInt recno
);

/***********************************************************************
* -Procedure ekffld_c ( EK, finish fast write )
*
* -Abstract
*
* Complete a fast write operation on a new E-kernel segment.
*
* void ekffld_c (
*       SpiceInt     handle,
*       SpiceInt     segno,
*       SpiceInt   * rcptrs )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* handle     I   File handle.
* segno      I   Segment number.
* rcptrs     I   Record pointers.
***********************************************************************/

%rename (ekffld) ekffld_c;
%apply (void RETURN_VOID) {void ekffld_c};
%apply (SpiceInt IN_ARRAY1[]) {SpiceInt rcptrs[]};

extern void ekffld_c(
        SpiceInt handle,
        SpiceInt segno,
        SpiceInt rcptrs[]
);

/***********************************************************************
* -Procedure ekfind_c ( EK, find data )
*
* -Abstract
*
* Find E-kernel data that satisfy a set of constraints.
*
* void ekfind_c (
*       ConstSpiceChar    * query,
*       SpiceInt            errmln,
*       SpiceInt          * nmrows,
*       SpiceBoolean      * error,
*       SpiceChar         * errmsg )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* query      I   Query specifying data to be found.
* errmln     I   Declared length of output error message string.
* nmrows     O   Number of matching rows.
* error      O   Flag indicating whether query parsed correctly.
* errmsg     O   Parse error description.
***********************************************************************/

%rename (ekfind) my_ekfind_c;
%apply (void RETURN_VOID) {void my_ekfind_c};
%apply (ConstSpiceChar *CONST_STRING) {ConstSpiceChar *query};
%apply (SpiceInt       *OUTPUT) {SpiceInt *nmrows};
%apply (SpiceBoolean   *OUTPUT) {SpiceBoolean *error};
%apply (SpiceChar OUT_STRING[ANY]) {SpiceChar errmsg[MESSAGELEN]};

%inline %{
    void my_ekfind_c(
        ConstSpiceChar *query,
        SpiceInt       *nmrows,
        SpiceBoolean   *error,
        SpiceChar      errmsg[MESSAGELEN])
    {
        ekfind_c(query, MESSAGELEN, nmrows, error, errmsg);
    }
%}

/***********************************************************************
* -Procedure ekgc_c  ( EK, get event data, character )
*
* -Abstract
*
* Return an element of an entry in a column of character
* type in a specified row.
*
* void ekgc_c (
*       SpiceInt          selidx,
*       SpiceInt          row,
*       SpiceInt          elment,
*       SpiceInt          cdatln,
*       SpiceChar       * cdata,
*       SpiceBoolean    * null,
*       SpiceBoolean    * found  )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* selidx     I   Index of parent column in SELECT clause.
* row        I   Row to fetch from.
* elment     I   Index of element, within column entry, to fetch.
* cdatln     I   Maximum length of column element.
* cdata      O   Character string element of column entry.
* null       O   Flag indicating whether column entry was null.
* found      O   Flag indicating whether column was present in row.
***********************************************************************/

%rename (ekgc) ekgc_c;
%apply (void RETURN_VOID) {void ekgc_c};
%apply (SpiceInt DIM1, SpiceChar OUT_STRING[ANY])
                    {(SpiceInt cdatln, SpiceChar cdata[COLLEN])};

extern void ekgc_c(
        SpiceInt     selidx,
        SpiceInt     row,
        SpiceInt     elment,
        SpiceInt     cdatln,        SpiceChar cdata[COLLEN],
        SpiceBoolean *OUTPUT,
        SpiceBoolean *OUTPUT
);

/***********************************************************************
* -Procedure ekgd_c  ( EK, get event data, double precision )
*
* -Abstract
*
* Return an element of an entry in a column of floating-point
* type in a specified row.
*
* void ekgd_c (
*       SpiceInt          selidx,
*       SpiceInt          row,
*       SpiceInt          elment,
*       SpiceDouble     * ddata,
*       SpiceBoolean    * null,
*       SpiceBoolean    * found  )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* selidx     I   Index of parent column in SELECT clause.
* row        I   Row to fetch from.
* elment     I   Index of element, within column entry, to fetch.
* ddata      O   Double precision element of column entry.
* null       O   Flag indicating whether column entry was null.
* found      O   Flag indicating whether column was present in row.
***********************************************************************/

%rename (ekgd) ekgd_c;
%apply (void RETURN_VOID) {void ekgd_c};

extern void ekgd_c(
        SpiceInt     selidx,
        SpiceInt     row,
        SpiceInt     elment,
        SpiceDouble  *OUTPUT,
        SpiceBoolean *OUTPUT,
        SpiceBoolean *OUTPUT
);

/***********************************************************************
* -Procedure ekgi_c  ( EK, get event data, integer )
*
* -Abstract
*
* Return an element of an entry in a column of integer
* type in a specified row.
*
* void ekgi_c (
*       SpiceInt          selidx,
*       SpiceInt          row,
*       SpiceInt          elment,
*       SpiceInt        * idata,
*       SpiceBoolean    * null,
*       SpiceBoolean    * found  )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* selidx     I   Index of parent column in SELECT clause.
* row        I   Row to fetch from.
* elment     I   Index of element, within column entry, to fetch.
* idata      O   Integer element of column entry.
* null       O   Flag indicating whether column entry was null.
* found      O   Flag indicating whether column was present in row.
***********************************************************************/

%rename (ekgi) ekgi_c;
%apply (void RETURN_VOID) {void ekgi_c};

extern void ekgi_c(
        SpiceInt     selidx,
        SpiceInt     row,
        SpiceInt     elment,
        SpiceInt     *OUTPUT,
        SpiceBoolean *OUTPUT,
        SpiceBoolean *OUTPUT
);

/***********************************************************************
* -Procedure ekifld_c ( EK, initialize segment for fast write )
*
* -Abstract
*
* Initialize a new E-kernel segment to allow fast writing.
*
* void ekifld_c (
*       SpiceInt           handle,
*       ConstSpiceChar   * tabnam,
*       SpiceInt           ncols,
*       SpiceInt           nrows,
*       SpiceInt           cnamln,
*       const void         cnames[][],
*       SpiceInt           declen,
*       const void         decls[][],
*       SpiceInt         * segno,
*       SpiceInt         * rcptrs )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* handle     I   File handle.
* tabnam     I   Table name.
* ncols      I   Number of columns in the segment.
* nrows      I   Number of rows in the segment.
* cnamln     I   Length of names in column name array.
* cnames     I   Names of columns.
* declen     I   Length of declaration strings in declaration array.
* decls      I   Declarations of columns.
* segno      O   Segment number.
* rcptrs     O   Array of record pointers.
***********************************************************************/

%rename (ekifld) my_ekifld_c;
%apply (void RETURN_VOID) {void my_ekifld_c};
%apply (ConstSpiceChar *CONST_STRING) {ConstSpiceChar *tabnam};
%apply (SpiceInt DIM1, SpiceInt DIM2, ConstSpiceChar *IN_STRINGS)
                    {(SpiceInt ncols, SpiceInt cnamln, ConstSpiceChar *cnames)};
%apply (SpiceInt DIM1, SpiceInt DIM2, ConstSpiceChar *IN_STRINGS)
                    {(SpiceInt ignore, SpiceInt declen, ConstSpiceChar *decls)};
%apply (SpiceInt *OUTPUT) {SpiceInt *segno};
%apply (SpiceInt *SIZE1, SpiceInt OUT_ARRAY1[ANY])
                    {(SpiceInt *nrows1, SpiceInt rcptrs[MAXROWS])};

%inline %{
    void my_ekifld_c(
        SpiceInt       handle,
        ConstSpiceChar *tabnam,
        SpiceInt       nrows,
        SpiceInt       ncols, SpiceInt cnamln, ConstSpiceChar *cnames,
        SpiceInt       ignore, SpiceInt declen, ConstSpiceChar *decls,
        SpiceInt       *segno,
        SpiceInt       *nrows1, SpiceInt rcptrs[MAXROWS])
    {
        *nrows1 = nrows;
        ekifld_c(handle, tabnam, ncols, nrows, cnamln, cnames, declen, decls,
                 segno, rcptrs);
    }
%}

/***********************************************************************
* -Procedure ekinsr_c ( EK, insert record into segment )
*
* -Abstract
*
* Add a new, empty record to a specified E-kernel segment at
* a specified index.
*
* void ekinsr_c (
*       SpiceInt  handle,
*       SpiceInt  segno,
*       SpiceInt  recno )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* handle     I   File handle.
* segno      I   Segment number.
* recno      I   Record number.
***********************************************************************/

%rename (ekinsr) ekinsr_c;
%apply (void RETURN_VOID) {void ekinsr_c};

extern void ekinsr_c(
        SpiceInt handle,
        SpiceInt segno,
        SpiceInt recno
);

/***********************************************************************
* -Procedure eklef_c ( EK, load event file )
*
* -Abstract
*
* Load an EK file, making it accessible to the EK readers.
*
* void eklef_c (
*       ConstSpiceChar  * fname,
*       SpiceInt        * handle )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* fname      I   Name of EK file to load.
* handle     O   File handle of loaded EK file.
***********************************************************************/

%rename (eklef) eklef_c;
%apply (void RETURN_VOID) {void eklef_c};

extern void eklef_c(
        ConstSpiceChar *CONST_STRING,
        SpiceInt       *OUTPUT
);

/***********************************************************************
* -Procedure eknelt_c  ( EK, get number of elements in column entry )
*
* -Abstract
*
* Return the number of elements in a specified column entry in
* the current row.
*
* SpiceInt eknelt_c (
*       SpiceInt  selidx,
*       SpiceInt  row     )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* selidx     I   Index of parent column in SELECT clause.
* row        I   Row containing element.
* count      R   Number of elements in column.
***********************************************************************/

%rename (eknelt) eknelt_c;
%apply (SpiceInt RETURN_INT) {SpiceInt eknelt_c};

extern SpiceInt eknelt_c(
        SpiceInt selidx,
        SpiceInt row
);

/***********************************************************************
* -Procedure eknseg_c ( EK, number of segments in file )
*
* -Abstract
*
* Return the number of segments in a specified EK.
*
* SpiceInt eknseg_c (
*       SpiceInt handle )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* handle     I   EK file handle.
* count      R   Numer of segments.
***********************************************************************/

%rename (eknseg) eknseg_c;
%apply (SpiceInt RETURN_INT) {SpiceInt eknseg_c};

extern SpiceInt eknseg_c(
        SpiceInt handle
);

/***********************************************************************
* -Procedure ekntab_c  ( EK, return number of loaded tables )
*
* -Abstract
*
* Return the number of loaded EK tables.
*
* void ekntab_c (
*       SpiceInt   * n )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* n          O   Number of loaded tables.
***********************************************************************/

%rename (ekntab) ekntab_c;
%apply (void RETURN_VOID) {void ekntab_c};

extern void ekntab_c(
        SpiceInt *OUTPUT
);

/***********************************************************************
* -Procedure ekopn_c ( EK, open new file )
*
* -Abstract
*
* Open a new E-kernel file and prepare the file for writing.
*
* void ekopn_c (
*       ConstSpiceChar    * fname,
*       ConstSpiceChar    * ifname,
*       SpiceInt            ncomch,
*       SpiceInt          * handle )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* fname      I   Name of EK file.
* ifname     I   Internal file name.
* ncomch     I   The number of characters to reserve for comments.
* handle     O   Handle attached to new EK file.
***********************************************************************/

%rename (ekopn) ekopn_c;
%apply (void RETURN_VOID) {void ekopn_c};

extern void ekopn_c(
        ConstSpiceChar *CONST_STRING,
        ConstSpiceChar *CONST_STRING,
        SpiceInt       ncomch,
        SpiceInt       *handle
);

/***********************************************************************
* -Procedure ekopr_c ( EK, open file for reading )
*
* -Abstract
*
* Open an existing E-kernel file for reading.
*
* void ekopr_c (
*       ConstSpiceChar  * fname,
*       SpiceInt        * handle )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* fname      I   Name of EK file.
* handle     O   Handle attached to EK file.
***********************************************************************/

%rename (ekopr) ekopr_c;
%apply (void RETURN_VOID) {void ekopr_c};

extern void ekopr_c(
        ConstSpiceChar *CONST_STRING,
        SpiceInt       *OUTPUT
);

/***********************************************************************
* -Procedure ekops_c ( EK, open scratch file )
*
* -Abstract
*
* Open a scratch (temporary) E-kernel file and prepare the file
* for writing.
*
* void ekops_c (
*       SpiceInt   * handle )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* handle     O   File handle attached to new EK file.
***********************************************************************/

%rename (ekops) ekops_c;
%apply (void RETURN_VOID) {void ekops_c};

extern void ekops_c(
        SpiceInt *OUTPUT
);

/***********************************************************************
* -Procedure ekopw_c ( EK, open file for writing )
*
* -Abstract
*
* Open an existing E-kernel file for writing.
*
* void ekopw_c (
*       ConstSpiceChar  * fname,
*       SpiceInt        * handle )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* fname      I   Name of EK file.
* handle     O   Handle attached to EK file.
***********************************************************************/

%rename (ekopw) ekopw_c;
%apply (void RETURN_VOID) {void ekopw_c};
%apply (ConstSpiceChar *CONST_STRING) {ConstSpiceChar *fname};

extern void ekopw_c(
        ConstSpiceChar *CONST_STRING,
        SpiceInt       *OUTPUT
);

/***********************************************************************
* -Procedure ekpsel_c ( EK, parse SELECT clause )
*
* -Abstract
*
* Parse the SELECT clause of an EK query, returning full particulars
* concerning each selected item.
*
* void ekpsel_c (
*       ConstSpiceChar        * query,
*       SpiceInt                msglen,
*       SpiceInt                tablen,
*       SpiceInt                collen,
*       SpiceInt              * n,
*       SpiceInt              * xbegs,
*       SpiceInt              * xends,
*       SpiceEKDataType       * xtypes,
*       SpiceEKExprClass      * xclass,
*       void                  * tabs,
*       void                  * cols,
*       SpiceBoolean          * error,
*       SpiceChar             * errmsg  )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* query      I   EK query.
* msglen     I   Available space in the output error message string.
* tablen     I   Length of strings in `tabs' output array.
* collen     I   Length of strings in `cols' output array.
* n          O   Number of items in SELECT clause of `query'.
* xbegs      O   Begin positions of expressions in SELECT clause.
* xends      O   End positions of expressions in SELECT clause.
* xtypes     O   Data types of expressions.
* xclass     O   Classes of expressions.
* tabs       O   Names of tables qualifying SELECT columns.
* cols       O   Names of columns in SELECT clause of `query'.
* error      O   Error flag.
* errmsg     O   Parse error message.
***********************************************************************/

%rename (ekpsel) my_ekpsel_c;
%apply (void RETURN_VOID) {void my_ekpsel_c};
%apply (ConstSpiceChar *CONST_STRING) {ConstSpiceChar *query};
%apply (SpiceInt *SIZE1, SpiceInt OUT_ARRAY1[ANY]) {(SpiceInt *n,  SpiceInt xbegs[CLAUSES])};
%apply (SpiceInt OUT_ARRAY1[ANY], SpiceInt *SIZE1) {(SpiceInt xends[CLAUSES],  SpiceInt *n1)};
%apply (SpiceInt OUT_ARRAY1[ANY], SpiceInt *SIZE1) {(SpiceInt xtypes[CLAUSES], SpiceInt *n2)};
%apply (SpiceInt OUT_ARRAY1[ANY], SpiceInt *SIZE1) {(SpiceInt xclass[CLAUSES], SpiceInt *n3)};
%apply (SpiceChar OUT_STRINGS[ANY][ANY], SpiceInt *NSTRINGS) {(SpiceChar tabs[CLAUSES][NAMELEN], SpiceInt *n4)};
%apply (SpiceChar OUT_STRINGS[ANY][ANY], SpiceInt *NSTRINGS) {(SpiceChar cols[CLAUSES][NAMELEN], SpiceInt *n5)};
%apply (SpiceBoolean *OUTPUT) {SpiceBoolean *error};
%apply (SpiceChar OUT_STRING[ANY]) {SpiceChar errmsg[MESSAGELEN]};

%inline %{
    void my_ekpsel_c(
        ConstSpiceChar *query,
        SpiceInt       *n,
        SpiceInt       xbegs[CLAUSES],
        SpiceInt       xends[CLAUSES],  SpiceInt *n1,
        SpiceInt       xtypes[CLAUSES], SpiceInt *n2,
        SpiceInt       xclass[CLAUSES], SpiceInt *n3,
        SpiceChar      tabs[CLAUSES][NAMELEN], SpiceInt *n4,
        SpiceChar      cols[CLAUSES][NAMELEN], SpiceInt *n5,
        SpiceBoolean   *error,
        SpiceChar      errmsg[MESSAGELEN])
    {
        SpiceEKDataType xtypes_[CLAUSES];   // 0 = char, 1 = float, 2 = int, 3 = time
        SpiceEKExprClass xclass_[CLAUSES];  // SPICE_EK_EXP_COL = 0 for column
                                            // SPICE_EK_EXP_FUNC = 1 for simple function
                                            // SPICE_EK_EXP_EXPR = 2 for general expression

        ekpsel_c(query, MESSAGELEN, NAMELEN, NAMELEN, n, xbegs, xends,
                 xtypes_, xclass_, tabs, cols, error, errmsg);
        if (*error) {
            *n1 = 0;
            *n2 = 0;
            *n3 = 0;
            *n4 = 0;
            *n5 = 0;
        } else {
            *n1 = *n;
            *n2 = *n;
            *n3 = *n;
            *n4 = *n;
            *n5 = *n;

            for (int j = 0; j < *n; j++) {
                xtypes[j] = (SpiceInt) xtypes_[j];
                xclass[j] = (SpiceInt) xclass_[j];
            }
        }
    }
%}

/***********************************************************************
* -Procedure ekrcec_c ( EK, read column entry element, character )
*
* -Abstract
*
* Read data from a character column in a specified EK record.
*
* void ekrcec_c (
*       SpiceInt           handle,
*       SpiceInt           segno,
*       SpiceInt           recno,
*       ConstSpiceChar   * column,
*       SpiceInt           cvalen,
*       SpiceInt         * nvals,
*       void             * cvals,
*       SpiceBoolean     * isnull )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* handle     I   Handle attached to EK file.
* segno      I   Index of segment containing record.
* recno      I   Record from which data is to be read.
* column     I   Column name.
* cvalen     I   Maximum length of output strings.
* nvals      O   Number of values in column entry.
* cvals      O   Character values in column entry.
* isnull     O   Flag indicating whether column entry is null.
***********************************************************************/

%rename (ekrcec) ekrcec_c;
%apply (void RETURN_VOID) {void ekrcec_c};
%apply (ConstSpiceChar *CONST_STRING) {ConstSpiceChar *column};
%apply (SpiceInt DIM2, SpiceInt *NSTRINGS, SpiceChar OUT_STRINGS[ANY][ANY])
            {(SpiceInt cvalen, SpiceInt *nvals, SpiceChar cvals[MAXVALS][COLLEN])};


extern void ekrcec_c(
        SpiceInt       handle,
        SpiceInt       segno,
        SpiceInt       recno,
        ConstSpiceChar *CONST_STRING,
        SpiceInt       cvalen, SpiceInt *nvals, SpiceChar cvals[MAXVALS][COLLEN],
        SpiceBoolean   *OUTPUT
);

/***********************************************************************
* -Procedure ekrced_c ( EK, read column entry element, d.p. )
*
* -Abstract
*
* Read data from a floating-point column in a specified EK
* record.
*
* void ekrced_c (
*       SpiceInt           handle,
*       SpiceInt           segno,
*       SpiceInt           recno,
*       ConstSpiceChar   * column,
*       SpiceInt         * nvals,
*       SpiceDouble      * dvals,
*       SpiceBoolean     * isnull )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* handle     I   Handle attached to EK file.
* segno      I   Index of segment containing record.
* recno      I   Record from which data is to be read.
* column     I   Column name.
* nvals      O   Number of values in column entry.
* dvals      O   D.p. values in column entry.
* isnull     O   Flag indicating whether column entry is null.
***********************************************************************/

%rename (ekrced) ekrced_c;
%apply (void RETURN_VOID) {void ekrced_c};
%apply (SpiceInt *SIZE1, SpiceDouble OUT_ARRAY1[ANY])
                {(SpiceInt *nvals, SpiceDouble dvals[MAXVALS])};

extern void ekrced_c(
        SpiceInt       handle,
        SpiceInt       segno,
        SpiceInt       recno,
        ConstSpiceChar *CONST_STRING,
        SpiceInt       *nvals, SpiceDouble dvals[MAXVALS],
        SpiceBoolean   *OUTPUT
);

/***********************************************************************
* -Procedure ekrcei_c ( EK, read column entry element, integer )
*
* -Abstract
*
* Read data from an integer column in a specified EK record.
*
* void ekrcei_c (
*       SpiceInt           handle,
*       SpiceInt           segno,
*       SpiceInt           recno,
*       ConstSpiceChar   * column,
*       SpiceInt         * nvals,
*       SpiceInt         * ivals,
*       SpiceBoolean     * isnull )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* handle     I   Handle attached to EK file.
* segno      I   Index of segment containing record.
* recno      I   Record from which data is to be read.
* column     I   Column name.
* nvals      O   Number of values in column entry.
* ivals      O   Integer values in column entry.
* isnull     O   Flag indicating whether column entry is null.
***********************************************************************/

%rename (ekrcei) ekrcei_c;
%apply (void RETURN_VOID) {void ekrcei_c};
%apply (SpiceInt *SIZE1, SpiceInt OUT_ARRAY1[ANY])
                {(SpiceInt *nvals, SpiceInt ivals[MAXVALS])};

extern void ekrcei_c(
        SpiceInt       handle,
        SpiceInt       segno,
        SpiceInt       recno,
        ConstSpiceChar *CONST_STRING,
        SpiceInt       *nvals, SpiceInt ivals[MAXVALS],
        SpiceBoolean   *OUTPUT
);

/***********************************************************************
* -Procedure ekssum_c ( EK, return segment summary )
*
* -Abstract
*
* Return summary information for a specified segment in a
* specified EK.
*
* void ekssum_c (
*       SpiceInt           handle,
*       SpiceInt           segno,
*       SpiceEKSegSum    * segsum )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* handle     I   Handle of EK.
* segno      I   Number of segment to be summarized.
* segsum     O   EK segment summary.
* nrows      O   The number of rows in the segment.
* ncols      O   The number of columns in the segment.
* tabnam     O   The name of the table to which the segment belongs.
* cnames     O   Column names.
* cclass     O   Column class codes.
* dtype      O   Data type codes: 0 for character; 1 for floating-point; 2 for integer; 3 for time.
* strln      O   String lengths.
* size       O   Column entry sizes; this is the number of array elements in a column entry.
* indexd     O   True if the column is indexed; False otherwise.
* nullok     O   True if the column may contain null values; False otherwise.
***********************************************************************/

%rename (ekssum) my_ekssum_c;
%apply (void RETURN_VOID) {void my_ekssum_c};
%apply (SpiceChar    OUT_STRING[ANY]) {SpiceChar tabnam[NAMELEN]};
%apply (SpiceInt     *OUTPUT)                     {(SpiceInt  *nrows)};
%apply (SpiceInt     *OUTPUT)                     {(SpiceInt  *ncols)};
%apply (SpiceChar    OUT_STRINGS[ANY][ANY], SpiceInt *NSTRINGS) {(SpiceChar cnames[SPICE_EK_MXCLSG][NAMELEN], SpiceInt *n1)};
%apply (SpiceInt     OUT_ARRAY1[ANY], SpiceInt *SIZE1) {(SpiceInt     cclass[SPICE_EK_MXCLSG], SpiceInt *n2)};
%apply (SpiceInt     OUT_ARRAY1[ANY], SpiceInt *SIZE1) {(SpiceInt      dtype[SPICE_EK_MXCLSG], SpiceInt *n3)};
%apply (SpiceInt     OUT_ARRAY1[ANY], SpiceInt *SIZE1) {(SpiceInt      strln[SPICE_EK_MXCLSG], SpiceInt *n4)};
%apply (SpiceInt     OUT_ARRAY1[ANY], SpiceInt *SIZE1) {(SpiceInt       size[SPICE_EK_MXCLSG], SpiceInt *n5)};
%apply (SpiceBoolean OUT_ARRAY1[ANY], SpiceInt *SIZE1) {(SpiceBoolean indexd[SPICE_EK_MXCLSG], SpiceInt *n6)};
%apply (SpiceBoolean OUT_ARRAY1[ANY], SpiceInt *SIZE1) {(SpiceBoolean nullok[SPICE_EK_MXCLSG], SpiceInt *n7)};

%inline %{
    void my_ekssum_c(
        SpiceInt     handle,
        SpiceInt     segno,
        SpiceChar    tabnam[NAMELEN],
        SpiceInt     *nrows,
        SpiceInt     *ncols,
        SpiceChar    cnames[SPICE_EK_MXCLSG][NAMELEN], SpiceInt *n1,
        SpiceInt     cclass[SPICE_EK_MXCLSG], SpiceInt *n2,
        SpiceInt      dtype[SPICE_EK_MXCLSG], SpiceInt *n3,
        SpiceInt      strln[SPICE_EK_MXCLSG], SpiceInt *n4,
        SpiceInt       size[SPICE_EK_MXCLSG], SpiceInt *n5,
        SpiceBoolean indexd[SPICE_EK_MXCLSG], SpiceInt *n6,
        SpiceBoolean nullok[SPICE_EK_MXCLSG], SpiceInt *n7)
    {
        SpiceEKSegSum segsum;

        ekssum_c(handle, segno, &segsum);

        strncpy(tabnam, segsum.tabnam, SPICE_EK_TSTRLN);
        *nrows = segsum.nrows;
        *ncols = segsum.ncols;

        for (int k = 0; k < *ncols; k++) {
            strncpy(&(cnames[k]), &(segsum.cnames[k]), SPICE_EK_CSTRLN);
            cclass[k] = (SpiceInt) segsum.cdescrs[k].cclass;
            dtype[k]  = (SpiceInt) segsum.cdescrs[k].dtype;
            strln[k]  = segsum.cdescrs[k].strlen;
            size[k]   = segsum.cdescrs[k].size;
            indexd[k] = segsum.cdescrs[k].indexd;
            nullok[k] = segsum.cdescrs[k].nullok;
        }

        *n1 = *ncols;
        *n2 = *ncols;
        *n3 = *ncols;
        *n4 = *ncols;
        *n5 = *ncols;
        *n6 = *ncols;
        *n7 = *ncols;
    }
%}

/***********************************************************************
* -Procedure ektnam_c  ( EK, return name of loaded table )
*
* -Abstract
*
* Return the name of a specified, loaded table.
*
* void ektnam_c (
*       SpiceInt     n,
*       SpiceInt     tablen,
*       SpiceChar  * table  )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* n          I   Index of table.
* tablen     I   Maximum table name length.
* table      O   Name of table.
***********************************************************************/

%rename (ektnam) ektnam_c;
%apply (void RETURN_VOID) {void ektnam_c};
%apply (SpiceInt DIM1, SpiceChar OUT_STRING[ANY])
                {(SpiceInt tablen, SpiceChar table[NAMELEN])};

extern void ektnam_c(
        SpiceInt  n,
        SpiceInt  tablen, SpiceChar table[NAMELEN]
);

/***********************************************************************
* -Procedure ekucec_c ( EK, update character column entry )
*
* -Abstract
*
* Update a character column entry in a specified EK record.
*
* void ekucec_c (
*       SpiceInt          handle,
*       SpiceInt          segno,
*       SpiceInt          recno,
*       ConstSpiceChar  * column,
*       SpiceInt          nvals,
*       SpiceInt          cvalen,
*       const void        cvals[][],
*       SpiceBoolean      isnull )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* handle     I   EK file handle.
* segno      I   Index of segment containing record.
* recno      I   Record to which data is to be updated.
* column     I   Column name.
* nvals      I   Number of values in new column entry.
* cvalen     I   Declared length of character values.
* cvals      I   Character values comprising new column entry.
* isnull     I   Flag indicating whether column entry is null.
***********************************************************************/

%rename (ekucec) ekucec_c;
%apply (void RETURN_VOID) {void ekucec_c};
%apply (SpiceInt DIM1, SpiceInt DIM2, ConstSpiceChar *IN_STRINGS)
                {(SpiceInt nvals, SpiceInt cvalen, ConstSpiceChar *cvals)};

extern void ekucec_c(
        SpiceInt       handle,
        SpiceInt       segno,
        SpiceInt       recno,
        ConstSpiceChar *CONST_STRING,
        SpiceInt       nvals, SpiceInt cvalen, ConstSpiceChar *cvals,
        SpiceBoolean   isnull
);

/***********************************************************************
* -Procedure ekuced_c ( EK, update d.p. column entry )
*
* -Abstract
*
* Update a floating-point column entry in a specified EK record.
*
* void ekuced_c (
*       SpiceInt             handle,
*       SpiceInt             segno,
*       SpiceInt             recno,
*       ConstSpiceChar     * column,
*       SpiceInt             nvals,
*       ConstSpiceDouble   * dvals,
*       SpiceBoolean         isnull )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* handle     I   Handle attached to EK file.
* segno      I   Index of segment containing record.
* recno      I   Record in which entry is to be updated.
* column     I   Column name.
* nvals      I   Number of values in new column entry.
* dvals      I   Double precision values comprising new column entry.
* isnull     I   Flag indicating whether column entry is null.
***********************************************************************/

%rename (ekuced) ekuced_c;
%apply (void RETURN_VOID) {void ekuced_c};
%apply (SpiceInt DIM1, ConstSpiceDouble IN_ARRAY1[])
                {(SpiceInt nvals, ConstSpiceDouble dvals[])};

extern void ekuced_c(
        SpiceInt       handle,
        SpiceInt       segno,
        SpiceInt       recno,
        ConstSpiceChar *CONST_STRING,
        SpiceInt       nvals, ConstSpiceDouble dvals[],
        SpiceBoolean   isnull
);

/***********************************************************************
* -Procedure ekucei_c ( EK, update integer column entry )
*
* -Abstract
*
* Update an integer column entry in a specified EK record.
*
* void ekucei_c (
*       SpiceInt          handle,
*       SpiceInt          segno,
*       SpiceInt          recno,
*       ConstSpiceChar  * column,
*       SpiceInt          nvals,
*       ConstSpiceInt   * ivals,
*       SpiceBoolean      isnull )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* handle     I   Handle attached to EK file.
* segno      I   Index of segment containing record.
* recno      I   Record in which entry is to be updated.
* column     I   Column name.
* nvals      I   Number of values in new column entry.
* ivals      I   Integer values comprising new column entry.
* isnull     I   Flag indicating whether column entry is null.
***********************************************************************/

%rename (ekucei) ekucei_c;
%apply (void RETURN_VOID) {void ekucei_c};
%apply (SpiceInt DIM1, ConstSpiceDouble IN_ARRAY1[])
                {(SpiceInt nvals, ConstSpiceInt ivals[])};

extern void ekucei_c(
        SpiceInt       handle,
        SpiceInt       segno,
        SpiceInt       recno,
        ConstSpiceChar *CONST_STRING,
        SpiceInt       nvals, ConstSpiceInt ivals[],
        SpiceBoolean   isnull
);

/***********************************************************************
* -Procedure ekuef_c  ( EK, unload event file )
*
* -Abstract
*
* Unload an EK file, making its contents inaccessible to the
* EK reader routines, and clearing space in order to allow other
* EK files to be loaded.
*
* void ekuef_c (
*       SpiceInt handle )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* handle     I   Handle of EK file.
***********************************************************************/

%rename (ekuef) ekuef_c;
%apply (void RETURN_VOID) {void ekuef_c};

extern void ekuef_c(
        SpiceInt handle
);

/***********************************************************************
* -Procedure evsgp4_c ( Evaluate "two-line" element data )
*
* -Abstract
*
* Evaluate NORAD two-line element data for earth orbiting
* spacecraft. This evaluator uses algorithms as described
* in Vallado 2006 [4].
*
* void evsgp4_c (
*       SpiceDouble         et,
*       ConstSpiceDouble    geophs[8],
*       ConstSpiceDouble    elems[10],
*       SpiceDouble         state[6] )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* et         I   Epoch in seconds past ephemeris epoch J2000.
* geophs     I   Geophysical constants
* elems      I   Two-line element data
* state      O   Evaluated state
***********************************************************************/

%rename (evsgp4) evsgp4_c;
%apply (void RETURN_VOID) {void evsgp4_c};
%apply (ConstSpiceDouble IN_ARRAY1[ANY]) {ConstSpiceDouble geophs[8]};
%apply (ConstSpiceDouble IN_ARRAY1[ANY]) {ConstSpiceDouble elems[10]};
%apply (SpiceDouble OUT_ARRAY1[ANY]) {SpiceDouble state[6]};

extern void evsgp4_c(
        SpiceDouble      et,
        ConstSpiceDouble geophs[8],
        ConstSpiceDouble elems[10],
        SpiceDouble      state[6]
);

//Vector version
VECTORIZE_d_dX_dY__dN(evsgp4, evsgp4_c, 6)

/***********************************************************************
* -Procedure esrchc_c ( Equivalence search, character )
*
* -Abstract
*
* Search for a given value within a character string array.
* Return the index of the first equivalent array entry, or -1
* if no equivalent element is found.
*
* SpiceInt esrchc_c (
*       ConstSpiceChar  * value,
*       SpiceInt          ndim,
*       SpiceInt          arrlen,
*       const void        array[][]    )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* value      I   Key value to be found in array.
* ndim       I   Dimension of array.
* arrlen     I   String length.
* array      I   Character string array to search.
* index      R   Index of entry in array.
***********************************************************************/

%rename (esrchc) esrchc_c;
%apply (SpiceInt RETURN_INT) {SpiceInt esrchc_c};
%apply (ConstSpiceChar *CONST_STRING) {ConstSpiceChar *value};
%apply (SpiceInt DIM1, SpiceInt DIM2, ConstSpiceChar *IN_STRINGS)
                {(SpiceInt ndim, SpiceInt arrlen, ConstSpiceChar *array)};

extern SpiceInt esrchc_c(
        ConstSpiceChar *CONST_STRING,
        SpiceInt       ndim, SpiceInt arrlen, ConstSpiceChar *array
);

/***********************************************************************
* -Procedure getelm_c ( Get the components from two-line elements )
*
* -Abstract
*
* Parse the "lines" of a two-line element set, returning the
* elements in units suitable for use in SPICE software.
*
* void getelm_c (
*       SpiceInt         frstyr,
*       SpiceInt         lineln,
*       const void       lines[2][],
*       SpiceDouble    * epoch,
*       SpiceDouble    * elems   )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* frstyr     I   Year of earliest representable two-line elements.
* lineln     I   Length of strings in lines array.
* lines      I   A pair of "lines" containing two-line elements.
* epoch      O   The epoch of the elements in seconds past J2000.
* elems      O   The elements converted to SPICE units.
***********************************************************************/

%rename (getelm) my_getelm_c;
%apply (void RETURN_VOID) {void my_getelm_c};
%apply (SpiceInt DIM1, SpiceInt DIM2, ConstSpiceChar *IN_STRINGS)
                {(SpiceInt two, SpiceInt lineln, ConstSpiceChar *lines)};
%apply (SpiceDouble OUT_ARRAY1[ANY]) {SpiceDouble elems[10]};
%apply (SpiceDouble *OUTPUT) {SpiceDouble *epoch};

%inline %{
    void my_getelm_c(
        SpiceInt    frstyr,
        SpiceInt    two, SpiceInt lineln, ConstSpiceChar *lines,
        SpiceDouble *epoch,
        SpiceDouble elems[10])
    {
        if (!my_assert_eq(two, 2, "getelm",
            "Array dimension error in getelm: "
            "lines rows = #; # is required")) return;

        getelm_c(frstyr, lineln, lines, epoch, elems);
    }
%}

/***********************************************************************
* -Procedure getfat_c ( Get file architecture and type )
*
* -Abstract
*
* Determine the file architecture and file type of most SPICE kernel
* files.
*
* void getfat_c (
*       ConstSpiceChar   * file,
*       SpiceInt           arclen,
*       SpiceInt           kertln,
*       SpiceChar        * arch,
*       SpiceChar        * kertyp   )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* file       I   The name of a file to be examined.
* arclen     I   Maximum length of output architecture string.
* kertln     I   Maximum length of output `kertyp' string.
* arch       O   The architecture of the kernel file.
* kertyp     O   The type of the kernel file.
***********************************************************************/

%rename (getfat) my_getfat_c;
%apply (void RETURN_VOID) {void my_getfat_c};
%apply (ConstSpiceChar *CONST_STRING) {ConstSpiceChar *file};
%apply (SpiceChar OUT_STRING[ANY]) {SpiceChar arch[NAMELEN]};
%apply (SpiceChar OUT_STRING[ANY]) {SpiceChar kertyp[NAMELEN]};

%inline %{
    void my_getfat_c(
        ConstSpiceChar *file,
        SpiceChar      arch[NAMELEN],
        SpiceChar      kertyp[NAMELEN])
    {
        getfat_c(file, NAMELEN-1, NAMELEN-1, arch, kertyp);
    }
%}

/***********************************************************************
* -Procedure getfvn_c (Get instrument FOV parameters, by instrument name)
*
* -Abstract
*
* Return the field-of-view (FOV) parameters for a specified
* instrument. The instrument is specified by name.
*
* void getfvn_c (
*       ConstSpiceChar    * inst,
*       SpiceInt            room,
*       SpiceInt            shalen,
*       SpiceInt            fralen,
*       SpiceChar         * shape,
*       SpiceChar         * frame,
*       SpiceDouble         bsight[3],
*       SpiceInt          * n,
*       SpiceDouble         bounds[][3] )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* inst       I   Name of an instrument.
* room       I   Maximum number of vectors that can be returned.
* shalen     I   Maximum length of output string `shape'.
* fralen     I   Maximum length of output string `frame'.
* shape      O   Instrument FOV shape.
* frame      O   Name of the frame in which FOV vectors are defined.
* bsight     O   Boresight vector.
* n          O   Number of boundary vectors returned.
* bounds     O   FOV boundary vectors.
***********************************************************************/

%rename (getfvn) my_getfvn_c;
%apply (void RETURN_VOID) {void my_getfvn_c};
%apply (ConstSpiceChar *CONST_STRING) {ConstSpiceChar *inst};
%apply (SpiceChar OUT_STRING[ANY]) {SpiceChar shape[NAMELEN]};
%apply (SpiceChar OUT_STRING[ANY]) {SpiceChar frame[NAMELEN]};
%apply (SpiceDouble OUT_ARRAY1[ANY]) {SpiceDouble bsight[3]};
%apply (SpiceDouble OUT_ARRAY2[ANY][ANY], SpiceInt *SIZE1)
                {(SpiceDouble bounds[FOVSHAPE][3], SpiceInt *n)};

%inline %{
    void my_getfvn_c(
        ConstSpiceChar *inst,
        SpiceChar      shape[NAMELEN],
        SpiceChar      frame[NAMELEN],
        SpiceDouble    bsight[3],
        SpiceDouble    bounds[FOVSHAPE][3], SpiceInt *n)
    {
        getfvn_c(inst, FOVSHAPE, NAMELEN-1, NAMELEN-1, shape, frame,
                 bsight, n, bounds);
    }
%}

/***********************************************************************
* -Procedure gfdist_c ( GF, distance search )
*
* -Abstract
*
* Return the time window over which a specified constraint on
* observer-target distance is met.
*
* void gfdist_c (
*       ConstSpiceChar     * target,
*       ConstSpiceChar     * abcorr,
*       ConstSpiceChar     * obsrvr,
*       ConstSpiceChar     * relate,
*       SpiceDouble          refval,
*       SpiceDouble          adjust,
*       SpiceDouble          step,
*       SpiceInt             nintvls,
*       SpiceCell          * cnfine,
*       SpiceCell          * result     )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* SPICE_GF_CNVTOL
*            P   Convergence tolerance.
* SPICE_GF_NWDIST
*            P   Number of workspace windows for distance search.
* target     I   Name of the target body.
* abcorr     I   Aberration correction flag.
* obsrvr     I   Name of the observing body.
* relate     I   Relational operator.
* refval     I   Reference value.
* adjust     I   Adjustment value for absolute extrema searches.
* step       I   Step size used for locating extrema and roots.
* nintvls    I   Workspace window interval count.
* cnfine     I   SPICE window to which the search is confined.
* result     O   SPICE window containing results.
***********************************************************************/

// cnfine changed to I from I-O per instructions of MRS.

%rename (gfdist) gfdist_c;
%apply (void RETURN_VOID) {void gfdist_c};
%apply (ConstSpiceChar *CONST_STRING) {ConstSpiceChar *target};
%apply (ConstSpiceChar *CONST_STRING) {ConstSpiceChar *abcorr};
%apply (ConstSpiceChar *CONST_STRING) {ConstSpiceChar *obsrvr};
%apply (ConstSpiceChar *CONST_STRING) {ConstSpiceChar *relate};
%apply (SpiceCellDouble* INPUT)       {SpiceCell *cnfine};
%apply (SpiceCellDouble* OUTPUT)      {SpiceCell *result};

extern void gfdist_c(
        ConstSpiceChar *target,
        ConstSpiceChar *abcorr,
        ConstSpiceChar *obsrvr,
        ConstSpiceChar *relate,
        SpiceDouble    refval,
        SpiceDouble    adjust,
        SpiceDouble    step,
        SpiceInt       nintvls,
        SpiceCell      *cnfine,
        SpiceCell      *result
);

/***********************************************************************
* -Procedure gfevnt_c (GF, geometric event finder )
*
* -Abstract
*
* Determine time intervals when a specified geometric quantity
* satisfies a specified mathematical condition.
*
*   void gfevnt_c (
*       void               (*udstep)(SpiceDouble et, SpiceDouble * step),
*       void               (*udrefn)(t1, t2, s1, s2, *t),
*       ConstSpiceChar     * gquant,
*       SpiceInt             qnpars,
*       SpiceInt             lenvals,
*       const void           qpnams[][],
*       const void           qcpars[][],
*       ConstSpiceDouble   * qdpars,
*       ConstSpiceInt      * qipars,
*       ConstSpiceBoolean  * qlpars,
*       ConstSpiceChar     * op,
*       SpiceDouble          refval,
*       SpiceDouble          tol,
*       SpiceDouble          adjust,
*       SpiceBoolean         rpt,
*       void               (*udrepi)(...),
*       void               (*udrepu)(...),
*       void               (*udrepf)(void),
*       SpiceInt             nintvls,
*       SpiceBoolean         bail,
*       SpiceBoolean       (*udbail) ( void ),
*       SpiceCell          * cnfine,
*       SpiceCell          * result     )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* SPICE_GFEVNT_MAXPAR
*            P   Maximum number of parameters required to define
*                any quantity.
* SPICE_GF_CNVTOL
*            P   Default convergence tolerance.
* udstep     I   Name of the routine that computes and returns a
*                time step.
* udrefn     I   Name of the routine that computes a refined time.
* gquant     I   Type of geometric quantity.
* qnpars     I   Number of quantity definition parameters.
* lenvals    I   Length of strings in 'qpnams' and 'qcpars'.
* qpnams     I   Names of quantity definition parameters.
* qcpars     I   Array of character quantity definition parameters.
* qdpars     I   Array of floating-point quantity definition
*                parameters.
* qipars     I   Array of integer quantity definition parameters.
* qlpars     I   Array of logical quantity definition parameters.
* op         I   Operator that either looks for an extreme value
*                (max, min, local, absolute) or compares the
*                geometric quantity value and a number.
* refval     I   Reference value.
* tol        I   Convergence tolerance in seconds
* adjust     I   Absolute extremum adjustment value.
* rpt        I   Progress reporter on (True) or off (False).
* udrepi     I   Function that initializes progress reporting.
* udrepu     I   Function that updates the progress report.
* udrepf     I   Function that finalizes progress reporting.
* nintvls    I   Workspace window interval count
* bail       I   Logical indicating program interrupt monitoring.
* udbail     I   Name of a routine that signals a program interrupt.
* cnfine     I   SPICE window to which the search is restricted.
* result     O   SPICE window containing results.
* windows    O   Array giving start/stop time pairs for the intervals found.
* step       I   Time step for searching.
***********************************************************************/

// cnfine changed to I from I-O per instructions of MRS.

%rename (gfevnt) my_gfevnt_c;
%apply (void RETURN_VOID) {void my_gfevnt_c};
%apply (ConstSpiceChar *CONST_STRING) {ConstSpiceChar *gquant};
%apply (SpiceInt DIM1, SpiceInt DIM2, ConstSpiceChar *IN_STRINGS)
                {(SpiceInt qnpars, SpiceInt ignore, ConstSpiceChar *qpnams)};
%apply (SpiceInt DIM1, SpiceInt DIM2, ConstSpiceChar *IN_STRINGS)
                {(SpiceInt ignore2, SpiceInt ignore3, ConstSpiceChar *qcpars)};
%apply (ConstSpiceDouble  *IN_ARRAY1) {ConstSpiceDouble  *qdpars};
%apply (ConstSpiceInt     *IN_ARRAY1) {ConstSpiceInt     *qipars};
%apply (ConstSpiceBoolean *IN_ARRAY1) {ConstSpiceBoolean *qlpars};
%apply (ConstSpiceChar *CONST_STRING) {ConstSpiceChar    *op};
%apply (SpiceCellDouble* INPUT)       {SpiceCell *cnfine};
%apply (SpiceCellDouble* OUTPUT)      {SpiceCell *result};

%inline %{
    void my_gfevnt_c(
        SpiceDouble       step,
        ConstSpiceChar    *gquant,
        SpiceInt          qnpars, SpiceInt ignore, ConstSpiceChar *qpnams,
        SpiceInt          ignore2, SpiceInt ignore3, ConstSpiceChar *qcpars,
        ConstSpiceDouble  *qdpars,
        ConstSpiceInt     *qipars,
        ConstSpiceBoolean *qlpars,
        ConstSpiceChar    *op,
        SpiceDouble       refval,
        SpiceDouble       tol,
        SpiceDouble       adjust,
        SpiceBoolean      rpt,
        SpiceInt          nintvls,
        SpiceCell         *cnfine,
        SpiceCell         *result)
    {
        gfsstp_c(step);
        gfevnt_c(&gfstep_c, &gfrefn_c, gquant, qnpars,
                 NAMELEN, qpnams, qcpars, qdpars, qipars, qlpars, op,
                 refval, tol, adjust, rpt, &gfrepi_c, &gfrepu_c, &gfrepf_c,
                 nintvls, SPICEFALSE, NULL, &cnfine, &result);
    }
%}

/***********************************************************************
* -Procedure gffove_c ( GF, is target in FOV? )
*
* -Abstract
*
* Determine time intervals when a specified target body or ray
* intersects the space bounded by the field-of-view (FOV) of a
* specified instrument. Report progress and handle interrupts if so
* commanded.
*
* void gffove_c (
*       ConstSpiceChar     * inst,
*       ConstSpiceChar     * tshape,
*       ConstSpiceDouble     raydir[3],
*       ConstSpiceChar     * target,
*       ConstSpiceChar     * tframe,
*       ConstSpiceChar     * abcorr,
*       ConstSpiceChar     * obsrvr,
*       SpiceDouble          tol,
*       void               (*udstep)(SpiceDouble et, SpiceDouble * step),
*       void               (*udrefn)(t1, t2, s1, s2, *t),
*       SpiceBoolean         rpt,
*       void               (*udrepi)(...),
*       void               (*udrepu)(...),
*       void               (*udrepf)(void),
*       SpiceBoolean         bail,
*       SpiceBoolean       (*udbail) ( void ),
*       SpiceCell          * cnfine,
*       SpiceCell          * result     )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* SPICE_GF_MARGIN
*            P   Minimum complement of FOV cone angle.
* SPICE_GF_CNVTOL
*            P   Convergence tolerance.
* SPICE_GF_MAXVRT
*            P   Maximum number of FOV boundary vertices.
* inst       I   Name of the instrument.
* tshape     I   Type of shape model used for target body.
* raydir     I   Ray's direction vector.
* target     I   Name of the target body.
* tframe     I   Body-fixed, body-centered frame for target body.
* abcorr     I   Aberration correction flag.
* obsrvr     I   Name of the observing body.
* tol        I   Convergence tolerance in seconds.
* udstep     I   Name of routine that returns a time step.
* udrefn     I   Name of the routine that computes a refined time.
* rpt        I   Progress report flag.
* udrepi     I   Function that initializes progress reporting.
* udrepu     I   Function that updates the progress report.
* udrepf     I   Function that finalizes progress reporting.
* bail       I   Logical indicating program interrupt monitoring.
* udbail     I   Name of a routine that signals a program interrupt.
* cnfine     I  SPICE window to which the search is restricted.
* result     O   SPICE window containing results.
* windows    O   Array giving start/stop time pairs for the intervals found.
* step       I   Time step for searching.
***********************************************************************/

// cnfine changed to I from I-O per instructions of MRS.

%rename (gffove) my_gffove_c;
%apply (void RETURN_VOID) {void my_gffove_c};
%apply (ConstSpiceDouble IN_ARRAY1[ANY]) {ConstSpiceDouble raydir[3]};

%apply (SpiceDouble OUT_ARRAY2[ANY][ANY], SpiceInt *SIZE1)
                {(SpiceDouble windows[WINDOWS][2], SpiceInt *intervals)};
%apply (SpiceCellDouble* INPUT)  {SpiceCell *cnfine};
%apply (SpiceCellDouble* OUTPUT) {SpiceCell *result};

%inline %{
    void my_gffove_c(
        ConstSpiceChar   *inst,
        ConstSpiceChar   *tshape,
        ConstSpiceDouble raydir[3],
        ConstSpiceChar   *target,
        ConstSpiceChar   *tframe,
        ConstSpiceChar   *abcorr,
        ConstSpiceChar   *obsrvr,
        SpiceDouble      tol,
        SpiceDouble      step,
        SpiceBoolean     rpt,
        SpiceCell        *cnfine,
        SpiceCell        *result)
    {
        gfsstp_c(step);
        gffove_c(inst, tshape, raydir, target, tframe, abcorr, obsrvr,
                 tol, &gfstep_c, &gfrefn_c, rpt, &gfrepi_c, &gfrepu_c, &gfrepf_c,
                 SPICEFALSE, NULL, &cnfine, &result);
    }
%}

/***********************************************************************
* -Procedure gfilum_c ( GF, illumination angle search )
*
* -Abstract
*
* Return the time window over which a specified constraint on
* the observed phase, solar incidence, or emission angle at
* a specified target body surface point is met.
*
* void gfilum_c (
*       ConstSpiceChar     * method,
*       ConstSpiceChar     * angtyp,
*       ConstSpiceChar     * target,
*       ConstSpiceChar     * illmn,
*       ConstSpiceChar     * fixref,
*       ConstSpiceChar     * abcorr,
*       ConstSpiceChar     * obsrvr,
*       ConstSpiceDouble     spoint[3],
*       ConstSpiceChar     * relate,
*       SpiceDouble          refval,
*       SpiceDouble          adjust,
*       SpiceDouble          step,
*       SpiceInt             nintvls,
*       SpiceCell          * cnfine,
*       SpiceCell          * result     )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* SPICE_GF_CNVTOL
*            P   Convergence tolerance.
* SPICE_GF_NWILUM
*            P   Number of workspace windows for angle search.
* method     I   Computation method.
* angtyp     I   Type of illumination angle.
* target     I   Name of the target body.
* illmn      I   Name of the illumination source.
* fixref     I   Body-fixed, body-centered target body frame.
* abcorr     I   Aberration correction flag.
* obsrvr     I   Name of the observing body.
* spoint     I   Body-fixed coordinates of a target surface point.
* relate     I   Relational operator.
* refval     I   Reference value.
* adjust     I   Adjustment value for absolute extrema searches.
* step       I   Step size used for locating extrema and roots.
* nintvls    I   Workspace window interval count.
* cnfine     I   SPICE window to which the search is confined.
* result     O   SPICE window containing results.
***********************************************************************/

// cnfine changed to I from I-O per instructions of MRS.

%rename (gfilum) gfilum_c;
%apply (void RETURN_VOID) {void gfilum_c};
%apply (ConstSpiceChar *CONST_STRING) {ConstSpiceChar *method};
%apply (ConstSpiceChar *CONST_STRING) {ConstSpiceChar *angtyp};
%apply (ConstSpiceChar *CONST_STRING) {ConstSpiceChar *target};
%apply (ConstSpiceChar *CONST_STRING) {ConstSpiceChar *illmn};
%apply (ConstSpiceChar *CONST_STRING) {ConstSpiceChar *fixref};
%apply (ConstSpiceChar *CONST_STRING) {ConstSpiceChar *abcorr};
%apply (ConstSpiceChar *CONST_STRING) {ConstSpiceChar *obsrvr};
%apply (ConstSpiceDouble IN_ARRAY1[ANY]) {ConstSpiceDouble spoint[3]};
%apply (ConstSpiceChar *CONST_STRING) {ConstSpiceChar *relate};
%apply (SpiceCellDouble* INPUT)       {SpiceCell *cnfine};
%apply (SpiceCellDouble* OUTPUT)      {SpiceCell *result};

extern void gfilum_c(
        ConstSpiceChar   *method,
        ConstSpiceChar   *angtyp,
        ConstSpiceChar   *target,
        ConstSpiceChar   *illmn,
        ConstSpiceChar   *fixref,
        ConstSpiceChar   *abcorr,
        ConstSpiceChar   *obsrvr,
        ConstSpiceDouble spoint[3],
        ConstSpiceChar   *relate,
        SpiceDouble      refval,
        SpiceDouble      adjust,
        SpiceDouble      step,
        SpiceInt         nintvls,
        SpiceCell        *cnfine,
        SpiceCell        *result
);

/***********************************************************************
* -Procedure gfocce_c ( GF, occultation event )
*
* -Abstract
*
* Determine time intervals when an observer sees one target
* occulted by another. Report progress and handle interrupts
* if so commanded. The surfaces of the target bodies may be represented
* by triaxial ellipsoids or by topographic data provided by DSK files.
*
* void gfocce_c (
*       ConstSpiceChar     * occtyp,
*       ConstSpiceChar     * front,
*       ConstSpiceChar     * fshape,
*       ConstSpiceChar     * fframe,
*       ConstSpiceChar     * back,
*       ConstSpiceChar     * bshape,
*       ConstSpiceChar     * bframe,
*       ConstSpiceChar     * abcorr,
*       ConstSpiceChar     * obsrvr,
*       SpiceDouble          tol,
*       void               (*udstep)(SpiceDouble et, SpiceDouble * step),
*       void               (*udrefn)(t1, t2, s1, s2, *t),
*       SpiceBoolean         rpt,
*       void               (*udrepi)(...),
*       void               (*udrepu)(...),
*       void               (*udrepf)(void),
*       SpiceBoolean         bail,
*       SpiceBoolean       (*udbail) ( void ),
*       SpiceCell          * cnfine,
*       SpiceCell          * result     )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* occtyp     I   Type of occultation.
* front      I   Name of body occulting the other.
* fshape     I   Type of shape model used for front body.
* fframe     I   Body-fixed, body-centered frame for front body.
* back       I   Name of body occulted by the other.
* bshape     I   Type of shape model used for back body.
* bframe     I   Body-fixed, body-centered frame for back body.
* abcorr     I   Aberration correction flag.
* obsrvr     I   Name of the observing body.
* tol        I   Convergence tolerance in seconds.
* udstep     I   Name of the routine that returns a time step.
* udrefn     I   Name of the routine that computes a refined time.
* rpt        I   Progress report flag.
* udrepi     I   Function that initializes progress reporting.
* udrepu     I   Function that updates the progress report.
* udrepf     I   Function that finalizes progress reporting.
* bail       I   Logical indicating program interrupt monitoring.
* udbail     I   Name of a routine that signals a program interrupt.
* cnfine     I  SPICE window to which the search is restricted.
* result     O   SPICE window containing results.
* windows    O   Array giving start/stop time pairs for the intervals found.
* step       I   Time step for searching.
***********************************************************************/

// cnfine changed to I from I-O per instructions of MRS.

%rename (gfocce) my_gfocce_c;
%apply (void RETURN_VOID) {void my_gfocce_c};
%apply (ConstSpiceChar *CONST_STRING) {ConstSpiceChar *occtyp};
%apply (ConstSpiceChar *CONST_STRING) {ConstSpiceChar *front};
%apply (ConstSpiceChar *CONST_STRING) {ConstSpiceChar *fshape};
%apply (ConstSpiceChar *CONST_STRING) {ConstSpiceChar *fframe};
%apply (ConstSpiceChar *CONST_STRING) {ConstSpiceChar *back};
%apply (ConstSpiceChar *CONST_STRING) {ConstSpiceChar *bshape};
%apply (ConstSpiceChar *CONST_STRING) {ConstSpiceChar *bframe};
%apply (ConstSpiceChar *CONST_STRING) {ConstSpiceChar *abcorr};
%apply (ConstSpiceChar *CONST_STRING) {ConstSpiceChar *obsrvr};
%apply (SpiceCellDouble* INPUT)       {SpiceCell *cnfine};
%apply (SpiceCellDouble* OUTPUT)      {SpiceCell *result};

%inline %{
    void my_gfocce_c(
        ConstSpiceChar *occtyp,
        ConstSpiceChar *front,
        ConstSpiceChar *fshape,
        ConstSpiceChar *fframe,
        ConstSpiceChar *back,
        ConstSpiceChar *bshape,
        ConstSpiceChar *bframe,
        ConstSpiceChar *abcorr,
        ConstSpiceChar *obsrvr,
        SpiceDouble    tol,
        SpiceDouble    step,
        SpiceBoolean   rpt,
        SpiceCell      *cnfine,
        SpiceCell      *result)
    {
        gfsstp_c(step);
        gfocce_c(occtyp, front, fshape, fframe, back, bshape, bframe, abcorr, obsrvr,
                 tol, &gfstep_c, &gfrefn_c, rpt, &gfrepi_c, &gfrepu_c, &gfrepf_c,
                 SPICEFALSE, NULL, &cnfine, &result);
    }
%}

/***********************************************************************
* -Procedure gfoclt_c ( GF, find occultation )
*
* -Abstract
*
* Determine time intervals when an observer sees one target occulted
* by, or in transit across, another.
* The surfaces of the target bodies may be represented by triaxial
* ellipsoids or by topographic data provided by DSK files.
*
* void gfoclt_c (
*       ConstSpiceChar   * occtyp,
*       ConstSpiceChar   * front,
*       ConstSpiceChar   * fshape,
*       ConstSpiceChar   * fframe,
*       ConstSpiceChar   * back,
*       ConstSpiceChar   * bshape,
*       ConstSpiceChar   * bframe,
*       ConstSpiceChar   * abcorr,
*       ConstSpiceChar   * obsrvr,
*       SpiceDouble        step,
*       SpiceCell        * cnfine,
*       SpiceCell        * result )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* SPICE_GF_CNVTOL
*            P   Convergence tolerance.
* occtyp     I   Type of occultation.
* front      I   Name of body occulting the other.
* fshape     I   Type of shape model used for front body.
* fframe     I   Body-fixed, body-centered frame for front body.
* back       I   Name of body occulted by the other.
* bshape     I   Type of shape model used for back body.
* bframe     I   Body-fixed, body-centered frame for back body.
* abcorr     I   Aberration correction flag.
* obsrvr     I   Name of the observing body.
* step       I   Step size in seconds for finding occultation
*                events.
* cnfine     I   SPICE window to which the search is restricted.
* result     O   SPICE window containing results.
***********************************************************************/

// cnfine changed to I from I-O per instructions of MRS.

%rename (gfoclt) gfoclt_c;
%apply (void RETURN_VOID) {void gfoclt_c};
%apply (ConstSpiceChar *CONST_STRING) {ConstSpiceChar *occtyp};
%apply (ConstSpiceChar *CONST_STRING) {ConstSpiceChar *front};
%apply (ConstSpiceChar *CONST_STRING) {ConstSpiceChar *fshape};
%apply (ConstSpiceChar *CONST_STRING) {ConstSpiceChar *fframe};
%apply (ConstSpiceChar *CONST_STRING) {ConstSpiceChar *back};
%apply (ConstSpiceChar *CONST_STRING) {ConstSpiceChar *bshape};
%apply (ConstSpiceChar *CONST_STRING) {ConstSpiceChar *bframe};
%apply (ConstSpiceChar *CONST_STRING) {ConstSpiceChar *abcorr};
%apply (ConstSpiceChar *CONST_STRING) {ConstSpiceChar *obsrvr};
%apply (SpiceCellDouble* INPUT)       {SpiceCell *cnfine};
%apply (SpiceCellDouble* OUTPUT)      {SpiceCell *result};


extern void gfoclt_c(
        ConstSpiceChar *occtyp,
        ConstSpiceChar *front,
        ConstSpiceChar *fshape,
        ConstSpiceChar *fframe,
        ConstSpiceChar *back,
        ConstSpiceChar *bshape,
        ConstSpiceChar *bframe,
        ConstSpiceChar *abcorr,
        ConstSpiceChar *obsrvr,
        SpiceDouble    step,
        SpiceCell      *cnfine,
        SpiceCell      *result
);

/***********************************************************************
* -Procedure gfpa_c ( GF, phase angle search )
*
* -Abstract
*
* Determine time intervals for which a specified constraint
* on the phase angle between an illumination source, a target,
* and observer body centers is met.
*
* void gfpa_c (
*       ConstSpiceChar     * target,
*       ConstSpiceChar     * illmn,
*       ConstSpiceChar     * abcorr,
*       ConstSpiceChar     * obsrvr,
*       ConstSpiceChar     * relate,
*       SpiceDouble          refval,
*       SpiceDouble          adjust,
*       SpiceDouble          step,
*       SpiceInt             nintvls,
*       SpiceCell          * cnfine,
*       SpiceCell          * result     )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* SPICE_GF_CNVTOL
*            P   Default convergence tolerance.
* target     I   Name of the target body.
* illmn      I   Name of the illuminating body.
* abcorr     I   Aberration correction flag.
* obsrvr     I   Name of the observing body.
* relate     I   Relational operator.
* refval     I   Reference value.
* adjust     I   Adjustment value for absolute extrema searches.
* step       I   Step size used for locating extrema and roots.
* nintvls    I   Workspace window interval count.
* cnfine     I  SPICE window to which the search is confined.
* result     O   SPICE window containing results.
***********************************************************************/

// cnfine changed to I from I-O per instructions of MRS.

%rename (gfpa) gfpa_c;
%apply (void RETURN_VOID) {void gfpa_c};
%apply (ConstSpiceChar *CONST_STRING) {ConstSpiceChar *target};
%apply (ConstSpiceChar *CONST_STRING) {ConstSpiceChar *illmn};
%apply (ConstSpiceChar *CONST_STRING) {ConstSpiceChar *abcorr};
%apply (ConstSpiceChar *CONST_STRING) {ConstSpiceChar *obsrvr};
%apply (ConstSpiceChar *CONST_STRING) {ConstSpiceChar *relate};
%apply (SpiceCellDouble* INPUT)       {SpiceCell *cnfine};
%apply (SpiceCellDouble* OUTPUT)      {SpiceCell *result};


extern void gfpa_c(
        ConstSpiceChar *target,
        ConstSpiceChar *illmn,
        ConstSpiceChar *abcorr,
        ConstSpiceChar *obsrvr,
        ConstSpiceChar *relate,
        SpiceDouble    refval,
        SpiceDouble    adjust,
        SpiceDouble    step,
        SpiceInt       nintvls,
        SpiceCell      *cnfine,
        SpiceCell      *result
);

/***********************************************************************
* -Procedure gfposc_c (GF, observer-target vector coordinate search)
*
* -Abstract
*
* Determine time intervals for which a coordinate of an
* observer-target position vector satisfies a numerical constraint.
*
* void gfposc_c (
*       ConstSpiceChar     * target,
*       ConstSpiceChar     * frame,
*       ConstSpiceChar     * abcorr,
*       ConstSpiceChar     * obsrvr,
*       ConstSpiceChar     * crdsys,
*       ConstSpiceChar     * coord,
*       ConstSpiceChar     * relate,
*       SpiceDouble          refval,
*       SpiceDouble          adjust,
*       SpiceDouble          step,
*       SpiceInt             nintvls,
*       SpiceCell          * cnfine,
*       SpiceCell          * result  )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* SPICE_GF_CNVTOL
*            P   Convergence tolerance.
* target     I   Name of the target body.
* frame      I   Name of the reference frame for coordinate
*                calculations.
* abcorr     I   Aberration correction flag.
* obsrvr     I   Name of the observing body.
* crdsys     I   Name of the coordinate system containing `coord'.
* coord      I   Name of the coordinate of interest.
* relate     I   Relational operator.
* refval     I   Reference value.
* adjust     I   Adjustment value for absolute extrema searches.
* step       I   Step size used for locating extrema and roots.
* nintvls    I   Workspace window interval count.
* cnfine     I   SPICE window to which the search is confined.
* result     O   SPICE window containing results.
* windows    O   Array giving start/stop time pairs for the intervals found.
***********************************************************************/

// cnfine changed to I from I-O per instructions of MRS.

%rename (gfposc) gfposc_c;
%apply (void RETURN_VOID) {void gfposc_c};
%apply (ConstSpiceChar *CONST_STRING) {ConstSpiceChar *target};
%apply (ConstSpiceChar *CONST_STRING) {ConstSpiceChar *frame};
%apply (ConstSpiceChar *CONST_STRING) {ConstSpiceChar *abcorr};
%apply (ConstSpiceChar *CONST_STRING) {ConstSpiceChar *obsrvr};
%apply (ConstSpiceChar *CONST_STRING) {ConstSpiceChar *crdsys};
%apply (ConstSpiceChar *CONST_STRING) {ConstSpiceChar *coord};
%apply (ConstSpiceChar *CONST_STRING) {ConstSpiceChar *relate};
%apply (SpiceCellDouble* INPUT)       {SpiceCell *cnfine};
%apply (SpiceCellDouble* OUTPUT)      {SpiceCell *result};

extern void gfposc_c(
        ConstSpiceChar *target,
        ConstSpiceChar *frame,
        ConstSpiceChar *abcorr,
        ConstSpiceChar *obsrvr,
        ConstSpiceChar *crdsys,
        ConstSpiceChar *coord,
        ConstSpiceChar *relate,
        SpiceDouble    refval,
        SpiceDouble    adjust,
        SpiceDouble    step,
        SpiceInt       nintvls,
        SpiceCell      *cnfine,
        SpiceCell      *result
);

/***********************************************************************
* -Procedure gfrfov_c ( GF, is ray in FOV? )
*
* -Abstract
*
* Determine time intervals when a specified ray intersects the
* space bounded by the field-of-view (FOV) of a specified
* instrument.
*
* void gfrfov_c (
*       ConstSpiceChar     * inst,
*       ConstSpiceDouble     raydir[3],
*       ConstSpiceChar     * rframe,
*       ConstSpiceChar     * abcorr,
*       ConstSpiceChar     * obsrvr,
*       SpiceDouble          step,
*       SpiceCell          * cnfine,
*       SpiceCell          * result  )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* SPICE_GF_MARGIN
*            P   Minimum complement of FOV cone angle.
* SPICE_GF_CNVTOL
*            P   Convergence tolerance.
* SPICE_GF_MAXVRT
*            P   Maximum number of FOV boundary vertices.
* inst       I   Name of the instrument.
* raydir     I   Ray's direction vector.
* rframe     I   Reference frame of ray's direction vector.
* abcorr     I   Aberration correction flag.
* obsrvr     I   Name of the observing body.
* step       I   Step size in seconds for finding FOV events.
* cnfine     I  SPICE window to which the search is restricted.
* result     O   SPICE window containing results.
***********************************************************************/

// cnfine changed to I from I-O per instructions of MRS.

%rename (gfrfov) gfrfov_c;
%apply (void RETURN_VOID) {void gfrfov_c};
%apply (ConstSpiceChar *CONST_STRING) {ConstSpiceChar *inst};
%apply (ConstSpiceDouble IN_ARRAY1[ANY]) {ConstSpiceDouble raydir[3]};
%apply (ConstSpiceChar *CONST_STRING) {ConstSpiceChar *rframe};
%apply (ConstSpiceChar *CONST_STRING) {ConstSpiceChar *abcorr};
%apply (ConstSpiceChar *CONST_STRING) {ConstSpiceChar *obsrvr};
%apply (SpiceCellDouble* INPUT)       {SpiceCell *cnfine};
%apply (SpiceCellDouble* OUTPUT)      {SpiceCell *result};

extern void gfrfov_c(
        ConstSpiceChar   *inst,
        ConstSpiceDouble raydir[3],
        ConstSpiceChar   *rframe,
        ConstSpiceChar   *abcorr,
        ConstSpiceChar   *obsrvr,
        SpiceDouble      step,
        SpiceCell        *cnfine,
        SpiceCell        *result
);

/***********************************************************************
* -Procedure gfrr_c (GF, range rate search )
*
* -Abstract
*
* Determine time intervals for which a specified constraint
* on the observer-target range rate is met.
*
* void gfrr_c (
*       ConstSpiceChar     * target,
*       ConstSpiceChar     * abcorr,
*       ConstSpiceChar     * obsrvr,
*       ConstSpiceChar     * relate,
*       SpiceDouble          refval,
*       SpiceDouble          adjust,
*       SpiceDouble          step,
*       SpiceInt             nintvls,
*       SpiceCell          * cnfine,
*       SpiceCell          * result  )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* SPICE_GF_CNVTOL
* P   Convergence tolerance.
* target     I   Name of the target body.
* abcorr     I   Aberration correction flag.
* obsrvr     I   Name of the observing body.
* relate     I   Relational operator.
* refval     I   Reference value.
* adjust     I   Adjustment value for absolute extrema searches.
* step       I   Step size used for locating extrema and roots.
* nintvls    I   Workspace window interval count.
* cnfine     I  SPICE window to which the search is confined.
* result     O   SPICE window containing results.
***********************************************************************/

// cnfine changed to I from I-O per instructions of MRS.

%rename (gfrr) gfrr_c;
%apply (void RETURN_VOID) {void gfrr_c};
%apply (ConstSpiceChar *CONST_STRING) {ConstSpiceChar *target};
%apply (ConstSpiceChar *CONST_STRING) {ConstSpiceChar *abcorr};
%apply (ConstSpiceChar *CONST_STRING) {ConstSpiceChar *obsrvr};
%apply (ConstSpiceChar *CONST_STRING) {ConstSpiceChar *relate};
%apply (SpiceCellDouble* INPUT)       {SpiceCell *cnfine};
%apply (SpiceCellDouble* OUTPUT)      {SpiceCell *result};

extern void gfrr_c(
        ConstSpiceChar *target,
        ConstSpiceChar *abcorr,
        ConstSpiceChar *obsrvr,
        ConstSpiceChar *relate,
        SpiceDouble    refval,
        SpiceDouble    adjust,
        SpiceDouble    step,
        SpiceInt       nintvls,
        SpiceCell      *cnfine,
        SpiceCell      *result
);

/***********************************************************************
* -Procedure gfsep_c (GF, angular separation search)
*
* -Abstract
*
* Determine time intervals when the angular separation between
* the position vectors of two target bodies relative to an observer
* satisfies a numerical relationship.
*
* void gfsep_c (
*       ConstSpiceChar     * targ1,
*       ConstSpiceChar     * shape1,
*       ConstSpiceChar     * frame1,
*       ConstSpiceChar     * targ2,
*       ConstSpiceChar     * shape2,
*       ConstSpiceChar     * frame2,
*       ConstSpiceChar     * abcorr,
*       ConstSpiceChar     * obsrvr,
*       ConstSpiceChar     * relate,
*       SpiceDouble          refval,
*       SpiceDouble          adjust,
*       SpiceDouble          step,
*       SpiceInt             nintvls,
*       SpiceCell          * cnfine,
*       SpiceCell          * result  )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* SPICE_GF_CNVTOL
* P   Convergence tolerance.
* targ1      I   Name of first body.
* shape1     I   Name of shape model describing the first body.
* frame1     I   The body-fixed reference frame of the first body.
* targ2      I   Name of second body.
* shape2     I   Name of the shape model describing the second body.
* frame2     I   The body-fixed reference frame of the second body.
* abcorr     I   Aberration correction flag.
* obsrvr     I   Name of the observing body.
* relate     I   Operator that either looks for an extreme value
*                (max, min, local, absolute) or compares the
*                angular separation value and `refval'.
* refval     I   Reference value.
* adjust     I   Absolute extremum adjustment value.
* step       I   Step size in seconds for finding angular separation
*                events.
* nintvls    I   Workspace window interval count.
* cnfine     I   SPICE window to which the search is restricted.
* result     O   SPICE window containing results.
***********************************************************************/

// cnfine changed to I from I-O per instructions of MRS.

%rename (gfsep) gfsep_c;
%apply (void RETURN_VOID) {void gfsep_c};
%apply (ConstSpiceChar *CONST_STRING) {ConstSpiceChar *targ1};
%apply (ConstSpiceChar *CONST_STRING) {ConstSpiceChar *shape1};
%apply (ConstSpiceChar *CONST_STRING) {ConstSpiceChar *frame1};
%apply (ConstSpiceChar *CONST_STRING) {ConstSpiceChar *targ2};
%apply (ConstSpiceChar *CONST_STRING) {ConstSpiceChar *shape2};
%apply (ConstSpiceChar *CONST_STRING) {ConstSpiceChar *frame2};
%apply (ConstSpiceChar *CONST_STRING) {ConstSpiceChar *abcorr};
%apply (ConstSpiceChar *CONST_STRING) {ConstSpiceChar *obsrvr};
%apply (ConstSpiceChar *CONST_STRING) {ConstSpiceChar *relate};
%apply (SpiceCellDouble* INPUT)       {SpiceCell *cnfine};
%apply (SpiceCellDouble* OUTPUT)      {SpiceCell *result};

extern void gfsep_c(
        ConstSpiceChar *targ1,
        ConstSpiceChar *shape1,
        ConstSpiceChar *frame1,
        ConstSpiceChar *targ2,
        ConstSpiceChar *shape2,
        ConstSpiceChar *frame2,
        ConstSpiceChar *abcorr,
        ConstSpiceChar *obsrvr,
        ConstSpiceChar *relate,
        SpiceDouble    refval,
        SpiceDouble    adjust,
        SpiceDouble    step,
        SpiceInt       nintvls,
        SpiceCell      *cnfine,
        SpiceCell      *result
);

/***********************************************************************
* -Procedure gfsntc_c (GF, surface intercept vector coordinate search)
*
* -Abstract
*
* Determine time intervals for which a coordinate of an
* surface intercept position vector satisfies a numerical constraint.
*
* void gfsntc_c (
*       ConstSpiceChar     * target,
*       ConstSpiceChar     * fixref,
*       ConstSpiceChar     * method,
*       ConstSpiceChar     * abcorr,
*       ConstSpiceChar     * obsrvr,
*       ConstSpiceChar     * dref,
*       ConstSpiceDouble     dvec[3],
*       ConstSpiceChar     * crdsys,
*       ConstSpiceChar     * coord,
*       ConstSpiceChar     * relate,
*       SpiceDouble          refval,
*       SpiceDouble          adjust,
*       SpiceDouble          step,
*       SpiceInt             nintvls,
*       SpiceCell          * cnfine,
*       SpiceCell          * result  )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* SPICE_GF_CNVTOL
* P   Convergence tolerance.
* target     I   Name of the target body.
* fixref     I   Body fixed frame associated with `target'.
* method     I   Name of method type for surface intercept
* calculation.
* abcorr     I   Aberration correction flag.
* obsrvr     I   Name of the observing body.
* dref       I   Reference frame of direction vector `dvec'.
* dvec       I   Pointing direction vector from `obsrvr'.
* crdsys     I   Name of the coordinate system containing `coord'.
* coord      I   Name of the coordinate of interest.
* relate     I   Relational operator.
* refval     I   Reference value.
* adjust     I   Adjustment value for absolute extrema searches.
* step       I   Step size used for locating extrema and roots.
* nintvls    I   Workspace window interval count.
* cnfine     I   SPICE window to which the search is confined.
* result     O   SPICE window containing results.
***********************************************************************/

// cnfine changed to I from I-O per instructions of MRS.

%rename (gfsntc) gfsntc_c;
%apply (void RETURN_VOID) {void gfsntc_c};
%apply (ConstSpiceChar *CONST_STRING) {ConstSpiceChar *target};
%apply (ConstSpiceChar *CONST_STRING) {ConstSpiceChar *fixref};
%apply (ConstSpiceChar *CONST_STRING) {ConstSpiceChar *method};
%apply (ConstSpiceChar *CONST_STRING) {ConstSpiceChar *abcorr};
%apply (ConstSpiceChar *CONST_STRING) {ConstSpiceChar *obsrvr};
%apply (ConstSpiceChar *CONST_STRING) {ConstSpiceChar *dref};
%apply (ConstSpiceDouble IN_ARRAY1[ANY]) {ConstSpiceDouble dvec[3]};
%apply (ConstSpiceChar *CONST_STRING) {ConstSpiceChar *crdsys};
%apply (ConstSpiceChar *CONST_STRING) {ConstSpiceChar *coord};
%apply (ConstSpiceChar *CONST_STRING) {ConstSpiceChar *relate};
%apply (SpiceCellDouble* INPUT)       {SpiceCell *cnfine};
%apply (SpiceCellDouble* OUTPUT)      {SpiceCell *result};

extern void gfsntc_c(
        ConstSpiceChar   *target,
        ConstSpiceChar   *fixref,
        ConstSpiceChar   *method,
        ConstSpiceChar   *abcorr,
        ConstSpiceChar   *obsrvr,
        ConstSpiceChar   *dref,
        ConstSpiceDouble dvec[3],
        ConstSpiceChar   *crdsys,
        ConstSpiceChar   *coord,
        ConstSpiceChar   *relate,
        SpiceDouble      refval,
        SpiceDouble      adjust,
        SpiceDouble      step,
        SpiceInt         nintvls,
        SpiceCell        *cnfine,
        SpiceCell        *result
);

/***********************************************************************
* -Procedure gfstol_c ( GF, set a tolerance value for GF )
*
* -Abstract
*
* Override the default GF convergence value used in the high
* level GF routines.
*
* void gfstol_c (
*       SpiceDouble value )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* value      I   Double precision value returned or to store.
***********************************************************************/

%rename (gfstol) gfstol_c;
%apply (void RETURN_VOID) {void gfstol_c};

extern void gfstol_c(
        SpiceDouble value
);

/***********************************************************************
* -Procedure gfsubc_c (GF, subpoint vector coordinate search)
*
* -Abstract
*
* Determine time intervals for which a coordinate of an
* subpoint position vector satisfies a numerical constraint.
*
* void gfsubc_c (
*       ConstSpiceChar     * target,
*       ConstSpiceChar     * fixref,
*       ConstSpiceChar     * method,
*       ConstSpiceChar     * abcorr,
*       ConstSpiceChar     * obsrvr,
*       ConstSpiceChar     * crdsys,
*       ConstSpiceChar     * coord,
*       ConstSpiceChar     * relate,
*       SpiceDouble          refval,
*       SpiceDouble          adjust,
*       SpiceDouble          step,
*       SpiceInt             nintvls,
*       SpiceCell          * cnfine,
*       SpiceCell          * result  )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* SPICE_GF_CNVTOL
*            P   Convergence tolerance.
* target     I   Name of the target body.
* fixref     I   Body fixed frame associated with `target'.
* method     I   Name of method type for subpoint calculation.
* abcorr     I   Aberration correction flag.
* obsrvr     I   Name of the observing body.
* crdsys     I   Name of the coordinate system containing `coord'.
* coord      I   Name of the coordinate of interest.
* relate     I   Relational operator.
* refval     I   Reference value.
* adjust     I   Adjustment value for absolute extrema searches.
* step       I   Step size used for locating extrema and roots.
* nintvls    I   Workspace window interval count.
* cnfine     I  SPICE window to which the search is confined.
* result     O   SPICE window containing results.
***********************************************************************/

// cnfine changed to I from I-O per instructions of MRS.

%rename (gfsubc) gfsubc_c;
%apply (void RETURN_VOID) {void gfsubc_c};
%apply (ConstSpiceChar *CONST_STRING) {ConstSpiceChar *target};
%apply (ConstSpiceChar *CONST_STRING) {ConstSpiceChar *fixref};
%apply (ConstSpiceChar *CONST_STRING) {ConstSpiceChar *method};
%apply (ConstSpiceChar *CONST_STRING) {ConstSpiceChar *abcorr};
%apply (ConstSpiceChar *CONST_STRING) {ConstSpiceChar *obsrvr};
%apply (ConstSpiceChar *CONST_STRING) {ConstSpiceChar *crdsys};
%apply (ConstSpiceChar *CONST_STRING) {ConstSpiceChar *coord};
%apply (ConstSpiceChar *CONST_STRING) {ConstSpiceChar *relate};
%apply (SpiceCellDouble* INPUT)       {SpiceCell *cnfine};
%apply (SpiceCellDouble* OUTPUT)      {SpiceCell *result};

extern void gfsubc_c(
        ConstSpiceChar *target,
        ConstSpiceChar *fixref,
        ConstSpiceChar *method,
        ConstSpiceChar *abcorr,
        ConstSpiceChar *obsrvr,
        ConstSpiceChar *crdsys,
        ConstSpiceChar *coord,
        ConstSpiceChar *relate,
        SpiceDouble    refval,
        SpiceDouble    adjust,
        SpiceDouble    step,
        SpiceInt       nintvls,
        SpiceCell      *cnfine,
        SpiceCell      *result
);

/***********************************************************************
* -Procedure gftfov_c ( GF, is target in FOV? )
*
* -Abstract
*
* Determine time intervals when a specified ephemeris object
* intersects the space bounded by the field-of-view (FOV) of a
* specified instrument.
*
* void gftfov_c (
*       ConstSpiceChar     * inst,
*       ConstSpiceChar     * target,
*       ConstSpiceChar     * tshape,
*       ConstSpiceChar     * tframe,
*       ConstSpiceChar     * abcorr,
*       ConstSpiceChar     * obsrvr,
*       SpiceDouble          step,
*       SpiceCell          * cnfine,
*       SpiceCell          * result  )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* SPICE_GF_MARGIN
*            P   Minimum complement of FOV cone angle.
* SPICE_GF_CNVTOL
*            P   Convergence tolerance.
* SPICE_GF_MAXVRT
*            P   Maximum number of FOV boundary vertices.
* inst       I   Name of the instrument.
* target     I   Name of the target body.
* tshape     I   Type of shape model used for target body.
* tframe     I   Body-fixed, body-centered frame for target body.
* abcorr     I   Aberration correction flag.
* obsrvr     I   Name of the observing body.
* step       I   Step size in seconds for finding FOV events.
* cnfine     I  SPICE window to which the search is restricted.
* result     O   SPICE window containing results.
***********************************************************************/

// cnfine changed to I from I-O per instructions of MRS.

%rename (gftfov) gftfov_c;
%apply (void RETURN_VOID) {void gftfov_c};
%apply (ConstSpiceChar *CONST_STRING) {ConstSpiceChar *inst};
%apply (ConstSpiceChar *CONST_STRING) {ConstSpiceChar *target};
%apply (ConstSpiceChar *CONST_STRING) {ConstSpiceChar *tshape};
%apply (ConstSpiceChar *CONST_STRING) {ConstSpiceChar *tframe};
%apply (ConstSpiceChar *CONST_STRING) {ConstSpiceChar *abcorr};
%apply (ConstSpiceChar *CONST_STRING) {ConstSpiceChar *obsrvr};
%apply (SpiceCellDouble* INPUT)       {SpiceCell *cnfine};
%apply (SpiceCellDouble* OUTPUT)      {SpiceCell *result};

extern void gftfov_c(
        ConstSpiceChar *inst,
        ConstSpiceChar *target,
        ConstSpiceChar *tshape,
        ConstSpiceChar *tframe,
        ConstSpiceChar *abcorr,
        ConstSpiceChar *obsrvr,
        SpiceDouble    step,
        SpiceCell      *cnfine,
        SpiceCell      *result
);

/***********************************************************************
* -Procedure hrmesp_c ( Hermite polynomial interpolation, equal spacing )
*
* -Abstract
*
* Evaluate, at a specified point, a Hermite interpolating polynomial
* for a specified set of equally spaced abscissa values and
* corresponding pairs of function and function derivative values.
*
* void hrmesp_c (
*       SpiceInt            n,
*       SpiceDouble         first,
*       SpiceDouble         step,
*       ConstSpiceDouble    yvals[],
*       SpiceDouble         x,
*       SpiceDouble       * f,
*       SpiceDouble       * df        )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* n          I   Number of points defining the polynomial.
* first      I   First abscissa value.
* step       I   Step size.
* yvals      I   Ordinate and derivative values.
* x          I   Point at which to interpolate the polynomial.
* f          O   Interpolated function value at `x'.
* df         O   Interpolated function's derivative at `x'.
***********************************************************************/

%rename (hrmesp) my_hrmesp_c;
%apply (void RETURN_VOID) {void my_hrmesp_c};
%apply (ConstSpiceDouble *IN_ARRAY1, SpiceInt DIM1)
                {(ConstSpiceDouble *yvals, SpiceInt nx2)};
%apply (SpiceDouble *OUTPUT) {SpiceDouble *f};
%apply (SpiceDouble *OUTPUT) {SpiceDouble *df};

%inline %{
    void my_hrmesp_c(
        SpiceDouble      first,
        SpiceDouble      step,
        ConstSpiceDouble *yvals, SpiceInt nx2,
        SpiceDouble      x,
        SpiceDouble      *f,
        SpiceDouble      *df)
    {
        hrmesp_c(nx2/2, first, step, yvals, x, f, df);
    }
%}

//Vector version
VECTORIZE_2d_di_d__2d(hrmesp, my_hrmesp_c)

/***********************************************************************
* -Procedure hrmint_c ( Hermite polynomial interpolation  )
*
* -Abstract
*
* Evaluate a Hermite interpolating polynomial at a specified
* abscissa value.
*
* void hrmint_c (
*       SpiceInt            n,
*       ConstSpiceDouble  * xvals,
*       ConstSpiceDouble    yvals[][2],
*       SpiceDouble         x,
*       SpiceDouble       * work,
*       SpiceDouble       * f,
*       SpiceDouble       * df )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* n          I   Number of points defining the polynomial.
* xvals      I   Abscissa values.
* yvals      I   Ordinate and derivative values.
* x          I   Point at which to interpolate the polynomial.
* work      I-O  Work space array.
* f          O   Interpolated function value at `x'.
* df         O   Interpolated function's derivative at `x'.
***********************************************************************/

%rename (hrmint) my_hrmint_c;
%apply (void RETURN_VOID) {void my_hrmint_c};
%apply (ConstSpiceDouble *IN_ARRAY1, SpiceInt DIM1)
                    {(ConstSpiceDouble *xvals, SpiceInt n)};
%apply (ConstSpiceDouble *IN_ARRAY2, SpiceInt DIM1, SpiceInt DIM2)
                    {(ConstSpiceDouble *yvals, SpiceInt n2, SpiceInt two)};
%apply (SpiceDouble *OUTPUT) {SpiceDouble *f};
%apply (SpiceDouble *OUTPUT) {SpiceDouble *df};

%inline %{
    void my_hrmint_c(
        ConstSpiceDouble *xvals, SpiceInt n,
        ConstSpiceDouble *yvals, SpiceInt n2, SpiceInt two,
        SpiceDouble      x,
        SpiceDouble      *f,
        SpiceDouble      *df)
    {
        *f = 0.;
        *df = 0.;

        if (!my_assert_eq(n2, n, "hrmint",
            "Array dimension mismatch in hrmint: "
            "xvals dimension = #; yvals dimension = #")) return;

        if (!my_assert_eq(two, 2, "hrmint",
            "Array dimension error in hrmint: "
            "second yvals dimension = #; should be 2")) return;

        SpiceDouble *work = my_malloc(4 * n + 4, "hrmint");
        if (work) {
            hrmint_c(n, xvals, yvals, x, work, f, df);
        }
        PyMem_Free(work);
    }
%}

//Vector version
VECTORIZE_di_dij_d__2d(hrmint, my_hrmint_c)

/***********************************************************************
* -Procedure hx2dp_c ( Hexadecimal string to d.p. number )
*
* -Abstract
*
* Convert a string representing a floating-point number in a
* base 16 "scientific notation" into its equivalent double
* precision number.
*
* void hx2dp_c (
*       ConstSpiceChar    * string,
*       SpiceInt            errmln,
*       SpiceDouble       * number,
*       SpiceBoolean      * error,
*       SpiceChar           errmsg[] )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* MAXMAN     P   Maximum number of digits in a hex mantissa.
* string     I   Hex form string to convert to floating-point.
* errmln     I   Available space for output string `errmsg'.
* number     O   Double precision value to be returned.
* error      O   A logical flag which is True on error.
* errmsg     O   A descriptive error message.
***********************************************************************/

%rename (hx2dp) my_hx2dp_c;
%apply (void RETURN_VOID) {void my_hx2dp_c};
%apply (ConstSpiceChar *CONST_STRING) {ConstSpiceChar *string};
%apply (SpiceDouble *OUTPUT) {SpiceDouble *number};
%apply (SpiceBoolean *OUTPUT) {SpiceBoolean *error};
%apply (SpiceInt DIM1, SpiceChar OUT_STRING[ANY])
                {(SpiceInt errmln, SpiceChar errmsg[MESSAGELEN])};

%inline %{
    void my_hx2dp_c(
        ConstSpiceChar *string,
        SpiceDouble    *number,
        SpiceBoolean   *error,
        SpiceInt       errmln, SpiceChar errmsg[MESSAGELEN])
    {
        hx2dp_c(string, errmln, number, error, errmsg);
    }
%}

/***********************************************************************
* -Procedure invstm_c ( Inverse of state transformation matrix )
*
* -Abstract
*
* Return the inverse of a state transformation matrix.
*
* void invstm_c (
*       ConstSpiceDouble    mat[6][6],
*       SpiceDouble         invmat[6][6] )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* mat        I   A state transformation matrix.
* invmat     O   The inverse of `mat'.
***********************************************************************/

%rename (invstm) invstm_c;
%apply (void RETURN_VOID) {void invstm_c};
%apply (ConstSpiceDouble IN_ARRAY2[ANY][ANY]) {ConstSpiceDouble mat[6][6]};
%apply (SpiceDouble OUT_ARRAY2[ANY][ANY]) {SpiceDouble invmat[6][6]};

extern void invstm_c(
        ConstSpiceDouble mat[6][6],
        SpiceDouble      invmat[6][6]
);

//Vector version
VECTORIZE_dXY__dMN(invstm, invstm_c, 6, 6)

/***********************************************************************
* -Procedure isrchc_c  ( Search in a character array )
*
* -Abstract
*
* Search for a given value within a character string array. Return
* the index of the first matching array entry, or -1 if the key
* value was not found.
*
* SpiceInt isrchc_c (
*       ConstSpiceChar  * value,
*       SpiceInt          ndim,
*       SpiceInt          arrlen,
*       const void        array[][]   )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* value      I   Key value to be found in array.
* ndim       I   Dimension of array.
* arrlen     I   String length.
* array      I   Character string array to search.
* index      R   Index of matching array entry.
***********************************************************************/

%rename (isrchc) isrchc_c;
%apply (SpiceInt RETURN_INT) {SpiceInt isrchc_c};
%apply (SpiceInt DIM1, SpiceInt DIM2, ConstSpiceChar *IN_STRINGS)
            {(SpiceInt ndim, SpiceInt arrlen, ConstSpiceChar *array)};

extern SpiceInt isrchc_c(
        ConstSpiceChar *CONST_STRING,
        SpiceInt       ndim, SpiceInt arrlen, ConstSpiceChar *array
);

/***********************************************************************
* -Procedure isrchd_c  ( Search in a double precision array )
*
* -Abstract
*
* Search for a given value within a floating-point array. Return
* the index of the first matching array entry, or -1 if the key value
* was not found.
*
* SpiceInt isrchd_c (
*       SpiceDouble         value,
*       SpiceInt            ndim,
*       ConstSpiceDouble  * array  )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* value      I   Key value to be found in array.
* ndim       I   Dimension of array.
* array      I   Double Precision array to search.
* index      R   Index of matching array entry.
***********************************************************************/

%rename (isrchd) isrchd_c;
%apply (SpiceInt RETURN_INT) {SpiceInt isrchd_c};
%apply (SpiceInt DIM1, ConstSpiceDouble *IN_ARRAY1)
                {(SpiceInt ndim, ConstSpiceDouble *array)};

extern SpiceInt isrchd_c(
        SpiceDouble value,
        SpiceInt    ndim, ConstSpiceDouble *array
);

/***********************************************************************
* -Procedure isrchi_c  ( Search in an integer array )
*
* -Abstract
*
* Search for a given value within an integer array. Return
* the index of the first matching array entry, or -1 if the key
* value was not found.
*
* SpiceInt isrchi_c (
*       SpiceInt         value,
*       SpiceInt         ndim,
*       ConstSpiceInt  * array  )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* value      I   Key value to be found in array.
* ndim       I   Dimension of array.
* array      I   Integer array to search.
* index      R   Index of matching array entry.
***********************************************************************/

%rename (isrchi) isrchi_c;
%apply (SpiceInt RETURN_INT) {SpiceInt isrchi_c};
%apply (SpiceInt DIM1, ConstSpiceInt *IN_ARRAY1)
                {(SpiceInt ndim, ConstSpiceInt *array)};

extern SpiceInt isrchi_c(
        SpiceInt      value,
        SpiceInt      ndim, ConstSpiceInt *array
);

/***********************************************************************
* -Procedure isordv_c ( Is array an order vector? )
*
* -Abstract
*
* Determine whether an array of n items contains the integers
* 0 through n-1.
*
* SpiceBoolean isordv_c (
*       ConstSpiceInt  * array,
*       SpiceInt         n      )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* array      I   Array of integers.
* n          I   Number of integers in array.
* flag       R   True if the condition is satisfied; False otherwise.
***********************************************************************/

%rename (isordv) isordv_c;
%apply (SpiceBoolean RETURN_BOOLEAN) {SpiceBoolean isordv_c};
%apply (ConstSpiceInt IN_ARRAY1[], SpiceInt DIM1)
                {(ConstSpiceInt array[], SpiceInt n)};

extern SpiceBoolean isordv_c(
        ConstSpiceInt array[], SpiceInt n
);

/***********************************************************************
* -Procedure iswhsp_c ( Determine whether a string is white space )
*
* -Abstract
*
* Return a boolean value indicating whether a string contains
* only white space characters.
*
* SpiceBoolean iswhsp_c (
*       ConstSpiceChar * string )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* string     I   String to be tested.
* flag       R   True if the condition is satisfied; False otherwise.
***********************************************************************/

%rename (iswhsp) iswhsp_c;
%apply (SpiceBoolean RETURN_BOOLEAN) {SpiceBoolean iswhsp_c};
%apply (ConstSpiceChar *CONST_STRING) {ConstSpiceChar *string};

extern SpiceBoolean iswhsp_c(
        ConstSpiceChar *CONST_STRING
);

/***********************************************************************
* -Procedure kclear_c ( Keeper clear )
*
* -Abstract
*
* Clear the KEEPER subsystem: unload all kernels, clear the kernel
* pool, and re-initialize the subsystem. Existing watches on kernel
* variables are retained.
*
* void kclear_c (
*       void )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
***********************************************************************/

%rename (kclear) kclear_c;
%apply (void RETURN_VOID) {void kclear_c};

extern void kclear_c(void);

/***********************************************************************
* -Procedure kdata_c ( Kernel Data )
*
* -Abstract
*
* Return data for the nth kernel that is among a list of specified
* kernel types.
*
* void kdata_c (
*       SpiceInt          which,
*       ConstSpiceChar  * kind,
*       SpiceInt          fileln,
*       SpiceInt          filtln,
*       SpiceInt          srclen,
*       SpiceChar       * file,
*       SpiceChar       * filtyp,
*       SpiceChar       * srcfil,
*       SpiceInt        * handle,
*       SpiceBoolean    * found  )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* which      I   Index of kernel to fetch from the list of kernels.
* kind       I   The kind of kernel to which fetches are limited.
* fileln     I   Maximum length of output string `fileln'.
* filtln     I   Maximum length of output string `filtln'.
* srclen     I   Maximum length of output string `srcfil'.
* file       O   The name of the kernel file.
* filtyp     O   The type of the kernel, one of "SPK", "SK", "DSK", "PCK",
*                "EK", "TEXT", "META", or "ALL". Default is "ALL".
*                To get multiple kinds, join them inside a string, separated by spaces.
* srcfil     O   Name of the source file used to load `file'.
* handle     O   The handle attached to `file'.
* found      O   True if the specified file could be located.
***********************************************************************/

%rename (kdata) my_kdata_c;
%apply (void RETURN_VOID) {void my_kdata_c};
%apply (ConstSpiceChar *CONST_STRING) {ConstSpiceChar *kind};
%apply (SpiceInt DIM1, SpiceChar OUT_STRING[ANY]) {(SpiceInt fileln, SpiceChar file[FILELEN])};
%apply (SpiceInt DIM1, SpiceChar OUT_STRING[ANY]) {(SpiceInt filtln, SpiceChar filtyp[NAMELEN])};
%apply (SpiceInt DIM1, SpiceChar OUT_STRING[ANY]) {(SpiceInt srclen, SpiceChar srcfil[FILELEN])};
%apply (SpiceInt *OUTPUT) {SpiceInt *handle};
%apply (SpiceBoolean *OUTPUT) {SpiceBoolean *found};

%inline %{
    void my_kdata_c(
        SpiceInt       which,
        ConstSpiceChar *kind,
        SpiceInt       fileln, SpiceChar file[FILELEN],
        SpiceInt       filtln, SpiceChar filtyp[NAMELEN],
        SpiceInt       srclen, SpiceChar srcfil[FILELEN],
        SpiceInt       *handle,
        SpiceBoolean   *found)
    {
        kdata_c(which, kind, fileln, filtln, srclen,
                file, filtyp, srcfil, handle, found);
    }
%}

//CSPYCE_DEFAULT:which:0
//CSPYCE_DEFAULT:kind:"ALL"

/***********************************************************************
* -Procedure kinfo_c ( Kernel Information )
*
* -Abstract
*
* Return information about a loaded kernel specified by name.
*
* void kinfo_c (
*       ConstSpiceChar  * file,
*       SpiceInt          filtln,
*       SpiceInt          srclen,
*       SpiceChar       * filtyp,
*       SpiceChar       * srcfil,
*       SpiceInt        * handle,
*       SpiceBoolean    * found  )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* file       I   Name of a kernel to fetch information for
* filtln     I   Available space in output kernel type string.
* srclen     I   Available space in output `srcfil' string.
* filtyp     O   The type of the kernel, one of "SPK", "SK", "DSK", "PCK",
*                "EK", "TEXT", "META", or "ALL".
* srcfil     O   Name of the source file used to load `file'.
* handle     O   The handle attached to `file'.
* found      O   True if the specified file could be located.
***********************************************************************/

%rename (kinfo) my_kinfo_c;
%apply (void RETURN_VOID) {void my_kinfo_c};
%apply (ConstSpiceChar *CONST_STRING) {ConstSpiceChar *file};
%apply (SpiceInt DIM1, SpiceChar OUT_STRING[ANY]) {(SpiceInt filtln, SpiceChar filtyp[NAMELEN])};
%apply (SpiceInt DIM1, SpiceChar OUT_STRING[ANY]) {(SpiceInt srclen, SpiceChar srcfil[FILELEN])};
%apply (SpiceInt *OUTPUT) {SpiceInt *handle};
%apply (SpiceBoolean *OUTPUT) {SpiceBoolean *found};

%inline %{
    void my_kinfo_c(
        ConstSpiceChar *file,
        SpiceInt       filtln,  SpiceChar filtyp[NAMELEN],
        SpiceInt       srclen,  SpiceChar srcfil[FILELEN],
        SpiceInt       *handle,
        SpiceBoolean   *found)
    {
        kinfo_c(file, filtln, srclen, filtyp, srcfil, handle, found);
    }
%}

/***********************************************************************
* -Procedure ktotal_c ( Kernel Totals )
*
* -Abstract
*
* Return the number of kernels of a specified type that are
* currently loaded via the furnsh_c interface.
*
* void ktotal_c (
*       ConstSpiceChar   * kind,
*       SpiceInt         * count )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* kind       I   The kind of kernels to count, one of
*                "SPK", "SK", "DSK", "PCK", "EK", "TEXT", "META", or "ALL".
*                To count multiple kinds, join them inside a string, separated by spaces.
*                Default is "ALL".
* count      O   The number of kernels of type `kind'.
***********************************************************************/

%rename (ktotal) ktotal_c;
%apply (void RETURN_VOID) {void ktotal_c};
%apply (ConstSpiceChar *CONST_STRING) {ConstSpiceChar *kind};

extern void ktotal_c(
        ConstSpiceChar *CONST_STRING,
        SpiceInt       *OUTPUT
);

//CSPYCE_DEFAULT:kind:"ALL"

/***********************************************************************
* -Procedure kxtrct_c ( Extract a substring starting with a keyword )
*
* -Abstract
*
* Locate a keyword in a string and extract the substring from
* the beginning of the first word following the keyword to the
* beginning of the first subsequent recognized terminator of a list.
*
* void kxtrct_c (
*       ConstSpiceChar       * keywd,
*       SpiceInt               termlen,
*       const void             terms[][],
*       SpiceInt               nterms,
*       SpiceInt               worlen,
*       SpiceInt               sublen,
*       SpiceChar            * wordsq,
*       SpiceBoolean         * found,
*       SpiceChar            * substr     )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* keywd      I   Word that marks the beginning of text of interest.
* termlen    I   Length of strings in string array `terms'.
* terms      I   Set of words, any of which marks the end of text.
* nterms     I   Number of terms.
* worlen     I   Declared length of string `wordsq'.
* sublen     I   Declared length of output string `substr'.
* wordsq    I-O  String containing a sequence of words.
* found      O   True if the keyword is found in the string.
* substr     O   String from end of `keywd' to beginning of first
*                `terms' item found.
***********************************************************************/

%rename (kxtrct) my_kxtrct_c;
%apply (void RETURN_VOID) {void my_kxtrct_c};
%apply (ConstSpiceChar *CONST_STRING) {ConstSpiceChar *keywd};
%apply (SpiceInt DIM1, SpiceInt DIM2, ConstSpiceChar *IN_STRINGS)
                {(SpiceInt nterms, SpiceInt termlen, ConstSpiceChar *terms)};
%apply (SpiceInt DIM1, SpiceChar *INOUT_STRING) {(SpiceInt worlen, SpiceChar *wordsq)};
%apply (SpiceInt DIM1, SpiceChar OUT_STRING[ANY])
                {(SpiceInt sublen, SpiceChar substr[MESSAGELEN])};

%inline %{
    void my_kxtrct_c(
        ConstSpiceChar *keywd,
        SpiceInt       nterms, SpiceInt  termlen, ConstSpiceChar *terms,
        SpiceInt       worlen, SpiceChar *wordsq,
        SpiceBoolean   *found,
        SpiceInt       sublen, SpiceChar substr[MESSAGELEN])
    {
        kxtrct_c(keywd, termlen, terms, nterms, worlen, sublen, wordsq,
                 found, substr);
    }
%}

/***********************************************************************
* -Procedure lgresp_c ( Lagrange interpolation on equally spaced points )
*
* -Abstract
*
* Evaluate a Lagrange interpolating polynomial for a specified
* set of coordinate pairs whose first components are equally
* spaced, at a specified abscissa value.
*
* SpiceDouble lgresp_c (
*       SpiceInt            n,
*       SpiceDouble         first,
*       SpiceDouble         step,
*       ConstSpiceDouble    yvals[],
*       SpiceDouble         x         )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* n          I   Number of points defining the polynomial.
* first      I   First abscissa value.
* step       I   Step size.
* yvals      I   Ordinate values.
* x          I   Point at which to interpolate the polynomial.
* value      R   Value of Lagrange polynomial.
***********************************************************************/

%rename (lgresp) my_lgresp_c;
%apply (SpiceDouble RETURN_DOUBLE) {SpiceDouble my_lgresp_c};
%apply (ConstSpiceDouble *IN_ARRAY1, SpiceInt DIM1)
                {(ConstSpiceDouble *yvals, SpiceInt n)};

%inline %{
    SpiceDouble my_lgresp_c(
        SpiceDouble      first,
        SpiceDouble      step,
        ConstSpiceDouble *yvals, SpiceInt n,
        SpiceDouble      x)
    {
        return lgresp_c(n, first, step, yvals, x);
    }
%}

//Vector version
VECTORIZE_2d_di_d__RETURN_d(lgresp, my_lgresp_c)

/***********************************************************************
* -Procedure lgrind_c (Lagrange polynomial interpolation with derivative)
*
* -Abstract
*
* Evaluate a Lagrange interpolating polynomial, for a specified
* set of coordinate pairs, at a specified abscissa value. Return
* both the value of the polynomial and its derivative.
*
* void lgrind_c (
*       SpiceInt            n,
*       ConstSpiceDouble  * xvals,
*       ConstSpiceDouble  * yvals,
*       SpiceDouble       * work,
*       SpiceDouble         x,
*       SpiceDouble       * p,
*       SpiceDouble       * dp )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* n          I   Number of points defining the polynomial.
* xvals      I   Abscissa values.
* yvals      I   Ordinate values.
* work      I-O  Work space array.
* x          I   Point at which to interpolate the polynomial.
* p          O   Polynomial value at `x'.
* dp         O   Polynomial derivative at `x'.
***********************************************************************/

%rename (lgrind) my_lgrind_c;
%apply (void RETURN_VOID) {void my_lgrind_c};
%apply (ConstSpiceDouble *IN_ARRAY1, SpiceInt DIM1) {(ConstSpiceDouble *xvals, SpiceInt n)};
%apply (ConstSpiceDouble *IN_ARRAY1, SpiceInt DIM1) {(ConstSpiceDouble *yvals, SpiceInt n2)};
%apply (SpiceDouble *OUTPUT) {SpiceDouble *p};
%apply (SpiceDouble *OUTPUT) {SpiceDouble *dp};

%inline %{
    void my_lgrind_c(
        ConstSpiceDouble *xvals, SpiceInt n,
        ConstSpiceDouble *yvals, SpiceInt n2,
        SpiceDouble x,
        SpiceDouble *p,
        SpiceDouble *dp)
    {
        *p = 0.;
        *dp = 0.;

        if (!my_assert_eq(n, n2, "lgrind",
            "Array dimension mismatch in lgrind: "
            "xvals dimension = #; yvals dimension = #")) return;

        SpiceDouble *work = my_malloc(2*n + 2, "lgrind");
        if (work) {
            lgrind_c(n, xvals, yvals, work, x, p, dp);
        }
        PyMem_Free(work);
    }
%}

//Vector version
VECTORIZE_di_di_d__2d(lgrind, my_lgrind_c)

/***********************************************************************
* -Procedure lgrint_c ( Lagrange polynomial interpolation )
*
* -Abstract
*
* Evaluate a Lagrange interpolating polynomial for a specified
* set of coordinate pairs, at a specified abscissa value.
*
* SpiceDouble lgrint_c (
*       SpiceInt            n,
*       ConstSpiceDouble    xvals[],
*       ConstSpiceDouble    yvals[],
*       SpiceDouble         x         )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* n          I   Number of points defining the polynomial.
* xvals      I   Abscissa values.
* yvals      I   Ordinate values.
* x          I   Point at which to interpolate the polynomial.
* value      R   Value of Lagrange polynomial.
***********************************************************************/

%rename (lgrint) my_lgrint_c;
%apply (SpiceDouble RETURN_DOUBLE) {SpiceDouble my_lgrint_c};
%apply (ConstSpiceDouble *IN_ARRAY1, SpiceInt DIM1) {(ConstSpiceDouble *xvals, SpiceInt n)};
%apply (ConstSpiceDouble *IN_ARRAY1, SpiceInt DIM1) {(ConstSpiceDouble *yvals, SpiceInt n2)};

%inline %{
    SpiceDouble my_lgrint_c(
        ConstSpiceDouble *xvals, SpiceInt n,
        ConstSpiceDouble *yvals, SpiceInt n2,
        SpiceDouble x)
    {
        if (!my_assert_eq(n, n2, "lgrint",
            "Array dimension mismatch in lgrint: "
            "xvals dimension = #; yvals dimension = #")) return 0.;

        return lgrint_c(n, xvals, yvals, x);
    }
%}

//Vector version
VECTORIZE_di_di_d__RETURN_d(lgrint, my_lgrint_c)

/***********************************************************************
* -Procedure lmpool_c ( Load variables from memory into the pool )
*
* -Abstract
*
* Load the variables contained in an internal buffer into the
* kernel pool.
*
* void lmpool_c (
*       const void    cvals[][],
*       SpiceInt      cvalen,
*       SpiceInt      n       )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* cvals      I   An array that contains a SPICE text kernel.
* cvalen     I   Length of strings in cvals.
* n          I   The number of entries in cvals.
***********************************************************************/

%rename (lmpool) my_lmpool_c;
%apply (void RETURN_VOID) {void lmpool_c};
%apply (ConstSpiceChar *IN_STRINGS, SpiceInt DIM1, SpiceInt DIM2)
                {(ConstSpiceChar *cvals, SpiceInt n, SpiceInt cvalen)};

%inline %{
    void my_lmpool_c(
        ConstSpiceChar *cvals, SpiceInt n, SpiceInt cvalen)
    {
        lmpool_c(cvals, cvalen, n);
    }
%}

/***********************************************************************
* -Procedure lparse_c ( Parse items from a list )
*
* -Abstract
*
* Parse a list of items delimited by a single character.
*
* void lparse_c (
*       ConstSpiceChar   * list,
*       ConstSpiceChar   * delim,
*       SpiceInt           nmax,
*       SpiceInt           itemln,
*       SpiceInt         * n,
*       void             * items   )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* list       I    List of items delimited by delim.
* delim      I    Single character used to delimit items.
* nmax       I    Maximum number of items to return.
* itemln     I    Length of strings in item array.
* n          O    Number of items in the list.
* items      O    Items in the list, left justified.
***********************************************************************/

%rename (lparse) lparse_c;
%apply (void RETURN_VOID) {void lparse_c};
%apply (ConstSpiceChar *CONST_STRING) {ConstSpiceChar *list};
%apply (ConstSpiceChar *CONST_STRING) {ConstSpiceChar *delim};
%apply (SpiceInt DIM1, SpiceInt DIM2, SpiceInt *NSTRINGS, SpiceChar OUT_STRINGS[ANY][ANY])
        {(SpiceInt nmax, SpiceInt itemln, SpiceInt *n, SpiceChar items[MAXVALS][NAMELEN])};

extern void lparse_c(
        ConstSpiceChar *CONST_STRING,
        ConstSpiceChar *CONST_STRING,
        SpiceInt       nmax, SpiceInt itemln, SpiceInt *n, SpiceChar items[MAXVALS][NAMELEN]
);

/***********************************************************************
* -Procedure lparsm_c (Parse a list of items having multiple delimiters)
*
* -Abstract
*
* Parse a list of items separated by multiple delimiters.
*
* void lparsm_c (
*       ConstSpiceChar   * list,
*       ConstSpiceChar   * delims,
*       SpiceInt           nmax,
*       SpiceInt           itemln,
*       SpiceInt         * n,
*       void             * items   )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* list       I    List of items delimited by delims.
* delims     I    Single characters which delimit items.
* nmax       I    Maximum number of items to return.
* itemln     I    Length of strings in item array.
* n          O    Number of items in the list.
* items      O    Items in the list, left justified.
***********************************************************************/

%rename (lparsm) lparsm_c;
%apply (void RETURN_VOID) {void lparsm_c};
%apply (ConstSpiceChar *CONST_STRING) {ConstSpiceChar *list};
%apply (ConstSpiceChar *CONST_STRING) {ConstSpiceChar *delims};
%apply (SpiceInt DIM1, SpiceInt DIM2, SpiceInt *NSTRINGS, SpiceChar OUT_STRINGS[ANY][ANY])
        {(SpiceInt nmax, SpiceInt itemln, SpiceInt *n, SpiceChar items[MAXVALS][COLLEN])};

extern void lparsm_c(
        ConstSpiceChar *CONST_STRING,
        ConstSpiceChar *CONST_STRING,
        SpiceInt       nmax, SpiceInt itemln, SpiceInt *n, SpiceChar items[MAXVALS][COLLEN]
);

/***********************************************************************
* -Procedure lstlec_c ( Last character element less than or equal to. )
*
* -Abstract
*
* Find the index of the largest array element less than or equal to
* a given character string in an ordered array of character strings.
*
* SpiceInt lstlec_c (
*       ConstSpiceChar  * string,
*       SpiceInt          n,
*       SpiceInt          arrlen,
*       const void        array[][]   )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* string     I   Upper bound value to search against.
* n          I   Number of elements in `array'.
* arrlen     I   Declared length of the strings in `array'.
* array      I   Array of possible lower bounds.
* index      R   Index of element in array.
***********************************************************************/

%rename (lstlec) lstlec_c;
%apply (SpiceInt RETURN_INT) {SpiceInt lstlec_c};
%apply (SpiceInt DIM1, SpiceInt DIM2, ConstSpiceChar *IN_STRINGS)
                {(SpiceInt n, SpiceInt arrlen, ConstSpiceChar *array)};

extern SpiceInt lstlec_c(
        ConstSpiceChar *CONST_STRING,
        SpiceInt       n, SpiceInt arrlen, ConstSpiceChar *array
);

/***********************************************************************
* -Procedure lstled_c ( Last double precision element less than or equal)
*
* -Abstract
*
* Find the index of the largest array element less than or equal
* to a given number `x' in an array of non-decreasing numbers.
*
* SpiceInt lstled_c (
*       SpiceDouble         x,
*       SpiceInt            n,
*       ConstSpiceDouble  * array )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* x          I   Upper bound value to search against.
* n          I   Number of elements in `array'.
* array      I   Array of possible lower bounds.
* index      R   Index of element in array.
***********************************************************************/

%rename (lstled) lstled_c;
%apply (SpiceInt RETURN_INT) {SpiceInt lstled_c};
%apply (SpiceInt DIM1, ConstSpiceDouble *IN_ARRAY1)
                {(SpiceInt n, ConstSpiceDouble *array)};

extern SpiceInt lstled_c(
        SpiceDouble x,
        SpiceInt    n, ConstSpiceDouble *array
);

/***********************************************************************
* -Procedure lstlei_c ( Last integer element less than or equal to )
*
* -Abstract
*
* Find the index of the largest array element less than or equal
* to a given integer `x' in an array of non-decreasing integers.
*
* SpiceInt lstlei_c (
*       SpiceInt            x,
*       SpiceInt            n,
*       ConstSpiceInt     * array )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* x          I   Upper bound value to search against.
* n          I   Number of elements in `array'.
* array      I   Array of possible lower bounds.
* index      R   Index of element in array.
***********************************************************************/

%rename (lstlei) lstlei_c;
%apply (SpiceInt RETURN_INT) {SpiceInt lstlei_c};
%apply (SpiceInt DIM1, ConstSpiceInt *IN_ARRAY1)
                {(SpiceInt n, ConstSpiceInt *array)};

extern SpiceInt lstlei_c(
        SpiceInt x,
        SpiceInt n, ConstSpiceInt *array
);

/***********************************************************************
* -Procedure lstltc_c ( Last character element less than )
*
* -Abstract
*
* Find the index of the largest array element less than a given
* character string in an ordered array of character strings.
*
* SpiceInt lstltc_c (
*       ConstSpiceChar  * string,
*       SpiceInt          n,
*       SpiceInt          arrlen,
*       const void        array[][]   )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* string     I   Upper bound value to search against.
* n          I   Number of elements in `array'.
* arrlen     I   Declared length of the strings in `array'.
* array      I   Array of possible lower bounds.
* index      R   Index of element in array.
***********************************************************************/

%rename (lstltc) lstltc_c;
%apply (SpiceInt RETURN_INT) {SpiceInt lstltc_c};
%apply (SpiceInt DIM1, SpiceInt DIM2, ConstSpiceChar *IN_STRINGS)
                {(SpiceInt n, SpiceInt arrlen, ConstSpiceChar *array)};

extern SpiceInt lstltc_c(
        ConstSpiceChar *CONST_STRING,
        SpiceInt       n, SpiceInt arrlen, ConstSpiceChar *array
);

/***********************************************************************
* -Procedure lstltd_c ( Last double precision element less than )
*
* -Abstract
*
* Find the index of the largest array element less than
* a given number `x' in an array of non-decreasing numbers.
*
* SpiceInt lstltd_c (
*       SpiceDouble         x,
*       SpiceInt            n,
*       ConstSpiceDouble  * array )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* x          I   Upper bound value to search against.
* n          I   Number of elements in `array'.
* array      I   Array of possible lower bounds.
* index      R   Index of element in array.
***********************************************************************/

%rename (lstltd) lstltd_c;
%apply (SpiceInt RETURN_INT) {SpiceInt lstltd_c};
%apply (SpiceInt DIM1, ConstSpiceDouble *IN_ARRAY1)
                {(SpiceInt n, ConstSpiceDouble *array)};

extern SpiceInt lstltd_c(
        SpiceDouble x,
        SpiceInt    n, ConstSpiceDouble *array
);

/***********************************************************************
* -Procedure lstlti_c ( Last integer element less than )
*
* -Abstract
*
* Find the index of the largest array element less than
* a given integer `x' in an array of non-decreasing integers.
*
* SpiceInt lstlti_c (
*       SpiceInt          x,
*       SpiceInt          n,
*       ConstSpiceInt   * array )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* x          I   Upper bound value to search against.
* n          I   Number of elements in `array'.
* array      I   Array of possible lower bounds.
* index      R   Index of element in array.
***********************************************************************/

%rename (lstlti) lstlti_c;
%apply (SpiceInt RETURN_INT) {SpiceInt lstlti_c};
%apply (SpiceInt DIM1, ConstSpiceInt *IN_ARRAY1)
                {(SpiceInt n, ConstSpiceInt *array)};

extern SpiceInt lstlti_c(
        SpiceInt x,
        SpiceInt n, ConstSpiceInt *array
);

/***********************************************************************
* -Procedure lx4dec_c (Scan for decimal number)
*
* -Abstract
*
* Scan a string from a specified starting position for the
* end of a decimal number.
*
* void lx4dec_c (
*       ConstSpiceChar   * string,
*       SpiceInt           first,
*       SpiceInt         * last,
*       SpiceInt         * nchar  )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* string     I   Any character string.
* first      I   First character to scan from in string.
* last       O   Last character that is part of a decimal number.
* nchar      O   Number of characters in the decimal number.
***********************************************************************/

%rename (lx4dec) lx4dec_c;
%apply (void RETURN_VOID) {void lx4dec_c};

extern void lx4dec_c(
        ConstSpiceChar *CONST_STRING,
        SpiceInt       first,
        SpiceInt       *OUTPUT,
        SpiceInt       *OUTPUT
);

/***********************************************************************
* -Procedure lx4num_c (Scan for number)
*
* -Abstract
*
* Scan a string from a specified starting position for the
* end of a number.
*
* void lx4num_c (
*       ConstSpiceChar   * string,
*       SpiceInt           first,
*       SpiceInt         * last,
*       SpiceInt         * nchar  )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* string     I   Any character string.
* first      I   First character to scan from in string.
* last       O   Last character that is part of a number.
* nchar      O   Number of characters in the number.
***********************************************************************/

%rename (lx4num) lx4num_c;
%apply (void RETURN_VOID) {void lx4num_c};

extern void lx4num_c(
        ConstSpiceChar *CONST_STRING,
        SpiceInt       first,
        SpiceInt       *OUTPUT,
        SpiceInt       *OUTPUT
);

/***********************************************************************
* -Procedure lx4sgn_c (Scan for signed integer)
*
* -Abstract
*
* Scan a string from a specified starting position for the
* end of a signed integer.
*
* void lx4sgn_c (
*       ConstSpiceChar   * string,
*       SpiceInt           first,
*       SpiceInt         * last,
*       SpiceInt         * nchar  )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* string     I   Any character string.
* first      I   First character to scan from in string.
* last       O   Last character that is part of a signed integer.
* nchar      O   Number of characters in the signed integer.
***********************************************************************/

%rename (lx4sgn) lx4sgn_c;
%apply (void RETURN_VOID) {void lx4sgn_c};

extern void lx4sgn_c(
        ConstSpiceChar *CONST_STRING,
        SpiceInt       first,
        SpiceInt       *OUTPUT,
        SpiceInt       *OUTPUT
);

/***********************************************************************
* -Procedure lx4uns_c (Scan for unsigned integer)
*
* -Abstract
*
* Scan a string from a specified starting position for the
* end of an unsigned integer.
*
* void lx4uns_c (
*       ConstSpiceChar   * string,
*       SpiceInt           first,
*       SpiceInt         * last,
*       SpiceInt         * nchar  )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* string     I   Any character string.
* first      I   First character to scan from in string.
* last       O   Last character that is part of an unsigned integer.
* nchar      O   Number of characters in the unsigned integer.
***********************************************************************/

%rename (lx4uns) lx4uns_c;
%apply (void RETURN_VOID) {void lx4uns_c};

extern void lx4uns_c(
        ConstSpiceChar *CONST_STRING,
        SpiceInt       first,
        SpiceInt       *OUTPUT,
        SpiceInt       *OUTPUT
);

/***********************************************************************
* -Procedure lxqstr_c ( Lex quoted string )
*
* -Abstract
*
* Scan (lex) a quoted string.
*
* void lxqstr_c (
*       ConstSpiceChar    * string,
*       SpiceChar           qchar,
*       SpiceInt            first,
*       SpiceInt          * last,
*       SpiceInt          * nchar  )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* string     I   String to be scanned.
* qchar      I   Quote delimiter character.
* first      I   Character position at which to start scanning.
* last       O   Character position of end of token.
* nchar      O   Number of characters in token.
***********************************************************************/

%rename (lxqstr) lxqstr_c;
%apply (void RETURN_VOID) {void lxqstr_c};

extern void lxqstr_c(
        ConstSpiceChar *CONST_STRING,
        SpiceChar      IN_STRING,
        SpiceInt       first,
        SpiceInt       *OUTPUT,
        SpiceInt       *OUTPUT
);

/***********************************************************************
* -Procedure matchi_c ( Match string against wildcard template )
*
* -Abstract
*
* Determine whether a string is matched by a template containing
* wild cards. The pattern comparison is case-insensitive.
*
* SpiceBoolean matchi_c (
*       ConstSpiceChar      * string,
*       ConstSpiceChar      * templ,
*       SpiceChar             wstr,
*       SpiceChar             wchr   )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* string     I   String to be tested.
* templ      I   Template (with wild cards) to test against string.
* wstr       I   Wild string token.
* wchr       I   Wild character token.
* flag       R   True if the string matches; False otherwise.
***********************************************************************/

%rename (matchi) matchi_c;
%apply (SpiceBoolean RETURN_BOOLEAN) {SpiceBoolean matchi_c};

extern void matchi_c(
        ConstSpiceChar *CONST_STRING,
        SpiceChar      *CONST_STRING,
        SpiceChar      IN_STRING,
        SpiceChar      IN_STRING
);

/***********************************************************************
* -Procedure matchw_c ( Match string against wildcard template )
*
* -Abstract
*
* Determine whether a string is matched by a template containing
* wild cards. The comparison is case-sensitive.
*
* SpiceBoolean matchw_c (
*       ConstSpiceChar      * string,
*       ConstSpiceChar      * templ,
*       SpiceChar             wstr,
*       SpiceChar             wchr   )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* string     I   String to be tested.
* templ      I   Template (with wild cards) to test against string.
* wstr       I   Wild string token.
* wchr       I   Wild character token.
* flag       R   True if the string matches; False otherwise.
***********************************************************************/

%rename (matchw) matchw_c;
%apply (SpiceBoolean RETURN_BOOLEAN) {SpiceBoolean matchw_c};

extern void matchw_c(
        ConstSpiceChar *CONST_STRING,
        ConstSpiceChar *CONST_STRING,
        SpiceChar      IN_STRING,
        SpiceChar      IN_STRING
);

/***********************************************************************
* -Procedure ncpos_c ( NOT Character position )
*
* -Abstract
*
* Find the first occurrence in a string of a character NOT belonging
* to a collection of characters, starting at a specified location,
* searching forward.
*
* SpiceInt ncpos_c (
*       ConstSpiceChar    * str,
*       ConstSpiceChar    * chars,
*       SpiceInt            start  )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* str        I   Any character string.
* chars      I   A collection of characters.
* start      I   Position to begin looking for one not in chars.
* index      R   Index of character in string.
***********************************************************************/

%rename (ncpos) ncpos_c;
%apply (SpiceInt RETURN_INT) {SpiceInt ncpos_c};

extern SpiceInt ncpos_c(
        ConstSpiceChar *CONST_STRING,
        ConstSpiceChar *CONST_STRING,
        SpiceInt       start
);

/***********************************************************************
* -Procedure ncposr_c ( Character position, reverse )
*
* -Abstract
*
* Find the first occurrence in a string of a character NOT belonging
* to a collection of characters, starting at a specified location,
* searching in reverse.
*
* SpiceInt ncposr_c (
*       ConstSpiceChar    * str,
*       ConstSpiceChar    * chars,
*       SpiceInt            start  )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* str        I   Any character string.
* chars      I   A collection of characters.
* start      I   Position to begin looking for one of chars.
* index      R   Index of character in string.
***********************************************************************/

%rename (ncposr) ncposr_c;
%apply (SpiceInt RETURN_INT) {SpiceInt ncposr_c};

extern SpiceInt ncposr_c(
        ConstSpiceChar *CONST_STRING,
        ConstSpiceChar *CONST_STRING,
        SpiceInt       start
);

/***********************************************************************
* -Procedure nextwd_c ( Next word in a character string )
*
* -Abstract
*
* Return the next word in a given character string, and
* left justify the rest of the string.
*
* void nextwd_c (
*       ConstSpiceChar    * string,
*       SpiceInt            nexlen,
*       SpiceInt            reslen,
*       SpiceChar         * next,
*       SpiceChar         * rest   )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* string     I   Input character string.
* nexlen     I   Maximum length of output string `next'.
* reslen     I   Maximum length of output string `rest'.
* next       O   The next word in the string.
* rest       O   The remaining part of `string', left-justified.
***********************************************************************/

%rename (nextwd) my_nextwd_c;
%apply (void RETURN_VOID) {void my_nextwd_c};
%apply (ConstSpiceChar *CONST_STRING) {ConstSpiceChar *string};
%apply (SpiceInt DIM1, SpiceChar OUT_STRING[ANY]) {(SpiceInt nexlen, SpiceChar next[COLLEN])};
%apply (SpiceInt DIM1, SpiceChar OUT_STRING[ANY]) {(SpiceInt reslen, SpiceChar rest[MESSAGELEN])};

%inline %{
    void my_nextwd_c(
        ConstSpiceChar *string,
        SpiceInt       nexlen, SpiceChar next[COLLEN],
        SpiceInt       reslen, SpiceChar rest[MESSAGELEN])
    {
        nextwd_c(string, nexlen, reslen, next, rest);
    }
%}

/***********************************************************************
* -Procedure nthwd_c ( n'th word in a character string )
*
* -Abstract
*
* Return the nth word in a character string, and its location
* in the string.
*
* void nthwd_c (
*       ConstSpiceChar    * string,
*       SpiceInt            nth,
*       SpiceInt            worlen,
*       SpiceChar         * word,
*       SpiceInt          * loc    )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* string     I   Input character string.
* nth        I   Index of the word to be returned.
* worlen     I   Maximum length of output string `word'.
* word       O   The `nth' word in `string'.
* loc        O   Location of `word' in `string'.
***********************************************************************/

%rename (nthwd) nthwd_c;
%apply (void RETURN_VOID) {void nthwd_c};
%apply (ConstSpiceChar *CONST_STRING) {ConstSpiceChar *string};
%apply (SpiceInt DIM1, SpiceChar OUT_STRING[ANY])
                {(SpiceInt worlen, SpiceChar word[COLLEN])};

extern void nthwd_c(
        ConstSpiceChar *CONST_STRING,
        SpiceInt       nth,
        SpiceInt       worlen, SpiceChar word[COLLEN],
        SpiceInt       *OUTPUT
);

/***********************************************************************
* -Procedure orderc_c ( Order of a character array )
*
* -Abstract
*
* Determine the order of elements in an array of character strings.
*
* void orderc_c (
*       SpiceInt      arrlen,
*       const void    array[][],
*       SpiceInt      ndim,
*       SpiceInt    * iorder  )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* arrlen     I   String length.
* array      I   Input array.
* ndim       I   Dimension of array.
* iorder     O   Order vector for array.
***********************************************************************/

%rename (orderc) my_orderc_c;
%apply (void RETURN_VOID) {void my_orderc_c};
%apply (SpiceInt DIM1, SpiceInt DIM2, ConstSpiceChar *IN_STRINGS)
                {(SpiceInt ndim, SpiceInt arrlen, ConstSpiceChar *array)};
%apply (SpiceInt *SIZE1, SpiceInt **OUT_ARRAY1) {(SpiceInt *n, SpiceInt **iorder)};

%inline %{
    void my_orderc_c(
        SpiceInt ndim, SpiceInt arrlen, ConstSpiceChar *array,
        SpiceInt *n,   SpiceInt **iorder)
    {
        *n = ndim;
        *iorder = my_int_malloc(ndim, "orderc");
        if (*iorder) {
            orderc_c(arrlen, array, ndim, *iorder);
        }
    }
%}

/***********************************************************************
* -Procedure orderd_c ( Order of a double precision array )
*
* -Abstract
*
* Determine the order of elements in a floating-point array.
*
* void orderd_c (
*       ConstSpiceDouble  * array,
*       SpiceInt            ndim,
*       SpiceInt          * iorder )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* array      I   Input array.
* ndim       I   Dimension of array.
* iorder     O   Order vector for array.
***********************************************************************/

%rename (orderd) my_orderd_c;
%apply (void RETURN_VOID) {void my_orderd_c};
%apply (ConstSpiceDouble *IN_ARRAY1, SpiceInt DIM1)
                {(ConstSpiceDouble *array, SpiceInt ndim)};
%apply (SpiceInt *SIZE1, SpiceInt **OUT_ARRAY1)
                {(SpiceInt *n, SpiceInt **iorder)};

%inline %{
    void my_orderd_c(
        ConstSpiceDouble *array,
        SpiceInt         ndim,
        SpiceInt         *n, SpiceInt **iorder)
    {
        *n = ndim;
        *iorder = my_int_malloc(ndim, "orderd");
        if (*iorder) {
            orderd_c(array, ndim, *iorder);
        }
    }
%}

/***********************************************************************
* -Procedure orderi_c ( Order of an integer array )
*
* -Abstract
*
* Determine the order of elements in an integer array.
*
* void orderi_c (
*       ConstSpiceInt  * array,
*       SpiceInt         ndim,
*       SpiceInt       * iorder )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* array      I    Input array.
* ndim       I    Dimension of array.
* iorder     O    Order vector for array.
***********************************************************************/

%rename (orderi) my_orderi_c;
%apply (void RETURN_VOID) {void my_orderi_c};
%apply (ConstSpiceInt *IN_ARRAY1, SpiceInt DIM1)
                {(ConstSpiceInt *array, SpiceInt ndim)};
%apply (SpiceInt *SIZE1, SpiceInt **OUT_ARRAY1) {(SpiceInt *n, SpiceInt **iorder)};

%inline %{
    void my_orderi_c(
        ConstSpiceInt *array, SpiceInt ndim,
        SpiceInt      *n,     SpiceInt **iorder)
    {
        *n = ndim;
        *iorder = my_int_malloc(ndim, "orderi");
        if (*iorder) {
            orderi_c(array, ndim, *iorder);
        };
    }
%}

/***********************************************************************
* -Procedure pckcls_c ( PCK, close file )
*
* -Abstract
*
* Close an open PCK file.
*
* void pckcls_c (
*       SpiceInt handle )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* handle     I   Handle of the PCK file to be closed.
***********************************************************************/

%rename (pckcls) pckcls_c;
%apply (void RETURN_VOID) {void pckcls_c};

extern void pckcls_c(
        SpiceInt handle
);

/***********************************************************************
* -Procedure pcklof_c ( PCK, load binary file )
*
* -Abstract
*
* Load a binary PCK file for use by the readers. Return the
* handle of the loaded file which is used by other PCK routines to
* refer to the file.
*
* void pcklof_c (
*       ConstSpiceChar * fname,
*       SpiceInt       * handle )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* fname      I   Name of the file to be loaded.
* handle     O   Loaded file's handle.
***********************************************************************/

%rename (pcklof) pcklof_c;
%apply (void RETURN_VOID) {void pcklof_c};

extern void pcklof_c(
        ConstSpiceChar *CONST_STRING,
        SpiceInt       *OUTPUT
);

/***********************************************************************
* -Procedure pckopn_c ( PCK, open new file )
*
* -Abstract
*
* Create a new PCK file, returning the handle of the opened file.
*
* void pckopn_c (
*       ConstSpiceChar   * name,
*       ConstSpiceChar   * ifname,
*       SpiceInt           ncomch,
*       SpiceInt         * handle  )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* name       I   The name of the PCK file to be opened.
* ifname     I   The internal filename for the PCK.
* ncomch     I   The number of characters to reserve for comments.
* handle     O   The handle of the opened PCK file.
***********************************************************************/

%rename (pckopn) pckopn_c;
%apply (void RETURN_VOID) {void pckopn_c};

extern void pckopn_c(
        ConstSpiceChar *CONST_STRING,
        ConstSpiceChar *CONST_STRING,
        SpiceInt       ncomch,
        SpiceInt       *OUTPUT
);

/***********************************************************************
* -Procedure pckuof_c ( PCK, unload binary file )
*
* -Abstract
*
* Unload a binary PCK file so that it will no longer be searched by
* the readers.
*
* void pckuof_c (
*       SpiceInt handle )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* handle     I   Handle of file to be unloaded
***********************************************************************/

%rename (pckuof) pckuof_c;
%apply (void RETURN_VOID) {void pckuof_c};

extern void pckuof_c(
        SpiceInt handle
);

/***********************************************************************
* -Procedure pckw02_c ( PCK, write type 2 segment )
*
* -Abstract
*
* Write a type 2 segment to a PCK binary file given the file handle,
* frame class ID, base frame, time range covered by the segment, and
* the Chebyshev polynomial coefficients.
*
* void pckw02_c (
*       SpiceInt           handle,
*       SpiceInt           clssid,
*       ConstSpiceChar   * frame,
*       SpiceDouble        first,
*       SpiceDouble        last,
*       ConstSpiceChar   * segid,
*       SpiceDouble        intlen,
*       SpiceInt           n,
*       SpiceInt           polydg,
*       SpiceDouble        cdata[],
*       SpiceDouble        btime      )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* handle     I   Handle of binary PCK file open for writing.
* clssid     I   Frame class ID of body-fixed frame.
* frame      I   Name of base reference frame.
* first      I   Start time of interval covered by segment.
* last       I   End time of interval covered by segment.
* segid      I   Segment identifier.
* intlen     I   Length of time covered by logical record.
* n          I   Number of logical records in segment.
* polydg     I   Chebyshev polynomial degree.
* cdata      I   Array of Chebyshev coefficients.
* btime      I   Begin time of first logical record.
***********************************************************************/

%rename (pckw02) pckw02_c;
%apply (void RETURN_VOID) {void pckw02_c};

extern void pckw02_c(
        SpiceInt       handle,
        SpiceInt       clssid,
        ConstSpiceChar *CONST_STRING,
        SpiceDouble    first,
        SpiceDouble    last,
        ConstSpiceChar *CONST_STRING,
        SpiceDouble    intlen,
        SpiceInt       n,
        SpiceInt       polydg,
        SpiceDouble    *IN_ARRAY1,
        SpiceDouble    btime
);

/***********************************************************************
* -Procedure pltnrm_c ( DSK, compute outward normal of plate )
*
* -Abstract
*
* Compute an outward normal vector of a triangular plate.
* The vector does not necessarily have unit length.
*
* void pltnrm_c (
*       ConstSpiceDouble    v1[3],
*       ConstSpiceDouble    v2[3],
*       ConstSpiceDouble    v3[3],
*       SpiceDouble         normal[3] )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* v1         I   First vertex of a plate.
* v2         I   Second vertex of a plate.
* v3         I   Third vertex of a plate.
* normal     O   Plate's outward normal vector.
***********************************************************************/

%rename (pltnrm) pltnrm_c;
%apply (void RETURN_VOID) {void pltnrm_c};
%apply (ConstSpiceDouble IN_ARRAY1[ANY]) {ConstSpiceDouble v1[3]};
%apply (ConstSpiceDouble IN_ARRAY1[ANY]) {ConstSpiceDouble v2[3]};
%apply (ConstSpiceDouble IN_ARRAY1[ANY]) {ConstSpiceDouble v3[3]};
%apply (SpiceDouble OUT_ARRAY1[ANY]) {SpiceDouble normal[3]};

extern void pltnrm_c(
        ConstSpiceDouble v1[3],
        ConstSpiceDouble v2[3],
        ConstSpiceDouble v3[3],
        SpiceDouble      normal[3]
);

//Vector version
VECTORIZE_dX_dX_dX__dN(pltnrm, pltnrm_c, 3)

/***********************************************************************
* -Procedure polyds_c ( Compute a Polynomial and its Derivatives )
*
* -Abstract
*
* Compute the value of a polynomial and its first
* `nderiv' derivatives at the value `t'.
*
* void polyds_c (
*       ConstSpiceDouble    * coeffs,
*       SpiceInt              deg,
*       SpiceInt              nderiv,
*       SpiceDouble           t,
*       SpiceDouble         * p )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* coeffs     I   Coefficients of the polynomial to be evaluated.
* deg        I   Degree of the polynomial to be evaluated.
* nderiv     I   Number of derivatives to compute.
* t          I   Point to evaluate the polynomial and derivatives
* p          O   Value of polynomial and derivatives.
***********************************************************************/

%rename (polyds) my_polyds_c;
%apply (void RETURN_VOID) {void my_polyds_c};
%apply (SpiceInt DIM1, ConstSpiceDouble *IN_ARRAY1)
                {(SpiceInt deg_plus_1, ConstSpiceDouble *coeffs)};
%apply (SpiceInt *SIZE1, SpiceDouble OUT_ARRAY1[ANY])
                {(SpiceInt *nderiv_plus_1, SpiceDouble p[10])};

// Copied from vectorize.i
%apply (ConstSpiceDouble *IN_ARRAY12, SpiceInt DIM1, SpiceInt DIM2)
                {(ConstSpiceDouble *in21, SpiceInt in21_dim1, SpiceInt in21_dim2)};
%apply (ConstSpiceDouble *IN_ARRAY01, SpiceInt DIM1)
                {(ConstSpiceDouble *in12, SpiceInt in12_dim1)};
%apply (SpiceDouble **OUT_ARRAY12, SpiceInt *SIZE1, SpiceInt *SIZE2)
                {(SpiceDouble **out21, SpiceInt *out21_dim1, SpiceInt *out21_dim2)};

%inline %{
    void my_polyds_c(
        SpiceInt deg_plus_1, ConstSpiceDouble *coeffs,
        SpiceInt nderiv,
        SpiceDouble t,
        SpiceInt *nderiv_plus_1, SpiceDouble p[10])
    {
        polyds_c(coeffs, deg_plus_1 - 1, nderiv, t, p);
        *nderiv_plus_1 = nderiv + 1;
    }

    // This function doesn't fit any of our vectorization templates, because
    // the rightmost dimension of the returned axis is variable.

    void polyds_vector(
        ConstSpiceDouble *in21, SpiceInt in21_dim1, SpiceInt in21_dim2,
        SpiceInt nderiv,
        ConstSpiceDouble *in12, SpiceInt in12_dim1,
        SpiceDouble **out21, SpiceInt *out21_dim1, SpiceInt *out21_dim2)
    {
        char *my_name = "polyds_vector";

        // in21 is coeffs
        // in12 is t
        // out21 is p

        int deg = in21_dim1 - 1;
        int nderiv_plus_1 = nderiv + 1;

         int maxdim = in21_dim1;
        if (maxdim < in12_dim1) maxdim = in12_dim1;

        int size = (maxdim == 0 ? 1 : maxdim);
        in21_dim1 = (in21_dim1 == 0 ? 1 : in21_dim1);
        in12_dim1 = (in12_dim1 == 0 ? 1 : in12_dim1);

        *out21_dim1 = maxdim;
        *out21_dim2 = nderiv_plus_1;
        *out21 = my_malloc(size * nderiv_plus_1, my_name);

        if (*out21) {
            for (int i = 0; i < size; i++) {
                polyds_c(
                    in21 + (i % in21_dim1) * in21_dim2,
                    deg, nderiv,
                    in12[i % in12_dim1],
                    *out21 + i * nderiv_plus_1
                );
            }
        }
    }
%}

/***********************************************************************
* -Procedure pos_c ( Position of substring )
*
* -Abstract
*
* Find the first occurrence in a string of a substring, starting at
* a specified location, searching forward.
*
* SpiceInt pos_c (
*       ConstSpiceChar     * str,
*       ConstSpiceChar    * substr,
*       SpiceInt            start  )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* str        I   Any character string.
* substr     I   Substring to locate in the character string.
* start      I   Position to begin looking for substr in str.
* index      R   Index of substring in string.
***********************************************************************/

%rename (pos) pos_c;
%apply (SpiceInt RETURN_INT) {SpiceInt pos_c};

extern SpiceInt pos_c(
        ConstSpiceChar *CONST_STRING,
        ConstSpiceChar *CONST_STRING,
        SpiceInt       start
);

/***********************************************************************
* -Procedure posr_c ( Position of substring, reverse search )
*
* -Abstract
*
* Find the first occurrence in a string of a substring, starting at
* a specified location, searching backward.
*
* SpiceInt posr_c (
*       ConstSpiceChar    * str,
*       ConstSpiceChar    * substr,
*       SpiceInt            start  )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* str        I   Any character string.
* substr     I   Substring to locate in the character string.
* start      I   Position to begin looking for substr in str.
* index      R   Index of substring in string.
***********************************************************************/

%rename (posr) posr_c;
%apply (SpiceInt RETURN_INT) {SpiceInt posr_c};

extern SpiceInt posr_c(
        ConstSpiceChar *CONST_STRING,
        ConstSpiceChar *CONST_STRING,
        SpiceInt       start
);

/***********************************************************************
* -Procedure prompt_c ( Prompt a user for a string )
*
* -Abstract
*
* Prompt a user for keyboard input.
*
* SpiceChar * prompt_c (
*       ConstSpiceChar * dspmsg,
*       SpiceInt         buflen,
*       SpiceChar      * buffer )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* dspmsg     I   The prompt string to display when asking for input.
* buflen     I   Minimum number of characters for response plus one.
* buffer     O   The string containing the response typed by a user.
***********************************************************************/

%rename (prompt) prompt_c;
%apply (SpiceChar *RETURN_STRING) {SpiceChar* prompt_c};
%apply (SpiceInt DIM1, SpiceChar OUT_STRING[ANY])
                {(SpiceInt buflen, SpiceChar buffer[MESSAGELEN])};

extern SpiceChar* prompt_c(
        ConstSpiceChar *CONST_STRING,
        SpiceInt       buflen, SpiceChar buffer[MESSAGELEN]
);

/***********************************************************************
* -Procedure prsdp_c   ( Parse d.p. number with error checking )
*
* -Abstract
*
* Parse a string as a floating-point number, encapsulating error
* handling.
*
* void prsdp_c (
*       ConstSpiceChar     * string,
*       SpiceDouble        * dpval  )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* string     I   String representing a numeric value.
* dpval      O   D.p. value obtained by parsing `string'.
***********************************************************************/

%rename (prsdp) prsdp_c;
%apply (void RETURN_VOID) {void prsdp_c};
%apply (ConstSpiceChar *CONST_STRING) {ConstSpiceChar *string};

extern void prsdp_c(
        ConstSpiceChar *CONST_STRING,
        SpiceDouble    *OUTPUT
);

/***********************************************************************
* -Procedure prsint_c   ( Parse integer with error checking )
*
* -Abstract
*
* Parse a string as an integer, encapsulating error handling.
*
* void prsint_c (
*       ConstSpiceChar  * string,
*       SpiceInt        * intval )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* string     I   String representing a numeric value.
* intval     O   Integer value obtained by parsing `string'.
***********************************************************************/

%rename (prsint) prsint_c;
%apply (void RETURN_VOID) {void prsint_c};
%apply (ConstSpiceChar *CONST_STRING) {ConstSpiceChar *string};

extern void prsint_c(
        ConstSpiceChar *CONST_STRING,
        SpiceInt       *OUTPUT
);

/***********************************************************************
* -Procedure qderiv_c ( Quadratic derivative )
*
* -Abstract
*
* Estimate the derivative of a function by finding the derivative
* of a quadratic approximating function. This derivative estimate
* is equivalent to that found by computing the average of forward
* and backward differences.
*
* void qderiv_c (
*       SpiceInt            ndim,
*       ConstSpiceDouble    f0[],
*       ConstSpiceDouble    f2[],
*       SpiceDouble         delta,
*       SpiceDouble         dfdt[] )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* ndim       I   Dimension of function to be differentiated.
* f0         I   Function values at left endpoint.
* f2         I   Function values at right endpoint.
* delta      I   Separation of abscissa points.
* dfdt       O   Derivative vector.
***********************************************************************/

%rename (qderiv) my_qderiv_c;
%apply (void RETURN_VOID) {void my_qderiv_c};
%apply (SpiceInt DIM1, ConstSpiceDouble *IN_ARRAY1)
            {(SpiceInt ndim, ConstSpiceDouble *f0)};
%apply (SpiceInt DIM1, ConstSpiceDouble *IN_ARRAY1)
            {(SpiceInt ndim1, ConstSpiceDouble *f2)};
%apply (SpiceInt *SIZE1, SpiceDouble **OUT_ARRAY1)
            {(SpiceInt *ndim2, SpiceDouble **dfdt)};

%inline %{
    void my_qderiv_c(
        SpiceInt    ndim, ConstSpiceDouble *f0,
        SpiceInt    ndim1, ConstSpiceDouble *f2,
        SpiceDouble delta,
        SpiceInt    *ndim2, SpiceDouble **dfdt)
    {
        if (!my_assert_eq(ndim, ndim1, "qderiv",
            "Array dimension mismatch in qderiv: "
            "f0 dimension = #; f2 dimension = #")) return;

        *ndim2 = ndim;
        *dfdt = my_malloc(ndim, "qderiv");
        if (*dfdt) {
            qderiv_c(ndim, f0, f2, delta, *dfdt);
        }
    }
%}

//Vector version not needed--it already handles vectors

/***********************************************************************
* -Procedure recazl_c ( Rectangular coordinates to AZ/EL )
*
* -Abstract
*
* Convert rectangular coordinates of a point to range, azimuth and
* elevation.
*
* void recazl_c (
*       ConstSpiceDouble    rectan[3],
*       SpiceBoolean        azccw,
*       SpiceBoolean        elplsz,
*       SpiceDouble       * range,
*       SpiceDouble       * az,
*       SpiceDouble       * el         )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* rectan     I   Rectangular coordinates of a point.
* azccw      I   Flag indicating how azimuth is measured, True for counterclockwise, False for clockwise.
* elplsz     I   Flag indicating how elevation is measured, True for increasing toward +Z, False for -Z.
* range      O   Distance of the point from the origin.
* az         O   Azimuth in radians.
* el         O   Elevation in radians.
***********************************************************************/

%rename (recazl) recazl_c;
%apply (void RETURN_VOID) {void recazl_c};
%apply (ConstSpiceDouble IN_ARRAY1[ANY]) {ConstSpiceDouble rectan[3]};

extern void recazl_c(
        ConstSpiceDouble rectan[3],
        SpiceBoolean     azccw,
        SpiceBoolean     elplsz,
        SpiceDouble      *OUTPUT,
        SpiceDouble      *OUTPUT,
        SpiceDouble      *OUTPUT
);

//Vector version
VECTORIZE_dX_2d__3d(recazl, recazl_c)

/***********************************************************************
* -Procedure reordc_c ( Reorder a character array )
*
* -Abstract
*
* Reorder the elements of an array of character strings according to
* a given order vector.
*
* void reordc_c (
*       ConstSpiceInt  * iorder,
*       SpiceInt         ndim,
*       SpiceInt         arrlen,
*       void             array[][]    )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* iorder     I   Order vector to be used to re-order array.
* ndim       I   Dimension of array.
* arrlen     I   String length.
* array     I-O  Array to be re-ordered.
***********************************************************************/

%rename (reordc) reordc_c;
%apply (void RETURN_VOID) {void reordc_c};
%apply (ConstSpiceInt *IN_ARRAY1) {ConstSpiceInt *iorder};
%apply (SpiceInt DIM1, SpiceInt DIM2, SpiceChar *INOUT_STRINGS)
                {(SpiceInt ndim, SpiceInt arrlen, SpiceChar *array)};

extern void reordc_c(
        ConstSpiceInt *iorder,
        SpiceInt      ndim, SpiceInt arrlen, SpiceChar *array
);

/***********************************************************************
* -Procedure reordd_c ( Reorder a double precision array )
*
* -Abstract
*
* Reorder the elements of a floating-point array according to a
* given order vector.
*
* void reordd_c (
*       ConstSpiceInt      * iorder,
*       SpiceInt             ndim,
*       SpiceDouble        * array  )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* iorder     I   Order vector to be used to re-order array.
* ndim       I   Dimension of array.
* array     I-O  Array to be re-ordered.
***********************************************************************/

%rename (reordd) reordd_c;
%apply (void RETURN_VOID) {void reordd_c};
%apply (ConstSpiceInt *IN_ARRAY1) {ConstSpiceInt *iorder};
%apply (SpiceInt DIM1, SpiceDouble *INOUT_ARRAY1)
                {(SpiceInt ndim, SpiceDouble *array)};

extern void reordd_c(
        ConstSpiceInt *iorder,
        SpiceInt      ndim, SpiceDouble *array
);

/***********************************************************************
* -Procedure reordi_c ( Reorder an integer array )
*
* -Abstract
*
* Reorder the elements of an integer array according to a given
* order vector.
*
* void reordi_c (
*       ConstSpiceInt   * iorder,
*       SpiceInt          ndim,
*       SpiceInt        * array )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* iorder     I   Order vector to be used to re-order array.
* ndim       I   Dimension of array.
* array     I-O  Array to be re-ordered.
***********************************************************************/

%rename (reordi) reordi_c;
%apply (void RETURN_VOID) {void reordi_c};
%apply (ConstSpiceInt *IN_ARRAY1) {ConstSpiceInt *iorder};
%apply (SpiceInt DIM1, SpiceInt *INOUT_ARRAY1)
                {(SpiceInt ndim, SpiceInt *array)};

extern void reordi_c(
        ConstSpiceInt *iorder,
        SpiceInt      ndim, SpiceInt *array
);

/***********************************************************************
* -Procedure reordl_c ( Reorder a logical array )
*
* -Abstract
*
* Reorder the elements of a logical array according to a given order
* vector.
*
* void reordl_c (
*       ConstSpiceInt   * iorder,
*       SpiceInt          ndim,
*       SpiceBoolean    * array )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* iorder     I   Order vector to be used to re-order array.
* ndim       I   Dimension of array.
* array     I-O  Array to be re-ordered.
***********************************************************************/

%rename (reordl) reordl_c;
%apply (void RETURN_VOID) {void reordl_c};
%apply (ConstSpiceInt *IN_ARRAY1) {ConstSpiceInt *iorder};
%apply (SpiceInt DIM1, SpiceBoolean *INOUT_ARRAY1)
                {(SpiceInt ndim, SpiceBoolean *array)};

extern void reordl_c(
        ConstSpiceInt *iorder,
        SpiceInt      ndim, SpiceBoolean *array
);

/***********************************************************************
* -Procedure repml_c ( Replace marker with logical value text )
*
* -Abstract
*
* Replace a marker with the text representation of a logical value.
*
* void repml_c (
*       ConstSpiceChar    * in,
*       ConstSpiceChar    * marker,
*       SpiceBoolean        value,
*       SpiceChar           rtcase,
*       SpiceInt            outlen,
*       SpiceChar         * out    )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* in         I   Input string.
* marker     I   Marker to be replaced.
* value      I   Replacement logical value.
* rtcase     I   Case of replacement text.
* outlen     I   Maximum length of output string `out'.
* out        O   Output string.
***********************************************************************/

%rename (repml) repml_c;
%apply (void RETURN_VOID) {void repml_c};
%apply (SpiceInt DIM1, SpiceChar OUT_STRING[ANY])
                {(SpiceInt outlen, SpiceChar out[MESSAGELEN])};

extern void repml_c(
        ConstSpiceChar   *CONST_STRING,
        ConstSpiceChar   *CONST_STRING,
        SpiceBoolean     value,
        SpiceChar        IN_STRING,
        SpiceInt         outlen, SpiceChar out[MESSAGELEN]
);

/***********************************************************************
* -Procedure return_c ( Immediate Return Indicator )
*
* -Abstract
*
* Return True if CSPICE routines should return immediately upon
* entry.
*
* SpiceBoolean return_c (
*       void )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* status     R   True if the routine should return immediately.
***********************************************************************/

%rename (return_) return_c;
%apply (SpiceBoolean RETURN_BOOLEAN) {SpiceBoolean return_c};

extern SpiceBoolean return_c(void);

/***********************************************************************
* -Procedure shellc_c ( Shell sort a character array )
*
* -Abstract
*
* Sort an array of character strings according to the ASCII
* collating sequence using the Shell Sort algorithm.
*
* void shellc_c (
*       SpiceInt     ndim,
*       SpiceInt     arrlen,
*       void         array[][]   )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* ndim       I   Dimension of the array.
* arrlen     I   String length.
* array     I-O  The array.
***********************************************************************/

%rename (shellc) shellc_c;
%apply (void RETURN_VOID) {void shellc_c};
%apply (SpiceInt DIM1, SpiceInt DIM2, SpiceChar *INOUT_STRINGS)
                {(SpiceInt ndim, SpiceInt arrlen, SpiceChar *array)};

extern void shellc_c(
        SpiceInt ndim, SpiceInt arrlen, SpiceChar *array
);

/***********************************************************************
* -Procedure shelld_c ( Shell sort a double precision array )
*
* -Abstract
*
* Sort a floating-point array using the Shell Sort algorithm.
*
* void shelld_c (
*       SpiceInt       ndim,
*       SpiceDouble  * array )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* ndim       I   Dimension of the array.
* array     I-O  The array to be sorted.
***********************************************************************/

%rename (shelld) shelld_c;
%apply (void RETURN_VOID) {void shelld_c};
%apply (SpiceInt DIM1, SpiceDouble *INOUT_ARRAY1)
                {(SpiceInt ndim, SpiceDouble *array)};

extern void shelld_c(
        SpiceInt ndim, SpiceDouble *array
);

/***********************************************************************
* -Procedure shelli_c ( Shell sort an integer array )
*
* -Abstract
*
* Sort an integer array using the Shell Sort algorithm.
*
* void shelli_c (
*       SpiceInt     ndim,
*       SpiceInt   * array )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* ndim       I   Dimension of the array.
* array     I-O  The array.
***********************************************************************/

%rename (shelli) shelli_c;
%apply (void RETURN_VOID) {void shelli_c};
%apply (SpiceInt DIM1, SpiceInt *INOUT_ARRAY1)
                {(SpiceInt ndim, SpiceInt *array)};

extern void shelli_c(
        SpiceInt ndim, SpiceInt *array
);

/***********************************************************************
* -Procedure spk14a_c ( SPK, add data to a type 14 segment )
*
* -Abstract
*
* Add data to a type 14 SPK segment associated with `handle'.
*
* void spk14a_c (
*       SpiceInt           handle,
*       SpiceInt           ncsets,
*       ConstSpiceDouble   coeffs[],
*       ConstSpiceDouble   epochs[]  )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* handle     I   The handle of an SPK file open for writing.
* ncsets     I   The number of coefficient sets and epochs.
* coeffs     I   The collection of coefficient sets.
* epochs     I   The epochs associated with the coefficient sets.
***********************************************************************/

%rename (spk14a) spk14a_c;
%apply (void RETURN_VOID) {void spk14a_c};

extern void spk14a_c(
        SpiceInt  handle,
        SpiceInt  ncsets,
        ConstSpiceDouble *IN_ARRAY1,
        ConstSpiceDouble *IN_ARRAY1
);

/***********************************************************************
* -Procedure spk14b_c ( SPK, begin a type 14 segment )
*
* -Abstract
*
* Begin a type 14 SPK segment in the SPK file associated with
* `handle'.
*
* void spk14b_c (
*       SpiceInt           handle,
*       ConstSpiceChar   * segid,
*       SpiceInt           body,
*       SpiceInt           center,
*       ConstSpiceChar   * frame,
*       SpiceDouble        first,
*       SpiceDouble        last,
*       SpiceInt           chbdeg  )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* handle     I   The handle of an SPK file open for writing.
* segid      I   The string to use for segment identifier.
* body       I   The NAIF ID code for the body of the segment.
* center     I   The center of motion for body.
* frame      I   The reference frame for this segment.
* first      I   The first epoch for which the segment is valid.
* last       I   The last epoch for which the segment is valid.
* chbdeg     I   The degree of the Chebyshev Polynomial used.
***********************************************************************/

%rename (spk14b) spk14b_c;
%apply (void RETURN_VOID) {void spk14b_c};

extern void spk14b_c(
        SpiceInt       handle,
        ConstSpiceChar *CONST_STRING,
        SpiceInt       body,
        SpiceInt       center,
        ConstSpiceChar *CONST_STRING,
        SpiceDouble    first,
        SpiceDouble    last,
        SpiceInt       chbdeg
);

/***********************************************************************
* -Procedure spk14e_c ( SPK, end a type 14 segment )
*
* -Abstract
*
* End the type 14 SPK segment currently being written to the SPK
* file associated with `handle'.
*
* void spk14e_c (
*       SpiceInt   handle )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* handle     I   The handle of an SPK file open for writing.
***********************************************************************/

%rename (spk14e) spk14e_c;
%apply (void RETURN_VOID) {void spk14e_c};

extern void spk14e_c(
        SpiceInt handle
);

/***********************************************************************
* -Procedure spkcls_c ( SPK, Close file )
*
* -Abstract
*
* Close an open SPK file.
*
* void spkcls_c (
*       SpiceInt handle )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* handle     I   Handle of the SPK file to be closed.
***********************************************************************/

%rename (spkcls) spkcls_c;
%apply (void RETURN_VOID) {void spkcls_c};

extern void spkcls_c(
        SpiceInt handle
);

/***********************************************************************
* -Procedure spkcpo_c ( SPK, constant position observer state )
*
* -Abstract
*
* Return the state of a specified target relative to an "observer,"
* where the observer has constant position in a specified reference
* frame. The observer's position is provided by the calling program
* rather than by loaded SPK files.
*
* void spkcpo_c (
*       ConstSpiceChar       * target,
*       SpiceDouble            et,
*       ConstSpiceChar       * outref,
*       ConstSpiceChar       * refloc,
*       ConstSpiceChar       * abcorr,
*       ConstSpiceDouble       obspos[3],
*       ConstSpiceChar       * obsctr,
*       ConstSpiceChar       * obsref,
*       SpiceDouble            state[6],
*       SpiceDouble          * lt         )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* target     I   Name of target ephemeris object.
* et         I   Observation epoch.
* outref     I   Reference frame of output state.
* refloc     I   Output reference frame evaluation locus.
* abcorr     I   Aberration correction.
* obspos     I   Observer position relative to center of motion.
* obsctr     I   Center of motion of observer.
* obsref     I   Frame of observer position.
* state      O   State of target with respect to observer.
* lt         O   One way light time between target and
* observer.
***********************************************************************/

%rename (spkcpo) spkcpo_c;
%apply (void RETURN_VOID) {void spkcpo_c};
%apply (ConstSpiceDouble IN_ARRAY1[ANY]) {ConstSpiceDouble obspos[3]};
%apply (SpiceDouble OUT_ARRAY1[ANY]) {SpiceDouble state[6]};

extern void spkcpo_c(
        ConstSpiceChar   *CONST_STRING,
        SpiceDouble      et,
        ConstSpiceChar   *CONST_STRING,
        ConstSpiceChar   *CONST_STRING,
        ConstSpiceChar   *CONST_STRING,
        ConstSpiceDouble obspos[3],
        ConstSpiceChar   *CONST_STRING,
        ConstSpiceChar   *CONST_STRING,
        SpiceDouble      state[6],
        SpiceDouble      *OUTPUT
);

//Vector version
VECTORIZE_s_d_3s_dX_2s__dN_d(spkcpo, spkcpo_c, 6)

/***********************************************************************
* -Procedure spkcpt_c ( SPK, constant position target state )
*
* -Abstract
*
* Return the state, relative to a specified observer, of a target
* having constant position in a specified reference frame. The
* target's position is provided by the calling program rather than
* by loaded SPK files.
*
* void spkcpt_c (
*       ConstSpiceDouble       trgpos[3],
*       ConstSpiceChar       * trgctr,
*       ConstSpiceChar       * trgref,
*       SpiceDouble            et,
*       ConstSpiceChar       * outref,
*       ConstSpiceChar       * refloc,
*       ConstSpiceChar       * abcorr,
*       ConstSpiceChar       * obsrvr,
*       SpiceDouble            state[6],
*       SpiceDouble          * lt          )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* trgpos     I   Target position relative to center of motion.
* trgctr     I   Center of motion of target.
* trgref     I   Frame of target position.
* et         I   Observation epoch.
* outref     I   Reference frame of output state.
* refloc     I   Output reference frame evaluation locus.
* abcorr     I   Aberration correction.
* obsrvr     I   Name of observing ephemeris object.
* state      O   State of target with respect to observer.
* lt         O   One way light time between target and
* observer.
***********************************************************************/

%rename (spkcpt) spkcpt_c;
%apply (void RETURN_VOID) {void spkcpt_c};
%apply (ConstSpiceDouble IN_ARRAY1[ANY]) {ConstSpiceDouble trgpos[3]};
%apply (SpiceDouble OUT_ARRAY1[ANY]) {SpiceDouble state[6]};

extern void spkcpt_c(
        ConstSpiceDouble trgpos[3],
        ConstSpiceChar   *CONST_STRING,
        ConstSpiceChar   *CONST_STRING,
        SpiceDouble      et,
        ConstSpiceChar   *CONST_STRING,
        ConstSpiceChar   *CONST_STRING,
        ConstSpiceChar   *CONST_STRING,
        ConstSpiceChar   *CONST_STRING,
        SpiceDouble      state[6],
        SpiceDouble      *OUTPUT
);

//Vector version
VECTORIZE_dX_2s_d_4s__dN_d(spkcpt, spkcpt_c, 6)

/***********************************************************************
* -Procedure spkcvo_c ( SPK, constant velocity observer state )
*
* -Abstract
*
* Return the state of a specified target relative to an "observer,"
* where the observer has constant velocity in a specified reference
* frame. The observer's state is provided by the calling program
* rather than by loaded SPK files.
*
* void spkcvo_c (
*       ConstSpiceChar       * target,
*       SpiceDouble            et,
*       ConstSpiceChar       * outref,
*       ConstSpiceChar       * refloc,
*       ConstSpiceChar       * abcorr,
*       ConstSpiceDouble       obssta[6],
*       SpiceDouble            obsepc,
*       ConstSpiceChar       * obsctr,
*       ConstSpiceChar       * obsref,
*       SpiceDouble            state[6],
*       SpiceDouble          * lt         )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* target     I   Name of target ephemeris object.
* et         I   Observation epoch.
* outref     I   Reference frame of output state.
* refloc     I   Output reference frame evaluation locus.
* abcorr     I   Aberration correction.
* obssta     I   Observer state relative to center of motion.
* obsepc     I   Epoch of observer state.
* obsctr     I   Center of motion of observer.
* obsref     I   Frame of observer state.
* state      O   State of target with respect to observer.
* lt         O   One way light time between target and
* observer.
***********************************************************************/

%rename (spkcvo) spkcvo_c;
%apply (void RETURN_VOID) {void spkcvo_c};
%apply (ConstSpiceDouble IN_ARRAY1[ANY]) {ConstSpiceDouble obssta[6]};
%apply (SpiceDouble OUT_ARRAY1[ANY]) {SpiceDouble state[6]};

extern void spkcvo_c(
        ConstSpiceChar   *CONST_STRING,
        SpiceDouble      et,
        ConstSpiceChar   *CONST_STRING,
        ConstSpiceChar   *CONST_STRING,
        ConstSpiceChar   *CONST_STRING,
        ConstSpiceDouble obssta[6],
        SpiceDouble      obsepc,
        ConstSpiceChar   *CONST_STRING,
        ConstSpiceChar   *CONST_STRING,
        SpiceDouble      state[6],
        SpiceDouble      *OUTPUT
);

//Vector version
VECTORIZE_s_d_3s_dX_d_2s__dN_d(spkcvo, spkcvo_c, 6)

/***********************************************************************
* -Procedure spkcvt_c ( SPK, constant velocity target state )
*
* -Abstract
*
* Return the state, relative to a specified observer, of a target
* having constant velocity in a specified reference frame. The
* target's state is provided by the calling program rather than by
* loaded SPK files.
*
* void spkcvt_c (
*       ConstSpiceDouble       trgsta[6],
*       SpiceDouble            trgepc,
*       ConstSpiceChar       * trgctr,
*       ConstSpiceChar       * trgref,
*       SpiceDouble            et,
*       ConstSpiceChar       * outref,
*       ConstSpiceChar       * refloc,
*       ConstSpiceChar       * abcorr,
*       ConstSpiceChar       * obsrvr,
*       SpiceDouble            state[6],
*       SpiceDouble          * lt         )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* trgsta     I   Target state relative to center of motion.
* trgepc     I   Epoch of target state.
* trgctr     I   Center of motion of target.
* trgref     I   Frame of target state.
* et         I   Observation epoch.
* outref     I   Reference frame of output state.
* refloc     I   Output reference frame evaluation locus.
* abcorr     I   Aberration correction.
* obsrvr     I   Name of observing ephemeris object.
* state      O   State of target with respect to observer.
* lt         O   One way light time between target and
* observer.
***********************************************************************/

%rename (spkcvt) spkcvt_c;
%apply (void RETURN_VOID) {void spkcvt_c};
%apply (ConstSpiceDouble IN_ARRAY1[ANY]) {ConstSpiceDouble trgsta[6]};
%apply (SpiceDouble OUT_ARRAY1[ANY]) {SpiceDouble state[6]};

extern void spkcvt_c(
        ConstSpiceDouble trgsta[6],
        SpiceDouble      trgepc,
        ConstSpiceChar   *CONST_STRING,
        ConstSpiceChar   *CONST_STRING,
        SpiceDouble      et,
        ConstSpiceChar   *CONST_STRING,
        ConstSpiceChar   *CONST_STRING,
        ConstSpiceChar   *CONST_STRING,
        ConstSpiceChar   *CONST_STRING,
        SpiceDouble      state[6],
        SpiceDouble      *OUTPUT
);

//Vector version
VECTORIZE_dX_d_2s_d_4s__dN_d(spkcvt, spkcvt_c, 6)

/***********************************************************************
* -Procedure spklef_c (  S/P Kernel, Load ephemeris file )
*
* -Abstract
*
* Load an ephemeris file for use by the readers. Return that file's
* handle, to be used by other SPK routines to refer to the file.
*
* void spklef_c (
*       ConstSpiceChar * fname,
*       SpiceInt       * handle )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* fname      I   Name of the file to be loaded.
* handle     O   Loaded file's handle.
***********************************************************************/

%rename (spklef) spklef_c;
%apply (void RETURN_VOID) {void spklef_c};

extern void spklef_c(
        ConstSpiceChar *CONST_STRING,
        SpiceInt       *OUTPUT
);

/***********************************************************************
* -Procedure spkopa_c ( SPK open for addition )
*
* -Abstract
*
* Open an existing SPK file for subsequent write.
*
* void spkopa_c (
*       ConstSpiceChar * file,
*       SpiceInt       * handle )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* file       I   The name of an existing SPK file.
* handle     O   Handle attached to the SPK file opened to append.
***********************************************************************/

%rename (spkopa) spkopa_c;
%apply (void RETURN_VOID) {void spkopa_c};

extern void spkopa_c(
        ConstSpiceChar *CONST_STRING,
        SpiceInt       *OUTPUT
);

/***********************************************************************
* -Procedure spkopn_c ( SPK, open new file. )
*
* -Abstract
*
* Create a new SPK file, returning the handle of the opened file.
*
* void spkopn_c (
*       ConstSpiceChar * fname,
*       ConstSpiceChar * ifname,
*       SpiceInt         ncomch,
*       SpiceInt       * handle  )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* fname      I   The name of the new SPK file to be created.
* ifname     I   The internal filename for the SPK file.
* ncomch     I   The number of characters to reserve for comments.
* handle     O   The handle of the opened SPK file.
***********************************************************************/

%rename (spkopn) spkopn_c;
%apply (void RETURN_VOID) {void spkopn_c};

extern void spkopn_c(
        ConstSpiceChar *CONST_STRING,
        ConstSpiceChar *CONST_STRING,
        SpiceInt       ncomch,
        SpiceInt       *OUTPUT
);

/***********************************************************************
* -Procedure spkpds_c ( SPK pack descriptor )
*
* -Abstract
*
* Perform routine error checks and if all check pass, pack the
* descriptor for an SPK segment
*
* void spkpds_c (
*       SpiceInt           body,
*       SpiceInt           center,
*       ConstSpiceChar   * frame,
*       SpiceInt           type,
*       SpiceDouble        first,
*       SpiceDouble        last,
*       SpiceDouble        descr[5] )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* body       I   The NAIF ID code for the body of the segment.
* center     I   The center of motion for body.
* frame      I   The frame for this segment.
* type       I   The type of SPK segment to create.
* first      I   The first epoch for which the segment is valid.
* last       I   The last  epoch for which the segment is valid.
* descr      O   An SPK segment descriptor.
***********************************************************************/

%rename (spkpds) spkpds_c;
%apply (void RETURN_VOID) {void spkpds_c};
%apply (SpiceDouble OUT_ARRAY1[ANY]) {SpiceDouble descr[5]};

extern void spkpds_c(
        SpiceInt       body,
        SpiceInt       center,
        ConstSpiceChar *CONST_STRING,
        SpiceInt       type,
        SpiceDouble    first,
        SpiceDouble    last,
        SpiceDouble    descr[5]
);

/***********************************************************************
* -Procedure spkpvn_c ( S/P Kernel, position and velocity in native frame )
*
* -Abstract
*
* Return, for a specified SPK segment and time, the state (position
* and velocity) of the segment's target body relative to its center
* of motion.
*
* void spkpvn_c (
*       SpiceInt             handle,
*       ConstSpiceDouble     descr[5],
*       SpiceDouble          et,
*       SpiceInt           * ref,
*       SpiceDouble          state[6],
*       SpiceInt           * center    )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* handle     I   File handle.
* descr      I   Segment descriptor.
* et         I   Evaluation epoch.
* ref        O   Segment reference frame ID code.
* state      O   Output state vector.
* center     O   Center of state.
***********************************************************************/

%rename (spkpvn) spkpvn_c;
%apply (void RETURN_VOID) {void spkpvn_c};
%apply (ConstSpiceDouble IN_ARRAY1[ANY]) {ConstSpiceDouble descr[5]};
%apply (SpiceDouble OUT_ARRAY1[ANY]) {SpiceDouble state[6]};

extern void spkpvn_c(
        SpiceInt         handle,
        ConstSpiceDouble descr[5],
        SpiceDouble      et,
        SpiceInt         *OUTPUT,
        SpiceDouble      state[6],
        SpiceInt         *OUTPUT
);

/***********************************************************************
* -Procedure spksfs_c ( S/P Kernel, Select file and segment )
*
* -Abstract
*
* Search through loaded SPK files to find the highest-priority
* segment applicable to the body and time specified and buffer
* searched segments in the process, to attempt to avoid re-reading
* files.
*
* void spksfs_c (
*       SpiceInt        body,
*       SpiceDouble     et,
*       SpiceInt        idlen,
*       SpiceInt      * handle,
*       SpiceDouble     descr[5],
*       SpiceChar     * ident,
*       SpiceBoolean  * found     )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* body       I   Body ID.
* et         I   Ephemeris time.
* idlen      I   Length of output segment ID string.
* handle     O   Handle of file containing the applicable segment.
* descr      O   Descriptor of the applicable segment.
* ident      O   Identifier of the applicable segment.
* found      O   Indicates whether or not a segment was found.
* SIDLEN     P   Maximum length of segment ID.
***********************************************************************/

%rename (spksfs) my_spksfs_c;
%apply (void RETURN_VOID) {void my_spksfs_c};
%apply (SpiceInt *OUTPUT) {SpiceInt *handle};
%apply (SpiceDouble OUT_ARRAY1[ANY]) {SpiceDouble descr[5]};
%apply (SpiceInt DIM1, SpiceChar OUT_STRING[ANY])
      {(SpiceInt idlen, SpiceChar ident[SIDLEN])};
%apply (SpiceBoolean *OUTPUT) {SpiceBoolean *found};

%inline %{
    void my_spksfs_c(
        SpiceInt     body,
        SpiceDouble  et,
        SpiceInt     *handle,
        SpiceDouble  descr[5],
        SpiceInt     idlen, SpiceChar ident[SIDLEN],
        SpiceBoolean *found)
    {
        spksfs_c(body, et, idlen, handle, descr, ident, found);
    }
%}

/***********************************************************************
* -Procedure spksub_c ( S/P Kernel, subset )
*
* -Abstract
*
* Extract a subset of the data in an SPK segment into a
* separate segment.
*
* void spksub_c (
*       SpiceInt            handle,
*       SpiceDouble         descr[5],
*       ConstSpiceChar    * ident,
*       SpiceDouble         begin,
*       SpiceDouble         end,
*       SpiceInt            newh    )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* handle     I   Handle of source segment.
* descr      I   Descriptor of source segment.
* ident      I   Identifier of source segment.
* begin      I   Beginning (initial epoch) of subset.
* end        I   End (final epoch) of subset.
* newh       I   Handle of new segment.
***********************************************************************/

%rename (spksub) spksub_c;
%apply (void RETURN_VOID) {void spksub_c};
%apply (SpiceDouble IN_ARRAY1[ANY]) {SpiceDouble descr[5]};

extern void spksub_c(
        SpiceInt       handle,
        SpiceDouble    descr[5],
        ConstSpiceChar *CONST_STRING,
        SpiceDouble    begin,
        SpiceDouble    end,
        SpiceInt       newh
);

/***********************************************************************
* -Procedure spkuds_c ( SPK - unpack segment descriptor )
*
* -Abstract
*
* Unpack the contents of an SPK segment descriptor.
*
* void spkuds_c (
*       ConstSpiceDouble     descr[5],
*       SpiceInt           * body,
*       SpiceInt           * center,
*       SpiceInt           * frame,
*       SpiceInt           * type,
*       SpiceDouble        * first,
*       SpiceDouble        * last,
*       SpiceInt           * baddrs,
*       SpiceInt           * eaddrs     )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* descr      I   An SPK segment descriptor.
* body       O   The NAIF ID code for the body of the segment.
* center     O   The center of motion for `body'.
* frame      O   The code for the frame of this segment.
* type       O   The type of SPK segment.
* first      O   The first epoch for which the segment is valid.
* last       O   The last  epoch for which the segment is valid.
* baddrs     O   Beginning DAF address of the segment.
* eaddrs     O   Ending DAF address of the segment.
***********************************************************************/

%rename (spkuds) spkuds_c;
%apply (void RETURN_VOID) {void spkuds_c};
%apply (ConstSpiceDouble IN_ARRAY1[ANY]) {ConstSpiceDouble descr[5]};

extern void spkuds_c(
        ConstSpiceDouble descr[5],
        SpiceInt         *OUTPUT,
        SpiceInt         *OUTPUT,
        SpiceInt         *OUTPUT,
        SpiceInt         *OUTPUT,
        SpiceDouble      *OUTPUT,
        SpiceDouble      *OUTPUT,
        SpiceInt         *OUTPUT,
        SpiceInt         *OUTPUT
);

/***********************************************************************
* -Procedure spkuef_c ( SPK Kernel, Unload ephemeris file )
*
* -Abstract
*
* Unload an ephemeris file so that it will no longer be searched by
* the readers.
*
* void spkuef_c (
*       SpiceInt handle )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* handle     I   Handle of file to be unloaded
***********************************************************************/

%rename (spkuef) spkuef_c;
%apply (void RETURN_VOID) {void spkuef_c};

extern void spkuef_c(
        SpiceInt handle
);

/***********************************************************************
* -Procedure spkw02_c ( Write SPK segment, type 2 )
*
* -Abstract
*
* Write a type 2 segment to an SPK file.
*
* void spkw02_c (
*       SpiceInt                handle,
*       SpiceInt                body,
*       SpiceInt                center,
*       ConstSpiceChar        * frame,
*       SpiceDouble             first,
*       SpiceDouble             last,
*       ConstSpiceChar        * segid,
*       SpiceDouble             intlen,
*       SpiceInt                n,
*       SpiceInt                polydg,
*       ConstSpiceDouble        cdata[],
*       SpiceDouble             btime     )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* MAXDEG     P   Maximum degree of Chebyshev expansions.
* TOLSCL     P   Scale factor used to compute time bound tolerance.
* handle     I   Handle of an SPK file open for writing.
* body       I   Body code for ephemeris object.
* center     I   Body code for the center of motion of the body.
* frame      I   The reference frame of the states.
* first      I   First valid time for which states can be computed.
* last       I   Last valid time for which states can be computed.
* segid      I   Segment identifier.
* intlen     I   Length of time covered by logical record.
* n          I   Number of coefficient sets.
* polydg     I   Chebyshev polynomial degree.
* cdata      I   Array of Chebyshev coefficients.
* btime      I   Begin time of first logical record.
***********************************************************************/

%rename (spkw02) spkw02_c;
%apply (void RETURN_VOID) {void spkw02_c};

extern void spkw02_c(
        SpiceInt         handle,
        SpiceInt         body,
        SpiceInt         center,
        ConstSpiceChar   *CONST_STRING,
        SpiceDouble      first,
        SpiceDouble      last,
        ConstSpiceChar   *CONST_STRING,
        SpiceDouble      intlen,
        SpiceInt         n,
        SpiceInt         polydg,
        ConstSpiceDouble *IN_ARRAY1,
        SpiceDouble      btime
);

/***********************************************************************
* -Procedure spkw03_c ( Write SPK segment, type 3 )
*
* -Abstract
*
* Write a type 3 segment to an SPK file.
*
* void spkw03_c (
*       SpiceInt                handle,
*       SpiceInt                body,
*       SpiceInt                center,
*       ConstSpiceChar        * frame,
*       SpiceDouble             first,
*       SpiceDouble             last,
*       ConstSpiceChar        * segid,
*       SpiceDouble             intlen,
*       SpiceInt                n,
*       SpiceInt                polydg,
*       ConstSpiceDouble        cdata[],
*       SpiceDouble             btime     )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* MAXDEG     P   Maximum degree of Chebyshev expansions.
* TOLSCL     P   Scale factor used to compute time bound tolerance.
* handle     I   Handle of SPK file open for writing.
* body       I   NAIF code for ephemeris object.
* center     I   NAIF code for the center of motion of the body.
* frame      I   Reference frame name.
* first      I   Start time of interval covered by segment.
* last       I   End time of interval covered by segment.
* segid      I   Segment identifier.
* intlen     I   Length of time covered by record.
* n          I   Number of records in segment.
* polydg     I   Chebyshev polynomial degree.
* cdata      I   Array of Chebyshev coefficients.
* btime      I   Begin time of first record.
***********************************************************************/

%rename (spkw03) spkw03_c;
%apply (void RETURN_VOID) {void spkw03_c};

extern void spkw03_c(
        SpiceInt         handle,
        SpiceInt         body,
        SpiceInt         center,
        ConstSpiceChar   *CONST_STRING,
        SpiceDouble      first,
        SpiceDouble      last,
        ConstSpiceChar   *CONST_STRING,
        SpiceDouble      intlen,
        SpiceInt         n,
        SpiceInt         polydg,
        ConstSpiceDouble *IN_ARRAY1,
        SpiceDouble      btime
);

/***********************************************************************
* -Procedure spkw05_c ( Write SPK segment, type 5 )
*
* -Abstract
*
* Write an SPK segment of type 5 given a time-ordered set of
* discrete states and epochs, and the gravitational parameter
* of a central body.
*
* void spkw05_c (
*       SpiceInt                handle,
*       SpiceInt                body,
*       SpiceInt                center,
*       ConstSpiceChar        * frame,
*       SpiceDouble             first,
*       SpiceDouble             last,
*       ConstSpiceChar        * segid,
*       SpiceDouble             gm,
*       SpiceInt                n,
*       ConstSpiceDouble        states[][6],
*       ConstSpiceDouble        epochs[]      )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* handle     I   Handle of an SPK file open for writing.
* body       I   Body code for ephemeris object.
* center     I   Body code for the center of motion of the body.
* frame      I   The reference frame of the states.
* first      I   First valid time for which states can be computed.
* last       I   Last valid time for which states can be computed.
* segid      I   Segment identifier.
* gm         I   Gravitational parameter of central body.
* n          I   Number of states and epochs.
* states     I   States.
* epochs     I   Epochs.
***********************************************************************/

%rename (spkw05) spkw05_c;
%apply (void RETURN_VOID) {void spkw05_c};

extern void spkw05_c(
        SpiceInt         handle,
        SpiceInt         body,
        SpiceInt         center,
        ConstSpiceChar   *CONST_STRING,
        SpiceDouble      first,
        SpiceDouble      last,
        ConstSpiceChar   *CONST_STRING,
        SpiceDouble      gm,
        SpiceInt         n,
        ConstSpiceDouble *IN_ARRAY1,
        ConstSpiceDouble *IN_ARRAY1
);

/***********************************************************************
* -Procedure spkw08_c ( Write SPK segment, type 8 )
*
* -Abstract
*
* Write a type 8 segment to an SPK file.
*
* void spkw08_c (
*       SpiceInt            handle,
*       SpiceInt            body,
*       SpiceInt            center,
*       ConstSpiceChar    * frame,
*       SpiceDouble         first,
*       SpiceDouble         last,
*       ConstSpiceChar    * segid,
*       SpiceInt            degree,
*       SpiceInt            n,
*       ConstSpiceDouble    states[][6],
*       SpiceDouble         begtim,
*       SpiceDouble         step           )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* MAXDEG     P   Maximum degree of interpolating polynomials.
* TOLSCL     P   Scale factor used to compute time bound tolerance.
* handle     I   Handle of an SPK file open for writing.
* body       I   NAIF code for an ephemeris object.
* center     I   NAIF code for center of motion of BODY.
* frame      I   Reference frame name.
* first      I   Start time of interval covered by segment.
* last       I   End time of interval covered by segment.
* segid      I   Segment identifier.
* degree     I   Degree of interpolating polynomials.
* n          I   Number of states.
* states     I   Array of states.
* begtim     I   Epoch of first state in states array.
* step       I   Time step separating epochs of states.
* MAXDEG     P   Maximum allowed degree of interpolating polynomial.
***********************************************************************/

%rename (spkw08) spkw08_c;
%apply (void RETURN_VOID) {void spkw08_c};

extern void spkw08_c(
        SpiceInt         handle,
        SpiceInt         body,
        SpiceInt         center,
        ConstSpiceChar   *CONST_STRING,
        SpiceDouble      first,
        SpiceDouble      last,
        ConstSpiceChar   *CONST_STRING,
        SpiceInt         degree,
        SpiceInt         n,
        ConstSpiceDouble *IN_ARRAY1,
        SpiceDouble      begtim,
        SpiceDouble      step
);

/***********************************************************************
* -Procedure spkw09_c ( Write SPK segment, type 9 )
*
* -Abstract
*
* Write a type 9 segment to an SPK file.
*
* void spkw09_c (
*       SpiceInt             handle,
*       SpiceInt             body,
*       SpiceInt             center,
*       ConstSpiceChar     * frame,
*       SpiceDouble          first,
*       SpiceDouble          last,
*       ConstSpiceChar     * segid,
*       SpiceInt             degree,
*       SpiceInt             n,
*       ConstSpiceDouble     states[][6],
*       ConstSpiceDouble     epochs[]     )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* handle     I   Handle of an SPK file open for writing.
* body       I   NAIF code for an ephemeris object.
* center     I   NAIF code for center of motion of body.
* frame      I   Reference frame name.
* first      I   Start time of interval covered by segment.
* last       I   End time of interval covered by segment.
* segid      I   Segment identifier.
* degree     I   Degree of interpolating polynomials.
* n          I   Number of states.
* states     I   Array of states.
* epochs     I   Array of epochs corresponding to states.
* maxdeg     P   Maximum allowed degree of interpolating polynomial.
***********************************************************************/

%rename (spkw09) spkw09_c;
%apply (void RETURN_VOID) {void spkw09_c};

extern void spkw09_c(
        SpiceInt         handle,
        SpiceInt         body,
        SpiceInt         center,
        ConstSpiceChar   *CONST_STRING,
        SpiceDouble      first,
        SpiceDouble      last,
        ConstSpiceChar   *CONST_STRING,
        SpiceInt         degree,
        SpiceInt         n,
        ConstSpiceDouble *IN_ARRAY1,
        ConstSpiceDouble *IN_ARRAY1
);

/***********************************************************************
* -Procedure spkw10_c (SPK - write a type 10 segment )
*
* -Abstract
*
* Write an SPK type 10 segment to the file specified by
* the input `handle'.
*
* void spkw10_c (
*       SpiceInt           handle,
*       SpiceInt           body,
*       SpiceInt           center,
*       ConstSpiceChar   * frame,
*       SpiceDouble        first,
*       SpiceDouble        last,
*       ConstSpiceChar   * segid,
*       ConstSpiceDouble   consts[8],
*       SpiceInt           n,
*       ConstSpiceDouble   elems[],
*       ConstSpiceDouble   epochs[]  )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* handle     I   The handle of a DAF file open for writing.
* body       I   The NAIF ID code for the body of the segment.
* center     I   The center of motion for `body'.
* frame      I   The reference frame for this segment.
* first      I   The first epoch for which the segment is valid.
* last       I   The last  epoch for which the segment is valid.
* segid      I   The string to use for segment identifier.
* consts     I   Array of geophysical constants for the segment.
* n          I   The number of element/epoch pairs to be stored
* elems      I   The collection of "two-line" element sets.
* epochs     I   The epochs associated with the element sets.
***********************************************************************/

%rename (spkw10) spkw10_c;
%apply (void RETURN_VOID) {void spkw10_c};
%apply (ConstSpiceDouble IN_ARRAY1[ANY]) {ConstSpiceDouble consts[8]};

extern void spkw10_c(
        SpiceInt         handle,
        SpiceInt         body,
        SpiceInt         center,
        ConstSpiceChar   *CONST_STRING,
        SpiceDouble      first,
        SpiceDouble      last,
        ConstSpiceChar   *CONST_STRING,
        ConstSpiceDouble consts[8],
        SpiceInt         n,
        ConstSpiceDouble *IN_ARRAY1,
        ConstSpiceDouble *IN_ARRAY1
);

/***********************************************************************
* -Procedure spkw12_c ( Write SPK segment, type 12 )
*
* -Abstract
*
* Write a type 12 segment to an SPK file.
*
* void spkw12_c (
*       SpiceInt             handle,
*       SpiceInt             body,
*       SpiceInt             center,
*       ConstSpiceChar     * frame,
*       SpiceDouble          first,
*       SpiceDouble          last,
*       ConstSpiceChar     * segid,
*       SpiceInt             degree,
*       SpiceInt             n,
*       ConstSpiceDouble     states[][6],
*       SpiceDouble          begtim,
*       SpiceDouble          step        )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* MAXDEG     P   Maximum degree of interpolating polynomials.
* TOLSCL     P   Scale factor used to compute time bound tolerance.
* handle     I   Handle of an SPK file open for writing.
* body       I   NAIF code for an ephemeris object.
* center     I   NAIF code for center of motion of body.
* frame      I   Reference frame name.
* first      I   Start time of interval covered by segment.
* last       I   End time of interval covered by segment.
* segid      I   Segment identifier.
* degree     I   Degree of interpolating polynomials.
* n          I   Number of states.
* states     I   Array of states.
* begtim     I   Epoch of first state in states array.
* step       I   Time step separating epochs of states.
* MAXDEG     P   Maximum allowed degree of interpolating polynomial.
***********************************************************************/

%rename (spkw12) spkw12_c;
%apply (void RETURN_VOID) {void spkw12_c};

extern void spkw12_c(
        SpiceInt         handle,
        SpiceInt         body,
        SpiceInt         center,
        ConstSpiceChar   *CONST_STRING,
        SpiceDouble      first,
        SpiceDouble      last,
        ConstSpiceChar   *CONST_STRING,
        SpiceInt         degree,
        SpiceInt         n,
        ConstSpiceDouble *IN_ARRAY1,
        SpiceDouble      begtim,
        SpiceDouble      step
);

/***********************************************************************
* -Procedure spkw13_c ( Write SPK segment, type 13 )
*
* -Abstract
*
* Write a type 13 segment to an SPK file.
*
* void spkw13_c (
*       SpiceInt             handle,
*       SpiceInt             body,
*       SpiceInt             center,
*       ConstSpiceChar     * frame,
*       SpiceDouble          first,
*       SpiceDouble          last,
*       ConstSpiceChar     * segid,
*       SpiceInt             degree,
*       SpiceInt             n,
*       ConstSpiceDouble     states[][6],
*       ConstSpiceDouble     epochs[]     )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* handle     I   Handle of an SPK file open for writing.
* body       I   NAIF code for an ephemeris object.
* center     I   NAIF code for center of motion of body.
* frame      I   Reference frame name.
* first      I   Start time of interval covered by segment.
* last       I   End time of interval covered by segment.
* segid      I   Segment identifier.
* degree     I   Degree of interpolating polynomials.
* n          I   Number of states.
* states     I   Array of states.
* epochs     I   Array of epochs corresponding to states.
* MAXDEG     P   Maximum allowed degree of interpolating polynomial.
***********************************************************************/

%rename (spkw13) spkw13_c;
%apply (void RETURN_VOID) {void spkw13_c};

extern void spkw13_c(
        SpiceInt         handle,
        SpiceInt         body,
        SpiceInt         center,
        ConstSpiceChar   *CONST_STRING,
        SpiceDouble      first,
        SpiceDouble      last,
        ConstSpiceChar   *CONST_STRING,
        SpiceInt         degree,
        SpiceInt         n,
        ConstSpiceDouble *IN_ARRAY1,
        ConstSpiceDouble *IN_ARRAY1
);

/***********************************************************************
* -Procedure spkw15_c ( SPK, write a type 15 segment )
*
* -Abstract
*
* Write an SPK segment of type 15 given a type 15 data record.
*
* void spkw15_c (
*       SpiceInt           handle,
*       SpiceInt           body,
*       SpiceInt           center,
*       ConstSpiceChar   * frame,
*       SpiceDouble        first,
*       SpiceDouble        last,
*       ConstSpiceChar   * segid,
*       SpiceDouble        epoch,
*       ConstSpiceDouble   tp[3],
*       ConstSpiceDouble   pa[3],
*       SpiceDouble        p,
*       SpiceDouble        ecc,
*       SpiceDouble        j2flg,
*       ConstSpiceDouble   pv[3],
*       SpiceDouble        gm,
*       SpiceDouble        j2,
*       SpiceDouble        radius     )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* handle     I   Handle of an SPK file open for writing.
* body       I   Body code for ephemeris object.
* center     I   Body code for the center of motion of the body.
* frame      I   The reference frame of the states.
* first      I   First valid time for which states can be computed.
* last       I   Last valid time for which states can be computed.
* segid      I   Segment identifier.
* epoch      I   Epoch of the periapse.
* tp         I   Trajectory pole vector.
* pa         I   Periapsis vector.
* p          I   Semi-latus rectum.
* ecc        I   Eccentricity.
* j2flg      I   J2 processing flag.
* pv         I   Central body pole vector.
* gm         I   Central body GM.
* j2         I   Central body J2.
* radius     I   Equatorial radius of central body.
***********************************************************************/

%rename (spkw15) spkw15_c;
%apply (void RETURN_VOID) {void spkw15_c};
%apply (ConstSpiceDouble IN_ARRAY1[ANY]) {ConstSpiceDouble tp[3]};
%apply (ConstSpiceDouble IN_ARRAY1[ANY]) {ConstSpiceDouble pa[3]};
%apply (ConstSpiceDouble IN_ARRAY1[ANY]) {ConstSpiceDouble pv[3]};

extern void spkw15_c(
        SpiceInt         handle,
        SpiceInt         body,
        SpiceInt         center,
        ConstSpiceChar   *CONST_STRING,
        SpiceDouble      first,
        SpiceDouble      last,
        ConstSpiceChar   *CONST_STRING,
        SpiceDouble      epoch,
        ConstSpiceDouble tp[3],
        ConstSpiceDouble pa[3],
        SpiceDouble      p,
        SpiceDouble      ecc,
        SpiceDouble      j2flg,
        ConstSpiceDouble pv[3],
        SpiceDouble      gm,
        SpiceDouble      j2,
        SpiceDouble      radius
);

/***********************************************************************
* -Procedure spkw17_c ( SPK, write a type 17 segment )
*
* -Abstract
*
* Write an SPK segment of type 17 given a type 17 data record.
*
* void spkw17_c (
*       SpiceInt           handle,
*       SpiceInt           body,
*       SpiceInt           center,
*       ConstSpiceChar   * frame,
*       SpiceDouble        first,
*       SpiceDouble        last,
*       ConstSpiceChar   * segid,
*       SpiceDouble        epoch,
*       ConstSpiceDouble   eqel[9],
*       SpiceDouble        rapol,
*       SpiceDouble        decpol      )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* handle     I   Handle of an SPK file open for writing.
* body       I   Body code for ephemeris object.
* center     I   Body code for the center of motion of the body.
* frame      I   The reference frame of the states.
* first      I   First valid time for which states can be computed.
* last       I   Last valid time for which states can be computed.
* segid      I   Segment identifier.
* epoch      I   Epoch of elements in seconds past J2000.
* eqel       I   Array of equinoctial elements.
* rapol      I   Right Ascension of the reference plane's pole.
* decpol     I   Declination of the reference plane's pole.
***********************************************************************/

%rename (spkw17) spkw17_c;
%apply (void RETURN_VOID) {void spkw17_c};
%apply (ConstSpiceDouble IN_ARRAY1[ANY]) {ConstSpiceDouble eqel[9]};

extern void spkw17_c(
        SpiceInt         handle,
        SpiceInt         body,
        SpiceInt         center,
        ConstSpiceChar   *CONST_STRING,
        SpiceDouble      first,
        SpiceDouble      last,
        ConstSpiceChar   *CONST_STRING,
        SpiceDouble      epoch,
        ConstSpiceDouble eqel[9],
        SpiceDouble      rapol,
        SpiceDouble      decpol
);

/***********************************************************************
* -Procedure spkw18_c ( Write SPK segment, type 18 )
*
* -Abstract
*
* Write a type 18 segment to an SPK file.
*
* void spkw18_c (
*       SpiceInt             handle,
*       SpiceSPK18Subtype    subtyp,
*       SpiceInt             body,
*       SpiceInt             center,
*       ConstSpiceChar     * frame,
*       SpiceDouble          first,
*       SpiceDouble          last,
*       ConstSpiceChar     * segid,
*       SpiceInt             degree,
*       SpiceInt             n,
*       const void         * packts,
*       ConstSpiceDouble     epochs[]     )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* handle     I   Handle of an SPK file open for writing.
* subtyp     I   SPK type 18 subtype code.
* body       I   NAIF code for an ephemeris object.
* center     I   NAIF code for center of motion of `body'.
* frame      I   Reference frame name.
* first      I   Start time of interval covered by segment.
* last       I   End time of interval covered by segment.
* segid      I   Segment identifier.
* degree     I   Degree of interpolating polynomials.
* n          I   Number of packets.
* packts     I   Array of packets.
* epochs     I   Array of epochs corresponding to packets.
* MAXDEG     P   Maximum allowed degree of interpolating polynomial.
***********************************************************************/

%rename (spkw18) my_spkw18_c;
%apply (void RETURN_VOID) {void my_spkw18_c};
%apply (ConstSpiceChar *CONST_STRING) {ConstSpiceChar *frame};
%apply (ConstSpiceChar *CONST_STRING) {ConstSpiceChar *segid};
%apply (ConstSpiceDouble *IN_ARRAY1) {ConstSpiceDouble *packts};
%apply (ConstSpiceDouble *IN_ARRAY1) {ConstSpiceDouble *epochs};

%inline %{
    void my_spkw18_c(
        SpiceInt          handle,
        ConstSpiceChar    *subtyp,
        SpiceInt          body,
        SpiceInt          center,
        ConstSpiceChar    *frame,
        SpiceDouble       first,
        SpiceDouble       last,
        ConstSpiceChar    *segid,
        SpiceInt          degree,
        SpiceInt          n,
        ConstSpiceDouble  *packts,
        ConstSpiceDouble  *epochs)
    {
        SpiceSPK18Subtype subtyp_;
        if (strcmp(subtyp, "S18TP0") == 0) {
            subtyp_ = S18TP0;
        } else if (strcmp(subtyp, "S18TP1") == 0) {
            subtyp_ = S18TP1;
        } else {
            chkin_c("spkw18");
            setmsg_c("subtyp value must be one of {\"S18TP0\", \"S18TP0\"}");
            sigerr_c("SPICE(SPICE(INVALIDARGUMENT)");
            chkout_c("spkw18");
            return;
        }

        spkw18_c(handle, subtyp_, body, center, frame, first, last, segid,
                 degree, n, packts, epochs);
    }
%}

/***********************************************************************
* -Procedure spkw20_c ( Write SPK segment, type 20 )
*
* -Abstract
*
* Write a type 20 segment to an SPK file.
*
* void spkw20_c (
*       SpiceInt            handle,
*       SpiceInt            body,
*       SpiceInt            center,
*       ConstSpiceChar    * frame,
*       SpiceDouble         first,
*       SpiceDouble         last,
*       ConstSpiceChar    * segid,
*       SpiceDouble         intlen,
*       SpiceInt            n,
*       SpiceInt            polydg,
*       ConstSpiceDouble    cdata[],
*       SpiceDouble         dscale,
*       SpiceDouble         tscale,
*       SpiceDouble         initjd,
*       SpiceDouble         initfr  )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* handle     I   Handle of SPK file open for writing.
* body       I   NAIF code for ephemeris object.
* center     I   NAIF code for the center of motion of the body.
* frame      I   Reference frame name.
* first      I   Start time of interval covered by segment.
* last       I   End time of interval covered by segment.
* segid      I   Segment identifier.
* intlen     I   Length of time covered by logical record (days).
* n          I   Number of logical records in segment.
* polydg     I   Chebyshev polynomial degree.
* cdata      I   Array of Chebyshev coefficients and positions.
* dscale     I   Distance scale of data.
* tscale     I   Time scale of data.
* initjd     I   Integer part of begin time (TDB Julian date) of
*                first record.
* initfr     I   Fractional part of begin time (TDB Julian date) of
*                first record.
* MAXDEG     P   Maximum allowed degree of Chebyshev expansions.
* DTOL       P   Absolute tolerance for coverage bound checking.
* TOLSCL     P   Tolerance scale for coverage bound checking.
***********************************************************************/

%rename (spkw20) spkw20_c;
%apply (void RETURN_VOID) {void spkw20_c};

extern void spkw20_c(
        SpiceInt         handle,
        SpiceInt         body,
        SpiceInt         center,
        ConstSpiceChar   *CONST_STRING,
        SpiceDouble      first,
        SpiceDouble      last,
        ConstSpiceChar   *CONST_STRING,
        SpiceDouble      intlen,
        SpiceInt         n,
        SpiceInt         polydg,
        ConstSpiceDouble *IN_ARRAY1,
        SpiceDouble      dscale,
        SpiceDouble      tscale,
        SpiceDouble      initjd,
        SpiceDouble      initfr
);

/***********************************************************************
* -Procedure sumad_c ( Sum of a double precision array )
*
* -Abstract
*
* Return the sum of the elements of a floating-point array.
*
* SpiceDouble sumad_c (
*       ConstSpiceDouble   * array,
*       SpiceInt             n     )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* array      I   Input array.
* n          I   Number of elements in `array'.
* sum        R   Sum of elements.
***********************************************************************/

%rename (sumad) sumad_c;
%apply (SpiceDouble RETURN_DOUBLE) {SpiceDouble sumad_c};
%apply (ConstSpiceDouble *IN_ARRAY1, SpiceInt DIM1)
                {(ConstSpiceDouble *array, SpiceInt n)};

extern SpiceDouble sumad_c(
        ConstSpiceDouble *array, SpiceInt n
);

/***********************************************************************
* -Procedure sumai_c ( Sum of an integer array )
*
* -Abstract
*
* Return the sum of the elements of an integer array.
*
* SpiceInt sumai_c (
*       ConstSpiceInt   * array,
*       SpiceInt          n     )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* array      I   Input array.
* n          I   Number of elements in `array'.
* sum        R   Sum of elements.
***********************************************************************/

%rename (sumai) sumai_c;
%apply (SpiceInt RETURN_INT) {SpiceInt sumai_c};
%apply (ConstSpiceInt *IN_ARRAY1, SpiceInt DIM1)
            {(ConstSpiceInt *array, SpiceInt n)};

extern SpiceInt sumai_c(
        ConstSpiceInt *array, SpiceInt n
);

/***********************************************************************
* -Procedure swpool_c ( Set watch on a pool variable )
*
* -Abstract
*
* Add a name to the list of agents to notify whenever a member of
* a list of kernel variables is updated.
*
* void swpool_c (
*       ConstSpiceChar    * agent,
*       SpiceInt            nnames,
*       SpiceInt            namlen,
*       const void          names[][]   )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* agent      I   The name of an agent to be notified after updates.
* nnames     I   The number of variables to associate with agent.
* namlen     I   Length of strings in the names array.
* names      I   Variable names whose update causes the notice.
***********************************************************************/

%rename (swpool) swpool_c;
%apply (void RETURN_VOID) {void swpool_c};
%apply (SpiceInt DIM1, SpiceInt DIM2, ConstSpiceChar *IN_STRINGS)
                {(SpiceInt nnames, SpiceInt namlen, ConstSpiceChar *names)};

extern void swpool_c(
        ConstSpiceChar *CONST_STRING,
        SpiceInt       nnames, SpiceInt namlen, ConstSpiceChar *names
);

/***********************************************************************
* -Procedure szpool_c (Get size limitations of the kernel pool)
*
* -Abstract
*
* Return the kernel pool size limitations.
*
* void szpool_c (
*       ConstSpiceChar * name,
*       SpiceInt       * n,
*       SpiceBoolean   * found )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* name       I   Name of the parameter to be returned, one of
*                "MAXVAR", "MAXLEN", "MAXVAL", "MXNOTE", "MAXAGT", "MAXCHR",
*                or "MAXLIN".
* n          O   Value of parameter specified by name.
* found      O   True if name is recognized.
***********************************************************************/

%rename (szpool) szpool_c;
%apply (void RETURN_VOID) {void szpool_c};
%apply (ConstSpiceChar *CONST_STRING) {ConstSpiceChar *name};

extern void szpool_c(
        ConstSpiceChar *CONST_STRING,
        SpiceInt       *OUTPUT,
        SpiceBoolean   *OUTPUT
);

/***********************************************************************
* -Procedure tangpt_c ( Ray-ellipsoid tangent point )
*
* -Abstract
*
* Compute, for a given observer, ray emanating from the observer,
* and target, the "tangent point": the point on the ray nearest
* to the target's surface. Also compute the point on the target's
* surface nearest to the tangent point. The locations of both points
* are optionally corrected for light time and stellar aberration.
* The surface shape is modeled as a triaxial ellipsoid.
*
* void tangpt_c (
*       ConstSpiceChar    * method,
*       ConstSpiceChar    * target,
*       SpiceDouble         et,
*       ConstSpiceChar    * fixref,
*       ConstSpiceChar    * abcorr,
*       ConstSpiceChar    * corloc,
*       ConstSpiceChar    * obsrvr,
*       ConstSpiceChar    * dref,
*       ConstSpiceDouble    dvec[3],
*       SpiceDouble         tanpt[3],
*       SpiceDouble       * alt,
*       SpiceDouble       * range,
*       SpiceDouble         srfpt[3],
*       SpiceDouble       * trgepc,
*       SpiceDouble         srfvec[3] )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* method     I   Computation method.
* target     I   Name of target body.
* et         I   Epoch in ephemeris seconds past J2000 TDB.
* fixref     I   Body-fixed, body-centered target body frame.
* abcorr     I   Aberration correction.
* corloc     I   Aberration correction locus: "TANGENT POINT" or
*                "SURFACE POINT".
* obsrvr     I   Name of observing body.
* dref       I   Reference frame of ray direction vector.
* dvec       I   Ray direction vector.
* tanpt      O   "Tangent point": point on ray nearest to surface.
* alt        O   Altitude of tangent point above surface.
* range      O   Distance of tangent point from observer.
* srfpt      O   Point on surface nearest to tangent point.
* trgepc     O   Epoch associated with correction locus.
* srfvec     O   Vector from observer to surface point `srfpt'.
***********************************************************************/

%rename (tangpt) tangpt_c;
%apply (void RETURN_VOID) {void tangpt_c};
%apply (ConstSpiceDouble IN_ARRAY1[ANY]) {ConstSpiceDouble dvec[3]};
%apply (SpiceDouble OUT_ARRAY1[ANY]) {SpiceDouble tanpt[3]};
%apply (SpiceDouble OUT_ARRAY1[ANY]) {SpiceDouble srfpt[3]};
%apply (SpiceDouble OUT_ARRAY1[ANY]) {SpiceDouble srfvec[3]};

extern void tangpt_c(
        ConstSpiceChar   *CONST_STRING,
        ConstSpiceChar   *CONST_STRING,
        SpiceDouble      et,
        ConstSpiceChar   *CONST_STRING,
        ConstSpiceChar   *CONST_STRING,
        ConstSpiceChar   *CONST_STRING,
        ConstSpiceChar   *CONST_STRING,
        ConstSpiceChar   *CONST_STRING,
        ConstSpiceDouble dvec[3],
        SpiceDouble      tanpt[3],
        SpiceDouble      *OUTPUT,
        SpiceDouble      *OUTPUT,
        SpiceDouble      srfpt[3],
        SpiceDouble      *OUTPUT,
        SpiceDouble      srfvec[3]
);

//Vector version
VECTORIZE_2s_d_5s_dX__dN_2d_dN_d_dN(tangpt, tangpt_c, 3, 3, 3)

/***********************************************************************
* -Procedure tkfram_c ( TK frame, find position rotation )
*
* -Abstract
*
* Find the position rotation matrix from a Text Kernel (TK) frame
* with the specified frame class ID to its base frame.
*
* void tkfram_c (
*       SpiceInt            frcode,
*       SpiceDouble         rot[3][3],
*       SpiceInt          * frame,
*       SpiceBoolean      * found         )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* frcode     I   Frame class ID of a TK frame.
* rot        O   Rotation matrix from TK frame to frame `frame'.
* frame      O   Frame ID of the base reference.
* found      O   True if the rotation could be determined.
***********************************************************************/

%rename (tkfram) tkfram_c;
%apply (void RETURN_VOID) {void tkfram_c};
%apply (SpiceDouble OUT_ARRAY2[ANY][ANY]) {SpiceDouble rot[3][3]};

extern void tkfram_c(
        SpiceInt     frcode,
        SpiceDouble  rot[3][3],
        SpiceInt     *OUTPUT,
        SpiceBoolean *OUTPUT
);

/***********************************************************************
* -Procedure tparch_c ( Parse check---check format of strings )
*
* -Abstract
*
* Restrict the set of strings that are recognized by SPICE time
* parsing routines to those that have standard values for all time
* components.
*
* void tparch_c (
*       ConstSpiceChar    * type )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* type       I   String: Use "YES" to restrict time inputs.
***********************************************************************/

%rename (tparch) tparch_c;
%apply (void RETURN_VOID) {void tparch_c};
%apply (ConstSpiceChar *CONST_STRING) {ConstSpiceChar *type};

extern void tparch_c(
        ConstSpiceChar *CONST_STRING
);

/***********************************************************************
* -Procedure trgsep_c ( Separation quantity from observer )
*
* -Abstract
*
* Compute the angular separation in radians between two spherical
* or point objects.
*
* SpiceDouble trgsep_c (
*       SpiceDouble         et,
*       ConstSpiceChar    * targ1,
*       ConstSpiceChar    * shape1,
*       ConstSpiceChar    * frame1,
*       ConstSpiceChar    * targ2,
*       ConstSpiceChar    * shape2,
*       ConstSpiceChar    * frame2,
*       ConstSpiceChar    * obsrvr,
*       ConstSpiceChar    * abcorr )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* et         I   Ephemeris seconds past J2000 TDB.
* targ1      I   First target body name.
* shape1     I   First target body shape.
* frame1     I   Reference frame of first target.
* targ2      I   Second target body name.
* shape2     I   First target body shape.
* frame2     I   Reference frame of second target.
* obsrvr     I   Observing body name.
* abcorr     I   Aberration corrections flag.
* sep        R   Separation angle in radians.
***********************************************************************/

%rename (trgsep) trgsep_c;
%apply (SpiceDouble RETURN_DOUBLE) {SpiceDouble trgsep_c};

extern SpiceDouble trgsep_c(
        SpiceDouble    et,
        ConstSpiceChar *CONST_STRING,
        ConstSpiceChar *CONST_STRING,
        ConstSpiceChar *CONST_STRING,
        ConstSpiceChar *CONST_STRING,
        ConstSpiceChar *CONST_STRING,
        ConstSpiceChar *CONST_STRING,
        ConstSpiceChar *CONST_STRING,
        ConstSpiceChar *CONST_STRING
);

//Vector version
VECTORIZE_d_8s__RETURN_d(trgsep, trgsep_c)

/***********************************************************************
* -Procedure twovxf_c ( Two states defining a frame transformation )
*
* -Abstract
*
* Find the state transformation from a base frame to the
* right-handed frame defined by two state vectors: one state
* vector defining a specified axis and a second state vector
* defining a specified coordinate plane.
*
* void twovxf_c (
*       ConstSpiceDouble    axdef[6],
*       SpiceInt            indexa,
*       ConstSpiceDouble    plndef[6],
*       SpiceInt            indexp,
*       SpiceDouble         xform[6][6] )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* axdef      I   State defining a principal axis.
* indexa     I   Principal axis number of `axdef' (x=1, y=2, z=3).
* plndef     I   State defining (with `axdef') a principal plane.
* indexp     I   Second axis number (with `indexa') of principal
*                plane.
* xform      O   Output state transformation matrix.
***********************************************************************/

%rename (twovxf) twovxf_c;
%apply (void RETURN_VOID) {void twovxf_c};
%apply (ConstSpiceDouble IN_ARRAY1[ANY]) {ConstSpiceDouble axdef[6]};
%apply (ConstSpiceDouble IN_ARRAY1[ANY]) {ConstSpiceDouble plndef[6]};
%apply (SpiceDouble OUT_ARRAY2[ANY][ANY]) {SpiceDouble xform[6][6]};

extern void twovxf_c(
        ConstSpiceDouble axdef[6],
        SpiceInt         indexa,
        ConstSpiceDouble plndef[6],
        SpiceInt         indexp,
        SpiceDouble      xform[6][6]
);

//Vector version
VECTORIZE_dX_i_dX_i__dMN(twovxf, twovxf_c, 6, 6)

/***********************************************************************
* -Procedure vprojg_c ( Vector projection, general dimension )
*
* -Abstract
*
* Compute the projection of one vector onto another vector. All
* vectors are of arbitrary dimension.
*
* void vprojg_c (
*       ConstSpiceDouble    a[],
*       ConstSpiceDouble    b[],
*       SpiceInt            ndim,
*       SpiceDouble         p[] )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* a          I   The vector to be projected.
* b          I   The vector onto which `a' is to be projected.
* ndim       I   Dimension of `a', `b', and `p'.
* p          O   The projection of `a' onto `b'.
***********************************************************************/

%rename (vprojg) my_vprojg_c;
%apply (void RETURN_VOID) {void my_vprojg_c};
%apply (ConstSpiceDouble *IN_ARRAY1, SpiceInt DIM1)
                {(ConstSpiceDouble *a, SpiceInt ndim)};
%apply (ConstSpiceDouble *IN_ARRAY1, SpiceInt DIM1)
                {(ConstSpiceDouble *b, SpiceInt ndim1)};
%apply (SpiceDouble **OUT_ARRAY1, SpiceInt *SIZE1)
                {(SpiceDouble **p, SpiceInt *ndim2)};

%inline %{
    void my_vprojg_c(
        ConstSpiceDouble *a, SpiceInt ndim,
        ConstSpiceDouble *b, SpiceInt ndim1, 
        SpiceDouble     **p, SpiceInt *ndim2)
    {
        if (!my_assert_eq(ndim, ndim1, "vprojg",
            "Array dimension mismatch in vprojg: "
            "a elements = #; b elements = #")) return;

        *ndim2 = ndim;
        *p = my_malloc(ndim, "vprojg");
        if (*p) {
            vprojg_c(a, b, ndim, *p);
        }
    }
%}

%{
    void my_vprojg_nomalloc(
        ConstSpiceDouble *a, SpiceInt ndim,
        ConstSpiceDouble *b, SpiceInt ndim1, 
        SpiceDouble      *p, SpiceInt *ndim2)
    {
        if (!my_assert_eq(ndim, ndim1, "vprojg",
            "Array dimension mismatch in vprojg: "
            "a elements = #; b elements = #")) return;

        vprojg_c(a, b, ndim, p);
        *ndim2 = ndim;
    }
%}

//Vector version
VECTORIZE_di_di__di(vprojg, my_vprojg_nomalloc)

/***********************************************************************
* -Procedure wncomd_c ( Complement a DP window )
*
* -Abstract
*
* Determine the complement of a floating-point window with
* respect to a specified interval.
*
* void wncomd_c (
*       SpiceDouble    left,
*       SpiceDouble    right,
*       SpiceCell    * window,
*       SpiceCell    * result )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* left       I   Left endpoint of complement interval.
* right      I   Right endpoint of complement interval.
* window     I   Input window.
* result     O   Complement of window with respect to [left,right].
***********************************************************************/

%rename (wncomd) wncomd_c;
%apply (void RETURN_VOID) {void wncomd_c};
%apply (SpiceCellDouble* INPUT) {SpiceCell *window};
%apply (SpiceCellDouble* OUTPUT) {SpiceCell *result};

extern void wncomd_c(
        SpiceDouble left,
        SpiceDouble right,
        SpiceCell   *window,
        SpiceCell   *result
);

/***********************************************************************
* -Procedure wncond_c ( Contract the intervals of a DP window )
*
* -Abstract
*
* Contract each of the intervals of a floating-point window.
*
* void wncond_c (
*       SpiceDouble     left,
*       SpiceDouble     right,
*       SpiceCell     * window )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* left       I   Amount added to each left endpoint.
* right      I   Amount subtracted from each right endpoint.
* window    I-O  Window to be contracted.
***********************************************************************/

%rename (wncond) wncond_c;
%apply (void RETURN_VOID) {void wncond_c};
%apply (SpiceCellDouble* INOUT) {SpiceCell *window};

extern void wncond_c(
        SpiceDouble left,
        SpiceDouble right,
        SpiceCell   *window
);

/***********************************************************************
* -Procedure wndifd_c ( Difference two DP windows )
*
* -Abstract
*
* Place the difference of two floating-point windows into
* a third window.
*
* void wndifd_c (
*       SpiceCell   * a,
*       SpiceCell   * b,
*       SpiceCell   * c  )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* a          I   First input window.
* b          I   Second input windows.
* c          O   Difference of `a' and `b'.
***********************************************************************/

%rename (wndifd) wndifd_c;
%apply (void RETURN_VOID) {void wndifd_c};

%apply (SpiceCellDouble* INPUT) {SpiceCell *a};
%apply (SpiceCellDouble* INPUT) {SpiceCell *b};
%apply (SpiceCellDouble* OUTPUT) {SpiceCell *c};

extern void wndifd_c(
        SpiceCell *a,
        SpiceCell *b,
        SpiceCell *c
);

/***********************************************************************
* -Procedure wnelmd_c ( Element of a DP window )
*
* -Abstract
*
* Determine whether a point is an element of a floating-point
* window.
*
* SpiceBoolean wnelmd_c (
*       SpiceDouble    point,
*       SpiceCell    * window )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* point      I   Input point.
* window     I   Input window.
* flag       R   True if the point is an element; False otherwise.
***********************************************************************/

%rename (wnelmd) wnelmd_c;
%apply (SpiceBoolean RETURN_BOOLEAN) {SpiceBoolean wnelmd_c};
%apply (SpiceCellDouble* INPUT) {SpiceCell *window};

extern SpiceBoolean wnelmd_c(
        SpiceDouble point,
        SpiceCell *window
);

/***********************************************************************
* -Procedure wnexpd_c ( Expand the intervals of a DP window )
*
* -Abstract
*
* Expand each of the intervals of a floating-point window.
*
* void wnexpd_c (
*       SpiceDouble    left,
*       SpiceDouble    right,
*       SpiceCell    * window )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* left       I   Amount subtracted from each left endpoint.
* right      I   Amount added to each right endpoint.
* window    I-O  Window to be expanded.
***********************************************************************/

%rename (wnexpd) wnexpd_c;
%apply (void RETURN_VOID) {void wnexpd_c};
%apply (SpiceCellDouble* INOUT) {SpiceCell *window};

extern void wnexpd_c(
        SpiceDouble left,
        SpiceDouble right,
        SpiceCell   *window
);

/***********************************************************************
* -Procedure wnextd_c ( Extract the endpoints from a DP window )
*
* -Abstract
*
* Extract the left or right endpoints from a floating-point
* window.
*
* void wnextd_c (
*       SpiceChar     side,
*       SpiceCell   * window )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* side       I   Extract left ('L') or right ('R') endpoints.
* window    I-O  Window to be extracted.
***********************************************************************/

%rename (wnextd) wnextd_c;
%apply (void RETURN_VOID) {void wnextd_c};
%apply (SpiceChar IN_STRING) {SpiceChar side};
%apply (SpiceCellDouble* INOUT) {SpiceCell *window};

extern void wnextd_c(
        SpiceChar side,
        SpiceCell   *window
);

/***********************************************************************
* -Procedure wnfild_c ( Fill small gaps in a DP window )
*
* -Abstract
*
* Fill small gaps between adjacent intervals of a floating-point
* window.
*
* void wnfild_c (
*       SpiceDouble     smlgap,
*       SpiceCell     * window )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* smlgap     I   Limiting measure of small gaps.
* window    I-O  Window to be filled.
***********************************************************************/

%rename (wnfild) wnfild_c;
%apply (void RETURN_VOID) {void wnfild_c};
%apply (SpiceCellDouble* INOUT) {SpiceCell *window};

extern void wnfild_c(
        SpiceDouble smlgap,
        SpiceCell   *window
);

/***********************************************************************
* -Procedure wnfltd_c ( Filter small intervals from a DP window )
*
* -Abstract
*
* Filter (remove) small intervals from a floating-point window.
*
* void wnfltd_c (
*       SpiceDouble     smlint,
*       SpiceCell    *  window )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* smlint     I   Limiting measure of small intervals.
* window    I-O  Window to be filtered.
***********************************************************************/

%rename (wnfltd) wnfltd_c;
%apply (void RETURN_VOID) {void wnfltd_c};
%apply (SpiceCellDouble* INOUT) {SpiceCell *window};

extern void wnfltd_c(
        SpiceDouble smlint,
        SpiceCell   *window
);

/***********************************************************************
* -Procedure wnincd_c ( Included in a double precision window )
*
* -Abstract
*
* Determine whether an interval is included in a floating-point
* window.
*
* SpiceBoolean wnincd_c (
*       SpiceDouble     left,
*       SpiceDouble     right,
*       SpiceCell     * window )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* left       I   Minimum of input interval.
* right      I   Maximum of input interval.
* window     I   Input window.
* flag       R   True if the interval is included; False otherwise.
***********************************************************************/

%rename (wnincd) wnincd_c;
%apply (SpiceBoolean RETURN_BOOLEAN) {SpiceBoolean wnincd_c};
%apply (SpiceCellDouble* INPUT) {SpiceCell *window};

extern SpiceBoolean wnincd_c(
        SpiceDouble left,
        SpiceDouble right,
        SpiceCell   *window
);

/***********************************************************************
* -Procedure wninsd_c ( Insert an interval into a DP window )
*
* -Abstract
*
* Insert an interval into a floating-point window.
*
* void wninsd_c (
*       SpiceDouble     left,
*       SpiceDouble     right,
*       SpiceCell     * window )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* left       I   Left endpoint of new interval.
* right      I   Right endpoint of new interval.
* window    I-O  Input window.
***********************************************************************/

%rename (wninsd) wninsd_c;
%apply (void RETURN_VOID) {void wninsd_c};

%apply (SpiceCellDouble *INOUT) {SpiceCellDouble *window};

extern void wninsd_c(
        SpiceDouble left,
        SpiceDouble right,
        SpiceCellDouble *window
);

/***********************************************************************
* -Procedure wnintd_c ( Intersect two DP windows )
*
* -Abstract
*
* Place the intersection of two floating-point windows into
* a third window.
*
* void wnintd_c (
*       SpiceCell  * a,
*       SpiceCell  * b,
*       SpiceCell  * c )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* a          I   First input window.
* b          I   Second input window.
* c          O   Intersection of `a' and `b'.
***********************************************************************/

%rename (wnintd) wnintd_c;
%apply (void RETURN_VOID) {void wnintd_c};
%apply (SpiceCellDouble* INPUT) {SpiceCell *a};
%apply (SpiceCellDouble* INPUT) {SpiceCell *b};
%apply (SpiceCellDouble* OUTPUT) {SpiceCell *c};

extern void wnintd_c(
        SpiceCell *a,
        SpiceCell *b,
        SpiceCell *c
);

/***********************************************************************
* -Procedure wnreld_c ( Compare two DP windows )
*
* -Abstract
*
* Compare two floating-point windows.
*
* SpiceBoolean wnreld_c (
*       SpiceCell       * a,
*       ConstSpiceChar  * op,
*       SpiceCell       * b   )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* a          I   First window.
* op         I   Comparison operator: "=" for equal;
*                "<>" for not equal;
*                "<=" for `a' a subset of `b';
*                "<" for `a' a proper subset of `b';
*                ">=" for `b' a subset of `a';
*                ">" for `b' a proper subset of `a'.
* b          I   Second window.
* flag       R   True if the comparison is satisfied.
***********************************************************************/

%rename (wnreld) wnreld_c;
%apply (SpiceBoolean RETURN_BOOLEAN) {SpiceBoolean wnreld_c};
%apply (SpiceCellDouble* INPUT) {SpiceCell *a};
%apply (SpiceCellDouble* INPUT) {SpiceCell *b};
%apply (ConstSpiceChar *CONST_STRING) {ConstSpiceChar *op};

extern SpiceBoolean wnreld_c(
        SpiceCell *a,
        ConstSpiceChar *op,
        SpiceCell *b
);

/***********************************************************************
* -Procedure wnsumd_c ( Summary of a double precision window )
*
* -Abstract
*
* Summarize the contents of a floating-point window.
*
* void wnsumd_c (
*       SpiceCell      * window,
*       SpiceDouble    * meas,
*       SpiceDouble    * avg,
*       SpiceDouble    * stddev,
*       SpiceInt       * idxsml,
*       SpiceInt       * idxlon   )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* window     I   Window to be summarized.
* meas       O   Total measure of intervals in window.
* avg        O   Average measure.
* stddev     O   Standard deviation.
* idxsml     O   Location of shortest interval.
* idxlon     O   Location of longest interval.
***********************************************************************/

%rename (wnsumd) wnsumd_c;
%apply (void RETURN_VOID) {void wnsumd_c};
%apply (SpiceCellDouble* INPUT) {SpiceCell *window};
%apply (SpiceDouble *OUTPUT) {SpiceDouble *meas};
%apply (SpiceDouble *OUTPUT) {SpiceDouble *avg};
%apply (SpiceDouble *OUTPUT) {SpiceDouble *stddev};
%apply (SpiceInt    *OUTPUT) {SpiceInt    *idxsml};
%apply (SpiceInt    *OUTPUT) {SpiceInt    *idxlon};

extern void wnsumd_c(
        SpiceCell   *window,
        SpiceDouble *meas,
        SpiceDouble *avg,
        SpiceDouble *stddev,
        SpiceInt    *idxsml,
        SpiceInt    *idxlon
);

/***********************************************************************
* -Procedure wnunid_c ( Union two DP windows )
*
* -Abstract
*
* Place the union of two floating-point windows into a third
* window.
*
* void wnunid_c (
*       SpiceCell   * a,
*       SpiceCell   * b,
*       SpiceCell   * c )
*
* -Brief_I/O
*
* Variable  I/O  Description
* --------  ---  --------------------------------------------------
* a          I   First input window.
* b          I   Second input window.
* c          O   Union of `a' and `b'.
***********************************************************************/

%rename (wnunid) wnunid_c;
%apply (void RETURN_VOID) {void wnunid_c};
%apply (SpiceCellDouble* INPUT) {SpiceCell *a};
%apply (SpiceCellDouble* INPUT) {SpiceCell *b};
%apply (SpiceCellDouble* OUTPUT) {SpiceCell *c};

extern void wnunid_c(
        SpiceCell *a,
        SpiceCell *b,
        SpiceCell *c
);

/**********************************************************************/
