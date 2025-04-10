import streamlit as st
from openai import OpenAI

from pydantic import BaseModel

OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
client = OpenAI(api_key=OPENAI_API_KEY)

st.title("Contamination and Unfairness Judge 🎓")
st.write("Submit your base code and user prompt!")

base_code = st.text_area("Base Code", "Provide the base code")
user_prompt = st.text_area("Prompt", "Provide the prompt.")


class TaskData(BaseModel):
    judge_response: str


class LLMJudge(TaskData):
    contaminated: bool
    contamination_link: str
    ambiguous_unfair: bool
    problem_description: str
    suggested_fix: str
    confidence_rating: str


def get_review(prompt, system_message, response_format):
    response = client.beta.chat.completions.parse(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": (
                    system_message
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        response_format=response_format,
    )

    return response.choices[0].message.parsed


if st.button("Evaluate"):
    with st.spinner("Evaluating..."):
        system_prompt = """
You are an expert coding task evaluator. Your job is to detect and report whether a programming prompt suffers from:
	1.	Contamination — The task or its solution can be found online in the same or a very similar form (e.g., LeetCode, Stack Overflow, GeeksforGeeks, and a Google search engine).
	2.	Unfairness — The task’s requirements are vague, inconsistent, or imply behavior that is under-specified (e.g., requiring time extraction logic without defining what constitutes a valid time).

Your output must follow this schema and provide clarity for educators or reviewers designing new problems.

Structure of Your Output (for JSON parsing):

{
  "contaminated": <true|false>,
  "contamination_link": "<if contaminated, give URL to matching problem or leave blank>",
  "ambiguous_unfair": <true|false>,
  "problem_description": "<why it is contaminated or unfair (e.g., too similar to GeeksforGeeks post or unclear rules)>",
  "suggested_fix": "<how to make the task more unique or fair>",
  "confidence_rating: percentage
}

Guidelines to Determine Contamination:
	•	Search for core logic or task phrasing online.
	•	If similar code or the same objective exists with minor variations, flag it as contaminated.

Guidelines to Determine Unfairness:
	•	Look for implied behavior not explicitly defined (e.g., multiple valid interpretations of the goal).
	•	Check whether required outputs (e.g., overlapping time extraction) are fully explained.

Examples of Suggested Fixes for Contaminated or Unfair Prompts:
	•	To decontaminate: Introduce additional constraints, dynamic inputs, or new output formats. For example:
	•	“Only return the earliest valid time found.”
	•	“Support delimiters other than colons (e.g., |, ,).”
	•	To remove unfairness: Define time validity clearly (e.g., must match hh:mm:ss with 0 <= hh < 24, etc.), and clarify how overlapping cases should be handled.

Think clearly about the information above before you provide a response. The link has to match the base code and the prompt. 
You should also include your level of confidence and suggest if there is a need to confirm your response.
⸻
        """
        response_format = LLMJudge

        prompt = str({
            'base_code': base_code,
            "prompt": user_prompt
        })

        response = get_review(prompt, system_prompt, response_format)

        result = response
        st.subheader("Evaluation Result:")
        st.write(result)