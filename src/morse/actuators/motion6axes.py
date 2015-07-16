import logging; logger = logging.getLogger("morse." + __name__)
from morse.core.services import service
import morse.core.actuator
from morse.helpers.components import add_data, add_property

class Motion6axes(morse.core.actuator.Actuator):
    """
    This actuator reads the values of forwards movement x, sidewards
    movement y and angular speed w and applies them to the robot as
    direct translation. This controller is supposed to be used with
    robots that allow for sidewards movements.
    """

    _name = 'Linear and angular speed (Vx, Vy, Vz, Rx, Ry, Rz) actuator'

    _short_desc = 'Motion controller using linear and angular speeds'

    add_data('x', 0.0, 'float',
             'linear velocity in x direction (forward movement) (m/s)')
    add_data('y', 0.0, 'float',
             'linear velocity in y direction (sidewards movement) (m/s)')
    add_data('z', 0.0, 'float',
             'linear velocity in z direction (upwards movement) (m/s)')
    add_data('rx', 0.0, 'float', 'angular velocity (rad/s)')
    add_data('ry', 0.0, 'float', 'angular velocity (rad/s)')
    add_data('rz', 0.0, 'float', 'angular velocity (rad/s)')

    add_property('_type', 'Velocity', 'ControlType', 'string',
                 "Kind of control, can be one of ['Velocity', 'Position']")

    def __init__(self, obj, parent=None):
        logger.info('%s initialization' % obj.name)
        # Call the constructor of the parent class
        morse.core.actuator.Actuator.__init__(self, obj, parent)

        logger.info('Component initialized')

    @service
    def set_speed(self, x, y, z, rx, ry, rz):
        """
        Modifies v and w according to the parameters

        :param v: desired linear velocity (meter by second)
        :param w: desired angular velocity (radian by second)
        """
        self.local_data['x'] = x
        self.local_data['y'] = y
        self.local_data['z'] = z
        self.local_data['rx'] = rx
        self.local_data['ry'] = ry
        self.local_data['rz'] = rz

    def default_action(self):
        """ Apply (x, y, w) to the parent robot. """

        # Reset movement variables
        vx, vy, vz = 0.0, 0.0, 0.0
        rx, ry, rz = 0.0, 0.0, 0.0

        # Scale the speeds to the time used by Blender
        try:
            if self._type == 'Position':
                vx = self.local_data['x'] / self.frequency
                vy = self.local_data['y'] / self.frequency
                vz = self.local_data['z'] / self.frequency
                rx = self.local_data['rx'] / self.frequency
                ry = self.local_data['ry'] / self.frequency
                rz = self.local_data['rz'] / self.frequency
            else:
                vx = self.local_data['x']
                vy = self.local_data['y']
                vz = self.local_data['z']
                rx = self.local_data['rx']
                ry = self.local_data['ry']
                rz = self.local_data['rz']

        # For the moment ignoring the division by zero
        # It happens apparently when the simulation starts
        except ZeroDivisionError:
            pass

        self.robot_parent.apply_speed(self._type, [vx, vy, vz], [rx, ry, rz])
