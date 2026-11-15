# Quote → approve → run → save → release

This is a bounded workflow with runnable small-task recipes. Installation, account connection and a completed payment do not by themselves approve a paid task.

## Discover and estimate

1. Read the anonymous [self-check](https://cloudgpu.app/v1/public/agent-self-check), [task fit documentation](https://cloudgpu.app/docs/agents), [contract](https://cloudgpu.app/agent-contract.json) and current catalog.
2. Collect minimum VRAM, GPU count, compatible environment/model licenses, input size, expected outputs and a duration including setup/download/collection. Do not assume a model fits because its file size fits the GPU.
3. Request a current estimate. The public `POST /v1/quotes` currently covers **minute-source estimates only**. It is not a stock reservation or a price guarantee. The [Compute Lab](https://cloudgpu.app/agent-lab/index.html#quote) exposes this scope explicitly.

Example anonymous estimate; no API key or allocation:

```sh
curl --fail --silent --show-error https://cloudgpu.app/v1/quotes \
  -H 'Content-Type: application/json' \
  --data '{"requirements":{"min_vram_gb":24,"gpu_count":1},"estimated_duration_seconds":900,"max_budget_usd":"2.00"}'
```

Choose a suitable candidate using its current fields, including Job support, estimated cost, balance needed to start, minimum charge, billing increment and quote expiry. A result being within budget is not proof the account has sufficient balance. Unknown compatibility or upstream health is not a green light.

## Connect and obtain explicit paid-work approval

Follow the [client setup](clients.md). The owner signs in and reviews the account/key limits. Ask the owner to approve the selected workload, fresh quote, minimum charge, caps, uploaded data and output plan. Credentials stay outside chat and logs.

For whole-hour inventory, obtain the binding rental billing quote and explicitly accept the minimum/billing period using the live API/tool fields. Each allocation needs its own current quote. `run_job` requires actual compatible inventory and, where applicable, `billing_quote_id` and `billing_accepted=true` in addition to the compute quote and execution approval. Do not silently renew an expired quote or switch billing rules. Each started hour is fully charged even after an early stop.

## Run a reviewed recipe

Start with [verified small-task scripts](https://github.com/cloudgpu-app/cloudgpu-mcp/tree/main/examples/verified-tasks): GPU environment, SmolLM2-135M causal-LM LoRA, and a tiny Wan2.1 1.3B video. Their exact sizes, elapsed times, final fees and unsuccessful development attempts are documented there; they do not certify arbitrary training/generation workflows.

From the MCP source repository after its documented dependency setup, preview a case locally:

```sh
node examples/verified-tasks/run.mjs gpu-environment
```

The preview does not authorize a submission. After reviewing the actual recipe, current quotes, source billing and limits, the documented runner has an explicit `CGPU_SUBMIT=YES` gate. Keep an original idempotency key and acceptance receipt; after a timeout, reconcile the accepted Job rather than creating a new paid task. Commands and file inputs must be reviewed separately for each workload.

Use only tools advertised in the current session. Stop on `needs_attention`, uncertain allocation, authorization denial, depleted funds or changed terms. An uncertain provider response never authorizes a replacement GPU.

## Save, verify and release

Before starting, configure explicit output paths, byte limits, storage consent and sufficient quota. Instance disks are erased on release. Native Job output collection must report `output_collection` success; a zero process exit code alone is insufficient. Partial output collection is not overall success.

Use the returned file metadata and the documented `GET /v1/files/{id}/download` / available file tools to retrieve authorized outputs. Verify byte counts, SHA-256 and workload-specific validity. The small-case runner implements resumable collection of its requested outputs; arbitrary directories are not implicitly persisted.

Confirm terminal/finalized cost and resource release. Distinguish platform release state from independently verified upstream release; report upstream verification as unknown when unavailable. Report GPU charges separately from storage, transfer or unsuccessful prior attempts. Persistent files retain their own budget, access and retention conditions.

## Acceptance boundary

The small-task evidence and actual CrewAI read-only tool have been exercised. A brand-new Google account's complete payment/approval flow, every listed client GUI, and a continuous owner-approval-to-release product video are **not** claimed as accepted by this runbook. Test those boundaries separately; do not manufacture an approval screen or label a read-only UI tour as a live paid run.
