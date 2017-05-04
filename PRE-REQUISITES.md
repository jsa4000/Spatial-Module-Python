======================
Python Installation
======================

> Recommendation is to installing Python using the executable Sutep since privileges are not mandatory for the installation.
> Also you could install additional packages such as Anaconda or WinPython. These two suites will install all common dependences and libraries needed.

In order to install Python without using the Setup installer.

1. Download the binaries by using your current Platform of choice (e.j. Windows x64)

https://www.python.org/downloads/

Extract all the content into a folder and open a Prompt or a Bash shell to start typing commands.
	This path will be %PYTHON_PATH%
	
2. Install the Necessary packages and Tools.

2.1 Download `get-pip.py` from https://bootstrap.pypa.io/get-pip.py and type the following command.

	python get-pip.py

This will install all the basics tools ans scripts to use in python.	
	
>https://pip.pypa.io/en/stable/installing/#do-i-need-to-install-pip
 
3. Set current global variables in the OS to add the Paths
 
In windows type the following command
 
	rundll32 sysdm.cpl,EditEnvironmentVariables
	
Add the following commands to the environment paths

	%PYTHON_PATH%\
	%PYTHON_PATH%\Lib
	%PYTHON_PATH%\Scripts

4. Install Packages and create virtual environments

4.1 Create a virtual environment

To create a virtual environment you could use 'venv' or 'virtualenv' methods.
If you don't have those modules you can type, to install them.
	pip install virtualenv
	virtualenv --version

> Also if you use conda you could also create your own conda environments.
	conda create -n yourenvname python=x.x anaconda
	activate yourenvname
	
- Create a new folder with all the environment to create
	
	%PYTHON_PATH%> md envs
	cd envs

- Create the new environment

By using 'virtualenv';
	%PYTHON_PATH%\envs>virtualenv my_env

By using 'venv' you can type the following command	
	ej. python -m venv ".\envs\myenv"

- Activate the environment

Navigate inside the \Script folder of the new virtual environment you've created and use activate.

	.\envs\myenv\scripts\activate.bat
	
Now you are inside a new environment  Where you can install every you want inside this virtual environment

	(myenv) C:\javier\>

> Also If you want to start a Visual IDE from this particular environment you just have to open the tool from this point.ç
	(myenv) C:\javier\> Code.exe
		

4.2 Install additional packages	
	
Following are some of the basics packages and modules to install. Basically you will need to install firsto all the modules dependences.	
	
	pip install --user numpy scipy matplotlib ipython jupyter pandas sympy nose	
		
> Sometimes using --used doesn't worl with virtual environments

Some packages requires some requisites to be installed completely. First you will need to download and install 'wheels' packages depending on your Platform and OS.

	pip install SomePackage-1.0-py2.py3-none-any.whl

or

	# numpy-1.9.3+mkl for Python 3.5 on Win AMD64
	pip3.5 install http://www.lfd.uci.edu/~gohlke/pythonlibs/xmshzit7/numpy-1.9.3+mkl-cp35-none-win_amd64.whl

See following URLs, to see the current version for Numpy and scipy wheels:
	http://www.lfd.uci.edu/~gohlke/pythonlibs/#numpy 
	http://www.lfd.uci.edu/~gohlke/pythonlibs/#scipy

Finally, once you have updated and installed correctly all the packages and dependences then you can install other libraries:

	pip install -U scikit-learn
	pip install --upgrade tensorflow
	pip install pylint

> numpy+mkl is important since it used BLAS or LAPACK libraries that enables multi-threading.
   mkl is the accronym for Intel® Math Kernel Library (Intel® MKL) 

















