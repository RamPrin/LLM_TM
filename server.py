from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI
from typing import Literal
import requests
import re
import anthropic
import os

app = FastAPI()
client_gpt = OpenAI()
client_claude = anthropic.Anthropic()
template="""
# Model:
<!---
Insert PyTM threat model as a codeblock:
- Boundaries
- Components
- Dataflows
tm.process()
-->
# Threats
<!---
Write list of threats for each STRIDE category in the following format:
Spoofing:
[List of all threats about Spoofing in format "Title: Short description"]
Tampering
[List of all threats about Tampering in format "Title: Short description"]
Repudiation
[List of all threats about Repudiation in format "Title: Short description"]
Information Disclosure
[List of all threats about Information Disclosure in format "Title: Short description"]
Denial of Service
[List of all threats about Denial of Service in format "Title: Short description"]
Elevation of Privilege
[List of all threats about Elevation of Privilege in format "Title: Short description"]
-->
"""
instructions = {
    "model":  "Compose a threat model from description using PyTM library. Use the last PyTM library version. Provide only model code snippet",
    
    "analyze": "Analyze the following threat model and retrieve threats. "
    "Use STRIDE methodology. Give only list of threats categorized by STRIDE with threat title and brief description."
    "Find as many threats as you can."
    "Evaluate these threats with DREAD approach.",

    "arch": "Compose the model from description using PyTM and analyze it for threats by STRIDE methodology."
    "Use the latest PyTM library version. Find as many threats as you can"
    f"Use the following template as an output:\n{template}"
}


class Query(BaseModel):
    model: str = 'gpt-4o'
    description: str

class TM(BaseModel):
    agent: str = 'gpt-4o'
    model: str



def ask_llm(content: str, model: str, role: Literal["model", "analyze", "arch"]):
    if model == "sonnet_3.7":
        return client_claude.messages.create(
            model="claude-3-7-sonnet-20250219",
            max_tokens=2048,
            messages=[
                {"role": "system", "content": instructions[role]},
                {"role": "user", "content": content}
            ]
        ).content
    else:
        return client_gpt.responses.create(
        model=model,
        input=content,
        instructions=instructions[role]
        ).output_text

@app.post("/modelize")
def modelize(description: Query):
    text = ask_llm(description.description, description.model, 'model')
    if "```python" not in text:
        text = f"```python\n{text}\n```"
    model : list[re.Match[str]] = re.findall(r"```python([\S\s]*?)\n```", text)
    return {"response": text, "model": model[0] if len(model) > 0 else ""}

@app.post("/analyze")
def analyze(model: TM):
    return {"threats": ask_llm(model.model, model.agent, 'analyze')}

@app.post("/one_agent")
def arch(description: Query):
    text = ask_llm(description.description, description.model, 'arch')
    model : list[re.Match[str]] = re.findall(r"# Model:\n```python([\S\s]*?)\n```", text)
    if len(model) != 0:
        model = model[0]
    else:
        model = ""
    threats = re.findall(r"(#\s*Threats[\S\s]*)", text)
    if len(threats) != 0:
        threats = threats[0]
    else:
        threats = ""
    return {
        "response": text,
        "model": model,
        "threats": threats
    }
