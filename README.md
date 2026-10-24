# Crucible

**Pitch it. We'll try to break it.**

Crucible is an AI venture-capitalist chatbot that stress-tests your startup idea. Describe what you're building and it points out the logical gaps, market risks and weak spots, then asks the three questions you'll need to answer in a real investor meeting. Defend your idea, and it responds to your answers.

**Live demo:** https://crucible-ai-deawj2t9kt7rdrwfjpwbtk.streamlit.app/

<!-- Add a screenshot here: ![Crucible screenshot](screenshot.png) -->

## Features

- **Structured critique:** every first analysis covers Verdict, Market Risk, Business Model, Execution Risk and Competition, and ends with 3 targeted questions.
- **Defend your idea:** reply to the questions and the AI judges which points now hold up and which are still weak.
- **Adjustable harshness:** choose Firm, Ruthless or Brutal to change how hard the critique hits.
- **Chat history:** past pitches are saved in the sidebar so you can reopen and continue them.
- **Live model picker:** the model list is loaded from your Groq account, so retired models never break the app.
- **Starter pitches:** one-click example ideas so you can try it right away.
- **Streaming responses:** answers appear word by word instead of after a long wait.

## Tech Stack

| Layer | Tool |
|---|---|
| Interface | [Streamlit](https://streamlit.io/) with custom CSS |
| AI inference | [Groq](https://groq.com/) API (OpenAI-compatible) |
| API client | `openai` Python SDK |
| Hosting | Streamlit Community Cloud |

## Getting Started

### Prerequisites

- Python 3.9 or newer
- A free Groq API key from [console.groq.com/keys](https://console.groq.com/keys)

### Installation

```bash
git clone https://github.com/your-username/crucible.git
cd crucible
pip install -r requirements.txt
```

### Run locally

```bash
streamlit run app.py
```

Open the link shown in your terminal (usually http://localhost:8501) and paste your Groq API key in the sidebar under **Settings**.

### Optional: store your API key

So you don't have to paste the key every time, set it as an environment variable:

```bash
# macOS / Linux
export GROQ_API_KEY="your_key_here"

# Windows (PowerShell)
$env:GROQ_API_KEY="your_key_here"
```

Or create `.streamlit/secrets.toml`:

```toml
GROQ_API_KEY = "your_key_here"
```

Never commit your API key to GitHub.

## How It Works

1. You describe your idea in the chat.
2. The app sends your conversation to a Groq-hosted language model, together with a system prompt that makes it act as a rigorous venture capitalist. The harshness setting changes the tone of that prompt.
3. The response streams back and is saved to your chat history.
4. You answer the three questions, and the model critiques your defence.

## Project Structure

```
crucible/
├── app.py                 # The whole app: UI, styling, chat logic
├── requirements.txt       # Python dependencies
├── .streamlit/
│   └── config.toml        # Dark theme settings
└── chat_history.json      # Created automatically; do not commit
```

## Deployment

The app is deployed on Streamlit Community Cloud. To deploy your own copy:

1. Push this repository to GitHub.
2. Go to [share.streamlit.io](https://share.streamlit.io/) and create a new app from the repository.
3. Under **Advanced settings → Secrets**, add `GROQ_API_KEY = "your_key_here"`.

## Limitations

- Chat history is saved to a local file, so on a shared public deployment visitors can see each other's saved pitches. Don't enter confidential ideas in a public instance.
- Responses come from a language model and can be wrong or one-sided. Treat the critique as a prompt for thinking, not as investment advice.

## Roadmap

- [ ] Per-user chat history
- [ ] Export a critique as PDF
- [ ] Pitch scoring across market, team and traction
- [ ] Voice input for practising pitches out loud

## Author

Built by Dhanya.

## License

Add a `LICENSE` file (for example MIT) and name it here.
