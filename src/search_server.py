import requests
import os
from dotenv import load_dotenv

load_dotenv()

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

def web_search(query: str):
    """
    Perform web search using Tavily API
    """

    url = "https://api.tavily.com/search"

    payload = {
        "api_key": TAVILY_API_KEY,
        "query": query,
        "search_depth": "basic",
        "max_results": 3
    }

    try:
        response = requests.post(url, json=payload)
        data = response.json()

        result_text = ""

        for item in data.get("results", []):
            result_text += f"""
Title: {item['title']}
Content: {item['content']}
URL: {item['url']}
"""

        return result_text.strip()

    except Exception as e:
        return f"Error fetching search results: {str(e)}"


# Test
if __name__ == "__main__":
    print(web_search("latest AI news"))