import streamlit as st
from openai import OpenAI
from pydantic import BaseModel
from file_operations import log_to_csv
from system_prompt import system_message_v1

OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
client = OpenAI(api_key=OPENAI_API_KEY)

st.title("Contamination and Unfairness Judge 🎓")
st.write("Submit your base code and user prompt!")

task_id = st.text_area("Task ID", "Provide the task ID")
base_code = st.text_area("Base Code", "Provide the base code")
user_prompt = st.text_area("Prompt", "Provide the prompt.")
additional_context = st.text_area("Additional Context", "Provide additional context.")


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
            {"role": "system", "content": system_message},
            {"role": "user", "content": prompt}
        ],
        response_format=response_format,
    )
    return response.choices[0].message.parsed


if st.button("Evaluate"):
    with st.spinner("Evaluating..."):
        system_prompt = system_message_v1
        system_version = "v1"
        response_format = LLMJudge

        prompt = str({
            'base_code': base_code,
            "system_prompt": user_prompt,
            "additional_context": additional_context,
        })

        result = get_review(prompt, system_prompt, response_format)

        log_to_csv(task_id, system_version, base_code, user_prompt, result)

        st.subheader("Evaluation Result:")
        st.write(result)