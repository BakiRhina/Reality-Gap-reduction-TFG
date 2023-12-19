import rclpy
from rclpy.node import Node

import torch
import torch.nn as nn
import os

from ddpg import DDPGAgent
from configuration import Configuration



class Inference(Node):
    def __init__(self):
        super().__init__('inference')

        self.get_logger().info("Starting inference node...")

        # Instantiate DDPGAgent and Configuration
        self.config = Configuration()
        self.ddpg_model = DDPGAgent(self.config.state_dim, self.config.action_dim)
                
        train_or_pretrained = input("Hey do you want to 'train' from scratch or use a 'pretrained' model?")

        if train_or_pretrained == "pretrained":
            self.get_pretrained_model()

        elif train_or_pretrained == "train":
            print(f"training ddpg model from scratch...")
            self.get_plain_model()

        else:
            print("STFU goodbye")


    def get_pretrained_model(self):
        print(f"using pretrained model located in {model_path} ...")

        model_name = self.config.model_name
        model_path = os.path.expanduser(f'~/tfg/Simulation/src/models/{model_name}')
            
        # Load the state dictionaries
        checkpoint = torch.load('ddpg_model.pth')

        # Load the state dictionaries into the actor and critic models
        self.ddpg_model.actor.load_state_dict(checkpoint['actor_state_dict'])
        self.ddpg_model.critic.load_state_dict(checkpoint['critic_state_dict'])

    def get_plain_model(self):
        pass




if __name__ == '__main__':
    rclpy.init()
    inference = Inference()
    rclpy.spin(inference)
    inference.destroy_node()
    rclpy.shutdown()