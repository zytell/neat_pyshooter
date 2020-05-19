import time
import pickle
import os
from config_files.neat_game_config import (
    INPUT_SIZE, OUTPUT_SIZE, MAX_CLIENTS, GENERATIONS
)
from neat.client import Client
from neat.neat_main import Neat
from neat.neat_visual.visual import Visual
import importlib
from game_files import graphics
from utils.frame_counter import FrameCounter
from timeit import default_timer as timer


def create_folder():
    # creates folder for saving logs, returns folder path.
    master_path = 'saved/'
    if not os.path.exists(master_path):
        os.mkdir(master_path)
    folder_path = time.strftime("%Y%m%d-%H%M%S")
    full_folder_path = os.path.join(master_path, folder_path + '/')
    os.mkdir(full_folder_path)
    return full_folder_path


def save_client(folder_path, best_client, generation):
    # saves n clients to folders split by generations
    generation_folder_path = folder_path + str(generation + 1)
    os.mkdir(generation_folder_path)
    file_name = 'client.pkl'
    file_path = os.path.join(generation_folder_path, file_name)
    with open(file_path, 'wb') as output:
        pickle.dump(best_client, output)


def load_client(path, show_genome=False):
    # load a saved client:
    with open(path, 'rb') as inp:
        client = pickle.load(inp)
    if show_genome:
        Visual(client.genome)
    return client


def run_neat(n):

    for c in n.clients.data[:MAX_CLIENTS // 4]:
        # make random mutations on a quarter of the clients on generation 0
        for _ in range(GENERATIONS // 4):
            c.genome.mutate_random()

    last_time = 0
    FrameCounter()
    folder_path = None

    for i in range(GENERATIONS):
        c: Client
        for c in n.clients.data:
            score = graphics.main(client=c)
            importlib.reload(graphics)
            c.score = score
            # print(score)

        n.evolve()
        n.print_species(generation=i)
        curr_time = timer()
        print('time: %s' % round(curr_time - last_time, 2))
        print('best client score: %s' % max(n.clients.data, key=lambda x: x.score).score)
        last_time = curr_time

        if i == 0:
            # for each program init (first generation), create new folder.
            folder_path = create_folder()

        best_clients = max(n.clients, key=lambda x: x.score)  # saves the best n clients every generation
        save_client(folder_path, best_clients, generation=i)

    best_client = max(n.clients, key=lambda x: x.score)
    n.print_details(best_client)
    Visual(best_client.genome)


def main():
    load_prev_save = False

    if load_prev_save:
        print(
              '# -------------------------------------- #\n'
              ' CONTINUING EVOLUTION FROM EXISTING FILE\n'
              '# -------------------------------------- #'
        )
        path = 'saved/20200514-164135/70/client_0.pkl'
        client = load_client(path, show_genome=False)

        n = client.genome.neat
    else:
        n = Neat(input_size=INPUT_SIZE, output_size=OUTPUT_SIZE, max_clients=MAX_CLIENTS)

    run_neat(n)


if __name__ == '__main__':
    main()
