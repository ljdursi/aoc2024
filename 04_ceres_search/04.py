#!/usr/bin/env python3
import argparse
from typing import Dict, List, Tuple
from pathlib import Path

class Board:
    def __init__(self, lines: List[str]):
        self.lookup : Dict[Tuple[int, int], str] = {}
        self._nrows = 0
        self._ncols = 0
        for i, line in enumerate(lines):
            self._nrows += 1
            self._ncols = max(self._ncols, len(line))
            for j, c in enumerate(line):
                self.lookup[(i,j)] = c
            
    def nrows(self) -> int:
        return self._nrows

    def ncols(self) -> int:
        return self._ncols

    def __getitem__(self, idx: Tuple[int, int]) -> str:
        if idx in self.lookup:
            return self.lookup[idx]
        else:
            return ""

    def find_word_at(self, word: str, at: Tuple[int, int], indir=None) -> int:
        if at[0] < 0 or at[1] < 0:
            return 0
        
        if at[0] >= self.nrows():
            return 0
        
        if at[1] >= self.ncols():
            return 0

        if len(word) == 0:
            return 1

        if self[at] != word[0]:
            return 0

        if len(word) == 1:
            return 1

        count = 0
        for dir in [(0,1), (1,1), (1,0), (1,-1), (0, -1), (-1, -1), (-1, 0), (-1, 1)]:
            if not indir or dir == indir:
                count += self.find_word_at(word[1:], (at[0] + dir[0], at[1] + dir[1]), dir )

        return count


def read_input(filename: str | Path) -> Dict[Tuple[int,int], str]:
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

    return Board(lines)


def main():
    parser = argparse.ArgumentParser(prog='04', description='Word search, kind of')
    parser.add_argument("input_filename")
    args = parser.parse_args()

    board = read_input(args.input_filename)

    print("Part 1")
    count = 0
    for i in range(board.nrows()):
        for j in range(board.ncols()):
            if board[(i,j)] == 'X':
                count += board.find_word_at("XMAS", (i,j))

    print(f"Number oF XMASes found: {count}")

    print("Part 2")
    count = 0
    for i in range(board.nrows()):
        for j in range(board.ncols()):
            if board[(i,j)] == 'A':
                left = board.find_word_at("MAS", (i-1, j-1), (1, 1)) \
                       + board.find_word_at("SAM", (i-1, j-1), (1,1))

                right = board.find_word_at("MAS", (i-1, j+1), (1, -1)) \
                       + board.find_word_at("SAM", (i-1, j+1), (1, -1))

                if left and right:
                    count += 1

    print(f"Number oF X-MASes found: {count}")

if __name__ == "__main__":
    main()