# `cspyce` DEVELOPERS' GUIDE
March 2022

Frank Yellin.

This guide is intended for those who have downloaded the 
[GitHub source code](https://github.com/SETI/pds-cspyce/) and are modifying
or extending the `cspyce` toolkit.
You do not need to read this if you are installing an existing `PyPI`
distribition of the sources.

## SETTING UP

The root of the GitHub tree is called `pds-cspyce`.
When we use `pds-cspyce` in this document, we are referring to that directory,
wherever it happens to be on your computer.

The GitHub source code intentionally does not include the source code to
CSPICE itself.
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

You must have swig and a newer version (≥ 3.8) of Python3 running on 
your computer for the first step:
```shell
python3 setup.py generate
```
This step re-creates all the generated .py and .c files needed to implement
the interface between Python and the CSPICE code.
This command will also determine what operating system and architecture you are running
on, and use this information to download the appropriate CSPICE sources.
The downloaded sources will appear in two directories:
* pds-cspyce/cspice/\<os>-\<arch>/src
* pds-cspyce/cspice/\<os>-\<arch>/include

where `<os>` and `<arch>` indicate your machine's operating system and architecture.

### Step 2
You compile the C implementation of the Spice library by running:
```shell
python setup.py build_clib
```
This may execute somewhat slowly because it is compiling several thousand files. 
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
If you have previously installed cspyce via pip, you should also look at the value of
```shell
> cspyce.__file__
```
to confirm that you area loading at the cspyce you have just built rather than the
pip-installed cspyce.  The value returned should be 
`"<your current directory>/cspyce/__init.py"`

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
This will create a file named `dist/cspyce-<version>.tar.gz`.
This file can be uploaded to PyPI and then downloaded by any version of
Python on any operating system. The `.tar.gz` contains all the sources needed
to compile and run `cspyce`.
It includes the necessary pieces of the `cspice/` source tree as well as an
already generated `cspyce0_wrap.c` file so that they do not need to install 
`swig.`

The installing process may take a few minutes because 2000 files from the CSPICE
library are being compiled.

### Wheel distributions

A second type of distribution is the "wheel". 
```shell
python setup.py bdist_wheel
```

This will create a file in the `dist/` subdirectory with suffix `.whl` and
whose name indicates the Python version,
the operating system, and the operating system version.

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
Neither site allows you to upload the same source distribution twice,
even if you have deleted a version.

By default, the version is that given in `setup.py`.
You add a suffix to this command by including `egginfo -b <tag>` where the tag
is either one of the letters a (for alpha), b (for beta), or c (for release
candidate). The letter can optionally be followed by a number. 

Hence a series of releases can be created by
```
python setup.py egg_info -b a1 sdist bdist_wheel
```
```
python setup.py egg_info -b a2 sdist bdist_wheel
```
etc. without causing a naming conflict at the distribution sites.

## UPLOADING A DISTRIBUTION TO PyPI

> These instructions do not work for wheels built on Linux. PyPI and TestPyPI have
> special rules for Linux to ensure that Linux releases can work on all the various
> versions of Linux.  
> 
> You can continue to use Linux wheels on your own computer. 
> Releases must be built on GitHub.
> See the next section.


Although `setup.py` supports the command `upload`, this usage has been deprecated.
You should instead use `twine`.
You should already have installed `twine` above.

The distributions you created above will be in a subdirectory `dist/`. 

You upload a distribution to test.pypi by running:
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

## USING GitHub TO CREATE A DISTRIBUTION

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

1. Log into your GitHub repository for pds-cspyce
2. Click "settings", then "secrets" on the left-hand menu, then "actions".
3. Use the "New Repository Secret" button to add two secrets named `PYPI_API_TOKEN` 
and `TEST_PYPI_API_TOKEN`. 
The value of each of these two secrets should be the appropriate API token
generated above.

#### (Optional) Install `GH`, the GitHub command-line interface

The GitHub commands to run the necessary actions can be executed either using a 
command-line interface (CLI), or by visiting the github website.

If you want to use the CLI, visit https://github.com/cli/cli for information on 
installing `gh` on your machine.

After installation, run the command `gh auth login` and follow the instructions to 
authorize `gh` to access your account.

### Creating a new distribution.

#### Step 1: Update the version

When you are planning on creating a pull request that requires a new distribution, make
sure that you update the version number in `setup.py`.
The version number appears in the `do_setup()` function at the very end of the file.

> Note to Rob: When approving a request that will require making a new distribution, 
> ensure that the version number is updated.
> 
#### Step 2: Ensure you have a local branch.

Make sure you have a local branch that points to the same commit as th development branch.

If you are the creator of the branch, then you are done.  If you are not the creator, 
then do a pull of the development branch from the GitHub repository.

#### Step 3: Modify the version.

You should first try releasing to Test PyPI before attempting to release to the public. 
Each release needs a separate version number.

Ensure that you are the development branch

Modify the version number in `setup.py`.
If the version number is, for example `2.0.5`, change it to `2.0.5a1` indicating
that this is the alpha-1 version of 2.0.5.
If you find problems in your alpha-1 release
and create a second Test PyPI, the versions should be `2.0.5a2`, `2.0.5a3`, etc.
If you feel like you're getting close to the public release version,
switch from alpha to beta by changing the
`a` to a `b` and start the numbering again from 1.

#### Step 4: Build a Test PyPI release

By default, we generate four MacOS builds (2.7, 3.8, 3.9, 3.10), three Windows
builds (3.8, 3.9, 3.10), three Linux builds (3.8, 3.9, 3.10), and a source build.
Feel free to comment out the obvious lines if needed.

> When new Python images become available, modify the above list in the `master` version of this file.
>
> Note that 3.10 needs to be quoted because yml thinks 3.10 is just 3.1.
> When 3.11 is released, this shouldn't be a problem

Commit and push the changes you made in the previous step. 

If using web interface, 

1. Log into your GitHub account, 
2. Select your repository,
3. Click the Actions "Button"
4. On the left-hand side, you will see "All Workflows" followed
by an entry whose name starts with "Public Python Distribution".  Click on the entry.
5. Click "Run Workflow". Leave the checked boxes alone.  Select the appropriate branch.
6. Click the green "Run Workflow" button.

If using the CLI command, run the following command:

```
gh workflow run publish-to-pypi.yml --ref <branch> -f pypi=false
```


#### Step 6: Verify actions

Log into GitHub.
Go to your repository and click 'Actions'.
Within a few minutes,
you should see your actions being run.

You may see a message saying that actions aren't being run in this forked repository.
If so, just click on "I understand" to continue.

You *will* see the error message that Python 2.7 isn't supported; thse can be ignored.
If there are any other errors, then investigate.

#### Step 7: Test and retry

Test the results.  If there are any problems, fix them.  Ensure that `GitActions` and
the development branch stay in sync, and that the only difference between the two branches
are the version number (which must be updated each time you do a new release) and the
changes to `publush_to_pypi.yml`.  Each time you do a push to GitHub, a new release
will be build.

#### Step 8: Publish to PyPI

Once everything is working, undo the change to the version number in `setup.py`
and change the `false` back to `true` in `publish_to_pypi.yml`.
Do not change back the branch name (if you changed it) or the repository name.
Perform one more commit and push.  

