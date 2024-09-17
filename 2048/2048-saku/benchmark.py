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
    return df_tmp


def run_benchmark(iterations: int,
                  max_depth: int,
                  draw: bool = True) -> pd.DataFrame:

    sim_results = pd.DataFrame(columns=['Score', 'Biggest Tile', 'Max Depth', 'Time (s)'])

    with ThreadPoolExecutor() as executor:
        results = executor.map(
            run_game,
            [max_depth] * iterations,
            [draw] * iterations,
            range(iterations))

    return pd.concat([sim_results, *results])
