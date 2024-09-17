import pandas as pd
import time
from concurrent.futures import ThreadPoolExecutor


def run_game(max_depth: int, draw: bool, index: int) -> pd.DataFrame:
    from puzzle import GameGrid
    time_start = time.time()

    game_grid = GameGrid(draw, max_depth=max_depth)

    tmp = {
        "Score": game_grid.points,
        "Biggest Tile": max(max(game_grid.matrix)),
        "Max Depth": max_depth,
        "Time (s)": (time.time() - time_start)
    }
    df_tmp = pd.DataFrame(tmp, index=[index])
    print(f"Game {index} has finished")
    return df_tmp


def run_benchmark(iterations: int,
                  max_depth: int,
                  draw: bool = True,
                  parallel: bool = False) -> pd.DataFrame:

    sim_results = pd.DataFrame(
        columns=['Score', 'Biggest Tile', 'Max Depth', 'Time (s)'])

    results: list[pd.DataFrame] = []

    if not parallel:
        for i in range(iterations):
            sim_results = pd.concat([
                sim_results if not sim_results.empty else pd.DataFrame(),
                run_game(max_depth, draw, i)
            ])
        return sim_results

    with ThreadPoolExecutor() as executor:
        results = list(executor.map(
            run_game,
            [max_depth] * iterations,
            [draw] * iterations,
            range(iterations)
        ))

        sim_results = pd.concat([
            sim_results if not sim_results.empty else pd.DataFrame(),
            *results
        ])

    # use this way of returning to avoid a FutureWarning
    return sim_results
