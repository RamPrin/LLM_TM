import requests
import json
import re
import os
import time
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--path', default="data/")
parser.add_argument('--host', default="http://localhost:8000")
parser.add_argument('--mode', default='arch', choices=['arch', 'analyze', 'model'])
parser.add_argument('--agent', default='gpt-4o')
parser.add_argument('-r', '--recursive', action='store_true')
args = parser.parse_args()

def write_this_down(response, path: str, model: str):
    dir_ = os.path.dirname(path)
    with open(f"{dir_}/response_{model}.json", "w", encoding="utf-8") as f:
        f.write(json.dumps(response))
    text = response["response"]
    with open(f"{dir_}/response_1_{model}.md", 'w', encoding="utf-8") as f:
        f.write(text)
    model : list[re.Match[str]] = re.findall(r"# Model:\n```python([\S\s]*?)\n```", text)
    if len(model) != 0:
        with open(f"{dir_}/model_1_{model}.py", "w", encoding="utf-8") as f:
            f.write(model[0])
    else:
        raise Exception("Failed to get model code :(")

def one_agent(content: str, model: str, path: str):
    response = requests.post(
        f"{args.host}/one_agent",
        json={
            "description": content,
            "model": model
        }
    )
    try:
        write_this_down(response.json(), path, model)
    except Exception as e:
        print(e)

def modelize(description: str, agent: str, path: str):
    response = requests.post(
        f"{args.host}/modelize",
        json={
            "description": description,
            "model": agent
        },
        timeout=10000
    ).json()
    model = response["model"]
    if len(model) != 0:
        with open(f"{os.path.dirname(path)}/model_2_{agent}.py", "w", encoding="utf-8") as f:
            f.write(model)

def analyze(model: str, agent: str, path: str):
    response = requests.post(
        f"{args.host}/analyze",
        json={
            "model": model,
            "agent": agent
        }, 
        timeout=10000).json()
    with open(f"{os.path.dirname(path)}/response_2_{agent}.md", "w", encoding="utf-8") as f:
        f.write(response["threats"])
    
def process(mode: str, content: str, agent: str, path: str):
    if mode == "arch":
        one_agent(content, agent, path)
    elif mode == "model":
        modelize(content, agent, path)
    elif mode == "analyze":
        analyze(content, agent, path)

if __name__ == "__main__":
    if not args.r:
        path = os.path.abspath(args.path)
        if not os.path.isfile(path):
            path = os.path.join(
                path,
                "description.md" if args.mode != 'analyze' 
                else f"model_2_{args.agent}.py"
            )
        process(args.mode, open(path).read(), args.agent, path)
    else:
        for (base, fold, file) in os.walk(os.path.abspath(args.path)):
            path = os.path.join(
                base,
                "description.md" if args.mode != 'analyze' 
                else f"model_2_{args.agent}.py"
            )
            if os.path.exists(path):
                process(args.mode, open(path).read(), args.agent, path)
