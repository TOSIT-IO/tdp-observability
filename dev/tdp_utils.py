#!/usr/bin/env python3
# Copyright 2022 TOSIT.IO",
# SPDX-License-Identifier: Apache-2.0"

from termcolor import colored
import os
import os.path

def tdp_banner(title, subtitle):
    print(colored(' '*80, 'cyan', 'on_white'))
    print(colored('{: ^80s}'.format(' '.join(title.upper())), 'black', 'on_white', attrs=["bold"]))
    print(colored(' '*80, 'cyan', 'on_white'))
    print(colored("      ....."+' '*69,'cyan', 'on_white'))
    print(colored("        ....  .***"+' '*62,'cyan', 'on_white'))
    print(colored("           ,*******"+' '*61,'cyan', 'on_white'))
    print(colored("     ,####.  * ", 'cyan', 'on_white')+colored("        (%%. .%%%%%%%%%%%%%%%%%%%%%%%%%%%    %%%%%%%%%%%.        ", 'black', 'on_white'))
    print(colored("  ,##########, ", 'cyan', 'on_white')+colored("      %%%%%. .%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% %%%%%%%%%%%%%%      ", 'black', 'on_white'))
    print(colored("   ###.  ##### ", 'cyan', 'on_white')+colored("    %%%%%%         %%%%.    %%%%%       %%%%%%%%%.     %%%%%     ", 'black', 'on_white'))
    print(colored("                  %%%%%    %%%    %%%%.    %%%%%         %%%%%%%.     %%%%%     ",'black', 'on_white'))
    print(colored("          %%%%%%%%%%%%            %%%%.                  %%%%%%%%%%%%%%%%%      ",'black', 'on_white'))
    print(colored("            #%%%%%%#              %%%%.                 %%%%%%%%%%%%%%%%        ",'black', 'on_white'))
    print(colored("                                  %%%%.         ####%%%%%%%%%%%%.               ",'black', 'on_white'))
    print(colored("                                  %%%%.         %%%%%%%%%%  %%%%.               ",'black', 'on_white'))
    print(colored(' '*80, 'cyan', 'on_white'))
    print(colored(' '*10+'{: <70s}'.format(subtitle), 'blue', 'on_white', attrs=["bold"]))
    print(colored(' '*80, 'cyan', 'on_white'))


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
