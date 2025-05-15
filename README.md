# Bird Watch Companion Bot

Bird Watch Companion Bot is a smart Streamlit application that helps you identify bird species from images and region input, and then generates a comprehensive observation and care guide. Powered by [Agno](https://github.com/agno-agi/agno), OpenAI's GPT-4o, and SerpAPI, the bot searches for high-quality habitat data, feeding insights, and conservation resources to deliver a beautifully formatted report for birdwatchers and nature enthusiasts.

## Folder Structure

```
Bird-Watch-Companion-Bot/
├── bird-watch-companion-bot.py
├── README.md
└── requirements.txt
```

* **bird-watch-companion-bot.py**: The main Streamlit application.
* **requirements.txt**: Required Python packages.
* **README.md**: This documentation file.

## Features

* **Bird Image + Region Input**
  Upload a bird photo and enter the region where it was spotted. Optionally describe the bird's behavior to improve identification.

* **AI-Powered Bird Identification**
  The Bird Species Identifier agent analyzes your image and classifies the bird using visual traits and region-specific context.

* **Real-Time Ecological Research**
  The Bird Habitat Researcher agent generates a focused Google search to find region-specific data on feeding habits, migration, nesting, and conservation.

* **Comprehensive Bird Report**
  The Birdwatching Guide Generator compiles a markdown-based report with structured sections on diet, activity, nesting, habitat, and conservation.

* **Structured Markdown Output**
  Reports are formatted with clean markdown sections, bullet points, and hyperlinked sources — great for field references or printing.

* **Download Option**
  Download the generated bird report as a `.md` file for offline access, study, or sharing.

* **Clean Streamlit UI**
  Built with Streamlit for an intuitive, fast, and responsive user experience.

## Prerequisites

* Python 3.11 or higher
* An OpenAI API key ([Get one here](https://platform.openai.com/account/api-keys))
* A SerpAPI key ([Get one here](https://serpapi.com/manage-api-key))

## Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/akash301191/Bird-Watch-Companion-Bot.git
   cd Bird-Watch-Companion-Bot
   ```

2. **(Optional) Create and activate a virtual environment**:

   ```bash
   python -m venv venv
   source venv/bin/activate        # On macOS/Linux
   # or
   venv\Scripts\activate           # On Windows
   ```

3. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. **Run the app**:

   ```bash
   streamlit run bird-watch-companion-bot.py
   ```

2. **In your browser**:

   * Enter your OpenAI and SerpAPI keys in the sidebar.
   * Upload a bird image and provide location and behavior details.
   * Click **🐦 Generate Bird Report** to start the analysis.
   * View and download the AI-generated birdwatching guide.

3. **Download Option**
   Use the **📥 Download Bird Report** button to save the markdown report for offline use.

## Code Overview

* **`render_bird_profile()`**: Collects bird image, region, and behavior input from the user.
* **`render_sidebar()`**: Stores API keys securely via the Streamlit sidebar.
* **`generate_bird_report()`**:

  * Uses the `Bird Species Identifier` agent to analyze the image and identify the bird.
  * Leverages `Bird Habitat Researcher` to find ecological data via SerpAPI.
  * Combines everything into a report using the `Birdwatching Guide Generator` agent.
* **`main()`**: Controls layout, input collection, agent workflow, and report rendering.

## Contributions

Contributions are welcome!
Feel free to fork the repo, suggest features, report bugs, or open a pull request. Make sure your changes are clear, tested, and aligned with the project’s educational and conservation-friendly goals.
