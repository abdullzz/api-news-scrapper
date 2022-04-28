from requests_html import AsyncHTMLSession
import asyncio
import pyppeteer
   
async def get_post(url):
    new_loop=asyncio.new_event_loop()
    asyncio.set_event_loop(new_loop)
    session = AsyncHTMLSession()
    browser = await pyppeteer.launch({ 
        'ignoreHTTPSErrors':True, 
        'headless':True, 
        'handleSIGINT':False, 
        'handleSIGTERM':False, 
        'handleSIGHUP':False
    })
    session._browser = browser
    resp_page = await session.get(url)
    await resp_page.html.arender(timeout=10)
    return resp_page

loop = asyncio.new_event_loop()
url = "https://www.cnnindonesia.com/nasional"
asyncio.set_event_loop(loop)
result = loop.run_until_complete(get_post(url))
print([x.text for x in result.html.find('span.box_text > h2.title')])
