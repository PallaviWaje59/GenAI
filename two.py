"""
01 - TOOL CALLING (Ollama)
--------------------------

COLLEGE NOTICE BOARD

The LLM DECIDES which tool to call.
Our Python code ACTUALLY runs the tool.
Then we send the result back to the model.

Run:

    python 01_tool_calling.py
"""

from langchain_ollama import ChatOllama
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, ToolMessage


# --------------------------------------------------
# 1. Define normal Python functions as "tools"
# --------------------------------------------------

@tool
def get_latest_notices() -> str:
    """Get the latest notices from the college notice board."""

    notices = [
        "1. MCA Semester 3 internal examination starts from 15 September.",
        "2. College fees must be paid before 10 September.",
        "3. Placement drive by Tech Solutions on 12 September.",
        "4. Workshop on Artificial Intelligence on 18 September.",
    ]

    return "\n".join(notices)


@tool
def search_notice(keyword: str) -> str:
    """Search college notices using a keyword such as exam, fees, placement, or workshop."""

    notices = {
        "exam": "MCA Semester 3 internal examination starts from 15 September.",
        "fees": "College fees must be paid before 10 September.",
        "placement": "Placement drive by Tech Solutions on 12 September.",
        "workshop": "Workshop on Artificial Intelligence on 18 September.",
    }

    return notices.get(
        keyword.lower(),
        "No notice found for this keyword."
    )


@tool
def get_notice_by_department(department: str) -> str:
    """Get notices related to a particular department."""

    department_notices = {
        "mca": "MCA: Internal examination starts from 15 September.",
        "bca": "BCA: Assignment submission deadline is 12 September.",
        "bsc it": "BSc IT: Database practical examination is on 20 September.",
    }

    return department_notices.get(
        department.lower(),
        "No notices available for this department."
    )


# List of available tools
tools = [
    get_latest_notices,
    search_notice,
    get_notice_by_department
]


# --------------------------------------------------
# 2. Load local Ollama model and attach tools
# --------------------------------------------------

llm = ChatOllama(
    model="llama3.2",
    temperature=0
)

llm_with_tools = llm.bind_tools(tools)


# --------------------------------------------------
# 3. Ask a question that needs a tool
# --------------------------------------------------

question = """
I am an MCA student.

Tell me about the latest placement notice
and also tell me all the latest notices.
"""

messages = [
    HumanMessage(content=question)
]


response = llm_with_tools.invoke(messages)

print("\nModel wants to call these tools:")
print(response.tool_calls)

messages.append(response)


# --------------------------------------------------
# 4. Run the tools selected by the AI
# --------------------------------------------------

tool_lookup = {
    t.name: t for t in tools
}


for call in response.tool_calls:

    tool_fn = tool_lookup[call["name"]]

    result = tool_fn.invoke(call["args"])

    print(
        f"\nRan tool '{call['name']}' "
        f"with args {call['args']} "
        f"-> {result}"
    )

    # Send the tool result back to the AI
    messages.append(
        ToolMessage(
            content=str(result),
            tool_call_id=call["id"]
        )
    )


# --------------------------------------------------
# 5. Ask the model for the final answer
# --------------------------------------------------

final = llm_with_tools.invoke(messages)

print("\nFINAL ANSWER:\n")
print(final.content)