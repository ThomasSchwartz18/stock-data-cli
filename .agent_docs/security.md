# Security Guidelines

## Purpose
Protect secrets, user input, and runtime behavior in this CLI application.

## Secrets and Credentials
- Never hardcode API keys, tokens, or secrets.
- Load secrets from environment variables (`python-dotenv` is acceptable for local development).
- Ensure `.env` is ignored by Git.
- If a template is needed, use `.env.example` with placeholder values only.

## Input Validation
- Validate ticker/symbol input before using it.
- Restrict symbols to expected character sets/length (for example uppercase letters, digits, `.`, `-` as needed).
- Reject unexpected characters and return a clear validation error.
- Never pass raw user input into shell commands or dynamic code execution.

## File System Safety
- Avoid writing files unless required by feature design.
- If writing files, use explicit allowlisted paths and safe filename handling.
- Do not overwrite arbitrary paths based on user input.

## Network and Request Safety
- Use HTTPS endpoints for provider APIs.
- Set explicit timeouts for all outbound requests.
- Avoid following untrusted redirect chains without controls.

## Logging and Data Handling
- Never log credentials or auth headers.
- Do not print sensitive environment variables in debug output.
- Redact potentially sensitive values in error messages.

## Unsafe Request Policy
If a request asks for insecure behavior (for example exposing API keys, bypassing validation, or adding arbitrary command execution):
- Refuse the unsafe action.
- Explain the risk briefly.
- Provide a secure alternative implementation approach.
