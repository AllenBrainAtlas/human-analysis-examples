#!/usr/bin/python
import sys
import argparse
import numpy as np

import aibs

from find_best_probes import find_best_probes

def main():
    parser = argparse.ArgumentParser(description="Compute a sample correlation matrix from a matrix of expression values.  Including --probes_csv causes this to only compute correlation values for one probe per gene (the 'median' probe).")
    parser.add_argument('-p','--probes_csv', help="path to Probes.csv.")
    parser.add_argument('expression_csv', help="path to MicroarrayExpression.csv")
    parser.add_argument('output_npz', help="output .npz file name")

    args = parser.parse_args()

    print "Reading Expression Values"
    values = aibs.read_expression_values(args.expression_csv)

    if args.probes_csv:
        print "Filtering Probes"
        probes, gene_probes = aibs.read_probes(args.probes_csv)
        best_probes = find_best_probes(gene_probes, values)
        
        best_probe_indices = np.array([ p['index'] for p in best_probes ])
        values = values[best_probe_indices, :]

        print values.shape

    values = np.transpose(values)
    
    print "Computing Sample Covariance"
    cov = np.corrcoef(values)
    
    print "Saving " + args.output_npz
    np.savez(args.output_npz, cov)
    
if __name__ == "__main__":
    main()
