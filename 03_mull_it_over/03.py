#!/usr/bin/env python3
import argparse
import re
from typing import Tuple, List
from pathlib import Path
from collections import Counter

def read_input(filename: str | Path) -> List[str]:
    result = []
    try:
        with open(filename, 'r') as file:
            for line in file:
                result.append(line)
    except FileNotFoundError:
        raise FileExistsError(f"File not found: {filename}")
    except PermissionError:
        raise PermissionError(f"Permission denied reading file: {filename}")
    except Exception as e:
        raise e

    return result

class Operation:
    rexec = r""
    pass

class Conditional(Operation):
    regex = r"do\(\)|don't\(\)"

    def __init__(self, input: str):
        self.input = input
        self.enable = True
        if input == "don't()":
            self.enable = False

    def result(self) -> int:
        return self.enable

    def __repr__(self) -> str:
        return "do()" if self.enable else "don't()"


class Multiplication(Operation):
    regex = r"mul\(\d+,\d+\)" 
    groups_pattern = re.compile(r"mul\((\d+),(\d+)\)")

    def __init__(self, input: str):
        items = Multiplication.groups_pattern.match(input)
        self.multiplicands = [int(items[1]), int(items[2])]

    def result(self) -> int:
        return self.multiplicands[0]*self.multiplicands[1]

    def __repr__(self) -> str:
        return f"mul({self.multiplicands[0]},{self.multiplicands[1]})"


def extract_muls(line: str) -> List[Multiplication]:
    pattern = re.compile(Multiplication.regex)
    return [Multiplication(item) for item in pattern.findall(line)]


class Computer:
    regex = Multiplication.regex + "|" + Conditional.regex
    condpattern = re.compile(Conditional.regex)
    multpattern = re.compile(Multiplication.regex)

    def operand(item: str) -> Operation:
        if Computer.condpattern.match(item):
            return Conditional(item)
        else:
            return Multiplication(item)

    def __init__(self, input: str):
        pattern = re.compile(Computer.regex)
        self.operations = [Computer.operand(item) for item in pattern.findall(input)]

    def __repr__(self) -> str:
        return " ".join(item.__repr__() for item in self.operations)

    def result(self) -> int:
        enabled = True
        total = 0
        for item in self.operations:
            result = item.result()
            if type(result) == bool:
                enabled = result
            elif type(result) == int:
                if enabled:
                    total += result
        return total


def main():
    parser = argparse.ArgumentParser(prog='01', description='Determine distance between lists')
    parser.add_argument("input_filename")
    args = parser.parse_args()

    lines = read_input(args.input_filename)
    mults = []
    print("Part 1")
    for line in lines:
        mults = mults + extract_muls(line)
    mults_sum = sum([m.result() for m in mults])
    print(f"Sum of multiplies: {mults_sum}")

    print("Part 2")
    line = " ".join(lines)
    compute = Computer(line)
    print(f"Sum of enabled multiplies: {compute.result()}")




if __name__ == "__main__":
    main()