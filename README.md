# Research Agent Example

This repository contains a Research Agent built using the `claude-agent-sdk`. The agent is equipped with custom skills (tools) to search the web and read URL contents, allowing it to perform research tasks and summarize findings.

## Features

- **Web Search**: Uses DuckDuckGo to search for information.
- **Web Reading**: Fetches and parses content from URLs using `httpx` and `BeautifulSoup`.
- **Autonomous Research**: The agent can plan and execute research steps based on a prompt.

## Prerequisites

- Python 3.7+
- A valid API key or configuration for `claude-agent-sdk` (assuming the SDK requires environment setup).

## Installation

1. Clone the repository (if applicable) or navigate to the project directory.

2. Install the required dependencies:

   ```bash
   pip install claude-agent-sdk duckduckgo-search httpx beautifulsoup4
   ```

## Usage

1. **Configure the Agent**:
   The agent is configured in `agent.py`. You can modify the `system_prompt` or the initial query in the `main` function.

2. **Run the Agent**:
   Execute the `agent.py` script to start the research process.

   ```bash
   python agent.py
   ```

3. **Output**:
   The agent will print its progress, including search queries, URLs being read, and the final summary provided by the Assistant.

## Project Structure

- `agent.py`: The main entry point. Initializes the `ClaudeSDKClient` with the research tools and runs the research loop.
- `research_skills.py`: Defines the tools (`search`, `read_url`) and wraps them into an MCP (Model Context Protocol) server.
- `AGENTS.md`: Original documentation file.

## Customization

You can extend the agent's capabilities by adding more tools in `research_skills.py` and registering them in the `research_server` configuration.
