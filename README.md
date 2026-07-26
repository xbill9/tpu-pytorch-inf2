# AWS Inferentia2 PyTorch & vLLM DevOps MCP

This repository packages an MCP server and Claude Code skill for operating
PyTorch/vLLM inference on AWS Inferentia2 (`inf2`) EC2 instances. It provisions
Neuron DLAMIs, starts an AWS Neuron vLLM Deep Learning Container, checks
NeuronCore health, reads logs through Systems Manager, manages instance
lifecycle, and queries the OpenAI-compatible endpoint.

## Quick start

Prerequisites:

- Python 3.11+ and the AWS CLI
- AWS credentials from an IAM role, AWS SSO, or a configured profile
- an existing VPC subnet and security group (allow the serving port only from
  trusted clients)
- an EC2 instance profile with `AmazonSSMManagedInstanceCore`, ECR Public pull
  access, and permission to read the configured Hugging Face secret
- EC2 Inferentia On-Demand or Spot vCPU quota in the target region

```bash
python3 -m pip install -r requirements.txt
./project-setup.sh . --region us-east-1 --instance-type inf2.xlarge
```

Restart Claude Code and confirm that `inf2-devops` appears under `/mcp`.
Store a gated-model token with `save_hf_token`, then call
`create_inf2_instance` with your subnet, security group, and instance-profile
names. Use `get_deployment_config` first if you want a reviewable AWS CLI
command without changing AWS.

## Configuration

| Variable | Default | Purpose |
|---|---|---|
| `AWS_REGION` | `us-east-1` | AWS region |
| `AWS_PROFILE` | unset | Optional shared-config profile |
| `MODEL_NAME` | `meta-llama/Llama-3.1-8B-Instruct` | Hugging Face model |
| `INSTANCE_TYPE` | `inf2.xlarge` | Inf2 size |
| `SERVICE_NAME` | `vllm-inf2` | EC2 Name tag |
| `HF_SECRET_ID` | `vllm/hf-token` | Secrets Manager secret |
| `VLLM_PORT` | `8000` | Host API port |
| `VLLM_IMAGE` | Neuron SDK 2.31 vLLM DLC | Versioned Neuron container |
| `NEURON_AMI_NAME` | `Deep Learning AMI Neuron*Ubuntu*` | Regional AMI filter |

Supported topology defaults are derived from EC2 hardware: `inf2.xlarge` and
`inf2.8xlarge` expose 1 device/2 NeuronCores, `inf2.24xlarge` exposes
6/12, and `inf2.48xlarge` exposes 12/24.

## Tools

- `get_deployment_config`, `create_inf2_instance`, `list_inf2_instances`
- `start_inf2_instance`, `stop_inf2_instance`, `terminate_inf2_instance`
- `verify_neuron_health`, `get_vllm_logs`, `get_endpoint`, `query_model`
- `save_hf_token`, `check_inf2_quotas`, `get_help`

Remote operations use SSM Run Command, so the generated deployment does not
require an SSH key or an internet-wide port 22 rule. Instances are tagged
`ManagedBy=inf2-devops`; discovery is deliberately scoped to that tag.

## Development

```bash
make skill
make test
make lint
make skill-package
```

The root `server.py`, `project-setup.sh`, and `requirements.txt` are
authoritative. `make skill` refreshes the bundled copies.
