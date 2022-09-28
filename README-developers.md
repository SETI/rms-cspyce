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
Instead the build process downloads the appropriate sources from
[NAIF](https://naif.jpl.nasa.gov/naif/toolkit.html).
The current SPICE Toolkit version is N0067, released January 3, 2022.

## BUILDING CSPYCE
Whenever we use the program `python` as a command, we mean your specific Python
runtime. If you have multiple versions of Python installed on your computer,
you may need to be running `python2` and `python3`, or `python3.8` and
`python3.9`.

In general, our `.py` and `.c` sources should work across all implementations of 
Python beyond 2.7. However, there is no expectation of binary compatibility between
multiple versions.

### Step1: 

You must have swig and ane newer version (≥ 3.8) of Python3 running on 
your computer for the first step:
```shell
python3 setup.py generate
```
This step re-creates all the generated .py and .c files needed to implement
the interface between Python and the CSpice code.
This command will also determine what operating system and architecture you are running
on, and use this information to download the appropriate CSpice sources.
The downloaded sources will appear in two directories:
* pds-cspyce/cspice/\<os>-\<arch>/src
* pds-cspyce/cspice/\<os>-\<arch>/include

where `<os>` and `<arch>` indicate your machine's operating system and architecture.

### Step 2
You compile the c-implementation of the Spice library by running:
```shell
python setup.py build_clib
```
This will execute somewhat slowly because it is compiling several thousand files. 
You should only need to do this once.

### Step 3
You then build `cspyce` by running the command
```shell
python setup.py build_ext --inplace
```
It is particularly important that you execute this command using the same
version of Python that you are planning to use for running cspyce.
Python does not guarantee binary compatibility between Python versions.

If you modify any of the templates, you will need to re-run the "generate"
command above (using Python3) and the "build_ext" command.
The Python `setuptools` is not yet smart enough to understand dependencies.

### Step 4
Once you have built `cspyce`, you should confirm that it works.
```shell
python
> import cspyce
> cspyce.tkvrsn('toolkit')
'CSPICE_N0067'
```
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

## USING GITHUB TO CREATE A DISTRIBUTION

### One-time steps

#### Create an account on PyPI and Test PyPI

Follow the steps for creating a new account at [Test PyPI](https://test.pypi.org/)
and at [PyPi](https://pypi.org/)

#### Get Permission to access cspyce

Separate permission needs to be provided for both PyPI and Test PyPI.
For now, only Frank and Rob can do this.
They should visit these two URLs and add you as a collaborator.
- https://pypi.org/manage/project/cspyce/collaboration/
- https://test.pypi.org/manage/project/cspyce/collaboration


#### Create tokens for PyPI and Test PyPI

PyPI and Test PyPI have separate API tokens.

Visit each of the following two URLs in turn:
  - https://pypi.org/manage/account/token/
  - https://test.pypi.org/manage/account/token

For each of the URLs, 
1. Fill in the two fields. The token name can be whatever you want.
The scope should be `Project: cspyce`
2. Click "Add token"
3. Keep a copy of the text that is generated. This is your API Token.


####  (Optional) Update your `.pypirc` file.

You can use the tokens created in the previous step in your `~/.pypirc` configuration
file rather than a username and password.
Use `__token__` as the username and the appropriate token generated above as the
password.

#### Tell GitHub these secrets.

1. Log into your github repository for pds-cspyce
2. Click "settings", then "secrets" on the left-hand menu, then "actions".
3. Use the "New Repository Secret" button to add two secrets named `PYPI_API_TOKEN` 
and `TEST_PYPI_API_TOKEN`. 
The value of each of these two secrets should be the appropriate API token
generated above.

### Creating a new distribution.

#### Step 1: Update the version

When you are planning on creating a pull request that requires a new distribution, make
sure that you update the version number in `setup.py`.
The version number appears in the `do_setup()` function at the very end of the file.

> Note to Rob: When approving a request that will require making a new distribution, 
> ensure that the version number is updated.
> 
#### Step 2: Create a new branch

Make a new branch that is a clone of the pull request. 
I've been calling my clone `GitActions` (and will use that name in the rest of this
document).

Do the following:

  1. You should have a local copy of the pull request.
If you are the creator of the pull requestion, then you should already have it.
If you are not the creator, then do a pull of the pull request.  (Instructions?)

  2. If you already have a branch named `GitActions`, then in GitKraken, checkout that
branch, then right click on the branch you want to clone, then select
"Reset GitActions to this branch" and "hard".

  3. If you do not already have a branch named `GitActions`, then checkout the branch
that you want to clone, right click on it and select "Create branch here" and give it
the name `GitActions`.
  

#### Step 3: Modify the version.

You should first try releasing to Test PyPI before attempting to release to the public. 
Each release needs a separate version number.

Ensure that you are in the branch `GitActions` or whatever you named your clone.

Modify the version number in `setup.py`.
If the version number is, for example `2.0.5`, change it to `2.0.5a1` indicating
that this is the alpha-1 version of 2.0.5.
If you find problems in your alpha-1 release
and create a second Test PyPI, the versions should be `2.0.5a2`, `2.0.5a3`, etc.
If you feel like you're getting close to the public release version,
switch from alpha to beta by changing the
`a` to a `b` and start the numbering again from 1.

#### Step 4: Modify the actions file

Modify the file `.github/workflows/publish_to_pypi.yml´ as follows:

If you named your clone branch something other than `GitActions`, modify the two
occurrences of `GitActions` in the file to be the name of your branch.

Change the line (approximately line 17)
```
    if: github.repository == 'fyellin/pds-cspyce'
```
to be the name of your github repository.

Change the second line of 
```
      - name: Publish distribution to PyPI
        if: true
```
to
```
      - name: Publish distribution to PyPI
        if: false
```
We are not performing the public release to PyPI yet.

By default, we generate four MacOS builds (2.7, 3.8, 3.9, 3.10), three Windows
builds (3.8, 3.9, 3.10), three Linux builds (3.8, 3.9, 3.10), and a source build.
Fell free to comment out the obvious lines if needed.

> When new Python images become available, modify the above list in the `master` version of this file.
>
> Note that 3.10 needs to be quoted because yml thinks 3.10 is just 3.1.
> When 3.11 is released, this shouldn't be a problem

#### Step 5: Commit and push to GitHub

Commit the changes to `setup.py` and `publish_to_pypi.yml`.
Push the changes to your github workspace.

Note that if you updated `GitActions` by doing a hard reset in Step 2, you may get an 
error when doing the push. Perform a `push --force` and ignore the warnings.

#### Step 6: Verify actions

Log into GitHub.
Go to your workspace and click 'Actions'.
Within a few minutes,
you should see your actions being run.

You *will* see the error message that Python 2.7 isn't supported; thse can be ignored.
If there are any other errors, then investigate.

#### Step 7: Test and retry

Test the results.  If there are any problems, fix them.  Ensure that `GitActions` and
the pull request stay in sync, and that the only difference between the two branches
are the version number (which must be updated each time you do a new release) and the
changes to `publush_to_pypi.yml`.  Each time you do a push to GitHub, a new release
will be build.

#### Step 8: Publish to PyPI

Once everything is working, undo the change to the version number in `setup.py`
and change the `false` back to `true` in `publish_to_pypi.yml`.  
Perform one more commit and push.  

