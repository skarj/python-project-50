#!/usr/bin/env python3

from gendiff import cmd
import json

def main():
    args = cmd.get_args()
    file1 = args.first_file
    file2 = args.second_file

    json1 = json.load(open(file1))
    json2 = json.load(open(file2))

    print(json1, json2)

if __name__ == '__main__':
    main()
