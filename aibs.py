import csv
import numpy as np

def read_expression_values(file_name):
    values = np.loadtxt(open(file_name, 'rb'), delimiter=",")
    return np.delete(values, 0, 1);

def read_probes(file_name):
    probes = []

    with open(file_name, 'rb') as probesfile:
        reader = csv.DictReader(probesfile)
        probes = list(reader)    

    gene_probes = {}
    for i, probe in enumerate(probes):
        gene_id = probe['gene_id']
        probe_info = { 'probe_id': probe['probe_id'], 'index': i }
        if not gene_probes.has_key(gene_id):
            gene_probes[gene_id] = [probe_info]
        else:
            gene_probes[gene_id].append(probe_info)

    return probes, gene_probes

def read_structures(file_name):
    structures = {}

    with open(file_name, 'rb') as structures_file:
        reader = csv.DictReader(structures_file)
        structure_list = list(reader)
        structures = { s['id']: s for s in structure_list }

    return structures

def read_samples(file_name):
    samples = []
    with open(file_name, 'rb') as samplesfile:
        reader = csv.DictReader(samplesfile)
        samples = list(reader)    

    return samples

