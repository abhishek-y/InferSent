#!/usr/bin/env python
import os
import torch
import argparse

import numpy as np


if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        prog='extract-features',
        description='Extract features from pretrained InferSent model')

    parser.add_argument('-g', '--glove-path', type=str, required=True,
                        help='Path to "glove.840B.300d.txt" file')
    parser.add_argument('-f', '--model-path', type=str, required=True,
                        help='Path to pretrained .pickle model file')
    parser.add_argument('-t', '--tokenize', action='store_true',
                        help='Passes tokenize=True to build_vocab()')
    parser.add_argument('-o', '--out-dir', type=str, required=True,
                        help='Output folder to save feature files')
    parser.add_argument('-c', '--cpu', action='store_true',
                        help='Use CPU instead of GPU.')
    parser.add_argument('-b', '--batch-size', type=int, default=64,
                        help='Batch size (default: 64)')
    parser.add_argument('files', nargs='+',
                        help='List of files to extract sentence embeddings')

    args = parser.parse_args()

    if args.cpu:
        model = torch.load(args.model_path, map_location=lambda s, l: s)
    else:
        model = torch.load(args.model_path)

    model.set_glove_path(args.glove_path)

    # Ensure directory
    if not os.path.exists(args.out_dir):
        os.makedirs(args.out_dir)

    # Read files and extract features
    for fpath in args.files:
        print('Reading file {}'.format(fpath))
        sents = []
        with open(fpath) as f:
            for line in f:
                line = line.strip()
                assert line, 'Empty line in {}'.format(fpath)
                sents.append(line)

        # Set output file name
        out_name = os.path.join(
            args.out_dir, "{}.embs.npy".format(os.path.basename(fpath)))

        # Build vocab
        print('Building vocabulary')
        model.build_vocab(sents, args.tokenize)

        # Get embeddings
        embs = model.encode(sents, tokenize=args.tokenize,
                            verbose=True, bsize=args.batch_size)

        print('Saving to {}'.format(out_name))
        np.save(out_name, embs)