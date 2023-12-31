import rclpy
import os

from .sub_modules.rosdata import RosData
from .sub_modules.reset import Reset
from .sub_modules.configuration import Configuration
from .sub_modules.plots import plot_results

import numpy as np
import torch


#TODO - Tune hyperparameters (lr)


#SECTION - TRAINING LOOP -

def main(args=None):
    rclpy.init(args=args)
    config = Configuration()
    ros_data = RosData()
    reset = Reset()
    num_episodes = config.num_episodes

    episode_rewards = []

    for episode in range(num_episodes):

        print(f'Running poch: {episode}')

        reset.reset()
        
        # Waiting for the first state message to be received
        while not ros_data.state.any():
            print("Waiting for state data ...")
            rclpy.spin_once(ros_data)

        print("Training!")

        episode_reward_list = []

        while True:
            state = ros_data.state
            action = ros_data.agent.select_action(state)
            ros_data.move_joints(action)
            next_state = ros_data.state
            reward = ros_data.reward_value

            terminal_condition = reset.terminal_condition(state)

            # Update agent
            ros_data.agent.update(state, action, reward, next_state, terminal_condition)

            # Collect data for the current episode
            episode_reward_list.append(reward)

            rclpy.spin_once(ros_data)

            if terminal_condition:
                print(f'Terminal condition reached!')
                break
            
            elif len(episode_reward_list) == config.reward_count_to_save_model:
                avg_reward = np.mean(episode_reward_list)

                if abs(avg_reward) <= config.avg_reward_threshold_to_save_model:
                    model_path = os.path.expanduser('~/tfg/models/ddpg_model.pth')

                    torch.save({
                        'actor_state_dict': ros_data.agent.actor.state_dict(),
                        'critic_state_dict': ros_data.agent.critic.state_dict(),
                    }, model_path)

                    print(f'Model saved due to average reward less than {config.avg_reward_threshold_to_save_model}: {avg_reward}')
                    break


        # Store episode data for plotting
        episode_rewards.append(episode_reward_list)

        # Plot at the end of each episode
        plot_results(episode_rewards, ros_data.agent.actor_losses, ros_data.agent.critic_losses)


    ros_data.destroy_node()
    rclpy.shutdown()

#!SECTION


if __name__ == '__main__':
    main() 