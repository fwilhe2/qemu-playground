#!/usr/bin/env python3

# SPDX-FileCopyrightText: Florian Wilhelm
# SPDX-License-Identifier: Apache-2.0

from urllib.request import urlopen
import json

fedora_version = '40'
url = 'https://gitlab.com/fedora/websites-apps/fedora-websites/fedora-websites-3.0/-/raw/develop/public/releases.json'

template = """images:
- location: "URL_x86_64"
  arch: "x86_64"
  digest: "sha256:SHA_x86_64"
- location: "URL_aarch64"
  arch: "aarch64"
  digest: "sha256:SHA_aarch64"
"""


def download_latest_fedora_versions():
    with urlopen(url) as response:
        versions = json.loads(response.read().decode())
        return versions

def filter_versions(versions, current_fedora_version, arch):
    return [x for x in versions if x['version'] == current_fedora_version and x['arch'] == arch and x['variant'] == 'Cloud' and x['subvariant'] == 'Cloud_Base' and x['link'].endswith('qcow2') ]

def geturl(versions, current_fedora_version, arch):
    recent_versions = filter_versions(versions, current_fedora_version, arch)
    assert len(recent_versions) == 1
    return recent_versions[0]['link']

def getsha(versions, current_fedora_version, arch):
    recent_versions = filter_versions(versions, current_fedora_version, arch)
    assert len(recent_versions) == 1
    return recent_versions[0]['sha256']

if __name__ == "__main__":
    latest_fedora_versions = download_latest_fedora_versions()

    manifest = template\
        .replace("URL_x86_64", geturl(latest_fedora_versions, fedora_version, 'x86_64')) \
        .replace("SHA_x86_64", getsha(latest_fedora_versions, fedora_version, 'x86_64')) \
        .replace("URL_aarch64", geturl(latest_fedora_versions, fedora_version, 'aarch64')) \
        .replace("SHA_aarch64", getsha(latest_fedora_versions, fedora_version, 'aarch64'))

    with open('fedora.yaml', 'w+') as file:
        file.write(manifest)