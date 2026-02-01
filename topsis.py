import sys
import pandas as pd


def main():
    args = sys.argv

    if len(args) != 5:
        print("Error: Incorrect number of arguments.")
        print("Usage: python topsis.py <input_file> <weights> <impacts> <output_file>")
        sys.exit(1)

    input_file = args[1]
    weights_str = args[2]
    impacts_str = args[3]
    output_file = args[4]

    try:
        weights = list(map(float, weights_str.split(',')))
    except ValueError:
        print("Error: Weights must be numeric and comma-separated.")
        sys.exit(1)

    impacts = impacts_str.split(',')

    for impact in impacts:
        if impact not in ['+', '-']:
            print("Error: Impacts must be either '+' or '-'.")
            sys.exit(1)

    if len(weights) != len(impacts):
        print("Error: Number of weights and impacts must match.")
        sys.exit(1)

    try:
        df = pd.read_csv(input_file)
    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found.")
        sys.exit(1)

    if df.shape[1] < 3:
        print("Error: Input file must contain at least three columns.")
        sys.exit(1)

    numeric_df = df.iloc[:, 1:]
    numeric_df = numeric_df.apply(pd.to_numeric, errors='coerce')

    if numeric_df.isnull().values.any():
        print("Error: From second to last column, all values must be numeric.")
        sys.exit(1)

    print("Input file validated successfully.")


if __name__ == "__main__":
    main()