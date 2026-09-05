#!/usr/bin/env python
import argparse
import os
import subprocess
import sys
from datetime import datetime, timedelta
from random import randint


def main(def_args=sys.argv[1:]):
    args = arguments(def_args)
    curr_date = datetime.now()
    directory = 'repository-' + curr_date.strftime('%Y-%m-%d-%H-%M-%S')
    repository = args.repository
    user_name = args.user_name
    user_email = args.user_email
    if repository is not None:
        start = repository.rfind('/') + 1
        end = repository.rfind('.')
        if end > start:
            directory = repository[start:end]
        else:
            directory = repository[start:]
    no_weekends = args.no_weekends
    frequency = args.frequency
    days_before = args.days_before
    if days_before < 0:
        sys.exit('days_before must not be negative')
    days_after = args.days_after
    if days_after < 0:
        sys.exit('days_after must not be negative')

    if os.path.exists(directory):
        import shutil
        shutil.rmtree(directory, ignore_errors=True)
    os.mkdir(directory)
    os.chdir(directory)

    run(['git', 'init', '-b', 'main'])

    if user_name is not None:
        run(['git', 'config', 'user.name', user_name])

    if user_email is not None:
        run(['git', 'config', 'user.email', user_email])

    start_date = curr_date.replace(hour=20, minute=0, second=0, microsecond=0) - timedelta(days=days_before)
    total_days = days_before + days_after
    total_commits = 0

    print(f"Generating activity for {total_days} days (from {start_date.strftime('%Y-%m-%d')} to {(start_date + timedelta(days=total_days)).strftime('%Y-%m-%d')})...")

    readme_path = os.path.join(os.getcwd(), 'README.md')
    with open(readme_path, 'w', encoding='utf-8') as file:
        file.write('# Activity Log\n\n')

    for i in range(total_days):
        day = start_date + timedelta(days=i)
        if (not no_weekends or day.weekday() < 5) and randint(0, 100) < frequency:
            commits_today = contributions_per_day(args)
            for m in range(commits_today):
                commit_time = day + timedelta(minutes=m * 10 + randint(1, 5))
                contribute(readme_path, commit_time)
                total_commits += 1

        if (i + 1) % 50 == 0 or (i + 1) == total_days:
            print(f"Progress: {i + 1}/{total_days} days processed ({total_commits} commits created)")

    if repository is not None:
        print(f"Configuring remote origin: {repository}")
        run(['git', 'remote', 'add', 'origin', repository])
        run(['git', 'branch', '-M', 'main'])
        print("Pushing commits to GitHub...")
        res = subprocess.run(['git', 'push', '-u', 'origin', 'main'], capture_output=True, text=True)
        if res.returncode != 0:
            print(f"Error pushing to repository: {res.stderr}")
            sys.exit(res.returncode)
        else:
            print(res.stdout)

    print(f"\nActivity generation completed successfully! Total commits generated: {total_commits}")


def contribute(readme_path, date):
    with open(readme_path, 'a', encoding='utf-8') as file:
        file.write(message(date) + '\n\n')
    subprocess.run(['git', 'add', 'README.md'], check=True, capture_output=True)
    date_str = date.strftime('%Y-%m-%d %H:%M:%S')
    subprocess.run(['git', 'commit', '-m', message(date), '--date', date_str], check=True, capture_output=True)


def run(commands):
    subprocess.run(commands, check=True)


def message(date):
    return date.strftime('Contribution: %Y-%m-%d %H:%M:%S')


def contributions_per_day(args):
    max_c = args.max_commits
    if max_c > 20:
        max_c = 20
    if max_c < 1:
        max_c = 1
    return randint(1, max_c)


def arguments(argsval):
    parser = argparse.ArgumentParser(description="GitHub Activity Generator")
    parser.add_argument('-nw', '--no_weekends',
                        required=False, action='store_true', default=False,
                        help="do not commit on weekends")
    parser.add_argument('-mc', '--max_commits', type=int, default=10,
                        required=False, help="maximum amount of commits a day (1-20)")
    parser.add_argument('-fr', '--frequency', type=int, default=80,
                        required=False, help="percentage of days with commits (default: 80)")
    parser.add_argument('-r', '--repository', type=str, required=False,
                        help="link to an empty non-initialized remote git repository")
    parser.add_argument('-un', '--user_name', type=str, required=False,
                        help="overrides user.name git config")
    parser.add_argument('-ue', '--user_email', type=str, required=False,
                        help="overrides user.email git config")
    parser.add_argument('-db', '--days_before', type=int, default=365,
                        required=False, help="number of days before current date (default: 365)")
    parser.add_argument('-da', '--days_after', type=int, default=0,
                        required=False, help="number of days after current date (default: 0)")
    return parser.parse_args(argsval)


if __name__ == "__main__":
    main()
