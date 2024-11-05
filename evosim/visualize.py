import os
import shutil
from concurrent.futures import ThreadPoolExecutor

import matplotlib
from matplotlib import patches

from evosim.constants import MAX_STEPS, NUM_GENERATIONS

matplotlib.use("Agg")

from matplotlib import pyplot as plt
from matplotlib.gridspec import GridSpec

from evosim.types import Coord, KillFn, Log
from evosim.utils import create_dir


def visualize(logs_by_gen: list[list["Log"]], kill_fn: KillFn):
    try:
        shutil.rmtree("./steps/")
    except:
        ...

    with ThreadPoolExecutor(max_workers=8) as executor:
        futures = [executor.submit(visualize_generation, generation, kill_fn) for generation in logs_by_gen]
        for future in futures:
            future.result()


def visualize_generation(generation: list["Log"], kill_fn: KillFn):
    # Only visualize first 3, last 3
    if not generation[0].generation in [
        0,
        1,
        2,
        NUM_GENERATIONS - 3,
        NUM_GENERATIONS - 2,
        NUM_GENERATIONS - 1,
        NUM_GENERATIONS ,
    ]:
        return

    # for log_state in generation:
    #     visualize_log(log_state, kill_fn)

    with ThreadPoolExecutor(max_workers=8) as executor:
        futures = [executor.submit(visualize_log, log_state, kill_fn) for log_state in generation]
        for future in futures:
            future.result()

    visualize_log(generation[-1], kill_fn, end_of_gen=True)


def visualize_log(log: Log, kill_fn: KillFn, end_of_gen: bool = False):
    agents = log.agents

    agent_colors = [agent.color for agent in agents]
    agent_coords = [agent.coord for agent in agents]
    agent_xs = [coord.x for coord in agent_coords]
    agent_ys = [coord.y for coord in agent_coords]

    # fig = plt.figure(figsize=(16, 10))
    fig = plt.figure(figsize=(8, 5))
    gs = GridSpec(2, 3, figure=fig)

    scatter_chart = fig.add_subplot(gs[:, :2])
    text_chart = fig.add_subplot(gs[:, 2])

    scatter_chart.set_title(f"World ({log.world_len}x{log.world_len})", fontsize=20)
    scatter_chart.scatter(agent_xs, agent_ys, c=agent_colors, label="Agents")
    scatter_chart.set_ylim(0, log.world_len)
    scatter_chart.set_xlim(0, log.world_len)

    # Highlight kill and live zone
    if end_of_gen:
        all_coords = [Coord(x, y) for x in range(log.world_len) for y in range(log.world_len)]
        for coord in all_coords:
            if kill_fn(log.world_len, coord):
                scatter_chart.add_patch(
                    patches.Rectangle(
                        (coord.x, coord.y),
                        1,
                        1,
                        linewidth=0,
                        edgecolor="r",
                        facecolor="red",
                        alpha=0.05,
                    )
                )

            else:
                scatter_chart.add_patch(
                    patches.Rectangle(
                        (coord.x, coord.y),
                        1,
                        1,
                        linewidth=0,
                        edgecolor="r",
                        facecolor="green",
                        alpha=0.1,
                    )
                )

    # Text
    fontsize = 24
    line_height = 0.05
    text_chart_y_pos = 1

    # text info
    generation_num = f"Generation: {log.generation}"
    step_num = f"Step: {log.step} / {MAX_STEPS}"
    if end_of_gen:
        step_num = f"Step: {MAX_STEPS} / {MAX_STEPS}"
    agent_num = f"Agent count: {len(agents)}"
    top_text = f"{generation_num}\n{step_num}\n{agent_num}"

    text_chart.text(
        0,
        text_chart_y_pos,
        top_text,
        horizontalalignment="left",
        verticalalignment="top",
        fontsize=fontsize,
        transform=text_chart.transAxes,
    )

    if end_of_gen:
        # Get agent death count
        agents_dead_num = len(list(filter(None, [kill_fn(log.world_len, agent.coord) for agent in agents])))
        agents_reproducing_num = len(agents) - agents_dead_num

        text_chart_y_pos -= line_height * top_text.count("\n") + 0.1

        agents_died_text = f"Agents died: {agents_dead_num}"
        text_chart.text(
            0,
            text_chart_y_pos,
            agents_died_text,
            horizontalalignment="left",
            verticalalignment="top",
            fontsize=fontsize,
            color="red",
            transform=text_chart.transAxes,
        )

        text_chart_y_pos -= line_height * agents_died_text.count("\n") + 0.1

        agents_reproduced_text = f"Agents reproduced: {agents_reproducing_num}"
        agents_next_gen_text = f"Agents next generation: {agents_reproducing_num*2}"
        blue_text = f"{agents_reproduced_text}\n{agents_next_gen_text}"
        text_chart.text(
            0,
            text_chart_y_pos,
            blue_text,
            horizontalalignment="left",
            verticalalignment="top",
            fontsize=fontsize,
            color="blue",
            transform=text_chart.transAxes,
        )

    text_chart.axis("off")  # hide axis

    # Add more details to the generation end text
    if end_of_gen:
        extra_details = ...

    # Create folder if doesn't exist
    create_dir(f"./steps")
    create_dir(f"./steps/{log.generation}")

    if end_of_gen:
        fig.savefig(f"./steps/{log.generation}/END.png")
    else:
        fig.savefig(f"./steps/{log.generation}/{log.generation}-{log.step}.png")
    fig.clf()
