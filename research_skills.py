from claude_agent_sdk import tool, create_sdk_mcp_server
from duckduckgo_search import DDGS
import httpx
from bs4 import BeautifulSoup
import logging
import asyncio

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@tool(
    name="search",
    description="Search the web for a query.",
    input_schema={
        "type": "object",
        "properties": {
            "query": {"type": "string", "description": "The search query"}
        },
        "required": ["query"]
    }
)
async def search(input_data: dict) -> dict:
    query = input_data["query"]
    logger.info(f"Searching for: {query}")
    try:
        # DDGS is synchronous, run in executor to avoid blocking
        loop = asyncio.get_event_loop()
        results = await loop.run_in_executor(None, lambda: list(DDGS().text(query, max_results=5)))
        return {"results": results}
    except Exception as e:
        logger.error(f"Search failed: {e}")
        return {"error": str(e)}

@tool(
    name="read_url",
    description="Read the content of a URL.",
    input_schema={
        "type": "object",
        "properties": {
            "url": {"type": "string", "description": "The URL to read"}
        },
        "required": ["url"]
    }
)
async def read_url(input_data: dict) -> dict:
    url = input_data["url"]
    logger.info(f"Reading URL: {url}")
    try:
        async with httpx.AsyncClient(follow_redirects=True) as client:
            response = await client.get(url, timeout=10)
            response.raise_for_status()
            content = response.content

        soup = BeautifulSoup(content, 'html.parser')

        # Extract text and clean it up
        text = soup.get_text(separator='\n', strip=True)

        # Limit the text length to avoid token limits
        return {"content": text[:5000]}
    except Exception as e:
        logger.error(f"Read URL failed: {e}")
        return {"error": str(e)}

# Create the MCP server config
research_server = create_sdk_mcp_server(
    name="research_skills",
    version="1.0.0",
    tools=[search, read_url]
)
