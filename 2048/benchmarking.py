import argparse
import os
import subprocess


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

    # check if windows or linux
    command = f'python3 {args.input}'
    if os.name == 'nt':
        command = f'python {args.input}'

    results = []

    # get the stdout of the command
    for i in range(args.n or 10):
        results.append(subprocess.run(command, shell=True,
                       capture_output=True, text=True))

    scores = []
    # print the results
    for i, result in enumerate(results):
        scores.append(int(result.stdout.split(':')[-1].strip()))
        print(f'Score Game #{i + 1}: {scores[-1]}')

    # get the average score
    average = sum([score for score in scores]) / len(scores)
    print(f'Average Score: {average:.2f}')
    # get the high score
    high_score = max(scores)
    print(f'High Score: {high_score}')
    # get the low score
    low_score = min(scores)
    print(f'Lowest Score: {low_score}')


if __name__ == '__main__':
    main()
