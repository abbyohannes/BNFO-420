#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec  2 19:52:28 2025

@author: hannah
"""

import pandas as pd
from itertools import product

# --- Your IUPAC map here ---
IUPAC_MAP = {
    "A": ["A"],
    "T": ["T"], 
    "C": ["C"], 
    "G": ["G"],
    "R": ["A", "G"], 
    "Y": ["C", "T"], 
    "S": ["G", "C"], 
    "W": ["A", "T"],
    "M": ["A", "C"], 
    "K": ["G", "T"], 
}

def expand_ambiguous_sequence(seq, max_expansions=10):
    seq = seq.upper()
    possibilities = [IUPAC_MAP[base] for base in seq]

    # Use generator instead of full list to reduce memory
    expanded_gen = product(*possibilities)

    # Only take the first max_expansions outputs
    expanded_limited = [''.join(p) for _, p in zip(range(max_expansions), expanded_gen)]

    return expanded_limited

# --- Load the CSV ---
df = pd.read_csv("/lustre/home/keenholdhc/nucleotide-transformer/Clean_sequences_labeled1.csv")

all_expanded_sequences = []
all_expanded_labels = []

for seq, label in zip(df["sequences"], df["label"]):
    expanded = expand_ambiguous_sequence(seq, max_expansions=10)

    all_expanded_sequences.extend(expanded)
    all_expanded_labels.extend([label] * len(expanded))

print("Total expanded sequences:", len(all_expanded_sequences))
# --- Export to combined CSV ---
combined_df = pd.DataFrame({
    "sequence": all_expanded_sequences,
    "label": all_expanded_labels
})

output_path = "/lustre/home/keenholdhc/nucleotide-transformer/Expanded_Limited_Sequences.csv"
combined_df.to_csv(output_path, index=False)

print("Saved file to:", output_path)
print("Final rows written:", len(combined_df))