import os

from backend.app import app
from real_agents.adapters.models import ChatOpenAI, ChatAnthropic
from real_agents.adapters.llm import BaseLanguageModel

LLAMA_DIR = "PATH_TO_LLAMA_DIR"


@app.route("/api/llm_list", methods=["POST"])
def get_llm_list():
    """Gets the whole llm list."""
    return [
        {"id": llm, "name": llm} for llm in [
            "bedrock-claude-v2",
            "gpt-3.5-turbo-16k",
            "gpt-4",
            "claude-v1",
            "claude-2",
            "lemur-chat"
        ]
    ]


def get_llm(llm_name: str, **kwargs) -> BaseLanguageModel:
    """Gets the llm model by its name."""
    if llm_name in ["gpt-3.5-turbo-16k", "gpt-4"]:
        return ChatOpenAI(
            model_name=llm_name,
            streaming=True,
            verbose=True,
            **kwargs
        )
    elif llm_name in ["claude-v1", "claude-2"]:
        anthropic_api_key = os.getenv("ANTHROPIC_API_KEY", "")
        return ChatAnthropic(
            model=llm_name,
            streaming=True,
            verbose=True,
            anthropic_api_key=anthropic_api_key,
            **kwargs,
        )
    elif llm_name == "lemur-chat":
        return ChatOpenAI(
            model_name="lemur-70b-chat-v1",
            streaming=True,
            openai_api_base="https://model-api.xlang.ai/v1",
            verbose=True,
            max_tokens=2048,
            **kwargs
        )
    elif llm_name == "bedrock-claude-v2":
        litellm_api_base = os.getenv("LITELLM_API_BASE", "")
        return ChatOpenAI(
            model_name="anthropic.claude-v2",
            openai_api_base=litellm_api_base,
            streaming=True,
            verbose=True,
            max_tokens=4096,
            **kwargs
        )
    else:
        raise ValueError(f"llm_name {llm_name} not found")
