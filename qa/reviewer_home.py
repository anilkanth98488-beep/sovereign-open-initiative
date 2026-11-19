"""Exercise every public homepage control and reopen each browser download."""
import json
import os
import re
from io import BytesIO
from urllib.parse import urljoin
import openpyxl
import pdfplumber
from playwright.sync_api import sync_playwright

base=os.environ.get('HOME_TEST_URL','http://127.0.0.1:8088/docs/index.html')
remote=os.environ.get('HOME_NETWORK_CHECKS')=='1'
def layout(page):
    assert page.evaluate('document.documentElement.scrollWidth<=document.documentElement.clientWidth')
    assert page.locator('main section').count()==4
    assert page.evaluate("""() => [...document.querySelectorAll('summary,.action,.choice,footer a')].filter(e=>e.getClientRects().length).every(e=>e.getBoundingClientRect().height >= 44)""")
    assert page.evaluate("""() => [...document.querySelectorAll('summary,dl div,.actions,header div')].every(parent=>{
      const rs=[...parent.children].filter(e=>e.getClientRects().length).map(e=>e.getBoundingClientRect());
      return rs.every((a,i)=>rs.slice(i+1).every(b=>Math.min(a.right,b.right)-Math.max(a.left,b.left)<1 || Math.min(a.bottom,b.bottom)-Math.max(a.top,b.top)<1))
    })""")
def activate(locator):
    if locator.page.viewport_size["width"] == 390:
        locator.tap()
    else:
        locator.click()

def download(page,kind):
    with page.expect_download() as info:activate(page.locator('#'+kind))
    d=info.value
    assert d.failure() is None and d.suggested_filename.endswith('.'+kind)
    data=d.path().read_bytes()
    if kind=='xlsx':
        book=openpyxl.load_workbook(BytesIO(data));fields=dict(list(book.active.values)[1:])
        assert fields['status']=='PASS' and str(fields['calculated_closing_balance'])=='1250.00'
    elif kind=='json':
        notes=json.loads(data)['exceptions'];assert [n['metric'] for n in notes]==['$200.00','$500.00','10 points']
        assert all(n['status']=='REVIEW_REQUIRED' and n['question'] for n in notes)
    else:
        with pdfplumber.open(BytesIO(data)) as doc:
            text=' '.join(p.extract_text() for p in doc.pages)
            assert all(v in text for v in ('$200.00','$500.00','90%','REVIEW_REQUIRED'))

def run(browser,engine,width,height):
    ctx=browser.new_context(viewport={'width':width,'height':height},has_touch=width==390,accept_downloads=True)
    p=ctx.new_page(); errors=[];bad=[]
    p.on('pageerror',lambda err:errors.append(str(err)))
    p.on('console',lambda msg: errors.append(msg.text) if msg.type=='error' else None)
    p.on('requestfailed',lambda req:bad.append(req.url))
    p.on('response',lambda response:bad.append(f'{response.status} {response.url}') if response.status>=400 else None)
    res=p.goto(base,wait_until='networkidle');assert res and res.status==200
    assert p.evaluate("getComputedStyle(document.querySelector('input')).fontSize")=='16px'
    layout(p);assert p.locator('#status').inner_text()=='PASS';download(p,'xlsx')
    activate(p.locator('label').filter(has_text='$1,251.00'));assert p.locator('#status').inner_text()=='FAIL'
    assert '−$1.00' in p.locator('#variance').inner_text()
    assert p.locator('#xlsx').is_hidden() and p.locator('#xlsx').get_attribute('href') is None
    activate(p.locator('label').filter(has_text='$1,250.00'));download(p,'xlsx')
    assert p.locator('details').count()==7
    for i,d in enumerate(p.locator('details').all()):
        activate(d.locator('summary'));assert d.get_attribute('open') is not None
        if i<3:
            assert d.locator('.flag').inner_text()=='REVIEW_REQUIRED' and '?' in d.locator('.inside').inner_text()
        else:
            expected=[1,3,1,2][i-3];assert d.locator('article').count()==expected
            for card in d.locator('article').all():
                assert card.locator('pre').count()==2
                for pre in card.locator('pre').all():assert pre.is_visible() and json.loads(pre.inner_text())
        layout(p);activate(d.locator('summary'));assert d.get_attribute('open') is None
    download(p,'json');download(p,'pdf')
    assert not re.search(r'\bundefined\b',p.locator('body').inner_text())
    assert p.locator('a').count()==5 and p.locator('button').count()==0
    for loc in ('#contact','footer a'):
        link=p.locator(loc);href=link.get_attribute('href');assert href
        if remote or loc=='footer a':
            target=urljoin(base,href)
            resp=ctx.request.get(target,timeout=60000)
            assert resp.ok,(target,resp.status)
            if loc=='footer a':assert 'id="ecosystem"' in resp.text()
        # Verify the click navigates to its exact intended target. External GitHub
        # availability is checked above; do not submit a contact request.
        target=urljoin(base,href)
        if loc=='#contact':
            p.route('https://github.com/**',lambda route:route.fulfill(status=200,body='GitHub walkthrough request'))
        activate(link)
        p.wait_for_url(lambda url: url == target, wait_until="domcontentloaded")
        assert p.url==target,(p.url,target)
        if loc=='footer a':assert p.locator('#ecosystem').is_visible()
        p.goto(base,wait_until='networkidle')
    assert not errors and not bad,(errors,bad)
    print(f'{engine} {width}x{height} PASS: two ledger controls, all seven disclosures, XLSX/PDF/JSON reopened, CTA and prototype link; layout, console and resources clean.',flush=True)
    ctx.close()
with sync_playwright() as pw:
    for engine in os.getenv('HOME_BROWSERS','chromium,webkit').split(','):
        kwargs={'executable_path':os.environ['CHROME_PATH']} if engine=='chromium' and os.getenv('CHROME_PATH') else {}
        b=getattr(pw,engine).launch(**kwargs)
        try:
            for w,h in ((390,844),(1280,800)):run(b,engine,w,h)
        finally:b.close()
