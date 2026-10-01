#!/usr/bin/env python3
"""Builds the AltQuick public info site into ./site from AltQuick's public API.
Run: python3 scripts/build.py   (no dependencies beyond the standard library)"""
import json, os, glob, html, shutil, urllib.request, datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "docs")
BASE_URL = os.environ.get("SITE_URL", "").rstrip("/")
API = "https://altquick.com"

# symbol -> (display name, altquick.com slug, kind)
ASSETS = {
 "SBTC": ("Bitcoin Signet", "bitcoin-signet", "test"),
 "TBTC4": ("Bitcoin Testnet4", "bitcoin-testnet4", "test"),
 "TBTC": ("Bitcoin Testnet3", "bitcoin-testnet3", "test"),
 "42": ("42-coin", "42-coin", "coin"), "AVAX": ("Avalanche", "avalanche", "coin"),
 "BCH": ("Bitcoin Cash", "bitcoin-cash", "coin"), "BTC2B": ("Bitcoin Blake2b", "bitcoin-blake2b", "coin"),
 "CLAM": ("Clamcoin", "clamcoin", "coin"), "CURE": ("Curecoin", "curecoin", "coin"),
 "DASH": ("Dash", "dash", "coin"), "DGB": ("DigiByte", "digibyte", "coin"),
 "DOGE": ("Dogecoin", "dogecoin", "coin"), "FLO": ("Florincoin", "florincoin", "coin"),
 "GAP": ("Gapcoin", "gapcoin", "coin"), "LTC": ("Litecoin", "litecoin", "coin"),
 "MAZA": ("Mazacoin", "mazacoin", "coin"), "NMC": ("Namecoin", "namecoin", "coin"),
 "PART": ("Particl", "particl", "coin"), "PPC": ("Peercoin", "peercoin", "coin"),
 "QTUM": ("Qtum", "qtum", "coin"), "RHOM": ("Rhombus", "rhombus", "coin"),
 "SOL": ("Solana", "solana", "coin"), "WOW": ("Wownero", "wownero", "coin"),
 "XMR": ("Monero", "monero", "coin"), "ZEC": ("Zcash", "zcash", "coin"),
}
TEST_BLURB = {
 "SBTC": "Signet is Bitcoin's signed test network. Blocks come on a steady schedule, which makes it the most predictable network for apps, Lightning work and CI.",
 "TBTC4": "Testnet4 is Bitcoin's newest public test network (BIP 94), the replacement for testnet3.",
 "TBTC": "Testnet3 is Bitcoin's long-running public test network, still used by many wallets, explorers and tutorials.",
}

GUIDE_TITLE = {
 "SBTC": "How to get Bitcoin signet coins",
 "TBTC4": "How to get Bitcoin testnet4 coins",
 "TBTC": "How to get Bitcoin testnet3 coins",
}
def guide(sym, name, slug):
    mkt = f'<a href="https://altquick.com/market/{slug}-bitcoin/">{sym}/BTC market</a>'
    if sym in GUIDE_TITLE:
        net = name.replace("Bitcoin ", "")
        return f"""<h2>Option 1: a faucet</h2>
<p>Faucets hand out free {net} coins, usually a small amount at a time with captchas, waits or daily limits. That's enough for a first test transaction.</p>
<h2>Option 2: buy them on AltQuick</h2>
<p>When you need more than a faucet gives, for example to open Lightning channels, run load tests or keep CI funded, you can buy {net} coins for a tiny amount of Bitcoin.</p>
<ol><li>Create a free account on <a href="https://altquick.com/">altquick.com</a> and deposit a little Bitcoin.</li>
<li>Open the {mkt} and place a buy order. The order book below shows current prices.</li>
<li>Withdraw to your {net} wallet address. Withdrawals are instant, with no faucet drip limits.</li></ol>
<p>Finished testing? Sell the spare coins back on the same market so the next developer can use them.</p>"""
    return f"""<h2>How to buy {name} with Bitcoin</h2>
<ol><li>Create a free account on <a href="https://altquick.com/">altquick.com</a> and deposit Bitcoin.</li>
<li>Open the {mkt}, check the order book, and place a limit or market order.</li>
<li>Withdraw {sym} to your own wallet, or keep it on AltQuick to trade later.</li></ol>
<p>To sell, deposit {sym} and place a sell order on the same market to receive Bitcoin.</p>"""

def get(path):
    req = urllib.request.Request(API + path, headers={"User-Agent": "altquick-info-site"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)

def f8(x):
    try: return f"{float(x):.8f}"
    except Exception: return "-"

def page(title, desc, body, path, depth, index=True):
    up = "../" * depth
    canon = f'<link rel="canonical" href="{BASE_URL}/{path}">' if BASE_URL else ""
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(title)}</title><meta name="description" content="{html.escape(desc)}">{canon}
{'' if index else '<meta name="robots" content="noindex,follow">'}<link rel="stylesheet" href="{up}style.css"></head><body>
<header><a href="{up}index.html"><img src="{up}altquick-wordmark-364x64.png" alt="AltQuick" height="32"></a>
<nav><a href="{up}index.html">Markets</a><a href="{up}testnet-markets.html">Why testnet markets</a><a href="{up}developers.html">Developers</a><a href="{up}reports/index.html">Reports</a><a href="{up}press.html">Press kit</a></nav></header>
<main>{body}</main>
<footer>AltQuick, US-based since 2015. <a href="https://altquick.com/">altquick.com</a> · <a href="https://github.com/AltQuick-com/api">API docs</a> · hello@altquick.com</footer></body></html>"""

def write(rel, text):
    p = os.path.join(OUT, rel); os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, "w").write(text)

def main():
    shutil.rmtree(OUT, ignore_errors=True); os.makedirs(OUT)
    for f in glob.glob(os.path.join(ROOT, "static", "*")): shutil.copy(f, OUT)
    tick = {t["market"]: t for t in get("/api/v1/ticker/24hr")}
    info = {m["symbol"]: m for m in get("/api/v1/exchangeInfo")["markets"]}
    now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    pages = ["index.html"]
    rows = {"test": [], "coin": []}
    for sym, (name, slug, kind) in ASSETS.items():
        mk = "BTC_" + sym
        if mk not in info: continue
        t = tick.get(mk, {})
        trades = f"https://altquick.com/api/v1/trades?market={mk}&limit=20"
        recent = []
        try: recent = get(f"/api/v1/trades?market={mk}&limit=10")
        except Exception: pass
        rt = "".join(f"<tr><td>{datetime.datetime.fromtimestamp(x['timestamp']/1000, datetime.timezone.utc):%Y-%m-%d %H:%M}</td><td>{x['side']}</td><td>{f8(x['price'])}</td><td>{f8(x['quantity'])}</td></tr>" for x in recent)
        verb = GUIDE_TITLE.get(sym, f"How to buy {name} ({sym}) with Bitcoin")
        lead = TEST_BLURB.get(sym, f"{name} ({sym}) trades against Bitcoin on AltQuick with a public order book and API.")
        body = f"""<h1>{verb}</h1><p class="lead">{lead}</p>
{guide(sym, name, slug)}
<p><a class="btn" href="https://altquick.com/market/{slug}-bitcoin/">Open the {sym}/BTC market on AltQuick</a></p>
<h2>Live {sym}/BTC numbers</h2><table class="kv"><tr><th>Last price</th><td>{f8(t.get('lastPrice'))} BTC</td></tr>
<tr><th>Best bid / ask</th><td>{f8(t.get('bidPrice'))} / {f8(t.get('askPrice'))} BTC</td></tr>
<tr><th>Trades, last 24h</th><td>{t.get('count', 0)}</td></tr>
<tr><th>Volume, last 24h</th><td>{f8(t.get('quoteVolume'))} BTC</td></tr>
<tr><th>Volume, last 7 days</th><td>{f8(t.get('weeklyQuoteVolume'))} BTC</td></tr></table>
<h2>Recent trades</h2><table><tr><th>Time (UTC)</th><th>Side</th><th>Price (BTC)</th><th>Amount ({sym})</th></tr>{rt or '<tr><td colspan=4>No recent trades</td></tr>'}</table>
<h2>Get this data yourself</h2><pre>curl "{trades}"
curl "https://altquick.com/api/v1/depth?market={mk}"</pre>
<p class="muted">Updated {now} from AltQuick's public API.</p>"""
        write(f"markets/{slug}/index.html", page(f"{verb} | AltQuick guide", f"{verb}: step-by-step guide with the live {sym}/BTC price and recent trades.", body, f"markets/{slug}/", 2, index=(kind == "test")))
        if kind == "test": pages.append(f"markets/{slug}/")
        rows[kind].append(f"<tr><td><a href=\"markets/{slug}/index.html\">{name} ({sym})</a></td><td>{f8(t.get('lastPrice'))}</td><td>{t.get('count', 0)}</td><td>{f8(t.get('weeklyQuoteVolume'))}</td></tr>")
    hdr = "<tr><th>Market</th><th>Last (BTC)</th><th>Trades 24h</th><th>Volume 7d (BTC)</th></tr>"
    idx = f"""<h1>Buy Bitcoin testnet and signet coins, and trade altcoins for BTC</h1>
<p class="lead">AltQuick has run its own exchange since 2015. It is one of the few places where developers can buy signet, testnet4 and testnet3 coins in any amount, instantly, instead of waiting on faucet drips.</p>
<h2>Bitcoin test networks</h2><table>{hdr}{''.join(rows['test'])}</table>
<h2>Coin markets</h2><table>{hdr}{''.join(rows['coin'])}</table>
<p class="muted">Updated {now} from AltQuick's public API.</p>"""
    write("index.html", page("AltQuick markets: buy signet, testnet4 & testnet3 coins | AltQuick", "Live prices and volume for every AltQuick market, including Bitcoin signet, testnet4 and testnet3.", idx, "", 0))
    # monthly reports
    reps = sorted(glob.glob(os.path.join(ROOT, "data", "report-*.json")))
    links = []
    for rp in reps:
        r = json.load(open(rp)); rr = sorted(r["rows"], key=lambda x: -x["trades_30d"])
        tot_t = sum(x["trades_30d"] for x in rr); tot_v = sum(x["btc_vol_30d"] for x in rr)
        act = sum(1 for x in rr if x["trades_30d"])
        trs = "".join(f"<tr><td>{ASSETS.get(x['base'], (x['base'],))[0]} ({x['base']})</td><td>{x['trades_30d']}</td><td>{x['btc_vol_30d']:.8f}</td></tr>" for x in rr if x["trades_30d"])
        b = f"<h1>AltQuick {r['label']} report</h1><p class=lead>{tot_t:,} trades and about {tot_v:.2f} BTC in volume across {act} markets.</p><p>{html.escape(r['note'])}</p><table><tr><th>Market</th><th>Trades</th><th>Volume (BTC)</th></tr>{trs}</table>"
        write(f"reports/{r['month']}/index.html", page(f"AltQuick {r['label']} trading report", f"AltQuick {r['label']}: {tot_t:,} trades across {act} markets.", b, f"reports/{r['month']}/", 2))
        pages.append(f"reports/{r['month']}/"); links.append(f"<li><a href=\"{r['month']}/index.html\">{r['label']}</a>: {tot_t:,} trades, about {tot_v:.2f} BTC</li>")
    write("reports/index.html", page("AltQuick monthly reports", "Monthly AltQuick trading numbers, every market included.", "<h1>Monthly reports</h1><ul>" + "".join(reversed(links)) + "</ul>", "reports/", 1)); pages.append("reports/")
    # static kit pages (markdown-free HTML fragments in kit/)
    for fp in sorted(glob.glob(os.path.join(ROOT, "kit", "*.html"))):
        name = os.path.basename(fp); txt = open(fp).read()
        title, desc, body = txt.split("\n", 2)
        write(name, page(title, desc, body, name, 0)); pages.append(name)
    if BASE_URL:
        write("sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + "".join(f"<url><loc>{BASE_URL}/{p if p != 'index.html' else ''}</loc></url>" for p in pages) + "</urlset>")
        write("robots.txt", f"User-agent: *\nAllow: /\nSitemap: {BASE_URL}/sitemap.xml\n")
    print(f"built {len(pages)} pages into {OUT}")

if __name__ == "__main__":
    main()
