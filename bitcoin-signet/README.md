<a href="../"><img src="../static/altquick-wordmark-364x64.png" alt="AltQuick" height="32"></a>

[All markets](../) · [Why testnet markets](../testnet-markets.md) · [Developers](../developers.md) · [Monthly reports](../reports/) · [Press kit](../press.md) · [altquick.com](https://altquick.com/)

# How to get Bitcoin signet coins

Signet is Bitcoin's signed test network. Blocks come on a steady schedule, which makes it the most predictable network for apps, Lightning work and CI.

## Option 1: a faucet

Faucets hand out free Signet coins, usually a small amount at a time with captchas, waits or daily limits. That's enough for a first test transaction.

## Option 2: buy them on AltQuick

When you need more than a faucet gives, for example to open Lightning channels, run load tests or keep CI funded, you can buy Signet coins for a tiny amount of Bitcoin.

1. Create a free account on [altquick.com](https://altquick.com/) and deposit a little Bitcoin.
2. Open the [SBTC/BTC market](https://altquick.com/market/bitcoin-signet-bitcoin/) and place a buy order. The order book below shows current prices.
3. Withdraw to your Signet wallet address. Withdrawals are instant, with no faucet drip limits.

Finished testing? Sell the spare coins back on the same market so the next developer can use them.

**[Open the SBTC/BTC market on AltQuick →](https://altquick.com/market/bitcoin-signet-bitcoin/)**

## Live SBTC/BTC numbers

| | |
|---|---|
| Last price | 0.00000009 BTC |
| Best bid / ask | 0.00000007 / 0.00000008 BTC |
| Trades, last 7 days | 50 |
| Volume, last 7 days | 0.00013440 BTC |
| Last trade | 2026-10-02 10:04 UTC |

## Recent trades

| Time (UTC) | Side | Price (BTC) | Amount (SBTC) |
|---|---|---|---|
| 2026-10-02 10:04 | buy | 0.00000009 | 1.00000000 |
| 2026-10-02 10:04 | sell | 0.00000007 | 152.58115517 |
| 2026-10-02 02:42 | buy | 0.00000009 | 1.00000000 |
| 2026-10-02 02:41 | sell | 0.00000007 | 46.27073889 |
| 2026-10-02 02:41 | sell | 0.00000008 | 1.12500000 |
| 2026-10-02 02:41 | sell | 0.00000008 | 37.35248766 |
| 2026-10-01 15:19 | buy | 0.00000009 | 1.00000000 |
| 2026-10-01 15:19 | sell | 0.00000008 | 121.41219075 |
| 2026-10-01 04:27 | buy | 0.00000010 | 1.00000000 |
| 2026-10-01 04:27 | sell | 0.00000008 | 34.86032159 |

## Get this data yourself

```
curl "https://altquick.com/api/v1/trades?market=BTC_SBTC&limit=20"
curl "https://altquick.com/api/v1/depth?market=BTC_SBTC&limit=20"
curl "https://altquick.com/api/v1/klines?market=BTC_SBTC&interval=1d&limit=90"
```

[See every AltQuick market](../)

Last updated: 2026-10-02 22:53 UTC from AltQuick's public API.

---

AltQuick, US-based since 2015. [altquick.com](https://altquick.com/) · [API docs](https://github.com/AltQuick-com/api) · hello@altquick.com
