"""Build a single-page HTML ebook from chapter Markdown files."""
import os, re, base64, markdown
from pathlib import Path

ROOT = Path(__file__).parent
IMG_DIR = ROOT / "images"

CHAPTERS_ZH = [
    ("ch00", "ch00-preface-zh.md", "前言"),
    ("ch01", "ch01-oldest-conversation-zh.md", "第一章 · 最古老的健康对话"),
    ("ch02", "ch02-living-in-rhythm-zh.md", "第二章 · 顺时而活"),
    ("ch03", "ch03-food-as-medicine-zh.md", "第三章 · 食养之道"),
    ("ch04", "ch04-emotional-body-zh.md", "第四章 · 情志与身体"),
    ("ch05", "ch05-moving-like-water-zh.md", "第五章 · 动如流水"),
    ("ch06", "ch06-art-of-prevention-zh.md", "第六章 · 治未病"),
    ("ch07", "ch07-yin-yang-balance-zh.md", "第七章 · 阴阳之道"),
    ("ch08", "ch08-sleep-healer-zh.md", "第八章 · 睡眠大药"),
    ("ch09", "ch09-90-day-reset-zh.md", "第九章 · 九十天养生计划"),
    ("ch10", "ch10-invisible-network-zh.md", "第十章 · 看不见的网络"),
    ("ch11", "ch11-breath-and-posture-zh.md", "第十一章 · 呼吸与姿态"),
    ("ch12", "ch12-ai-meets-tcm-zh.md", "第十二章 · 当AI遇上中医"),
]

CHAPTERS_EN = [
    ("ch00", "ch00-preface-en.md", "Preface"),
    ("ch01", "ch01-oldest-conversation-en.md", "Ch 1 · The Oldest Health Conversation"),
    ("ch02", "ch02-living-in-rhythm-en.md", "Ch 2 · Living in Rhythm"),
    ("ch03", "ch03-food-as-medicine-en.md", "Ch 3 · Food as Medicine"),
    ("ch04", "ch04-emotional-body-en.md", "Ch 4 · The Emotional Body"),
    ("ch05", "ch05-moving-like-water-en.md", "Ch 5 · Moving Like Water"),
    ("ch06", "ch06-art-of-prevention-en.md", "Ch 6 · The Art of Prevention"),
    ("ch07", "ch07-yin-yang-balance-en.md", "Ch 7 · The Yin-Yang Balance"),
    ("ch08", "ch08-sleep-healer-en.md", "Ch 8 · The Sleep Healer"),
    ("ch09", "ch09-90-day-reset-en.md", "Ch 9 · The 90-Day Reset"),
    ("ch10", "ch10-invisible-network-en.md", "Ch 10 · The Invisible Network"),
    ("ch11", "ch11-breath-and-posture-en.md", "Ch 11 · Breath and Posture"),
    ("ch12", "ch12-ai-meets-tcm-en.md", "Ch 12 · When AI Meets TCM"),
]


def svg_to_data_uri(svg_path: Path) -> str:
    if svg_path.exists():
        raw = svg_path.read_bytes()
        b64 = base64.b64encode(raw).decode()
        return f"data:image/svg+xml;base64,{b64}"
    return ""


def convert_md(md_text: str) -> str:
    html = markdown.markdown(
        md_text,
        extensions=["tables", "fenced_code", "toc"],
        output_format="html5",
    )
    html = re.sub(
        r'<blockquote>\s*<p>(.*?)</p>\s*</blockquote>',
        r'<blockquote class="bq"><p>\1</p></blockquote>',
        html, flags=re.DOTALL,
    )

    def replace_img(m):
        alt = m.group(1)
        src = m.group(2)
        if src.startswith("images/") and src.endswith(".svg"):
            svg_path = ROOT / src
            data_uri = svg_to_data_uri(svg_path)
            if data_uri:
                return (
                    f'<figure class="diagram">'
                    f'<div class="svg-wrap"><img src="{data_uri}" alt="{alt}" style="max-width:100%;height:auto"></div>'
                    f'<figcaption>{alt}</figcaption></figure>'
                )
        return m.group(0)

    html = re.sub(r'<img\s+alt="([^"]*?)"\s+src="([^"]*?)"[^>]*/?>', replace_img, html)
    return html


def build_cover_html() -> str:
    cover_path = IMG_DIR / "book-cover-final.png"
    if cover_path.exists():
        b64 = base64.b64encode(cover_path.read_bytes()).decode()
        cover_src = f"data:image/png;base64,{b64}"
    else:
        cover_src = ""
    return f'''<section id="cover" class="chapter active">
<div style="display:flex;flex-direction:column;align-items:center;justify-content:center;min-height:80vh;text-align:center;">
<img src="{cover_src}" alt="Book Cover" style="max-width:420px;width:100%;border-radius:12px;box-shadow:0 8px 32px rgba(0,0,0,.3);margin-bottom:32px;">
<h1 style="font-size:2.2rem;color:var(--accent2);border:none;margin:0 0 8px">养生两千五百年</h1>
<p style="font-size:1.1rem;color:var(--text2);margin:0 0 4px">2,500 Years of Wellness</p>
<p style="font-size:.9rem;color:var(--text2);margin:0 0 24px">黄帝内经的生活智慧 · The Yellow Emperor's Guide to Living Well</p>
<div style="display:flex;gap:12px;margin-top:16px">
<button onclick="switchLang('zh');showChapter('ch00-zh')" style="padding:12px 32px;background:var(--accent);color:#fff;border:none;border-radius:8px;font-size:1rem;cursor:pointer;transition:all .2s">开始阅读 (中文)</button>
<button onclick="switchLang('en');showChapter('ch00-en')" style="padding:12px 32px;background:transparent;color:var(--accent2);border:2px solid var(--accent);border-radius:8px;font-size:1rem;cursor:pointer;transition:all .2s">Read in English</button>
</div>
</div>
</section>'''


def build_chapters_html(chapters, lang):
    sections = []
    for i, (cid, fname, _title) in enumerate(chapters):
        fpath = ROOT / fname
        if not fpath.exists():
            continue
        md_text = fpath.read_text(encoding="utf-8")
        html_body = convert_md(md_text)
        full_id = f"{cid}-{lang}"
        prev_full = f"{chapters[i - 1][0]}-{lang}" if i > 0 else "cover"
        next_full = f"{chapters[i + 1][0]}-{lang}" if i < len(chapters) - 1 else None
        prev_label = chapters[i - 1][2] if i > 0 else ("封面" if lang == "zh" else "Cover")
        next_label = chapters[i + 1][2] if i < len(chapters) - 1 else None

        nav = '<div class="chapter-nav">'
        nav += f'<a href="#" onclick="showChapter(\'{prev_full}\');return false">← {prev_label}</a>'
        if next_full:
            nav += f'<a href="#" onclick="showChapter(\'{next_full}\');return false">{next_label} →</a>'
        else:
            nav += "<span></span>"
        nav += "</div>"

        sections.append(
            f'<section id="{full_id}" class="chapter lang-{lang}">\n'
            f'{html_body}\n{nav}\n</section>'
        )
    return "\n".join(sections)


def build_toc_html(chapters, lang):
    items = []
    for cid, _fname, title in chapters:
        full_id = f"{cid}-{lang}"
        items.append(
            f'<a href="#" class="toc-item toc-{lang}" data-chapter="{full_id}" onclick="showChapter(\'{full_id}\');return false">{title}</a>'
        )
    return "\n".join(items)


def build_full_html():
    cover = build_cover_html()
    zh_html = build_chapters_html(CHAPTERS_ZH, "zh")
    en_html = build_chapters_html(CHAPTERS_EN, "en")
    zh_toc = build_toc_html(CHAPTERS_ZH, "zh")
    en_toc = build_toc_html(CHAPTERS_EN, "en")

    return f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>养生两千五百年 | 2,500 Years of Wellness</title>
<meta name="description" content="基于《黄帝内经》的现代养生指南，中英双语版。A modern wellness guide based on the Huangdi Neijing, bilingual Chinese-English.">
<style>
:root{{
  --bg:#0d1117;--bg2:#161b22;--bg3:#1c2333;
  --text:#e6edf3;--text2:#8b949e;--text-strong:#ffffff;
  --accent:#7c3aed;--accent2:#a78bfa;
  --border:#30363d;--green:#3fb950;--orange:#d29922;--red:#e94560;
  --bq-bg:rgba(124,58,237,.08);--hover-bg:rgba(124,58,237,.06);
  --svg-bg:#ffffff;--shadow:rgba(0,0,0,.3);
}}
[data-theme="light"]{{
  --bg:#f8f6f1;--bg2:#ffffff;--bg3:#eee9df;
  --text:#2c2418;--text2:#6b5f50;--text-strong:#1a1208;
  --accent:#6d28d9;--accent2:#7c3aed;
  --border:#d6cfc3;--green:#16a34a;--orange:#b45309;--red:#dc2626;
  --bq-bg:rgba(109,40,217,.06);--hover-bg:rgba(109,40,217,.05);
  --svg-bg:#ffffff;--shadow:rgba(0,0,0,.08);
}}
*{{margin:0;padding:0;box-sizing:border-box}}
html{{scroll-behavior:smooth}}
body{{font-family:-apple-system,"Noto Sans SC","PingFang SC","Microsoft YaHei",sans-serif;background:var(--bg);color:var(--text);line-height:1.8;display:flex;min-height:100vh;transition:background .3s,color .3s}}

/* Sidebar */
.sidebar{{width:280px;min-width:280px;background:var(--bg2);border-right:1px solid var(--border);position:fixed;top:0;left:0;height:100vh;overflow-y:auto;z-index:100;transition:transform .3s,background .3s,border-color .3s;display:flex;flex-direction:column}}
.sidebar-header{{padding:20px;border-bottom:1px solid var(--border);display:flex;align-items:center;justify-content:space-between}}
.sidebar-header div h1{{font-size:1.15rem;color:var(--accent2);font-weight:700;letter-spacing:1px}}
.sidebar-header div p{{font-size:.75rem;color:var(--text2);margin-top:4px}}
.theme-toggle{{background:var(--bg3);border:1px solid var(--border);border-radius:8px;width:36px;height:36px;display:flex;align-items:center;justify-content:center;cursor:pointer;font-size:1.1rem;transition:all .2s;flex-shrink:0;color:var(--text)}}
.theme-toggle:hover{{border-color:var(--accent);color:var(--accent)}}
.lang-switch{{display:flex;gap:0;margin:12px 20px;border:1px solid var(--border);border-radius:6px;overflow:hidden}}
.lang-btn{{flex:1;padding:6px 0;text-align:center;font-size:.82rem;cursor:pointer;background:transparent;color:var(--text2);border:none;transition:all .2s;font-family:inherit}}
.lang-btn.active{{background:var(--accent);color:#fff}}
.toc-scroll{{flex:1;overflow-y:auto;padding:8px 0}}
.toc-item{{display:block;padding:9px 20px;color:var(--text2);text-decoration:none;font-size:.85rem;border-left:3px solid transparent;transition:all .15s;cursor:pointer}}
.toc-item:hover,.toc-item.active{{background:var(--bg3);color:var(--text);border-left-color:var(--accent);text-decoration:none}}

/* Main content */
.main{{margin-left:280px;flex:1;max-width:860px;padding:40px 48px 120px;transition:margin .3s}}
.chapter{{display:none}}.chapter.active{{display:block}}
h1{{font-size:1.8rem;margin:32px 0 16px;color:var(--accent2);border-bottom:2px solid var(--border);padding-bottom:10px}}
h2{{font-size:1.35rem;margin:28px 0 12px;color:var(--text)}}
h3{{font-size:1.1rem;margin:20px 0 8px;color:var(--accent2)}}
h4{{font-size:1rem;margin:16px 0 6px;color:var(--text);font-weight:600}}
p{{margin:10px 0}}
hr{{border:none;border-top:1px solid var(--border);margin:28px 0}}
strong{{color:var(--text-strong)}}em{{color:var(--accent2);font-style:italic}}
code{{background:var(--bg3);padding:2px 6px;border-radius:4px;font-size:.88em;color:var(--orange)}}
pre{{background:var(--bg3);padding:16px;border-radius:8px;overflow-x:auto;margin:16px 0;border:1px solid var(--border);transition:background .3s}}
pre code{{background:none;padding:0;color:var(--text);font-size:.85rem}}
a{{color:var(--accent2)}}

/* Tables */
.table-wrap{{overflow-x:auto;margin:16px 0}}
table{{width:100%;border-collapse:collapse;font-size:.88rem}}
th{{background:var(--bg3);color:var(--accent2);padding:10px 14px;text-align:left;border-bottom:2px solid var(--accent);font-weight:600}}
td{{padding:9px 14px;border-bottom:1px solid var(--border)}}
tr:hover td{{background:var(--hover-bg)}}

/* Lists */
ul,ol{{margin:10px 0 10px 24px}}li{{margin:4px 0}}li::marker{{color:var(--accent)}}

/* Blockquotes */
blockquote.bq{{border-left:4px solid var(--accent);padding:12px 20px;margin:16px 0;background:var(--bq-bg);border-radius:0 8px 8px 0;font-style:italic}}
blockquote.bq p{{color:var(--text2);margin:4px 0}}
blockquote{{border-left:4px solid var(--border);padding:8px 16px;margin:12px 0;color:var(--text2)}}

/* Diagrams */
.diagram{{margin:24px 0;text-align:center}}
.svg-wrap{{background:var(--svg-bg);border-radius:10px;padding:16px;display:inline-block;max-width:100%;overflow-x:auto;border:1px solid var(--border)}}
.svg-wrap img{{max-width:100%;height:auto}}
.diagram figcaption{{font-size:.82rem;color:var(--text2);margin-top:8px;font-style:italic}}

/* Chapter nav */
.chapter-nav{{display:flex;justify-content:space-between;margin-top:48px;padding-top:20px;border-top:1px solid var(--border)}}
.chapter-nav a{{color:var(--accent2);text-decoration:none;padding:8px 16px;border:1px solid var(--border);border-radius:6px;transition:all .2s;font-size:.88rem}}
.chapter-nav a:hover{{background:var(--bg3);border-color:var(--accent);text-decoration:none}}

/* Controls */
.hamburger{{display:none;position:fixed;top:12px;left:12px;z-index:200;background:var(--bg2);border:1px solid var(--border);color:var(--text);padding:8px 12px;border-radius:6px;font-size:1.2rem;cursor:pointer;transition:background .3s,border-color .3s}}
.progress-bar{{position:fixed;top:0;left:0;height:3px;background:linear-gradient(90deg,var(--accent),var(--accent2));z-index:300;transition:width .3s}}
.back-top{{position:fixed;bottom:24px;right:24px;width:44px;height:44px;background:var(--bg2);border:1px solid var(--border);border-radius:50%;color:var(--accent2);font-size:1.2rem;cursor:pointer;display:none;align-items:center;justify-content:center;z-index:200;transition:all .2s}}
.back-top:hover{{background:var(--accent);color:#fff;border-color:var(--accent)}}

/* Mobile */
@media(max-width:860px){{
  .sidebar{{transform:translateX(-100%)}}.sidebar.open{{transform:translateX(0)}}
  .main{{margin-left:0;padding:24px 20px 80px}}
  .hamburger{{display:block}}
  h1{{font-size:1.4rem}}
  .chapter-nav a{{font-size:.8rem;padding:6px 10px}}
}}
</style>
</head>
<body>
<div class="progress-bar" id="progressBar"></div>
<button class="hamburger" onclick="toggleSidebar()">&#9776;</button>
<button class="back-top" id="backTop" onclick="window.scrollTo({{top:0,behavior:'smooth'}})">↑</button>
<nav class="sidebar" id="sidebar">
  <div class="sidebar-header">
    <div>
      <h1>养生两千五百年</h1>
      <p>2,500 Years of Wellness</p>
    </div>
    <button class="theme-toggle" id="themeToggle" onclick="toggleTheme()" title="切换主题 / Toggle theme">🌙</button>
  </div>
  <div class="lang-switch">
    <button class="lang-btn active" id="btn-zh" onclick="switchLang('zh')">中文</button>
    <button class="lang-btn" id="btn-en" onclick="switchLang('en')">English</button>
  </div>
  <div class="toc-scroll">
    <a href="#" class="toc-item" data-chapter="cover" onclick="showChapter('cover');return false" style="text-align:center;color:var(--accent2);font-weight:600">📖 封面 / Cover</a>
    <div id="toc-zh">
{zh_toc}
    </div>
    <div id="toc-en" style="display:none">
{en_toc}
    </div>
  </div>
</nav>
<main class="main" id="main">
{cover}
{zh_html}
{en_html}
</main>
<script>
let currentLang='zh',currentChapter='cover';

function toggleTheme(){{
  const html=document.documentElement;
  const isLight=html.getAttribute('data-theme')==='light';
  html.setAttribute('data-theme',isLight?'dark':'light');
  document.getElementById('themeToggle').textContent=isLight?'🌙':'☀️';
  localStorage.setItem('book-theme',isLight?'dark':'light');
}}
(function(){{
  const saved=localStorage.getItem('book-theme');
  if(saved==='light'){{
    document.documentElement.setAttribute('data-theme','light');
    document.addEventListener('DOMContentLoaded',function(){{
      const btn=document.getElementById('themeToggle');
      if(btn)btn.textContent='☀️';
    }});
  }}
}})();

function switchLang(lang){{
  currentLang=lang;
  document.getElementById('btn-zh').classList.toggle('active',lang==='zh');
  document.getElementById('btn-en').classList.toggle('active',lang==='en');
  document.getElementById('toc-zh').style.display=lang==='zh'?'block':'none';
  document.getElementById('toc-en').style.display=lang==='en'?'block':'none';
  if(currentChapter!=='cover'){{
    const base=currentChapter.replace(/-zh$|‐en$/,'').replace(/-en$/,'');
    showChapter(base+'-'+lang);
  }}
}}

function showChapter(id){{
  currentChapter=id;
  document.querySelectorAll('.chapter').forEach(function(c){{c.classList.remove('active');}});
  document.querySelectorAll('.toc-item').forEach(function(t){{t.classList.remove('active');}});
  var el=document.getElementById(id);
  if(el){{
    el.classList.add('active');
  }}
  document.querySelectorAll('.toc-item').forEach(function(t){{
    if(t.getAttribute('data-chapter')===id)t.classList.add('active');
  }});
  window.scrollTo({{top:0}});
  var sb=document.getElementById('sidebar');
  if(sb.classList.contains('open'))sb.classList.remove('open');
}}

function toggleSidebar(){{document.getElementById('sidebar').classList.toggle('open')}}

window.addEventListener('scroll',function(){{
  var h=document.documentElement;
  var pct=h.scrollTop/(h.scrollHeight-h.clientHeight)*100;
  document.getElementById('progressBar').style.width=Math.min(pct,100)+'%';
  document.getElementById('backTop').style.display=h.scrollTop>400?'flex':'none';
}});

document.querySelectorAll('.chapter table').forEach(function(t){{
  if(!t.parentElement.classList.contains('table-wrap')){{
    var w=document.createElement('div');w.className='table-wrap';
    t.parentNode.insertBefore(w,t);w.appendChild(t);
  }}
}});
</script>
</body>
</html>'''


if __name__ == "__main__":
    html = build_full_html()
    out = ROOT / "index.html"
    out.write_text(html, encoding="utf-8")
    size_mb = out.stat().st_size / 1024 / 1024
    print(f"Built {out} ({size_mb:.1f} MB)")
    print(f"Chapters: {len(CHAPTERS_ZH)} ZH + {len(CHAPTERS_EN)} EN = {len(CHAPTERS_ZH)+len(CHAPTERS_EN)} total")
