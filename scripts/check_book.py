from pathlib import Path
import json,re,xml.etree.ElementTree as E,struct,zlib
ROOT=Path(__file__).resolve().parents[1]

def main():
    book=json.loads((ROOT/'book.json').read_text());figures=0;sources=set();chars=0
    docs=[{'path':book['frontmatter']}]+book['chapters']+book['appendices']
    for c in docs:
        p=ROOT/c['path'];s=p.read_text();assert s.startswith('# '),p
        for target in re.findall(r'(?:!?)\[[^\]]*\]\(([^)]+)\)',s):
            if target.startswith('http'):sources.add(target)
            elif not target.startswith('#'):assert (p.parent/target.split('#')[0]).is_file(),(p,target)
        if c in book['chapters']:
            assert '![' in s and 'https://' in s,p
            figures+=len(re.findall(r'!\[',s));chars+=len(re.findall(r'[\u3400-\u9fff]',s))
    for p in (ROOT/'assets/images').glob('*.svg'):E.parse(p)
    print(f'Validated {len(book["chapters"])} chapters, {figures} chapter figures, {chars} Chinese characters and {len(sources)} source URLs.')

if __name__=='__main__':main()
