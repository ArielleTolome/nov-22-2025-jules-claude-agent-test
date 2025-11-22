# Research Agent

This is an example agent using `claude-agent-sdk` and Custom Skills (Tools).

## Components

- `agent.py`: The main entry point that initializes the agent and runs a query.
- `research_skills.py`: Defines the skills (tools) for the agent:
    - `search`: Searches the web using DuckDuckGo.
    - `read_url`: Reads the content of a URL using Requests and BeautifulSoup.

## Usage

1. Install dependencies:
   ```bash
   pip install claude-agent-sdk duckduckgo-search requests beautifulsoup4
   ```

2. Run the agent:
   ```bash
   python agent.py
   ```
