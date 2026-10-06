import { createRequire } from 'node:module';
import { readFile, mkdir, writeFile } from 'node:fs/promises';
import { resolve } from 'node:path';
const require=createRequire(import.meta.url);
const {chromium}=require(process.env.CODEX_PRIMARY_RUNTIME_NODE_MODULES ? process.env.CODEX_PRIMARY_RUNTIME_NODE_MODULES+'/playwright' : 'playwright');
const base=process.env.PORTFOLIO_BASE_URL||'http://127.0.0.1:8765';
const paths=['/','/projects/insulin-assistant/','/projects/clinical-research-hub/','/projects/advisor-matching/','/projects/glucoguide/','/projects/woundguard/','/projects/aegis/','/evidence/','/profile/','/privacy/'];
const browser=await chromium.launch({headless:true,executablePath:chromium.executablePath(),args:['--no-sandbox']});
const context=await browser.newContext({viewport:{width:1440,height:1000},reducedMotion:'reduce'});
const page=await context.newPage();
const failures=[];const checks=[];
const assert=(condition,message)=>{checks.push({message,pass:Boolean(condition)});if(!condition)failures.push(message);};
await mkdir(resolve('tests/artifacts'),{recursive:true});
const pageErrors=[];page.on('pageerror',error=>pageErrors.push(error.message));

// Capture the existing empty-state clinical interface for documentation only.
if(!process.env.PORTFOLIO_BASE_URL){
 await page.setViewportSize({width:1360,height:950});
 await page.goto(base+'/insulin-infusion/',{waitUntil:'load'});
 await page.locator('#langEN').click();
 await page.screenshot({path:'tests/artifacts/live-insulin-interface.jpg'});
}

const internalUrls=new Set();const titles=new Set();
for(const path of paths){
 const response=await page.goto(base+path,{waitUntil:'networkidle'});
 assert(response?.status()===200,path+' returns 200');
 const state=await page.evaluate(()=>({title:document.title,h1:document.querySelectorAll('h1').length,main:document.querySelectorAll('main').length,lang:document.documentElement.lang,description:document.querySelector('meta[name="description"]')?.content,canonical:document.querySelector('link[rel="canonical"]')?.href,ogImage:document.querySelector('meta[property="og:image"]')?.content,images:[...document.images].map(i=>({src:i.getAttribute('src'),alt:i.alt,loaded:i.complete&&i.naturalWidth>0,hidden:Boolean(i.closest('[hidden]'))})),links:[...document.querySelectorAll('a[href]')].map(a=>({href:a.getAttribute('href'),target:a.target,rel:a.rel})),scripts:[...document.querySelectorAll('script[type="application/ld+json"]')].map(s=>JSON.parse(s.textContent))}));
 assert(state.h1===1,path+' has one main heading');assert(state.main===1,path+' has one main landmark');assert(state.lang==='en',path+' declares English');assert(!titles.has(state.title),path+' has a unique title');titles.add(state.title);
 assert(state.description?.length>20,path+' has a description');assert(state.canonical==='https://gurkancamok.github.io'+path,path+' has the correct canonical URL');assert(state.ogImage?.endsWith('/assets/social-card.png'),path+' has a social preview');assert(state.scripts.flat().some(s=>s['@type']==='Person'),path+' contains Person structured data');
 for(const img of state.images)assert((img.hidden||img.loaded)&&img.alt.length>0,path+' visible image loads with alt text: '+img.src);
 for(const a of state.links){if(a.target==='_blank')assert(a.rel.includes('noopener'),path+' external tab isolation: '+a.href);if(a.href.startsWith('/')||a.href.startsWith('#'))internalUrls.add(new URL(a.href,base+path).href);}
 for(const width of [360,390,768,1280,1440]){
  await page.setViewportSize({width,height:950});
  const layout=await page.evaluate(()=>({width:innerWidth,scrollWidth:document.documentElement.scrollWidth}));
  assert(layout.scrollWidth<=layout.width+1,path+' has no horizontal page overflow at '+width+'px');
 }
}
await page.goto(base+'/',{waitUntil:'networkidle'});
const gallery=page.getByRole('region',{name:'Awards and professional recognition'});
const activeSlide=gallery.locator('[data-gallery-slide]:not([hidden])');
const galleryCheck=async(title,position)=>{
 assert(await activeSlide.count()===1,'Gallery displays one award at a time');
 assert(await activeSlide.getAttribute('data-title')===title,'Gallery displays '+title);
 assert(await gallery.locator('[data-gallery-counter]').textContent()===position,'Gallery updates its position to '+position);
 assert(await gallery.locator('[data-gallery-caption]').textContent()===await activeSlide.getAttribute('data-caption'),'Gallery updates the photograph caption with the active award');
 await activeSlide.locator('img').evaluate(img=>img.decode());
 assert(await activeSlide.locator('img').evaluate(img=>img.naturalWidth>0),'Active award photograph loads');
};
await galleryCheck('WoundGuard','01 / 04');
await gallery.getByRole('button',{name:'Next recognition',exact:true}).click();
await galleryCheck('Doktorclub Awards','02 / 04');
await gallery.getByRole('button',{name:'Next recognition',exact:true}).click();
await galleryCheck('Blood Loss Measurement Device','03 / 04');
await gallery.getByRole('button',{name:'Next recognition',exact:true}).click();
await galleryCheck('Honorable Mention','04 / 04');
await gallery.getByRole('button',{name:'Next recognition',exact:true}).click();
await galleryCheck('WoundGuard','01 / 04');
await gallery.getByRole('button',{name:'Previous recognition',exact:true}).click();
await galleryCheck('Honorable Mention','04 / 04');
await gallery.getByRole('button',{name:'Show Blood Loss Measurement Device',exact:true}).click();
await galleryCheck('Blood Loss Measurement Device','03 / 04');
await gallery.focus();await page.keyboard.press('ArrowLeft');
await galleryCheck('Doktorclub Awards','02 / 04');
await page.keyboard.press('End');await galleryCheck('Honorable Mention','04 / 04');
await page.keyboard.press('Home');await galleryCheck('WoundGuard','01 / 04');
await gallery.dispatchEvent('pointerdown',{pointerType:'touch',clientX:200,clientY:100});
await gallery.dispatchEvent('pointerup',{pointerType:'touch',clientX:110,clientY:102});
await galleryCheck('Doktorclub Awards','02 / 04');
await gallery.dispatchEvent('pointerdown',{pointerType:'touch',clientX:200,clientY:100});
await gallery.dispatchEvent('pointerup',{pointerType:'touch',clientX:202,clientY:200});
await galleryCheck('Doktorclub Awards','02 / 04');
for(const url of internalUrls){const parsed=new URL(url);const response=await context.request.get(url);assert(response.status()===200,'Internal destination exists: '+parsed.pathname);if(parsed.hash){await page.goto(url,{waitUntil:'load'});assert(await page.locator(parsed.hash).count()===1,'Anchor target exists: '+parsed.pathname+parsed.hash);}}
await page.setViewportSize({width:390,height:844});await page.goto(base+'/',{waitUntil:'load'});
const toggle=page.getByRole('button',{name:'Menu',exact:true});await toggle.click();assert(await toggle.getAttribute('aria-expanded')==='true','Mobile menu opens');assert(await page.locator('#primary-navigation').isVisible(),'Mobile navigation visible');await page.keyboard.press('Escape');assert(await toggle.getAttribute('aria-expanded')==='false','Escape closes mobile menu');assert(await toggle.evaluate(e=>e===document.activeElement),'Escape restores menu-button focus');await toggle.click();await page.getByRole('navigation',{name:'Main navigation'}).getByRole('link',{name:'Evidence',exact:true}).click();assert(await toggle.getAttribute('aria-expanded')==='false','Following a mobile link closes menu');
await page.goto(base+'/insulin-infusion-calculator-digital-health-tools-icu-clinical-support-app-diabetes-care-app/',{waitUntil:'load'});await page.waitForURL('**/insulin-infusion/');assert(page.url().endsWith('/insulin-infusion/'),'Legacy insulin link redirects to current application');
await page.goto(base+'/404.html',{waitUntil:'load'});assert(await page.locator('meta[name="robots"]').getAttribute('content')==='noindex, follow','404 page is not indexed');
await page.goto(base+'/',{waitUntil:'networkidle'});await page.setViewportSize({width:1440,height:1000});await page.screenshot({path:'tests/artifacts/desktop-home.png'});await page.screenshot({path:'tests/artifacts/desktop-full.png',fullPage:true});await page.setViewportSize({width:390,height:844});await page.screenshot({path:'tests/artifacts/mobile-home.png'});await page.screenshot({path:'tests/artifacts/mobile-full.png',fullPage:true});await page.goto(base+'/projects/insulin-assistant/',{waitUntil:'load'});await page.setViewportSize({width:1440,height:1000});await page.screenshot({path:'tests/artifacts/insulin-case-study.png'});
assert(pageErrors.length===0,'No application JavaScript errors');
await writeFile('tests/artifacts/check-results.json',JSON.stringify({checkedAt:new Date().toISOString(),total:checks.length,failed:failures.length,checks,pageErrors},null,2));
await browser.close();
console.log(JSON.stringify({checks:checks.length,failed:failures.length,failures,pageErrors},null,2));
if(failures.length)process.exitCode=1;
