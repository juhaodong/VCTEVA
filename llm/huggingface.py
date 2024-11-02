from huggingface_hub import InferenceClient
from typing import List, Tuple

def message_builder(system_prompt: str, message: str, history: List[Tuple[str, str]]):
    """
    为普通文本模型构建消息格式，huggingface的llama
    """
    messages = []
    for user_msg, assistant_msg in history:
        if user_msg:
            messages.append({"role": "user", "content": user_msg})
        if assistant_msg:
            messages.append({"role": "assistant", "content": assistant_msg})

    full_message = system_prompt + \
        "### Based on the requirements above, respond to the following query: " + message
    messages.append({"role": "user", "content": full_message})

    return messages

def llama_completion(messages: list[dict[str, str]]):
    llm_client = InferenceClient(
        "meta-llama/Meta-Llama-3-8B-Instruct", 
        token="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"
    )
    
    response = ""
    for mes in llm_client.chat_completion(
        messages,
        max_tokens=2048,
        stream=True,
        temperature=0.7,
        top_p=0.95,
    ):
        token = mes.choices[0].delta.content
        response += token
    return response 