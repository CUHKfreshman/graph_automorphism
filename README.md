# graph_automorphism
Before running, cd to DviCL, comment stat(), i.e., "//stat();" in main function of bliss.cc (line 1396), then cmd "make".
"chmod -R 777 ." to enable permissions.
Run python3 app.py to access the Dash application.
Note: Not compatible with Windows.

# LEDA
To install LEDA on Linux using the command line, you can follow these steps:

Open a terminal window on your Linux machine.

Install the required dependencies for LEDA using the following command:

csharp
Copy code
sudo apt-get install libx11-dev libxt-dev
This will install the X Window System development libraries, which are needed for LEDA's graphical tools.

Download the LEDA archive to a directory on your computer using the following command:

javascript
Copy code
wget https://www.algorithmic-solutions.com/leda-download/leda-6.4-free-linux.tar.gz
Extract the LEDA archive using the following command:

c
Copy code
tar -zxvf leda-6.4-free-linux.tar.gz
Set the environment variable LEDA to the path of the LEDA directory using the following command:

javascript
Copy code
export LEDA=/path/to/leda-6.4-free-linux
Replace /path/to/leda-6.4-free-linux with the actual path to your LEDA directory.

Add the LEDA library to your C++ project's include and library search paths by adding the following flags to your compiler command:

bash
Copy code
-I${LEDA}/incl -L${LEDA}/lib -lL -lX11
The -I flag adds the LEDA include directory to the search path, the -L flag adds the LEDA library directory to the search path, and the -l flags link against the LEDA library and its dependencies.

Include the necessary LEDA headers in your C++ source files by adding the appropriate #include statements. For example, to use the LEDA graph data structure, you should include the LEDA/graph/graph.h header.

Build and link your C++ program as you normally would. Be sure to include the LEDA library and its dependencies in the linker inputs.

Following these steps should allow you to install LEDA on Linux using the command line and use it in your C++ projects. Note that the specific steps and commands may vary depending on your development environment and operating system.