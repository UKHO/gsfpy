# gsfpy - Generic Sensor Format for Python

![Python package](https://github.com/UKHO/gsfpy/workflows/Python%20package/badge.svg)

Python wrapper for the C implementation of the Generic Sensor Format library.

- Free software: MIT license

## Features

- gsfpy.bindings provides wrappers for all GSFlib functions, including I/O, utility and info functions.
  Minor exceptions are noted in the sections below.

- For added convenience the gsfpy top level package provides the following higher level abstractions:
  - `open_gsf()`
  - `GSFFile` (class)
  - `GSFFile.read()`
  - `GSFFile.get_number_records()`
  - `GSFFile.seek()`
  - `GSFFile.write()`
  - `GSFFile.close()`

## Install

```shell script
pip install git+ssh://git@github.com/UKHO/gsfpy.git@master
```

```shell script
pip install git+https://github.com/UKHO/gsfpy.git@master
```

## Examples of usage

### Open/close/read from a GSF file

```python
from ctypes import string_at

from gsfpy import open_gsf
from gsfpy.enums import RecordType

with open_gsf("path/to/file.gsf") as gsf_file:
    # Note - file is closed automatically upon exiting 'with' block
    _, record = gsf_file.read(RecordType.GSF_RECORD_COMMENT)

    # Note use of ctypes.string_at() to access POINTER(c_char) contents of
    # c_gsfComment.comment field.
    print(string_at(record.comment.comment))
```

### Write to a GSF file

```python
from ctypes import c_int, create_string_buffer

from gsfpy import open_gsf
from gsfpy.enums import FileMode, RecordType
from gsfpy.gsfRecords import c_gsfRecords

comment = "My comment"

# Initialize the contents of the record that will be written.
# Note use of ctypes.create_string_buffer() to set POINTER(c_char) contents.
record = c_gsfRecords()
record.comment.comment_time.tvsec = c_int(1000)
record.comment.comment_length = c_int(len(comment))
record.comment.comment = create_string_buffer(comment)

with open_gsf("path/to/file.gsf", mode=FileMode.GSF_CREATE) as gsf_file:
    gsf_file.write(record, RecordType.GSF_RECORD_COMMENT)
```

### Copy GSF records

```python
from ctypes import byref, c_int, pointer

import gsfpy
from gsfpy.enums import FileMode, RecordType
from gsfpy.gsfDataID import c_gsfDataID
from gsfpy.gsfRecords import c_gsfRecords


# This example uses gsfpy.bindings to illustrate use of the lower level functions
file_handle = c_int(0)
data_id = c_gsfDataID()
source_records = c_gsfRecords()
target_records = c_gsfRecords()

ret_val_open = gsfpy.bindings.gsfOpen(
    "path/to/file.gsf", FileMode.GSF_READONLY, byref(file_handle)
)

# Note use of ctypes.byref() as a shorthand way of passing POINTER parameters to
# the underlying foreign function call. ctypes.pointer() may also be used.
bytes_read = gsfpy.bindings.gsfRead(
    file_handle,
    RecordType.GSF_RECORD_COMMENT,
    byref(data_id),
    byref(source_records),
)

# Note use of pointer() rather than byref() when passing parameters to
# gsfCopyRecords(). Implementation of this function is in Python as calling
# the native underlying function causes memory ownership clashes. byref()
# is only suitable for passing parameters to foreign function calls (see
# ctypes docs).
ret_val_cpy = gsfpy.bindings.gsfCopyRecords(
    pointer(target_records), pointer(source_records)
)
ret_val_close = gsfpy.bindings.gsfClose(file_handle)
```

### Troubleshoot

```python
import gsfpy

# The gsfIntError() and gsfStringError() functions are useful for
# diagnostics. They return an error code and corresponding error
# message, respectively.
retValIntError = gsfpy.bindings.gsfIntError()
retValStringError = gsfpy.bindings.gsfStringError()
print(retValStringError)
```

## Notes on implementation

### gsfPrintError()

The `gsfPrintError()` method of GSFlib is not implemented as there is no
FILE* equivalent in Python. Use `gsfStringError()` instead - this will
give the same error message, which can then be written to file as
required.

### gsfCopyRecords() and gsfFree()

`gsfFree()` the sibling method to `gsfCopyRecord()` in GSFlib, used to
deallocate memory assigned by the library but managed by the calling
application, is not required by gsfpy as memory allocation and
deallocation is handled by ctypes. `gsfFree()` is therefore omitted from
the package.

### gsf_register_progress_callback()

Implementation of the GSFlib function
`gsf_register_progress_callback()` is not applicable for gsfpy as the
DISPLAY_SPINNER macro was not defined during compilation. It is
therefore omitted from the package.

## Generic Sensor Format Documentation

Generic Sensor Format specification: see e.g.
<https://github.com/schwehr/generic-sensor-format/blob/master/doc/GSF_lib_03-06.pdf>

Generic Sensor Format C library v3.06 specification: see e.g.
<https://github.com/schwehr/generic-sensor-format/blob/master/doc/GSF_spec_03-06.pdf>

More recent versions of these documents can be downloaded from the
[Leidos](https://www.leidos.com/products/ocean-marine) website.

## Dev Setup

### Pyenv (Recommended)

```shell script
git clone git@github.com:UKHO/gsfpy.git
cd gsfpy
pyenv install 3.8.3
pyenv virtualenv 3.8.3 gsfpy
pyenv local gsfpy
pip install -r requirements-dev.txt
```

### Virtualenv

```shell script
git clone git@github.com:UKHO/gsfpy.git
virtualenv gsfpy (--always-copy)
cd gsfpy
source bin/activate
pip install -r requirements-dev.txt
```

## Run tests

```shell script
make test
```

## Notes on Security

Some known concerns relating to the underlying GSFlib C library are
documented at <https://github.com/dwcaress/MB-System/issues/368> and
<https://github.com/schwehr/generic-sensor-format/issues>. Note that
gsfpy simply wraps GSFlib and does not purport to stop or mitigate these
potential vulnerabilities. It is left to the authors of applications
calling gsfpy to assess these risks and mitigate where deemed necessary.

GSF data processed using gsfpy should be sourced from reliable providers
and checked for integrity where possible.

Please also refer to the LICENSE file for the terms of use of gsfpy.

## Credits

`libgsf03-08.so` was built from the
[Leidos](https://www.leidos.com/products/ocean-marine) C code using the
Makefile in [UKHO/libgsf](https://github.com/UKHO/libgsf)

This package was created with
[Cookiecutter](https://github.com/cookiecutter/cookiecutter) and the
[UKHO/cookiecutter-pypackage](https://github.com/UKHO/cookiecutter-pypackage)
project template.

## Related Projects

Also see [schwehr/generic-sensor-format](https://github.com/schwehr/generic-sensor-format/)
