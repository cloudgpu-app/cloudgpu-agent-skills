# Install a Skill and connect its tools

A Skill supplies task instructions; MCP supplies executable tools. Installing either one starts no GPU. Connecting an account and approving a paid workload are separate steps. Do not paste credentials into chat.

## 1. Install selected Skills

Use the official Agent Skills CLI:

```sh
npx skills add cloudgpu-app/cloudgpu-agent-skills --agent codex --skill cloudgpu-discover-compute
```

Replace `codex` with your client identifier. Omit `--skill` to choose interactively from the five skills. Add `--global` only if you want a user-wide installation rather than a project installation. Review the install prompts.

| Client | CLI identifier |
| --- | --- |
| Codex | `codex` |
| Claude Code | `claude-code` |
| Cursor | `cursor` |
| VS Code / GitHub Copilot | `github-copilot` |
| OpenCode | `opencode` |
| Windsurf | `windsurf` |
| Cline | `cline` |
| Goose | `goose` |

These identifiers were checked against the installed Skills CLI definitions. Repository discovery listed all five Skills. This is not a claim that every application's complete GUI, login or paid workflow was tested. Reload your client's Skills/session as its documentation requires.

To inspect the repository without installing:

```sh
npx skills add cloudgpu-app/cloudgpu-agent-skills --list
```

Directory exposure depends on genuine usage. CLI discovery checks here used disabled telemetry and did not install Skills to simulate user adoption. No leaderboard placement is guaranteed.

## 2. Configure MCP without putting a key in command history

Requires a supported Node.js installation for local stdio. Use the current package/runtime requirements documented by [cloudgpu-mcp](https://github.com/cloudgpu-app/cloudgpu-mcp).

Codex:

```sh
codex mcp add cloudgpu -- npx -y cloudgpu-mcp
codex mcp list
```

Claude Code:

```sh
claude mcp add cloudgpu -- npx -y cloudgpu-mcp
```

Cursor, in the client's supported project/user MCP settings:

```json
{
  "mcpServers": {
    "cloudgpu": {
      "command": "npx",
      "args": ["-y", "cloudgpu-mcp"]
    }
  }
}
```

Other local clients: configure a stdio server with command `npx` and arguments `["-y", "cloudgpu-mcp"]` using that client's current schema; their JSON root keys are not interchangeable. See the [client-specific MCP instructions](https://cloudgpu.app/docs/mcp).

For clients supporting remote Streamable HTTP and OAuth, use `https://cloudgpu.app/mcp`. Codex clients supporting this transport can use:

```sh
codex mcp add cloudgpu --url https://cloudgpu.app/mcp
codex mcp login cloudgpu
```

Choose the transport appropriate to your client. Remote and stdio sessions expose different tools; remote tools cannot access your local filesystem or SSH. A Skill installation does not automatically add a connector to ChatGPT or another cloud assistant.

## 3. Test discovery, then connect

Ask your agent:

> Inspect CloudGPU readiness and task fit, list suitable compute and request an estimate. Do not allocate compute, pay, transfer storage funds or execute a paid request.

Inspect the tools actually listed in that MCP session. Use `connect_account` / `finish_connect` where exposed; the owner opens the returned link, signs in and approves scoped limits. Remote clients use their documented OAuth approval flow. Keep device secrets and returned keys inside the client's credential storage.

If needed, `request_top_up` returns an owner payment link and `wait_for_funds` checks actual credit. Neither approves compute or charges a card automatically. The next step is the [quote → approve → run → save → release runbook](runbook.md).
