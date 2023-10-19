#!/usr/bin/env python3
# Copyright 2022 TOSIT.IO",
# SPDX-License-Identifier: Apache-2.0"

import sys
import re
import os
import json
from pathlib import Path
from git import Repo
from braceexpand import braceexpand
from termcolor import colored

from tdp_utils import tdp_banner, find_file_path

def include_file(filename, exclude_list):
    """ Returns true if filename not to be exluded """
    for exclude in exclude_list:
        if filename.startswith(exclude):
            return False
    return True

def glob_with_excludes(path, braced_glob, exclude_list):
    """ returns the list of files in path and subdirs that match braced_glob
        and that are not excluded by exclude list """
    file_list = [] 
    # glob does not handle braced globs    eg: *.{py,yml})
    # braceexpand will return simple globs eg: ['*.py', '*.yml']
    for glob in braceexpand(braced_glob):
        filtered = [ x for x in path.glob(glob) if include_file(str(x.relative_to(path)), exclude_list) ]
        file_list.extend(filtered)
    return file_list

def file_ok(file, matches):
    """ returns True if given file matches all regular expressions in matches """
    requested_lines = matches.copy()
    for line in open(file):
        for pattern in requested_lines:
            if re.search(pattern, line):
                requested_lines.remove(pattern)
        if len(requested_lines) == 0:
            return True
    return False

def license_check(files):
    """ check license headers """
    repo = Repo('.', search_parent_directories=True)
    git_root = os.path.basename(repo.git.rev_parse("--show-toplevel"))

    tdp_banner(git_root,'Running license block checker...')
    cfg_path=find_file_path('.licenserc.json')
    config = json.loads(Path(cfg_path+'/.licenserc.json').read_text())
    excludes=config['ignore']
    file_matchers=list(config.keys()-['ignore'])
    p = Path('.')
    ret=0
    for matcher in file_matchers:
        file_list=glob_with_excludes(p, matcher, excludes)        
        if files:
            asked_files = [];
            for file in files:
                if not os.path.exists(file):
                    print(colored("file does not exists",'yellow'), file.relative_to(p) )
                else:
                    if os.path.isdir(file):
                        asked_files.extend(p.glob(file+'/**/*'))
                    else:
                        asked_files.extend([ Path(file) ])
            file_list = list(set(file_list) & set(asked_files))
            file_list.sort()
        for file in file_list:
            if not file_ok(file, list(config[matcher])):
                print(colored("Copyright block missing or invalid.",'red'))
                print(colored(file.relative_to(p), 'blue')+':1')
                print()
                ret=1
    if ret == 0:
        print(colored("All files checked OK",'green'))

    return ret      

if __name__ == '__main__':
    sys.exit(license_check(sys.argv[1:]))
