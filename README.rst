*****
ECG-featurizer
*****

.. image:: /docs/source/img/ECG-featurizer_banner.png

A method to extract features from electrocardiographic recordings
=================================================================
The purpose of this package is to make tabular data from ECG-recordings by calculating many features. The package is built on WFDB [#]_ and NeuroKit2 [#]_.

.. image:: https://readthedocs.org/projects/ECG-featurizer/badge/?version=latest
   :target: https://ECG-featurizer.readthedocs.io/en/latest/?badge=latest
   :alt: Documentation Status


.. image:: https://travis-ci.org/ECG-featurizer/ECG-featurizer.svg?branch=master
   :target: https://travis-ci.org/ECG-featurizer/ECG-featurizer

.. image:: https://coveralls.io/repos/github/ECG-featurizer/ECG-featurizer/badge.svg?branch=master
   :target: https://coveralls.io/github/ECG-featurizer/ECG-featurizer?branch=master

.. image:: https://badge.fury.io/py/ECG-featurizer.svg
   :target: https://badge.fury.io/py/ECG-featurizer


.. image:: https://pypip.in/d/ECG-featurizer/badge.svg
        :target: https://pypi.python.org/pypi/ECG-featurizer/

.. image:: https://img.shields.io/github/forks/ECG-featurizer/ECG-featurizer.svg
   :alt: GitHub Forks
   :target: https://github.com/ECG-featurizer/ECG-featurizer/network

.. image:: https://img.shields.io/github/issues/ECG-featurizer/ECG-featurizer.svg
   :alt: GitHub Open Issues
   :target: https://github.com/ECG-featurizer/ECG-featurizer/issues

.. image:: http://www.repostatus.org/badges/latest/active.svg
   :alt: Project Status: Active - The project has reached a stable, usable state and is being actively developed.
   :target: http://www.repostatus.org/#active



Documentation:
--------------

.. code-block:: python

    from ECG-featurizer import featurize as ef

    # Make ECG-featurizer object
    Feature_object =ef.get_features()

    # Preprocess the data (filter, find peaks, etc.)
    My_features=Feature_object.featurizer(features=ecg_filenames,labels=labels,directory="./data/",demographical_data=demo_data)

features:
^^^^^^^^^
A numpy array of ECG-recordings in directory. Each recording should have a file with the recording as a time series and one file with meta data containing information about    the patient and measurement information. This is standard format for WFDB and PhysioNet-files [1]_ [#]_  

**Supported input files:**

 +-------------------+---------------------------+
 | **Input data**    | **Supported file format** |
 +-------------------+---------------------------+
 | ECG-recordings    | .dat files                |
 +-------------------+---------------------------+
 | Patient meta data | .hea files                |
 +-------------------+---------------------------+

labels:
^^^^^^^
A numpy array of labels / diagnoses for each ECG-recording. The length of the labels-array should have the same length as the features-array
.. code-block:: python

        len(labels) == len(features)
    
directory:
^^^^^^^^^^
A string with the path to the features. If the folder structure looks like this:
    
 | mypath
 | ├── ECG-recordings          
 | │   ├── A0001.hea
 | │   ├── A0001.dat
 | │   ├── A0002.hea
 | │   ├── A0002.dat
 | │   └── Axxxx.dat
    
then the feature and directory varaible could be:
    
.. code-block:: python
        features[0]
            "A0001"
        directory
            "./mypath/ECG-recordings/"
       
demographical_data:
^^^^^^^^^^^^^^^^^^^
The demographical data that is used in this function is *age* and *gender*. A Dataframe with the following 3 columns should be passed to the featurizer() function.
    
+---+---------+------------+-----------------+
|   | **age** | **gender** | **filename_hr** |
+===+=========+============+=================+
| 0 | 11.0    | 1          | "A0001"         |
+---+---------+------------+-----------------+
| 1 | 57.0    | 0          | "A0002"         |
+---+---------+------------+-----------------+
| 2 | 94.0    | 0          | "A0003"         |
+---+---------+------------+-----------------+
| 3 | 34.0    | 1          | "A0004"         |
+---+---------+------------+-----------------+
    
The strings in the *filename_hr* -column should be the same as the strings in the feature array.
In this example gender is OneHot encoded such that
 .. math::
     1 = Female 
     0 = Male
        
Installation
-------------

To install ECG-featurizer, run this command in your terminal:

.. code-block::

    pip install ECG-featurizer

Contributing
------------

|GPLv3 license|

.. |GPLv3 license| image:: https://img.shields.io/badge/License-GPLv3-blue.svg
   :target: http://perso.crans.org/besson/LICENSE.html



Tutorials:
^^^^^^^^^^

-  `A tutorial will come <https://github.com/ECG-featurizer/ECG-featurizer/blob/main/docs/source/index.rst>`_



Other examples:
^^^^^^^^^^^^^^^

-  `Some examples will come <https://github.com/ECG-featurizer/ECG-featurizer/blob/main/docs/source/index.rst>`_


Citation:
^^^^^^^^^




Popularity:
-----------

.. image:: https://img.shields.io/pypi/dd/ECG-featurizer
        :target: https://pypi.python.org/pypi/ECG-featurizer

.. image:: https://img.shields.io/github/stars/ECG-featurizer/ECG-featurizer
        :target: https://github.com/ECG-featurizer/ECG-featurizer/stargazers

.. image:: https://img.shields.io/github/forks/ECG-featurizer/ECG-featurizer
        :target: https://github.com/ECG-featurizer/ECG-featurizer/network

References:
-----------

.. [#] WFDB: https://github.com/MIT-LCP/wfdb-python
.. [#] Makowski, D., Pham, T., Lau, Z. J., Brammer, J. C., Lesspinasse, F., Pham, H.,
  Schölzel, C., & S H Chen, A. (2020). NeuroKit2: A Python Toolbox for Neurophysiological
  Signal Processing. Retrieved March 28, 2020, from https://github.com/neuropsychology/NeuroKit
.. [#] Goldberger AL, Amaral LAN, Glass L, Hausdorff JM, Ivanov PCh, Mark RG, Mietus JE, Moody GB, Peng CK, Stanley HE. PhysioBank, PhysioToolkit, and PhysioNet: Components of a New Research Resource for Complex Physiologic Signals. Circulation 101(23):e215-e220 [Circulation Electronic Pages; http://circ.ahajournals.org/content/101/23/e215.full]; 2000 (June 13). PMID: 10851218; doi: 10.1161/01.CIR.101.23.e215

