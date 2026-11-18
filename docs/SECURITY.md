# Velora-AI Security Policy

## 1. Purpose

Define the security requirements for developing, testing, and deploying Velora-AI.

Security must be enforced by the backend. Frontend restrictions alone are not sufficient.

## 2. Secrets and Environment Configuration

- Never hardcode production secrets.
- Load credentials from environment variables.
- Use a strong, randomly generated JWT signing secret.
- Keep local environment files out of version control.
- Provide a safe example environment file without real credentials.
- Never expose API keys or database credentials in frontend code.
- Rotate credentials if they are exposed.

## 3. Password Security

- Hash passwords using a modern password-hashing algorithm.
- Never store plaintext passwords.
- Never return password hashes through APIs.
- Validate password input.
- Use safe authentication error messages.

## 4. Authentication

- Validate tokens on protected endpoints.
- Verify token signatures and expiration.
- Reject invalid or expired tokens.
- Use a consistent authentication implementation.
- Avoid trusting user IDs supplied by the frontend without verifying ownership.

## 5. Authorization and User Isolation

- Every protected resource must have an authenticated owner.
- Users must access only resources they are authorized to use.
- Verify ownership before reading, updating, or deleting resources.
- Enforce administrative permissions on the backend.
- Apply user-level filters to document retrieval and memory retrieval.
- Test access attempts between two different users.

## 6. API Security

- Configure CORS with an explicit production origin allowlist.
- Validate all request data.
- Apply appropriate rate limits.
- Avoid exposing internal exception details.
- Use HTTPS in production.
- Restrict administrative endpoints.
- Set reasonable request and response size limits.

## 7. File Upload Security

- Allow only supported file formats.
- Validate file extensions and actual file content.
- Enforce upload size limits.
- Generate safe server-side filenames.
- Prevent path traversal.
- Avoid executing uploaded content.
- Handle malformed and corrupted files safely.
- Enforce document ownership.
- Define secure file deletion and retention behavior.

## 8. Database Security

- Use parameterized queries and ORM protections.
- Restrict database credentials.
- Do not expose database connections to the frontend.
- Enforce relationships and ownership constraints.
- Back up production data.
- Use migrations for schema changes.
- Avoid logging sensitive database values.

## 9. AI and RAG Security

- Treat user messages and uploaded documents as untrusted input.
- Do not treat retrieved document instructions as trusted system instructions.
- Restrict tools to explicitly authorized operations.
- Validate tool inputs and outputs.
- Prevent one user's retrieved content from entering another user's context.
- Do not expose provider credentials in prompts or responses.
- Apply execution limits and timeouts.

## 10. Logging and Privacy

- Do not log passwords, tokens, or API keys.
- Avoid collecting unnecessary personal information.
- Limit access to application logs.
- Define data retention and deletion policies.
- Ensure errors do not reveal sensitive implementation details.

## 11. Dependencies and Deployment

- Keep dependencies maintained.
- Review security advisories.
- Pin or constrain dependency versions appropriately.
- Separate development and production configuration.
- Disable debug mode in production.
- Restrict production database and administrative access.
- Verify deployment secrets and allowed origins.

## 12. Security Verification

Before production release, verify:

- Password hashing.
- JWT signature and expiration.
- Authentication consistency.
- Authorization and resource ownership.
- CORS restrictions.
- Upload validation.
- RAG user isolation.
- Memory user isolation.
- Rate limiting.
- Secret management.
- Error handling.
- Dependency security.

## 13. Security Incident Response

If a credential or sensitive user data is exposed:

1. Restrict the affected access.
2. Rotate compromised credentials.
3. Assess the affected resources.
4. Fix the root cause.
5. Review logs for suspicious activity.
6. Notify affected users when legally or operationally required.
7. Record the incident and corrective actions.

## 14. Maintenance

Review this document whenever authentication, data storage, AI integrations, file processing, or deployment architecture changes.

Do not claim a security control is implemented until it has been verified.
