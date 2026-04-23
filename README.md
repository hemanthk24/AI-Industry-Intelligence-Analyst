# AI Industry Intelligence Analyst

## Overview
**AI Industry Intelligence Analyst** is an agentic AI system designed to analyze and summarize the latest developments in artificial intelligence and machine learning. The system integrates real-time data from **GitHub repositories** and **arXiv research papers**, using a Large Language Model (LLM) to generate structured, human-readable insights.

Unlike traditional applications, this project follows an **agent-based architecture** where the model dynamically decides which tools to use, enabling adaptive and context-aware responses.

---

## Problem Statement
With the rapid growth of AI research and open-source development, it has become increasingly difficult to stay updated. Information is scattered across various platforms, making manual tracking inefficient. 

This project addresses this by building an intelligent agent that:
* **Aggregates** data from multiple live sources.
* **Filters and organizes** relevant information.
* **Generates** concise, newsletter-style insights for users.

---

## Key Features

* **Agentic AI Architecture:** The LLM acts as the central brain, determining when to call external tools and how to synthesize their outputs.
* **MCP-Style Tool Integration:** Simulates Model Context Protocol (MCP) behavior by exposing local Python functions as tools via dynamic function calling.
* **Multi-Source Integration:** * **GitHub:** Fetches trending or recent AI/ML repositories.
    * **arXiv:** Retrieves the latest research papers and abstracts.
* **Conversational Interface:** Built with **Streamlit**, allowing users to interact naturally and ask follow-up questions.
* **Context Awareness:** The agent maintains conversation history for a continuous dialogue experience.

---

## System Architecture

```mermaid
graph TD
    User((User Query)) --> UI[Streamlit Chat Interface]
    UI --> LLM[LLM Agent Controller]
    LLM --> Tools{Tool Selection}
    
    subgraph External_Tools [MCP-Style Tools]
        Tools --> GH[GitHub Fetcher]
        Tools --> AX[arXiv Fetcher]
        Tools --> SH[Search Tool]
    end

    GH --> Data[(Data Retrieval)]
    AX --> Data
    SH --> Data
    
    Data --> LLM_Response[LLM Synthesis]
    LLM_Response --> UI

## Project Structure

## Project Structure

```text
ai_industry_intelligence_analyst/
│
├── app.py                  # Streamlit chatbot UI
├── agent.py                # Core agent logic and tool handling
├── tools.py                # Tool definitions (MCP-style abstraction)
├── server.py               # Tool server / Search integration logic
│
├── src/
│   ├── github_fetcher.py   # GitHub API integration
│   ├── arxiv_fetcher.py    # arXiv API integration
│   └── search_tool.py      # Web search integration
│
├── .env                    # API keys (Configuration)
├── pyproject.toml          # Dependency management (uv)
└── README.md


## Technologies Used
- Python 3.10+
- Streamlit (UI Framework)
- OpenAI API (LLM & Function Calling)
- GitHub REST API
- arXiv API
- uv (Fast Python package manager)

## Installation and Setup

### 1. Clone the Repository
```bash
git clone [https://github.com/hemanthk24/AI-Industry-Intelligence-Analyst.git](https://github.com/hemanthk24/AI-Industry-Intelligence-Analyst.git)
cd AI-Industry-Intelligence-Analyst
```

Here is that specific section formatted in clean, standard Markdown for your README.md:

Markdown
## Installation and Setup

### 1. Clone the Repository
```bash
git clone [https://github.com/hemanthk24/AI-Industry-Intelligence-Analyst.git](https://github.com/hemanthk24/AI-Industry-Intelligence-Analyst.git)
cd AI-Industry-Intelligence-Analyst
2. Install Dependencies
This project uses uv for lightning-fast dependency management.
```
```Bash
uv sync
```
3. Configure Environment Variables
```
Create a .env file in the root directory and add your OpenAI API key:
```
```Code snippet
OPENAI_API_KEY=your_api_key_here
```
4. Run the Application
```Bash
uv run streamlit run app.py
```
## Usage
- Open the Streamlit URL provided in your terminal (usually http://localhost:8501).

- Interact with the agent using natural language:

- "What are the latest AI trends on GitHub?"

- "Create a newsletter based on today's machine learning papers."

- "Explain the recent breakthroughs in LLM research."

## How It Works
- **Intent Analysis:** The LLM parses the user's prompt to see if it needs external data.

- **Tool Execution:** If required, the LLM triggers get_github_data or get_arxiv_data.

- **Synthesis:** The LLM receives the raw JSON/data from the tools and transforms it into a structured, user-friendly format (Markdown tables, bullet points, etc.).

- **Multi-Tool Handling:** The agent can call multiple tools in a single turn if the query requires data from both GitHub and arXiv.

## Future Improvements

- **Enhanced Filtering:** Implementing better ranking logic for GitHub repositories.

- **Persistent Memory:** Adding a database (like SQLite or ChromaDB) to store historical insights.

- **Expanded Sources:** Integrating News APIs, X (Twitter) tech trends, and Hugging Face.

- **Caching:** Reducing API latency and costs by caching frequent queries.

## Conclusion
This project demonstrates a practical implementation of Agentic AI and MCP concepts. By moving beyond simple prompting and into dynamic tool orchestration, it provides a powerful way to navigate the rapidly evolving AI landscape.