# tasknotes

This is a stand-alone utility to enhance how you use [TaskWarrior](https://taskwarrior.org/). It uses the stardard TaskWarrior CLI commands and does not *directly* integrate into it, so you don't have to worry about it intefering with your TaskWarrior setup

## Install Instructions
Clone to your preferred spot.

Create a symlink to the python file: `sudo ln -s <path to tasknotes.py> /usr/local/bin/tasknotes`

...or use whatever your preferred method is.

## Configuration
There are two variables in tasknotes.py that you will be interested in modifying:

```
task_notes_parent_directory = '~/Documents/github/notes/tasknotes/'
editor = 'nvim'
```

## Usage
Use `tasknotes -t <task id>` to open the notes file for a task in your preferred editor.

tasknotes will automatically handle maintaining a set of project folders for your tasks.
