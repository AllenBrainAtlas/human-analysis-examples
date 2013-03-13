Human Brain Atlas Analysis Example Code
=======================================

This repository contains some simple analysis code that can be run on Human Brain Atlas data.

Sample Correlation
------------------

This is a python example that computes the gene expression correlation between all samples from a single donor. There is also a script for generating a heatmap of the matrix. It specifically runs on the contents of any of the donor zip files found here: http://human.brain-map.org/static/download/. 

To run this example, first unzip the data for one of the donors.  Then run the following:

    $ python compute_sample_correlation.py -p Probes.csv MicroarrayExpression.csv correlation.npz
    $ python make_heatmap.py -o Ontology.csv -s SampleAnnot.csv correlation.npz heatmap.png

Find the Best Probes for a Gene
-------------------------------

Inside the python directory You'll see find_best_probes.py.  This is a function used by compute_sample_correlation.py to pick one probe per gene to be used during correlation computation.  You can run it directly as follows:

   $ python find_best_probes.p Probes.csv MicroarrayExpression.csv best_probes.csv

All of the python code has been tested with python 2.7.3 and requires the following libraries to be installed:

* numpy
* scipy
* matplotlib




