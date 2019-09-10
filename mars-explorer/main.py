#! /Users/kevinwkt/anaconda3/bin/python3
import argparse
import os
import sys
file_dir = os.path.dirname(__file__)
sys.path.append(file_dir)

from gui import GUI
from objects.command_center import CommandCenter
from objects.obstacle import Obstacle
from objects.rock import Rock
from objects.universe import Universe
from settings.defaults.default_map_1 import default_map_cfg_1

def create_universe(n_obstacles, n_rocks, n_explorers, default_map, mode):

    # Overrite universe details with default config files.
    if default_map == 'default_map_1':
        print('MAIN:: Overwriting universe with default_map_1...')
        n_rocks = default_map_cfg_1['rocks']
        n_obstacles = default_map_cfg_1['obstacles']
        n_explorers = default_map_cfg_1['explorers']

    # Create base universe.
    universe = Universe(1600, 1200, n_rocks)

    if mode == 'single':
        command_center = CommandCenter(800, 500)
        universe.add_object(command_center)
    else:
        universe.is_multiverse = True
        command_center_a = CommandCenter(200, 200)
        universe.add_object(command_center_a)
        command_center_b = CommandCenter(1500 - 200, 1000 - 200)
        universe.add_object(command_center_b)

    print(universe.is_multiverse)

    obstacles = Obstacle.create_obstacles(n_obstacles, universe)
    for obstacle in obstacles:
        universe.add_object(obstacle)

    rocks = Rock.create_rocks(n_rocks, universe)
    for rock in rocks:
        universe.add_object(rock)

    return universe

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--map', default='default_map_1', dest='default_map', type=str)
    parser.add_argument('--obstacles', default=500, dest='obstacles', type=int)
    parser.add_argument('--rocks', default=100, dest='rocks', type=int)
    parser.add_argument('--explorers', default=10, dest='explorers', type=int)
    parser.add_argument('--mode', default='double', dest='mode', type=str)


    args = parser.parse_args()

    print('MAIN:: Creating Universe...')
    # Create World States.
    universe = create_universe(args.obstacles,
                               args.rocks,
                               args.explorers,
                               args.default_map,
                               args.mode)

    print('MAIN:: Creating GUI...')
    gui = GUI(universe)
    print('MAIN:: Starting GUI...')
    gui.start()

if __name__ == '__main__':
    main()