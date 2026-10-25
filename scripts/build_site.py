#!/usr/bin/env python3
"""Build a lightweight, portable reading site from the single book manifest."""
import argparse,html,json,re,shutil
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
import markdown

ROOT=Path(__file__).resolve().parents[1]
REPO='https://github.com/YZYExp/Learn-Music'
GROUPS=[('foundation','声音与原理',1,4),('strings','弦上的世界',5,8),('winds','气息与管道',9,12),('percussion-keys','打击、键盘与电子',13,16),('practice','合奏与入门实践',17,22)]
AUDIO=[('01-harmonics.wav','同一音高，三种组成','220 Hz不变，比较1、4、10个谐波。'),('02-envelope.wav','声音的时间轮廓','相同频率组成，比较衰减与持续包络。'),('03-beating.wav','两个近音的相遇','先听220＋222 Hz，再听220＋220.5 Hz。'),('04-grouping.wav','重音改变了什么','等间隔的十二声，比较每2声与每3声一重音。')]

def esc(s):return html.escape(str(s),quote=True)
def group(ch):return next((key for key,_,lo,hi in GROUPS if lo<=int(ch.get('id','0'))<=hi),'appendix')
def plain(s):
    s=re.sub(r'!\[[^\]]*\]\([^)]*\)','',s)
    s=re.sub(r'\[([^\]]+)\]\([^)]*\)',r'\1',s)
    return re.sub(r'\s+',' ',re.sub(r'[#*`_<>]','',s)).strip()

def page(title,content,base,*,slug='',article_title=''):
    return f'''<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="theme-color" content="#faf7ef"><title>{esc(title)} · 听见乐器</title><meta name="description" content="中文乐器图解读本：从发声原理到世界乐器、听辨与入门实践。22章，图解与试听配套。"><link rel="icon" href="{base}assets/favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="{base}assets/style.css"><script defer src="{base}assets/app.js"></script></head>
<body data-base="{base}" data-slug="{esc(slug)}" data-title="{esc(article_title)}"><a class="skip" href="#main">跳到正文</a>{'<div class="reader-progress" aria-hidden="true"></div>' if slug else ''}
<header class="site-header"><a class="brand" href="{base}">听见乐器<span>HEARING INSTRUMENTS</span></a><nav class="top-nav" aria-label="主导航"><a href="{base}#chapters">章节</a><a href="{base}#listen">试听</a><a href="{base}#download">下载</a><a class="repo-link" href="{REPO}">GitHub ↗</a></nav></header>
{content}<footer class="site-footer">《听见乐器》 · 中文图解兴趣读本 · 第一版 2026.10<a href="{REPO}">书稿与来源</a><a href="{base}read/listening-guide/">试听说明</a></footer></body></html>'''

def audio_cards(base,selection=None):
    return '<div class="audio-grid">'+''.join(f'<section class="audio-card"><h3>{esc(title)}</h3><p>{esc(description)}</p><audio controls preload="none" aria-label="{esc(title)}"><source src="{base}assets/audio/{filename}" type="audio/wav">此浏览器不支持音频播放。<a href="{base}assets/audio/{filename}">下载音频</a></audio></section>' for filename,title,description in AUDIO if selection is None or filename[:2] in selection)+'</div>'

def nav(items,current,base):
    out=['<aside class="book-nav" aria-label="全书目录"><details open><summary>全书目录 · 22章</summary>']
    previous=None
    for c in items:
        g=group(c) if c['id'].isdigit() else 'appendix'
        if g!=previous:
            label=next((name for key,name,_,_ in GROUPS if key==g),'导读与附录')
            out.append(f'<p class="group-label">{label}</p>');previous=g
        label=(c['id']+' ' if c['id'].isdigit() else '')+c['title']
        out.append(f'<a href="{base}read/{c["slug"]}/"'+(' aria-current="page"' if c['slug']==current else '')+f'>{esc(label)}</a>')
    return ''.join(out)+'</details></aside>'

def check_site(out,base):
    class Links(HTMLParser):
        def __init__(self):super().__init__();self.links=[]
        def handle_starttag(self,tag,attrs):
            for k,v in attrs:
                if k in ('href','src') and v:self.links.append(v)
    count=0
    for f in out.rglob('*.html'):
        p=Links();p.feed(f.read_text())
        for link in p.links:
            url=urlsplit(link)
            if url.scheme or url.netloc or not url.path:continue
            path=unquote(url.path)
            if path.startswith('/'):
                assert path.startswith(base),(f,link)
                target=out/path[len(base):]
            else:target=f.parent/path
            if target.is_dir():target/='index.html'
            assert target.is_file(),(f,link,target)
        count+=1
    print(f'Checked {count} HTML pages; all local image, audio, download and navigation targets exist.')

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--base-path',default='/');ap.add_argument('--output',default='build/site');args=ap.parse_args()
    base='/'+args.base_path.strip('/')+'/' if args.base_path.strip('/') else '/'
    out=(ROOT/args.output).resolve();build=(ROOT/'build').resolve()
    assert out.is_relative_to(build) and out!=build,'Output must be a subdirectory of build/'
    if out.exists():shutil.rmtree(out)
    out.mkdir(parents=True)
    book=json.loads((ROOT/'book.json').read_text());chapters=book['chapters']
    for name in ['images','audio']:shutil.copytree(ROOT/'assets'/name,out/'assets'/name)
    for name in ['style.css','app.js']:shutil.copy2(ROOT/'site'/name,out/'assets'/name)
    (out/'assets/favicon.svg').write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="14" fill="#177e78"/><path d="M23 43V17l25-5v25M23 22l25-5" fill="none" stroke="#faf7ef" stroke-width="5"/><ellipse cx="17" cy="44" rx="8" ry="6" fill="#faf7ef"/><ellipse cx="42" cy="38" rx="8" ry="6" fill="#faf7ef"/></svg>')
    download=ROOT/'downloads/Hearing-Instruments.epub';assert download.is_file()
    (out/'downloads').mkdir();shutil.copy2(download,out/'downloads'/download.name)
    search=[];cards=[]
    for c in chapters:
        s=(ROOT/c['path']).read_text();text=plain(s)
        first=next((p for p in s.split('\n\n') if not p.startswith(('#','!','<','*')) and p.strip()),'')
        description=plain(first)[:72]+'…'
        g=group(c);label=next(name for key,name,_,_ in GROUPS if key==g)
        cards.append(f'<a class="chapter-card" href="{base}read/{c["slug"]}/" data-group="{g}"><span class="chapter-num">{c["id"]}</span><div><small>{label}</small><h3>{esc(c["title"])}</h3><p>{esc(description)}</p></div></a>')
        search.append({**{k:c[k] for k in ['id','title','slug']},'group':g,'text':text})
    (out/'search.json').write_text(json.dumps(search,ensure_ascii=False))
    filters='<button class="filter" data-group="all" aria-pressed="true">全部章节</button>'+''.join(f'<button class="filter" data-group="{key}" aria-pressed="false">{name}</button>' for key,name,_,_ in GROUPS)
    home=f'''<main id="main" class="wrap">
<section class="hero"><div class="hero-copy"><div class="eyebrow">一本关于声音、器物与人的书</div><h1>听见乐器，<br>也听懂<em>声音的来处。</em></h1><p>一根弦、一束气流、一张鼓膜。沿着声音的产生与变化，认识中西及世界各地的乐器，走近它们的结构、历史与演奏。</p><div class="actions"><a class="button primary" href="{base}read/listening/">从第一声开始 →</a><a class="button" href="#chapters">浏览全书目录</a></div><a id="resume" class="resume" hidden></a><div class="hero-stats"><span><strong>22</strong>章节</span><span><strong>22</strong>章内图解</span><span><strong>4</strong>试听实验</span></div></div><figure><img src="{base}assets/images/opening.png" width="1024" height="1536" alt="暖色音乐室内的大提琴、吉他、钢琴与手鼓" fetchpriority="high"><figcaption>AI生成的现代情境插画；结构教学以章内图解为准。</figcaption></figure></section>
<section class="section"><div class="section-heading"><div><div class="eyebrow">选择你的阅读方式</div><h2>从兴趣进入，沿着声音探索。</h2></div><p>无需先买乐器，也无需先读懂全部乐谱。可以顺序阅读，也可以从一件熟悉的乐器开始。</p></div><div class="route-grid"><div class="route"><h3>我想听得更明白</h3><p>先观察起音、延续与收尾，再用听辨实验区分音高、音色与节奏。</p><a href="{base}read/ear/">进入听辨实验室 →</a></div><div class="route"><h3>我想认识不同乐器</h3><p>比较弦、气流、膜与器体的振动，也看它们怎样进入各地的音乐生活。</p><a href="{base}read/maps-history/">打开分类地图 →</a></div><div class="route"><h3>我想亲手试一试</h3><p>从桌面节奏、键盘三音与竖笛短句开始，做出能重复、能听见的小变化。</p><a href="{base}read/first-play/">试一次简单演奏 →</a></div></div></section>
<section class="section" id="chapters"><div class="section-heading"><div><div class="eyebrow">全书目录</div><h2>从发声原理，到音乐现场。</h2></div><p>同一套分章书稿，在线阅读与电子书相互配套。</p></div><label class="search-box"><span class="note">搜索全书正文，例如“二胡”“泛音”“MIDI”</span><input id="chapter-search" type="search" placeholder="输入乐器名或你想了解的问题" autocomplete="off"></label><div class="directory-tools" aria-label="按主题筛选">{filters}</div><p class="search-status" id="search-status" role="status" aria-live="polite"></p><div id="search-results" class="search-results"></div><div class="chapter-grid">{''.join(cards)}</div><p class="note"><a href="{base}read/introduction/">导读</a> · <a href="{base}read/glossary/">术语与阅读路线</a> · <a href="{base}read/listening-guide/">试听与资料入口</a></p></section>
<section class="section" id="listen"><div class="section-heading"><div><div class="eyebrow">先听，再比较</div><h2>四个可以反复听的小实验。</h2></div><p>这些是控制变量的合成模型，不是真实乐器录音。先调到舒适音量，再比较声音的变化。</p></div>{audio_cards(base)}<p class="note">真实演奏与实物的机构资料，见各章就近引用及<a href="{base}read/listening-guide/">试听附录</a>。</p></section>
<section class="section" id="download"><div class="download-panel"><div><div class="eyebrow" style="color:#b6d5c6">离线阅读</div><h2>把整本书带走。</h2><p>EPUB · 第一版 · {download.stat().st_size/1024/1024:.1f} MB · 含图解与合成试听资源</p></div><a class="button" download href="{base}downloads/Hearing-Instruments.epub">下载电子书 ↓</a></div><p class="note">音频播放取决于阅读器支持，也可在本页试听。<a href="{REPO}">在 GitHub 查看分章稿、图源与构建方法 ↗</a></p></section></main>'''
    (out/'index.html').write_text(page('从一声开始',home,base))
    items=[{'id':'intro','title':'导读','path':book['frontmatter'],'slug':'introduction'}]+chapters+book['appendices']
    for i,c in enumerate(items):
        s=(ROOT/c['path']).read_text();s=re.sub(r'^# [^\n]+\n','',s,count=1)
        s=s.replace('../assets/','assets/')
        s=re.sub(r'(?<![\w/])assets/',base+'assets/',s)
        md=markdown.Markdown(extensions=['tables','fenced_code','toc'],extension_configs={'toc':{'toc_depth':'2-3','permalink':False}})
        content=md.convert(s)
        content=re.sub(r'<img\s', '<img loading="lazy" decoding="async" ',content)
        content=re.sub(r'(<table>.*?</table>)',r'<div class="table-scroll">\1</div>',content,flags=re.S)
        toc=f'<details class="chapter-toc"><summary>本章内容</summary>{md.toc}</details>' if md.toc_tokens else ''
        extras=''
        if c['id'] in ('02','18','19'):
            selection=['01','02'] if c['id']=='02' else ['03','04'] if c['id']=='18' else None
            extras='<section class="section"><h2>配套听觉实验</h2><p class="note">原创合成对照音，非真实乐器采样。</p>'+audio_cards(base,selection)+'</section>'
        links=[]
        for j,label in [(i-1,'上一章'),(i+1,'下一章')]:
            if 0<=j<len(items):
                other=items[j];links.append(f'<a href="{base}read/{other["slug"]}/"><small>{label}</small>{esc(other["title"])}</a>')
            else:links.append(f'<a href="{base}#chapters"><small>全书</small>返回目录</a>')
        count=f'第 {int(c["id"]):02} / 22 章' if c['id'].isdigit() else '导读与附录'
        reading=f'''<main id="main" class="reader-layout">{nav(items,c['slug'],base)}<article><header class="article-head"><div class="article-meta">听见乐器 / {count}</div><h1>{esc(c['title'])}</h1><a href="{REPO}/blob/main/{c['path']}">查看本章书稿与引用 ↗</a></header>{toc}<div class="reading-body">{content}</div>{extras}<nav class="next-prev" aria-label="前后章">{''.join(links)}</nav></article></main>'''
        target=out/'read'/c['slug']/'index.html';target.parent.mkdir(parents=True);target.write_text(page(c['title'],reading,base,slug=c['slug'],article_title=c['title']))
    (out/'.nojekyll').touch()
    check_site(out,base)
    print(f'Built homepage, {len(items)} reading pages, full-text index and 4 audio experiments at {out}')

if __name__=='__main__':main()
