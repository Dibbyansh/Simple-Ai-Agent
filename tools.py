from pathvalidate import sanitize_filename
from datetime import datetime
import textwrap

from langchain_community.tools import DuckDuckGoSearchRun, WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain_core.tools import tool


# 🔹 Tool: Save research result to file
@tool("save_tool")
def save_tool(data: str, filename: str = "output.txt") -> str:
    """
    Save research summary to a local text file.
    """
    
    # 🔥 Clean filename (important for OS compatibility)
    filename = sanitize_filename(filename, replacement_text="_")
    # 🔥 Wrap text to make it readable (avoid long single line)
    wrapped_data = textwrap.fill(data, width=80)
    
    # 🔹 Format content
    content = f"""=== Research Summary ===
Time: {datetime.now()}
--------------
{wrapped_data}
"""

    # 🔹 Write to file
    with open(filename, "a", encoding="utf-8") as f:
        f.write(content)

    return f"Saved to {filename}"


# 🔹 Tool: Web search
search_tool = DuckDuckGoSearchRun(name="web_search")


# 🔹 Tool: Wikipedia search
wiki = WikipediaAPIWrapper(top_k_results=1)
wiki_tool = WikipediaQueryRun(api_wrapper=wiki, name="wikipedia_search")