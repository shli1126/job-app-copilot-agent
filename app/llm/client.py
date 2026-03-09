import os
from openai import OpenAI
from dotenv import load_dotenv
from  pydantic import BaseModel
from typing import Type, TypeVar

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

MODEL = "gpt-4o-mini"

SchemaT = TypeVar("SchemaT", bound=BaseModel)

def call_llm(prompt: str):
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "You are a helpful career assistant."},
            {"role": "user", "content": prompt},
        ],
    )

    return response.choices[0].message.content

def call_llm_and_parse(prompt: str, schema: Type[SchemaT]) -> SchemaT:
    content = call_llm(prompt)
    return schema.model_validate_json(content)