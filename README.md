# 听见乐器

从发声原理到世界乐器、听辨与入门实践。面向非专业兴趣读者的中文图解知识书。

**[在线阅读](https://YZYExp.github.io/Learn-Music/) · [下载第一版EPUB](downloads/Hearing-Instruments.epub) · [网站发布状态](https://github.com/YZYExp/Learn-Music/actions/workflows/pages.yml)**

第一版：2026-10-25。22章、约3.4万中文字、22幅章内图解、4段原创合成试听。历史、实物和真实演奏在正文就近给出来源；合成模型与真实录音分别标明。

## 阅读主线

| 部分 | 章节 | 内容 |
|---|---|---|
| 声音与原理 | 01—04 | 观察方法、振动、音色、分类与弦的共同原理 |
| 弦上的世界 | 05—08 | 拉弦、吉他与贝斯、中国弦乐、世界弦乐 |
| 气息与管道 | 09—12 | 边棱发声、单／双簧、铜管、自由簧 |
| 打击、键盘与电子 | 13—16 | 鼓、体鸣、钢琴与历史键盘、管风琴与电子声源 |
| 合奏与实践 | 17—22 | 乐队关系、记谱与调律、听辨、首次演奏、练习与录音 |

[导读](frontmatter.md) · [术语与阅读路线](appendices/glossary.md) · [试听说明](appendices/listening.md) · [资料索引](references/sources.md)

## 本地构建网站

网页只需Python 3与一个Markdown依赖，不依赖Pandoc、Inkscape、中文字库或EPUB导出。

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r site/requirements.txt
.venv/bin/python scripts/check_book.py
.venv/bin/python scripts/build_site.py --base-path /Learn-Music/
```

输出`build/site/`，含独立主页、25份导读／章节／附录阅读页、全文搜索索引、音频与已验证的第一版EPUB下载。标题、排序、路径统一来自`book.json`；正文不复制为第二套网站稿。

本地根路径预览可改用`--base-path /`，然后运行：

```bash
python3 -m http.server 8000 --directory build/site
```

## GitHub Pages CI

`.github/workflows/pages.yml`在main更新时构建并部署，PR只构建检查。网页与电子书导出使用独立工作流与并发组。构建会检查导航、资源、图片、音频、下载与子路径链接。

首次启用：仓库 **Settings → Pages → Build and deployment → Source → GitHub Actions**。完成设置后，在Actions重新运行`Publish homepage and reading site`。普通工作流令牌不负责首次开启仓库Pages设置。

## 单独导出EPUB

需Python 3与Pandoc，直接使用已核验的PNG，无需重新渲染SVG。

```bash
python3 scripts/build_book.py
```

输出`build/Hearing-Instruments.epub`，校验XML、图片引用、音频链接与资源完整性。`.github/workflows/export.yml`在书稿／资源变动或手动运行时独立导出；Actions artifact名称为`Hearing-Instruments-EPUB`，保留90天，下载通常需GitHub登录。网站直接下载的第一版EPUB是已验证快照，不冒充未来改稿的实时导出。

## 工程

- `chapters/`：分章Markdown；`appendices/`：附录。
- `assets/images/`：22幅SVG与阅读PNG，另有AI情境插画。
- `assets/audio/`：4段合成WAV，演示谐波、包络、拍频与重音分组。
- `site/`与`scripts/build_site.py`：样式、交互与静态构建。
- `editorial/`：内部编辑记录，不进入阅读站。

本书覆盖代表案例，不代替全球所有地方传统、考级教材、维修手册或器种教师指导。机构页面与录音权利归原持有人，未打包转载。图解的教学简化边界在图注说明。
