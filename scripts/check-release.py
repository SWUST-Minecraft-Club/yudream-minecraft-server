"""Validate version, changelog, tag and release inputs in a standalone repository."""
import argparse
import json
from pathlib import Path
import re
import hashlib

ROOT=Path(__file__).resolve().parent.parent
SEMVER=re.compile(r'(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)(?:-(?:alpha|beta|rc)\.[1-9][0-9]*)?')


def check(tag=None):
    version=re.search(r'(?m)^version=(.+)$',(ROOT/'gradle.properties').read_text()).group(1).strip()
    if not SEMVER.fullmatch(version):raise ValueError('version must be SemVer, e.g. 1.2.0-beta.1')
    if tag is not None and tag!='v'+version:raise ValueError('tag must equal v'+version)
    if f'## [{version}]' not in (ROOT/'CHANGELOG.md').read_text():raise ValueError('Missing current CHANGELOG entry')
    for dep in json.loads((ROOT/'dependencies.lock.json').read_text()).get('dependencies',[]):
        path=ROOT/dep['path']
        if hashlib.sha256(path.read_bytes()).hexdigest()!=dep['sha256']:raise ValueError('Dependency checksum mismatch: '+dep['path'])
    print(version)
    return version


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--tag');args=parser.parse_args();check(args.tag)
