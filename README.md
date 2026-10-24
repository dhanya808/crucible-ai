# Crucible

**Pitch it. We'll try to break it.**

Crucible is an AI venture capitalist that stress-tests startup ideas. Describe what you're building and it returns a structured, unsparing critique, then asks the three questions you'll need to answer in a real investor meeting. Argue back, and it judges your defence.

**Live demo:** https://crucible-ai-deawj2t9kt7rdrwfjpwbtk.streamlit.app/

<!-- Add a screenshot: ![Crucible screenshot](screenshot.png) -->

## Why Crucible

Startups rarely fail because of bad code. They fail because founders sit in echo chambers, and friends and teammates are often too polite to name the fatal flaw. Crucible gives you that honest conversation early, when fixing the flaw is still cheap.

## Features

- **Structured critique:** every first analysis covers Verdict, Market Risk, Business Model, Execution Risk and Competition.
- **Three defence questions:** each analysis ends with three targeted questions the founder must be able to answer.
- **Argue back:** Crucible keeps the conversation in context, so you can defend or pivot and it says which points now hold up.
- **Harshness control:** choose Firm, Ruthless or Brutal to change how hard the critique hits.
- **Saved chat history:** past pitches appear in the sidebar and can be reopened and continued.
- **Live model selection:** the model list is fetched from the provider, so a retired model does not break the app.
- **Streaming responses:** answers appear as they are written.
- **Custom interface:** a dark gradient theme with Bricolage Grotesque and Instrument Sans, built on Streamlit with custom CSS.

## Tech Stack

| Layer | Tool |
|---|---|
| Interface | [Streamlit](https://streamlit.io/) with custom CSS |
| Inference | [Nebius Token Factory](https://tokenfactory.nebius.com/) |
| Model | NVIDIA Nemotron family |
| API client | `openai` Python SDK (OpenAI-compatible endpoint) |
| Storage | Local JSON file |
| Hosting | Streamlit Community Cloud |

## Getting Started

### Prerequisites

- Python 3.9 or newer
- A Nebius Token Factory API key. Create one in the [API keys](https://tokenfactory.nebius.com/project/api-keys) section of the console.

### Install

```bash
git clone https://github.com/your-username/crucible.git
cd crucible
pip install -r requirements.txt
```

### Configure your API key

Set the key as an environment variable:

```bash
# macOS / Linux
export NEBIUS_API_KEY="your_key_here"

# Windows (PowerShell)
$env:NEBIUS_API_KEY="your_key_here"
```

Alternatively, add it to `.streamlit/secrets.toml`:

```toml
NEBIUS_API_KEY = "your_key_here"
```

Never commit your API key to GitHub.

### Run

```bash
streamlit run app.py
```

Open the address shown in the terminal (usually http://localhost:8501).

## How It Works

1. You describe your idea in the chat.
2. The app sends the conversation to a Nemotron model on Nebius Token Factory, through the OpenAI-compatible endpoint at `https://api.tokenfactory.nebius.com/v1/`.
3. A system prompt defines the investor persona and the critique format. The harshness setting adjusts its tone at runtime.
4. The reply streams back and is saved to your chat history.
5. You answer the three questions, and the model critiques your defence.

## Challenges

- **Overriding Streamlit's default styling:** inputs, dropdowns and chat elements kept falling back to a light theme, so each layer of their markup had to be styled.
- **Harsh but useful feedback:** early prompts were either vague or just insulting. Getting actionable, structural criticism took repeated prompt revisions and temperature tuning.
- **Consistent persona over long chats:** follow-up turns needed their own instructions so the model keeps its voice and format while the user argues and pivots.
- **Provider changes:** a model was retired mid-build, which led to loading the available models from the API instead of hard-coding names.

## Limitations

- Chat history is stored in a single local JSON file. On a shared public deployment, visitors can see each other's saved pitches, so do not enter confidential ideas in a public instance.
- Output comes from a language model and can be wrong or one-sided. Treat it as a prompt for thinking, not as investment advice.

## Roadmap

- [ ] Per-user accounts and private chat history
- [ ] Pitch deck upload with PDF parsing
- [ ] Text-to-speech so Crucible can deliver its critique out loud
- [ ] Speech input for practising pitches live
- [ ] Scorecards across market, team, traction and defensibility
- [ ] Export a critique as a PDF

## Author

Built by Dhanya.

## License

Add a `LICENSE` file (for example MIT) and name it here.
