"""Generate static review pages. Production: --base-url https://your-confirmed-host/"""
from pathlib import Path
import re, html, argparse, json, hashlib
from PIL import Image
from urllib.parse import urljoin
P=Path(__file__).resolve().parents[1]; D=P/'dist'
def asset_version(name):
    return hashlib.sha256((D/name).read_bytes()).hexdigest()[:10]
a=argparse.ArgumentParser(); a.add_argument('--base-url'); args=a.parse_args()
if args.base_url and not args.base_url.startswith('https://'): a.error('base URL must use HTTPS')
s=(P/'content/original-landing.html').read_text()
def section(id):
    match=re.search(r'<section\b[^>]*\bid="'+id+r'"[^>]*>.*?</section>',s,re.S)
    return match.group() if match else ''
services=[('korporativnoe-pitanie','Корпоративное питание','Рационы и обслуживание под график предприятия.','canteen.webp',['Завтраки, обеды и ужины','Ланч-боксы и столы заказов','VIP-обслуживание','Протокольные и праздничные мероприятия'],'Предприятия, офисы и вахтовые площадки','Численность людей, сменность, имеющаяся кухня, условия доставки и требования к меню.'),('gostinichnyy-servis','Гостиничный сервис и санатории','Питание и повседневный сервис для гостей и персонала.','sanatorium.webp',['Заказное питание и шведский стол','Лечебно-профилактические рационы','Рестораны, бары и кафе','Доставка блюд в номера'],'Гостиницы, санатории и объекты размещения','Категории гостей, загрузка объекта, режим питания и требования к специальным рационам.'),('klining','Профессиональный клининг','Чистота помещений и территории с учётом режима объекта.','cleaning.webp',['Ежедневная и генеральная уборка','Уборка после ремонта','Окна, фасады и территория','Снег, отходы, дезинфекция и дератизация'],'Производственные, административные и жилые помещения','Площадь, типы покрытий, интенсивность использования и допустимое время выполнения работ.'),('tekhnicheskaya-ekspluatatsiya','Техническая эксплуатация','Обслуживание инженерных систем, зданий и сооружений.','engineering.webp',['Электричество, тепло и вода','Вентиляция и канализация','Слаботочные сети','Холодильное и лифтовое оборудование'],'Объекты с инженерной инфраструктурой','Перечень оборудования, техническая документация, состояние систем и действующие регламенты.'),('transport-i-snabzhenie','Транспорт и снабжение','Перевозки и обеспечение повседневной работы объекта.','transport.webp',['Грузоперевозки','Доставка персонала','Работы спецтехники','Снабжение СИЗ и питьевой водой'],'Городские и удалённые площадки','Маршруты, график перевозок, объёмы грузов, сезонность и условия доступа на объект.'),('servisnaya-podderzhka','Сервисная поддержка','Сопутствующие процессы в единой системе обслуживания.','remote-food.webp',['Прачечная и химчистка','Поездки и размещение','Подбор, учёт и подготовка персонала','Координация и контроль услуг'],'Объекты, которым требуется несколько связанных сервисов','Перечень процессов, график работы, распределение ответственности и приоритеты заказчика.')]
nav=[('company/','Компания'),('services/','Услуги'),('suppliers/','Поставщикам'),('career/','Карьера'),('contacts/','Контакты')]
dialog=re.search(r'<dialog.*?</dialog>',s,re.S).group()
footer='<footer><div class="wrap"><a class="brand" href="{root}"><img src="{root}assets/logo.svg" alt="РЕСК" width="1000" height="310"></a><p>Российская Единая Сервисная Компания<br>Забота о людях. Надёжная работа объекта.</p><a href="{root}contacts/">Обсудить сотрудничество →</a></div></footer>'
def cards(root):
    return '<div class="direction-grid">'+''.join(f'<a class="direction" style="--direction-image:url({root}assets/{Path(services[i][3]).stem}-small.webp)" href="{root}services/{slug}/"><span class="eyebrow">0{i+1}</span><h3>{title}</h3><p>{desc}</p><span class="arrow" aria-hidden="true">↗</span></a>' for i,(slug,title,desc,*_) in enumerate(services))+'</div>'
def cta(root): return f'<section class="closing compact"><div class="wrap"><div><span class="eyebrow light">СЛЕДУЮЩИЙ ШАГ</span><h2>Обсудим задачи<br>вашего объекта</h2></div><a class="button coral" href="{root}contacts/">Перейти к обсуждению →</a></div></section>'
def page(path,title,desc,body,crumbs=()):
    depth=path.count('/') if path else 0; root='../'*depth or './'
    head=f'<meta name="robots" content="{"index,follow" if args.base_url else "noindex,follow"}">'
    if args.base_url:
        url=urljoin(args.base_url.rstrip('/')+'/',path)
        head+=f'<link rel="canonical" href="{url}"><meta property="og:url" content="{url}">'
    head+=f'<meta property="og:type" content="website"><meta property="og:title" content="{html.escape(title)}"><meta property="og:description" content="{html.escape(desc)}">'
    links=''.join(f'<a href="{root}{url}"'+(' aria-current="page"' if path==url else '')+f'>{label}</a>' for url,label in nav)
    bread=''
    if path:
        bread=f'<nav class="breadcrumbs wrap" aria-label="Хлебные крошки"><a href="{root}">Главная</a>'
        for url,label in crumbs: bread+=f'<span aria-hidden="true">/</span><a href="{root}{url}">{label}</a>'
        bread+=f'<span aria-hidden="true">/</span><span>{html.escape(title.split(" — ")[0])}</span></nav>'
    out=f'<!doctype html><html lang="ru"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{html.escape(title)}</title><meta name="description" content="{html.escape(desc)}">{head}<link rel="icon" type="image/svg+xml" href="{root}assets/favicon.svg"><link rel="stylesheet" href="{root}style.css"><link rel="stylesheet" href="{root}architecture.css"></head><body><a class="skip" href="#main">К содержанию</a><header><div class="wrap header"><a class="brand" href="{root}" aria-label="РЕСК — главная"><img src="{root}assets/logo.svg" alt="РЕСК" width="1000" height="310"></a><nav id="primary-nav" aria-label="Главное меню">{links}</nav><button id="menu" aria-controls="primary-nav" aria-expanded="false" aria-label="Открыть меню">Меню</button></div></header><main id="main">{bread}{body.replace("{{root}}",root)}</main>{footer.format(root=root)}{dialog}<script src="{root}script.js"></script></body></html>'
    # Retained content sections use local assets.
    for name in ['style.css','architecture.css','script.js']:
        out=out.replace(f'{root}{name}"',f'{root}{name}?v={asset_version(name)}"')
    out=out.replace('src="assets/','src="'+root+'assets/')
    def optimize_image(match):
        tag=match.group()
        source=re.search(r'src="([^"]+)"',tag)
        if not source:return tag
        name=Path(source.group(1)).name
        if 'decoding=' not in tag:tag=tag.replace('<img ','<img decoding="async" ',1)
        if name.endswith('.webp'):
            image=D/'assets'/name
            width,height=Image.open(image).size
            tag=re.sub(r' width="\d+"| height="\d+"','',tag)
            stem=Path(name).stem
            small=D/'assets'/(stem+'-small.webp')
            attrs=f' width="{width}" height="{height}"'
            if small.exists():
                small_width=Image.open(small).width
                sizes='100vw' if stem=='hero' else '(max-width:820px) calc(100vw - 40px), (max-width:1439px) 50vw, 660px'
                attrs+=f' srcset="{root}assets/{small.name} {small_width}w, {root}assets/{name} {width}w" sizes="{sizes}"'
            tag=tag[:-1]+attrs+'>'
        return tag
    out=re.sub(r'<img\b[^>]*>',optimize_image,out)
    target=D/path/'index.html'; target.parent.mkdir(parents=True,exist_ok=True); target.write_text(out)
    return path
paths=[]
def add(path,title,desc,body,crumbs=()): paths.append(page(path,title,desc,body,crumbs))
def intro(label,title,text): return f'<section class="page-intro wrap"><div class="eyebrow">{label}</div><h1>{title}</h1><p class="lead">{text}</p></section>'
hero='<section class="hero hero-background"><img class="hero-backdrop" src="assets/hero.webp" alt="" fetchpriority="high" width="1600" height="1000"><div class="wrap hero-grid"><div class="hero-copy"><div class="eyebrow light">РОССИЙСКАЯ ЕДИНАЯ СЕРВИСНАЯ КОМПАНИЯ</div><h1>Комплексный сервис<br>для <span>вашего объекта</span></h1><p>Питание, комфорт и надёжная работа инфраструктуры. От Крайнего Севера до крупных городов.</p><div class="actions"><button class="button coral" data-brief>Подготовить запрос</button><a class="text-link" href="services/">Наши направления</a></div><div class="hero-note"><span class="line"></span>Забота о людях. Каждый день.</div></div></div></section>'
home_end='<section class="home-finale"><div class="wrap"><div class="eyebrow light">ОТ ЗАДАЧИ К СЕРВИСУ</div><div class="finale-grid"><h2>Начнём с задач<br>вашего объекта.</h2><div><p>Изучим условия площадки, определим состав услуг и организацию работы. Это основа для обсуждения решения и его запуска.</p><div class="actions"><a class="button coral" href="contacts/">Обсудить объект →</a><a class="text-link" href="company/">Как работает РЕСК</a></div></div></div></div></section>'
add('','РЕСК — комплексное обслуживание объектов','Корпоративное питание, клининг, техническая эксплуатация и сервисная поддержка объектов. Изучите направления услуг РЕСК.',hero+'<section class="section wrap"><div class="section-head"><div><div class="eyebrow">НАПРАВЛЕНИЯ</div><h2>Шесть направлений.<br>Одна система сервиса.</h2></div><a class="text-link" href="services/">Все услуги →</a></div>'+cards('./')+'</section>'+home_end)
add('services/','Услуги по обслуживанию объектов — РЕСК','Шесть направлений РЕСК: питание, гостиничный сервис, клининг, эксплуатация, транспорт и сервисная поддержка.',intro('УСЛУГИ','Сервис под задачи<br>вашего объекта','Выберите отдельное направление или объедините несколько услуг в комплексное решение.')+'<section class="section wrap no-top">'+cards('../')+'</section>'+cta('../'))
for slug,title,desc,img,items,where,inputs in services:
    body=intro('НАПРАВЛЕНИЕ УСЛУГ',title,desc)+f'<section class="service-detail wrap"><img src="{{{{root}}}}assets/{img}" alt="Иллюстрация направления: {title.lower()}" width="1000" height="700"><div><h2>Состав услуг</h2><ul class="scope">'+''.join('<li>'+x+'</li>' for x in items)+f'</ul><p>Состав и условия обслуживания определяются техническим заданием заказчика.</p></div></section><section class="section wrap information"><div><h2>Для каких объектов</h2><p>{where}. Решение адаптируется к условиям площадки и потребностям людей.</p></div><div><h2>Что обсудим на старте</h2><p>{inputs}</p><a class="text-link" href="../../contacts/">Подготовить исходные данные →</a></div></section>'
    if slug=='korporativnoe-pitanie': body+=section('formats')
    body+='<section class="related wrap"><h2>Другие направления</h2><div class="related-links">'+''.join(f'<a href="../{other}/">{name} →</a>' for other,name,*_ in services if other!=slug)+'</div></section>'+cta('../../')
    add('services/'+slug+'/',title+' — РЕСК',desc+' Состав работ и исходные данные для обсуждения обслуживания.',body,[('services/','Услуги')])
add('company/','О компании — РЕСК','Подход РЕСК к комплексному сервису: организация работы, качество, безопасность и профессиональный опыт руководителей.',intro('КОМПАНИЯ','Забота о людях.<br>Ответственность за сервис.','Российская Единая Сервисная Компания объединяет питание, комфорт и обслуживание инфраструктуры объекта.')+section('operations')+section('quality')+section('team')+cta('../'))
add('suppliers/','Поставщикам — РЕСК','Информация для поставщиков продуктов, оборудования, расходных материалов и услуг: что включить в предложение для РЕСК.',intro('ПАРТНЁРАМ','Сотрудничество<br>с поставщиками','Для обсуждения сотрудничества важно понимать ассортимент, условия поставки и возможности работы на конкретном объекте.')+'<section class="section wrap no-top information"><div><h2>Направления поставок</h2><ul class="scope"><li>Продукты и питьевая вода</li><li>Профессиональное оборудование</li><li>Моющие средства и расходные материалы</li><li>Спецодежда и СИЗ</li><li>Транспортные и сопутствующие услуги</li></ul></div><div><h2>Что включить в предложение</h2><p>Укажите ассортимент или состав услуг, географию работы, сроки поставки, минимальный объём заказа и коммерческие условия. Приложите сведения о компании и документы на продукцию, если они применимы.</p><p>Требования к конкретной поставке и порядок сотрудничества необходимо согласовать с представителем РЕСК.</p></div></section>'+cta('../'))
add('career/','Карьера в сфере сервиса — РЕСК','Профессиональные направления в РЕСК: питание, гостиничный сервис, клининг и техническая эксплуатация. Информация для кандидатов.',intro('КАРЬЕРА','Люди, которые<br>создают ежедневный сервис','Питание, чистота и работа инженерных систем зависят от команды. Здесь можно узнать о профессиональных направлениях и подготовиться к разговору о работе.')+'<section class="section wrap no-top information"><div><h2>Профессиональные направления</h2><ul class="scope"><li>Организация питания и обслуживание гостей</li><li>Гостиничный сервис и клининг</li><li>Техническая эксплуатация</li><li>Снабжение и координация сервиса</li></ul></div><div><h2>Для обсуждения работы</h2><p>Подготовьте резюме: профессиональный опыт, желаемое направление, город проживания и удобный график. Для технических специальностей укажите квалификацию и действующие допуски.</p><p>Открытые вакансии и условия работы пока не опубликованы. Их наличие необходимо уточнять у представителя компании.</p></div></section>'+cta('../'))
add('contacts/','Контакты и обсуждение объекта — РЕСК','Подготовьте запрос на обслуживание объекта для РЕСК. Исходные данные для заказчиков, поставщиков и кандидатов.',intro('КОНТАКТЫ','Начнём<br>с вашей задачи','Выберите тему обращения и подготовьте данные для обсуждения с представителем РЕСК.')+'<section class="section wrap no-top information"><div><h2>Обслуживание объекта</h2><p>Тип и расположение площадки, количество людей, график работы, нужные услуги и желаемый срок запуска.</p><button class="button coral" data-brief>Подготовить запрос .txt</button><p class="form-note">Запрос сохраняется файлом на вашем устройстве. Сайт не отправляет его в компанию.</p></div><div><h2>Другие темы</h2><div class="related-links"><a href="../suppliers/">Предложение поставщика →</a><a href="../career/">Работа в компании →</a></div><div class="contact-note"><h3>Контактные данные</h3><p>Телефон, электронная почта и реквизиты появятся здесь после подтверждения компанией. Пока используйте имеющийся у вас контакт представителя РЕСК.</p></div></div></section>')
if args.base_url:
    (D/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join('<url><loc>'+html.escape(urljoin(args.base_url.rstrip('/')+'/',p))+'</loc></url>' for p in paths)+'</urlset>')
    (D/'robots.txt').write_text('User-agent: *\nAllow: /\nSitemap: '+urljoin(args.base_url.rstrip('/')+'/','sitemap.xml')+'\n')
else:
    (D/'robots.txt').write_text('User-agent: *\nAllow: /\n# Review pages contain noindex; enable production with tools/build_site.py --base-url\n')
    (D/'sitemap.xml').unlink(missing_ok=True)
print(f'Generated {len(paths)} pages; mode: '+('production' if args.base_url else 'local review (noindex)'))
