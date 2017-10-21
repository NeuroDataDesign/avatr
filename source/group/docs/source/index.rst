.. NeuroData Annotation documentation master file, created by
   sphinx-quickstart on Sun Oct 15 23:15:51 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to NeuroData Annotation's documentation!
================================================

1. Clone annotation repo. In Terminal type:
    ``git clone https://github.com/rguo123/NeuroData_Annotate.git``

2. Install dependences by typing: ``pip3 install -r requirements.txt``

3. Get BOSS API token by logging in to https://api.boss.neurodata.io/. Note: You need resource manager permissions to upload data to the BOSS.

4. Create ``neurodata.cfg`` file and insert BOSS token as shown below:

  .. code-block:: bash
     :emphasize-lines: 4

     [Default]
     protocol = https
     host = api.boss.neurodata.io
     token = INSERT TOKEN HERE

  .. toctree::
     :maxdepth: 2
     :caption: Contents:

5. Pull data from BOSS by typing ``python3 NeuroDataResource.py`` in terminal and following the input prompt.

.. figure::  images/ndr_show.png
   :align:   center

6. Annotate (FIJI demo incoming)

7. To push annotations to the BOSS, edit ``gen_commands.py`` file and input annotation file parameters.

8. Once all inputs are filled out, type ``python3 gen_commands.py`` in terminal.

9. Paste command line output into terminal.

10. Pray it works.

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
