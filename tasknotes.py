#!/usr/bin/python
# install via symbolic link: sudo ln -s <path to tasknotes.py> /usr/local/bin/tasknotes

import argparse
import os.path
import subprocess

argparser = argparse.ArgumentParser(prog='tasknotes')
arggroup = argparser.add_mutually_exclusive_group(required=True)
arggroup.add_argument('-s', '--sync', action='store_true', help="Creates folders for projects and text files for tasks.")
arggroup.add_argument('-t', '--task', type=str, help="Open notes for the task for editing.")
args = argparser.parse_args()

task_notes_parent_directory = '~/Documents/github/notes/tasknotes/'
editor = 'nvim'


def parse_task(task_id):
    task_data = subprocess.run('task ' + task_id, shell=True, capture_output=True, text=True).stdout.split('\n')
    for td in task_data:
        if len(set(td.replace(' ', ''))) == 1:
            fixed_width_fields = td.split(' ')
            name_col_width = len(fixed_width_fields[0])
            break
    
    task_dict = {}
    for td in task_data:
        if len(td) > 0:
            task_dict[td[:name_col_width].strip()] = td[name_col_width + 1:].strip()

    return task_dict


def sync():
    # sync project folders
    task_list = subprocess.run('task ls', shell=True, capture_output=True, text=True).stdout.split('\n')
    id_field_width = len(task_list[2].split(' ')[0])
    project_field_width = len(task_list[2].split(' ')[1])

    # strip the header and footer lines
    task_list = task_list[3:len(task_list)-3]

    for task in task_list:
        if task[:id_field_width].strip() != '':
            project = task[id_field_width+1:project_field_width+id_field_width+1].strip()
            subprocess.run('mkdir -p ' + task_notes_parent_directory + project.replace('.', '/'), shell=True)

            id = task[:id_field_width].strip()
            uuid = subprocess.run('task ' + id + ' uuids', shell=True, capture_output=True, text=True).stdout.strip()
            task_file = task_notes_parent_directory + project.replace('.','/') + '/' + uuid + '.txt'
            # turns out that python doesn't handle things like ~ for home directory, so also using bash to test if file exists
            if subprocess.run('if [ -f ' + task_file + ' ]; then echo "True"; else echo "False"; fi', shell=True, capture_output=True, text=True).stdout.strip() == "False":
                subprocess.run('task ' + id + ' > ' + task_file, shell=True)

def edit(task_id):
    task_data = parse_task(task_id)
    subprocess.run(editor + ' ' + task_notes_parent_directory + task_data['Project'].replace('.','/') + '/' + task_data['UUID'] + '.txt', shell=True)

if args.sync:
    sync()
elif args.task:
    edit(args.task)
