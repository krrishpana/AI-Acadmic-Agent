from langchain_core.messages import HumanMessage, AIMessage

import prompts
from graph_agent import rag_agent

TOOL_INSTRUCTIONS = """
You are an AI Academic Agent. You have access to specialized tools:
- search_notes: Searches the student's vector store notes for specific information.
- summarize_notes: Summarizes relevant context blocks from the vector database.
- create_quiz: Generates conceptual quizzes on topics.
- generate_flashcards: Generates active recall flashcards.
- study_plan: Creates structured study schedules.

Use your tools whenever appropriate to fulfill the user's intent.

CRITICAL CITATION RULE:
Whenever you use the 'search_notes' tool to answer a question, you MUST include a "Sources:" section at the very end of your response, listing the exact PDF filenames and page numbers provided in the tool output.
"""


def build_system_prompt(persona: str) -> str:
    return f"{prompts.get_persona(persona)}\n\n{TOOL_INSTRUCTIONS}"


def chat(message: str, thread_id: str, persona: str = "1") -> dict:
    run_config = {
        "configurable": {"thread_id": thread_id},
        "recursion_limit": 10,
    }

    # How many messages are already saved for this thread?
    old_count = len(rag_agent.get_state(run_config).values.get("messages", []))

    result = rag_agent.invoke(
        {
            "messages": [HumanMessage(content=message)],
            "system_prompt": build_system_prompt(persona),
        },
        config=run_config,
    )

    # Only the messages added in THIS turn
    new_messages = result["messages"][old_count:]

    tools_used = []
    for msg in new_messages:
        if isinstance(msg, AIMessage):
            for call in msg.tool_calls:
                tools_used.append(call["name"])

    return {
        "answer": result["messages"][-1].text,
        "tools_used": tools_used,
    }