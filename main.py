from agents.data_agent import data_agent
from langchain_core.messages import HumanMessage

if __name__ == "__main__":
    response = data_agent.invoke(
        {"messages":[HumanMessage(content="List the tables of the database and explain the schema of the 'rides' table")],
         "route_response": ""}
    )

    print(response.get("messages")[-1].content)