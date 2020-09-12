#!/usr/local/bin/python3

"""
This file contains the class used to collect the JUnit reports
and merge them together.
"""

import fnmatch
import os
import argparse
import sys


# pylint: disable=too-few-public-methods
class JUnitReportCollector:
    """
    This class scans for JUnit-generated XML files and merges them together
    to create a roll-up of the pass/fail tests. This class also prints the number
    of passing and failing tests along with the name of the failing tests
    """

    def __init__(self):
        self.report_files = []
        self.output_report_name = 'TEST-AllJUnitTests.xml'
        self.passing_tests = []
        self.failing_tests = []
        self.root_path = ''

    def collect(self, root_path: str) -> None:
        """
        Finds the JUnit report XML files
        """
        if os.path.isdir(root_path):
            self.root_path = root_path
            for root, _, file_names in os.walk(root_path):
                for filename in fnmatch.filter(file_names, 'TEST-*.xml'):
                    if filename != self.output_report_name:
                        self.report_files.append(os.path.join(root, filename))
            if self.report_files:
                self.__create_rollup__()
                self.__print_summary__()
            else:
                print('ERROR: Unable to find any files matching ' \
                      'TEST-*.xml to create the JUnit report')
                sys.exit(1)
        else:
            print('ERROR: The provided directory does not exist %s' % root_path)
            sys.exit(1)

    def __create_rollup__(self) -> None:
        if os.path.isdir(self.root_path):
            new_report = open(os.path.join(
                self.root_path, self.output_report_name), 'w')
            new_report.write('<?xml version="1.0" encoding="UTF-8" ?>\n')
            new_report.write('<testsuites>\n')

            self.__extract_report_data__(new_report)

            new_report.write('</testsuites>\n')
            new_report.close()

    def __extract_report_data__(self, new_report) -> None:
        for report in self.report_files:
            with open(report) as current_report:
                is_first = True
                lines = current_report.read().splitlines()
                for i in range(0, len(lines)):
                    if not is_first:
                        new_report.write(lines[i])
                        if '<testcase classname=' in lines[i]:
                            test_suite = lines[i].split(' ')[3].strip(
                                'classname=').strip("\"")
                            test_case = lines[i].split(
                                ' ')[4].strip('name=').strip("\"")
                            if i < len(lines):
                                if '<failure' in lines[i + 1]:
                                    self.failing_tests.append(
                                        test_suite + ':' + test_case)
                                else:
                                    self.passing_tests.append(
                                        test_suite + ':' + test_case)
                    else:
                        is_first = False

    def __print_summary__(self) -> None:
        if self.failing_tests:
            print('\nFailures:')
            count = 1
            for failing_test in self.failing_tests:
                print(str(count) + '. ' + failing_test)
        print("******JUnit Test Metrics******")
        print('Passing Tests... %s' % str(len(self.passing_tests)))
        print('Failing Tests... %s' % str(len(self.failing_tests)))
        print("******JUnit Test Metrics******\n")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Recursively scans for JUnit report files to create a roll-up')
    parser.add_argument(
        '-dir', help='Directory to start searching from', required=True)
    args = parser.parse_args()

    report_collector = JUnitReportCollector()
    report_collector.collect(args.dir)
