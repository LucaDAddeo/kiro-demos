# Kiro Ambassador Demos

Multi-language demonstration repository showcasing [Kiro IDE](https://kiro.dev) capabilities for the Kiro Ambassador program. Each demo folder isolates a single Kiro feature with working examples you can explore, modify, and learn from.

---

## Table of Contents

| Folder | Capability | Mode | Language |
|--------|-----------|------|----------|
| [`demo-specs/`](demo-specs/) | Spec-driven development | local-only | Python |
| [`demo-hooks/`](demo-hooks/) | Hooks automation | local-only | Bash/JSON |
| [`demo-steering/`](demo-steering/) | Steering files | local-only | Markdown |
| [`demo-powers/`](demo-powers/) | MCP Powers | local-only | TypeScript |
| [`demo-agents/`](demo-agents/) | Agent workflows | deployable | Python |
| [`showcase-serverless-assistant/`](showcase-serverless-assistant/) | End-to-end showcase | deployable | Python |

**Local-only** demos run entirely on your machine with no AWS account or network required.  
**Deployable** demos include AWS infrastructure (SAM/CDK) and provide cost estimates and teardown scripts.

---

## Relationship with cloud-ops-toolkit

This repository and [cloud-ops-toolkit](https://github.com/lucadaddeo/cloud-ops-toolkit) serve complementary purposes:

| Aspect | cloud-ops-toolkit | kiro-ambassador-demos |
|--------|-------------------|----------------------|
| Purpose | Production-ready Bash scripts for AWS operations | Educational demos of Kiro IDE features |
| Language | Bash exclusively | Python, TypeScript, Bash |
| Audience | DevOps engineers | Developers learning Kiro |
| Integration | Standalone scripts | References toolkit as Git submodule |

The agent workflow demos invoke cloud-ops-toolkit scripts via subprocess — they never duplicate them. If you need the toolkit locally, the `demo-agents/` folder includes submodule configuration to pull it in.

---

## Prerequisites

- [Kiro IDE](https://kiro.dev) (latest version)
- [AWS CLI v2](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html) (for deployable demos)
- Python 3.11+
- Node.js 18+
- [jq](https://jqlang.github.io/jq/) (JSON processing)

---

## Quick Start

```bash
# Clone the repository
git clone https://github.com/your-username/kiro-ambassador-demos.git
cd kiro-ambassador-demos

# Initialize submodules (for agent demos that reference cloud-ops-toolkit)
git submodule update --init --recursive

# Install pre-commit hooks for secret scanning
pip install pre-commit
pre-commit install

# Explore a local-only demo
cd demo-specs
pip install -r requirements.txt
python src/url_shortener.py --help
```

For deployable demos, configure your AWS profile first:

```bash
export AWS_PROFILE=your-profile-name
cd demo-agents
sam build && sam deploy --guided
```

---

## Repository Structure

```
kiro-ambassador-demos/
├── README.md                          # This file (English)
├── README.it.md                       # Italian translation
├── .gitignore                         # Python, TypeScript, Bash exclusions
├── .pre-commit-config.yaml            # gitleaks secret scanning
├── docs/
│   └── presentations/                 # Italian talk/workshop materials
├── demo-specs/                        # Spec-driven development (local-only)
├── demo-hooks/                        # Hooks automation (local-only)
├── demo-steering/                     # Steering files (local-only)
├── demo-powers/                       # MCP Powers (local-only)
├── demo-agents/                       # Agent workflows (deployable)
└── showcase-serverless-assistant/     # End-to-end showcase (deployable)
```

---

## License

This project is licensed under the [MIT License](LICENSE).
