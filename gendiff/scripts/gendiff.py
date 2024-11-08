#!/usr/bin/env python3

from gendiff.generate_diff import get_args, generate_diff


def main():
    args = get_args()

    print(generate_diff(args.first_file, args.second_file))


if __name__ == '__main__':
    main()
