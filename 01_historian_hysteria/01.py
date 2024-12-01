#!/usr/bin/env python3
import argparse
from typing import Tuple, List
from pathlib import Path
from collections import Counter

def read_input(filename: str | Path) -> Tuple[List[int], List[int]]:
    lists: List[List[int]] = []
    try:
        with open(filename, 'r') as file:
            for line in file:
                row = [int(item) for item in line.split()]
                lists.append(row)
    except FileNotFoundError:
        raise FileExistsError(f"File not found: {filename}")
    except PermissionError:
        raise PermissionError(f"Permission denied reading file: {filename}")
    except Exception as e:
        raise e

    lists = tuple(zip(*lists))
    return list(lists[0]), list(lists[1])

def main():
    parser = argparse.ArgumentParser(prog='01', description='Determine distance between lists')
    parser.add_argument("input_filename")
    args = parser.parse_args()

    l1, l2 = read_input(args.input_filename)
    l1.sort()
    l2.sort()
    print("Part 1")
    tot_dist = sum([abs(i1-i2) for i1, i2 in zip(l1, l2)])
    print(f"Total distance: {tot_dist}")

    print("Part 2")
    rightCounter = Counter(l2)
    similarity = sum([leftItem*rightCounter[leftItem] for leftItem in l1 if leftItem in rightCounter])
    print(f"Total similarity: {similarity}")

if __name__ == "__main__":
    main()