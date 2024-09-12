import argparse
import os
import subprocess
import concurrent.futures
import statistics


def run_python_script(script_path: str):
    # check if windows or linux
    command = f'python3 {script_path}'
    if os.name == 'nt':
        command = f'python {script_path}'

    output = subprocess.run(command, shell=True,
                            capture_output=True, text=True)
    print(output.stdout.split("\n")[0])
    return output


def main():
    parser = argparse.ArgumentParser(
        description='Benchmarking script for the 2048 games.')
    parser.add_argument('--input', type=str, help='Input file')
    parser.add_argument('-n', nargs="?", const=10,
                        type=int, help='Number of iterations')
    args = parser.parse_args()

    if not args.input:
        print('Input file is required with --input [puzzle.py]')
        return

    results = []

    # get the stdout of the command
    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = list(executor.map(run_python_script,
                       [args.input] * (args.n or 10)))

    scores = []
    # print the results
    for i, result in enumerate(results):
        score = int(result.stdout.split(':')[-1].strip())
        if not score:
            print("Error: No score found, please make sure that the puzzle.py prints out the score at the end of the game.")
            print(
                "Example: `print(f'Score: {score}')` <- the `:` is important, or else it cannot parse the score.")
            return
        scores.append(score)

    print(f'Number of iterations: {args.n or 10}')
    # get the average score
    average = sum([score for score in scores]) / len(scores)
    print(f'Average Score: {average:.2f}')
    # get the median score
    mean = statistics.mean(scores)
    print(f'Mean Score: {mean:.2f}')
    # get the high score
    high_score = max(scores)
    print(f'High Score: {high_score}')
    # get the low score
    low_score = min(scores)
    print(f'Lowest Score: {low_score}')


if __name__ == '__main__':
    main()
