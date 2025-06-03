#!/usr/bin/env python3
# gg.py

import os
import argparse
import google.generativeai as genai
import sys
import xml.etree.ElementTree as ET
from rich.console import Console
from rich.markdown import Markdown
from rich.text import Text # NEW: Import Text for consistent styling

# --- Configuration Constants ---
DEFAULT_MODEL = 'gemini-1.5-flash-latest' # Set your default model here
CONFIG_FILE_NAME = 'gg_config.htgeml' # Your config file name

# Global variables to store loaded config
CONFIG = {
    "ems": {},
    "colors": {}
}

# No longer need COLOR_MAP for direct ANSI codes, rich handles styles directly.
# Keeping it commented out for reference if needed for very specific non-rich cases.
# COLOR_MAP = {
#     "black": "\033[30m", "red": "\033[31m", "green": "\033[32m", "yellow": "\033[33m",
#     "blue": "\033[34m", "magenta": "\033[35m", "cyan": "\033[36m", "white": "\033[37m",
#     "light_black": "\033[90m", "light_red": "\033[91m", "light_green": "\033[92m",
#     "light_yellow": "\033[93m", "light_blue": "\033[94m", "light_magenta": "\033[95m",
#     "light_cyan": "\033[96m", "light_white": "\033[97m",
#     "reset": "\033[0m"
# }


# Initialize Rich Console for all output
console = Console()

def get_rich_style_name(element_name):
    """
    Retrieves the rich-compatible style name from CONFIG["colors"].
    Rich understands common color names (e.g., "cyan", "light_red")
    and can even use hex codes like "#FF00FF" if you configure them.
    """
    color_name = CONFIG["colors"].get(element_name)
    return color_name if color_name else "default" # Fallback to rich's default style


def apply_rich_style(text, element_name):
    """
    Applies rich styling to text using Text objects.
    Returns a rich.text.Text object ready for console.print().
    """
    style_name = get_rich_style_name(element_name)
    return Text(text, style=style_name)


def get_api_key():
    """
    Retrieves the Google Gemini API key from environment variables.
    Exits if the key is not found.
    """
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        console.print(apply_rich_style("Error: GOOGLE_API_KEY environment variable not set.", "error-message"))
        console.print(apply_rich_style("Please set your Gemini API key: export GOOGLE_API_KEY='YOUR_API_KEY'", "system-message"))
        sys.exit(1)
    return api_key


def configure_gemini(api_key):
    """
    Configures the Google Gemini API client.
    """
    genai.configure(api_key=api_key)


def load_config():
    """
    Loads configuration from the gg_config.htgeml file.
    Parses 'ems' and 'colors' sections.
    """
    config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), CONFIG_FILE_NAME)
    if not os.path.exists(config_path):
        console.print(apply_rich_style(f"Warning: Configuration file '{CONFIG_FILE_NAME}' not found at '{config_path}'.", "system-message"))
        console.print(apply_rich_style("Running with default settings (no 'ems' or custom colors loaded).", "system-message"))
        return

    try:
        tree = ET.parse(config_path)
        root = tree.getroot()

        # Load Ems
        ems_section = root.find('ems')
        if ems_section is not None:
            for em_element in ems_section.findall('em'):
                em_name = em_element.get('name')
                prompt_element = em_element.find('prompt')
                if em_name and prompt_element is not None and prompt_element.text:
                    CONFIG["ems"][em_name] = prompt_element.text.strip()

        # Load Colors
        colors_section = root.find('colors')
        if colors_section is not None:
            for color_element in colors_section:
                tag_name = color_element.tag
                color_value = color_element.get('color')
                if tag_name and color_value:
                    CONFIG["colors"][tag_name] = color_value.lower() # Store color name in lowercase

    except ET.ParseError as e:
        console.print(apply_rich_style(f"Error parsing config file '{CONFIG_FILE_NAME}': {e}", "error-message"))
        console.print(apply_rich_style("Please check the XML/HTML-like structure of your config file.", "system-message"))
    except Exception as e:
        console.print(apply_rich_style(f"An unexpected error occurred while loading config: {e}", "error-message"))


def get_gemini_response(prompt_text, chat_history=None, model_name=DEFAULT_MODEL):
    """
    Sends a prompt to the Gemini model and returns the response.
    If chat_history is provided, it continues a chat session.
    Allows specifying a model name.
    """
    try:
        model = genai.GenerativeModel(model_name)

        if chat_history is not None:
            chat = chat_history
            response = chat.send_message(prompt_text)
        else:
            chat = model.start_chat(history=[])
            response = chat.send_message(prompt_text)

        if response and response.text:
            return response.text.strip(), chat
        else:
            return apply_rich_style("Gemini returned an empty response.", "system-message"), chat

    except Exception as e:
        return apply_rich_style(f"Error communicating with Gemini (model: {model_name}): {e}", "error-message"), None


def main():
    """
    Main function to parse arguments and run the gg CLI tool.
    """
    parser = argparse.ArgumentParser(
        description=apply_rich_style("A Gemini-powered terminal assistant (gg).", "system-message"),
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        "query",
        nargs="*",
        help=apply_rich_style("Your question or command for Gemini.\n"
                         "  E.g., `gg \"How do I list files?\"`\n"
                         "  To use an 'em', prefix with 'em:' (e.g., `gg em:explain-error \"E: Broken packages\"`)\n"
                         "  Use `gg chat` or `gg -c` for interactive mode.", "system-message")
    )
    parser.add_argument(
        "-c", "--chat",
        action="store_true",
        help=apply_rich_style("Enter interactive chat mode with Gemini.", "system-message")
    )
    parser.add_argument(
        "-m", "--model",
        default=DEFAULT_MODEL,
        help=apply_rich_style(f"Specify the Gemini model to use (default: {DEFAULT_MODEL}).\n"
                         "  E.g., `gg -m gemini-1.5-flash-latest \"Explain tensors.\"`", "system-message")
    )

    args = parser.parse_args()

    api_key = get_api_key()
    configure_gemini(api_key)
    load_config() # Load configuration from gg_config.htgeml

    selected_model = args.model

    is_em_call = False
    em_name = None
    em_input = ""

    if args.query and len(args.query) > 0:
        first_arg = args.query[0]
        if first_arg.lower().startswith('em:'):
            parts = first_arg.split(':', 1)
            if len(parts) == 2:
                em_name = parts[1].split(' ', 1)[0].lower()
                if len(parts[1].split(' ', 1)) > 1:
                    em_input = parts[1].split(' ', 1)[1].strip()
                is_em_call = True


    if args.chat or (args.query and args.query[0].lower() == 'chat'):
        # Interactive chat mode
        console.print(apply_rich_style(f"--- Entering interactive chat mode (Model: {selected_model}) ---", "system-message"))
        console.print(apply_rich_style("Type 'exit', 'quit', 'bye', or Ctrl+C to end.", "system-message"))
        chat_history = None
        current_chat_session = None

        try:
            while True:
                try:
                    # Using console.input which can take a rich.text.Text object as prompt
                    user_input = console.input(apply_rich_style("(Gemini) > ", "system-message")).strip()
                    if user_input.lower() in ["exit", "quit", "bye"]:
                        console.print(apply_rich_style("--- Exiting chat mode. Goodbye! ---", "system-message"))
                        break
                    if not user_input:
                        continue

                    if user_input.lower().startswith('em:'):
                        parts = user_input.split(':', 1)
                        if len(parts) == 2:
                            em_name_interactive = parts[1].split(' ', 1)[0].lower()
                            em_input_interactive = parts[1][len(em_name_interactive):].strip()

                            if em_name_interactive in CONFIG["ems"]:
                                full_prompt = CONFIG["ems"][em_name_interactive].replace("{input}", em_input_interactive)
                                console.print(apply_rich_style(f"(Using Em '{em_name_interactive}'...)", "system-message"))
                                response_text, current_chat_session = get_gemini_response(full_prompt, current_chat_session, model_name=selected_model)
                            else:
                                response_text = apply_rich_style(f"Error: Em '{em_name_interactive}' not found in '{CONFIG_FILE_NAME}'.", "error-message")
                                current_chat_session = current_chat_session
                        else:
                            response_text, current_chat_session = get_gemini_response(user_input, current_chat_session, model_name=selected_model)
                    else:
                        response_text, current_chat_session = get_gemini_response(user_input, current_chat_session, model_name=selected_model)

                    # Use Rich for rendering Gemini's response with its default formatting
                    # We can use the style argument for the Markdown object directly if the config color is a rich-compatible style
                    response_style = get_rich_style_name("response-text")
                    console.print(Markdown(response_text, style=response_style))


                except KeyboardInterrupt:
                    console.print(apply_rich_style("\n--- Exiting chat mode. Goodbye! ---", "system-message"))
                    break
                except EOFError:
                    console.print(apply_rich_style("\n--- Exiting chat mode. Goodbye! ---", "system-message"))
                    break
        except Exception as e:
            console.print(apply_rich_style(f"An unexpected error occurred in chat mode: {e}", "error-message"))

    elif is_em_call:
        # Single-shot "em" query mode
        if em_name in CONFIG["ems"]:
            full_prompt = CONFIG["ems"][em_name].replace("{input}", em_input)
            console.print(apply_rich_style(f"Using Em '{em_name}' (Model: {selected_model})...", "system-message"))
            response_text, _ = get_gemini_response(full_prompt, model_name=selected_model)
            # Use Rich for rendering Gemini's response with its default formatting
            response_style = get_rich_style_name("response-text")
            console.print(Markdown(response_text, style=response_style))
        else:
            console.print(apply_rich_style(f"Error: Em '{em_name}' not found in '{CONFIG_FILE_NAME}'.", "error-message"))
            console.print(apply_rich_style("Please check your config file or the 'em' name.", "system-message"))
            sys.exit(1)

    elif args.query:
        # Standard single-shot query mode
        query = " ".join(args.query).strip()
        if not query:
            parser.print_help()
            sys.exit(1)

        console.print(apply_rich_style(f"Sending query to Gemini (Model: {selected_model})...", "system-message"))
        response_text, _ = get_gemini_response(query, model_name=selected_model)
        # Use Rich for rendering Gemini's response with its default formatting
        response_style = get_rich_style_name("response-text")
        console.print(Markdown(response_text, style=response_style))
    else:
        # No arguments given, print help
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
