# AutoRASAero
## Setup
1. Download and install [RASAero](http://www.rasaero.com/dl_software_ii.htm).
2. Download and install [Python](https://www.python.org/downloads/). When installing be sure to check the box to "Add Python to PATH".
3. Import necessary packages by running the following commands in a terminal  
    a. Run `pip install pywinauto`. [Pywinauto](https://pypi.org/project/pywinauto/) is a package to help control RASAero.  
    b. Run `pip install keyboard`. [Keyboard](https://pypi.org/project/keyboard/) is a package that controls the keyboard and is also used to help control RASAero.  
4. Clone this repository
5. (Optional) Read/Run the example to become familiar with the code

## CD Neural Network Training
1. Complete the setup instructions above
2. Open CDTester.py
3. Edit the `STARTING_ROW` and `ENDING_ROW` variables for the rows you want to run through the CD calculator
4. Run CDTester.py
5. Copy values from  `NN Training/Output.csv` into the `NN Training\Mach Input D2 Hypercube 12000.jmp.xlsx` spreadsheet

