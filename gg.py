#!/usr/bin/env python3
# gg.py

import os
import argparse
import google.generativeai as genai
import sys
import xml.etree.ElementTree as ET
from rich.console import Console
from rich.markdown import Markdown
from rich.text import Text
import re # For regular expressions to parse .gss files

# --- Configuration Constants ---
DEFAULT_MODEL = 'gemini-1.5-flash-latest' # Set your default model here
CONFIG_FILE_NAME = 'gg_config.htgeml' # Your main config file name
EMS_FOLDER_NAME = 'ems' # Name of the base folder for .gss files
GLOBAL_EMS_SUBFOLDER = '_global' # Name of the subfolder for global ems
INPUT_PLACEHOLDER = 'INPUT_PLACEHOLDER' # Define the placeholder

# Global variables to store loaded config
CONFIG = {
    "ems": {},      # Stores {'em_name': {'params': ['p1', 'p2'], 'is_global': True/False, 'other_prop': 'value'}}
    "colors": {}
}

# Initialize Rich Console for all output
console = Console()

def get_rich_style_name(element_name: str) -> str:
    """
    Retrieves the rich-compatible style name from CONFIG["colors"].
    """
    color_name = CONFIG["colors"].get(element_name)
    return color_name if color_name else "default"


def apply_rich_style(text: str, element_name: str) -> Text:
    """
    Applies rich styling to text using Text objects.
    Returns a rich.text.Text object ready for console.print().
    """
    style_name = get_rich_style_name(element_name)
    return Text(text, style=style_name)


def get_api_key() -> str:
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


def configure_gemini(api_key: str):
    """
    Configures the Google Gemini API client.
    """
    genai.configure(api_key=api_key)


def parse_gss_file(file_path: str) -> dict:
    """
    Parses a single .gss file to extract em definitions.
    Supports a simplified CSS-like syntax: name { param: "value"; param: "value"; }
    """
    ems_from_gss = {}
    try:
        with open(file_path, 'r') as f:
            content = f.read()
    except Exception as e:
        console.print(apply_rich_style(f"Error reading .gss file '{file_path}': {e}", "error-message"))
        return ems_from_gss

    # Regex to find blocks like 'name { ... }'
    blocks = re.findall(r'([a-zA-Z0-9_-]+)\s*{(.*?)}', content, re.DOTALL)

    for em_name, block_content in blocks:
        em_data = {'params': []} # Initialize params list for this em
        # console.print(f"DEBUG: Processing em '{em_name}' from '{file_path}'") # Commented out

        # Regex to find all 'key: "value";' pairs within the block content
        # Captures key and value, handling escaped quotes
        properties = re.findall(r'(\S+?):\s*"((?:[^"\\]|\\.)*)"\s*;', block_content, re.DOTALL)

        for key, value in properties:
            # Handle escaped double quotes within the value
            parsed_value = value.replace('\\"', '"')
            # console.print(f"DEBUG: Found property '{key}': '{parsed_value}' for '{em_name}'") # Commented out

            if key.lower() == 'param':
                em_data['params'].append(parsed_value)
            else:
                # Store other properties directly for future use
                em_data[key.lower()] = parsed_value

        # console.print(f"DEBUG: Em '{em_name}' has params: {em_data['params']}") # Commented out


        if em_data['params']: # Only add em if it has at least one param
            ems_from_gss[em_name.lower()] = em_data
        else:
            console.print(apply_rich_style(f"Warning: Em '{em_name}' in '{file_path}' has no 'param: \"value\";' defined and will be skipped.", "system-message"))

    return ems_from_gss


def load_all_gss_ems() -> dict:
    """
    Loads em definitions from all .gss files in the 'ems' folder and its subfolders.
    Determines if an em is global based on its location in the _global subfolder.
    """
    gss_ems = {}
    script_dir = os.path.dirname(os.path.abspath(__file__))
    base_ems_folder_path = os.path.join(script_dir, EMS_FOLDER_NAME)
    global_ems_folder_path = os.path.join(base_ems_folder_path, GLOBAL_EMS_SUBFOLDER)

    if not os.path.exists(base_ems_folder_path):
        console.print(apply_rich_style(
            f"Warning: '{EMS_FOLDER_NAME}' folder not found at '{base_ems_folder_path}'. No .gss ems loaded.",
            "system-message"
        ))
        return gss_ems

    for root, _, files in os.walk(base_ems_folder_path):
        is_global_em_folder = (os.path.normpath(root) == os.path.normpath(global_ems_folder_path))

        for file in files:
            if file.endswith(".gss"):
                file_path = os.path.join(root, file)

                console.print(apply_rich_style(
                    f"Loading .gss file: '{file_path}' (Global: {is_global_em_folder})",
                    "system-message"
                ))
                loaded_ems = parse_gss_file(file_path)
                for em_name, em_data in loaded_ems.items():
                    if em_name in gss_ems:
                        console.print(apply_rich_style(
                            f"Warning: Duplicate em name '{em_name}' found. Overwriting definition from '{file_path}'.",
                            "system-message"
                        ))
                    em_data['is_global'] = is_global_em_folder # Add globality flag
                    gss_ems[em_name] = em_data # Store the dict {'params': [...], 'is_global': ...}

    return gss_ems


def load_config():
    """
    Loads configuration from the gg_config.htgeml file and all .gss files.
    .gss defined ems override .htgeml defined ems if names conflict.
    """
    config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), CONFIG_FILE_NAME)

    # Load from gg_config.htgeml first
    if os.path.exists(config_path):
        try:
            tree = ET.parse(config_path)
            root = tree.getroot()

            # Load Ems from htgeml - these are always callable (not global)
            ems_section = root.find('ems')
            if ems_section is not None:
                for em_element in ems_section.findall('em'):
                    em_name = em_element.get('name')
                    prompt_element = em_element.find('prompt')
                    if em_name and prompt_element is not None and prompt_element.text:
                        # Convert old 'prompt' to new 'params' list for consistency
                        CONFIG["ems"][em_name.lower()] = {'params': [prompt_element.text.strip()], 'is_global': False}

            # Load Colors
            colors_section = root.find('colors')
            if colors_section is not None:
                for color_element in colors_section:
                    tag_name = color_element.tag
                    color_value = color_element.get('color')
                    if tag_name and color_value:
                        CONFIG["colors"][tag_name] = color_value.lower()
        except ET.ParseError as e:
            console.print(apply_rich_style(
                f"Error parsing config file '{CONFIG_FILE_NAME}': {e}", "error-message"
            ))
            console.print(apply_rich_style(
                "Please check the XML/HTML-like structure of your config file.", "system-message"
            ))
        except Exception as e:
            console.print(apply_rich_style(
                f"An unexpected error occurred while loading config: {e}", "error-message"
            ))
    else:
        console.print(apply_rich_style(
            f"Warning: Main config file '{CONFIG_FILE_NAME}' not found at '{config_path}'.",
            "system-message"
        ))
        console.print(apply_rich_style(
            "Running with default settings (no 'ems' or custom colors loaded from main config).",
            "system-message"
        ))

    # Load from .gss files and update CONFIG["ems"]. .gss ems take precedence.
    gss_ems = load_all_gss_ems()
    CONFIG["ems"].update(gss_ems)


def get_gemini_response(prompt_text: str, chat_history=None, model_name: str = DEFAULT_MODEL) -> tuple[bool, str, any]:
    """
    Sends a prompt to the Gemini model and returns the response.
    Returns (success_status: bool, response_content: str, chat_session_obj).
    """
    try:
        model = genai.GenerativeModel(model_name)

        if chat_history is not None:
            chat = chat_history
            response = chat.send_message(prompt_text)
        else:
            # For single queries, start a new chat each time
            # For ongoing chat mode, chat object is passed in and reused
            chat = model.start_chat(history=[] if chat_history is None else chat_history.history)
            response = chat.send_message(prompt_text)


        if response and response.text:
            return True, response.text.strip(), chat
        else:
            return False, "Gemini returned an empty response.", chat

    except Exception as e:
        return False, f"Error communicating with Gemini (model: {model_name}): {e}", None


def main():
    """
    Main function to parse arguments and run the gg CLI tool.
    """
    parser = argparse.ArgumentParser(
        description="A Gemini-powered terminal assistant (gg).",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        "query",
        nargs="*",
        help="Your question or command for Gemini.\n"
             "  E.g., `gg \"How do I list files?\"`\n"
             f"  To use an 'em', prefix with 'em:' (e.g., `gg em:explain-command \"ls -l\"`)\n"
             f"  The input to the em will replace '{INPUT_PLACEHOLDER}' in its definition.\n"
             "  Global ems (in the `ems/_global/` folder) are always active by default.\n"
             "  Use `gg chat` or `gg -c` for interactive mode."
    )
    parser.add_argument(
        "-c", "--chat",
        action="store_true",
        help="Enter interactive chat mode with Gemini."
    )
    parser.add_argument(
        "-m", "--model",
        default=DEFAULT_MODEL,
        help=f"Specify the Gemini model to use (default: {DEFAULT_MODEL}).\n"
             "  E.g., `gg -m gemini-1.5-flash-latest \"Explain tensors.\"`"
    )
    parser.add_argument(
        "-ng", "--no-global-ems",
        action="store_true",
        help="Temporarily disable all global ems for this query or chat session."
    )

    args = parser.parse_args()

    api_key = get_api_key()
    configure_gemini(api_key)
    load_config()

    selected_model = args.model

    # Prepare global em prompt prefix
    global_em_prefix = ""
    if not args.no_global_ems:
        global_ems_prompts = [] # Collect raw prompt strings for global ems
        for em_name, em_data in CONFIG["ems"].items():
            if em_data.get('is_global', False) and 'params' in em_data:
                # Combine all params for this global em into a single string
                global_ems_prompts.append("".join(em_data['params']))

        # Sort combined global em prompts for consistent order
        global_ems_prompts.sort() # Sorts based on the actual prompt strings

        if global_ems_prompts:
            global_em_prefix = " ".join(global_ems_prompts) + " "
            # This line informs the user about active global ems. You can comment it out if you prefer less verbose startup.
            console.print(apply_rich_style(f"Active global ems prefix: {global_em_prefix.strip()}", "system-message"))


    is_em_call = False
    em_name_to_call = None
    em_user_input = ""

    # Check for 'em:' call structure in single-shot mode
    if args.query and args.query[0].lower().startswith('em:'):
        parts = args.query[0].split(':', 1)
        if len(parts) == 2:
            potential_em_name_parts = parts[1].split(' ', 1)
            potential_em_full_name = potential_em_name_parts[0].lower()

            if potential_em_full_name in CONFIG["ems"] and not CONFIG["ems"][potential_em_full_name].get('is_global', False):
                em_name_to_call = potential_em_full_name
                em_input_from_first_arg = potential_em_name_parts[1] if len(potential_em_name_parts) > 1 else ""
                em_input_from_remaining_args = " ".join(args.query[1:])
                em_user_input = (em_input_from_first_arg + " " + em_input_from_remaining_args).strip()
                is_em_call = True
            elif potential_em_full_name in CONFIG["ems"] and CONFIG["ems"][potential_em_full_name].get('is_global', False):
                console.print(apply_rich_style(
                    f"Error: Global Em '{potential_em_full_name}' cannot be called directly with 'em:'. It's always active (unless --no-global-ems is used).",
                    "error-message"
                ))
                sys.exit(1)
            else:
                console.print(apply_rich_style(
                    f"Error: Callable Em '{potential_em_full_name}' not found. Check name and ensure it's not global.",
                    "error-message"
                ))
                sys.exit(1)
        else:
            pass


    if args.chat or (args.query and args.query[0].lower() == 'chat' and not is_em_call):
        console.print(apply_rich_style(f"--- Entering interactive chat mode (Model: {selected_model}) ---", "system-message"))
        if args.no_global_ems:
            console.print(apply_rich_style("--- Global ems are temporarily DISABLED for this session. ---", "system-message"))
        console.print(apply_rich_style("Type 'exit', 'quit', 'bye', or Ctrl+C to end.", "system-message"))
        current_chat_session = None

        try:
            while True:
                try:
                    user_input_raw = str(console.input(apply_rich_style("(Gemini) > ", "system-message"))).strip()
                    if user_input_raw.lower() in ["exit", "quit", "bye"]:
                        console.print(apply_rich_style("--- Exiting chat mode. Goodbye! ---", "system-message"))
                        break
                    if not user_input_raw:
                        continue

                    prompt_to_gemini = user_input_raw

                    if user_input_raw.lower().startswith('em:'):
                        chat_em_parts = user_input_raw.split(':', 1)
                        if len(chat_em_parts) == 2:
                            chat_em_name_and_input = chat_em_parts[1].split(' ', 1)
                            chat_em_name = chat_em_name_and_input[0].lower()
                            chat_em_input_val = chat_em_name_and_input[1] if len(chat_em_name_and_input) > 1 else ""

                            if chat_em_name in CONFIG["ems"] and not CONFIG["ems"][chat_em_name].get('is_global', False):
                                callable_em_full_prompt = "".join(CONFIG["ems"][chat_em_name]['params'])
                                specific_em_prompt = callable_em_full_prompt.replace(INPUT_PLACEHOLDER, chat_em_input_val)
                                prompt_to_gemini = global_em_prefix + specific_em_prompt
                                console.print(apply_rich_style(f"(Using Em '{chat_em_name}'...)", "system-message"))
                            elif chat_em_name in CONFIG["ems"] and CONFIG["ems"][chat_em_name].get('is_global', False):
                                console.print(apply_rich_style(
                                    f"Error: Global Em '{chat_em_name}' cannot be called directly. It's always active.", "error-message"
                                ))
                                continue
                            else:
                                console.print(apply_rich_style(f"Error: Em '{chat_em_name}' not found.", "error-message"))
                                continue
                        else:
                            prompt_to_gemini = global_em_prefix + user_input_raw
                    else:
                        prompt_to_gemini = global_em_prefix + user_input_raw

                    success, response_content, current_chat_session = get_gemini_response(prompt_to_gemini, current_chat_session, model_name=selected_model)

                    if success:
                        response_style = get_rich_style_name("response-text")
                        console.print(Markdown(response_content, style=response_style))
                    else:
                        console.print(apply_rich_style(response_content, "error-message"))
                except KeyboardInterrupt:
                    console.print(apply_rich_style("\n--- Exiting chat mode. Goodbye! ---", "system-message"))
                    break
                except EOFError:
                    console.print(apply_rich_style("\n--- Exiting chat mode. Goodbye! ---", "system-message"))
                    break
        except Exception as e:
            console.print(apply_rich_style(f"An unexpected error occurred in chat mode: {e}", "error-message"))

    elif is_em_call:
        callable_em_full_prompt = "".join(CONFIG["ems"][em_name_to_call]['params'])
        specific_em_prompt = callable_em_full_prompt.replace(INPUT_PLACEHOLDER, em_user_input)
        final_prompt_to_gemini = global_em_prefix + specific_em_prompt

        console.print(apply_rich_style(f"Using Em '{em_name_to_call}' (Model: {selected_model})...", "system-message"))
        success, response_content, _ = get_gemini_response(final_prompt_to_gemini, model_name=selected_model)

        if success:
            response_style = get_rich_style_name("response-text")
            console.print(Markdown(response_content, style=response_style))
        else:
            console.print(apply_rich_style(response_content, "error-message"))

    elif args.query:
        query = " ".join(args.query).strip()
        if not query:
            console.print(apply_rich_style(parser.format_help(), "system-message"))
            sys.exit(1)

        final_query_to_gemini = global_em_prefix + query

        console.print(apply_rich_style(f"Sending query to Gemini (Model: {selected_model})...", "system-message"))
        success, response_content, _ = get_gemini_response(final_query_to_gemini, model_name=selected_model)

        if success:
            response_style = get_rich_style_name("response-text")
            console.print(Markdown(response_content, style=response_style))
        else:
            console.print(apply_rich_style(response_content, "error-message"))
    else:
        console.print(apply_rich_style(parser.format_help(), "system-message"))
        sys.exit(1)


if __name__ == "__main__":
    main()
