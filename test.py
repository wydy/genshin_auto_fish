import keyboard
import winsound
from models import FishNet
from environment import *
import torch
import argparse
import os

parser = argparse.ArgumentParser(description='Test Genshin finsing with DQN')
parser.add_argument('--n_states', default=3, type=int)
parser.add_argument('--n_actions', default=2, type=int)
parser.add_argument('--step_tick', default=12, type=int)
parser.add_argument('--model_dir', default='./output/fish_ys_net_46.pth', type=str)
args = parser.parse_args()

if __name__ == '__main__':

    net = FishNet(in_ch=args.n_states, out_ch=args.n_actions)
    env = Fishing(delay=0.1, max_step=10000, show_det=False)

    net.load_state_dict(torch.load(args.model_dir))
    net.eval()

    while True:
        winsound.Beep(500, 500)
        keyboard.wait('r')
        state = env.reset()
        for i in range(10000):
            state = torch.FloatTensor(state).unsqueeze(0)
            action = net(state)
            action = torch.argmax(action, dim=1).numpy()
            state, reward, done = env.step(action)
            if done:
                break