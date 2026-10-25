import re,hashlib,base64,subprocess,sys
src,out=sys.argv[1],sys.argv[2]
s=open(src,encoding='utf-8').read()
# strip previous build artifacts so the script is repeatable
s=re.sub(r'<style id="tw">.*?</style>\s*','',s,flags=re.S)
s=re.sub(r'<meta http-equiv="Content-Security-Policy"[^>]*>\s*','',s)
s=re.sub(r'<meta name="referrer"[^>]*>\s*','',s)
s=re.sub(r'<script src="https://cdn.tailwindcss.com"></script>\s*','',s)
s=re.sub(r'<script>\s*tailwind\.config = \{.*?\};\s*</script>\s*','',s,flags=re.S)
open('src_clean.html','w',encoding='utf-8').write(s)
subprocess.run(['npx','tailwindcss','-c','tailwind.config.js','-i','in.css','-o','out.css','--minify','--content','src_clean.html'],check=True,capture_output=True)
css=open('out.css',encoding='utf-8').read()
# hash the single executable inline script
scripts=[m for m in re.finditer(r'<script([^>]*)>(.*?)</script>',s,flags=re.S) if 'ld+json' not in m.group(1) and 'src=' not in m.group(1)]
assert len(scripts)==1,len(scripts)
h=base64.b64encode(hashlib.sha256(scripts[0].group(2).encode('utf-8')).digest()).decode()
csp=("default-src 'none'; script-src 'sha256-%s'; style-src 'unsafe-inline' https://fonts.googleapis.com; "
     "font-src https://fonts.gstatic.com; img-src 'self' data:; frame-src https://calendar.google.com https://calendar.app.google; "
     "connect-src 'none'; form-action 'none'; base-uri 'none'; object-src 'none'; manifest-src 'none'")%h
head='  <meta http-equiv="Content-Security-Policy" content="%s">\n  <meta name="referrer" content="strict-origin-when-cross-origin">\n  <style id="tw">%s</style>\n'%(csp,css)
i=s.index('  <style>')
s=s[:i]+head+s[i:]
open(out,'w',encoding='utf-8').write(s)
print('built',len(s),'bytes; css',len(css))
