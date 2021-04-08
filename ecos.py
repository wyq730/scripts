#!/usr/bin/env python3

import sys
from argparse import ArgumentParser
import textwrap
import os
import subprocess


class AutoHintArgumentParser(ArgumentParser):
    def error(self, message):
        sys.stderr.write('error: %s\n' % message)
        self.print_help()
        sys.exit(2)


def prepend(filepath, content):
    with open(filepath, 'r') as original:
        data = original.read()
    with open(filepath, 'w') as modified:
        modified.write(content + "\n" + data)


def main():
    parser = AutoHintArgumentParser()
    parser.add_argument("host_ip", help="the IP of the host to login")
    parser.add_argument('-f', '--first', action='store_true',
                        help='if it\'s the first time to login')
    parser.add_argument('-u', '--user', default='root', help='the user to login')
    parser.add_argument('--password', default='root', help='the password to login')
    parser.add_argument('--port', default=22, help='the SSH port')

    args = parser.parse_args()

    host_ip = args.host_ip
    port = args.port
    user = args.user
    password = args.password
    is_first = args.first

    ssh_pass = 'sshpass -p {}'.format(password)
    ssh = 'ssh {}@{} -p {}'.format(user, host_ip, port)

    if is_first:
        ssh_config_content = textwrap.dedent("""
        # This is an SSH config for an ECOS container.
        # Please remove it if the ECOS container has been killed.
        Host {}
            StrictHostKeyChecking no
            ForwardAgent yes
        """.format(host_ip))
        prepend(os.path.expanduser('~/.ssh/config'), ssh_config_content)

        res = subprocess.run(
            '{} {} "test -e ~/.ready && echo \'yes\' || echo \'no\'"'.format(ssh_pass, ssh),
            shell=True, capture_output=True, check=True)

        subprocess.run(
            '{} ssh-copy-id {}@{} -p {}'.format(ssh_pass, user, host_ip, port),
            shell=True, check=True)

        if res.stdout == b'yes\n':
            print('The container has already been set up. Login directly now.')
        else:
            subprocess.run(
                '{} \'python3 -c \"$(curl -L https://raw.githubusercontent.com/wyq730/scripts/main/setup_environment.py\?$(date +%s))\"\''.format(ssh),
                shell=True, check=True)
            subprocess.run('{} {} "touch ~/.ready"'.format(ssh_pass, ssh), shell=True, check=True)

    subprocess.run(ssh, shell=True, check=True)


if __name__ == "__main__":
    main()
