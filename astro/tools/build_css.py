import re,subprocess,pathlib,json
C=pathlib.Path('/workspace/finclix/finclix/css'); D=pathlib.Path('/workspace/finclix/astro/dist')
parts=[(C/'bootstrap.min.css').read_text()]
st=(C/'style.css').read_text(); st=re.sub(r'@import url\([^)]*\);','',st)
parts+= [(C/'tm-bs-mp.css').read_text(),(C/'tm-utility-classes.css').read_text(),st,(C/'responsive.css').read_text(),(C/'diler.css').read_text(),pathlib.Path('/workspace/finclix/astro/tools/extra.css').read_text()]
css='\n'.join(parts)
css=css.replace('../images/','/images/')
css=css.replace('[hidden]{display:none!important}','[hidden]{display:none!important}:where(div.h4,div.h6){margin-top:0;margin-bottom:.5rem}',1)
css=re.sub(r'(?<![\w.#-])h([46])\b(?![-\w])',r':is(h\1,.h\1)',css)
css=re.sub(r'>\s*img\b',' img',css)
raw=pathlib.Path('/tmp/site.full.css'); raw.write_text(css)
cfg={"content":[str(D/'index.html'),str(D/'_astro/*.js')],"css":[str(raw)],"output":"/tmp/purged.css",
 "safelist":{"standard":["show","active","active-block","current","fixed-header","mobile-menu-visible","in","js","fade"],"deep":[],"greedy":[]},
 "fontFace":False,"keyframes":True,"variables":False}
pathlib.Path('/tmp/purgecss.json').write_text(json.dumps(cfg))
subprocess.run(['node','tools/purge.mjs','/tmp/purgecss.json'],check=True,cwd='/workspace/finclix/astro')
out=pathlib.Path('/tmp/purged.css').read_text()
out=re.sub(r'/\*.*?\*/','',out,flags=re.S); out=re.sub(r'\s+',' ',out)
(D/'css').mkdir(exist_ok=True); (D/'css/site.css').write_text(out)
print(len(css),'->',len(out))
for u in sorted(set(re.findall(r'url\(["\']?(/images/[^)"\']+)',out))): print('url',u, (D/u.lstrip('/')).exists())
