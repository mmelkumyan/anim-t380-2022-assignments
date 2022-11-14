from maya import OpenMayaUI as omui
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from shiboken2 import wrapInstance

import math

# Get a reference to the main Maya application window
mayaMainWindowPtr = omui.MQtUtil.mainWindow()
mayaMainWindow = wrapInstance(int(mayaMainWindowPtr), QWidget)


def create_parametric_sphere(radius, step_size):
    """
    Generates a parametric sphere out of default cubes. Centered at the origin.
    Parametric sphere equation: https://external-content.duckduckgo.com/iu/?u=http%3A%2F%2Fwww.songho.ca%2Fopengl%2Ffiles%2Fgl_sphere01.png&f=1&nofb=1&ipt=9cbb49b70493462ee88c03662117bd09799c84ccdae76ded3fe82271a91ec09d&ipo=images

    :param radius: Radius of the generated sphere.
    :param step_size: Size of each step around sphere in degrees. A higher value yields
        a lower resolution.
    """
    print("Creating a parametric sphere...")

    # Loop through positions on a sphere
    # Phi is latitude, theta is longitude
    for phi in range(-90, 91, step_size):
        for theta in range(0, 360, step_size):
            # Convert phi and theta to radians
            t, p = math.radians(theta), math.radians(phi)

            # Calculate position
            pos = radius * math.cos(p) * math.cos(t), \
                  radius * math.sin(p), \
                  radius * math.cos(p) * math.sin(t)

            # Generate and move cube
            maya.cmds.polyCube()
            maya.cmds.move(*pos)


class MyMayaWidget(QWidget):
    def __init__(self, *args, **kwargs):
        super(MyMayaWidget, self).__init__(*args, **kwargs)

        # Parent widget under Maya main window        
        self.setParent(mayaMainWindow)
        self.setWindowFlags(Qt.Window)

        # Set the UI display title and size    
        self.setWindowTitle('Parametric Sphere Generator')
        self.setGeometry(50, 50, 250, 150)

        # Create a button with the text 'Test'
        # You can see all the available widgets available
        # in PySide here:
        # https://srinikom.github.io/pyside-docs/PySide/QtGui/index.html
        self.generate_button = QPushButton('Test', self)

        # When the button is clicked, connect a signal to run
        # the function below
        self.generate_button.clicked.connect(self.generate_onClicked)

    def generate_onClicked(self):
        # Add code to run when the button is clicked here.
        # maya.cmds...
        print("Clicked!")
        create_parametric_sphere(5, 5)


my_widget = MyMayaWidget()
my_widget.show()
