# `cspyce` DEVELOPERS' GUIDE
March 2022

Frank Yellin, PDS Ring-Moon Systems Node, SETI Institute volunteer.

This guide is intended for those who have downloaded the 
[github source code](https://github.com/SETI/pds-cspyce/) and are modifying
or extending the `cspyce` toolkit.
You do not need to read this if you are installing an existing `PyPI`
distribition of the sources.

## SETTING UP

The root of the github tree is called `pds-cspyce`.
When we use `pds-cspcyce` in this document, we are referring to that directory,
wherever it happens to be on your computer.

The github source code intentionally does not include the source code to
cspice itself.
You should download the cspice sources from XXXX.
You should make a soft link from your cspice directory to `pds-cspyce/cspice`.
```shell
ln -s <path-to-your-cspice-directory> <path-to-your-pds-cspyce>/cspice
```
Confirm that `pds-cspyce/cspice/include` has a bunch of `.h` files and that
`pds-cspyce/cspice/src/cspice` contains several thousand `.c` files.

## BUILDING CSPYCE
Whenever I use the program `python` as a command, I mean your specific Python
runtime.  If you have multiple versions of Python installed on your computer,
you may need to be running `python2` and `python3`, or `python3.7` and
`python3.8`.

In general, our `.py` and `.c` sources should work across all implementations of 
Python beyond 2.7. There is no expectation of binary compatibility between
multiple versions.

You build `cspyce` by running the command
```shell
python setup.py build_ext --inplace
```

If you have modified any of the template files, you should instead run
```shell
python setup.py generate build_ext --inplace
```
The Python setuptools is not yet smart enough to understand dependencies,
and you must tell it to regenerate `cspcye0_wrap.c` whenever any of the files
that affect it have changed.

The first time you run one of these commands will be slow, as the build
system also recompiles all of the spice code and generates a shared libray
for it.
Subsequent builds should be fast.


Once you have built `cspyce`, you should confirm that it works.
```shell
python
> import cspyce
> cspyce.tkvrsn('toolkit')
```

## CREATING a DISTRIBUTION

### Source Distributions

The simplist type of distribution is a source distribution:

```
python setup.py sdist
```
This will create a filel named `dist/cspyce-<version>.tar.gz`.
This file can be uploaded at PyPI and then downloaded by any version of
Python on any operating system.  The `.tar.gz` contains all the sources needed
to compile and run `cspyce`.
It includes the necessary pieces of the `cspice/` source tree as well as an
already generated `cspyce0_wrap.c` file so that they do not need to install 
`swig.`

The installing process takes a few minutes because 2000 files from the Cspice
library are being compiled.

### Wheel distributions

A second type of distribution is the "wheel".  
```shell
python setup.py bdist_wheel
```
A wheel includes binaries that have been compiled specifically for this version
of Python running on this specific operating system.
Some web sites indicate that there is no guarantee of compatibility between
various flavors of Linux.

The installation of a wheel, if you have the correct one, is incredibly quick.
All binaries have been pre-compiled, and the various files simply need to be put
into the correct place.

### Tags

To be written

### Multiple distributions

Multiple distributions can be created with a single command:
```shell
python setup.py bdist_wheel sdist
```
This is particularly useful with tags.

## UPLOADING A DISTRIBUTION TO PyPI

To be written.
