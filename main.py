import os
import asyncio
import requests
import streamlit as st
from dotenv import load_dotenv
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, function_tool
from agents.run import RunConfig

# Load environment variables
load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")

if not gemini_api_key:
    st.error("GEMINI_API_KEY is not set. Please add it to your .env file.")
    st.stop()

# Setup the external client
external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=external_client
)

config = RunConfig(
    model=model,
    model_provider=external_client,
    tracing_disabled=True
)

# Define the tool with logging and headers

@function_tool
def get_info_coin(symbol: str) -> str:
    print(f"🔧 Getting price for: {symbol}")
    
    # Convert symbol like BTCUSDT -> btc
    coin_map = {
        "BTCUSDT": "bitcoin",
        "ETHUSDT": "ethereum",
        "SOLUSDT": "solana",
        "BNBUSDT": "binancecoin",
        "DOGEUSDT": "dogecoin"
    }

    coin_id = coin_map.get(symbol.upper())
    if not coin_id:
        return "Symbol not supported in CoinGecko."

    try:
        url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin_id}&vs_currencies=usd"
        response = requests.get(url, timeout=5)
        print(f"📦 {response.status_code} - {response.text}")

        if response.status_code == 200:
            price = response.json()[coin_id]["usd"]
            return f"The current price of {symbol.upper()} is {price} USD"
        else:
            return "Failed to fetch price. Try again later."
    except Exception as e:
        print(f"❌ Exception: {e}")
        return "An error occurred while fetching price."

# Define agent
agent = Agent(
    name="Crypto Price Agent",
    instructions="""
You are a helpful Crypto Price Agent.

- When the user mentions a symbol like BTCUSDT, ETHUSDT, or SOLUSDT, you MUST use the `get_info_coin` tool.
- DO NOT make up prices.
- If no symbol is given, respond helpfully or explain how to use the tool.

Only use the tool when a valid symbol is mentioned.
""",
    model=model,
    tools=[get_info_coin],
)

# Streamlit UI
st.title("🪙 Crypto Price Assistant")
st.markdown("""
Ask any question about crypto prices or market.

**💡 Note:** Please use coin symbols like `BTCUSDT`, `ETHUSDT`, or `SOLUSDT` instead of names like 'bitcoin' or 'ethereum'.
""")

user_input = st.text_input("Enter your crypto-related query:", "")

if st.button("Get Answer") and user_input.strip():
    # Step 1: Detect symbol
    symbols = ["BTCUSDT", "ETHUSDT", "SOLUSDT", "BNBUSDT", "DOGEUSDT"]
    query = user_input.strip().upper()
    detected_symbol = next((s for s in symbols if s in query), None)



    # Step 2: Run the agent
    async def run_agent():
        result = await Runner.run(agent, user_input, run_config=config)
        return result.final_output

    try:
        result = asyncio.run(run_agent())
        st.success("✅ Answer:")
        st.write(result)
    except Exception as e:
        st.error(f"❌ Error: {e}")

