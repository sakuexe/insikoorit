import pandas as pd
from concurrent.futures import ThreadPoolExecutor


def _run_game(max_depth: int, draw: bool, index: int) -> pd.DataFrame:
    from puzzle import GameGrid

    game_grid = GameGrid(draw, max_depth=max_depth)
    tmp = {
        "Score": game_grid.points,
        "Biggest Tile": max(max(game_grid.matrix)),
        "Max Depth": max_depth
    }
    df_tmp = pd.DataFrame(tmp, index=[index])
    return df_tmp


def run_benchmark(iterations: int,
                  max_depth: int,
                  draw: bool = True) -> pd.DataFrame:

    sim_results = pd.DataFrame(columns=['Score', 'Biggest Tile', 'Max Depth'])

    for i in range(iterations):
        sim_results = pd.concat([sim_results, _run_game(max_depth, draw, i)])

    return sim_results
