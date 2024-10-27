import os
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Redact a file')
    parser.add_argument('--names', type=bool, default=False, help='Redact names')
    parser.add_argument('--dates', type=bool, default=False, help='Redact dates')
    parser.add_argument('--phones', type=bool, default=False, help='Redact phone numbers')
    parser.add_argument('--addresses', type=bool, default=False, help='Redact addresses')
    parser.add_argument('--input', type=str, help='glob pattern for input files')
    parser.add_argument('--output', type=str, help='output directory')
    parser.parse_args()