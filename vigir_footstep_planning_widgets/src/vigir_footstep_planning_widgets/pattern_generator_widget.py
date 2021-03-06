#!/usr/bin/env python

import math

import rospy
import tf
import std_msgs.msg

from rqt_gui_py.plugin import Plugin
from python_qt_binding.QtCore import Qt, Slot, QAbstractListModel
from python_qt_binding.QtGui import QWidget, QHBoxLayout, QVBoxLayout, QCheckBox, QLabel, QListWidget, QPushButton, QDoubleSpinBox, QFrame

from vigir_footstep_planning_msgs.msg import PatternGeneratorParameters
from vigir_footstep_planning_lib.parameter_set_widget import *
from vigir_footstep_planning_lib.qt_helper import *
from vigir_footstep_planning_lib.logging import *


class PatternGeneratorDialog(Plugin):

    def __init__(self, context):
        super(PatternGeneratorDialog, self).__init__(context)
        self.setObjectName('PatternGeneratorDialog')

        self._parent = QWidget()
        self._widget = PatternGeneratorWidget(self._parent)

        context.add_widget(self._parent)

    def shutdown_plugin(self):
        self._widget.shutdown_plugin()


class PatternGeneratorWidget(QObject):

    enable_pattern_generator = False

    def __init__(self, context):
        super(PatternGeneratorWidget, self).__init__()

        # publisher
        self.pattern_generator_params_pub = rospy.Publisher('pattern_generator/set_params', PatternGeneratorParameters, queue_size = 1)

        # start widget
        widget = context

        # start upper part
        hbox = QHBoxLayout()

        # start left column
        left_vbox = QVBoxLayout()

        # start button
        start_command = QPushButton("Start")
        start_command.clicked.connect(self.start_command_callback)
        left_vbox.addWidget(start_command)

        # simulation checkbox
        self.simulation_mode_checkbox = QCheckBox()
        self.simulation_mode_checkbox.setText("Simulation Mode")
        self.simulation_mode_checkbox.setChecked(False)
        left_vbox.addWidget(self.simulation_mode_checkbox)

        # realtime checkbox
        self.realtime_mode_checkbox = QCheckBox()
        self.realtime_mode_checkbox.setText("Realtime Mode")
        self.realtime_mode_checkbox.setChecked(False)
        left_vbox.addWidget(self.realtime_mode_checkbox)

        # joystick checkbox
        self.joystick_mode_checkbox = QCheckBox()
        self.joystick_mode_checkbox.setText("Joystick Mode")
        self.joystick_mode_checkbox.setChecked(False)
        self.joystick_mode_checkbox.clicked.connect(self.joystick_mode_check_callback)
        left_vbox.addWidget(self.joystick_mode_checkbox)

        # foot seperation
        self.foot_seperation = generate_q_double_spin_box(0.2, 0.15, 0.3, 2, 0.01)
        self.foot_seperation.valueChanged.connect(self.callback_spin_box)
        add_widget_with_frame(left_vbox, self.foot_seperation, "Foot Seperation (m):")

        # delta x
        self.delta_x = generate_q_double_spin_box(0.0, -0.4, 0.4, 2, 0.01)
        self.delta_x.valueChanged.connect(self.callback_spin_box)
        add_widget_with_frame(left_vbox, self.delta_x, "dX (m):")

        # delta y
        self.delta_y = generate_q_double_spin_box(0.0, -2.2, 2.2, 2, 0.01)
        self.delta_y.valueChanged.connect(self.callback_spin_box)
        add_widget_with_frame(left_vbox, self.delta_y, "dY (m):")

        # delta yaw
        self.delta_yaw = generate_q_double_spin_box(0.0, -30.0, 30.0, 0, 1.0)
        self.delta_yaw.valueChanged.connect(self.callback_spin_box)
        add_widget_with_frame(left_vbox, self.delta_yaw, "dYaw (deg):")

        # roll
        self.roll = generate_q_double_spin_box(0.0, -30.0, 30.0, 0, 1.0)
        self.roll.valueChanged.connect(self.callback_spin_box)
        add_widget_with_frame(left_vbox, self.roll, "Roll (deg):")

        # pitch
        self.pitch = generate_q_double_spin_box(0.0, -30.0, 30.0, 0, 1.0)
        self.pitch.valueChanged.connect(self.callback_spin_box)
        add_widget_with_frame(left_vbox, self.pitch, "Pitch (deg):")

        # end left column
        left_vbox.addStretch()
        hbox.addLayout(left_vbox, 1)

        # start right column
        right_vbox = QVBoxLayout()

        # stop button
        stop_command = QPushButton("Stop")
        stop_command.clicked.connect(self.stop_command_callback)
        right_vbox.addWidget(stop_command)

        # ignore collision
        self.collision_checkbox = QCheckBox()
        self.collision_checkbox.setText("Ignore Collision")
        self.collision_checkbox.setChecked(True)
        right_vbox.addWidget(self.collision_checkbox)

        # override 3D
        self.override_checkbox = QCheckBox()
        self.override_checkbox.setText("Override 3D")
        self.override_checkbox.setChecked(False)
        right_vbox.addWidget(self.override_checkbox)

        # end right coloumn
        right_vbox.addStretch()
        hbox.addLayout(right_vbox, 1)

        # add upper part
        hbox.setMargin(0)
        vbox = QVBoxLayout()
        vbox.addLayout(hbox)

        # parameter set selection
        self.parameter_set_widget = QParameterSetWidget()
        add_widget_with_frame(vbox, self.parameter_set_widget, "Parameter Set:")

        # end widget
        widget.setLayout(vbox)
        #context.add_widget(widget)

    def shutdown_plugin(self):
        print "Shutting down ..."
        self.pattern_generator_params_pub.unregister()
        print "Done!"

    # message publisher
    def _publish_parameters(self):
        params = PatternGeneratorParameters()

        params.enable = self.enable_pattern_generator
        params.simulation_mode = self.simulation_mode_checkbox.isChecked()
        params.joystick_mode = self.joystick_mode_checkbox.isChecked()
        params.d_step.position.x = self.delta_x.value()
        params.d_step.position.y = self.delta_y.value()
        params.d_step.position.z = 0
        q = tf.transformations.quaternion_from_euler(math.radians(self.roll.value()), math.radians(self.pitch.value()), math.radians(self.delta_yaw.value()))
        params.d_step.orientation.x = q[0]
        params.d_step.orientation.y = q[1]
        params.d_step.orientation.z = q[2]
        params.d_step.orientation.w = q[3]
        params.foot_seperation = self.foot_seperation.value()
        params.parameter_set_name.data = self.parameter_set_widget.current_parameter_set_name()

        print "Send stepping command = \n",params
        self.pattern_generator_params_pub.publish(params)

    # Define system command strings
    def start_command_callback(self):
        self.enable_pattern_generator = True
        self._publish_parameters()

    def stop_command_callback(self):
        self.enable_pattern_generator = False
        self._publish_parameters()

    def callback_spin_box(self, value_as_int):
        if self.realtime_mode_checkbox.isChecked():
            self._publish_parameters()

    def joystick_mode_check_callback(self):
        self.enable_pattern_generator = False
        self._publish_parameters()
