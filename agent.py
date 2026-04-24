from openai import OpenAI
import os
import json
from dotenv import load_dotenv
from tools import fetch_ai_repos, fetch_arxiv, web_search
from functools import lru_cache

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# CACHING (important for speed)
@lru_cache(maxsize=20)
def cached_arxiv():
    return fetch_arxiv()

@lru_cache(maxsize=20)
def cached_github():
    return fetch_ai_repos()

@lru_cache(maxsize=20)
def cached_search(query):
    return web_search(query)



# TOOL ROUTER (extra control)
def route_tool(query):
    query = query.lower()

    if "github" in query or "repo" in query:
        return ["fetch_ai_repos"]

    elif "paper" in query or "research" in query:
        return ["fetch_arxiv"]

    elif "news" in query or "latest" in query:
        return ["web_search"]

    return []


# TOOL DEFINITIONS (LLM)
tools = [
    {
        "type": "function",
        "function": {
            "name": "fetch_ai_repos",
            "description": "Get latest AI GitHub repositories",
            "parameters": {"type": "object", "properties": {}}
        }
    },
    {
        "type": "function",
        "function": {
            "name": "fetch_arxiv",
            "description": "Get latest AI research papers",
            "parameters": {"type": "object", "properties": {}}
        }
    },
    {
        "type": "function",
        "function": {
            "name": "web_search",
            "description": "Search latest AI news",
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
# MAIN AGENT
# -------------------------------
def run_agent(user_query, chat_history):

    # -------------------------------
    # Step 1: Optional pre-routing
    # -------------------------------
    forced_tools = route_tool(user_query)

    # -------------------------------
    # Step 2: LLM decides tools
    # -------------------------------
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {
                "role": "system",
                "content": """
                You are a production-level AI Intelligence Agent.

                - Use tools only when needed
                - Prefer combining multiple tools if relevant
                - Return structured output
                """
            },
            *chat_history,
            {"role": "user", "content": user_query}
        ],
        tools=tools,
        tool_choice="auto"
    )

    message = response.choices[0].message

    tool_messages = []

    # -------------------------------
    # Step 3: Execute tools
    # -------------------------------
    try:
        if message.tool_calls:

            for tool_call in message.tool_calls:
                name = tool_call.function.name

                args = {}
                if tool_call.function.arguments:
                    try:
                        args = json.loads(tool_call.function.arguments)
                    except:
                        pass

                # Cached execution
                if name == "fetch_arxiv":
                    result = cached_arxiv()

                elif name == "fetch_ai_repos":
                    result = cached_github()

                elif name == "web_search":
                    result = cached_search(args.get("query", user_query))

                else:
                    result = "Unknown tool"

                tool_messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": str(result)
                })

        # fallback if LLM didn't call tool but router suggests
        elif forced_tools:
            for t in forced_tools:
                if t == "fetch_arxiv":
                    result = cached_arxiv()
                elif t == "fetch_ai_repos":
                    result = cached_github()
                elif t == "web_search":
                    result = cached_search(user_query)

                tool_messages.append({
                    "role": "tool",
                    "tool_call_id": "fallback",
                    "content": result
                })

    except Exception as e:
        tool_messages.append({
            "role": "tool",
            "tool_call_id": "error",
            "content": f"Tool error: {str(e)}"
        })

    # -------------------------------
    # Step 4: Final response
    # -------------------------------
    final = client.chat.completions.create(
    model="gpt-4.1-mini",
    messages=[
                {
                "role": "system",
                "content": """
            You are an AI Industry Intelligence Analyst.

            Generate a clean, structured response based ONLY on available data.

            Rules:
            - Include a section ONLY if relevant data exists
            - Do NOT hallucinate or create fake content
            - Do NOT repeat the same information
            - Merge similar information instead of duplicating
            - Keep response concise but informative
            - Only generate sections if corresponding tool data is present
            - Use ONLY the provided tool outputs

            IMPORTANT:
            - If user asks for "explain", "detail", or "more info":
            → Expand the explanation significantly
            → Explain purpose, use-case, and what the project does
            → Add possible applications and real-world usage
            → Do NOT just repeat the same summary

            Format:

            📰 News:
            - Only if web search data is available
            - Summarize key updates in 2–3 bullet points

            📑 Research Papers:
            - Include title + 1–2 line summary
            - If asked in detail → explain methodology and significance

            💻 GitHub Projects:
            - Include repo name + short description
            - If asked in detail → explain:
            • what the project does  
            • key features  
            • possible use cases  

            🔍 Key Insights:
            - 2–3 high-level observations from all data

            If a section has no data → SKIP it completely.
            """
            },
            *chat_history,
            {"role": "user", "content": user_query},
            message,
            *tool_messages
        ]
    )

    return final.choices[0].message.content