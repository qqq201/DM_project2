from dataframe import *
import argparse

def main():
    df = Dataframe()

    parser = argparse.ArgumentParser()
    parser.add_argument("input", help="Input file", type=str)
    subparsers = parser.add_subparsers()

    parser_i = subparsers.add_parser('impute')
    parser_i.add_argument('--output', type=str)
    parser_i.set_defaults(function=df.impute)

    args = parser.parse_args()

    if args.input is not None:
        df.load_csv(args.input)
        df.switch_to_last('Species')

    args.function(args)


if __name__ == '__main__':
    main()
