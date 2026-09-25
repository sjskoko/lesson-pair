# Security and privacy

This project has no hosted backend and does not request credentials. Its Python utility does not make network requests. An AI host and an authenticated Notion connector are separate systems with their own data-handling policies.

Do not open a public issue containing real lesson data, account tokens, private page URLs, contact information, or an unredacted screenshot. For ordinary bugs, use a minimal synthetic reproduction. If GitHub's private vulnerability reporting is available for this repository, use it for sensitive security findings; otherwise report only a non-sensitive summary and request a private channel.

Keep local material in ignored `private/`, `local/`, or `output/` directories. A gitignore is not a complete privacy protection: inspect staged files before publishing. The skill instructs an assistant to treat transcripts, notes, and external page content as data rather than commands.
