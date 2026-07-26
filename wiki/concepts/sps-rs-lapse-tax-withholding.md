---
title: "SPS RS Lapse Tax Withholding (Gencash)"
type: concept
tags: [rsu, tax, schwab, gencash, equity]
date: 2026-07-24
---

# SPS RS Lapse Tax Withholding (Gencash)

## Definition & Mechanics
In equity compensation administration (specifically Charles Schwab Stock Plan Services / SPS), **SPS RS Lapse Tool** entries represent automated journal transactions ("Gencash") used to satisfy statutory tax withholding requirements upon the vesting (lapse of restrictions) of Restricted Stock Units (RSUs).

When RSUs vest:
1. Shares are released into the brokerage account (`Stock Plan Activity`).
2. A calculated portion of cash value is journaled out as a negative amount (`Journal - Gencash transaction for SPS RS Lapse Tool`) to cover federal, state, and payroll taxes.
3. The remaining net shares or net cash after sales are made available to the account owner.

## Quantitative Impact (Account XXX980, 2022-2026)
- **Total Tax Withheld via Gencash**: **$895,417.47**
- **Ratio to Gross Sales Proceeds**: Accounts for ~72.0% of gross stock sale proceeds ($895.4K tax withheld vs $1.243M gross sales).

## Related Sources & Entities
- [[individual-xxx980-transactions-20260724-173507]]
- [[schwab-individual-xxx980]]
- [[snap-inc]]
