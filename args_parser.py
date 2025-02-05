import argparse
from argparse import Namespace


def cli_args() -> Namespace:
    parser = argparse.ArgumentParser(description='Optimize distribution costs for a retail chain.')
    parser.add_argument('--input-file', type=str, required=True, help='Path to the input JSON file')
    parser.add_argument('--visualise', action='store_true', help='Visualise the results')

    return parser.parse_args()
