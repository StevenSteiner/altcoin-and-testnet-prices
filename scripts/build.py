#!/usr/bin/env python3
"""Builds the AltQuick market guides as GitHub-flavored Markdown (README.md at the root plus one
folder per market) from AltQuick's public API, so the pages render directly on github.com.
Run: python3 scripts/build.py   (no dependencies beyond the standard library)"""
import json, os, glob, shutil, urllib.request, datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPO_URL = "https://github.com/StevenSteiner/altcoin-and-testnet-prices"
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
    mkt = f"[{sym}/BTC market](https://altquick.com/market/{slug}-bitcoin/)"
    if sym in GUIDE_TITLE:
        net = name.replace("Bitcoin ", "")
        return f"""## Option 1: a faucet

Faucets hand out free {net} coins, usually a small amount at a time with captchas, waits or daily limits. That's enough for a first test transaction.

## Option 2: buy them on AltQuick

When you need more than a faucet gives, for example to open Lightning channels, run load tests or keep CI funded, you can buy {net} coins for a tiny amount of Bitcoin.

1. Create a free account on [altquick.com](https://altquick.com/) and deposit a little Bitcoin.
2. Open the {mkt} and place a buy order. The order book below shows current prices.
3. Withdraw to your {net} wallet address. Withdrawals are instant, with no faucet drip limits.

Finished testing? Sell the spare coins back on the same market so the next developer can use them."""
    return f"""## How to buy {name} with Bitcoin

1. Create a free account on [altquick.com](https://altquick.com/) and deposit Bitcoin.
2. Open the {mkt}, check the order book, and place a limit or market order.
3. Withdraw {sym} to your own wallet, or keep it on AltQuick to trade later.

To sell, deposit {sym} and place a sell order on the same market to receive Bitcoin."""

COINS = json.load(open(os.path.join(ROOT, "data", "coins.json")))
DAY = 86400000
STAMP = "Last updated:"   # scripts/refresh.sh ignores lines containing this when deciding whether to commit

def get(path):
    req = urllib.request.Request(API + path, headers={"User-Agent": "altquick-info-site"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)

def f8(x):
    try: return f"{float(x):.8f}"
    except Exception: return "-"

def utc(ms, fmt="%Y-%m-%d %H:%M"):
    return datetime.datetime.fromtimestamp(ms / 1000, datetime.timezone.utc).strftime(fmt)

def nav(up):
    return (f'<a href="{up or "./"}"><img src="{up}static/altquick-wordmark-364x64.png" alt="AltQuick" height="32"></a>\n\n'
            f"[All markets]({up or './'}) · [Why testnet markets]({up}testnet-markets.md) · [Developers]({up}developers.md) · "
            f"[Monthly reports]({up}reports/) · [Press kit]({up}press.md) · [altquick.com](https://altquick.com/)\n\n")

FOOT = "\n\n---\n\nAltQuick, US-based since 2015. [altquick.com](https://altquick.com/) · [API docs](https://github.com/AltQuick-com/api) · hello@altquick.com\n"

def write(rel, text):
    p = os.path.join(ROOT, rel); os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, "w").write(text)

def activity(trades, t, now_ms):
    """Recent activity computed from /api/v1/trades (the 24h ticker count/volume fields are stale)."""
    wk = [x for x in trades if x["timestamp"] >= now_ms - 7 * DAY]
    vol = sum(float(x["price"]) * float(x["quantity"]) for x in wk)
    capped = len(trades) >= 1000 and len(wk) == len(trades)
    try: wq = float(t.get("weeklyQuoteVolume"))
    except Exception: wq = None
    if wq is not None and not capped and abs(wq - vol) <= max(0.05 * vol, 1e-8): vol = wq
    last = max((x["timestamp"] for x in trades), default=None)
    return {"n7": f"{len(wk)}{'+' if capped else ''}", "v7": vol, "last": last}

def sparkline(sym, closes, w=640, h=140, pad=8):
    vals = [float(c) for c in closes]
    if len(vals) < 2: return ""
    lo, hi = min(vals), max(vals); rng = (hi - lo) or 1
    pts = " ".join(f"{pad + i * (w - 2 * pad) / (len(vals) - 1):.1f},{(h - pad - (v - lo) / rng * (h - 2 * pad)) if hi > lo else h / 2:.1f}" for i, v in enumerate(vals))
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" font-family="sans-serif">'
            f'<title>{sym}/BTC daily close, last {len(vals)} days</title>'
            f'<rect x="0" y="0" width="{w}" height="{h}" fill="#fafbfc" stroke="#e3e6ea"/>'
            f'<polyline fill="none" stroke="#f7931a" stroke-width="2" points="{pts}"/>'
            f'<text x="{pad}" y="16" font-size="12" fill="#6b7280">{sym}/BTC, {len(vals)} days</text>'
            f'<text x="{w - pad}" y="16" text-anchor="end" font-size="12" fill="#6b7280">high {hi:.8f}</text>'
            f'<text x="{w - pad}" y="{h - 12}" text-anchor="end" font-size="12" fill="#6b7280">low {lo:.8f}</text></svg>\n')

def pct(a, b):
    try:
        a, b = float(a), float(b)
        return f"{(b - a) / a * 100:+.1f}%" if a else "-"
    except Exception: return "-"

def history(sym, slug, kl):
    if not kl: return "## Price history\n\nNo price history is available for this market yet.\n"
    closes = [k[4] for k in kl]
    write(f"{slug}/price-90d.svg", sparkline(sym, closes))
    rows = "\n".join(f"| {utc(k[0], '%Y-%m-%d')} | {f8(k[4])} | {f8(k[2])} | {f8(k[3])} | {float(k[5]):g} |" for k in reversed(kl[-30:]))
    hi = max(float(c) for c in closes); lo = min(float(c) for c in closes)
    ch30 = pct(closes[-31] if len(closes) > 30 else closes[0], closes[-1])
    return f"""## {sym}/BTC price history, last {len(kl)} days

![{sym}/BTC daily closing price, last {len(kl)} days](price-90d.svg)

| | |
|---|---|
| Change, 30 days | {ch30} |
| Change, {len(kl)} days | {pct(closes[0], closes[-1])} |
| Highest daily close | {hi:.8f} BTC |
| Lowest daily close | {lo:.8f} BTC |

Daily candles from AltQuick's klines API, UTC days. On days without trades the previous close carries forward.

<details open><summary>Daily closes, last 30 days</summary>

| Date (UTC) | Close (BTC) | High | Low | Volume ({sym}) |
|---|---|---|---|---|
{rows}

</details>
"""

def book(sym, d):
    bids, asks = (d or {}).get("bids", [])[:5], (d or {}).get("asks", [])[:5]
    n = max(len(bids), len(asks))
    if not n: return "## Order book snapshot\n\nThe order book is empty right now.\n"
    cell = lambda rows, i: (f"{f8(rows[i]['price'])} | {float(rows[i]['quantity']):g}" if i < len(rows) else " | ")
    rows = "\n".join(f"| {cell(bids, i)} | {cell(asks, i)} |" for i in range(n))
    return f"""## Order book snapshot

Top {n} bids (buy orders) and asks (sell orders).

| Bid price (BTC) | Bid amount ({sym}) | Ask price (BTC) | Ask amount ({sym}) |
|---|---|---|---|
{rows}
"""

def stats(sym, t, act):
    last = utc(act["last"]) + " UTC" if act["last"] else "none recorded"
    return f"""## Live {sym}/BTC numbers

| | |
|---|---|
| Last price | {f8(t.get('lastPrice'))} BTC |
| Best bid / ask | {f8(t.get('bidPrice'))} / {f8(t.get('askPrice'))} BTC |
| Trades, last 7 days | {act['n7']} |
| Volume, last 7 days | {act['v7']:.8f} BTC |
| Last trade | {last} |
"""

def recent_trades(sym, trades):
    recent = sorted(trades, key=lambda x: -x["timestamp"])[:10]
    rows = "\n".join(f"| {utc(x['timestamp'])} | {x['side']} | {f8(x['price'])} | {f8(x['quantity'])} |" for x in recent) or "| No recent trades | | | |"
    return f"## Recent trades\n\n| Time (UTC) | Side | Price (BTC) | Amount ({sym}) |\n|---|---|---|---|\n{rows}\n"

def api_block(mk):
    return f"""## Get this data yourself

```
curl "https://altquick.com/api/v1/trades?market={mk}&limit=20"
curl "https://altquick.com/api/v1/depth?market={mk}&limit=20"
curl "https://altquick.com/api/v1/klines?market={mk}&interval=1d&limit=90"
```
"""

def faq_items(sym, name, c, slug):
    q = [(f"What is {name} ({sym})?", c["summary"])]
    if c.get("launched"): q.append((f"When did {name} launch?", c["launched"]))
    if c.get("consensus"): q.append((f"How is the {name} network secured?", c["consensus"]))
    q.append((f"How do I buy {name} with Bitcoin?", f"Create a free account on altquick.com, deposit Bitcoin, then place a limit or market order on the [{sym}/BTC market](https://altquick.com/market/{slug}-bitcoin/). You can withdraw {sym} to your own wallet afterwards. AltQuick's trading fee is 1%."))
    q.append((f"Where does the {sym} price on this page come from?", f"From AltQuick's public API: the last price, order book and trades of the {sym}/BTC market, and daily candles for the price history. No other exchanges are included."))
    return q

def main():
    tick = {t["market"]: t for t in get("/api/v1/ticker/24hr")}
    info = {m["symbol"]: m for m in get("/api/v1/exchangeInfo")["markets"]}
    now_dt = datetime.datetime.now(datetime.timezone.utc)
    now = now_dt.strftime("%Y-%m-%d %H:%M UTC"); now_ms = int(now_dt.timestamp() * 1000)
    rows = {"test": [], "coin": []}; files = ["README.md"]
    for sym, (name, slug, kind) in ASSETS.items():
        mk = "BTC_" + sym
        if mk not in info: continue
        shutil.rmtree(os.path.join(ROOT, slug), ignore_errors=True)
        t = tick.get(mk, {})
        trades = []
        try: trades = get(f"/api/v1/trades?market={mk}&limit=1000")
        except Exception: pass
        act = activity(trades, t, now_ms)
        btn = f"**[Open the {sym}/BTC market on AltQuick →](https://altquick.com/market/{slug}-bitcoin/)**"
        if kind == "test":
            verb = GUIDE_TITLE[sym]; summary = TEST_BLURB[sym]
            md = f"""{nav('../')}# {verb}

{summary}

{guide(sym, name, slug)}

{btn}

{stats(sym, t, act)}
{recent_trades(sym, trades)}
{api_block(mk)}
[See every AltQuick market](../)

{STAMP} {now} from AltQuick's public API."""
        else:
            c = COINS[sym]; summary = c["summary"]
            kl, dp = [], {}
            try: kl = [k for k in get(f"/api/v1/klines?market={mk}&interval=1d&limit=90") if k[0] <= now_ms][-90:]
            except Exception: pass
            try: dp = get(f"/api/v1/depth?market={mk}&limit=20")
            except Exception: pass
            facts = f"| Ticker | {sym} |\n" + "".join(f"| {k} | {c[f]} |\n" for k, f in (("Launched", "launched"), ("Consensus", "consensus")) if c.get(f))
            links = "\n".join(f"- {l}: [{u.split('//', 1)[1].rstrip('/')}]({u})" for l, u in c["links"])
            faq = "\n\n".join(f"### {q}\n\n{a}" for q, a in faq_items(sym, name, c, slug))
            rel = "\n".join(f"- [{ASSETS[r][0]} ({r})](../{ASSETS[r][1]}/): {COINS[r]['summary']}" for r in c["related"] if r in ASSETS)
            about = "\n\n".join(c["about"])
            md = f"""{nav('../')}# {name} ({sym}) price in Bitcoin and how to buy it

{summary} It trades against Bitcoin on AltQuick with a public order book and API.

{btn}

{stats(sym, t, act)}
## About {name}

| | |
|---|---|
{facts}
{about}

{'### Official links' + chr(10) + chr(10) + links if links else ''}

{history(sym, slug, kl)}
{book(sym, dp)}
{recent_trades(sym, trades)}
{guide(sym, name, slug)}

## {name} FAQ

{faq}

## Related markets

{rel}

[See every AltQuick market](../) · [{name} on altquick.com](https://altquick.com/asset/{slug}/)

{api_block(mk)}
Background facts were checked against each project's own sites and public sources. Nothing here is investment advice.

{STAMP} {now} from AltQuick's public API."""
        write(f"{slug}/README.md", md + FOOT); files.append(f"{slug}/README.md")
        last = utc(act["last"], "%Y-%m-%d") if act["last"] else "-"
        rows[kind].append(f"| [{name} ({sym})]({slug}/) | {f8(t.get('lastPrice'))} | {act['n7']} | {act['v7']:.8f} | {last} | [Trade {sym}/BTC](https://altquick.com/market/{slug}-bitcoin/) |")
    th = "| Market | Last price (BTC) | Trades, 7 days | Volume, 7 days (BTC) | Last trade (UTC) | Trade |\n|---|---|---|---|---|---|"
    coin_list = "\n".join(f"- **[{n} ({s})]({sl}/)**: {COINS[s]['summary']}" for s, (n, sl, k) in ASSETS.items() if k == "coin")
    idx = f"""{nav('')}# Buy Bitcoin signet, testnet4 and testnet3 coins + live prices for Namecoin, Gapcoin, Wownero and more on AltQuick

[AltQuick](https://altquick.com) is a US-based exchange that has run its own exchange engine since 2015. It is one of the few places where developers can buy Bitcoin **signet**, **testnet4** and **testnet3** coins in any amount, instead of waiting on faucet drips. It also keeps Bitcoin markets for older and smaller coins that most big exchanges have dropped, such as Namecoin, Gapcoin, Clamcoin, Peercoin, Wownero and Monero.

Each market below has its own page with live prices, the order book and recent trades. The coin pages also have a plain-language background write-up and a 90-day price history.

## Bitcoin test networks

{th}
{chr(10).join(rows['test'])}

Guides: [How to get signet coins](bitcoin-signet/) · [How to get testnet4 coins](bitcoin-testnet4/) · [How to get testnet3 coins](bitcoin-testnet3/) · [Why testnet coin markets exist](testnet-markets.md)

## Coin markets

{th}
{chr(10).join(rows['coin'])}

## What each coin is

{coin_list}

Trade counts and volume are computed from AltQuick's public trades API ([docs](https://github.com/AltQuick-com/api)). AltQuick's trading fee is 1%.

{STAMP} {now}

## How these pages are built

`scripts/build.py` (Python standard library only) pulls live numbers from AltQuick's public API and writes this README plus one folder per market. Coin write-ups live in `data/coins.json`, monthly reports in `data/report-YYYY-MM.json`, and the developer, press and testnet pages in `kit/`. `scripts/refresh.sh` rebuilds and pushes when the numbers change.

```
python3 scripts/build.py
```"""
    write("README.md", idx + FOOT)
    # monthly reports
    reps = sorted(glob.glob(os.path.join(ROOT, "data", "report-*.json")))
    links = []
    for rp in reps:
        r = json.load(open(rp)); rr = sorted(r["rows"], key=lambda x: -x["trades_30d"])
        tot_t = sum(x["trades_30d"] for x in rr); tot_v = sum(x["btc_vol_30d"] for x in rr)
        act_n = sum(1 for x in rr if x["trades_30d"])
        def mname(b):
            a = ASSETS.get(b)
            return f"[{a[0]} ({b})](../{a[1]}/)" if a else b
        trs = "\n".join(f"| {mname(x['base'])} | {x['trades_30d']} | {x['btc_vol_30d']:.8f} |" for x in rr if x["trades_30d"])
        b = f"{nav('../')}# AltQuick {r['label']} report\n\n{tot_t:,} trades and about {tot_v:.2f} BTC in volume across {act_n} markets.\n\n{r['note']}\n\n| Market | Trades | Volume (BTC) |\n|---|---|---|\n{trs}\n"
        write(f"reports/{r['month']}.md", b + FOOT); files.append(f"reports/{r['month']}.md")
        links.append(f"- [{r['label']}]({r['month']}.md): {tot_t:,} trades, about {tot_v:.2f} BTC")
    write("reports/README.md", f"{nav('../')}# Monthly reports\n\nMonthly AltQuick trading numbers, every market included.\n\n" + "\n".join(reversed(links)) + "\n" + FOOT); files.append("reports/README.md")
    # static kit pages: kit/<name>.md is the Markdown body
    for fp in sorted(glob.glob(os.path.join(ROOT, "kit", "*.md"))):
        name = os.path.basename(fp)
        write(name, nav("") + open(fp).read().strip() + "\n" + FOOT); files.append(name)
    print(f"built {len(files)} pages")

if __name__ == "__main__":
    main()
