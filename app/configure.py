#!/usr/bin/env python3
import os
import shutil
from jinja2 import Environment, FileSystemLoader


def setup_dirs(conf):
    print('Setting up html directory:', conf['html_root'])
    os.makedirs(conf['html_root'], exist_ok=True)
    if not os.listdir(conf['html_root']):
        print('Copying default site to:', conf['html_root'])
        shutil.copytree('html', conf['html_root'], dirs_exist_ok=True)


def render_template(conf):
    print('Rendering nginx template...')
    env = Environment(loader=FileSystemLoader('.'))
    template = env.get_template('nginx.jinja2')
    output = template.render({'conf': conf})
    print(output)
    with open('/etc/nginx/nginx.conf', 'w+') as f:
        f.write(output)


def get_conf():
    return {
        'html_root': os.getenv('HTML_ROOT', '/data'),
        'html_index': os.getenv('HTML_INDEX', 'index.html index.php'),
        'ssl_crt': os.getenv('SSL_CRT', '/ssl/ssl.crt'),
        'ssl_key': os.getenv('SSL_KEY', '/ssl/ssl.key'),
    }


if __name__ == '__main__':
    print('Initializing configuration...')
    render_template(get_conf())
    setup_dirs(get_conf())
    print('Done configuration site.')
