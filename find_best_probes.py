#!/usr/bin/python

import sys
import csv
import argparse
import numpy as np

import aibs

def find_best_probes(gene_probes, values):
    out_probes = []
    for gene_id, probes in gene_probes.iteritems():
        probe_indices = [ p['index'] for p in probes ]
        num_probes = len(probe_indices)

        out_probe = probes[0]
        if num_probes > 1:
            probe_values = values[probe_indices, :]

            cor = np.corrcoef(probe_values)
            meancor = np.mean(cor, axis=0)
            maxrow = np.argmax(meancor, axis=0)

            out_probe = probes[maxrow]

        out_probes.append(out_probe)    

    return out_probes

def main():
    parser = argparse.ArgumentParser(description="Create a CSV file that lists one probe (the 'median' probe) for every gene.")
    parser.add_argument('probes_csv', help="path to Probes.csv")
    parser.add_argument('expression_csv', help="path to MicroarrayExpression.csv")
    parser.add_argument('output_csv', help="output .csv file name")

    args = parser.parse_args()

    print "Reading Expression Values"
    values = aibs.read_expression_values(args.expression_csv)

    print "Reading Probes"
    probes, gene_probes = aibs.read_probes(args.probes_csv)

    print "Finding Best Probes"
    out_probes = find_best_probes(gene_probes, values)

    print "Writing " + args.output_csv
    with open(args.output_csv, 'w') as outfile:
        print>>outfile, "probe_id,array_index"
        for probe in out_probes:
            print>>outfile, ','.join([probe['probe_id'], str(probe['index'])])

if __name__ == "__main__":
    main()
