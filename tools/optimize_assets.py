"""Create delivery assets from preserved sources; run before build_site.py."""
from pathlib import Path
from PIL import Image
from fontTools import subset
from fontTools.ttLib import TTFont
P=Path(__file__).resolve().parents[1]; src=P/'content/source-assets'; dest=P/'dist/assets'
for name in ['logo.svg','favicon.svg']:
    (dest/name).write_bytes((src/name).read_bytes())
photos=['hero','canteen','cleaning','engineering','remote-food','restaurant','sanatorium','transport']
for name in photos:
    source=src/(name+('.png' if name=='transport' else '.webp'))
    im=Image.open(source).convert('RGB')
    main=im.copy();main.thumbnail((1600 if name=='hero' else 1000,1600 if name=='hero' else 1000),Image.Resampling.LANCZOS)
    main.save(dest/(name+'.webp'),'WEBP',quality=78,method=6)
    mobile=im.copy();mobile.thumbnail((768 if name=='hero' else 480,768 if name=='hero' else 480),Image.Resampling.LANCZOS)
    mobile.save(dest/(name+'-small.webp'),'WEBP',quality=72,method=6)
im=Image.open(src/'presentation-background.png').convert('RGB');im.thumbnail((1280,1280),Image.Resampling.LANCZOS);im.save(dest/'presentation-background.webp','WEBP',quality=75,method=6)
im=Image.open(src/'symbol.png');im.thumbnail((64,64),Image.Resampling.LANCZOS);im.save(dest/'symbol.png',optimize=True)
unicodes=set(range(0x20,0x100))|set(range(0x400,0x530))|set(range(0x2000,0x2300))
for name in ['noto-regular','noto-bold']:
    font=TTFont(src/(name+'.ttf'))
    options=subset.Options();options.flavor='woff';options.layout_features=['*']
    sub=subset.Subsetter(options=options);sub.populate(unicodes=unicodes);sub.subset(font)
    font.flavor='woff';font.save(dest/(name+'.woff'))
for old in ['logo.png','transport.png','presentation-background.png','noto-regular.ttf','noto-bold.ttf']:
    (dest/old).unlink(missing_ok=True)
print('Source images: {:.0f} KB; delivery images (including mobile variants + SVG): {:.0f} KB'.format(sum(p.stat().st_size for p in src.iterdir() if p.suffix in ('.png','.webp'))/1024,sum(p.stat().st_size for p in dest.iterdir() if p.suffix in ('.png','.webp','.svg'))/1024))
print('Fonts: {:.0f} KB → {:.0f} KB'.format(sum((src/(n+'.ttf')).stat().st_size for n in ['noto-regular','noto-bold'])/1024,sum(p.stat().st_size for p in dest.glob('*.woff'))/1024))
