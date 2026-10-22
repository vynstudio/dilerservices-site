import sys, asyncio
from playwright.async_api import async_playwright
base=sys.argv[1]; tag=sys.argv[2]
async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch(executable_path='/usr/bin/google-chrome')
    for w,h in [(390,844),(1280,800)]:
      for L in ['','es/','pt/']:
        pg=await b.new_page(viewport={'width':w,'height':h})
        await pg.goto(base+L,wait_until='networkidle')
        await pg.wait_for_timeout(2500)
        # scroll through to trigger wow
        H=await pg.evaluate('document.body.scrollHeight')
        for y in range(0,H,600):
          await pg.evaluate(f'window.scrollTo(0,{y})'); await pg.wait_for_timeout(120)
        await pg.evaluate('window.scrollTo(0,0)'); await pg.wait_for_timeout(2500)
        sw=await pg.evaluate('[document.documentElement.scrollWidth, window.innerWidth, document.body.scrollWidth]')
        wide=await pg.evaluate('''()=>[...document.querySelectorAll('body *')].filter(e=>{const r=e.getBoundingClientRect();return r.right>innerWidth+1&&r.width>0&&getComputedStyle(e).position!='fixed'}).slice(0,6).map(e=>e.className+':'+Math.round(e.getBoundingClientRect().right))''')
        print(w,L or 'en',sw, wide[:4])
        if L=='':
          await pg.add_style_tag(content='.wow{visibility:visible!important;animation:none!important;clip-path:none!important;opacity:1!important}')
          await pg.wait_for_timeout(500)
          await pg.screenshot(path=f'/workspace/shots-ds-finclix/{tag}home-{w}.png',full_page=True)
        await pg.close()
    await b.close()
asyncio.run(main())
