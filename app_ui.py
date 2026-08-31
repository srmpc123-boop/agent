import os
import sys
import time
import glob
import streamlit as st
from langchain_core.messages import HumanMessage

sys.path.append(os.path.dirname(__file__))

from agents.data_agent import data_agent
from utils.database import DatabaseUtil
from evals.run_evals import BENCHMARK_CASES

st.set_page_config(
    page_title="Agentic AI Data Agent",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 Agentic AI Data Agent Dashboard")
st.caption("Stateful Multi-Agent System powered by LangGraph, Groq, PostgreSQL, and Pandas")

# Sidebar Configuration
st.sidebar.header("⚙️ Agent Configuration")
provider = st.sidebar.selectbox("LLM Provider", ["groq", "openai", "anthropic"], index=0)
os.environ["LLM_PROVIDER"] = provider

if provider == "groq":
    st.sidebar.info("Free High-Speed LPU Inference")
    model_low = st.sidebar.text_input("Low Model", "llama-3.1-8b-instant")
    model_med = st.sidebar.text_input("Medium/High Model", "llama-3.3-70b-versatile")
    os.environ["GROQ_MODEL_LOW"] = model_low
    os.environ["GROQ_MODEL_MEDIUM"] = model_med
    os.environ["GROQ_MODEL_HIGH"] = model_med

tab1, tab2, tab3 = st.tabs(["💬 Agent Chat Interface", "🕸️ Architecture & DB Inspector", "📊 Benchmarks & Evals"])

# ---------------- Tab 1: Chat Interface ----------------
with tab1:
    st.subheader("Interactive Multi-Agent Assistant")
    
    if "messages" not in st.session_state:
        st.session_state["messages"] = []

    for msg in st.session_state["messages"]:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    user_input = st.chat_input("Ask a question about database analytics, ETL operations, or chart visualizations...")
    if user_input:
        st.session_state["messages"].append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        with st.chat_message("assistant"):
            with st.spinner("Multi-Agent Graph Orchestrating..."):
                start_t = time.time()
                try:
                    response = data_agent.invoke({
                        "messages": [HumanMessage(content=user_input)],
                        "route_response": ""
                    })
                    latency = round(time.time() - start_t, 2)
                    
                    route = response.get("route_response", "unknown")
                    messages = response.get("messages", [])
                    last_msg = messages[-1] if messages else ""
                    ans_text = last_msg.content if hasattr(last_msg, 'content') else str(last_msg)

                    st.markdown(f"**Route Chosen:** `{route.upper()}` | **Latency:** `{latency}s`")
                    st.markdown(ans_text)
                    
                    # Display latest generated visualization if available
                    viz_files = sorted(glob.glob("data/visualizations/chart_*.png"), key=os.path.getmtime, reverse=True)
                    if viz_files and route == "viz":
                        st.image(viz_files[0], caption="Generated Data Visualization", use_container_width=True)

                    st.session_state["messages"].append({"role": "assistant", "content": f"**[{route.upper()} Agent]** ({latency}s)\n\n{ans_text}"})
                except Exception as e:
                    st.error(f"Error processing request: {e}")

# ---------------- Tab 2: Architecture & DB Inspector ----------------
with tab2:
    st.subheader("PostgreSQL Database Schema")
    try:
        conn_details = {
            "host": os.environ.get('host', 'localhost'),
            "port": int(os.environ.get('port', 5432)),
            "user": os.environ.get('user', 'postgres'),
            "password": os.environ.get('password', 'postgres'),
            "dbname": os.environ.get('database', 'postgres')
        }
        db = DatabaseUtil(conn_details)
        schema_text = db.schema_details("public")
        st.text_area("Live Database Schema Context", schema_text, height=300)
    except Exception as e:
        st.warning(f"Could not connect to PostgreSQL: {e}")

    st.subheader("LangGraph State Graphs")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("**Data Agent Router**")
        if os.path.exists("data_agent_graph.png"):
            st.image("data_agent_graph.png")
    with col2:
        st.markdown("**SQL Analyst Agent**")
        if os.path.exists("sql_analyst_graph.png"):
            st.image("sql_analyst_graph.png")
    with col3:
        st.markdown("**ETL Analyst Agent**")
        if os.path.exists("etl_analyst_graph.png"):
            st.image("etl_analyst_graph.png")

# ---------------- Tab 3: Benchmarks & Evals ----------------
with tab3:
    st.subheader("System Evaluation & Benchmark Suite")
    st.write(f"Total Benchmark Test Cases: **{len(BENCHMARK_CASES)}**")
    
    if st.button("Run Benchmark Evaluation Harness"):
        with st.spinner("Running benchmarks against agent graph..."):
            passed_route = 0
            results = []
            for test in BENCHMARK_CASES:
                st_t = time.time()
                try:
                    res = data_agent.invoke({
                        "messages": [HumanMessage(content=test['prompt'])],
                        "route_response": ""
                    })
                    lat = round(time.time() - st_t, 2)
                    act_route = res.get("route_response", "")
                    route_pass = act_route.lower() == test['expected_route'].lower()
                    if route_pass:
                        passed_route += 1
                    results.append({
                        "ID": test['id'],
                        "Prompt": test['prompt'][:40] + "...",
                        "Expected Route": test['expected_route'],
                        "Actual Route": act_route,
                        "Route Pass": "✅ PASS" if route_pass else "❌ FAIL",
                        "Latency (s)": lat
                    })
                except Exception as ex:
                    results.append({
                        "ID": test['id'],
                        "Prompt": test['prompt'][:40] + "...",
                        "Expected Route": test['expected_route'],
                        "Actual Route": "ERROR",
                        "Route Pass": "❌ FAIL",
                        "Latency (s)": 0.0
                    })
            
            st.dataframe(results, use_container_width=True)
            st.success(f"Routing Accuracy: {(passed_route / len(BENCHMARK_CASES)) * 100:.1f}%")
