from morse.builder import *
from math import pi

bpymorse.set_speed(1000, 1, 1)

environment = 'TunnelFig11'
FOV = 12


""" rotor (atrv)"""
rotor = Bee()#Quadrotor()#ATRV()
rotor.translate (x=0,y=0.5, z=0.5)
rotor.rotate(z=0)
rotor.properties(NoGravity=True, GroundRobot=False)

rotord = Bee()#Quadrotor()#ATRV()
rotord.translate (x=1,y=0.5, z=0.5)
rotord.rotate(z=0)
rotord.properties(NoGravity=False, GroundRobot=False)

pose = Pose()
rotor.append(pose)
pose.add_service('socket')
pose.add_stream('socket')

#keyb = Keyboard()
#keyb.properties(Speed=5.5)
#rotor.append(keyb)

position = Position()
rotor.append(position)
position.add_stream('socket')
position.add_service('socket')

#motion6axes = Motion6axes()
#motion6axes.properties(ControlType='Position')
#rotor.append(motion6axes)
#motion6axes.add_stream('socket')
#motion6axes.add_service('socket')

collision = Collision()
rotor.append(collision)
collision.add_stream('socket')

#Sur matlab : FOV = 2*atand(32/(2*focal))
#           : focal = 32/2*tand(FOV/2)
#
#En Python  : focal = 32/(2*tan(radians(FOV/2)))
#
#Focale commune au camera (DeltaRho = DeltaPhy = FOV/3)

camG = Dem2px()
camG.translate(x=0.0, y=0.0, z=0.0)
camG.rotate(x=pi/2, y=0.0, z=pi)
rotor.append(camG)
camG.properties(Vertical_Flip=False, capturing = True, cam_width = 152, cam_height = 100, cam_fov = FOV)
camG.frequency(1000)
camG.add_service('socket')
camG.add_stream('socket')

camD = VideoCamera()
camD.translate(x=0.0, y=0.0, z=0.0)
camD.rotate(x=-pi/2, y=0.0, z=0.0)
rotor.append(camD)
camD.properties(Vertical_Flip=False, capturing = True, cam_width = 152, cam_height = 100, cam_fov = FOV)
camD.frequency(1000)
camD.add_service('socket')
camD.add_stream('socket')

camV = VideoCamera()
camV.translate(x=0.0, y=0.0, z=0.0)
camV.rotate(x=-pi/2, y=-pi/2, z=0.0)
rotor.append(camV)
camV.properties(Vertical_Flip=False, capturing = True, cam_width = 152, cam_height = 100, cam_fov = FOV)
camV.frequency(1000)
camV.add_service('socket')
camV.add_stream('socket')

camU = VideoCamera()
camU.translate(x=0.0, y=0.0, z=0.0)
camU.rotate(x=-pi/2, y=pi/2, z=0)
rotor.append(camU)
camU.properties(Vertical_Flip=False, capturing = True, cam_width = 152, cam_height = 100, cam_fov = FOV)
camU.frequency(1000)
camU.add_service('socket')
camU.add_stream('socket')

""" The playground """
env = Environment(environment)
env.set_gravity(0.0)
env.set_camera_location([-0.9, 0.25, 0.65])
env.set_camera_rotation([1.4, 0, -1.4])
env.set_camera_clip(0.01,50)
env.set_physics_step_sub(1)
env.configure_stream_manager('socket', time_sync = True, sync_port = 12000)
env.select_display_camera(camG)
#env.show_debug_properties()
env.show_framerate()
env.set_time_strategy(TimeStrategies.FixedSimulationStep)



