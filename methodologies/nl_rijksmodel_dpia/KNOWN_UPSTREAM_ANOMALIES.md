# Known upstream anomalies — Dutch Government pre-scan adapter

Pinned upstream: `MinBZK/par-dpia-form@d8d690989da03287b8879ba1319f78ca8a404bd5`

## `0.4.1` reference in international-transfer score

The `internationale_doorgifte` calculation in `sources/prescan.yaml` references `answers('0.4.1')`.

In the pinned pre-scan 2.0 definition, the legal-basis question is ID `0.4`; no pre-scan field with ID `0.4.1` was identified.

SolidPrivacy therefore does **not** claim byte-for-byte runtime parity for this score component. The adapter uses a documented normalized interpretation based on:

- whether a transfer outside the EEA is indicated;
- whether storage/support is outside the EEA; and
- whether special-category data is part of the transfer.

This normalization affects only the official-methodology risk-score representation. It does not create a binding legal conclusion. International-transfer legal conclusions must use dedicated transfer-law sources and human review.

If the upstream project corrects or explains this reference, this adapter and its regression fixtures must be re-evaluated against the newly pinned commit.
