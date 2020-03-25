================================
Generic Sensor Format for Python
================================


.. image:: https://github.com/UKHO/gsfpy/workflows/Python%20package/badge.svg
     :target: https://github.com/UKHO/gsfpy/actions?query=workflow%3A%22Python+package%22

Python wrapper for the C implementation of the Generic Sensor Format library.


* Free software: MIT license

Features
--------

* TODO

Install
-------

.. code-block:: bash

    SSH: pip install git+ssh://git@github.com/UKHO/gsfpy.git@master
    HTTPS: pip install git+https://github.com/UKHO/gsfpy.git@master

Examples of usage
-----------------

Open/close a GSF file
^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

    import gsfpy
    from ctypes import *
    from gsfpy.enums import FileMode

    mode = FileMode.GSF_READONLY
    c_int_ptr = POINTER(c_int)
    p_gsf_fileref = c_int_ptr(c_int(0))

    # Note - pass file paths as byte strings
    retValOpen = gsfpy.gsfOpen(b'path/to/file.gsf', mode, p_gsf_fileref)
    retValClose = gsfpy.gsfClose(p_gsf_fileref[0])


Read from a GSF file
^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

    import gsfpy
    from ctypes import *
    from gsfpy.enums import FileMode, RecordType

    mode = FileMode.GSF_READONLY
    c_int_ptr = POINTER(c_int)
    p_gsf_fileref = c_int_ptr(c_int(0))

    commentID = c_gsfDataID()
    commentID.recordID = c_uint(RecordType.GSF_RECORD_COMMENT.value)

    c_gsfDataID_ptr = POINTER(c_gsfDataID)
    p_dataID = c_gsfDataID_ptr(commentID)

    c_gsfRecords_ptr = POINTER(c_gsfRecords)
    p_rec = c_gsfRecords_ptr(c_gsfRecords())

    c_ubyte_ptr = POINTER(c_ubyte)
    p_stream = c_ubyte_ptr()

    retValOpen = gsfpy.gsfOpen(b'path/to/file.gsf', mode, p_gsf_fileref)
    bytesRead = gsfpy.gsfRead(p_gsf_fileref[0], c_int(RecordType.GSF_RECORD_COMMENT.value), p_dataID, p_rec, p_stream, 0)

    # Retrieve the value of a field from the comment that was read.
    # Note the use of ctypes.string_at() to get POINTER(c_char) contents.
    print(string_at(p_rec.contents.comment.comment))

    retValClose = gsfpy.gsfClose(p_gsf_fileref[0])

Write to a GSF file
^^^^^^^^^^^^^^^^^^^

.. code-block:: python

    import gsfpy
    from ctypes import *
    from gsfpy.enums import FileMode, RecordType

    createMode = FileMode.GSF_CREATE
    c_int_ptr = POINTER(c_int)
    p_gsf_fileref = c_int_ptr(c_int(0))

    commentID = c_gsfDataID()
    commentID.recordID = c_uint(RecordType.GSF_RECORD_COMMENT.value)

    c_gsfDataID_ptr = POINTER(c_gsfDataID)
    p_dataID = c_gsfDataID_ptr(commentID)

    # Initialize the contents of the record that will be written.
    # Note use of ctypes.create_string_buffer() to set POINTER(c_char) contents.
    c_gsfRecords_ptr = POINTER(c_gsfRecords)
    p_rec = c_gsfRecords_ptr(c_gsfRecords())
    p_rec.contents.comment.comment_time.tvsec = c_int(1000)
    p_rec.contents.comment.comment_length = c_int(17)
    p_rec.contents.comment.comment = create_string_buffer(b'My first comment')

    retValOpenCreate = gsfpy.gsfOpen(b'path/to/new-file.gsf', createMode, p_gsf_fileref)
    bytesWritten = gsfpy.gsfWrite(p_gsf_fileref[0], p_dataID, p_rec)
    retValClose = gsfpy.gsfClose(p_gsf_fileref[0])

Copy GSF records
^^^^^^^^^^^^^^^^

.. code-block:: python

    import gsfpy
    from ctypes import *
    from gsfpy.enums import FileMode, RecordType

    file_handle = c_int(0)
    data_id = c_gsfDataID()
    source_records = c_gsfRecords()
    target_records = c_gsfRecords()

    ret_val_open = gsfpy.bindings.gsfOpen(
        self.test_data_path, FileMode.GSF_READONLY, byref(file_handle)
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

Troubleshoot
^^^^^^^^^^^^

.. code-block:: python

    # The gsfIntError() and gsfStringError() functions are useful for
    # diagnostics. They return an error code and corresponding error
    # message, respectively.
    retValIntError = gsfpy.gsfIntError()
    retValStringError = gsfpy.gsfStringError()
    print(retValStringError)

Notes on implementation
-----------------------
gsfPrintError()
^^^^^^^^^^^^^^^
The gsfPrintError() method of GSFlib is not implemented as there is no FILE* equivalent in Python. Use gsfStringError() instead - this will
give the same error message, which can then be written to file as required.

gsfCopyRecords() and gsfFree()
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
gsfFree() the sibling method to gsfCopyRecord() in GSFlib, used to deallocate memory assigned by the library but managed by the calling application,
is not required by gsfpy as memory allocation and deallocation is handled by ctypes. gsfFree() is therefore omitted from the package.

gsf_register_progress_callback()
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Implementation of the GSFlib function gsf_register_progress_callback() is not applicable for gsfpy as the DISPLAY_SPINNER macro was not defined
during compilation. It is therefore omitted from the package.

Generic Sensor Format Documentation
-----------------------------------

Generic Sensor Format specification: see https://github.com/schwehr/generic-sensor-format/blob/master/doc/GSF_lib_03-06.pdf

Generic Sensor Format C library v3.06 specification: see https://github.com/schwehr/generic-sensor-format/blob/master/doc/GSF_spec_03-06.pdf

Dev Setup
---------

Pyenv (Recommended)
^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

    git clone git@github.com:UKHO/gsfpy.git
    cd gsfpy/
    pyenv install 3.8.1
    pyenv virtualenv 3.8.1 gsfpy
    pyenv local gsfpy
    pip install -r requirements-dev.txt

Virtualenv
^^^^^^^^^^

.. code-block:: bash

    git clone git@github.com:UKHO/gsfpy.git
    virtualenv gsfpy/ (--always-copy)
    cd gsfpy/
    source bin/activate
    pip install -r requirements-dev.txt

Run tests
---------

.. code-block:: bash

    make test

Credits
-------

C implementation of the GSF library provided by Leidos_ under the LGPL license v2.1.

libgsf03-08.so was built from the Leidos_ C code using Make scripts based on those from `schwehr/generic-sensor-format`_

This package was created with Cookiecutter_ and the `UKHO/cookiecutter-pypackage`_ project template.

.. _Leidos: https://www.leidos.com/products/ocean-marine
.. _`schwehr/generic-sensor-format`: https://github.com/schwehr/generic-sensor-format/
.. _Cookiecutter: https://github.com/cookiecutter/cookiecutter
.. _`UKHO/cookiecutter-pypackage`: https://github.com/UKHO/cookiecutter-pypackage
