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
When we use `pds-cspyce` in this document, we are referring to that directory,
wherever it happens to be on your computer.

The github source code intentionally does not include the source code to
cspice itself.
You should download the cspice sources from
https://naif.jpl.nasa.gov/naif/toolkit.html. 
The current SPICE Toolkit version is N0067, released January 3, 2022.
You should make a soft link from your cspice directory to `pds-cspyce/cspice`.
```shell
ln -s <path-to-your-cspice-directory> <path-to-your-pds-cspyce>/cspice
```
Confirm that `pds-cspyce/cspice/include` has a bunch of `.h` files and that
`pds-cspyce/cspice/src/cspice` contains several thousand `.c` files.

## BUILDING CSPYCE
Whenever we use the program `python` as a command, we mean your specific Python
runtime. If you have multiple versions of Python installed on your computer,
you may need to be running `python2` and `python3`, or `python3.7` and
`python3.8`.

In general, our `.py` and `.c` sources should work across all implementations of 
Python beyond 2.7. However, there is no expectation of binary compatibility between
multiple versions.

You must have swig and at least one newer version (≥ 3.8) of Python3 running on 
your computer for the first step:
```shell
python3 setup.py generate
```
This step re-creates all the generated files .py and .c needed to implement
the templates. 

You compile the c-implementation of the Spice library by running:
```shell
python setup.py build_clib
```
This will execute somewhat slowly because it is compiling several thousand files. 
You should only need to do this once.

You then build `cspyce` by running the command
```shell
python setup.py build_ext --inplace
```
It is particularly important that you execute this command using the same
version of Python that you are planning to use for running cspyce.
Python does not guarantee binary compatibility between Python versions.

If you modify any of the templates, you will need to re-run the "generate"
command above (using Python3) and the "build_ext" command.
The Python setuptools is not yet smart enough to understand dependencies.

Once you have built `cspyce`, you should confirm that it works.
```shell
python
> import cspyce
> cspyce.tkvrsn('toolkit')
'CSPICE_N0067'
```
Your actual result will depends on which toolkit version you downloaded from NAIF.
## CREATING A DISTRIBUTION

### Before you begin

Make sure you have the latest versions of the necessary Python software:
```shell
python -m pip install --upgrade pip setuptools wheel twine
```
### Source Distributions

The simplist type of distribution is a source distribution:

```
python setup.py sdist
```
This will create a filel named `dist/cspyce-<version>.tar.gz`.
This file can be uploaded at PyPI and then downloaded by any version of
Python on any operating system. The `.tar.gz` contains all the sources needed
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

### Multiple distributions

Multiple distributions can be created with a single command:
```shell
python setup.py bdist_wheel sdist
```
This is particularly useful with tags.

### Tags

If you are planning on uploading your distributions to PyPI or test.PyPI, you
must ensure that it has a unique version number.
Neither site allows you to upload the same same source distribution twice,
even if you have deleted a version.

By default, the version is that given in the `setup.py`.
You add a suffix to this command by including `egginfo -b <tag>` where the tag
is either one of the letters a (for alpha), b (for beta), or c (for release
candidate). The digit can optionally be followed by a number. 

Hence a series of releases can be created by
```
python setup.py egg_info -b a1 sdist bdist_wheel
```
```
python setup.py egg_info -b a2 sdist bdist_wheel
```
etc. without causing a naming conflict at the distribution sites.

## UPLOADING A DISTRIBUTION TO PyPI

Although `setup.py` supports the command `upload`, this usage has been deprecated.
You should instead use twine.

The distributions you created above will be in a subdirectory `dist/`. 

You upload a distribution to test.pypi
```shell
twine upload --repository testpypi <file1>, <file2>, <file3>, ...
```
(`--repository` can be shorted to `-r`)
You upload a distribution to the main PyPI repository by simply running
```shell
twine upload <file1>, <file2>, ...
```
In either case, you will be asked for your name and password.
The name and password for test.pypi are separate from the name and password for the
main PyPI repository.

You can create the following file at `~/.pypirc`
```
[distutils]
index-servers =
    pypi
    testpypi

[pypi]
repository = https://upload.pypi.org/legacy/
username = your_pypi_username
password = your_pypi_password

[testpypi]
repository = https://test.pypi.org/legacy/
username = your_test_pypi_usename
password = your_test_pypi_password
```
Be sure to make this file publicly unreadable since it contains your passwords.
