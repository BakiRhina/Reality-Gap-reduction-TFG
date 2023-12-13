import subprocess
import os
import time
import psutil

from .configuration import Configuration
from .rosdata import RosData

class Reset():
    def __init__(self):
        print("Reset init...")
        self.config = Configuration()
        self.ros_data = RosData()

        self.reward_list = []
        self.reward_value = self.config.reward_init_value
        self.margin_value = self.config.margin_value
        
        self.maximum_accumulative_reward = self.config.maximum_accumulative_reward

    def reset(self):
        print("Resetting simulation...")
        self.kill_gazebo_process()
        time.sleep(3)
        self.run_gazebo()
        time.sleep(7)
        self.unpause()

    def kill_gazebo_process(self):
        # Find and kill the Gazebo process
        try:
            subprocess.run(['pkill', '-f', 'gazebo'], check=True)
        except subprocess.CalledProcessError:
            print("Failed to kill Gazebo process.")

    def run_gazebo(self):
        print("Check if gazebo is dead...")
        print(not self.is_gazebo_running())

        if not self.is_gazebo_running():
            print("starting gazebo simulator...")
            home_directory = os.path.expanduser("~")
            sdf_file_path = os.path.join(home_directory, 'tfg', 'Simulation', 'src', 'sdf_files', 'full_env_simpler.sdf')

            try:
                subprocess.Popen(['ign', 'gazebo', sdf_file_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            except subprocess.CalledProcessError:
                print("Failed to start Gazebo process.")
        
        else:
            print("Gazebo is still running...")
            time.sleep(1)
            print("Trying again...")
            self.reset()

    def unpause(self):
        # Use subprocess to execute the ros2 service call command
        command = 'ros2 service call /world/full_env_simpler/control ros_gz_interfaces/srv/ControlWorld "{world_control: {pause: false}}"'
        try:
            subprocess.run(command, shell=True, check=True)
            print("Simulation unpaused successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Failed to unpause simulation. Error: {e}")

    def is_gazebo_running(self):
        for process in psutil.process_iter(['pid', 'name']):
            if 'gazebo' in process.info['name']:
                return True
        return False
    
    def terminal_condition(self):
        self.reward_list.append(self.reward_value)

        if self.maximum_accumulative_reward == len(self.reward_list):
            margin = abs(self.margin_value * self.reward_list[0])
            difference = abs(self.reward_list[0] - self.reward_list[-1]) 
            self.reward_list = []

            if difference <= margin:
                print(f'Reached local minimum!')
                print(f'Difference: {round(difference, 4)}')
                print(f'Margin: {round(margin, 4)}')
                return True
                        
        elif (self.ros_data.state[11] or self.ros_data.state[8]) < 1.2:
            print(f'Oops, object dropped')
            return True
        
        else:
            return False
        
        return False
