#!/usr/bin/env python

'''
Script that checks for the presence of a primer in a fasta.
'''

import argparse, itertools, sys, tempfile, subprocess
from SmileTrain import util, util_primer
from Bio import Seq


if __name__ == '__main__':
    # parse command line arguments
    parser = argparse.ArgumentParser(description='Look at every Nth entry and try to find the primer', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('fastq', help='input fastq file')
    parser.add_argument('primer', help='primer sequence')
    parser.add_argument('-l', '--log_frac', type=int, default=4, help='negative logarithm of fraction of sequences to take')
    parser.add_argument('-m', '--max_primer_diffs', default=0, type=int, help='maximum number of nucleotide mismatches in the primer')
    parser.add_argument('-c', '--reverse_complement', action='store_true', help='take reverse complement of primer?')
    parser.add_argument('-o', '--output', default=sys.stdout, type=argparse.FileType('w'), help='output file')
    
    args = parser.parse_args()

    # get the number of entries in the original file
    n_lines = int(subprocess.check_output(['wc', '-l', args.fastq]).split()[0])
    n_entries = n_lines / 4
    frac = 10 ** -args.log_frac
    skip = int(frac * n_lines)

    # reverse complement if desired
    if args.reverse_complement:
        args.primer = str(Seq.Seq(args.primer).reverse_complement())
    
    print "of %s entries, taking ~%s, or every %s-th" %(n_entries, frac, skip)
    
    r = util_primer.PrimerRemover(args.fastq, args.primer, args.max_primer_diffs, skip=skip)
    r.check_entries()
    
    args.output.write(r.diagnostic_message())
