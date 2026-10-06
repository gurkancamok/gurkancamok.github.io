'use strict';
const menuButton=document.querySelector('.menu-toggle');
const navigation=document.querySelector('#primary-navigation');
if(menuButton&&navigation){
 const closeMenu=()=>{navigation.classList.remove('open');menuButton.setAttribute('aria-expanded','false');menuButton.textContent='Menu';};
 menuButton.addEventListener('click',()=>{const open=menuButton.getAttribute('aria-expanded')!=='true';navigation.classList.toggle('open',open);menuButton.setAttribute('aria-expanded',String(open));menuButton.textContent=open?'Close':'Menu';});
 navigation.addEventListener('click',event=>{if(event.target.closest('a'))closeMenu();});
 document.addEventListener('keydown',event=>{if(event.key==='Escape'&&menuButton.getAttribute('aria-expanded')==='true'){closeMenu();menuButton.focus();}});
 document.addEventListener('click',event=>{if(!event.target.closest('.nav'))closeMenu();});
 window.matchMedia('(min-width:781px)').addEventListener('change',event=>{if(event.matches)closeMenu();});
}
