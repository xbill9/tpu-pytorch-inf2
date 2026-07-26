# CLAUDE.md — AWS Inferentia2 DevOps MCP

This repository packages the `inf2-management` Claude Code skill and the
`inf2-devops` FastMCP server. It provisions and operates AWS EC2 Inf2 instances
running the AWS Neuron vLLM Deep Learning Container.

## Authoritative files

- `server.py`: MCP server and AWS lifecycle implementation
- `project-setup.sh`: skill installer and MCP registration
- `requirements.txt`: runtime dependencies
- `.claude/skills/inf2-management/SKILL.md`: workflow and guardrails

Run `make skill` after editing sources. This refreshes the MCP snapshots and
the plugin-layout copy. Run `make skill-package` when publishing a release.

## Engineering rules

- Use boto3 and the standard AWS credential provider chain.
- Require explicit existing subnet, security-group, and instance-profile
  identifiers for creation. Do not create broad network or IAM policy.
- Use SSM Run Command for remote administration; do not require SSH keys.
- Scope instance discovery to the `ManagedBy=inf2-devops` tag.
- Store Hugging Face tokens in Secrets Manager, never user data.
- Accept supported Inf2 sizes only and derive device/Core topology from them.
- Treat stopping and termination as destructive. Termination is permanent.
- Keep Neuron SDK, PyTorch, vLLM, and DLC versions compatible as a unit.

Validation without AWS credentials can cover Python compilation, shell syntax,
tool schemas, cloud-init rendering, and package synchronization. Live lifecycle
checks require an authorized AWS account with Inf2 quota.
