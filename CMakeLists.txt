cmake_minimum_required (VERSION 3.10)

#find_package(Java REQUIRED)
#include(UseJava)

enable_testing()

project (TestJUnit NONE)

#Runs all of the unit tests within the build.xml file but CTest recognizes
#the results as a single test suite known as TestJUnit	
add_test(
	NAME 
		TestJUnit 
	COMMAND 
		/usr/local/bin/ant -f ../build.xml)
		
#This gathers all of the XML files and merges into a single roll-up report
#Might be a good idea for the Test SMEs when gathering the entire repo metrics
add_custom_target(collect-junit-results
	COMMAND
		/Users/gledford/git/JUnitReportCollector/junit_report_collector.py -dir ../
	VERBATIM
)