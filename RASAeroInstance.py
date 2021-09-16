import keyboard
import time

from pywinauto.application import Application
from enum import Enum

class RocketSection(Enum):
    BodyTube = 0
    Booster = 1

class RASAeroInstance:
    def __init__(self):
        self.app = None
        self.mainWindow = None

    def start(self):
        self.app = Application(backend="uia").start("C:\Program Files (x86)\RASAero II\RASAero II.exe")
        self.mainWindow = self.app.RASAero

    def loadRocket(self, path):
        # Open File menu
        self.mainWindow.Menu.File.click_input()
        # Scroll to and select Open menu option
        keyboard.send("down")
        keyboard.send("down")
        keyboard.send("enter")
        # Enter path and open file
        keyboard.write(path)
        keyboard.send("enter")

    def loadEngine(self, path):
        # Open File menu
        self.mainWindow.Menu.File.click_input()
        # Scroll to and select Open menu option
        keyboard.send("down")
        keyboard.send("down")
        keyboard.send("down")
        keyboard.send("down")
        keyboard.send("down")
        keyboard.send("enter")
        # Enter path and open file
        keyboard.write(path)
        keyboard.send("enter")

    def setFinParameters(self, rocketSection, rootChord, span, tipChord, sweepDistance, finThickness):
        tubeWindow = self.__getTubeWindow(rocketSection)
        tubeWindow.type_keys("{ENTER}")
        clearField = "{BACKSPACE 3}{RIGHT 2}{DELETE 3}{LEFT}"
        # Change fields
        tubeWindow.FinsDialog.type_keys("{TAB 3}" + clearField + str(rootChord))
        tubeWindow.FinsDialog.type_keys("{TAB 2}" + clearField + str(finThickness))
        tubeWindow.FinsDialog.type_keys("{TAB}" + clearField + str(sweepDistance))
        tubeWindow.FinsDialog.type_keys("{TAB}" + clearField + str(tipChord))
        tubeWindow.FinsDialog.type_keys("{TAB}" + clearField + str(span))
        # Save find parameters and close dialogs
        tubeWindow.FinsDialog.OK.click_input()
        tubeWindow.Save.click_input()

    def __getTubeWindow(self, rocketSection):
        window = None

        if (rocketSection == RocketSection.BodyTube):
            self.mainWindow.ListBox1.ListItem4.click_input(double=True)
            window = self.mainWindow.child_window(title="Body Tube", top_level_only=False)
        elif (rocketSection == RocketSection.Booster):
            self.mainWindow.ListBox1.ListItem5.click_input(double=True)
            window = self.mainWindow.child_window(title="Booster", top_level_only=False)

        return window

    def setIgnitionDelayAndExportFlightSimData(self, filePath, ignitionDelay):
        # Set ignition delay
        self.mainWindow.ToolStrip1.Button8.click_input(double=True)
        self.mainWindow.child_window(title="Motor(s) Loaded Row 0", top_level_only=False).click_input(double=True)
        self.mainWindow.Flight.FlightDataEntry.type_keys("{TAB 6}{BACKSPACE 2}" + str(ignitionDelay))
        self.mainWindow.Flight.FlightDataEntry.Save.click_input()
        # Export CSV
        self.mainWindow.child_window(title="ViewData Row 0", top_level_only=False).click_input()
        keyboard.send("alt+f")
        keyboard.send("enter")
        keyboard.send("enter")
        keyboard.send("tab")
        keyboard.send("enter")
        keyboard.write(filePath)
        keyboard.send("enter")
        keyboard.send("left")
        keyboard.send("enter")
        keyboard.send("alt+f4")
        # Return to main window
        keyboard.send("alt+f4")
        keyboard.send("enter")
