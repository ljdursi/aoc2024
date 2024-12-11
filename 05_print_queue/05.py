#!/usr/bin/env python3
import argparse
from typing import Dict, List, Set, Tuple
from pathlib import Path
from collections import defaultdict
import re

def read_input(filename: str | Path) -> Tuple[Dict[int, int], List[List[int]]]:
    lines = []
    try:
        with open(filename, 'r') as file:
            for line in file:
                lines.append(line)
            
    except FileNotFoundError:
        raise FileExistsError(f"File not found: {filename}")
    except PermissionError:
        raise PermissionError(f"Permission denied reading file: {filename}")
    except Exception as e:
        raise e

    constraints: Dict[int, Set[int]] = defaultdict(set)
    layouts : List[List[int]] = []

    constraint_re = re.compile(r"(\d+)\|(\d+)")
    in_constraints = True
    for line in lines:
        if in_constraints:
            match = constraint_re.match(line)
            if not match:
                in_constraints = False
                continue
            else: 

                constraints[int(match[1])].add(int(match[2]))
        else:
            layouts.append([int(i) for i in line.split(',')])
    
    return constraints, layouts

def valid_layout(layout: List[int], constraints: Dict[int, Set[int]]) -> bool:
    previous = set()
    for i, item in enumerate(layout):
        after = constraints[item]
        if after.intersection(previous):
            return False
        previous.add(item)

    return True

def insertion_sort(layout: List[int], constraints: Dict[int, Set[int]]):
    n = len(layout)
    if n <= 1:
        return  

    def less_than(a, b):
        if b in constraints[a]:
            return True
        return False
 
    for i in range(1, n):
        key = layout[i]
        j = i-1
        while j >= 0 and less_than(key, layout[j]):
            layout[j+1] = layout[j]
            j -= 1
        layout[j+1] = key


def main():
    parser = argparse.ArgumentParser(prog='01', description='Determine distance between lists')
    parser.add_argument("input_filename")
    args = parser.parse_args()

    constraints, layouts = read_input(args.input_filename)

    print("Part 1")
    middle_sum = 0
    for layout in layouts:
        if valid_layout(layout, constraints):
            n = len(layout)
            middle_sum += layout[n//2]
    print(f"Sum of middles of valid layouts: {middle_sum}")

    print("Part 2")
    middle_sum = 0
    for layout in layouts:
        if valid_layout(layout, constraints):
            continue
        insertion_sort(layout, constraints)
        n = len(layout)
        middle_sum += layout[n//2]

    print(f"Sum of middles of fixed layouts: {middle_sum}")

if __name__ == "__main__":
    main()