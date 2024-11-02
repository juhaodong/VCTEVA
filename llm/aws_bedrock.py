import boto3
import json
from typing import List, Tuple


def message_builder(system_prompt: str, message: str, history: List[Tuple[str, str]]):
    """
    为多模态模型构建消息格式，bedrock
    """
    messages = []
    for user_msg, assistant_msg in history:
        if user_msg:
            user_msg = [{"text": user_msg}]
            messages.append({"role": "user", "content": user_msg})
        if assistant_msg:
            assistant_msg = [{"text": assistant_msg}]
            messages.append({"role": "assistant", "content": assistant_msg})

    message = [{"text": system_prompt +
                "### Based on the requirements above, respond to the following qeury: " + message}]
    messages.append({"role": "user", "content": message})

    return messages


def bedrock_completion(messages: list[dict[str, str]]):

    # 初始化 bedrock 客户端

    # 初始化 bedrock 客户端
    # model_id = 'meta.llama3-70b-instruct-v1:0' #'meta.llama3-70b-instruct-v1:0'
    # model_id = "anthropic.claude-3-sonnet-20240229-v1:0"
    bedrock_client = boto3.client(

        # Inference parameters to use.
        # temperature = 0.7
        service_name='bedrock-runtime', region_name="eu-central-1")
    model_id = "anthropic.claude-3-haiku-20240307-v1:0"
    # Base inference parameters to use.
    # inference_config = {"temperature": temperature}
    # Additional inference parameters to use.
    # additional_model_fields = {"top_k": top_k}

    # Send the message.
    top_k = 0.9

    response = bedrock_client.converse(
        # system=system_prompts, #效果不太好
        # inferenceConfig=inference_config
        # additionalModelRequestFields=additional_model_fields
        modelId=model_id,
        messages=messages,
    )

    return response['output']['message']['content'][0]['text']
