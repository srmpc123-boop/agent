import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.llm_pick import pick_llm
from Models.schema import RouterSchema, DataAgentSchema
from langchain_core.messages import AIMessage, HumanMessage
from langgraph.graph import StateGraph, START, END
from agents.etl_analyst import etl_analyst
from agents.sql_analyst import sql_analyst
from agents.viz_analyst import viz_analyst


llm = pick_llm("claude")
llm_router = llm.with_structured_output(RouterSchema)


# ---------------------------- DATA AGENT GRAPH ---------------------------- #


def router_node(state: DataAgentSchema):
    message = state.messages[-1].content
    route_response_dict = llm_router.invoke(message).model_dump()
    route_response = route_response_dict['answer']
    state.route_response = route_response
    return state


def etl_node(state: DataAgentSchema):
    message = state.messages[-1].content
    response = etl_analyst.invoke({"messages": [HumanMessage(content=message)]})
    last_msg = response["messages"][-1]
    msg_content = last_msg.content if hasattr(last_msg, 'content') else str(last_msg)
    state.messages = state.messages + [AIMessage(content=msg_content)]
    return state


def sql_node(state: DataAgentSchema):
    message = state.messages[-1].content
    input_schema = {
        "messages": [],
        "user_question": message,
        "curated_ques": "",
        "prompt_query_context": "",
        "generated_sql_query": "",
        "is_safe": "No",
        "comments": "",
        "sql_query_execution_result": "",
        "sql_retry_count": 0,
        "sql_error_message": "",
        "chart_image_path": "",
        "final_answer": ""
    }

    response = sql_analyst.invoke(input_schema)
    final_ans = response.get("final_answer", "")
    if not final_ans:
        last_msg = response.get("messages", [])[-1] if response.get("messages") else ""
        final_ans = last_msg.content if hasattr(last_msg, 'content') else str(last_msg)

    state.messages = state.messages + [AIMessage(content=final_ans)]
    return state


def viz_node(state: DataAgentSchema):
    message = state.messages[-1].content
    response = viz_analyst.invoke({"messages": [HumanMessage(content=message)]})
    summary = response.get("summary", "")
    state.messages = state.messages + [AIMessage(content=summary)]
    return state


data_agent_graph = StateGraph(DataAgentSchema)

data_agent_graph.add_node("router_node", router_node)
data_agent_graph.add_node("etl_node", etl_node)
data_agent_graph.add_node("sql_node", sql_node)
data_agent_graph.add_node("viz_node", viz_node)

data_agent_graph.add_edge(START, "router_node")


def route_edge(state: DataAgentSchema) -> str:
    if state.route_response == "sql":
        return "sql_node"
    elif state.route_response == "etl":
        return "etl_node"
    elif state.route_response == "viz":
        return "viz_node"
    else:
        raise ValueError(f"Invalid route response: {state.route_response}")


data_agent_graph.add_conditional_edges("router_node", route_edge,
                                      {
                                          "sql_node": "sql_node",
                                          "etl_node": "etl_node",
                                          "viz_node": "viz_node"
                                      })

data_agent_graph.add_edge("sql_node", END)
data_agent_graph.add_edge("etl_node", END)
data_agent_graph.add_edge("viz_node", END)

data_agent = data_agent_graph.compile()


# Optional|
from IPython.display import display, Image
img = Image(data_agent.get_graph().draw_mermaid_png())
with open("data_agent_graph.png", "wb") as f:
    f.write(img.data)



if __name__ == "__main__":

    response = data_agent.invoke(
        {"messages":[HumanMessage(content="I want to extract the data from the API endpoint 'https://pokeapi.co/api/v2/pokemon' and save it to data/extract folder in the csv folder")],
         "route_response": ""}
    )

    print(response)