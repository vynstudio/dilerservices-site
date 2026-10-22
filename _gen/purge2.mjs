import {PurgeCSS} from 'purgecss'; import fs from 'fs';
const r=await new PurgeCSS().purge({
 content:[...process.env.PC.split(','),'/workspace/diler-consult/assets/js/*.js','/workspace/diler-consult/assets/js/plugins/owl.carousel.min.js','/workspace/diler-consult/assets/js/plugins/jquery.nice-select.js','/workspace/diler-consult/assets/js/plugins/aos.js','/workspace/diler-consult/assets/js/plugins/bootstrap.min.js'],
 css:['/tmp/all.css'],fontFace:true,keyframes:true,
 safelist:{standard:['sticky','active','show','open','selected','focus','disabled','collapse','collapsing','collapsed','on','mobile-menu-active','active-progress','hidden',/^owl-/,/^nice-select/,/^aos/,/^ds-/,/^accordion/,/^mobile/,/^sub-menu/,/^submenu/,/^has-sub/,/^hash/,/^option/,/^list/],greedy:[/data-aos/]}});
fs.writeFileSync(process.env.PO,r[0].css); console.log(r[0].css.length);
