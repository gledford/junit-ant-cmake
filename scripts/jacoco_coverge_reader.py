#!/usr/local/bin/python3

"""
This file merges all of the Jacoco Java Coverage reports
"""

import os
import csv
import argparse
import sys


parser = argparse.ArgumentParser(
    description='Recursively scans for Jacoco report files to create a roll-up')
parser.add_argument(
    '-dir', help='Directory to start searching from', required=True)
args = parser.parse_args()

if not os.path.isdir(args.dir):
    print("ERROR: The input directory does not exist!")
    sys.exit(1)

COVERAGE_FILE_NAME = 'coverage.csv'
coverage_file_list = []

for root, dirs, files in os.walk(os.path.join(args.dir, '../')):
    if COVERAGE_FILE_NAME in files:
        coverage_file_list.append(os.path.join(root, COVERAGE_FILE_NAME))

if not coverage_file_list:
    print("ERROR: No coverage.csv files found!")
    sys.exit(1)

CSV_HEADER = 'GROUP,PACKAGE,CLASS,INSTRUCTION_MISSED,INSTRUCTION_COVERED,BRANCH_MISSED'\
             ',BRANCH_COVERED,LINE_MISSED,LINE_COVERED,COMPLEXITY_MISSED,COMPLEXITY_COVERED'\
             ',METHOD_MISSED,METHOD_COVERED'

totals_dict = {}

attrs = CSV_HEADER.split(',')
for attr in attrs:
    if 'MISSED' in attr or 'COVERED' in attr:
        totals_dict[attr] = "0"
    else:
        totals_dict[attr] = ""

CSV_MERGED = open(os.path.join(args.dir, 'JUnitCoverageReport.csv'), 'w')
CSV_MERGED.write(CSV_HEADER)
CSV_MERGED.write('\n')

for file in coverage_file_list:
    csv_in = open(file)
    for line in csv_in:
        if line.startswith(CSV_HEADER):
            continue
        CSV_MERGED.write(line)
    csv_in.close()

CSV_MERGED.close()

with open(os.path.join(args.dir, 'JUnitCoverageReport.csv')) as csv_file:
    reader = csv.DictReader(csv_file)
    for row in reader:
        for attr in attrs:
            if 'MISSED' in attr or 'COVERED' in attr:
                totals_dict[attr] = str(int(totals_dict[attr]) + int(row[attr]))

with open(os.path.join(args.dir, 'JUnitCoverageReport.csv'), 'a') as csv_file:
    FIRST = True
    for data in totals_dict.values():
        if FIRST:
            csv_file.write('Totals')
            FIRST = False
        else:
            csv_file.write(',' + data)
    csv_file.write('\n')

print("\nJUnit Code Coverage Report: " + os.path.join(os.path.abspath(args.dir), 'JUnitCoverageReport.csv'))
print("******JUnit Code Coverage Metrics******")

try:
    total_lines = int(totals_dict['LINE_COVERED']) + int(totals_dict['LINE_MISSED'])
    line_coverage = (int(totals_dict['LINE_COVERED']) / int(total_lines)) * 100
except ZeroDivisionError:
    line_coverage = 0
print("1. Line Coverage:\t\t%0.2f" % line_coverage + "%")

try:
    total_branch = int(totals_dict['BRANCH_COVERED']) + int(totals_dict['BRANCH_MISSED'])
    branch_coverage = (int(totals_dict['BRANCH_COVERED']) / int(total_branch)) * 100
except ZeroDivisionError:
    branch_coverage = 100
print("2. Branch Coverage:\t\t%0.2f" % branch_coverage + "%")

try:
    total_instruction = int(totals_dict['INSTRUCTION_COVERED']) + int(totals_dict['INSTRUCTION_MISSED'])
    instruction_coverage = (int(totals_dict['INSTRUCTION_COVERED']) / int(total_instruction)) * 100
except ZeroDivisionError:
    instruction_coverage = 0
print("3. Instruction Coverage:\t%0.2f" % instruction_coverage + "%")

try:
    total_method = int(totals_dict['METHOD_COVERED']) + int(totals_dict['METHOD_MISSED'])
    method_coverage = (int(totals_dict['METHOD_COVERED']) / int(total_method)) * 100
except ZeroDivisionError:
    method_coverage = 0
print("4. Method Coverage:\t\t%0.2f" % method_coverage + "%")
print("******JUnit Code Coverage Metrics******\n")
