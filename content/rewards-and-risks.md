# Rewards, converting and risks

{{STATUS_BODY}}

This page explains the mechanics. It is not financial or tax advice, and it makes no statement about the value of any token.

## How rewards arise

- **Validators test every miner.** Each round (about every 2 minutes) a validator sends your miner fresh decision questions (8 for s1-fast and s1-pro, 4 for s1-lite and s1-cpu) and compares your answers with its own reference run of the same pinned model. Answers that match score; speed adds up to 20 % of a round's score. A wrong or quantised model, a modified prompt or downtime scores zero, and serious mismatches reset your score.
- **Scores become weights.** Validators submit weights for all miners; the chain combines them, weighted by validator stake (the chain's consensus method, called Yuma consensus).
- **Emission is shared by weight.** Each block the subnet's emission is split between the subnet owner, validators and miners under the chain's rules. Your miner's share follows its weight.
- **Paid in the subnet's token.** Miner rewards on netuid 92 are paid in the subnet's own token, called **alpha**, and accrue as alpha stake on your miner's hotkey, owned by your coldkey.
- **Variable, and can be zero.** Rewards depend on the number of competing miners, your score and uptime, and chain parameters that can change. A new miner starts at score 0 and its score builds up over about an hour of good rounds; no score is promised.

## How miner rewards are split {#how-miner-rewards-are-split}

Miner emissions are split between inference and competitions. From the day the competitions open (**16 October 2026, 12:00 UTC**), the split is:

- **50 %**: **Inference.** Hosting the pinned decision models, distributed by contribution (scored on correct answers and speed).
- **20 %**: **REAX Engine competition** (permanent). Make the engine that serves the model faster (open since 20 October 2026, 18:00 UTC; until an engine award is approved, its share goes to inference miners; [live queue](https://reax.co/competitions/live/)).
- **15 %**: **Use-case fine-tune track A.** Rotates every 2 weeks.
- **15 %**: **Use-case fine-tune track B.** Rotates every 2 weeks.

One generalist decision-model track is planned soon to replace the two use-case tracks; the date is to be announced. Until it opens, both tracks keep running unchanged.

Each competition is winner-takes-most with decay (similar to Affine, subnet 120). **Nothing is burned:** a competition share that nobody wins, or that has decayed, flows back to the inference miners. Use-case tracks take open-weight Jev-compatible models, evaluated on sealed items, trained on any hardware. Rules are published before a competition starts. See [How mining works on reax.co](https://reax.co/mining/).

### Inference tiers and pools

The inference part is split by hardware tier, with the average per miner in a tier at most half of the tier above:

| Tier | Pools | Share of the inference part |
|---|---|---|
| GPU | `s1-fast` 35 %, `s1-pro` 65 % of the tier | 80 % |
| Small GPU | `s1-lite` (NVIDIA ≥ 8 GB, incl. Jetson Orin) | 15 % |
| CPU | `s1-cpu` (AVX2 or ARMv8.2 CPU) | 5 % |

Inside a pool, weight = score × verified capacity, capped at the pool's target. Capacity is measured by surprise load probes that hit all UIDs of a pool at once, so many hotkeys on one machine add nothing. An empty pool passes its share to the other pools. Tiers and shares are release constants; a change needs a new release and is announced in advance. See [hardware](/hardware).

Until the competitions open, **100 %** of miner emissions goes to inference miners. The split can change. Any change is announced in advance on this site and on reax.co, with the date it takes effect. No amount is promised, and rewards can be zero.

## What you can do with earned alpha {#what-you-can-do-with-earned-alpha}

Every step below is signed by you with your coldkey (Talisman, btcli or another wallet). An agent can explain the commands; it cannot and must not sign for you.

**Keep or stake.** You can also keep your alpha staked to a validator; staked alpha takes part in validator emissions under the protocol rules. Whether you keep, stake or convert is your own decision; this is not financial or tax advice.

```bash
btcli stake list --wallet-name reax        # where your stake is
btcli stake move --wallet-name reax        # interactive: move alpha from your miner hotkey to a validator hotkey on netuid 92
```

**Convert alpha to TAO.** Unstaking swaps alpha for TAO through the subnet's liquidity pool. The amount you receive depends on the pool at that moment (price impact and slippage), and a pool fee of about 0.05 % applies (October 2026). At the time of writing there is no unbonding period. btcli shows the expected amount before you confirm and by default refuses if the price moves more than 5 % (`--tolerance`). Moving stake to another hotkey on the same subnet is not a swap.

```bash
btcli stake remove --netuid 92 --wallet-name reax --interactive   # choose the miner hotkey position and amount
btcli wallet balance --wallet-name reax                           # TAO now in your coldkey
```

**Convert TAO to euros or dollars.** Use an exchange that lists TAO and is authorised to serve customers in your country (in the EU, check the provider's MiCAR authorisation in the ESMA register). We do not recommend and are not affiliated with any exchange; examples seen listing TAO in October 2026 include Kraken, Bitvavo and Coinbase. Listings and availability change:

1. Open and verify an account at the exchange (identity check).
2. In the exchange, get your **TAO deposit address** (Bittensor network).
3. Send a small test amount first: `btcli wallet transfer --destination <deposit-address> --amount <amount> --wallet-name reax`, or "Send" in Talisman. Wait for it to arrive, then send the rest.
4. Sell TAO for EUR or USD on the exchange and withdraw to your bank account.

Costs to expect: pool slippage when unstaking, network fees, exchange trading and withdrawal fees.

**Taxes.** Mining rewards, staking rewards and later disposals can be taxable, depending on your country and situation. Keep records (dates, amounts, transaction hashes) and ask a tax adviser. For Germany, the Federal Ministry of Finance's letter on crypto assets of 6 March 2025 is the official reference ([PDF, German](https://www.bundesfinanzministerium.de/Content/DE/Downloads/BMF_Schreiben/Steuerarten/Einkommensteuer/2025-03-06-einzelfragen-kryptowerte-bmf-schreiben.pdf)).

## Risks and costs

- You pay for hardware or rent, electricity and your connection.
- Registration burns TAO and is **non-refundable**. Check the live fee before signing.
- Rewards can be low or zero: competition, downtime, chain parameter changes or a new model version (which resets scores) all affect them.
- Token exchange rates change, so the amount you receive when you convert depends on the time and on the pool. We make no statement about future value.
- Keys: whoever holds your recovery phrase controls your funds. Nobody from Decision Models or REAX will ever ask for it.

A human approves every payment. Never buy hardware or fund an account just because an agent says setup succeeded.

[Protocol and scoring](https://reax.dev/mine/) · [Agent playbook](/agent.md) · [Wallets](/wallets) · [Mining terms explained](/wallets#glossary)
