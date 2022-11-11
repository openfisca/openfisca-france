import argparse
import requests
import logging


logging.basicConfig(level=logging.INFO)


def get_info(package_name: str = '') -> dict:
    '''
    Get minimal informations needed by .conda/meta.yaml from PyPi JSON API.
    ::package_name:: Name of package to get infos from.
    ::return:: A dict with last_version, url and sha256
    '''
    if package_name == '':
        raise ValueError('Package name not provided.')
    resp = requests.get(f'https://pypi.org/pypi/{package_name}/json').json()
    version = resp['info']['version']
    for v in resp['releases'][version]:
        if v['packagetype'] == 'sdist':  # for .tag.gz
            return {
                'last_version': version,
                'url': v['url'],
                'sha256': v['digests']['sha256']
                }


def replace_in_file(filepath: str, info: dict):
    '''
    ::filepath:: Path to meta.yaml, with filename
    ::info:: Dict with information to populate
    '''
    with open(filepath, 'rt') as fin:
        meta = fin.read()
    # Replace with info from PyPi
    meta = meta.replace('PYPI_VERSION', info['last_version'])
    meta = meta.replace('PYPI_URL', info['url'])
    meta = meta.replace('PYPI_SHA256', info['sha256'])
    with open(filepath, 'wt') as fout:
        fout.write(meta)
    logging.info(f'File {filepath} has been updated with informations from PyPi.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--package', type=str, default='', required=True, help='The name of the package')
    parser.add_argument('-f', '--filename', type=str, default='.conda/meta.yaml', help='Path to meta.yaml, with filename')
    args = parser.parse_args()
    info = get_info(args.package)
    logging.info(f'Information of the last published PyPi package : {info}')
    replace_in_file(args.filename, info)
