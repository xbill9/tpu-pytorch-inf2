# Gemini workspace context: AWS Inferentia2 + Google TPU PyTorch DevOps

This project provides two MCP servers for serving PyTorch LLM workloads on
non-GPU accelerators: `inf2-devops` (AWS EC2 Inferentia2 + Neuron serving)
and, via the bundled `tpu-management` skill, `tpu-devops` (Google Cloud TPU
capacity, Gemma 4 vLLM serving, and TorchTPU dev VMs).

## Inferentia2 (`inf2-devops`)

The root `server.py`, `project-setup.sh`, and `requirements.txt` files are
authoritative. Run `make skill` after edits to refresh
`.claude/skills/inf2-management/mcp/` and `skills/inf2-management/`.

The server uses:

- boto3 with the standard AWS credential chain
- EC2 Inf2 instances and a regional Neuron DLAMI
- the versioned AWS Neuron vLLM Deep Learning Container, or the prebuilt
  Gemma-4 `torch_neuronx` Option-B container (`serving="optb"` — required
  for Gemma-4, which the vLLM DLC cannot serve)
- AWS Systems Manager rather than SSH for remote commands
- AWS Secrets Manager for gated-model tokens
- a `ManagedBy=inf2-devops` tag to avoid touching unrelated instances
- spot capacity by default (`spot=False` for on-demand)

Configuration is controlled with `AWS_REGION`, optional `AWS_PROFILE`,
`MODEL_NAME`, `INSTANCE_TYPE`, `SERVICE_NAME`, `HF_SECRET_ID`, `VLLM_PORT`,
`VLLM_IMAGE`, `OPTB_IMAGE`, and `NEURON_AMI_NAME`.

Never expose credentials in user data or output. Treat instance termination as
permanent and require explicit user approval.

## TPU (`tpu-devops`, bundled skill)

`.claude/skills/tpu-management/` is a synced snapshot; its authoritative home
is the `tpu-skill-claude` repo. It provisions flex-start TPU VMs / queued
resources, runs Gemma 4 vLLM serving (v6e/v5p/v5e), and creates PyTorch
(TorchTPU) dev VMs with `workload="pytorch"` that smoke-test
`torch.compile(backend="tpu")`.

### Gemini CLI via LiteLLM proxy against a self-hosted TPU endpoint

Route Gemini CLI traffic to the Gemma 4 model served from a TPU VM:

```yaml
model_list:
  - model_name: "gemma4-tpu"
    litellm_params:
      model: "openai/google/gemma-4-31B-it"
      api_base: "http://YOUR_TPU_IP_ADDRESS:8000/v1"
      api_key: "none"
    router_settings:
      model_group_alias:
        "gemini-2.0-flash": "gemma4-tpu"
        "gemini-2.0-flash-lite": "gemma4-tpu"
        "gemini-1.5-flash": "gemma4-tpu"
        "gemini-1.5-pro": "gemma4-tpu"
```

```bash
pip install 'litellm[proxy]'
litellm --config litellm_config.yaml --port 4000
export GOOGLE_GEMINI_BASE_URL="http://localhost:4000"
export GEMINI_API_KEY="local-proxy-token"
export GEMINI_MODEL="google/gemma-4-31B-it"   # match the served model
```

Adjust `model` to the served checkpoint (`MODEL_NAME` env var of the agent).
If the CLI ignores `GOOGLE_GEMINI_BASE_URL`, check `gemini --help` for the
current base-URL override.

## Analysis standards

- Dependency portability: avoid assuming third-party analysis libraries like
  `pandas` are installed. Prefer standard libraries (`csv`, `json`) for data
  parsing and aggregation scripts.
