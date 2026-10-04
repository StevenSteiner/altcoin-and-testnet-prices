<a href="../"><img src="../static/altquick-wordmark-364x64.png" alt="AltQuick" height="32"></a>

[All markets](../) · [Why testnet markets](../testnet-markets.md) · [Developers](../developers.md) · [Monthly reports](../reports/) · [Press kit](../press.md) · [altquick.com](https://altquick.com/)

# How to get Bitcoin testnet4 coins

Testnet4 is Bitcoin's newest public test network (BIP 94), the replacement for testnet3.

## Option 1: a faucet

Faucets hand out free Testnet4 coins, usually a small amount at a time with captchas, waits or daily limits. That's enough for a first test transaction.

## Option 2: buy them on AltQuick

When you need more than a faucet gives, for example to open Lightning channels, run load tests or keep CI funded, you can buy Testnet4 coins for a tiny amount of Bitcoin.

1. Create a free account on [altquick.com](https://altquick.com/) and deposit a little Bitcoin.
2. Open the [TBTC4/BTC market](https://altquick.com/market/bitcoin-testnet4-bitcoin/) and place a buy order. The order book below shows current prices.
3. Withdraw to your Testnet4 wallet address. Withdrawals are instant, with no faucet drip limits.

Finished testing? Sell the spare coins back on the same market so the next developer can use them.

**[Open the TBTC4/BTC market on AltQuick →](https://altquick.com/market/bitcoin-testnet4-bitcoin/)**

## Live TBTC4/BTC numbers

| | |
|---|---|
| Last price | 0.00000004 BTC |
| Best bid / ask | 0.00000003 / 0.00000004 BTC |
| Trades, last 7 days | 6 |
| Volume, last 7 days | 0.00000187 BTC |
| Last trade | 2026-10-03 02:32 UTC |

## Recent trades

| Time (UTC) | Side | Price (BTC) | Amount (TBTC4) |
|---|---|---|---|
| 2026-10-03 02:32 | buy | 0.00000004 | 5.00000000 |
| 2026-10-02 14:45 | sell | 0.00000003 | 7.00000000 |
| 2026-09-28 17:22 | buy | 0.00000004 | 21.00000000 |
| 2026-09-28 05:12 | sell | 0.00000003 | 7.32333333 |
| 2026-09-28 05:12 | sell | 0.00000003 | 13.66666667 |
| 2026-09-27 16:11 | buy | 0.00000005 | 1.00000001 |
| 2026-09-25 14:36 | buy | 0.00000005 | 2.00000000 |
| 2026-09-21 17:51 | buy | 0.00000005 | 97.00000000 |
| 2026-09-20 22:39 | buy | 0.00000005 | 50.00000000 |
| 2026-09-20 18:48 | buy | 0.00000005 | 4.20000000 |

## Get this data yourself

```
curl "https://altquick.com/api/v1/trades?market=BTC_TBTC4&limit=20"
curl "https://altquick.com/api/v1/depth?market=BTC_TBTC4&limit=20"
curl "https://altquick.com/api/v1/klines?market=BTC_TBTC4&interval=1d&limit=90"
```

[See every AltQuick market](../)

Last updated: 2026-10-04 10:43 UTC from AltQuick's public API.

---

AltQuick, US-based since 2015. [altquick.com](https://altquick.com/) · [API docs](https://github.com/AltQuick-com/api) · hello@altquick.com
