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
Instead, the build process downloads the appropriate sources from
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
You compile the C implementation of the SPICE library by running:
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
version of Python that you are planning to use for running `cspyce`.
Python does not guarantee binary compatibility between Python versions.

If you modify any of the templates, you will need to re-run the "generate"
command above (using python3) and the "build_ext" command.
The Python `setuptools` module is not yet smart enough to understand
dependencies.

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
to confirm that you are looking at the `cspyce` you have just built rather than
the pip-installed `cspyce`.
The value returned should be `"<your current directory>/cspyce/__init__.py"`

## CREATING A DISTRIBUTION

### Before you begin

Make sure you have the latest versions of the necessary Python software:
```shell
python -m pip install --upgrade pip setuptools wheel twine
```
### Source Distributions

The simplest type of distribution is a source distribution:

```
python setup.py sdist
```
This will create a file named `dist/cspyce-<version>.tar.gz`.
This file can be uploaded to PyPI and then downloaded by any version of
Python on any operating system. The `.tar.gz` contains all the sources needed
to compile and run `cspyce`.
It includes the necessary pieces of the `cspice/` source tree as well as an
already generated `cspyce0_wrap.c` file so that the end user does not need to
install `swig.`

Although building a source distribution is very quick,
the installing process (`pip install cspyce`) may take a few minutes because
2000 files from the CSPICE library are being compiled.

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
is either one of the letters a (for alpha), b (for beta), or rc (for release
candidate). The letter can optionally be followed by a number.

Hence, a series of releases can be created by

      python setup.py egg_info -b a1 sdist bdist_wheel
      python setup.py egg_info -b a2 sdist bdist_wheel

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
You should have already installed `twine` above.

The distributions you created above will be in a subdirectory `dist/`.

You upload a distribution to test.pypi by running:
```shell
twine upload --repository testpypi <file1>, <file2>, <file3>, ...
```
(`--repository` can be shortened to `-r`)

You upload a distribution to the main PyPI repository by simply running
```shell
twine upload <file1>, <file2>, ...
```
In either case, you will be asked for your name and password.
The name and password for test.pypi are separate from the name and password for the
main PyPI repository.

You can create the following file at `~/.pypirc`

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

Be sure to make this file publicly unreadable since it contains your passwords.

## USING GitHub TO CREATE A DISTRIBUTION

### One-time steps

#### Create an account on PyPI and Test PyPI

Follow the steps for creating a new account at [Test PyPI](https://test.pypi.org/)
and at [PyPi](https://pypi.org/)

#### Get Permission to access cspyce

If necessary, contact the owner of the destination package on PyPi to be added
as a collaborator.

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

#### (Optional) Update your `.pypirc` file

You can use the tokens created in the previous step in your `~/.pypirc` configuration
file rather than a username and password.
Use `__token__` as the username and the appropriate token generated above as the
password.

#### Tell GitHub these secrets

1. Log into your GitHub repository for pds-cspyce
2. Click "settings", then "secrets" on the left-hand menu, then "actions".
3. Use the "New Repository Secret" button to add two secrets named `PYPI_API_TOKEN`
and `TEST_PYPI_API_TOKEN`.
The value of each of these two secrets should be the appropriate API token
generated above.

#### (Optional) Install `gh`, the GitHub command-line interface

The GitHub commands to run the actions can be executed either using a
command-line interface (CLI), or by visiting the GitHub website.

To use the CLI, visit https://github.com/cli/cli for information on
installing `gh` on your machine.

After installation, you must run the command `gh auth login` and follow the instructions to
authorize `gh` to access your account.

### Creating a new distribution

#### Step 1: Update the version

When you are planning on creating a pull request that requires a new distribution, make
sure that you update the version number in `setup.py`.
The version number appears in the `do_setup()` function at the very end of the file.

> Note to Rob: When approving a request that will require making a new distribution,
> ensure that the version number is updated.
>
#### Step 2: Ensure you have a local branch

Make sure you have a local branch that points to the commit where you want to create the distribution.

If you are the creator of the development branch, then you are done.
If you are not the creator, then do a pull of the development branch from the GitHub repository.

#### Step 3: Understand version numbers

You should first try releasing alpha and beta versions of your code to Test PyPI
before attempting to release to the public. Each release needs a separate version number.

You can find the version number in `setup.py`.

If the version number is, for example, `2.0.5`, we would want the first release sent to
Test PyPI to be `2.0.5a1` indicating that this is the alpha-1 version of 2.0.5.
This would be followed by `2.0.5a2`, `2.0.5a3`, etc.

As we got closer to a final version, we would change `a` to `b`, and restart the numbering
from 1, indicating we are at beta.  Then we would change the `b` to `rc`, indicating that
this is a release candidate (again, restarting the numbering from 1).

We call the suffix you append to the `version` listed in `setup.py`
as the "Prerelease Version".

#### Step 4: Build a Test PyPI release

Ensure that your development branch is committed and pushed to your GitHub repository,
including setting the appropriate version number in `setup.py`.

If using the GitHub web interface,

   1. Log into your GitHub account.
   2. Select your repository.
   3. Click the Actions "Button".
      You may see a message saying that actions aren't being run in this forked repository.
      If so, just click on "I understand" to continue.
   4. On the left-hand side, you will see "All Workflows" followed by "Publish to PyPI".
      Click on that entry.
   5. Click "Run Workflow".
   6. Fill in the form:
      1. Select your development branch.
      2. Set "Prerelease Version" to be "a2" or "b0" or whatever is the current
         prerelease version as described in the previous step.
      3. Leave the checkboxes as is. For debugging, you want to release only to Test PyPI.
   7. Click Run workflow

If using the CLI, run the following command:

```shell
gh workflow run publish-to-pypi.yml --ref <branch> -f prerelease_version=<xx> -f test_pypi=true -f pypi=false
```

where `<branch>` is the name of your development branch and `<xx>` is the prerelease version
as described above.

When you create a new workflow, using either the GUI or the CLI,
a new line will appear on the table of the Actions page.
Click on the left side of a row, and it will take you to a page showing the status of
the run.

You *may* see the several error messages that Python 2.7 isn't supported;
these can be ignored.
If you see any other error messages, please investigate.
Otherwise, your build has been released to TestPyPI.

#### Step 5: Test and retry

Test the results.

You should generally create a new virtual environment for testing a prerelease cspyce.

      $ python -m venv tester
      $ source tester/bin/activate
      $ pip install numpy
      $ pip install -i https://test.pypi.org/simple/ cspyce==2.0.5a1
      $ python
      > import cspyce

Of course, replace `2.0.5a1` with your current pre-release version number.

> Note: For release images on PyPI, `numpy` is installed automatically when installing
> `cspyce`.  This does not work when installing from Test PyPI.
>
If there are any problems, fix them.

Repeat Steps 4 and 5 as many times as necessary.
Remember that you need to update the value of the prerelease version  in step 6.2
each time you create a new release.

#### Step 6: Publish to PyPI

Repeat the instructions of Step 4, but fill in the form as follows:

  6. Fill in the form:
     1. Select your appropriate branch
     2. Set "Prerelease Version" to be the string `release`
     3. Click both "Release to PyPI" and "Release to Test PyPI"

If using the CLI, run the following command:
```
gh workflow run publish-to-pypi.yml --ref <branch> -f prerelease_version=release -f test_pypi=true -f pypi=true
```
where `<branch>` is the name of your development branch and `<xx>` is the prerelease suffix
you would have entered in step 6.2 above.


> Note: I am trying to figure out how to get rid of "Release to PyPI" and make
> it depend on whether the prerelease version is "release" or not.
> No one's answered my question on stackoverflow yet.

> Note: It seems the "Prerelease Version" field cannot be empty.
> I would have liked
> to leave this empty for the release, but the GUI won't let me.

> Question: Should we *always* send a release to Test PyPI.
> I can't think of a reason
> not to, but it was easy enough to always have a button.
