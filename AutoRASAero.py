import RASAeroInstance
import keyboard
import pathlib
import sys
import time

CDX1_FILE = r"C:\Users\jaden\Documents\Github\AutoRASAero\MBS_43.CDX1"
ENG_FILE = r"C:\Users\jaden\Documents\GitHub\AutoRASAero\TCIMC3_(9899.7771)_5_5_2.329_11.0789_2.eng"

# 0 seconds
RASAero = RASAeroInstance.RASAeroInstance()
RASAero.start()
RASAero.loadRocket(CDX1_FILE)
RASAero.loadEngine(ENG_FILE)
"""csv = str(pathlib.Path.cwd())  + "\\fin.csv"
RASAero.exportFlightSimData(csv, 6)"""
sys.exit()
# 12.5 seconds
#RASAero.setFinParameters(RASAeroInstance.RocketSection.BodyTube, 16, 7, 4, 10, 0.4)
# 32.5 seconds tabbed
#RASAero.setFinParameters(RASAeroInstance.RocketSection.Booster, 16, 7, 4, 10, 0.4)

#RASAero.mainWindow.Flight.DataGridView
#print_control_identifiers()
"""
Open and set ignition delay in dialog
RASAero.mainWindow.ToolStrip1.Button8.click_input(double=True)
RASAero.mainWindow.child_window(title="Motor(s) Loaded Row 0", top_level_only=False).click_input(double=True)
RASAero.mainWindow.Flight.FlightDataEntry.type_keys("{TAB 6}{BACKSPACE 2}" + str(6))
RASAero.mainWindow.Flight.FlightDataEntry.Save.click_input()
"""
RASAero.mainWindow.child_window(title="ViewData Row 0", top_level_only=False).click_input()
#time.sleep(5)
keyboard.send("alt+f")
keyboard.send("enter")
keyboard.send("enter")
keyboard.send("tab")
keyboard.send("enter")

keyboard.write(csv)
keyboard.send("enter")
keyboard.send("alt+f4")
"""
w = RASAero.app.top_window()
print(w.GetProperties())
w.type_keys("%F")"""
#RASAero.mainWindow.Flight.Flight.Menu.File.click_input()
#RASAero.mainWindow.Flight.Flight.type_keys("{RIGHT 2}{ENTER}")
