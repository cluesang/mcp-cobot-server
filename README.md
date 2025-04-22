# MCP Cobot Server

This repository contains the **MCP Cobot Server**, a **FastMCP** server implementation for the M5 MyCobot280 robot.

Based on the model context protocol python-sdk: https://github.com/modelcontextprotocol/python-sdk?tab=readme-ov-file#quickstart

## Features

- Implements the MCP standard for efficient context management.
- Built with **FastMCP** for high performance and scalability.
- Designed for integration with collaborative robot (myCobot) systems.

## Requirements

- Python 3.8+
- FastMCP library

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/your-username/mcp-cobot-server.git
    cd mcp-cobot-server
    ```

2. Install dependencies:
    ```bash
    uv sync
    source .venv/bin/activate
    ```

**Note** This project uses `uv` to install manage the python virtual environment and dependencies. Learn more here: https://docs.astral.sh/uv/guides/projects/

## Usage

Start the server:
```bash
mcp install server.py
```

For development:
```bash
mcp dev server.py
```
## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.