import json,sys
p="channels/yellow-bot/topic_queue.json"
raw=open(p,encoding="utf-8",newline="").read()
crlf="\r\n" in raw
q=json.loads(raw)
op=sys.argv[1]
if op=="news":
    q.append({"id":"claude-code-2-1-318-login-expiry","title":"Claude Code 2.1.318: login expiry date","url":"https://code.claude.com/docs/en/changelog.md","summary":"2.1.318 (2026-11-04) shows when a stored claude.ai sign-in ends in claude auth status and claude -p JSON, and warns 10 days before in claude -p text output.","status":"uploaded","story":"022_claude-code-login-expiry","priority":"news","org":"Anthropic"})
else:
    for it in q:
        if it["id"]==sys.argv[2]:
            it["status"]="uploaded"; it["story"]=sys.argv[3]
out=json.dumps(q,ensure_ascii=False,indent=2)
if crlf: out=out.replace("\n","\r\n")
assert json.loads(out)==q
open(p,"w",encoding="utf-8",newline="").write(out)
print("ok",len(q),"crlf",crlf)
