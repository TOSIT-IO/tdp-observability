#!/usr/bin/env python3
# Copyright 2022 TOSIT.IO
# SPDX-License-Identifier: Apache-2.0

import sys, os, re
from git import Repo
from tdp_utils import tdp_banner
from termcolor import colored

def is_conventionnal_commit(message):
    commit_types = [ "feat", "fix", "docs", "style", "refactor", "test", "build", "perf", "ci", "chore", "revert", "merge", "wip" ]
    pattern = '('+'|'.join(commit_types)+')(\([\w\-\s]+\))?!?\s?:\s.*'
    if message.startswith('Merge ') or message.startswith('Revert '):
        return True

    if re.match(pattern, message) == None:
        return False
    return True

def check_commit_messages(ranges):
    repo = Repo('.', search_parent_directories=True)
    git_root = os.path.basename(repo.git.rev_parse("--show-toplevel"))
    tdp_banner(git_root,'Running commit messages checker...')
    ret = 0
    count = 0
    for git_range in ranges:
        commits = repo.git.log(git_range, "--pretty=tformat:%h %s").split('\n')
        if commits != ['']:
            for commit in commits:
                count += 1
                git_hash = commit.split(' ')[0]
                message = ' '.join(commit.split(' ')[1:])
                if is_conventionnal_commit(message):
                    print(colored(git_hash,'blue'),":",colored("commit message OK", 'green'),":", message)
                else:
                    ret = 1
                    print(colored(git_hash,'blue'),":",colored("commit message KO", 'red'),":", message)
    if count == 0:
        print(colored("INFO :",'blue'),":","no commits to check")


    return ret
if __name__ == '__main__':
    if len(sys.argv) == 1:
        commit_ranges=[ 'origin/HEAD..HEAD' ]
    else:
        commit_ranges=sys.argv[1:]
    sys.exit(check_commit_messages(commit_ranges))
