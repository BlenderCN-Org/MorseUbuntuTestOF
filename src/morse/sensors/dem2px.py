import logging; logger = logging.getLogger("morse." + __name__)
from morse.core.services import async_service
from morse.core import status
import morse.core.blenderapi
from morse.core import blenderapi
from morse.core import mathutils
import morse.sensors.camera
from morse.helpers.components import add_data
from math import radians
from math import tan
import copy
import time
from PIL import Image
import os, sys
from PIL import ImageFilter
#from numpy import *
import numpy as np
#import glumpy

from morse.sensors.conv_gauss import convGauss

#import wx

BLENDER_HORIZONTAL_APERTURE = 32.0

class Dem2px(morse.sensors.camera.Camera):
    """
    This sensor emulates a single video camera. It generates a series of
    RGBA images.  Images are encoded as binary char arrays, with 4 bytes
    per pixel.

    Camera calibration matrix
    -------------------------

    The camera configuration parameters implicitly define a geometric camera in
    blender units. Knowing that the **cam_focal** attribute is a value that
    represents the distance in Blender unit at which the largest image dimension is
    32.0 Blender units, the camera intrinsic calibration matrix is defined as

    +--------------+-------------+---------+
    | **alpha_u**  |      0      | **u_0** |
    +--------------+-------------+---------+
    |       0      | **alpha_v** | **v_0** |
    +--------------+-------------+---------+
    |       0      |      0      |    1    |
    +--------------+-------------+---------+

    where:

    - **alpha_u** == **alpha_v** = **cam_width** . **cam_focal** / 32 (we suppose
      here that **cam_width** > **cam_height**. If not, then use **cam_height** in
      the formula)
    - cam_focal = 32/2*tan(radians(FOV/2))
    - **u_0** = **cam_height** / 2
    - **v_0** = **cam_width** / 2

    See also :doc:`./camera` for generic informations about Morse cameras.
    """
    _name = "DEM 2px"
    _short_desc = "DEM 2px"
    
    
    add_data('image', 'none', 'buffer', 'scalb',
           "The data captured by the camera, stored as a Python Buffer \
            class  object. The data is of size ``(cam_width * cam_height * 4)``\
            bytes. The image is stored as RGBA.")
    add_data('intrinsic_matrix', 'none', 'mat3<float>',
        "The intrinsic calibration matrix, stored as a 3x3 row major Matrix.")

    def __init__(self, obj, parent=None):
        """ Constructor method.

        Receives the reference to the Blender object.
        The second parameter should be the name of the object's parent.
        """
        logger.info('%s initialization' % obj.name)
        # Call the constructor of the parent class
        morse.sensors.camera.Camera.__init__(self, obj, parent)

        
        self.gaussMat = np.float32(np.array(np.genfromtxt('gauss.txt')))
        #self.gaussMat = np.array(np.genfromtxt('gauss8.txt'), dtype=np.int32)
        pxNb = round((self.image_width/50)-1)
        self.local_data['scalb'] = np.ndarray(pxNb)
        
        
        # Prepare the intrinsic matrix for this camera.
        # Note that the matrix is stored in row major
        intrinsic = mathutils.Matrix.Identity(3)
        alpha_u = self.image_width  * \
                  32/(2*tan(radians(self.image_fov/2))) / BLENDER_HORIZONTAL_APERTURE
        intrinsic[0][0] = alpha_u
        intrinsic[1][1] = alpha_u
        intrinsic[0][2] = self.image_width / 2.0
        intrinsic[1][2] = self.image_height / 2.0
        self.local_data['intrinsic_matrix'] = intrinsic

        self.capturing = False
        self._n = -1

        # Variable to indicate this is a camera
        self.camera_tag = True

        # Position of the robot where the last shot is taken
        self.robot_pose = copy.copy(self.robot_parent.position_3d)
        
        if not os.path.exists(self.name()):
            os.mkdir( self.name() )
        #fig = glumpy.figure((100,100))

        logger.info(" Component initialized, runs at %.2f Hz alpha_u = %0.2f", self.frequency, alpha_u)

    def interrupt(self):
        self._n = 0
        morse.sensors.camera.Camera.interrupt(self)

    @async_service
    def capture(self, n):
        """
        Capture **n** images

        :param n: the number of images to take. A negative number means
                  take image indefinitely
        """
        self._n = n

    def default_action(self):
        """ Update the texture image. """

        # Grab an image from the texture
        if self.bge_object['capturing'] and (self._n != 0) :

            # Call the action of the parent class
            morse.sensors.camera.Camera.default_action(self)

            # NOTE: Blender returns the image as a binary string
            #  encoded as RGBA
            image_data = morse.core.blenderapi.cameras()[self.name()].source
            
            #tload = time.time()

            img = Image.frombuffer('RGBA', (self.image_width, self.image_height), image_data)

            img = img.convert('L')
 
            
            tgauss = time.time()
            
            self.local_data['scalb'][:] = convGauss(np.array(img), self.gaussMat, self.image_height)
           
            tgauss = time.time() - tgauss


            
            
            #self.pixelFile.write("%0.3f  %0.3f  %0.3f  %0.3f  %0.3f  %0.3f  %0.3f  %0.3f  %0.3f  %0.3f  %0.3f  %0.3f  %f  %f  %f  %f\n" % (scal[0], scal[1], scal[2], scal[3], scal[4], scal[5], scalb[0], scalb[1], scalb[2], scalb[3], scalb[4], scalb[5], tgauss, tgrey, tblur, tload))
            
            
            #print("%0.4f" % blenderapi.persistantstorage().current_time)
            #print('%0.6f' % tgauss)
            

            self.robot_pose = copy.copy(self.robot_parent.position_3d)

            # Fill in the exportable data
            self.capturing = True

            if self._n > 0:
                self._n -= 1
                if self._n == 0:
                    self.completed(status.SUCCESS)
        else:
            self.capturing = False
