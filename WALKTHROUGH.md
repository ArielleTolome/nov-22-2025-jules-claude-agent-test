# Code Walkthrough

This guide explains the internal working of the Research Agent.

## Overview

The project consists of two main Python files:
1. `agent.py`: Configures and runs the Claude agent.
2. `research_skills.py`: Defines the tools (skills) the agent can use.

## Detailed Analysis

### 1. Defining Skills (`research_skills.py`)

This file defines the capabilities of the agent using the Model Context Protocol (MCP).

#### Tools
Two tools are defined using the `@tool` decorator from `claude_agent_sdk`.

- **`search`**:
  - Uses `duckduckgo_search.DDGS` to perform web searches.
  - It runs the synchronous `DDGS` call in a separate thread using `loop.run_in_executor` to prevent blocking the async event loop.
  - Returns a list of search results.

- **`read_url`**:
  - Uses `httpx.AsyncClient` to fetch the HTML content of a given URL asynchronously.
  - Uses `BeautifulSoup` to parse the HTML and extract text.
  - Limits the output to the first 5000 characters to manage context window usage.

#### MCP Server
The tools are bundled into a server object:
```python
research_server = create_sdk_mcp_server(
    name="research_skills",
    version="1.0.0",
    tools=[search, read_url]
)
```
This `research_server` object is imported by `agent.py`.

### 2. The Agent Logic (`agent.py`)

This file sets up the agent environment and executes the task.

#### Configuration
The `ClaudeAgentOptions` are used to configure the agent:
```python
options = ClaudeAgentOptions(
    mcp_servers={
        "research": research_server
    },
    system_prompt="...",
    max_turns=10
)
```
- `mcp_servers`: Registers the `research_server` we defined, making the `search` and `read_url` tools available to the agent.
- `system_prompt`: Gives the agent its persona and instructions.

#### Execution Loop
The `main` function runs the agent:
1. **Initialization**: `ClaudeSDKClient` is initialized with the options.
2. **Query**: `client.query(...)` sends the initial instruction to the agent ("Research the latest news about DeepSeek AI...").
3. **Response Handling**: The code iterates through the response stream:
   ```python
   async for message in client.receive_response():
       if isinstance(message, AssistantMessage):
           # Print the agent's text response
   ```

   Behind the scenes, if the agent decides to use a tool (like `search`), the SDK handles the tool execution request, runs the function from `research_skills.py`, and feeds the result back to the agent. The agent then continues its thought process or provides a final answer.

## Flow of Operations

1. **Start**: `python agent.py` is executed.
2. **Init**: Agent initializes with "research" tools enabled.
3. **Prompt**: "Research DeepSeek AI".
4. **Reasoning**: Agent realizes it needs information and decides to call `search(query="DeepSeek AI news")`.
5. **Tool Execution**: The `search` function in `research_skills.py` runs and returns URLs.
6. **Reasoning**: Agent picks a relevant URL and decides to call `read_url(url=...)`.
7. **Tool Execution**: The `read_url` function fetches and parses the page, returning text.
8. **Synthesis**: Agent processes the text and generates a summary.
9. **Output**: The summary is printed to the console.
