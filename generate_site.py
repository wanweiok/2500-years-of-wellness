"""
Generate an AES-encrypted single-page HTML book from Markdown chapters.
Password-protected via CryptoJS client-side decryption.
"""

import os, hashlib, base64, json, re, secrets
from pathlib import Path

try:
    from Crypto.Cipher import AES
    from Crypto.Util.Padding import pad
except ImportError:
    from Cryptodome.Cipher import AES
    from Cryptodome.Util.Padding import pad

import markdown

PASSWORD = "440726"

CHAPTERS_ZH = [
    ("ch00-preface-zh.md", "前言", "Preface"),
    ("ch01-oldest-conversation-zh.md", "第一章 最古老的健康对话", "Ch1 The Oldest Conversation"),
    ("ch02-living-in-rhythm-zh.md", "第二章 顺时而活", "Ch2 Living in Rhythm"),
    ("ch03-food-as-medicine-zh.md", "第三章 食养之道", "Ch3 Food as Medicine"),
    ("ch04-emotional-body-zh.md", "第四章 情志与身体", "Ch4 The Emotional Body"),
    ("ch05-moving-like-water-zh.md", "第五章 动如流水", "Ch5 Moving Like Water"),
    ("ch06-art-of-prevention-zh.md", "第六章 治未病", "Ch6 Art of Prevention"),
    ("ch07-yin-yang-balance-zh.md", "第七章 阴阳之道", "Ch7 Yin-Yang Balance"),
    ("ch08-sleep-healer-zh.md", "第八章 睡眠大药", "Ch8 Sleep: The Great Healer"),
    ("ch09-90-day-reset-zh.md", "第九章 九十天养生计划", "Ch9 90-Day Wellness Reset"),
]

CHAPTERS_EN = [
    ("ch00-preface-en.md", "Preface", "前言"),
    ("ch01-oldest-conversation-en.md", "Ch1: The Oldest Conversation About Health", "第一章"),
    ("ch02-living-in-rhythm-en.md", "Ch2: Living in Rhythm", "第二章"),
    ("ch03-food-as-medicine-en.md", "Ch3: You Are What You Eat", "第三章"),
    ("ch04-emotional-body-en.md", "Ch4: The Emotional Body", "第四章"),
    ("ch05-moving-like-water-en.md", "Ch5: Moving Like Water", "第五章"),
    ("ch06-art-of-prevention-en.md", "Ch6: The Art of Not Getting Sick", "第六章"),
    ("ch07-yin-yang-balance-en.md", "Ch7: Balance, Not Perfection", "第七章"),
    ("ch08-sleep-healer-en.md", "Ch8: Sleep: The Great Healer", "第八章"),
    ("ch09-90-day-reset-en.md", "Ch9: Your 90-Day Wellness Reset", "第九章"),
]


def encrypt_aes_cryptojs(plaintext: str, password: str) -> str:
    salt = secrets.token_bytes(8)
    key, iv = evp_bytes_to_key(password.encode(), salt, 32, 16)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    ct = cipher.encrypt(pad(plaintext.encode("utf-8"), AES.block_size))
    return base64.b64encode(b"Salted__" + salt + ct).decode()


def evp_bytes_to_key(password, salt, key_len=32, iv_len=16):
    d, dtot = b"", b""
    while len(dtot) < key_len + iv_len:
        d = hashlib.md5(d + password + salt).digest()
        dtot += d
    return dtot[:key_len], dtot[key_len : key_len + iv_len]


def md_to_html(md_text):
    md_text = re.sub(r"```mermaid\n(.*?)```", r'<div class="mermaid">\1</div>', md_text, flags=re.DOTALL)
    return markdown.markdown(md_text, extensions=["tables", "fenced_code"])


def build_book_html(chapters, lang_label):
    sections = []
    toc_items = []
    for i, (fname, title, _) in enumerate(chapters):
        path = Path(fname)
        if not path.exists():
            continue
        md_text = path.read_text(encoding="utf-8")
        html = md_to_html(md_text)
        cid = f"ch{i:02d}"
        sections.append(f'<section id="{cid}" class="chapter">{html}</section>')
        toc_items.append(f'<li><a href="#{cid}" onclick="showChapter(\'{cid}\')">{title}</a></li>')
    return "\n".join(toc_items), "\n".join(sections)


def main():
    toc_zh, body_zh = build_book_html(CHAPTERS_ZH, "zh")
    toc_en, body_en = build_book_html(CHAPTERS_EN, "en")

    book_content = f"""
    <div id="book-app">
      <nav id="sidebar">
        <div class="book-title">养生两千五百年</div>
        <div class="book-subtitle">黄帝内经的生活智慧</div>
        <div class="lang-toggle">
          <button onclick="switchLang('zh')" id="btn-zh" class="active">中文</button>
          <button onclick="switchLang('en')" id="btn-en">English</button>
        </div>
        <ul id="toc-zh" class="toc">{toc_zh}</ul>
        <ul id="toc-en" class="toc" style="display:none">{toc_en}</ul>
      </nav>
      <main id="content">
        <div id="body-zh">{body_zh}</div>
        <div id="body-en" style="display:none">{body_en}</div>
      </main>
    </div>
    """

    encrypted = encrypt_aes_cryptojs(book_content, PASSWORD)

    html = generate_full_html(encrypted)

    os.makedirs("docs", exist_ok=True)
    Path("docs/index.html").write_text(html, encoding="utf-8")
    print(f"Generated docs/index.html ({len(html):,} bytes)")
    print(f"Password: {PASSWORD}")


def generate_full_html(encrypted_content):
    return f"""<!DOCTYPE html>
<html lang="zh">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>养生两千五百年 — 2,500 Years of Wellness</title>
<script src="https://cdnjs.cloudflare.com/ajax/libs/crypto-js/4.2.0/crypto-js.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
:root{{--bg:#0a0a0f;--card:#12121a;--text:#e0ddd5;--dim:#8a8780;--accent:#c8a96e;--accent2:#8b7355;--border:#2a2a35;--sidebar-w:300px;--pre-bg:#1a1a25;--quote-bg:rgba(200,169,110,0.05);--th-bg:rgba(200,169,110,0.15);--row-alt:rgba(255,255,255,0.02);--code-bg:rgba(200,169,110,0.1);--mermaid-bg:rgba(255,255,255,0.03);--login-bg:linear-gradient(135deg,#0a0a0f 0%,#1a1520 50%,#0a0a0f 100%);--input-bg:#1a1a25;--shadow:rgba(0,0,0,0.5)}}
[data-theme="light"]{{--bg:#f5f0e8;--card:#ffffff;--text:#2c2c2c;--dim:#6b6560;--accent:#8b6914;--accent2:#a07830;--border:#d4cfc5;--pre-bg:#f0ebe3;--quote-bg:rgba(139,105,20,0.06);--th-bg:rgba(139,105,20,0.1);--row-alt:rgba(0,0,0,0.02);--code-bg:rgba(139,105,20,0.08);--mermaid-bg:rgba(0,0,0,0.02);--login-bg:linear-gradient(135deg,#f5f0e8 0%,#ebe4d6 50%,#f5f0e8 100%);--input-bg:#f0ebe3;--shadow:rgba(0,0,0,0.1)}}
body{{font-family:'Georgia','Noto Serif SC','Source Han Serif CN',serif;background:var(--bg);color:var(--text);line-height:1.85;font-size:17px;transition:background .3s,color .3s}}
a{{color:var(--accent);text-decoration:none}}a:hover{{text-decoration:underline}}

/* Login Gate */
#login-gate{{display:flex;align-items:center;justify-content:center;min-height:100vh;background:var(--login-bg);transition:background .3s}}
.login-box{{background:var(--card);border:1px solid var(--border);border-radius:16px;padding:60px 50px;text-align:center;max-width:440px;width:90%;box-shadow:0 20px 60px var(--shadow);transition:background .3s,border-color .3s,box-shadow .3s}}
.login-box h1{{font-size:28px;color:var(--accent);margin-bottom:8px;font-weight:400;letter-spacing:2px}}
.login-box .subtitle{{color:var(--dim);font-size:14px;margin-bottom:40px;font-style:italic}}
.login-box input{{width:100%;padding:14px 20px;background:var(--input-bg);border:1px solid var(--border);border-radius:8px;color:var(--text);font-size:16px;font-family:inherit;text-align:center;letter-spacing:2px;outline:none;transition:border-color .3s,background .3s}}
.login-box input:focus{{border-color:var(--accent)}}
.login-box button{{margin-top:20px;padding:12px 40px;background:var(--accent);color:#0a0a0f;border:none;border-radius:8px;font-size:16px;font-family:inherit;cursor:pointer;font-weight:600;transition:all .3s}}
.login-box button:hover{{background:#d4b87a;transform:translateY(-1px)}}
.login-box .error{{color:#e74c3c;margin-top:15px;font-size:14px;display:none}}
.login-box .ornament{{color:var(--accent2);font-size:32px;margin-bottom:20px;opacity:0.6}}

/* Book Layout */
#book-app{{display:none}}
#sidebar{{position:fixed;left:0;top:0;width:var(--sidebar-w);height:100vh;background:var(--card);border-right:1px solid var(--border);overflow-y:auto;padding:30px 20px;z-index:100}}
.book-title{{font-size:20px;color:var(--accent);font-weight:400;letter-spacing:1px}}
.book-subtitle{{font-size:13px;color:var(--dim);margin-top:4px;margin-bottom:20px}}
.lang-toggle{{display:flex;gap:8px;margin-bottom:20px}}
.lang-toggle button{{flex:1;padding:6px;background:transparent;border:1px solid var(--border);border-radius:6px;color:var(--dim);font-size:13px;cursor:pointer;font-family:inherit;transition:all .2s}}
.lang-toggle button.active{{background:var(--accent);color:#0a0a0f;border-color:var(--accent);font-weight:600}}
.toc{{list-style:none}}
.toc li{{margin-bottom:6px}}
.toc li a{{display:block;padding:8px 12px;border-radius:6px;color:var(--dim);font-size:14px;transition:all .2s}}
.toc li a:hover,.toc li a.active{{background:rgba(200,169,110,0.1);color:var(--accent);text-decoration:none}}

#content{{margin-left:var(--sidebar-w);padding:40px 60px 80px;max-width:900px}}

/* Typography */
.chapter{{display:none}}.chapter.active{{display:block}}
.chapter h1{{font-size:32px;color:var(--accent);font-weight:400;margin:0 0 30px;padding-bottom:15px;border-bottom:1px solid var(--border)}}
.chapter h2{{font-size:24px;color:var(--text);font-weight:400;margin:40px 0 20px;padding-bottom:10px;border-bottom:1px solid var(--border)}}
.chapter h3{{font-size:19px;color:var(--accent2);margin:30px 0 12px}}
.chapter p{{margin-bottom:16px}}
.chapter blockquote{{border-left:3px solid var(--accent);padding:12px 20px;margin:20px 0;background:var(--quote-bg);border-radius:0 8px 8px 0;font-style:italic}}
.chapter blockquote p{{margin-bottom:8px}}
.chapter table{{width:100%;border-collapse:collapse;margin:20px 0;font-size:15px}}
.chapter th{{background:var(--th-bg);padding:10px 14px;text-align:left;border:1px solid var(--border);color:var(--accent);font-weight:600}}
.chapter td{{padding:10px 14px;border:1px solid var(--border)}}
.chapter tr:nth-child(even){{background:var(--row-alt)}}
.chapter ul,.chapter ol{{margin:12px 0 16px 24px}}
.chapter li{{margin-bottom:6px}}
.chapter code{{background:var(--code-bg);padding:2px 6px;border-radius:4px;font-size:0.9em;color:var(--accent)}}
.chapter pre{{background:var(--pre-bg);padding:16px 20px;border-radius:8px;overflow-x:auto;margin:16px 0;border:1px solid var(--border);transition:background .3s}}
.chapter pre code{{background:none;padding:0;color:var(--text)}}
.chapter strong{{color:var(--accent)}}
.chapter hr{{border:none;border-top:1px solid var(--border);margin:30px 0}}
.mermaid{{background:var(--mermaid-bg);padding:20px;border-radius:8px;margin:20px 0;text-align:center}}

/* Theme Toggle */
#theme-toggle{{position:fixed;top:15px;right:15px;z-index:200;background:var(--card);border:1px solid var(--border);border-radius:8px;padding:8px 12px;color:var(--accent);font-size:18px;cursor:pointer;transition:all .3s;line-height:1}}
#theme-toggle:hover{{border-color:var(--accent)}}

/* Mobile */
#menu-toggle{{display:none;position:fixed;top:15px;left:15px;z-index:200;background:var(--card);border:1px solid var(--border);border-radius:8px;padding:8px 12px;color:var(--accent);font-size:20px;cursor:pointer}}
@media(max-width:768px){{
  #menu-toggle{{display:block}}
  #sidebar{{transform:translateX(-100%);transition:transform .3s}}
  #sidebar.open{{transform:translateX(0)}}
  #content{{margin-left:0;padding:20px 20px 60px}}
  .chapter h1{{font-size:24px}}.chapter h2{{font-size:20px}}
}}
</style>
</head>
<body>

<div id="login-gate">
  <div class="login-box">
    <div class="ornament">☯</div>
    <h1>养生两千五百年</h1>
    <div class="subtitle">2,500 Years of Wellness — The Yellow Emperor's Guide to Living Well</div>
    <input type="password" id="pwd-input" placeholder="请输入访问密码 / Enter password" onkeydown="if(event.key==='Enter')unlock()">
    <br>
    <button onclick="unlock()">进入 / Enter</button>
    <div class="error" id="pwd-error">密码错误 / Incorrect password</div>
  </div>
</div>

<button id="theme-toggle" onclick="toggleTheme()" title="切换主题 / Toggle theme">🌙</button>
<button id="menu-toggle" onclick="document.getElementById('sidebar').classList.toggle('open')">☰</button>

<div id="encrypted-payload" style="display:none">{encrypted_content}</div>

<script>
function unlock(){{
  var pwd=document.getElementById('pwd-input').value;
  var payload=document.getElementById('encrypted-payload').textContent;
  try{{
    var decrypted=CryptoJS.AES.decrypt(payload,pwd).toString(CryptoJS.enc.Utf8);
    if(!decrypted||decrypted.length<100)throw new Error('bad');
    document.getElementById('login-gate').style.display='none';
    var container=document.createElement('div');
    container.innerHTML=decrypted;
    document.body.appendChild(container.firstElementChild);
    document.getElementById('book-app').style.display='block';
    initBook();
    var mTheme=document.documentElement.getAttribute('data-theme')==='light'?'default':'dark';
    try{{mermaid.initialize({{theme:mTheme,startOnLoad:true}});mermaid.run()}}catch(e){{}}
  }}catch(e){{
    document.getElementById('pwd-error').style.display='block';
    document.getElementById('pwd-input').value='';
    document.getElementById('pwd-input').focus();
  }}
}}

function initBook(){{
  var chapters=document.querySelectorAll('.chapter');
  if(chapters.length>0){{chapters[0].classList.add('active')}}
  var links=document.querySelectorAll('.toc a');
  if(links.length>0){{links[0].classList.add('active')}}
}}

function showChapter(id){{
  document.querySelectorAll('.chapter').forEach(function(c){{c.classList.remove('active')}});
  var el=document.getElementById(id);
  if(el){{el.classList.add('active');window.scrollTo(0,0)}}
  document.querySelectorAll('.toc a').forEach(function(a){{a.classList.remove('active')}});
  var link=document.querySelector('.toc a[onclick*="'+id+'"]');
  if(link)link.classList.add('active');
  document.getElementById('sidebar').classList.remove('open');
}}

function switchLang(lang){{
  document.getElementById('body-zh').style.display=lang==='zh'?'block':'none';
  document.getElementById('body-en').style.display=lang==='en'?'block':'none';
  document.getElementById('toc-zh').style.display=lang==='zh'?'block':'none';
  document.getElementById('toc-en').style.display=lang==='en'?'block':'none';
  document.getElementById('btn-zh').className=lang==='zh'?'active':'';
  document.getElementById('btn-en').className=lang==='en'?'active':'';
  document.querySelectorAll('.chapter').forEach(function(c){{c.classList.remove('active')}});
  var first=document.querySelector('#body-'+ lang+' .chapter');
  if(first)first.classList.add('active');
  window.scrollTo(0,0);
}}

function toggleTheme(){{
  var html=document.documentElement;
  var btn=document.getElementById('theme-toggle');
  if(html.getAttribute('data-theme')==='light'){{
    html.removeAttribute('data-theme');
    btn.textContent='🌙';
    localStorage.setItem('book-theme','dark');
    try{{mermaid.initialize({{theme:'dark'}});mermaid.run()}}catch(e){{}}
  }}else{{
    html.setAttribute('data-theme','light');
    btn.textContent='☀️';
    localStorage.setItem('book-theme','light');
    try{{mermaid.initialize({{theme:'default'}});mermaid.run()}}catch(e){{}}
  }}
}}

(function(){{
  var saved=localStorage.getItem('book-theme');
  if(saved==='light'){{
    document.documentElement.setAttribute('data-theme','light');
    document.getElementById('theme-toggle').textContent='☀️';
  }}
}})();

document.getElementById('pwd-input').focus();
</script>
</body>
</html>"""


if __name__ == "__main__":
    main()
