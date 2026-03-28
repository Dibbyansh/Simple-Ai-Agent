from dotenv import load_dotenv
from pydantic import BaseModel
from langchain_core.messages import HumanMessage
from langchain_openrouter import ChatOpenRouter
from langgraph.prebuilt import create_react_agent

from tools import search_tool, wiki_tool, save_tool

load_dotenv()


class ResearchResult(BaseModel):
    topic: str
    summary: str
    sources: list[str]
    tools_used: list[str]


llm = ChatOpenRouter(model="stepfun/step-3.5-flash:free")
tools = [search_tool, wiki_tool, save_tool]

SYSTEM_PROMPT = """You are a research assistant that helps produce research summaries.

Use your tools when they improve the answer:
- Web search for recent or niche facts.
- Wikipedia for broad, stable background.
- After every answer, call save_tool with the full summary and filename='topicofthesearch'.txt”
Be concise in tool queries. After tools return, synthesize a clear answer.

A separate step will turn your work into structured fields (topic, summary, sources, tools_used).
List only real URLs or titles in sources. In tools_used, use the exact tool names you invoked."""


def main() -> None:
    agent = create_react_agent(
        llm,
        tools,
        prompt=SYSTEM_PROMPT,
        response_format=ResearchResult,
    )

    query = input("What can i help you research? ")
    result = agent.invoke({"messages": [HumanMessage(content=query)]})

    structured = result.get("structured_response")
    if structured is not None:
        print(structured)
        return

    for msg in reversed(result["messages"]):
        if msg.type == "ai":
            print(msg.content)
            return


if __name__ == "__main__":
    main()