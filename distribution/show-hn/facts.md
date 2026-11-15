# Show HN preparation — verified facts, not submission copy

HN requires authors to write their own submission text and prohibits generated text and automated posting. Do not paste this file as a submission or have an assistant post it.

Rules: https://news.ycombinator.com/newsguidelines.html and https://news.ycombinator.com/showhn.html

## Material the owner can inspect

- Playable, no-login demo: https://cloudgpu.app/agent-lab/index.html
- Anonymous live contract: https://cloudgpu.app/v1/public/agent-self-check
- Source: https://github.com/cloudgpu-app/cloudgpu-agent-skills
- Real small-task evidence and scripts: https://github.com/cloudgpu-app/cloudgpu-mcp/tree/main/examples/verified-tasks
- Demo video: published alongside the Compute Lab, labeled as a read-only UI tour.

## Boundaries to preserve in any personally authored discussion

- Discovery is anonymous; paid compute requires owner authorization and spending approval.
- Billing is source-specific: minute sources and whole-hour sources, not universally per-minute.
- Small internal smoke tests are not customer success-rate or production SLA evidence.
- ComfyUI test: Wan2.1 1.3B, 17 frames, 256×256; successful attempt 1,064s / $0.1105; all 12 development attempts $0.8775.
- LoRA test: causal-LM SmolLM2-135M, 8 steps; not diffusion LoRA or 7B training; successful attempt 190s / $0.0097; four development attempts $0.0339.
- GPU environment test: 191s / $0.0048.
- The demo allocates no GPU, uses no customer data, and records no visitor event analytics.
- Current known issues and sample sufficiency are available at the live readiness endpoint. Do not claim issues were resolved based on this static demo.
- Installation and account connection alone do not approve a paid task.

Publication status: not submitted by automation. Owner-authored text and owner submission required by HN's rules.
