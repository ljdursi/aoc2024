#!/usr/bin/env python3
import argparse
from typing import Set, Dict, List, Tuple, Optional
from pathlib import Path

class Board:
    up : Tuple[int, int] = (-1, 0)
    right : Tuple[int, int] = (0, 1)
    down : Tuple[int, int] = (1, 0)
    left : Tuple[int, int] = (0, -1)
    
    right_turn: Dict[Tuple[int, int], Tuple[int, int]] = {
        up: right, 
        right: down,
        down: left,
        left: up
    }

    orientation : Dict[str, Tuple[int, int]] = {'^': up, '>': right, 'v': down, '<': left}

    def __init__(self, lines: List[str]):
        self.obstacles : Set[Tuple[int, int]] = set()
        self.guard : Tuple[int, int] = (-1, -1)
        self.guard_orientation : Tuple[int, int] = (0, -1)

        self._nrows = len(lines)
        self._ncols = len(lines[0])-1
        for i, line in enumerate(lines):
            for j, c in enumerate(line):
                if c == '.':
                    continue
                if c == '#':
                    self.obstacles.add((i,j))
                    continue
                if c in Board.orientation.keys():
                    self.guard = (i, j)
                    self.guard_orientation = Board.orientation[c]

    def nrows(self) -> int:
        return self._nrows

    def ncols(self) -> int:
        return self._ncols

    def guard_pos(self) -> Tuple[int, int]:
        return self.guard

    def on_board(self, pos: Tuple[int, int]) -> bool:
        i, j = pos

        if i < 0 or i >= self._nrows:
            return False
        if j < 0 or j >= self._ncols:
            return False

        return True

    def guard_step(self) -> Optional[Tuple[int, int]]:
        newpos = self.guard[0] + self.guard_orientation[0], self.guard[1] + self.guard_orientation[1]
        if not newpos in self.obstacles:
            if not self.on_board(newpos):
                return None
            self.guard = newpos
        else:
            self.guard_orientation = Board.right_turn[self.guard_orientation]
        
        return self.guard

    def as_grid(self) -> List[List[str]]:
        cells = []
        for row in range(self._nrows):
            line = ['.'] * self._ncols
            for col in range(self._ncols):
                if (row, col) in self.obstacles:
                    line[col] = '#'
                if self.guard == (row, col):
                    for k, v in Board.orientation.items():
                        if v == self.guard_orientation:
                            line[col] = k
            cells.append(line)
        return cells
        
    def __repr__(self) -> str:
        cells = self.as_grid() 
        lines = ["".join(row) for row in cells]
        return "\n".join(lines)


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
    parser = argparse.ArgumentParser(prog='06', description='Guard tracking')
    parser.add_argument("input_filename")
    args = parser.parse_args()

    board = read_input(args.input_filename)

    print("Part 1")
    guard_posns = set([board.guard_pos()])
    while 1:
        new_posn = board.guard_step()
        if not new_posn:
            break
        guard_posns.add(new_posn)
    print(len(guard_posns))


if __name__ == "__main__":
    main()