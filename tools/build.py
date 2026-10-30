"""Rebuild index.html from the Manchester United artifact page.
Usage: python3 tools/build.py <page.html> [repo_dir]
<page.html> is the artifact's HTML, either the source (starting with <title>)
or the published copy the Artifact tool saves (wrapped in its own <html><body>).
Also bumps the service worker cache so installed apps pick up the change."""
import sys,re,os
src=open(sys.argv[1],encoding="utf8").read()
out=sys.argv[2] if len(sys.argv)>2 else "."
if not src.lstrip().startswith("<title>"):
    src=src[src.index("<body>")+len("<body>"):]
    src=re.sub(r"</body>\s*</html>\s*$","",src.strip())
src=src.strip()
assert src.startswith("<title>"),"page should start with <title>"
i=src.index("</style>")+len("</style>")
head,body=src[:i],src[i:]
head=head.replace('<meta name="claude:viewport-fit-sides" content="cover">\n','')
page=f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="theme-color" content="#c8102e">
<meta name="description" content="Manchester United squad, transfers, managers and player stats since 2013, plus rivals' transfers.">
<link rel="manifest" href="manifest.json">
<link rel="icon" href="icon-192.png">
<link rel="apple-touch-icon" href="apple-touch-icon.png">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-title" content="United">
{head}
<style>[hidden]{{display:none!important}}</style>
</head>
<body>
{body}
<script>if('serviceWorker' in navigator){{window.addEventListener('load',()=>{{navigator.serviceWorker.register('./sw.js').catch(()=>{{}});}});}}</script>
</body>
</html>
'''
open(os.path.join(out,"index.html"),"w",encoding="utf8").write(page)
sw=os.path.join(out,"sw.js");s=open(sw,encoding="utf8").read()
s=re.sub(r"united-v(\d+)",lambda m:f"united-v{int(m.group(1))+1}",s,count=1)
open(sw,"w",encoding="utf8").write(s)
print("built index.html;",re.search(r"united-v\d+",s).group(0))
