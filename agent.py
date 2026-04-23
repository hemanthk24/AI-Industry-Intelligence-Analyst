# agent.py

from openai import OpenAI
import os
import json
from dotenv import load_dotenv
from tools import fetch_ai_repos, fetch_arxiv, web_search

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# -------------------------------
# TOOL DEFINITIONS (LLM SIDE)
# -------------------------------
tools = [
    {
        "type": "function",
        "function": {
            "name": "fetch_ai_repos",
            "description": "Fetch latest AI GitHub repositories",
            "parameters": {"type": "object", "properties": {}}
        }
    },
    {
        "type": "function",
        "function": {
            "name": "fetch_arxiv",
            "description": "Fetch latest AI research papers",
            "parameters": {"type": "object", "properties": {}}
        }
    },
    {
        "type": "function",
        "function": {
            "name": "web_search",
            "description": "Search the web for latest AI news or information",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string"}
                },
                "required": ["query"]
            }
        }
    }
]


# -------------------------------
# AGENT FUNCTION
# -------------------------------
def run_agent(user_query):

    # Step 1: LLM decides tool
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {
                "role": "system",
                "content": """
                You are an AI Industry Intelligence Analyst.

                Use tools when:
                - GitHub repos → fetch_ai_repos
                - Research papers → fetch_arxiv
                - Latest news / current info → web_search

                Otherwise answer normally.
                """
            },
            {"role": "user", "content": user_query}
        ],
        tools=tools,
        tool_choice="auto"
    )

    message = response.choices[0].message

    # -------------------------------
    # TOOL EXECUTION
    # -------------------------------
    if message.tool_calls:

        tool_messages = []

        for tool_call in message.tool_calls:
            tool_name = tool_call.function.name

            # Default args
            args = {}

            # Parse arguments if present
            if tool_call.function.arguments:
                try:
                    args = json.loads(tool_call.function.arguments)
                except:
                    args = {}

            # Execute correct tool
            if tool_name == "fetch_ai_repos":
                result = fetch_ai_repos()

            elif tool_name == "fetch_arxiv":
                result = fetch_arxiv()

            elif tool_name == "web_search":
                result = web_search(args.get("query", user_query))

            else:
                result = "Unknown tool"

            tool_messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": str(result)
            })

        # Step 3: Final response with tool results
        final_response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {
                    "role": "system",
                    "content": "Provide a clean, structured and concise response."
                },
                {"role": "user", "content": user_query},
                message,
                *tool_messages
            ]
        )

        return final_response.choices[0].message.content

    # NO TOOL CASE
    else:
        return message.content