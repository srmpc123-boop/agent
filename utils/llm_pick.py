import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic

load_dotenv()


def pick_llm(level: str):
    """
    Picks the appropriate LLM based on provider configuration and question difficulty level.
    Defaults to Groq for free, high-speed LPU inference.

    Args:
        level (str): The level of the question ("low", "medium", "high", or "claude").

    Returns:
        BaseChatModel: The LLM instance to be used.
    """
    provider = os.getenv("LLM_PROVIDER", "groq").lower()

    if provider == "groq":
        groq_api_key = os.getenv("GROQ_API_KEY")
        if level.lower() == "low":
            model = os.getenv("GROQ_MODEL_LOW", "llama-3.1-8b-instant")
            return ChatGroq(model_name=model, temperature=0, groq_api_key=groq_api_key)
        elif level.lower() == "medium":
            model = os.getenv("GROQ_MODEL_MEDIUM", "llama-3.3-70b-versatile")
            return ChatGroq(model_name=model, temperature=0, groq_api_key=groq_api_key)
        elif level.lower() in ["high", "claude"]:
            model = os.getenv("GROQ_MODEL_HIGH", "llama-3.3-70b-versatile")
            return ChatGroq(model_name=model, temperature=0, groq_api_key=groq_api_key)
        else:
            return ChatGroq(model_name="llama-3.1-8b-instant", temperature=0, groq_api_key=groq_api_key)

    elif provider == "openai":
        if level.lower() == "low":
            return ChatOpenAI(model_name=os.getenv("OPENAI_MODEL_LOW", "gpt-4o-mini"), temperature=0)
        elif level.lower() == "medium":
            return ChatOpenAI(model_name=os.getenv("OPENAI_MODEL_MEDIUM", "gpt-4o"), temperature=0)
        else:
            return ChatOpenAI(model_name=os.getenv("OPENAI_MODEL_HIGH", "gpt-4o"), temperature=0)

    elif provider == "anthropic":
        return ChatAnthropic(model_name=os.getenv("ANTHROPIC_MODEL", "claude-3-5-sonnet-20240620"), temperature=0)

    else:
        raise ValueError(f"Unsupported LLM provider: {provider}")


if __name__ == "__main__":
    llm_obj = pick_llm("low")
    print(f"Loaded LLM Provider instance: {llm_obj}")

