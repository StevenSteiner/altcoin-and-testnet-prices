<a href="./"><img src="static/altquick-wordmark-364x64.png" alt="AltQuick" height="32"></a>

[All markets](./) · [Why testnet markets](testnet-markets.md) · [Developers](developers.md) · [Monthly reports](reports/) · [Press kit](press.md) · [altquick.com](https://altquick.com/)

# Developer guide: buy signet and testnet coins with an API

Get test coins in bulk and read live market data without any API key.

## Getting test coins

1. Create a free account on [altquick.com](https://altquick.com/) and deposit a little Bitcoin.
2. Buy on the [signet](bitcoin-signet/), [testnet4](bitcoin-testnet4/) or [testnet3](bitcoin-testnet3/) market.
3. Withdraw to any testnet wallet. Withdrawals are instant, with no faucet drip limits.

For market orders without an account, see the [AltQuick Swap API](https://github.com/AltQuick-com/api/blob/master/swap-api.md).

## Public market data

```
# every market and its trading rules
curl "https://altquick.com/api/v1/exchangeInfo"

# 24-hour stats for all markets
curl "https://altquick.com/api/v1/ticker/24hr"

# signet order book and recent trades
curl "https://altquick.com/api/v1/depth?market=BTC_SBTC&limit=20"
curl "https://altquick.com/api/v1/trades?market=BTC_SBTC&limit=50"
```

## Python

```python
import json, urllib.request
url = "https://altquick.com/api/v1/trades?market=BTC_SBTC&limit=50"
for t in json.load(urllib.request.urlopen(url)):
    print(t["timestamp"], t["side"], t["price"], t["quantity"])
```

Full reference, including signed trading endpoints: [github.com/AltQuick-com/api](https://github.com/AltQuick-com/api).


---

AltQuick, US-based since 2015. [altquick.com](https://altquick.com/) · [API docs](https://github.com/AltQuick-com/api) · hello@altquick.com
