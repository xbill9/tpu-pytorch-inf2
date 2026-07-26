# Gemini workspace context: AWS Inferentia2

This project provides an `inf2-devops` MCP server for AWS EC2 Inferentia2 and
AWS Neuron vLLM serving.

The root `server.py`, `project-setup.sh`, and `requirements.txt` files are
authoritative. Run `make skill` after edits to refresh
`.claude/skills/inf2-management/mcp/` and `skills/inf2-management/`.

The server uses:

- boto3 with the standard AWS credential chain
- EC2 Inf2 instances and a regional Neuron DLAMI
- the versioned AWS Neuron vLLM Deep Learning Container
- AWS Systems Manager rather than SSH for remote commands
- AWS Secrets Manager for gated-model tokens
- a `ManagedBy=inf2-devops` tag to avoid touching unrelated instances

Configuration is controlled with `AWS_REGION`, optional `AWS_PROFILE`,
`MODEL_NAME`, `INSTANCE_TYPE`, `SERVICE_NAME`, `HF_SECRET_ID`, `VLLM_PORT`,
`VLLM_IMAGE`, and `NEURON_AMI_NAME`.

Never expose credentials in user data or output. Treat instance termination as
permanent and require explicit user approval.
