import keyboard
import time

from pywinauto.application import Application
from enum import Enum

class RocketSection(Enum):
    Sustainer = 0
    Booster = 1
    NoseCone = 2

class RASAeroInstance:
    def __init__(self):
        self.app = None
        self.mainWindow = None
        self.clearField = ["backspace", "backspace", "backspace", "right", "right", "delete", "delete", "delete", "left"]

    def start(self):
        """
        Open an instance of RASAero
        
            Parameters:
                
            Returns:
        """
        self.app = Application(backend="uia").start("C:\Program Files (x86)\RASAero II\RASAero II.exe")
        self.mainWindow = self.app.RASAero

    def close(self):
        """
        Close an instance of RASAero previously opened in the start() function
        
            Parameters:
                
            Returns:
        """
        keyboard.send("alt+f4")
        keyboard.send("right")
        keyboard.send("enter")
        self.app = None
        self.mainWindow = None

    def loadRocket(self, path):
        """
        Open the specified rocket file in RASAero
        
            Parameters:
                path (string): path to the rocket file
                
            Returns:
        """
        # Open File menu
        self.mainWindow.Menu.File.click_input()
        # Scroll to and select Open menu option
        self.__repeatKeyboardInput("down", 2)
        keyboard.send("enter")
        # Enter path and open file
        keyboard.write(path)
        keyboard.send("enter")

    def loadEngine(self, path):
        """
        Open the specified engine file in RASAero
        
            Parameters:
                path (string): path to the engine file
                
            Returns:
        """
        # Open File menu
        self.mainWindow.Menu.File.click_input()
        # Scroll to and select Open menu option
        self.__repeatKeyboardInput("down", 5)
        keyboard.send("enter")
        # Enter path and open file
        keyboard.write(path)
        keyboard.send("enter")

    def setFinParameters(self, rocketSection, rootChord, span, tipChord, sweepDistance):
        """
        Set the root chord, span, tip chord, and sweep distance of the specified rocket section
        
            Parameters:
                rocketSection (RocketSection): the rocket section attatched to the fins
                rootChord (float): the root chord of the fin
                span (float): the span of the fin
                tipChord (float): the tip chord of the fin
                sweepDistance (float): the sweep distance of the fin
                
            Returns:
        """
        tubeWindow = self.__getTubeWindow(rocketSection)
        keyboard.send("enter")
        clearField = ["backspace", "backspace", "backspace", "right", "right", "delete", "delete", "delete", "left"]
        # Change root chord
        self.__repeatKeyboardInput("tab", 3)
        self.__inputKeyboardSequence(clearField)
        keyboard.write(str(rootChord))
        # Change sweep distance
        self.__repeatKeyboardInput("tab", 3)
        self.__inputKeyboardSequence(clearField)
        keyboard.write(str(sweepDistance))
        # Change tip chord
        keyboard.send("tab")
        self.__inputKeyboardSequence(clearField)
        keyboard.write(str(tipChord))
        # Change span
        keyboard.send("tab")
        self.__inputKeyboardSequence(clearField)
        keyboard.write(str(span))
        # Save fin parameters and close dialogs
        self.__repeatKeyboardInput("shift+tab", 8)
        keyboard.send("enter")
        if rocketSection == RocketSection.Sustainer:
            self.__repeatKeyboardInput("tab", 4)
        else:
            self.__repeatKeyboardInput("tab", 2)
        keyboard.send("enter")

    def setBodyDiameter(self, diameter):
        self.__getTubeWindow(RocketSection.NoseCone)
        self.__repeatKeyboardInput("tab", 2)
        self.__inputKeyboardSequence(self.clearField)
        keyboard.write(str(diameter))
        keyboard.send("shift+tab")
        keyboard.send("enter")

    def setTubeParameters(self, rocketSection, rootChord, span, tipChord, sweepDistance, tubeLength):
        """
        
        """
        tubeWindow = self.__getTubeWindow(rocketSection)
        keyboard.send("enter")
        
        # Change root chord
        self.__repeatKeyboardInput("tab", 3)
        self.__inputKeyboardSequence(self.clearField)
        keyboard.write(str(rootChord))
        # Change fin distance from base
        keyboard.send("tab")
        self.__inputKeyboardSequence(self.clearField)
        keyboard.write(str(rootChord + 1.5))
        # Change sweep distance
        self.__repeatKeyboardInput("tab", 2)
        self.__inputKeyboardSequence(self.clearField)
        keyboard.write(str(sweepDistance))
        # Change tip chord
        keyboard.send("tab")
        self.__inputKeyboardSequence(self.clearField)
        keyboard.write(str(tipChord))
        # Change span
        keyboard.send("tab")
        self.__inputKeyboardSequence(self.clearField)
        keyboard.write(str(span))
        # Save fin parameters and close fin dialog
        self.__repeatKeyboardInput("shift+tab", 8)
        keyboard.send("enter")
        # Set tube length and close tube dialog
        if rocketSection == RocketSection.Sustainer:
            self.__repeatKeyboardInput("shift+tab", 5)
            self.__inputKeyboardSequence(self.clearField)
            keyboard.write(str(tubeLength))
            keyboard.send("shift+tab")
        else:
            pass
            self.__repeatKeyboardInput("tab", 6)
            self.__inputKeyboardSequence(self.clearField)
            keyboard.write(str(tubeLength))
            self.__repeatKeyboardInput("tab", 7)
        keyboard.send("enter")

    def setIgnitionDelayAndExportFlightSimData(self, filePath, ignitionDelay):
        """
        Set the ignition delay then export to csv and return to the main window
        
            Parameters:
                filePath (string): the file path including directory, file name, and extension
                ignitionDelay (string): the ignition delay of the simulation
                
            Returns:
                True if successful and False on failure to run the flight sim
        """
        # Set ignition delay
        self.mainWindow.ToolStrip1.Button8.click_input(double=True)
        self.mainWindow.child_window(title="Motor(s) Loaded Row 0", top_level_only=False).click_input(double=True)
        tabToIgnitionDelayField = ["tab", "tab", "tab", "tab", "tab", "tab", "backspace", "backspace"]
        self.__inputKeyboardSequence(tabToIgnitionDelayField)
        keyboard.write(str(ignitionDelay))
        self.__repeatKeyboardInput("tab", 6)
        keyboard.send("enter")
        # Verify sim completed
        if self.__verifySimCompletion():
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
            return True
        else:
            keyboard.send("alt+f4")
            keyboard.send("enter")
            return False

    def exportAeroPlot(self, filePath, sustainerOnly):
        self.mainWindow.ToolStrip1.Button7.click_input()
        time.sleep(5)

        if (not sustainerOnly):
            time.sleep(5)
            keyboard.send("shift+tab")
            time.sleep(2)
            keyboard.send("right")
            time.sleep(5)

        keyboard.send("alt+f")
        keyboard.send("enter")
        keyboard.send("enter")
        keyboard.write(filePath)
        keyboard.send("enter")
        keyboard.send("alt+f4")

    def __getTubeWindow(self, rocketSection):
        window = None

        if (rocketSection == RocketSection.Sustainer):
            self.mainWindow.ListBox1.ListItem4.click_input(double=True)
            window = self.mainWindow.child_window(title="Body Tube", top_level_only=False)
        elif (rocketSection == RocketSection.Booster):
            self.mainWindow.ListBox1.ListItem5.click_input(double=True)
            window = self.mainWindow.child_window(title="Booster", top_level_only=False)
        elif (rocketSection == RocketSection.NoseCone):
            self.mainWindow.ListBox1.ListItem1.click_input(double=True)
            window = self.mainWindow.child_window(title="Nose Cone", top_level_only=False)

        return window

    def __verifySimCompletion(self):
        valid = True
        keyboard.send("alt+f")
        keyboard.send("right")
        keyboard.send("down")
        keyboard.send("down")
        keyboard.send("enter")
        if self.mainWindow.Flight.UnstableDialog.exists() or self.mainWindow.Flight.Marginal.exists():
            valid = False
            keyboard.send("alt+f4")
            keyboard.send("alt+f4")
        return valid

    
    def __repeatKeyboardInput(self, keyName, repeatNum):
        for i in range(repeatNum):
            keyboard.send(keyName)

    def __inputKeyboardSequence(self, sequence):
        for key in sequence:
            keyboard.send(key)