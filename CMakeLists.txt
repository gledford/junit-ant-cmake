cmake_minimum_required (VERSION 3.10)

project (TestJUnit NONE)

#Runs all of the unit tests within the build.xml file but CTest recognizes
#the results as a single test suite known as TestJUnit	
add_test(
	NAME 
		TestJUnit 
	COMMAND 
		/usr/local/bin/ant -f ${CMAKE_CURRENT_SOURCE_DIR}/build.xml)