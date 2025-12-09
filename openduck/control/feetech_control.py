import rustypot
import numpy as np
import time

joints = {
    "left_hip_yaw": 20,
    "left_hip_roll": 21,
    "left_hip_pitch": 22,
    "left_knee": 23,
    "left_ankle": 24,
    # "neck_pitch": 30,
    # "head_pitch": 31,
    # "head_yaw": 32,
    # "head_roll": 33,
    "right_hip_yaw": 10,
    "right_hip_roll": 11,
    "right_hip_pitch": 12,
    "right_knee": 13,
    "right_ankle": 14,
}

zero_pos = {
        "left_hip_yaw": 0,
        "left_hip_roll": 0,
        "left_hip_pitch": 0,
        "left_knee": 0,
        "left_ankle": 0,
        "neck_pitch": 0,
        "head_pitch": 0,
        "head_yaw": 0,
        "head_roll": 0,
        # "left_antenna":0,
        # "right_antenna":0,
        "right_hip_yaw": 0,
        "right_hip_roll": 0,
        "right_hip_pitch": 0,
        "right_knee": 0,
        "right_ankle": 0,
    }

init_pos = {
        "left_hip_yaw": 0.04755340442445499,
        "left_hip_roll": 0.023009711818284817,
        "left_hip_pitch": -1.1320778214596032,
        "left_knee": 1.8499808301900833,
        "left_ankle": -0.5506991028509454,
        "neck_pitch": 0.0,
        "head_pitch": 0.0,
        "head_yaw": 0,
        "head_roll": 0,
        # "left_antenna": 0,
        # "right_antenna": 0,
        "right_hip_yaw": -0.19941750242513345,
        "right_hip_roll": -0.04141748127291223,
        "right_hip_pitch": 1.254796284490454,
        "right_knee": 1.7717478100079154,
        "right_ankle": -0.6013204688511715,
    }

stad_middle_pos = {
        "left_hip_yaw": 0.04755340442445499,
        "left_hip_roll": 0.05982525072754008,
        "left_hip_pitch": -0.6028544496390569,
        "left_knee": 1.0062913968529807,
        "left_ankle": -0.23163109897073175,
        "neck_pitch": 0.0,
        "head_pitch": 0.0,
        "head_yaw": 0,
        "head_roll": 0,
        # "left_antenna": 0,
        # "right_antenna": 0,
        "right_hip_yaw": -0.15186409800067846,
        "right_hip_roll": -0.009203884727313927,
        "right_hip_pitch": 0.6197282383057989,
        "right_knee": 1.0691846091562915,
        "right_ankle": -0.5307573526084317,
    }

stad_up_pos = {
        "left_hip_yaw": 0.16566992509164935,
        "left_hip_roll": 0.004601942363656963,
        "left_hip_pitch": -0.29912625363769996,
        "left_knee": 0.3052621767892427,
        "left_ankle": 0.13805827090970757,
        "neck_pitch": 0.0,
        "head_pitch": 0.0,
        "head_yaw": 0,
        "head_roll": 0,
        # "left_antenna": 0,
        # "right_antenna": 0,
        "right_hip_yaw": -0.16413594430376355,
        "right_hip_roll": 0.038349519697141066,
        "right_hip_pitch": 0.1334563285460506,
        "right_knee": 0.28071848418307255,
        "right_ankle": -0.1948155600614765,
    }


'''
{'left_hip_yaw': [0.16566992509164935], 'left_hip_roll': [0.004601942363656963], 'left_hip_pitch': [-0.29912625363769996], 'left_knee': [0.3052621767892427], 'left_ankle': [0.13805827090970757], 
'right_hip_yaw': [-0.16413594430376355], 'right_hip_roll': [0.038349519697141066], 'right_hip_pitch': [0.1334563285460506], 'right_knee': [0.28071848418307255], 'right_ankle': [-0.1948155600614765]}
'''

class FeetechControl:
    def __init__(self, port="/dev/ttyACM0", baudrate=1000000):
        self.port = port
        self.baudrate = baudrate
        self.driver = rustypot.feetech(self.port, self.baudrate)

        self.kps = list(np.ones(len(joints)) * 15)
        self.kds = list(np.ones(len(joints)) * 0)
        self.low_torque_kps = list(np.ones(len(joints)) * 3)
        self.high_torque_kps = list(np.ones(len(joints)) * 33) #For small jumps

    def set_kp(self, joint_name, kp):
        self.driver.set_kps(
            [joints[joint_name]], 
            [kp]
        )

    def set_kd(self, joint_name, kd):
        self.driver.set_kds(
            [joints[joint_name]], 
            [kd]
        )

    def set_position(self, joint_name, position):
        
        self.driver.write_goal_position(
            [joints[joint_name]], 
            [position]
        )
    
    def turn_on(self, high_torque=False):
        for id_, motor in enumerate(joints):
            if high_torque:
                self.driver.set_kps(
                    [joints[motor]],
                    [self.high_torque_kps[id_]]
                )
            else:
                self.driver.set_kps(
                    [joints[motor]],
                    [self.low_torque_kps[id_]]
                )

        print('Turning ON - Low kps set')
        time.sleep(0.2)

    def change_to_high_torque(self):
        for id_, motor in enumerate(joints):
            self.driver.set_kps(
                [joints[motor]],
                [self.high_torque_kps[id_]]
            )
        print('High kps set')
        time.sleep(0.2)

    def change_to_low_torque(self):
        for id_, motor in enumerate(joints):
            self.driver.set_kps(
                [joints[motor]],
                [self.low_torque_kps[id_]]
            )
        print('Low kps set')
        time.sleep(0.2)

    def set_positions(self, positions):
        for motor in joints.keys():
            self.driver.write_goal_position(
                [joints[motor]],
                [positions[motor]]
            )

    def read_positions(self):
        present_positions = {}
        for motor in joints.keys():
            present_positions[motor] = self.driver.read_present_position(
                [joints[motor]]
            )

        return present_positions

    def read_velocities(self):
        present_velocities = {}
        for motor in joints.keys():
            present_velocities[motor] = self.driver.read_present_velocity(
                [joints[motor]]
            )

        return present_velocities
        
    def turn_off(self):
        self.driver.disable_torque(
            list(joints.values())
        )

def main():
    driver = FeetechControl()
    driver.turn_on(high_torque=False)
    while True:
        driver.set_positions(init_pos)
        time.sleep(2)
        driver.set_positions(stad_middle_pos)
        time.sleep(2)


if __name__ == "__main__":
    main()