#!/usr/bin/env python3
import argparse
from typing import Tuple, List
from pathlib import Path
from collections import Counter

def read_input(filename: str | Path) -> List[List[int]]:
    reports: List[List[int]] = []
    try:
        with open(filename, 'r') as file:
            for line in file:
                row = [int(item) for item in line.split()]
                reports.append(row)
    except FileNotFoundError:
        raise FileExistsError(f"File not found: {filename}")
    except PermissionError:
        raise PermissionError(f"Permission denied reading file: {filename}")
    except Exception as e:
        raise e

    return reports

def running_diff(report: List[int]) -> List[int]:
    return [j-i for i,j in zip(report, report[1:])]

def safe_report_noexclusions(report: List[int]) -> bool:
    diffs = running_diff(report)
    if not(all([diff < 0 for diff in diffs]) or all([diff > 0 for diff in diffs])):
        return False

    absdiffs = [abs(diff) for diff in diffs]
    if min(absdiffs) < 1 or max(absdiffs) > 3:
        return False

    return True

def safe_report_exclusions(report: List[int], nExclusions: int) -> bool:
    excluded: int = 0
    index: int = 0
    lastIdx: int = 0

    if safe_report_noexclusions(report):
        return True

    if nExclusions == 0:
        return False

    positive, negative = True, True
    # positive
    for i, (a, b) in enumerate(zip(report, report[1:])):
       delta = b-a
       if (delta < 1 or delta >3):
           positive = safe_report_exclusions(report[:i] + report[i+1:], nExclusions-1) or safe_report_exclusions(report[:i+1] + report[i+2:], nExclusions-1)
       
    for i, (a, b) in enumerate(zip(report, report[1:])):
       delta = a-b
       if (delta < 1 or delta >3):
           negative = safe_report_exclusions(report[:i] + report[i+1:], nExclusions-1) or safe_report_exclusions(report[:i+1] + report[i+2:], nExclusions-1)
       
    return positive or negative        
           

def main():
    parser = argparse.ArgumentParser(prog='02', description='Count safe reports')
    parser.add_argument("input_filename")
    args = parser.parse_args()

    reports = read_input(args.input_filename)
    print("Part 1")
    nSafeReports = sum([safe_report_noexclusions(report) for report in reports])
    print(f"Safe Reports: {nSafeReports}")

    print("Part 2")
    nSafeReports = sum([safe_report_exclusions(report, 1) for report in reports])
    print(f"Safe Reports with Dampener: {nSafeReports}")

if __name__ == "__main__":
    main()