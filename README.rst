=========
zmq_debug
=========


.. image:: https://img.shields.io/pypi/v/zmq_debug.svg
        :target: https://pypi.python.org/pypi/zmq_debug

.. image:: https://img.shields.io/travis/mmyros/zmq_debug.svg
        :target: https://travis-ci.com/mmyros/zmq_debug

.. image:: https://readthedocs.org/projects/zmq-debug/badge/?version=latest
        :target: https://zmq-debug.readthedocs.io/en/latest/?version=latest
        :alt: Documentation Status




Debugging zmq for open ephys


Basic usage
-----
0. Install dependencies: `pip install -r requirements.txt`
1. Start Open Ephys GUI
2. Open one of the datasets in `data` folder in Open Ephys' File reader
3. Add ZMQ Interface (keep default dataport of 5556)
4. Run `reporter_new.py` or `stream_zmq_minimap.py`
5. Press play on Open Ephys GUI
6. Use OrgVsStream.ipynb to visualize results

* Free software: MIT license
* Documentation: https://zmq-debug.readthedocs.io.


Features
--------

* TODO

Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
