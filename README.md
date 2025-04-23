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

## MyCobot M5 280 

The myCobot SDK I'm using is documented here: https://github.com/elephantrobotics/pymycobot/blob/main/docs/MyCobot_280_en.md
The robot I'm using is here: [Elephant Robotics myCobot 280 M5Stack 2023 - 6 DOF Collaborative Robot](https://shop.elephantrobotics.com/products/mycobot-worlds-smallest-and-lightest-six-axis-collaborative-robot?dm_acc=3657328933&dm_cam=17566429188&dm_grp=&dm_ad=&dm_src=x&dm_tgt=&dm_kw=&dm_mt=&dm_net=adwords&dm_ver=3&gad_source=1&gbraid=0AAAAACw-MsX9jVF8Xrf8qY-f4wy-ED5Vm&gclid=CjwKCAjwn6LABhBSEiwAsNJrjmO4CfRjIuTkjNdP-N-cR6z23fo_WFmzp2MMJ79UGylbz7paE1rwsxoCgSgQAvD_BwE)

### Joint ranges

| Joint Id | Range         |
|----------|--------------|
| 1        | -168 ~ 168   |
| 2        | -135 ~ 135   |
| 3        | -150 ~ 150   |
| 4        | -145 ~ 145   |
| 5        | -165 ~ 165   |
| 6        | -180 ~ 180   |

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.