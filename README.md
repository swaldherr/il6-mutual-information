Mutual information analysis of IL-6 induced JAK/STAT signalling
===============================================================

In order to validate the program dependencies, it is recommended to
first work with the test dataset. This can be done with the following
commands:

```
python src/load_data.py -v -d data/test-data/
python main.py -d data/test-data/
```

During the computations, a number of mutual information results should
be printed on the command line. Also, scatter plots of the data will
be created in a subfolder of the ``results`` directory. If that works,
one can then choose one of the actual data folders under the directory
``rawdata`` to work with.

For example, to compute the mutual information from the datasets
stored in ``"rawdata/MEF/90 min"``, the following commands should be used:

```
python src/load_data.py -v -d "rawdata/MEF/90 min/" -x
python main.py -d "rawdata/MEF/90 min/"
```

In all cases, running ``src/load_data.py`` will only be required once
for each data folder.

