from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

#client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
client = "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"
def get_ai_summary_and_steps(rfp_text):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are an assistant trained to analyze Requests for Proposals (RFPs). Your tasks are: 1) Summarize the most important points from the RFP. 2) Break down key details into actionable steps. 3) Propose a detailed plan with suggested actions for the agent to follow. 4) Provide recommendations for next steps and follow-up proposals."},
            {"role": "user", "content": rfp_text}
        ]
    )
    summary = response.choices[0].text
    return summary