"""This module handles loading and parsing of external prompt configurations (YAML)."""

from pathlib import Path

import yaml
from langchain_core.prompts import PromptTemplate

from logs.log_generator import log_message


def load_prompt_from_yaml(filename: str) -> PromptTemplate:
    """
    Loads a prompt configuration from a YAML file.

    Args:
        filename: The name of the file.

    Returns:
        PromptTemplate: A LangChain prompt template ready for formatting.
    """
    # Dynamically resolve path relative to this file
    base_dir = Path(__file__).parent / "yaml"
    file_path = base_dir / filename

    if not file_path.exists():
        log_message(f"❌ Prompt Loader: File not found at: {file_path}", "error")
        raise FileNotFoundError(f"Prompt file '{filename}' missing.")

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            config = yaml.safe_load(f)

        log_message(
            f"📄 Prompt Loader: Loaded template '{filename}' successfully.", "info"
        )

        return PromptTemplate(
            template=config["template"], input_variables=config["input_variables"]
        )
    except Exception as e:
        log_message(f"❌ Prompt Loader: Error parsing YAML: {e}", "error")
        raise e
