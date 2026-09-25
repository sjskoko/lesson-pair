# Use your own AI

## In ChatGPT or another skill host

The skill uses the model already active in that host. It does not need a separate provider key. Install the LessonPair plugin through a supported repository marketplace or your workspace's plugin workflow. Availability and admin controls vary. Adding a marketplace is not the same as installing its plugin. This project is independent and is not approved or listed in OpenAI's public directory by default.

For a chat-only host, attach SKILL.md plus guided-session.md and source-access.md. Ask it to follow the workflow with your video transcript. This is manual prompt use, not native plugin installation. Never paste an API key into a conversation.

## Local terminal tutor

Python 3.10+; the tutor uses the standard library. A compatible model must accept `POST <base>/chat/completions` with `model` and text `messages`, and return `choices[0].message.content`. Provider-specific APIs require an adapter; support for all providers/models is not implied.

From the repository root:

```bash
python skills/lesson-pair/scripts/learn.py start --source transcript.txt --language Korean
python skills/lesson-pair/scripts/learn.py run
python skills/lesson-pair/scripts/learn.py export
```

Configure the provider before `run`:

```bash
export LESSONPAIR_BASE_URL='https://YOUR-PROVIDER.example/v1'
export LESSONPAIR_MODEL='YOUR-MODEL-ID'
# Enter a key with your shell/secret manager, not in source or chat.
read -rs -p 'Provider key: ' LESSONPAIR_API_KEY
export LESSONPAIR_API_KEY
```

An OpenAI-compatible local server, such as Ollama, can use:

```bash
export LESSONPAIR_BASE_URL='http://localhost:11434/v1'
export LESSONPAIR_MODEL='YOUR-INSTALLED-MODEL'
unset LESSONPAIR_API_KEY
```

Start your server and install a supported model separately. We test the HTTP contract against a local stub; actual compatibility and teaching quality depend on your endpoint/model. No paid provider is bundled or provisioned.

For a YouTube URL, install optional yt-dlp yourself, then:

```bash
python skills/lesson-pair/scripts/learn.py start --url 'https://www.youtube.com/watch?v=VIDEO_ID' --language Korean
```

This attempts English captions, not transcription. If access fails or captions are absent, supply a transcript file. No guaranteed support for every video.

## Session controls

Type one short answer and press Enter. `/hint` and `/example` work during practice; `/quit` pauses. `run` resumes the same session, including failed provider requests. Choose a new `--session private/another.json` for another video. The CLI offers a compact baseline → one practice exchange → retry → comparison; the chat skill can adapt with more practice when needed.

The first attempt and retry are saved before each AI call. Assistance on the retry is self-reported (unknown if not supplied). AI feedback is labeled separately. Exports make no model calls. No speech recognition, pronunciation scoring, automatic reminders, or native Notion writes are built into the CLI.

## Privacy and costs

`start --source` and `export` are offline. `start --url` contacts the video service through yt-dlp. `run` sends the transcript and session answers to the endpoint you explicitly configure. Provider policies and billing apply; a ChatGPT subscription does not automatically include third-party API credits. Local-model inference still uses compute.

Keys come only from environment variables, are never written to the session, and are not included in errors. Redirects are refused. Remote endpoints require HTTPS; loopback HTTP is allowed. Default private output is ignored by Git, but another output path may not be. Inspect files before sharing. The static website never asks for keys.
