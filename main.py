import os
import asyncio
import datetime
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

# Define tool
@function_tool
def get_info_coin(symbol: str) -> str:
    url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol.upper()}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        return f"The current price of {symbol.upper()} is {data['price']} USDT"
    else:
        return "Failed to fetch price. Please check the symbol."

# Define agent
agent = Agent(
    name="Crypto Price Agent",
    instructions="""
You are a helpful Crypto Price Agent.

- When the user mentions a symbol like BTCUSDT, ETHUSDT, or SOLUSDT, you MUST use the `get_info_coin` tool.
- DO NOT make up prices.
- If no symbol is given, respond helpfully or explain how to use the tool.

Only use the tool when a valid symbol is mentioned.
"""
    ,
    model=model,
    tools=[get_info_coin],
)

# Streamlit UI
st.title("🪙 Crypto Price Assistant")
st.markdown(
    """
    Ask any question about crypto prices or market.

    **💡 Note:** Please use coin symbols like `BTCUSDT`, `ETHUSDT`, or `SOLUSDT` instead of coin names like 'bitcoin', 'ethereum', or 'solana'.
    """
)

user_input = st.text_input("Enter your crypto-related query:", "")
if st.button("Get Answer") and user_input.strip():
    # Step 1: Detect common symbols
    symbols = ["BTCUSDT", "ETHUSDT", "SOLUSDT", "BNBUSDT", "DOGEUSDT"]
    query = user_input.strip().upper()
    detected_symbol = next((s for s in symbols if s in query), None)

    if detected_symbol:
        st.info(f"🔍 Detected symbol: {detected_symbol}")
    else:
        st.warning("⚠️ No valid symbol detected. Please use symbols like BTCUSDT, ETHUSDT, etc.")

    # Step 2: Run the agent
    async def run_agent():
        result = await Runner.run(agent, user_input, run_config=config)
        return result.final_output

    result = asyncio.run(run_agent())
    st.success("✅ Answer:")
    st.write(result)
