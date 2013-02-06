#!/usr/bin/python
import sys
import argparse
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.cm as cm

import aibs

LEGEND_STRUCTURE_IDS = [ '4009', '4220', '4249', '4180', '4084', '4132', '4275', '4391', '9001', '4696', '9131', '9512' ]
COLORMAP_RANGE = [ 0.9, 1.0 ]

def make_heatmap(samples, structures, data, output_file):

    # get meta data for the sample structures (order, color)
    sample_structures = [ structures[s['structure_id']] for s in samples ]
    
    sample_order = [int(s['graph_order']) for s in sample_structures]
    sample_order = np.argsort(np.array(sample_order))

    # get the rgb color values from the color hex triplet
    sample_colors = [ s['color_hex_triplet'] for s in sample_structures ]
    sample_colors = np.array([ [ int(c[0:2], 16) / 255.0, 
                                 int(c[2:4], 16) / 255.0, 
                                 int(c[4:6], 16) / 255.0] for c in sample_colors ])
    sample_colors = sample_colors[sample_order, :]

    # permute and clamp the data
    data = data[sample_order, : ][:, sample_order]
    np.clip(data, 0, 1, out=data)

    # lay out the figure
    mpl.rc('xtick', labelsize=10)
    mpl.rc('ytick', labelsize=10)
    fig = plt.figure(figsize=(10,10))
    
    # create the heatmap
    ax = fig.add_axes([ 0.15, 0.15, .7, .7 ]);
    heatmap = ax.imshow(data, aspect='auto')
    heatmap.set_clim(COLORMAP_RANGE)
    heatmap.set_cmap('hot')
    ax.axis('off')

    # create the heatmap colorbar
    cb2 = fig.add_axes([ 0.9, 0.15, .05, .7 ]);
    heatcb = plt.colorbar(heatmap, cax=cb2, orientation='vertical')
    heatcb.ax.set_xlabel('p')

    # create the left structure colorbar
    cb1 = fig.add_axes([ 0.05, 0.15, .05, .7 ]);
    structure_cm = mpl.colors.ListedColormap(sample_colors[::-1])
    norm = mpl.colors.Normalize(vmin=0, vmax=len(sample_structures)-1)
    structure_cb = mpl.colorbar.ColorbarBase(cb1, cmap=structure_cm, norm=norm, orientation='vertical')
    cb1.axis('off')
    
    # create the upper structure colorbar
    cb3 = fig.add_axes([ 0.15, 0.9, .7, .05 ]);
    structure_cm_h = mpl.colors.ListedColormap(sample_colors)
    structure_cb_h = mpl.colorbar.ColorbarBase(cb3, cmap=structure_cm_h, norm=norm, orientation='horizontal')
    cb3.axis('off')
    
    # create the title
    plt.suptitle('Sample-Sample Expression Correlation',
                 horizontalalignment='center',
                 verticalalignment='center',
                 fontsize=18)
    
    # create the structure color legend
    leg = fig.add_axes([0, 0, 1, .15]);
    leg.axis('off')
    legend_structures = [ structures[id] for id in LEGEND_STRUCTURE_IDS ]
    legend_rectangles = [ plt.Rectangle( ( 0 , 0 ), 1, 1, fc=("#"+s['color_hex_triplet'])) for s in legend_structures ]
    legend_labels = [ s['name'].strip('"') for s in legend_structures ]

    plt.legend(legend_rectangles, 
               legend_labels,
               loc='center',
               ncol=4,
               frameon=False,
               prop= {'size':12})
    
    # save the figure
    plt.savefig(output_file)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-o', '--ontology_csv', help="path to Ontology.csv", required=True)
    parser.add_argument('-s', '--samples_csv', help="path to SampleAnnot.csv", required=True)
    parser.add_argument('data_file', help="path to output of compute_sample_correlation.py")
    parser.add_argument('output_file', help="output image file name")

    args = parser.parse_args()

    # read the samples
    samples = aibs.read_samples(args.samples_csv)

    # read the structures
    structures = aibs.read_structures(args.ontology_csv)

    # read the data
    data = np.load(args.data_file)['arr_0']
    
    # make the heatmap
    make_heatmap(samples, structures, data, args.output_file)

if __name__ == "__main__":
    main()
