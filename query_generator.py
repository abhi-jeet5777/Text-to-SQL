# query_generator.py

import boto3
import json
import os
from dotenv import load_dotenv

load_dotenv()

def get_bedrock_client():
    return boto3.client(
        service_name="bedrock-runtime",
        region_name=os.getenv("AWS_REGION"),
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    )

def generate_sql_from_prompt(prompt: str, schema_description: str) -> str:
    client = get_bedrock_client()
    model_id = os.getenv("BEDROCK_MODEL_ID")

    full_prompt = f"""
You are a helpful assistant that converts natural language questions into SQL queries.

Given the following SQLite database schema:
{schema_description}

Convert this natural language question into a SQL query:
Question: "{prompt}"
Only return the SQL code without any explanation.
"""

    payload = {
        "anthropic_version": "bedrock-2023-05-31",
        "messages": [
            {
                "role": "user",
                "content": full_prompt.strip()
            }
        ],
        "max_tokens": 300,
        "temperature": 0.3,
        "top_p": 0.9,
        "stop_sequences": ["```", "<|end|>"]
    }

    try:
        response = client.invoke_model(
            body=json.dumps(payload),
            modelId=model_id,
            accept="application/json",
            contentType="application/json"
        )

        response_body = json.loads(response["body"].read())

        content_list = response_body.get("content", [])
        if content_list and isinstance(content_list[0], dict):
            return content_list[0].get("text", "").strip()

        return "-- ERROR: No valid content returned by model."

    except Exception as e:
        return f"-- ERROR: {str(e)}"
