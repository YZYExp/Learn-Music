"""EPUB export uses checked-in raster images; independent of website dependencies."""
from pathlib import Path
import json,re,subprocess,zipfile,posixpath,xml.etree.ElementTree as E
ROOT=Path(__file__).resolve().parents[1]

def main():
    subprocess.run(['python3',str(ROOT/'scripts/check_book.py')],check=True)
    b=json.loads((ROOT/'book.json').read_text());build=ROOT/'build';build.mkdir(exist_ok=True)
    paths=[b['frontmatter']]+[c['path'] for c in b['chapters']+b['appendices']]
    (build/'reader.md').write_text('\n\n'.join((ROOT/p).read_text().replace('../assets/','assets/') for p in paths))
    css=build/'reader.css';css.write_text('body{line-height:1.7}h1{break-before:page;line-height:1.4}img{max-width:100%;height:auto}table{font-size:.85em;width:100%}td,th{padding:.4em}a{color:#177e78}')
    out=build/'Hearing-Instruments.epub'
    subprocess.run(['pandoc',str(build/'reader.md'),'-f','gfm','-t','epub3','--toc','--toc-depth=1','--resource-path='+str(ROOT),'--css='+str(css),'--metadata=title:'+b['title'],'--metadata=subtitle:'+b['subtitle'],'--metadata=lang:zh-CN','--epub-cover-image='+str(ROOT/b['cover']),'-o',str(out)],cwd=ROOT,check=True)
    with zipfile.ZipFile(out) as z:parts={n:z.read(n) for n in z.namelist()}
    opf=next(n for n in parts if n.endswith('.opf'));base=posixpath.dirname(opf);items=[]
    for p in sorted((ROOT/'assets/audio').glob('*.wav')):
        dest=posixpath.join(base,'media',p.name);parts[dest]=p.read_bytes();items.append(f'<item id="audio-{p.stem}" href="media/{p.name}" media-type="audio/wav"/>')
        for n in list(parts):
            if n.endswith('.xhtml'):
                target=posixpath.relpath(dest,posixpath.dirname(n));s=parts[n].decode()
                s=re.sub(r'href="(?:\.\./)*assets/audio/'+re.escape(p.name)+r'"','href="'+target+'"',s);parts[n]=s.encode()
    parts[opf]=parts[opf].decode().replace('</manifest>',''.join(items)+'</manifest>').encode()
    with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED) as z:
        z.writestr('mimetype',parts.pop('mimetype'),compress_type=zipfile.ZIP_STORED)
        for n,data in parts.items():z.writestr(n,data)
    with zipfile.ZipFile(out) as z:
        assert z.testzip() is None
        files=set(z.namelist());image_refs=set();audio_refs=set()
        for n in files:
            if n.endswith(('.opf','.xhtml','.xml')):E.fromstring(z.read(n))
            if n.endswith('.xhtml'):
                for target in re.findall(r'(?:src|href)="([^"]+)"',z.read(n).decode()):
                    if re.match(r'^[a-zA-Z]+:',target) or target.startswith('#'):continue
                    path=target.split('#')[0]
                    if not path:continue
                    resolved=posixpath.normpath(posixpath.join(posixpath.dirname(n),path));assert resolved in files,(n,target)
                    if resolved.endswith(('.png','.jpg')):image_refs.add(resolved)
                    if resolved.endswith('.wav'):audio_refs.add(resolved)
        assert len(image_refs)>=23,len(image_refs)
        assert len(audio_refs)==4,len(audio_refs)
    print('EPUB validated:',out)

if __name__=='__main__':main()
