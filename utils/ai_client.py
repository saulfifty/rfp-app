import openai
from dotenv import load_dotenv
import os

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")
print(f"API Key: {openai.api_key}")

def get_ai_summary_and_steps(rfp_text):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are an assistant trained to analyze Requests for Proposals (RFPs). Your tasks are: 1) Summarize the most important points from the RFP. 2) Break down key details into actionable steps. 3) Propose a detailed plan with suggested actions for the agent to follow. 4) Provide recommendations for next steps and follow-up proposals."},
            {"role": "user", "content": rfp_text}
        ]
    )
    summary = response["choices"][0]["message"]["content"]
    return summary
