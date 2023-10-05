#!/usr/bin/env python3
# Copyright 2022 TOSIT.IO",
# SPDX-License-Identifier: Apache-2.0"

from termcolor import colored
import os
import os.path

def tdp_banner(title, subtitle):
    f=colored('.', 'white', 'on_white')
    def blue(text):
        return colored(text, 'blue', 'on_white', attrs=["bold"])
    def blck(text):
        return colored(text, 'black', 'on_white')
    def bblk(text):
        return colored(text, 'black', 'on_white', attrs=["bold"])
    print(f*80)
    print(f+bblk('{: ^78}'.format(' '.join(title.upper())))+f)
    print(f+blue("      ::: "+' '*68)+f)
    print(f+blue("       ::::  %%%%"+' '*61)+f)
    print(f+blue("        :: %%%%%% "+' '*60)+f)
    print(f+blue("     #### %%%%")+blck("        /%%%% %%%%%%%%%%%%%%%%%%%%%%%%%%%    %%%%%%%%%%%.       ")+f)
    print(f+blue("   ########   ")+blck("       %%%%%% %%%%%%%%%%%%%%%%%%%%%%%%%%%%%% %%%%%%%%%%%%%%     ")+f)
    print(f+blue("  ###   ####  ")+blck("     %%%%%   O     %%%%.    %%%%%       %%%%%%%%%.     %%%%%    ")+f)
    print(f+blck(         "        %%%%     %%%%%           %%%%.    %%%%%         %%%%%%%.     %%%%%    ")+f)
    print(f+blck(         "         %%%%%%%%%%%%            %%%%.                  %%%%%%%%%%%%%%%%%     ")+f)
    print(f+blck(         "           %%%%%%%%              %%%%.                 %%%%%%%%%%%%%%%%       ")+f)
    print(f+blck(         "                                 %%%%.         %%%%%%%%%%%%%%%%.              ")+f)
    print(f+blck(         "                                 %%%%.         %%%%%%%%%%  %%%%.              ")+f)
    print(f*80)
    print(f+blue(' '*9+'{: <69}'.format(subtitle))+f)
    print(f*80)


def find_file_path(file_name, cur_dir = os.getcwd()):
    while True:
        file_list = os.listdir(cur_dir)
        parent_dir = os.path.dirname(cur_dir)
        if file_name in file_list:
            return cur_dir
        else:
            if cur_dir == parent_dir: #if dir is root dir
                return None
            else:
                cur_dir = parent_dir


if __name__ == '__main__':
    tdp_banner('tdp utils', 'This is a banner')
