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
        self.resize(316, 105)

        # Create a button with the text 'Test'
        # You can see all the available widgets available
        # in PySide here:
        # https://srinikom.github.io/pyside-docs/PySide/QtGui/index.html
        self.generate_button = QPushButton('Generate', self)
        self.generate_button.setGeometry(QRect(230, 70, 75, 23))
        self.generate_button.clicked.connect(self.generate_onClicked)

        # Create radius text label
        self.radius_label = QLabel(self)
        self.radius_label.setGeometry(QRect(10, 10, 47, 13))
        self.radius_label.setText("Radius")

        # Create radius slider
        self.radius_slider = QSlider(self)
        self.radius_slider.setGeometry(QRect(60, 10, 160, 22))
        self.radius_slider.setOrientation(Qt.Horizontal)
        self.radius_slider.setRange(1, 20)
        self.radius_slider.setValue(5)
        self.radius_slider.valueChanged.connect(self.update_radius)

        # Create radius value label
        self.radius_val = QLineEdit(self)
        self.radius_val.setGeometry(QRect(230, 10, 71, 20))
        self.radius_val.setReadOnly(True)
        self.radius_val.setText(str(self.radius_slider.value()))

        # Create step text label
        self.step_label = QLabel(self)
        self.step_label.setGeometry(QRect(10, 40, 47, 13))
        self.step_label.setText("Step size")

        # Create step slider
        self.step_slider = QSlider(self)
        self.step_slider.setGeometry(QRect(60, 40, 160, 22))
        self.step_slider.setOrientation(Qt.Horizontal)
        self.step_slider.setRange(15, 90)
        self.step_slider.setValue(24)
        self.step_slider.valueChanged.connect(self.update_step)

        # Create step value label
        self.step_val = QLineEdit(self)
        self.step_val.setGeometry(QRect(230, 40, 71, 20))
        self.step_val.setReadOnly(True)
        self.step_val.setText(str(self.step_slider.value()))

    def update_radius(self):
        """
        Updates the value of radius value label on slider change
        """
        self.radius_val.setText(str(self.radius_slider.value()))

    def update_step(self):
        """
        Updates the value of step size value label on slider change
        """
        self.step_val.setText(str(self.step_slider.value()))

    def generate_onClicked(self):
        """
        Generates a parametric sphere using the given radius value
        """
        print("Generate clicked!")
        create_parametric_sphere(self.radius_slider.value(), self.step_slider.value())


my_widget = MyMayaWidget()
my_widget.show()
