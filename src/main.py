import argparse
import json
import os
import sys

import imageio
import matplotlib
from matplotlib import pyplot as plt

from src.agents.simple_agent import SimpleAgent
from src.behaviours.behaviour_utils import create_behaviours
from src.worlds.hexagon_2D.hexagon_2D_location import Hexagon2DLocation
from src.worlds.hexagon_2D.hexagon_2D_world import Hexagon2DWorld

matplotlib.use("Agg")


def create_parser() -> argparse.ArgumentParser:
    argument_parser = argparse.ArgumentParser()
    argument_parser.add_argument("--configuration_file", nargs="?", default="./configurations/40_agents_vers1.json")
    argument_parser.add_argument("--path_to_results", nargs="?", default="./result")
    argument_parser.add_argument("--create_result_graph", nargs="?", default="True")
    argument_parser.add_argument("--create_step_images", nargs="?", default="True")
    argument_parser.add_argument("--create_gif", nargs="?", default="True")
    argument_parser.add_argument("--gif_duration", nargs="?", default="4")

    return argument_parser


def create_agents(
    agent_locations: list[Hexagon2DLocation],
    target_location: Hexagon2DLocation,
    walls: list[Hexagon2DLocation],
    strategy: str
) -> list[SimpleAgent]:
    behaviours = create_behaviours(agent_locations, target_location, walls, strategy)
    return [
        SimpleAgent(agent_id=i, cluster_id=0, behaviour=behaviour)
        for i, behaviour in zip(range(len(behaviours)), behaviours)
    ]


def create_gif(path_to_results: str, gif_duration: str, num_of_steps: int) -> None:
    images = []
    for index in range(num_of_steps):
        images.append(imageio.v2.imread(path_to_results + f"/img/img_{index}.png"))
    imageio.mimsave(path_to_results + "/result.gif", images, duration=int(gif_duration))


def create_accuracy_graph(path_to_results: str, strategy: str):
    figure = plt.figure(figsize=(18, 5))

    sub_plot_accuracy = figure.add_subplot(1, 3, 1)
    plt.xlabel("Step number", fontsize="xx-large")
    plt.ylabel("Accuracy", fontsize="xx-large")

    with open(path_to_results + "/result.json", "r") as file:
        result = json.load(file)
        x_value = [value for value in result["accuracy"]]

    plt.plot(range(len(x_value)), x_value, label=strategy)
    plt.legend(loc="upper right")

    sub_plot_diameter = figure.add_subplot(1, 3, 2)
    plt.xlabel("Step number", fontsize="xx-large")
    plt.ylabel("Diameter", fontsize="xx-large")

    with open(path_to_results + "/result.json", "r") as file:
        result = json.load(file)
        x_value = [value for value in result["diameter"]]

    plt.plot(range(len(x_value)), x_value, label=strategy)
    plt.legend(loc="upper right")

    sub_plot_num_of_clusters = figure.add_subplot(1, 3, 3)
    plt.xlabel("Step number", fontsize="xx-large")
    plt.ylabel("Number of clusters", fontsize="xx-large")

    if strategy == "Meso":
        with open(path_to_results + "/result.json", "r") as file:
            result = json.load(file)
            x_value = [value for value in result["num_of_clusters"]]

        plt.plot(range(len(x_value)), x_value, label=strategy)
        plt.legend(loc="upper right")

    plt.savefig(path_to_results + f"/accuracy.svg", transparent=False, facecolor="white", dpi=300)


def main():
    parser = create_parser()
    args = parser.parse_args(sys.argv[1:])
    print(args)

    with open(args.configuration_file, "r", encoding="utf-8") as file:
        configuration_data = json.load(file)

    num_of_tiles_side = configuration_data["num_of_tiles"]
    num_of_steps = configuration_data["num_of_steps"]
    target_location = Hexagon2DLocation.of(configuration_data["target_location"])
    strategy = configuration_data["type_of_strategy"]
    walls = [
        Hexagon2DLocation.of(location)
        for location in configuration_data["wall_locations"]
    ]
    agent_locations = [
        Hexagon2DLocation.of(location)
        for location in configuration_data["agent_locations"]
    ]
    agents = create_agents(
        agent_locations=agent_locations,
        target_location=target_location,
        walls=walls,
        strategy=strategy
    )

    path_to_results = args.path_to_results + "/" + strategy
    simulation_world = Hexagon2DWorld(
        num_of_tiles_side=num_of_tiles_side,
        agents=agents,
        num_steps=num_of_steps,
        walls=walls,
        path_to_results=path_to_results,
        create_step_images=args.create_step_images
    )

    if not os.path.exists(path_to_results):
        os.mkdir(path_to_results)

    simulation_world.start()
    simulation_world.join()

    if args.create_gif == "True":
        if args.create_step_images == "True":
            create_gif(
                path_to_results=path_to_results,
                gif_duration=args.gif_duration,
                num_of_steps=num_of_steps
            )
        else:
            print("Can't create gif: not created step images")

    if args.create_result_graph == "True":
        create_accuracy_graph(path_to_results=path_to_results, strategy=strategy)


if __name__ == "__main__":
    main()
