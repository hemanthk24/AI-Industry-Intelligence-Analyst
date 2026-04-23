import time
import arxiv

def fetch_arxiv(
    query_list=["Machine Learning", "Artificial Intelligence", "LLM", "NLP"],
    max_results=3
):
    """
    Fetch latest AI/ML papers from arXiv
    """

    search = arxiv.Search(
        query=" OR ".join(query_list),
        max_results=max_results,
        sort_by=arxiv.SortCriterion.SubmittedDate
    )

    client = arxiv.Client()

    result_text = ""

    try:
        for result in client.results(search=search):
            result_text += f"""
Title: {result.title}
Summary: {result.summary}
Link: {result.entry_id}
"""
            time.sleep(1)

        return result_text.strip()

    except Exception as e:
        return f"Error fetching arXiv data: {str(e)}"


# Test
if __name__ == "__main__":
    print(fetch_arxiv())