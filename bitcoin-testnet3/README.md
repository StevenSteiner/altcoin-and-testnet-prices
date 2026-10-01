<a href="../"><img src="../static/altquick-wordmark-364x64.png" alt="AltQuick" height="32"></a>

[All markets](../) · [Why testnet markets](../testnet-markets.md) · [Developers](../developers.md) · [Monthly reports](../reports/) · [Press kit](../press.md) · [altquick.com](https://altquick.com/)

# How to get Bitcoin testnet3 coins

Testnet3 is Bitcoin's long-running public test network, still used by many wallets, explorers and tutorials.

## Option 1: a faucet

Faucets hand out free Testnet3 coins, usually a small amount at a time with captchas, waits or daily limits. That's enough for a first test transaction.

## Option 2: buy them on AltQuick

When you need more than a faucet gives, for example to open Lightning channels, run load tests or keep CI funded, you can buy Testnet3 coins for a tiny amount of Bitcoin.

1. Create a free account on [altquick.com](https://altquick.com/) and deposit a little Bitcoin.
2. Open the [TBTC/BTC market](https://altquick.com/market/bitcoin-testnet3-bitcoin/) and place a buy order. The order book below shows current prices.
3. Withdraw to your Testnet3 wallet address. Withdrawals are instant, with no faucet drip limits.

Finished testing? Sell the spare coins back on the same market so the next developer can use them.

**[Open the TBTC/BTC market on AltQuick →](https://altquick.com/market/bitcoin-testnet3-bitcoin/)**

## Live TBTC/BTC numbers

| | |
|---|---|
| Last price | 0.00000061 BTC |
| Best bid / ask | 0.00000051 / 0.00000086 BTC |
| Trades, last 7 days | 14 |
| Volume, last 7 days | 0.00007709 BTC |
| Last trade | 2026-09-28 00:27 UTC |

## Recent trades

| Time (UTC) | Side | Price (BTC) | Amount (TBTC) |
|---|---|---|---|
| 2026-09-28 00:27 | sell | 0.00000061 | 4.07614517 |
| 2026-09-28 00:27 | sell | 0.00000064 | 10.00000000 |
| 2026-09-28 00:27 | sell | 0.00000064 | 10.00000000 |
| 2026-09-28 00:27 | sell | 0.00000064 | 10.00000000 |
| 2026-09-28 00:27 | sell | 0.00000067 | 10.00000000 |
| 2026-09-28 00:27 | sell | 0.00000067 | 10.00000000 |
| 2026-09-28 00:27 | sell | 0.00000069 | 10.00000000 |
| 2026-09-28 00:27 | sell | 0.00000069 | 10.00000000 |
| 2026-09-28 00:27 | sell | 0.00000071 | 5.00000000 |
| 2026-09-28 00:27 | sell | 0.00000071 | 0.74231423 |

## Get this data yourself

```
curl "https://altquick.com/api/v1/trades?market=BTC_TBTC&limit=20"
curl "https://altquick.com/api/v1/depth?market=BTC_TBTC&limit=20"
curl "https://altquick.com/api/v1/klines?market=BTC_TBTC&interval=1d&limit=90"
```

[See every AltQuick market](../)

Last updated: 2026-10-01 00:42 UTC from AltQuick's public API.

---

AltQuick, US-based since 2015. [altquick.com](https://altquick.com/) · [API docs](https://github.com/AltQuick-com/api) · hello@altquick.com
