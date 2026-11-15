# The hourly GPU price is not your agent's task budget

An agent can find a cheap GPU and still make an expensive decision. The quoted hourly rate is only one input: billing increments, environment preparation, model download time, output persistence and uncertain startup results change what a task actually costs.

Here is a small, provider-neutral way to make that decision inspectable before an agent is allowed to spend.

## 1. Represent the billing increment explicitly

Two offers can advertise the same hourly rate but bill differently. At an illustrative $0.40/hour, a 12-minute task costs $0.08 on a source that bills whole minutes, and $0.40 on one with a one-hour minimum and whole-hour increments. An early stop does not erase the agreed minimum.

Use decimal arithmetic for money, and keep the minimum separate from the increment:

```python
from decimal import Decimal, ROUND_CEILING

def estimate_compute_fee(seconds, hourly_usd, minimum_seconds, increment_seconds):
    if seconds <= 0 or minimum_seconds <= 0 or increment_seconds <= 0:
        raise ValueError("Durations and increments must be positive")
    rate = Decimal(hourly_usd)
    if not rate.is_finite() or rate < 0:
        raise ValueError("Rate must be finite and nonnegative")
    duration = Decimal(str(seconds))
    units = (duration / Decimal(increment_seconds)).to_integral_value(
        rounding=ROUND_CEILING
    )
    billed_seconds = max(Decimal(minimum_seconds), units * increment_seconds)
    return rate * billed_seconds / Decimal(3600)

print(estimate_compute_fee(720, "0.40", 60, 60))      # 0.08
print(estimate_compute_fee(720, "0.40", 3600, 3600))  # 0.40
```

This is an estimate, not an invoice. Production integrations also need the provider's actual start condition, pricing expiry and finalized ledger. Do not round away the precision the ledger uses.

## 2. Budget for preparation and persistence

A duration estimate should include environment setup and model loading, not just the compute kernel. Downloading several gigabytes can take longer than a small generation task.

A useful planning decomposition is:

```text
expected task cost =
  billed compute(setup + download + execution + output collection)
  + applicable storage
  + applicable transfer
```

Each term needs a source and a timestamp. If transfer charges or storage retention are unknown, report that uncertainty instead of silently assigning zero. Record the successful attempt separately from the total cost of development retries.

## 3. Make approval a specific contract

An account connection grants access; it is not informed approval of every future action. Before allocation, show the selected offer, minimum charge, billing increment, estimated total, hard limits, data to upload and intended output location.

Bind that approval to a current quote. If an expired quote is replaced by a different source with a different minimum charge, obtain approval for the new terms. A GPU's model name does not imply a billing policy.

## 4. Reconcile uncertain allocation instead of retrying blindly

A timeout is not proof that allocation failed. Creating another instance can leave two billable resources.

Persist the request identity and inspect the existing resource state before retrying. Use documented idempotency semantics where supported; do not assume a create endpoint is idempotent because another endpoint accepts an idempotency key. If the result remains uncertain, surface that state for reconciliation rather than spawning a replacement.

## 5. Treat output verification and release as part of success

A process exit code of zero is insufficient when the disk will disappear on termination. A task acceptance record should capture:

- Workload and dependency revisions.
- Execution status and exit code.
- Output manifest, byte counts and checksums.
- Finalized compute fees and separate storage or transfer charges.
- Resource release confirmation, including whether that confirmation came from the upstream supplier.

It is useful to expose a read-only discovery endpoint for agents that have no credentials yet. Return capabilities, billing rules, task limitations, known issues and sample sizes. If there is too little production data for a success rate, return `null` with an explanation. A failed discovery request should remain a failure, not be replaced with a cached green check.

The practical result is a better planning boundary: the agent can explain whether a workload fits before the human grants spending authority, and the final receipt describes an actual completed task rather than just an hourly price.

---
Disclosure: this article was prepared with AI assistance and checked against implemented billing and task-control behavior. The examples are illustrative and do not invoke a GPU or any paid service.
