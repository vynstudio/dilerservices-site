"""Full-page shots: grow the viewport to the page height so every wow animation fires, then capture."""
import sys, asyncio
from playwright.async_api import async_playwright
url=sys.argv[1]; out=sys.argv[2]; w=int(sys.argv[3])
async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch(executable_path='/usr/bin/google-chrome')
    pg=await b.new_page(viewport={'width':w,'height':900})
    await pg.goto(url,wait_until='networkidle'); await pg.wait_for_timeout(3000)
    H=await pg.evaluate('document.documentElement.scrollHeight')
    for y in range(0,H,500):
      await pg.evaluate(f'window.scrollTo(0,{y})'); await pg.wait_for_timeout(120)
    await pg.wait_for_timeout(2000); await pg.evaluate('window.scrollTo(0,0)')
    await pg.set_viewport_size({'width':w,'height':H}); await pg.wait_for_timeout(4000)
    print(out, await pg.evaluate('[document.documentElement.scrollWidth, innerWidth]'))
    await pg.screenshot(path=out)
    await b.close()
asyncio.run(main())
