
ECG-featurizer
--------------

.. image:: /docs/source/img/ECG-featurizer_banner.png

**A method to extract features from electrocardiographic recordings**


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



Code Example
------------

.. code-block:: python

    from ECG-featurizer import featurize as ef

    # Make ECG-featurizer object
    Feature_object =ef.get_features()

    # Preprocess the data (filter, find peaks, etc.)
    My_features=Feature_object.featurizer(features=ecg_filenames,labels=labels,directory="./data/",demographical_data=demo_data)



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




Documentation
-------------


Tutorials
^^^^^^^^^^

-  `A tutorial will come <https://github.com/ECG-featurizer/ECG-featurizer/blob/main/docs/source/index.rst>`_



Other examples
^^^^^^^^^^^^^^

-  `Some examples will come <https://github.com/ECG-featurizer/ECG-featurizer/blob/main/docs/source/index.rst>`_




Citation
---------




Popularity
---------------------

.. image:: https://img.shields.io/pypi/dd/ECG-featurizer
        :target: https://pypi.python.org/pypi/ECG-featurizer

.. image:: https://img.shields.io/github/stars/ECG-featurizer/ECG-featurizer
        :target: https://github.com/ECG-featurizer/ECG-featurizer/stargazers

.. image:: https://img.shields.io/github/forks/ECG-featurizer/ECG-featurizer
        :target: https://github.com/ECG-featurizer/ECG-featurizer/network




