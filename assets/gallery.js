'use strict';
function initializeRecognitionGalleries(root=document){
 root.querySelectorAll('[data-recognition-gallery]').forEach(gallery=>{
  if(gallery.dataset.galleryReady==='true')return;
  const slides=Array.from(gallery.querySelectorAll('[data-gallery-slide]'));
  if(slides.length<2)return;
  gallery.dataset.galleryReady='true';
  const dots=Array.from(gallery.querySelectorAll('[data-gallery-index]'));
  const caption=gallery.querySelector('[data-gallery-caption]');
  const counter=gallery.querySelector('[data-gallery-counter]');
  const announcement=gallery.querySelector('[data-gallery-announcement]');
  let current=0;
  const show=(index,announce=true)=>{
   current=(index+slides.length)%slides.length;
   slides.forEach((slide,i)=>{slide.hidden=i!==current;});
   dots.forEach((dot,i)=>{dot.setAttribute('aria-pressed',String(i===current));});
   if(caption)caption.textContent=slides[current].dataset.caption;
   if(counter)counter.textContent=String(current+1).padStart(2,'0')+' / '+String(slides.length).padStart(2,'0');
   if(announce&&announcement)announcement.textContent=`${current+1} of ${slides.length}: ${slides[current].dataset.title}`;
  };
  gallery.querySelectorAll('[data-gallery-step]').forEach(button=>{
   button.addEventListener('click',()=>show(current+Number(button.dataset.galleryStep)));
  });
  dots.forEach(button=>button.addEventListener('click',()=>show(Number(button.dataset.galleryIndex))));
  gallery.addEventListener('keydown',event=>{
   if(event.key==='ArrowLeft'||event.key==='ArrowRight'){
    event.preventDefault();show(current+(event.key==='ArrowRight'?1:-1));
   }else if(event.key==='Home'||event.key==='End'){
    event.preventDefault();show(event.key==='Home'?0:slides.length-1);
   }
  });
  let start=null;
  gallery.addEventListener('pointerdown',event=>{
   if(event.pointerType==='touch'&&!event.target.closest('button'))start={x:event.clientX,y:event.clientY};
  });
  gallery.addEventListener('pointerup',event=>{
   if(!start)return;
   const dx=event.clientX-start.x,dy=event.clientY-start.y;start=null;
   if(Math.abs(dx)>50&&Math.abs(dx)>Math.abs(dy)*1.5)show(current+(dx<0?1:-1));
  });
  gallery.addEventListener('pointercancel',()=>{start=null;});
  gallery.querySelectorAll('[data-gallery-controls]').forEach(controls=>{controls.hidden=false;});
  show(0,false);
 });
}
initializeRecognitionGalleries();
