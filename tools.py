from src.arxiv_fetcher import fetch_arxiv
from src.github_fetcher import fetch_ai_repos
from src.search_server import web_search

# Optional: tool registry (useful later)
TOOLS = {
    "fetch_arxiv": fetch_arxiv,
    "fetch_ai_repos": fetch_ai_repos,
    "web_search": web_search
}