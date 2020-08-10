cmake_minimum_required (VERSION 3.10)

#find_package(Java REQUIRED)
#include(UseJava)

enable_testing()

project (TestJUnit NONE)

add_test(
	NAME 
		ControllerTest 
	COMMAND 
		/usr/local/bin/ant -f ../build.xml ControllerTest)
		
add_test(
	NAME 
		HelloWorldTest 
	COMMAND 
		/usr/local/bin/ant -f ../build.xml HelloWorldTest)
		
add_custom_target(App_TestCoverage
	COMMAND
		ctest -VV; echo 'Run jacoco')