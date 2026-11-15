---
title: CloudGPU Agent Compute Lab
emoji: 🧭
colorFrom: green
colorTo: gray
sdk: static
pinned: false
license: mit
short_description: Read-only agent compute discovery and billing explorer
---

# Agent Compute Lab

A static, free-to-host demo: billing illustration, links to live anonymous readiness, verified internal smoke-test evidence, and Skill/MCP installation. No API keys, customer data, paid GPU allocation or model execution occurs here.

Source: https://github.com/cloudgpu-app/cloudgpu-agent-skills

Copy `docs/index.html` to this Space's root as `index.html`, and `docs/assets` as `assets`. The self-check opens the actual CloudGPU endpoint directly, so browser cross-origin restrictions cannot be confused with a platform outage.

## Publishing

Install `huggingface_hub`, configure `HF_TOKEN` in a secure environment and `HF_SPACE_ID=your-account/agent-compute-lab`, then run `python publish.py`. The token is read only from the environment and is never printed. `python publish.py --dry-run` validates the static bundle without credentials or network.
