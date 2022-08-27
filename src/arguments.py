import argparse
import os


def get_args():
    parser = argparse.ArgumentParser()
    
    # data file
    parser.add_argument("--in_file", type=str, default=None, help='input file')
    parser.add_argument("--output_dir", type=str, default=None, help='output dir for clustering results')
    
    # similarity
    parser.add_argument("--k", type=int, default=2, help='k shingles')
    parser.add_argument("--threshold", type=float, default=0.5, help='threshold for simlilarity')
    parser.add_argument("--num_perm", type=int, default=128, help='num_perm for MinHashLSH')
    parser.add_argument("--short_length_bound", type=int, default=10, help='specially use k=1 to calculate minhash for texts whose length are less than short_length_bound')
    
    args = parser.parse_args()
    
    for k, v in vars(args).items():
        print(f"{k}: {v}")
        
    if not os.path.exists(args.output_dir):
        print(f'{args.output_dir} does not exist, create')
        os.makedirs(args.output_dir)
    
    return args