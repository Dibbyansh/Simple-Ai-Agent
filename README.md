# 🤖 AI Research Agent

A simple AI agent that performs research using tools and returns **structured, concise results**.

---

## 🚀 Features

* 🔍 Web + Wikipedia search
* 🧠 ReAct AI agent (tool usage)
* 📦 Structured output using Pydantic
* ✂️ Short summaries (~120 words)
* 💾 Optional save to file

---

## 🧠 How it works

```text
User Input
   ↓
AI Agent (uses tools)
   ↓
Raw Output
   ↓
Formatter (structured result)
   ↓
Clean Output + Save Option
```

---

## 📌 Example

```text
Enter your research topic: cats

Topic: Domestic Cats

Summary:
Short, concise explanation...

Sources: Wikipedia, Web Search
Tools used: wikipedia_search, web_search
```

---

## 🛠 Tech

* Python
* LangChain
* OpenRouter
* Pydantic

---
