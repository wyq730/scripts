#!/usr/bin/env python3

import subprocess
import os
import textwrap


def main():
    subprocess.run('apt-get update', shell=True, check=True)

    # Setup Zsh.
    try:
        subprocess.run(
            'yes | ZSH=$HOME/.oh-my-zsh RUNZSH=no sh -c "$(curl -fsSL https://raw.github.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"',
            shell=True, check=True)
    except subprocess.CalledProcessError as e:
        if e.returncode == 1:  # Zsh is already installed.
            subprocess.run('rm -r $HOME/.oh-my-zsh', shell=True, check=True)
            subprocess.run(
                'yes | ZSH=$HOME/.oh-my-zsh RUNZSH=no sh -c "$(curl -fsSL https://raw.github.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"',
                shell=True, check=True)
            print('finish')
        else:
            raise e
    subprocess.run('sed -i \'s/ZSH_THEME.*/ZSH_THEME="kphoen"/\' ~/.zshrc', shell=True, check=True)
    subprocess.run('export SHELL=$(which zsh)', shell=True, check=True)

    # Setup tmux.
    tmux_conf_filepath = os.path.expanduser('~/.tmux.conf')
    tmux_conf_content = textwrap.dedent("""
        set -g mouse on
        unbind C-b
        set-option -g prefix `
        bind ` send-prefix

        setenv -g SSH_AUTH_SOCK $HOME/.ssh/ssh_auth_sock
    """)
    with open(tmux_conf_filepath, 'w') as tmux_conf_file:
        tmux_conf_file.write(tmux_conf_content)

    # Setup Git.
    git_config_filepath = os.path.expanduser('~/.gitconfig')
    git_config_content = textwrap.dedent("""
        [user]
            name = Yanqing Wang
            email = yanqing.wang@tusimple.ai
        [push]
            default = simple
        [pull]
            rebase = false
        [alias]
            st = status
            co = commit
            di = diff
            lo = log --color --graph --decorate -M --pretty=oneline --abbrev-commit -M
    """)
    with open(git_config_filepath, 'w') as git_config_file:
        git_config_file.write(git_config_content)


if __name__ == "__main__":
    main()
