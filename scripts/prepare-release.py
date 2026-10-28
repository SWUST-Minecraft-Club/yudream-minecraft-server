"""Stage only current-version build outputs, source archive and SHA-256 sums."""
import gzip
import hashlib
from pathlib import Path
import re
import shutil
import subprocess
from importlib.util import spec_from_file_location,module_from_spec

ROOT=Path(__file__).resolve().parent.parent
spec=spec_from_file_location('check_release',ROOT/'scripts/check-release.py')
checker=module_from_spec(spec);spec.loader.exec_module(checker)
version=checker.check()
output=ROOT/'build/publish'
if output.exists():shutil.rmtree(output)
output.mkdir(parents=True)
pattern=re.compile(r'-'+re.escape(version)+r'(?:-(?:api|sources|install))?\.(?:jar|zip)$')
for base in [ROOT/'release',ROOT/'build/libs',ROOT/'server/build/libs']:
    if base.exists():
        for path in base.rglob('*'):
            if path.is_file() and pattern.search(path.name):shutil.copyfile(path,output/path.name)
if not list(output.glob('*.jar')):raise RuntimeError('No current-version JAR was built')
archive=subprocess.check_output(['git','archive','--format=tar','--prefix=source/','HEAD'],cwd=ROOT)
(output/f'Source-{version}.tar.gz').write_bytes(gzip.compress(archive,mtime=0))
files=sorted(output.iterdir())
(output/'SHA256SUMS.txt').write_text(''.join(hashlib.sha256(path.read_bytes()).hexdigest()+'  '+path.name+'\n' for path in files))
print('\n'.join(path.name for path in files))
