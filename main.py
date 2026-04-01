import os
from dotenv import load_dotenv
from pydantic import BaseModel
from langchain_openrouter import ChatOpenRouter
from langchain_core.messages import HumanMessage
from langchain.agents import create_agent

from tools import search_tool, wiki_tool, save_tool

# 🔹 Load environment variables (.env file)
load_dotenv()

# 🔹 Model name stored in .env
MODEL = os.getenv("MODEL")


# 🔹 Define structured output format (final result schema)
class ResearchResult(BaseModel):
    topic: str
    summary: str
    sources: list[str]
    tools_used: list[str]


# 🔹 Helper: get last AI response from agent messages
def _last_ai_text(messages) -> str | None:
    for msg in reversed(messages):
        if getattr(msg, "type", None) == "ai" and msg.content:
            return msg.content
    return None


def main() -> None:
    # 🔹 Step 1: Initialize LLM
    llm = ChatOpenRouter(model=MODEL)

    # 🔹 Step 2: Register tools (agent can use these)
    tools = [search_tool, wiki_tool]

    # 🔹 Step 3: Define agent behavior
    system_prompt = """You are a research assistant.
    Use web_search for recent information and wikipedia_search for general background.
    Answer clearly and mention sources."""

    # 🔹 Step 4: Create agent (ReAct style)
    agent = create_agent(llm, tools, system_prompt=system_prompt)

    # 🔹 Step 5: Take user input
    query = input("Enter your research topic: ").strip()
    if not query:
        print("Please enter something.")
        return

    # 🔹 Step 6: Run agent → generates raw research output
    result = agent.invoke({"messages": [HumanMessage(content=query)]})

    # 🔹 Step 7: Extract last AI response
    raw = _last_ai_text(result["messages"])
    if not raw:
        print("Failed to generate a response.")
        return

    # 🔹 Step 8: Convert raw output → structured format
    # This ensures consistent output (topic, summary, etc.)
    formatter = llm.with_structured_output(ResearchResult)

    structured = formatter.invoke(
        "Convert this research into the required structured format. "
        "Summary under 120 words, concise.\n\n" + str(raw)
    )

    # 🔹 Step 9: Handle failure safely
    if structured is None:
        print("Structured output failed. Raw response:\n")
        print(raw)
        return

    # 🔹 Step 10: Display clean output
    print("\n=== RESULT ===\n")
    print(f"Topic: {structured.topic}\n")
    print(f"Summary:\n{structured.summary}\n")
    print(f"Sources: {', '.join(structured.sources)}\n")
    print(f"Tools used: {', '.join(structured.tools_used)}")

    # 🔹 Step 11: Ask user if they want to save result
    if input("\nSave to file? (y/n): ").strip().lower() == "y":
        filename = structured.topic.replace(" ", "_") + ".txt"

        # Call save tool manually
        save_tool.invoke({
            "data": structured.summary,
            "filename": filename
        })

        print("Saved.")
    else:
        print("Not saved.")


# 🔹 Entry point
if __name__ == "__main__":
    main()