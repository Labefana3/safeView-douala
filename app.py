from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse, RedirectResponse
import uvicorn, json, os, re
from datetime import datetime, timedelta
from pathlib import Path

app = FastAPI()
MTN="673871381"
ORANGE="658230809"
CLIENTS_FILE="clients.json"
RECORDINGS_DIR=Path("recordings")
RECORDINGS_DIR.mkdir(exist_ok=True)

PLANS={
    "basic": {"nom":"BASIC","jours":3,"prix":"15,000 FCFA","desc":"3 jours"},
    "pro": {"nom":"PRO","jours":7,"prix":"25,000 FCFA","desc":"7 jours"},
    "vip": {"nom":"VIP","jours":30,"prix":"40,000 FCFA","desc":"30 jours"},
}

def slugify(t): return re.sub(r'[^a-z0-9]+','_',t.lower().strip()).strip('_')
def load_clients(): return json.load(open(CLIENTS_FILE,"r",encoding="utf-8")) if os.path.exists(CLIENTS_FILE) else {}
def save_clients(d):
    with open(CLIENTS_FILE,"w",encoding="utf-8") as f:
        json.dump(d,f,indent=2,ensure_ascii=False)

STYLE = """
    *{box-sizing:border-box} body{margin:0;background:#08080a;color:white;font-family:Arial,sans-serif}
 .navbar{background:#101010;border-bottom:1px solid #222;padding:16px 30px;display:flex;justify-content:space-between;align-items:center;position:sticky;top:0;z-index:10}
 .logo{font-weight:800;font-size:20px}.logo span{color:#ff7900}
 .nav-links{display:flex;gap:22px;color:#aaa;font-size:13px}
 .hero{text-align:center;padding:40px 20px 20px}
 .cam-circle{width:160px;height:160px;margin:0 auto 30px;background:radial-gradient(circle,#ff8a1a 0%,#ff6a00 40%,#c44a00 100%);border-radius:50%;display:flex;align-items:center;justify-content:center;box-shadow:0 0 40px rgba(255,121,0,.9),0 0 80px rgba(255,121,0,.5);animation:glow 2s ease-in-out infinite alternate;font-size:70px}
    @keyframes glow{from{box-shadow:0 0 40px rgba(255,121,0,.9)} to{box-shadow:0 0 60px rgba(255,121,0,1)}}
    h1{font-size:42px;margin:10px 0;font-weight:800;line-height:1.1} h1 span{color:#ffcc00}
 .sub{color:#9a9a9a;font-size:18px;margin-bottom:40px}
 .pricing{max-width:1150px;margin:0 auto;display:grid;grid-template-columns:1fr 1fr 1fr;gap:22px;padding:0 20px}
 .card{background:#121214;border:1px solid #2a2a2e;border-radius:14px;padding:22px;text-align:left;position:relative;cursor:pointer;transition:0.2s}
 .card:hover{transform:translateY(-5px);border-color:#ff7900;box-shadow:0 10px 30px rgba(255,121,0,.3)}
 .card.popular{border:2.5px solid #ff7900;box-shadow:0 0 30px rgba(255,121,0,.35);transform:scale(1.04)}
 .card.popular:hover{transform:scale(1.05) translateY(-5px)}
 .badge{position:absolute;top:-12px;left:50%;transform:translateX(-50%);background:#ff7900;color:white;padding:4px 14px;border-radius:20px;font-size:11px;font-weight:bold}
 .card-title{font-size:12px;color:#aaa;letter-spacing:1px}
 .card-price{font-size:34px;font-weight:800;margin:6px 0}
 .card-desc{font-size:13px;color:#888;margin-bottom:16px}
 .feat{font-size:13px;margin:7px 0;display:flex;gap:8px}
 .feat::before{content:"✅";font-size:11px}
 .choose{margin-top:15px;background:#1e1e21;padding:10px;border-radius:8px;text-align:center;color:#ff7900;font-weight:bold}
 .choose-pop{background:#ff7900;color:white}
 .btn{display:inline-block;padding:16px 28px;border-radius:10px;font-weight:700;text-decoration:none;margin:8px;font-size:15px}
 .btn-green{background:#00c853;color:white}.btn-blue{background:#1e88ff;color:white}
 .cta{text-align:center;margin:40px 0 20px}
 .footer{text-align:center;color:#555;font-size:12px;padding-bottom:30px}
    @media(max-width:800px){.pricing{grid-template-columns:1fr}.card.popular{transform:scale(1)}.card.popular:hover{transform:translateY(-5px)} h1{font-size:28px}}
    @keyframes blink{0%{opacity:1}50%{opacity:0}100%{opacity:1}}.rec{animation:blink 1s infinite;color:red}
"""

@app.get("/", response_class=HTMLResponse)
def home():
    return f"""
    <html><head><meta name='viewport' content='width=device-width, initial-scale=1'><style>{STYLE}</style></head><body>
    <div class='navbar'><div class='logo'>🛡️ Safe<span>View</span></div><div class='nav-links'><span>Tarifs</span><span style='color:white;border:1px solid #333;padding:6px 12px;border-radius:20px'>Se connecter</span></div></div>
    <div class='hero'>
        <div class='cam-circle'>📹</div>
        <h1>Sécurisez votre boutique à <span>Douala</span></h1>
        <div class='sub'>Surveillance 24h/24 pour commerçants - Cliquez sur un plan 👇</div>
    </div>
    <div class='pricing'>
        <div class='card' onclick="window.location.href='/register?plan=basic'">
            <div class='card-title'>BASIC</div>
            <div class='card-price'>15,000 FCFA</div>
            <div class='card-desc'>3 jours sauvés</div>
            <div class='feat'>3 caméras connectées</div>
            <div class='feat'>Notifications SMS</div>
            <div class='feat'>Support email 9h-18h</div>
            <div class='feat'>Stockage cloud 24h</div>
            <div class='choose'>👉 Choisir BASIC</div>
        </div>
        <div class='card popular' onclick="window.location.href='/register?plan=pro'">
            <div class='badge'>Most Popular</div>
            <div class='card-title'>PRO</div>
            <div class='card-price'>25,000 FCFA</div>
            <div class='card-desc'>7 jours sauvés</div>
            <div class='feat'>5 caméras connectées</div>
            <div class='feat'>Notifications temps réel</div>
            <div class='feat'>Stockage cloud 7 jours</div>
            <div class='feat'>Alertes IA intelligentes</div>
            <div class='feat'>Support prioritaire</div>
            <div class='choose choose-pop'>👉 Choisir PRO</div>
        </div>
        <div class='card' onclick="window.location.href='/register?plan=vip'">
            <div class='card-title'>VIP</div>
            <div class='card-price'>40,000 FCFA</div>
            <div class='card-desc'>30 jours sauvés</div>
            <div class='feat'>10 caméras connectées</div>
            <div class='feat'>Stockage cloud 30 jours</div>
            <div class='feat'>Monitoring 24/7 dédié</div>
            <div class='feat'>Tableau de bord personnalisé</div>
            <div class='feat'>Assistance dédiée</div>
            <div class='choose'>👉 Choisir VIP</div>
        </div>
    </div>
    <div class='cta'>
        <a class='btn btn-green' href='/register?plan=basic'>Créer mon compte boutique</a>
        <a class='btn btn-blue' href='/login'>Demander une démo</a>
    </div>
    <div class='footer'>Paiement sécurisé Mobile Money • Orange Money • MTN<br>MoMo {MTN} | OM {ORANGE} • <a href='/admin' style='color:#ff7900'>Admin</a></div>
    </body></html>
    """

@app.get("/register", response_class=HTMLResponse)
def reg(plan: str = "basic"):
    sel_b = "selected" if plan=="basic" else ""
    sel_p = "selected" if plan=="pro" else ""
    sel_v = "selected" if plan=="vip" else ""
    plan_obj = PLANS.get(plan, PLANS["basic"])
    return f"<html><head><meta name='viewport' content='width=device-width, initial-scale=1'><style>{STYLE}.box{{max-width:450px;margin:40px auto;background:#121214;padding:30px;border-radius:14px;border:1px solid #222}} input,select{{width:100%;padding:12px;margin:8px 0;border-radius:8px;border:1px solid #333;background:#1e1e21;color:white}}.btn{{display:block;width:100%;text-align:center;border:none;cursor:pointer}}</style></head><body><div class='navbar'><div class='logo'>🛡️ Safe<span>View</span></div></div><div class='box'><h2 style='text-align:center'>Inscription<br><span style='color:#ff7900'>{plan_obj['nom']} - {plan_obj['prix']} - {plan_obj['jours']} jours</span></h2><form method='post' action='/register'><input name='name' placeholder='Nom boutique ex: Quincaillerie Akwa' required><input name='whatsapp' placeholder='WhatsApp' required><select name='plan'><option value='basic' {sel_b}>BASIC 15K - 3 jours sauvés</option><option value='pro' {sel_p}>PRO 25K - 7 jours (Populaire)</option><option value='vip' {sel_v}>VIP 40K - 30 jours</option></select><input name='password' type='password' placeholder='Mot de passe' required><button class='btn btn-green'>Créer mon compte {plan_obj['nom']}</button></form><a href='/' style='display:block;text-align:center;color:#666;margin-top:12px;text-decoration:none'>← Retour</a></div></body></html>"

@app.post("/register")
def register(name: str = Form(...), whatsapp: str = Form(...), plan: str = Form(...), password: str = Form(...)):
    clients=load_clients(); cid=slugify(name) or f"b_{len(clients)+1}"
    if cid in clients: cid=f"{cid}_{len(clients)+1}"
    clients[cid]={"name":name,"whatsapp":whatsapp,"password":password,"active":False,"plan":plan}
    save_clients(clients); (RECORDINGS_DIR/cid).mkdir(exist_ok=True)
    return RedirectResponse(f"/client/{cid}",303)

@app.get("/login", response_class=HTMLResponse)
def login_p():
    return f"<html><head><meta name='viewport' content='width=device-width, initial-scale=1'><style>{STYLE}.box{{max-width:450px;margin:40px auto;background:#121214;padding:30px;border-radius:14px;border:1px solid #222}} input{{width:100%;padding:12px;margin:8px 0;border-radius:8px;border:1px solid #333;background:#1e1e21;color:white}}</style></head><body><div class='navbar'><div class='logo'>SafeView</div></div><div class='box'><h2>Connexion</h2><form method='post' action='/login'><input name='client_id' placeholder='ID boutique' required><input name='password' type='password' placeholder='Mot de passe' required><button class='btn btn-blue' style='width:100%;border:none'>Se connecter</button></form></div></body></html>"

@app.post("/login")
def login(client_id: str = Form(...), password: str = Form(...)):
    c=load_clients().get(client_id)
    if not c or c["password"]!=password: return HTMLResponse("Mauvais ID",401)
    return RedirectResponse(f"/client/{client_id}",303)

@app.get("/client/{client_id}", response_class=HTMLResponse)
def client_page(client_id: str):
    clients=load_clients(); c=clients.get(client_id)
    if not c: return HTMLResponse("Introuvable",404)
    plan=PLANS.get(c.get("plan","basic"),PLANS["basic"])
    exp=(datetime.now()+timedelta(days=plan["jours"])).strftime("%d/%m/%Y")
    if not c["active"]:
        return HTMLResponse(f"<body style='background:#08080a;color:white;text-align:center;padding:40px;font-family:Arial'><h1 style='color:#ff7900'>🔒 Paiement {plan['prix']} requis</h1><p>{plan['nom']} - {plan['jours']} jours sauvés</p><p>MoMo: {MTN}</p></body>")
    return HTMLResponse(f"<html><head><meta name='viewport' content='width=device-width, initial-scale=1'><style>{STYLE}.video{{max-width:900px;margin:20px auto;background:#000;border:2px solid #ff7900;border-radius:12px;height:420px;position:relative;overflow:hidden}}.bg{{width:100%;height:100%;background:linear-gradient(45deg,#111 25%,#1a1a1a 25%);background-size:40px 40px;display:flex;align-items:center;justify-content:center;flex-direction:column;animation:slide 2s linear infinite}} @keyframes slide{{to{{background-position:40px 40px}}}}</style></head><body><div class='navbar'><div class='logo'>SafeView LIVE</div><div style='color:#00c853'>● {plan['nom']} {plan['jours']}j</div></div><div style='padding:20px;max-width:900px;margin:auto'><h2>{c['name']} - <span style='color:#00c853'>LIVE</span></h2><div class='video'><div class='bg'><div style='font-size:60px'>📹</div><div style='color:#ff7900'>CAM 01</div><div id='t' style='color:#888;font-size:12px'></div></div><div style='position:absolute;top:10px;left:10px;background:rgba(0,0,0,.7);padding:6px 10px;border-radius:6px'><span class='rec'>● REC</span> <span id='clock'></span></div><div style='position:absolute;top:10px;right:10px;background:rgba(0,0,0,.7);padding:6px 10px;border-radius:6px;font-size:12px'>🔴 {plan['jours']} JOURS SAUVÉS</div><div style='position:absolute;bottom:10px;left:10px;background:rgba(0,0,0,.7);padding:6px 10px;border-radius:6px;font-size:11px'>Jusqu'au {exp} • Auto-efface après {plan['jours']}j</div></div></div><script>function u(){{const n=new Date();document.getElementById('clock').textContent=n.toLocaleTimeString('fr-FR');document.getElementById('t').textContent=n.toLocaleString('fr-FR');}}setInterval(u,1000);u();</script></body></html>")

@app.get("/admin", response_class=HTMLResponse)
def admin():
    clients=load_clients()
    html=f"<html><head><meta name='viewport' content='width=device-width, initial-scale=1'><style>{STYLE}.wrap{{max-width:900px;margin:auto;padding:20px}}.box{{background:#121214;padding:20px;border-radius:12px;border:1px solid #ff7900;margin-bottom:20px}} input,select{{width:100%;padding:10px;margin:6px 0;border-radius:8px;border:1px solid #333;background:#1e1e21;color:white}}</style></head><body><div class='navbar'><div class='logo'>ADMIN</div></div><div class='wrap'><div class='box'><h3 style='color:#ff7900'>➕ Créer boutique</h3><form method='post' action='/admin/create'><input name='name' placeholder='Nom' required><input name='whatsapp' placeholder='WhatsApp' required><select name='plan'><option value='basic'>BASIC 15K - 3j</option><option value='pro'>PRO 25K - 7j</option><option value='vip'>VIP 40K - 30j</option></select><button class='btn btn-green' style='width:100%;border:none'>Créer & Activer</button></form></div>"
    for cid,c in clients.items():
        plan=PLANS.get(c.get("plan","basic"),PLANS["basic"])
        html+=f"<div style='background:#121214;border:1px solid #222;padding:12px;margin:8px 0;border-radius:10px'>{c['name']} ({cid}) - {plan['nom']} {plan['jours']}j - Pass: {c['password']} <a href='/client/{cid}' style='color:#ff7900'>LIVE</a></div>"
    return HTMLResponse(html+"</div></body></html>")

@app.post("/admin/create")
def ac(name: str = Form(...), whatsapp: str = Form(...), plan: str = Form("basic")):
    clients=load_clients(); cid=slugify(name) or f"b_{len(clients)+1}"
    if cid in clients: cid=f"{cid}_{len(clients)+1}"
    clients[cid]={"name":name,"whatsapp":whatsapp,"password":"demo123","active":True,"plan":plan}
    save_clients(clients); (RECORDINGS_DIR/cid).mkdir(exist_ok=True)
    return RedirectResponse("/admin",303)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
