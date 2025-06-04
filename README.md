# ✨🚀🌟 Introducing **GERMINAL**! Your Personal AI Assistant, Right in Your Terminal! 🌟🚀✨

Welcome, future `GERMINAL` master! 🎉 Get ready to experience the incredible power of Google Gemini AI, instantly accessible from your Linux terminal! `GERMINAL` is here to be your super-smart, always-ready assistant, no matter what you need to explore.

Forget complicated programs or switching windows – with `GERMINAL` (using the `gg` command!), you can ask questions, brainstorm ideas, write creative texts, get quick facts, summarize information, or just chat with an intelligent AI, all directly from your command prompt! It's like magic! ✨

-----

## **🌟 What Can `GERMINAL` Do For YOU? (Awesome Features!)**

* **Instant Answers!** 💡 Just ask `GERMINAL` (using the `gg` command!), and it'll give you clear, concise answers to almost any question you can imagine, right in your terminal.
* **Chat Mode!** 💬 Dive into a real conversation with `GERMINAL`. It remembers what you've said, so you can have a flowing, natural chat. Perfect for brainstorming or exploring complex ideas!
* **Custom "Ems" with `.gss` Files (Your Personal Commands!)** ✍️ Create your own unique shortcuts, called "ems," for tasks you do often. Ems are now defined in simple text files with a `.gss` extension, located in an `ems` folder right next to your `gg.py` script.
    * **Callable Ems:** Define specific prompt templates that you can call with `gg em:your-em-name "your input"`.
    * **Global Ems:** Place `.gss` files in a special `ems/_global/` subfolder. These ems define instructions or context that are *always* active, automatically prepended to every query you send to Gemini (unless disabled with `--no-global-ems`). Perfect for setting persona, style, or default instructions!
* **Beautiful Output!** 🌈 `GERMINAL` makes AI responses easy on the eyes. It understands fancy text formatting (like **bold**, bullet points, and special text blocks) and displays them beautifully in your terminal, all in colors *you* choose via `gg_config.htgeml`!
* **Model Flexibility!** 🧠 You can decide which Google Gemini AI brain `GERMINAL` uses, giving you control over its style and capabilities.

-----

## **🚀 Let's Get Started! (Your Step-by-Step Installation Adventure!)**

Don't worry if you've never touched a command prompt or heard of Git before! This guide is built just for you. We'll go slowly, step-by-step, and make sure `GERMINAL` is up and running smoothly on your computer. You got this! 💪

### **Before You Begin (Quick Checklist!)**

Please make sure you have these things ready:

1.  **A Computer with Debian-based Linux:** This guide is specifically written for Linux operating systems that are based on Debian. This includes popular choices like **MX Linux** (which is what I initially spun up this project on!), **Ubuntu**, Linux Mint, Pop!_OS, and many others.
2.  **An Active Internet Connection:** `GERMINAL` needs the internet to talk to Google's super-smart AI brains!
3.  **A Google Account:** You'll need this to get your special AI key from Google.

-----

### **Step 1: Get Your Secret Google Gemini AI Key (Your VIP Pass to AI Power!)**

To make `GERMINAL` work its magic, it needs a special "key" to talk to Google's powerful Gemini AI. Think of this key as a secret VIP pass that allows your `GERMINAL` tool to access all the AI services.

**🔑 EXTREMELY IMPORTANT SECURITY ALERT! Your AI Key is like a super-secret password. NEVER share it with anyone, never type it directly into a program's code, and absolutely NEVER post it publicly (like on GitHub or forums). If you EVER accidentally expose your key, you MUST revoke it immediately (see "Crucial Security Step: What if My Key is Exposed?" at the end of this README).**

1.  **Open Your Web Browser:** Go to this special Google page:
    [https://aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey)
    (You might need to sign in with your regular Google Account if you haven't already).

2.  **Create Your New API Key:** On this page, look for a big button that says something like **"Create API key in new project"** or simply **"Create API key"**. Click it!
    * Google will instantly generate a very long string of letters, numbers, and symbols. This is your unique API key! ✨

3.  **Copy Your API Key:** Click the **"Copy"** icon right next to your new key (it usually looks like two overlapping squares 📋). Make sure you copy the *entire* key! Keep this key safe and secret – you'll need it in a moment!

-----

### **Step 2: Prepare Your Linux System (Setting Up Your "Workshop")**

Now, let's get your Linux computer ready for `GERMINAL`! We'll use a powerful text-based tool called the "terminal."

1.  **Open Your Terminal:**
    * Usually by pressing `Ctrl` + `Alt` + `T`.
    * Or look for "Terminal," "Konsole," etc., in your applications menu.

2.  **Update Your Computer's Software List:**
    In the terminal window, type this command exactly as you see it, and then press `Enter`:
    ```bash
    sudo apt update
    ```
    * Enter your password when prompted (typing will be invisible).

3.  **Install Essential Tools (`GERMINAL`'s Foundations!):**
    Type this entire command into your terminal and press `Enter`:
    ```bash
    sudo apt install python3 python3-pip python3-venv git -y
    ```
    * **`python3`**: The programming language `GERMINAL` is written in.
    * **`python3-pip`**: Installs other Python "libraries."
    * **`python3-venv`**: Creates "virtual environments."
    * **`git`**: Downloads project code.
    * **`-y`**: Auto-confirms installation.

4.  **Create a Cozy Home for `GERMINAL`'s Code:**
    ```bash
    mkdir -p ~/Projects/dev
    ```

5.  **Step Inside Your New Project Folder:**
    ```bash
    cd ~/Projects/dev
    ```

6.  **Download `GERMINAL`'s Secret Sauce (Clone the Repository):**
    ```bash
    git clone [https://github.com/elijahcommits/germinal.git](https://github.com/elijahcommits/germinal.git)
    ```
    * This creates a new folder named `germinal`.

7.  **Dive into the `GERMINAL` Project Folder:**
    ```bash
    cd germinal
    ```
    * You should now be in `~/Projects/dev/germinal`.

8.  **Create a Virtual Environment (Your Super Clean Workspace!):**
    ```bash
    python3 -m venv venv
    ```
    * This creates an isolated "box" called `venv` inside your `germinal` folder for its Python libraries.

9.  **Activate Your Virtual Environment (Step Inside the Box!):**
    ```bash
    source venv/bin/activate
    ```
    * Your terminal prompt should now start with **`(venv)`**. This means you're working inside `GERMINAL`'s isolated space.

-----

### **Step 3: Install `GERMINAL`'s Brains and Beauty (All the Goodies!)**

Now that your virtual environment is active (you see `(venv)` at your prompt!), let's install the Python libraries `GERMINAL` needs.

1.  **Install `GERMINAL`'s Libraries:**
    Make sure your `(venv)` is active. Then, type this command and press `Enter`:
    ```bash
    pip install -r requirements.txt
    ```
    * **`pip install -r requirements.txt`**: This tells `pip` to read the list of libraries `GERMINAL` needs from `requirements.txt` (which came with the code) and install them *into your active virtual environment*.

-----

### **Step 4: Make `GERMINAL` Super Accessible (Your Instant Command!)**

Let's make `gg` a command you can type anywhere in your terminal!

1.  **Tell Your Computer Your Secret AI Key Permanently:**
    We need to set an environment variable for your API key.
    * Open your `.bashrc` file (a special file your terminal runs at startup):
        ```bash
        nano ~/.bashrc
        ```
    * Scroll to the **very end** of the file.
    * On a new, empty line, add the following (replace `'YOUR_ACTUAL_API_KEY_HERE'` with the *exact* API key you copied in Step 1!):
        ```bash
        export GOOGLE_API_KEY='YOUR_ACTUAL_API_KEY_HERE'
        ```
    * **Save and Exit `nano`:** Press `Ctrl` + `O`, then `Enter`, then `Ctrl` + `X`.
    * **Apply Changes to Your Current Terminal:**
        ```bash
        source ~/.bashrc
        ```

2.  **Make `gg.py` Executable:**
    Ensure you are in your `GERMINAL` project folder (`~/Projects/dev/germinal`). The `gg.py` script already has the necessary `#!/usr/bin/env python3` line.
    ```bash
    chmod +x gg.py
    ```
    * **`chmod +x`**: Grants "execute" permission to the file.

3.  **Create a Special Folder for Your Personal Commands (if it doesn't exist):**
    ```bash
    mkdir -p ~/bin
    ```
    * Your system often automatically checks `~/bin` for commands. If it doesn't, you might need to add `export PATH="$HOME/bin:$PATH"` to your `~/.bashrc` and run `source ~/.bashrc` (but try without this first, as it's usually pre-configured).

4.  **Create a "Shortcut" (Symbolic Link) for `gg`!**
    This lets you just type `gg` from anywhere.
    * Make sure you are in your `GERMINAL` project folder: `cd ~/Projects/dev/germinal`
    * Create the shortcut:
        ```bash
        ln -s "$(pwd)/gg.py" ~/bin/gg
        ```
        * **`ln -s`**: Creates a symbolic link.
        * **`"$(pwd)/gg.py"`**: Gets the full path to your `gg.py`.
        * **`~/bin/gg`**: Creates the shortcut named `gg` in `~/bin/`.

5.  **Set up your Ems Folder Structure:**
    `GERMINAL` looks for "ems" in an `ems` folder located in the same directory as `gg.py`.
    * Make sure you are in your `GERMINAL` project folder: `cd ~/Projects/dev/germinal`
    * Create the main ems folder and the subfolder for global ems:
        ```bash
        mkdir -p ems/_global
        ```
    * This creates `~/Projects/dev/germinal/ems/` and `~/Projects/dev/germinal/ems/_global/`.

-----

### **Step 5: Customize `GERMINAL`! (Your Personal Touch! ✨)**

`GERMINAL` allows for powerful customization!

1.  **Customize Colors (via `gg_config.htgeml`):**
    * Your `GERMINAL` tool comes with `gg_config.htgeml` located in `~/Projects/dev/germinal/`. Open it with `nano ~/Projects/dev/germinal/gg_config.htgeml`.
    * Inside the `<colors>` section, you'll see lines like `<response-text color="cyan" />`.
    * Change the `color` value to:
        * Basic: `black`, `red`, `green`, `yellow`, `blue`, `magenta`, `cyan`, `white`
        * Brighter: `light_red`, `light_green`, etc.
    * Experiment to find your favorite look! 🎨 Save and exit `nano`.

2.  **Create Your Own "Ems" (via `.gss` files)!**
    "Ems" are your custom command templates, now defined in `.gss` files within the `~/Projects/dev/germinal/ems/` directory.

    * **Structure of a `.gss` file:**
        It's a simple text file. Each em definition looks like this:
        ```gss
        your-em-name-here {
            param: "Your prompt template text INPUT_PLACEHOLDER more text.";
            param: "An optional second part of the prompt."; /* All 'param' values are joined */
            description: "A short note about what this em does."; /* Optional */
            author: "Your Name"; /* Optional */
        }

        another-em-name {
            param: "This em acts as a general instruction.";
            /* It doesn't need INPUT_PLACEHOLDER if it's not meant to take direct user input */
        }
        ```
        * **`your-em-name-here`**: The name you'll use (e.g., `gg em:your-em-name-here ...`). Must be one word (can use hyphens).
        * **`param: "..."`**: This defines a piece of the prompt. All `param` lines within an em block are concatenated together to form the full prompt for that em. You **must** end each `param` line with a semicolon `;`.
        * **`INPUT_PLACEHOLDER`**: This is crucial! For ems that take user input, this exact string (`INPUT_PLACEHOLDER`) in your `param` text will be replaced by whatever you type after the em call (e.g., in `gg em:my-em "this part"`, "this part" replaces `INPUT_PLACEHOLDER`).
        * You can have other properties like `description: "text";` or `author: "text";`. These are loaded but not directly used by the default script logic (you could extend the script to use them!).
        * Avoid using literal `{` or `}` characters in your `param` strings unless they are part of the `INPUT_PLACEHOLDER` itself, as they can interfere with parsing. Use `(` `)` or other alternatives if needed.

    * **Creating a Callable Em:**
        1.  Go to your ems folder: `cd ~/Projects/dev/germinal/ems/`
        2.  Create a new file, e.g., `my_utility_ems.gss`: `nano my_utility_ems.gss`
        3.  Add your em definition:
            ```gss
            story-idea {
                param: "Write a short, engaging INPUT_PLACEHOLDER story about a talking animal who saves the day.";
                description: "Generates a story idea based on a genre.";
            }
            ```
        4.  Save and exit.
        5.  Usage: `gg em:story-idea "fantasy"`
            `GERMINAL` replaces `INPUT_PLACEHOLDER` with "fantasy" and sends the combined prompt.

    * **Creating a Global Em (Always Active):**
        Global ems provide context or instructions that are *always* prepended to your queries or other em calls.
        1.  Go to the global ems subfolder: `cd ~/Projects/dev/germinal/ems/_global/`
        2.  Create a new file, e.g., `persona.gss`: `nano persona.gss`
        3.  Add your global em definition:
            ```gss
            always-polite {
                param: "Please ensure all your responses are extremely polite and begin with 'Salutations!'.";
            }
            ```
        4.  Save and exit.
        5.  This em will now automatically activate. You don't call it directly. When you type `gg "hello"`, the actual prompt sent will include the "always-polite" instruction.
        6.  You can disable all global ems for a single query with the `--no-global-ems` flag: `gg --no-global-ems "just give me the facts"`

-----

## **🎉 YOU DID IT! Time to Unleash `GERMINAL`! 🎉**

Congratulations! You've successfully set up `GERMINAL`! 👏

1.  **Open a *BRAND NEW* Terminal Window:** This is super important to ensure all new settings and PATH changes are loaded.

2.  **Ask `GERMINAL` Anything (Quick Questions!):**
    ```bash
    gg "What is the highest mountain in the world?"
    ```
    ```bash
    gg "Tell me a fun fact about giraffes."
    ```

3.  **Start an Interactive Chat (Let's Talk!):**
    ```bash
    gg chat
    ```
    You'll see `(Gemini) > `. Type questions, press `Enter`. Exit with `exit`, `quit`, `bye`, or `Ctrl+C`.

4.  **Use Your Custom Callable "Ems" (Your Superpowers!):**
    If you created the `story-idea` em:
    ```bash
    gg em:story-idea "mystery"
    ```
    The text "mystery" will replace `INPUT_PLACEHOLDER` in your `story-idea` em's prompt.

5.  **Global Ems In Action:**
    If you created the `always-polite` global em, just try a normal query:
    ```bash
    gg "What's the weather like?"
    ```
    The response should reflect the global instruction! To temporarily ignore it:
    ```bash
    gg --no-global-ems "What's the weather like?"
    ```

6.  **Change the AI Model (For the Curious!):**
    Use the `-m` flag:
    ```bash
    gg -m gemini-1.5-pro-latest "Give me a creative name for a new coffee shop."
    ```
    Your default is `gemini-1.5-flash-latest` (set in `gg.py`).

-----

## **💡 Troubleshooting (Friendly Help if You Hit a Snag!)**

* **`gg: command not found`**
    * **Solutions:**
        1.  Did you open a **new terminal window** after Step 4?
        2.  Check the symlink: `ls -l ~/bin/gg` (should point to `.../germinal/gg.py`). If not, re-do Step 4.4.
        3.  Verify `~/bin` is in your PATH: `echo $PATH`. If not, you might need to add `export PATH="$HOME/bin:$PATH"` to `~/.bashrc` and `source ~/.bashrc` (and open a new terminal).

* **`Error: GOOGLE_API_KEY environment variable not set.`**
    * **Solution:** Ensure Step 4.1 was completed correctly (key in `~/.bashrc`, saved, and `source ~/.bashrc` run). Check for typos.

* **`ModuleNotFoundError: No module named 'google'` (or `rich`, etc.)**
    * **Problem:** Python can't find necessary libraries.
    * **Solution:**
        1.  Make sure your virtual environment is active! You should see `(venv)` at the start of your terminal prompt. If not, navigate to `~/Projects/dev/germinal` and run `source venv/bin/activate`.
        2.  Once the venv is active, re-run `pip install -r requirements.txt` from within the `~/Projects/dev/germinal` directory.

* **Em not found or not working:**
    * **Solutions:**
        1.  **File Location:** Ensure your `.gss` file is in the `~/Projects/dev/germinal/ems/` directory (or `ems/_global/` for global ems).
        2.  **Syntax:** Carefully check the syntax within your `.gss` file. Each em block should be `em-name { ... }`. Each `param` line inside must be `param: "text content INPUT_PLACEHOLDER text";` (note the colon, quotes, and semicolon).
        3.  **Placeholder:** Ensure you are using `INPUT_PLACEHOLDER` exactly if your em is meant to take input.
        4.  **Curly Braces:** Avoid using literal `{` or `}` characters within your `param` string text, as they can interfere with parsing. Use alternatives like `()` if you need to group text.
        5.  **Permissions:** Unlikely, but ensure `gg.py` can read the `.gss` files.
        6.  **Debug Output:** The "Loading .gss file..." messages and any warnings during startup (when you first run `gg`) can provide clues.

* **`Error communicating with Gemini (model: ...): 429 You exceeded your current quota...`**
    * **Problem:** Free tier rate limits.
    * **Solutions:** Wait, switch to a "Flash" model (`gemini-1.5-flash-latest` is default and good for this), or check [Google's rate limits documentation](https://ai.google.dev/gemini-api/docs/rate-limits).

* **`Error communicating with Gemini (model: ...): 404 models/... is not found`**
    * **Problem:** Model unavailable.
    * **Solution:** Use `gemini-1.5-flash-latest` or another known available model.

* **Colors not showing up:**
    * **Solution:**
        1.  Ensure libraries installed correctly (Step 3 in venv).
        2.  Check `~/Projects/dev/germinal/gg_config.htgeml` for correct color names and XML structure.

-----

### **🔑 Crucial Security Step: What if My API Key is Exposed? 🔑**

If you ever accidentally show or commit your API key to a public place (like on a social media post, a public GitHub repository, or anywhere else!), you **MUST** take these steps immediately:

1.  **Immediately revoke the exposed API key:** Go back to [Google AI Studio](https://aistudio.google.com/app/apikey), find the exposed key, and click the "Delete" or "Revoke" button next to it. This stops the exposed key from working immediately.
2.  **Generate a brand new API key:** Create a fresh key on the same page.
3.  **Update your `GOOGLE_API_KEY`:** Replace the old key in your `~/.bashrc` file (from Step 4.1) with your new, secret key, and run `source ~/.bashrc`.
4.  While Git history rewriting can remove it from *future* clones, **revoking the key is the absolute most critical immediate step** to prevent unauthorized use.

-----

## **💖 Getting Involved & Feedback!**

`GERMINAL` is your tool! We'd love to hear your ideas for new "ems," suggestions for amazing features, or if you run into any issues not covered here. Feel free to open an issue or discussion on the project's GitHub repository.

## Happy exploring with `GERMINAL`! ✨🚀🌟
