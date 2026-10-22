#!/bin/bash
cd /workspace/diler-consult/assets && C=css/plugins; { cat fonts/fonts.css; cat $C/bootstrap.min.css; sed "s#\.\./webfonts#/assets/fa/webfonts#g" fa/css/all.min.css; for f in $C/nice-select.css $C/owl.carousel.min.css $C/aos-cdn.css $C/mobile.css css/typography.css css/master.css $C/responsive.css css/diler.css; do sed -E "s#url\(([\"']?)(\.\./)+images#url(\1/assets/images#g" $f; echo; done; } > /tmp/all.css
python3 -c "import re;p='/tmp/all.css';s=open(p).read();s=re.sub(r'@font-face\\s*{[^}]*fa-brands[^}]*}','',s);open(p,'w').write(s)"
sed -i "s/font-display:block/font-display:swap/g" /tmp/all.css
sed -i "s/color: rgb(252,118,50) background-image/color: rgb(252,118,50); background-image/" /tmp/all.css
cd /workspace/consult/purge && node purge.mjs && npx cleancss -O1 -o /workspace/diler-consult/assets/css/site.min.css /tmp/purged.css
cd /workspace/diler-consult && INNER=$(find . -name '*.html' ! -path './index.html' ! -path './_gen/*' ! -path './assets/*' | sed 's#^\.#/workspace/diler-consult#' | paste -sd,)
cd /workspace/consult/purge && PC=/workspace/diler-consult/index.html PO=/tmp/p_home.css node purge2.mjs && PC=$INNER PO=/tmp/p_inner.css node purge2.mjs && npx cleancss -O1 -o /workspace/diler-consult/assets/css/home.min.css /tmp/p_home.css && npx cleancss -O1 -o /workspace/diler-consult/assets/css/inner.min.css /tmp/p_inner.css
