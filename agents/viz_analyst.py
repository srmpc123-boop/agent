import os
import sys
import time
import re

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.llm_pick import pick_llm
from utils.etl_tools import ETLTools
from Models.schema import VizAgentSchema
from langchain_core.messages import AIMessage, HumanMessage
from langgraph.graph import StateGraph, START, END


def generate_chart_node(state: VizAgentSchema) -> VizAgentSchema:
    message = state.messages[-1].content
    llm = pick_llm("medium")

    viz_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data', 'visualizations'))
    os.makedirs(viz_dir, exist_ok=True)
    
    chart_filename = f"chart_{int(time.time())}.png"
    full_chart_path = os.path.join(viz_dir, chart_filename)

    prompt = f"""
    You are a Data Visualization Engineer using Python (Matplotlib and Seaborn).
    Generate standalone Python code that creates a high-quality visualization based on the user's request:
    "{message}"

    Rules:
    1. The code MUST save the generated chart image to: '{full_chart_path.replace('\\', '/')}'
    2. Set a modern theme (e.g. sns.set_theme(style='darkgrid')).
    3. Include title, axis labels, legends, and call plt.tight_layout().
    4. Call plt.savefig('{full_chart_path.replace('\\', '/')}', dpi=150, bbox_inches='tight') and then plt.close().
    5. Output ONLY executable Python code within standard markdown blocks. No explanations.
    """

    response = llm.invoke(prompt).content
    code_match = re.search(r'```python\s*(.*?)\s*```', response, re.DOTALL)
    if code_match:
        chart_code = code_match.group(1).strip()
    else:
        chart_code = response.strip().strip('```').strip().lstrip('python').strip()

    etl_tools = ETLTools()
    exec_result = etl_tools.execute_code(chart_code)

    state.chart_code = chart_code
    state.chart_image_path = full_chart_path if os.path.exists(full_chart_path) else ""
    state.summary = f"Chart generated and saved to {full_chart_path}. Execution status: {exec_result}"
    state.messages = state.messages + [AIMessage(content=state.summary)]

    return state


viz_graph = StateGraph(VizAgentSchema)
viz_graph.add_node("generate_chart_node", generate_chart_node)
viz_graph.add_edge(START, "generate_chart_node")
viz_graph.add_edge("generate_chart_node", END)

viz_analyst = viz_graph.compile()

if __name__ == "__main__":
    result = viz_analyst.invoke({
        "messages": [HumanMessage(content="Create a bar chart of top 5 car make distribution with sample data [Toyota: 450, Honda: 380, Ford: 310, Chevrolet: 290, BMW: 150]")]
    })
    print(result["summary"])
