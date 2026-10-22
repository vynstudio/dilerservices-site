#!/bin/bash
set -e
cd /workspace/consult/gen && python3 inner.py
bash /workspace/consult/purge/rebuild.sh >/dev/null
cd /workspace/consult/purge && node crit.mjs && node palettes.mjs
mkdir -p /workspace/diler-consult/_gen && cp /workspace/consult/gen/{build_head.py,inner.py,faq.json} /workspace/consult/purge/{rebuild.sh,crit.mjs,purge2.mjs,palettes.mjs} /workspace/consult/palettes/pal.json /workspace/consult/make.sh /workspace/diler-consult/_gen/ && rm -f /workspace/diler-consult/_gen/build.py /workspace/diler-consult/assets/css/site.min.css
