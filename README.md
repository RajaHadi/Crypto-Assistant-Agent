# 🪙 Crypto Price Agent

A real-time AI-powered assistant that answers cryptocurrency price questions using live market data from CoinGecko API. Built with [Streamlit](https://streamlit.io/) and [OpenAI Agents SDK](https://platform.openai.com/docs/agents).

> 🎓 Built as a homework project for hands-on learning with LLMs, APIs, and interactive UIs.

---

## 🔗 Live Demo

🚀 Try it now: [crypto-assistant-agent.streamlit.app](https://crypto-assistant-agent-umrzr6lqrfeadd7jjbb7gp.streamlit.app/)

---

## ⚙️ Features

- ✅ Ask about crypto prices using trading symbols (e.g., `BTCUSDT`, `ETHUSDT`)
- ✅ Live data via [CoinGecko API](https://www.coingecko.com/en/api)
- ✅ Natural language understanding using Gemini (Google's AI model)
- ✅ Clean, interactive UI with Streamlit
- ✅ Hosted on Streamlit Cloud (100% free)

---

## 🛠 Tech Stack

| Tech           | Purpose                         |
|----------------|---------------------------------|
| `Streamlit`    | Frontend UI                     |
| `OpenAI Agents SDK` | Agent-based LLM framework     |
| `Gemini API`   | AI model (via OpenAI Agents SDK)|
| `CoinGecko API`| Live crypto price data          |
| `Python`       | Backend logic & tools           |

---

## 📦 Setup Instructions

### 1. Clone the repo

```bash
git clone https://github.com/your-username/crypto-price-agent.git
cd crypto-price-agent
2. Install dependencies (using uv)
bash
Copy
Edit
uv pip install streamlit python-dotenv openai-agents requests
Or use traditional pip:

bash
Copy
Edit
pip install -r requirements.txt
3. Add your .env file
ini
Copy
Edit
GEMINI_API_KEY=your_gemini_api_key_here
Get your Gemini key from Google AI Studio

4. Run the app
bash
Copy
Edit
streamlit run app.py
