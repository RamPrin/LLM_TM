# TMLLM

## Description

This is an example of server, which can communicate with OpenAI and Anthropic APIs to use LLMs for threat modeling

## Prerequisites

- Python 3.11.x

- Install prerequisites from requirements.txt

    ```bash
    pip install -i requirements.txt
    ```

- OpenAI and Anthropic API keys should be stored as enviroment variables (`OPENAI_API_KEY` and `ANTHROPIC_API_KEY`)

## Usage

Run the server by this command:

```bash
fastapi dev server.py
```

After this, SwaggerAPI should be accessible by (http://localhost:8000/docs) URL
