import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-m', '--mode', type=str, help="The render mode",
                    choices=['human', 'ai', 'ai-cli'], 
                    default='human')
parser.add_argument('-e', "--episodes", type=int, 
                    help="The number of episodes.", 
                    default=1000)
parser.add_argument('-fps', "--fps", type=int, 
                    help="The rendering speed in frames per second",
                    default=None)
parser.add_argument('-f', "--file", type=str, 
                    help="The file name of the Q-table file",
                    default=None)
args = parser.parse_args()
print(args)
