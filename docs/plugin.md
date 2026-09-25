# LessonPair plugin for ChatGPT and Codex

LessonPair v0.2 is a **skills-only plugin**. It supplies the learning workflow to the host's active AI. It needs no MCP server, backend, OAuth, or API key. The local BYO-model tool is a separate route for people who want to select an API endpoint.

## Package

```text
.agents/plugins/marketplace.json
plugins/lesson-pair/
  plugin.json
  skills/lesson-pair/
    SKILL.md
    agents/openai.yaml
    references/
    scripts/
```

The portable `plugin.json` follows the [Agent Plugins manifest schema](https://agent-plugins.org/schemas/1.0.0/plugin.schema.json). The marketplace points to `./plugins/lesson-pair`, relative to the repository root. No server authentication is configured.

## Repository marketplace route

In a Codex installation with plugin marketplace support:

```bash
codex plugin marketplace add sjskoko/lesson-pair --ref main
```

Then restart the ChatGPT desktop app, open its Plugins Directory, choose the **LessonPair** marketplace, and install **lesson-pair**. Use a trusted local checkout when following the repository marketplace route. Check that the skill appears before beginning a lesson. Adding a marketplace registers a source; it does not install the plugin by itself.

For a reproducible version after the release is published, use `--ref v0.2.0`. For local development, clone this repository and follow the host's local marketplace workflow. Never assume that a CLI source addition propagates automatically to every ChatGPT client/account.

## ChatGPT availability

ChatGPT supports plugins that package skills, subject to client, account, and workspace controls. Use the repository/workspace installation flow available in your environment. If your interface only shows the public plugin directory and has no repository or workspace import, there is no universal one-click installation link for this repository yet. Use the portable workflow below until a public-directory version becomes available. No submission is currently pending.

**Status: package developed; not submitted to or approved for OpenAI's public plugin directory.** Directory publication and workspace distribution are separate from a public GitHub release. We do not claim a completed host installation based on package validation alone.

Official references (checked 2026-09-25):
- [Build plugins](https://developers.openai.com/plugins/build/plugins)
- [Plugins quickstart](https://developers.openai.com/plugins/quickstart)
- [ChatGPT plugin documentation](https://learn.chatgpt.com/docs/plugins)

## Portable fallback: any capable chat assistant

Download or attach these three files together:

- [SKILL.md](../skills/lesson-pair/SKILL.md)
- [Guided session](../skills/lesson-pair/references/guided-session.md)
- [Source access](../skills/lesson-pair/references/source-access.md)

Ask: “Use LessonPair with this English video. Guide me one question at a time and wait for my own retry.” Supply captions or an excerpt if the host cannot access the source. A custom GPT can use these as manually configured instructions/knowledge; they do not automatically install themselves from a GitHub link. Fetch other references only for features you use.

## Developer validation

`skills/lesson-pair` is the source of truth in this repository. Run `python scripts/build_plugin.py` after edits; CI checks for drift. Do not edit the generated plugin copy independently.

Run the unit suite, plugin build check, and documentation checks. In a plugin-capable host, complete [the manual scenarios](plugin-evaluation.md) after installation. The development environment for v0.2 had no Codex plugin CLI, so package structure and tutor behavior were checked without claiming an end-to-end host install.

Public directory submission should include this repository, license, privacy description, synthetic examples, and results from an actual host install. Publisher identity and workspace permissions must be handled by the account owner; no private learner records belong in the submission.
