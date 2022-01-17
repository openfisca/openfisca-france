import requests


def get_info(package_name: str = "") -> dict:
    """
    Get minimal informations needed by .conda/meta.yaml from PyPi JSON API.
    ::package_name:: Name of package to get infos from.
    ::return:: A dict with last_version, url and sha256
    """
    resp = requests.get(f"https://pypi.org/pypi/{package_name}/json").json()
    version = resp["info"]["version"]
    # print(resp["releases"][version][0])
    for v in resp["releases"][version]:
        if v["packagetype"] == "sdist":
            return {
                "last_version": version,
                "url": v["url"],
                "sha256": v["digests"]["sha256"]
                }


def replace_in_file(filepath: str, info: dict):
    '''
    ::filepath:: Chemin vers le fichier meta.yaml, contenant le nom de fichier
    ::info:: Dictionnaire contenant les informations à renseigner
    '''
    with open(filepath, "rt") as fin:
        meta = fin.read()
    # Replace with info from PyPi
    meta = meta.replace("PYPI_VERSION", info["last_version"])
    meta = meta.replace("PYPI_URL", info["url"])
    meta = meta.replace("PYPI_SHA256", info["sha256"])
    with open(filepath, "wt") as fout:
        fout.write(meta)
    print(f"File {filepath} writen.")  # noqa: T001


info = get_info("OpenFisca-France")
print("Information sur le dernier package PyPi:", info)  # noqa: T001
replace_in_file(".conda/meta.yaml", info)
