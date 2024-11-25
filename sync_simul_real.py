import time
import numpy as np
import mujoco
import mujoco.viewer

from interface import SimulatedRobot
from robot import Robot

m = mujoco.MjModel.from_xml_path('low_cost_robot/scene.xml')
d = mujoco.MjData(m)

r = SimulatedRobot(m, d)

robot = Robot(device_name='/dev/tty.usbmodem58760435301')
# robot._disable_torque()
pwm = robot.read_position()
pwm = np.array(pwm)
d.qpos[:6] = r._pwm2pos(pwm)

with mujoco.viewer.launch_passive(m, d) as viewer:
    start = time.time()
    while viewer.is_running():
        step_start = time.time()
        # # TODO: ADD SYNC HERE
        pwm = robot.read_position()
        pwm = np.array(pwm)
        d.qpos[:6] = r._pwm2pos(pwm)

        mujoco.mj_step(m, d)

        viewer.sync()
        # Rudimentary time keeping, will drift relative to wall clock.
        time_until_next_step = m.opt.timestep - (time.time() - step_start)
        if time_until_next_step > 0:
            time.sleep(time_until_next_step)
