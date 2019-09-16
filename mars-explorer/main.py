#! /Users/kevinwkt/anaconda3/bin/python3
import argparse
import random

from gui import GUI
from objects.command_center import CommandCenter
from objects.explorer import Explorer
from objects.obstacle import Obstacle
from objects.rock import Rock
from objects.universe import Universe
from settings.constants import MarsBaseEnum
from settings.constants import UniverseEnum
from settings.defaults.default_map_1 import default_map_cfg_1, default_map_cfg_2

def create_universe(n_obstacles, n_rocks, n_explorers, default_map, mode, multi_agent):

    print(multi_agent)

    # Let's avoid magic numbers.
    ARBITRARY_EDGE_SPACE = 200
    ARBITRARY_UNIVERSE_WIDTH = 1600
    ARBITRARY_UNIVERSE_HEIGHT = 900
    ARBITRARY_SPAWN_OFFSET = 10

    # Overrite universe details with default config files.
    if default_map == 'default_map_1':
        print('MAIN:: Overwriting universe with default_map_1...')
        n_rocks = default_map_cfg_1['rocks']
        n_obstacles = default_map_cfg_1['obstacles']
        n_explorers = default_map_cfg_1['explorers']
    elif default_map == 'default_map_2':
        print('MAIN:: Overwriting universe with default_map_2...')
        n_rocks = default_map_cfg_2['rocks']
        n_obstacles = default_map_cfg_2['obstacles']
        n_explorers = default_map_cfg_2['explorers']

    # Create base universe. We also send n_rocks for terminal condition.
    universe = Universe(ARBITRARY_UNIVERSE_WIDTH, ARBITRARY_UNIVERSE_HEIGHT, n_rocks, mode)

    # Create command centers depending on the execution mode.
    if mode == UniverseEnum.MICROVERSE:
        print('MAIN:: Implementing universe in single mode...')
        command_center_a = CommandCenter(ARBITRARY_UNIVERSE_WIDTH/2,
                                         ARBITRARY_UNIVERSE_HEIGHT/2,
                                         MarsBaseEnum.A)
        universe.add_object(command_center_a, MarsBaseEnum.A)
    elif mode == UniverseEnum.MULTIVERSE:
        print('MAIN:: Implementing universe in multiverse (2 mars bases) mode...')
        universe.is_multiverse = True
        command_center_a = CommandCenter(ARBITRARY_EDGE_SPACE, ARBITRARY_EDGE_SPACE, MarsBaseEnum.A)
        universe.add_object(command_center_a, MarsBaseEnum.A)
        command_center_b = CommandCenter(ARBITRARY_UNIVERSE_WIDTH-ARBITRARY_EDGE_SPACE,
                                         ARBITRARY_UNIVERSE_HEIGHT-ARBITRARY_EDGE_SPACE,
                                         MarsBaseEnum.B)
        universe.add_object(command_center_b, MarsBaseEnum.B)

    # Create explorers in the universe.
    print('MAIN:: Deploying explorers into the universe...')
    for _ in range(n_explorers):
        random_team = bool(random.getrandbits(1)) if mode == UniverseEnum.MULTIVERSE else True
        if random_team:
            explorer = Explorer(command_center_a.x + ARBITRARY_SPAWN_OFFSET,
                                command_center_a.y + ARBITRARY_SPAWN_OFFSET,
                                MarsBaseEnum.A,
                                universe,
                                multi_agent)
        else:
            explorer = Explorer(command_center_b.x + ARBITRARY_SPAWN_OFFSET,
                                command_center_b.y + ARBITRARY_SPAWN_OFFSET,
                                MarsBaseEnum.B,
                                universe,
                                multi_agent)
        universe.add_object(explorer)

    # Create obstacles in the universe.
    print('MAIN:: Forming obstacles in the universe...')
    obstacles = Obstacle.create_obstacles(n_obstacles, universe)
    for obstacle in obstacles:
        universe.add_object(obstacle)

    # Create rocks to collect in the universe.
    print('MAIN:: Forming rocks in the universe...')
    rocks = Rock.create_rocks(n_rocks, universe)
    for rock in rocks:
        universe.add_object(rock)

    return universe

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--map', default='default_map_1', dest='default_map', type=str,
                        help='load default maps from /settings/defaults, defaults to default_map_1')
    parser.add_argument('--obstacles', default=40, dest='obstacles', type=int,
                        help='total number of obstacles, defaults to 40')
    parser.add_argument('--rocks', default=100, dest='rocks', type=int,
                        help='total number of rocks, defaults to 100')
    parser.add_argument('--explorers', default=10, dest='explorers', type=int,
                        help='total number of explorers, defaults to 10')
    parser.add_argument('--mode', default='double', dest='mode', type=str,
                        help=('mode of simulation, single or double (number of mars bases), '
                        'defaults to double'))
    parser.add_argument('--multi_agent', default=False, dest='multi_agent', action='store_true',
                        help=('if multi-agent mode is enabled, explorers will share a message queue so that'
                        ' they know where to go'))

    args = parser.parse_args()

    print('MAIN:: Creating Universe...')
    # Create Universe States.
    universe = create_universe(args.obstacles,
                               args.rocks,
                               args.explorers,
                               args.default_map,
                               UniverseEnum.MICROVERSE if args.mode=='single' else UniverseEnum.MULTIVERSE,
                               args.multi_agent)

    print('MAIN:: Creating GUI...')
    gui = GUI(universe)
    print('MAIN:: Starting GUI...')
    gui.start()

if __name__ == '__main__':
    main()