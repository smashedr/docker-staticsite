#!/usr/bin/env python3
import os
import shutil
from jinja2 import Environment, FileSystemLoader


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


def setup_dirs(site, default=False):
    print('Setting up directory for site:', site)
    data_dir = os.environ.get('SFTP_HOME').rstrip('/')
    dest = '{}/html/{}'.format(data_dir, site)
    if not os.path.isdir(dest):
        print('Creating directory:', dest)
        if default:
            print('Copying default site to:', dest)
            shutil.copytree('html/default', dest)
        os.makedirs(dest, exist_ok=True)


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


if __name__ == '__main__':
    print('Initializing pyconf...')
    sites = get_sites()
    for idx, site in enumerate(sites):
        if idx == 0:
            render_template(site, default=True)
            setup_dirs(site, default=True)
        else:
            render_template(site)
            setup_dirs(site)
    print('Done rendering templates.')
