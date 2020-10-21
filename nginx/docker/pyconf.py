#!/usr/bin/env python3
import os
import subprocess
from jinja2 import Environment, FileSystemLoader


def run_command(command, raise_exception=True):
    try:
        command = command.split() if isinstance(command, str) else command
        return subprocess.run(
            command, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
    except Exception as error:
        if raise_exception:
            raise error
        return error


def do_rsync(src, dest):
    print('Syncing static for:', src)
    cmd = ['rsync', '-avPh', src, dest]
    r = run_command(cmd)
    print(r)


def get_sites():
    envs = []
    for key in os.environ:
        envs.append(key)
    envs.sort()
    sites = []
    for key in envs:
        if key.startswith('WWW_'):
            sites.append(os.getenv(key))
    return sites


def render_template(site, default=False):
    vhost = site.split()[0]
    if os.environ.get('ENVIRONMENT', 'prod') != 'prod':
        vhost = os.environ.get('DEV_PREFIX', 'dev.') + vhost

    print('Rendering template for site:', site)
    file_loader = FileSystemLoader('.')
    env = Environment(loader=file_loader)
    template = env.get_template('site.jinja2')
    data = {
        'default': 'default_server' if default else '',
        'name': site,
        'vhost': vhost,
    }
    output = template.render({'site': data})
    print(output)
    with open('/etc/nginx/conf.d/%s.conf' % site, 'w+') as f:
        f.write(output)


def copy_static(site, default=False):
    site = site.split()[0]
    source = 'html/%s/' % site
    if os.path.isdir(source):
        do_rsync(source, '/data/html/%s' % site)
    elif default:
        do_rsync('html/default/', '/data/html/%s' % site)
    else:
        try:
            os.mkdir('/data/html/%s/' % site)
        except FileExistsError:
            pass


if __name__ == '__main__':
    print('Initializing pyconf...')
    sites = get_sites()
    for idx, site in enumerate(sites):
        if idx == 0:
            render_template(site, default=True)
            copy_static(site, default=True)
        else:
            render_template(site)
            copy_static(site)
    print('Done rendering templates.')
