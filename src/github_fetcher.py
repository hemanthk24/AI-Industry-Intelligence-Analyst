import requests
from datetime import datetime, timedelta, UTC

def fetch_ai_repos():
    """
    Fetch recently updated AI-related GitHub repositories
    """

    date = (datetime.now(UTC) - timedelta(days=3)).strftime("%Y-%m-%d")

    query = "AI OR LLM OR 'machine learning' OR 'deep learning' OR NLP OR 'computer vision'"

    url = f"https://api.github.com/search/repositories?q={query}+pushed:>{date}&sort=updated&order=desc&per_page=3"

    try:
        response = requests.get(url)
        data = response.json()

        if "items" not in data:
            return f"Error fetching GitHub data: {data}"

        result_text = ""

        for repo in data["items"]:
            result_text += f"""
Name: {repo['full_name']}
Description: {repo['description']}
URL: {repo['html_url']}
"""

        return result_text.strip()

    except Exception as e:
        return f"Error: {str(e)}"


# Test
if __name__ == "__main__":
    print(fetch_ai_repos())