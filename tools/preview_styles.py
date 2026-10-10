"""Build local, unlinked styling comparisons from the company page."""
from pathlib import Path

root = Path(__file__).resolve().parents[1]
preview = root / 'dist/review-style'
preview.mkdir(exist_ok=True)
company = (root / 'dist/company/index.html').read_text()
common = '''
.team-grid article::after{display:none}
.team-grid article{box-shadow:none;border-radius:16px;padding:32px}
.team-grid .experience{background:transparent;border:0;border-radius:0;padding:0 0 24px;margin:26px 0;min-height:135px;border-bottom:1px solid #ffffff40}
.team-grid .role{min-height:3em}
.team-grid .experience strong{font-size:2.4rem}
@media(max-width:820px){.team-grid .experience{min-height:0}.team-grid .role{min-height:0}.team-grid article{padding:28px}}
'''
dark = '''
header.is-scrolled{top:0;margin:0;border-radius:0;background:#102942;border-bottom:1px solid #3EAAC04d;box-shadow:0 10px 24px #10294240}
header.is-scrolled .brand{background:#fff;border-radius:8px;padding:5px 9px}
header.is-scrolled nav a{color:#fff}
header.is-scrolled nav a:hover{color:#a7dce7}
header.is-scrolled.menu-open nav{background:#102942;border-color:#3EAAC04d}
.team-grid article{background:#102942;color:#fff;border:1px solid #102942}
.team-grid .role,.team-grid article>p:last-child,.team-grid .experience span{color:#d6e2eb}
.team-grid .experience strong{color:#77d0df}
'''
floating = '''
header{transition:margin .2s,box-shadow .2s,background-color .2s}
header.is-scrolled{top:12px;margin:12px 16px -12px;border:1px solid #10294255;border-radius:14px;background:#fff;box-shadow:0 12px 30px #10294240}
header.is-scrolled .wrap{width:min(1200px,calc(100% - 40px))}
header.is-scrolled.menu-open nav{left:-1px;right:-1px;border:1px solid #10294255;border-top:0;border-radius:0 0 14px 14px;box-shadow:0 16px 30px #10294230}
.team-grid article{background:white;border:1.5px solid #102942;border-left:6px solid #102942}
.team-grid .experience{border-color:#10294233}
.team-grid .experience strong{color:#b33842}
.team-grid .role,.team-grid article>p:last-child,.team-grid .experience span{color:#344d63}
@media(max-width:520px){header.is-scrolled{top:8px;margin:8px 8px -8px}header.is-scrolled .wrap{width:calc(100% - 24px)}header.is-scrolled .brand img{width:144px}}
'''
for name, css in [('dark',dark),('floating',floating)]:
    out = company.replace('</head>',f'<style>{common}{css}</style></head>')
    (preview / f'{name}.html').write_text(out)
(preview / 'index.html').write_text('''<!doctype html>
<html lang="ru"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex,nofollow"><title>Варианты оформления РЕСК</title>
<style>
@font-face{font-family:Noto;src:url('../assets/noto-regular.woff');font-display:swap}@font-face{font-family:Noto;src:url('../assets/noto-bold.woff');font-weight:700;font-display:swap}
*{box-sizing:border-box}body{margin:0;background:#fff;color:#102942;font-family:Noto,sans-serif}main{padding:22px 24px;max-width:1320px;margin:auto}h1{font-size:26px;margin:0 0 12px}p{font-size:15px;line-height:1.5;margin:0 0 16px}nav{display:flex;gap:10px;flex-wrap:wrap}button{font:inherit;font-size:15px;padding:11px 16px;background:#fff;border:1px solid #102942;border-radius:8px;color:#102942;cursor:pointer}button[aria-pressed=true]{background:#102942;color:#fff}a{color:#102942;font-size:14px}iframe{display:block;width:100%;height:calc(100vh - 208px);min-height:620px;border:0;border-top:1px solid #10294233}#description{margin-top:14px;margin-bottom:8px}@media(max-width:600px){main{padding:18px 16px}h1{font-size:22px}iframe{height:75vh}}
</style></head><body><main><h1>Два варианта оформления</h1><p>Переключайте варианты и прокручивайте страницу ниже: хедер меняется при скролле. Фон финального блока в обоих вариантах занимает всю секцию.</p><nav aria-label="Варианты оформления"><button data-variant="dark" aria-pressed="false">1. Тёмный хедер и карточки</button><button data-variant="floating" aria-pressed="true">2. Плавающий хедер и рамки</button></nav><p id="description">Более строгий вариант: белая шапка с отступом от краёв, заметной тенью и контуром; карточки с тёмной боковой гранью и коралловыми показателями.</p><a id="open" href="floating.html#team" target="_blank">Открыть вариант на всю ширину →</a></main><iframe title="Предпросмотр оформления компании" src="floating.html#team"></iframe>
<script>const descriptions={dark:'Контрастный вариант: тёмно-синяя шапка, логотип на белой подложке, тёмные карточки и крупные бирюзовые показатели.',floating:'Более строгий вариант: белая шапка с отступом от краёв, заметной тенью и контуром; карточки с тёмной боковой гранью и коралловыми показателями.'};document.querySelectorAll('[data-variant]').forEach(button=>button.addEventListener('click',()=>{document.querySelectorAll('[data-variant]').forEach(b=>b.setAttribute('aria-pressed',String(b===button)));const url=button.dataset.variant+'.html#team';document.querySelector('iframe').src=url;document.querySelector('#open').href=url;document.querySelector('#description').textContent=descriptions[button.dataset.variant]}));</script></body></html>''')
print(f'Local comparison: {preview}/index.html')
