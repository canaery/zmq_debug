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
2. Open one of the datasets in `data` folder in Open Ephys' File readee (NOTE: ONLY 2022-10-20_11-45-33 dataset is currently working. Synthetic and 544 are currently openable in OE GUI, but not loadable with OE python library
3. Add ZMQ Interface (keep default dataport of 5556)
4. Run `stress_test_minimal.py` or `stream_zmq_minimap.py`
5. Press play on Open Ephys GUI now or before running `stress_test_minimal`
6. Use `compare_original_to_streamed.ipynb` to visualize results

Note two paths in the notebook:
streamed_path = Path('~/PycharmProjects/zmq_debug/zmq_data/').expanduser()
original_data_path = Path('~/PycharmProjects/zmq_debug/data/').expanduser()

and one path in the script:
path_out = Path('~/PycharmProjects/zmq_debug/zmq_data').expanduser()




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
