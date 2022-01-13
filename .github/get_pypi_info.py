import requests


def get_info(package_name: str = '') -> dict:
    '''
    Get minimal informations needed by .conda/meta.yaml from PyPi JSON API.
    ::package_name:: Name of package to get infos from.
    ::return:: A dict with last_version, url and sha256
    '''
    resp = requests.get(f'https://pypi.org/pypi/{package_name}/json').json()
    version = resp['info']['version']
    # print(resp['releases'][version][0])
    for v in resp['releases'][version]:
        if v["packagetype"] == "sdist":
            return {
                "last_version": version,
                "url": v['url'],
                "sha256": v['digests']['sha256']
                }


info = get_info('OpenFisca-France')
print(info)  # noqa: T001
