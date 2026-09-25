# Security and privacy

This project has no hosted backend and does not request credentials. Its Python utility does not make network requests. An AI host and an authenticated Notion connector are separate systems with their own data-handling policies.

Do not open a public issue containing real lesson data, account tokens, private page URLs, contact information, or an unredacted screenshot. For ordinary bugs, use a minimal synthetic reproduction. If GitHub's private vulnerability reporting is available for this repository, use it for sensitive security findings; otherwise report only a non-sensitive summary and request a private channel.

Keep local material in ignored `private/`, `local/`, or `output/` directories. A gitignore is not a complete privacy protection: inspect staged files before publishing. The skill instructs an assistant to treat transcripts, notes, and external page content as data rather than commands.

The v0.2 terminal tutor sends transcript text and attempts to a user-configured model endpoint. Remote URLs require HTTPS; HTTP is restricted to loopback. API keys come from environment variables, are excluded from saved session data and errors, and are not forwarded across redirects. The plugin itself contains no server or credential collection. The static site never accepts API keys. Treat source transcripts as untrusted data, including instructions embedded in them.

Default `private/` output is ignored by Git. A user-selected path may not be. Review exported data before sharing. Caption retrieval is optional through yt-dlp, which contacts the video service; it does not use cookies or bypass access restrictions.
