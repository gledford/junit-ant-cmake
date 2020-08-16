# junit-ant-cmake
Integration of JUnit tests using Ant in a CMake build system.

For a project that has mixed C++ and Java source code, having a singular build generation tool and test runner is helpful.
This demo project shows how to use Apache Ant for the JUnit tests and integrated the Ant scripts with CMake so developers
can run CTest to execute their tests.

Additional Python modules are needed to get the output from the JUnit reports given that CTest sees the single build.xml file
as a single test. Collecting the unit test counts is done through scanning for the JUnit generated XML files.
