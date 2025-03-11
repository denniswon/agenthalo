# AgentHalo

AgentHalo is a collection of LLM-powered AI agents running inside TEE (Intel TDX) for Private, Verifiable AI.

AgentHalo can interpret natural language trading strategies, analyze real-time market signals, and autonomously execute trades across multiple chains.

All operations can be cryptographically verified using TEE remote attestation off-chain, and on-chain as well via zero knowledge proof of the attestation for every operation happening inside the TEE.

For more information on on-chain verification of TEE remote attestation, please refer to [TEE Remote Attestation On-chain Verification](https://magiclabs.notion.site/TEE-Remote-Attestation-On-chain-Verification-1aead65b2b7080b0876bfdbb11634e78?pvs=4)

## Features

### AI-Powered Trading with Agents

- LLM-powered agents capable of processing complex, unstructured signals for trading decisions
- Intelligent tool selection and chaining for complex multi-step analysis
- Dynamic composition and execution of Python code using available tools
- Natural language strategy definition and real-time reasoning
- Iterative agentic reasoning to evaluate market conditions, weigh multiple input signals, and make trading decisions given input trading strategy

### Trading & Execution

- Real-time strategy execution and monitoring
- Execution modes:
  - Automated trading alerts via Telegram
  - Autonomous trade execution
- Multi-chain support with DEX integrations (Uniswap, Jupiter)

## Prerequisites

- Python 3.11 or higher
  - Download and install Python
- [Poetry](https://python-poetry.org/docs/) 2.1 or higher

## Getting Started

```bash
git clone https://github.com/denniswon/agenthalo.git
cd agenthalo
```

### 1. Installation

```bash
# For basic installation
make install

# For development (includes dev dependencies)
make dev-install
```

Note: Poetry manages its own virtual environments, so a separate virtual environment should not be required.

### 2. API Keys Setup

1. **LLM API Key**:

   - [Anthropic API Key](https://docs.anthropic.com/en/api/getting-started) if using Claude models (default)
   - [OpenAI API Key](https://platform.openai.com/docs/quickstart) if using GPT models
   - or any other LLM provider [supported by LiteLLM](https://models.litellm.ai/)

2. **Blockchain Access**:

   - [Alchemy API Key](https://www.alchemy.com/) for blockchain data, or another RPC provider of choice

3. **Optional - Telegram Bot** for notifications:
   - Create a bot through [BotFather](https://t.me/botfather) with `/newbot` and securely save the chat id and the bot token

### 3. Environment Configuration

```bash
cp .env.example .env
```

#### Required environment variables

LLM Configuration (at least one required):

- `ANTHROPIC_API_KEY`: Your Anthropic API key if using Claude models (default)
- `OPENAI_API_KEY`: Your OpenAI API key if using GPT models

Blockchain Access:

- `ALCHEMY_API_KEY`: Your Alchemy API key for accessing blockchain data

#### Optional configurations

Notification settings:

- `TELEGRAM_BOT_TOKEN`: Required for sending alerts via Telegram bot
- `TELEGRAM_CHAT_ID`: Required chat ID for receiving Telegram alerts
- `TELEGRAM_SERVER_IP`: IP address for Telegram server (defaults to 0.0.0.0)
- `TELEGRAM_SERVER_PORT`: Port for Telegram server (defaults to 8000)

Logging configuration:

- `LOG_LEVEL`: Sets logging verbosity level (defaults to INFO)
- `LOG_FORMAT`: Custom format for log messages (default: "%(asctime)s - %(name)s - %(levelname)s - %(message)s")

## Run

We also need to download the [DStack](https://github.com/Dstack-TEE/dstack) simulator:

```shell
# Mac
wget https://github.com/Leechael/tappd-simulator/releases/download/v0.1.4/tappd-simulator-0.1.4-aarch64-apple-darwin.tgz
tar -xvf tappd-simulator-0.1.4-aarch64-apple-darwin.tgz
cd tappd-simulator-0.1.4-aarch64-apple-darwin
./tappd-simulator -l unix:/tmp/tappd.sock

# Linux
wget https://github.com/Leechael/tappd-simulator/releases/download/v0.1.4/tappd-simulator-0.1.4-x86_64-linux-musl.tgz
tar -xvf tappd-simulator-0.1.4-x86_64-linux-musl.tgz
cd tappd-simulator-0.1.4-x86_64-linux-musl
./tappd-simulator -l unix:/tmp/tappd.sock
```

Once the simulator is running, you need to open another terminal to start your FastAPI development server:

```shell
# Start the FastAPI dev server
python -m fastapi dev
```

## Development

### Running Tests

```bash
# Run all tests
make all-tests

# Run specific test suites
make unit-tests
make integration-tests  # Requires API keys to be specified
```

### Code Quality

The project uses:

- Black for code formatting
- isort for import sorting
- ruff for linting
- mypy for type checking

```bash
# Format code
poetry run black .
poetry run isort .

# Run linters
poetry run ruff check .
poetry run mypy .
```

or use Makefile shortcuts:

```bash
make dev-lint
```
