from pathlib import Path
import re

root = Path(__file__).resolve().parents[1]
package_dir = root / 'docs/packages'
existing = {re.sub(r'^\d{3}-', '', p.stem) for p in package_dir.glob('*.md')}
aliases = {'pymodbus': 'modbus-pymodbus', 'python-dateutil': 'dateutil'}
rows = []
hub = next(package_dir.glob('[0-9][0-9][0-9]-index.md'))
for line in hub.read_text(encoding='utf-8').splitlines():
    m = re.match(r'\| ([^|]+) \| `([^`]+)` \|', line)
    if m:
        label, package = m.groups()
        slug = aliases.get(package, package.lower().replace('_', '-'))
        rows.append((label.strip(), package, slug))
for label, package, slug in rows:
    if slug not in existing:
        print(f'{label}\t{package}\t{slug}')
print(f'missing={sum(slug not in existing for _,_,slug in rows)} total={len(rows)}', file=__import__('sys').stderr)
