import asyncio
import logging
from claude_agent_sdk import ClaudeSDKClient, ClaudeAgentOptions, AssistantMessage, UserMessage, TextBlock
from research_skills import research_server

# Configure logging
logging.basicConfig(level=logging.INFO)

async def main():
    # Initialize the client with the research skill
    options = ClaudeAgentOptions(
        mcp_servers={
            "research": research_server
        },
        system_prompt="You are a helpful research assistant. Use the available tools to research topics.",
        max_turns=10
    )

    async with ClaudeSDKClient(options=options) as client:
        print("Agent initialized. Starting research on 'DeepSeek AI'...")

        # Start the conversation
        await client.query(prompt="Research the latest news about DeepSeek AI and summarize it.")

        async for message in client.receive_response():
            if isinstance(message, AssistantMessage):
                 for block in message.content:
                    if isinstance(block, TextBlock):
                        print(f"\nAssistant: {block.text}\n")
            elif isinstance(message, UserMessage):
                 pass

if __name__ == "__main__":
    asyncio.run(main())
