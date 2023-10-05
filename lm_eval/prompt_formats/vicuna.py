
class Format():
    """A class that manages prompt templates and keeps all conversation history"""

    system: str = "A chat between a curious user and an artificial intelligence assistant. The assistant gives helpful, detailed, and polite answers to the user's questions."

    def get_prompt_instruct(self, messages) -> str:
        return self.get_prompt_chat(messages)

    def get_prompt_chat(self, messages) -> str:
        conversation_parts = []

        for i in range(0, len(messages) - 1, 2):
            user_msg = f"USER: {messages[i]['content'].strip()}"
            assistant_msg = f"ASSISTANT: {messages[i + 1]['content'].strip()}</s>"
            conversation_parts.append(f"{user_msg} {assistant_msg}")

        conversation = " ".join(conversation_parts)
        ret = f"{self.system} {conversation}"
        return ret

    def get_prompt(self, messages) -> str:
        """Get the prompt for generation"""
        assert isinstance(messages, list), "The 'messages' parameter should be a list."
        assert len(messages) >= 2, "Need at least 2 messages"

        if messages and messages[0].get("role") == "system":
            self.system = messages[0].get("content")
            messages.pop(0)

        assert len(messages) % 2 == 0, "Need an even number of messages"
        assert all([msg["role"] == "user" for msg in messages[::2]]) and all(
            [msg["role"] == "assistant" for msg in messages[1::2]]
        ), (
            "model only supports 'system', 'user' and 'assistant' roles, "
            "starting with 'system', then 'user' and alternating (u/a/u/a/u...)"
        )

        if len(messages) == 2:
            return self.get_prompt_instruct(messages)
        else:
            return self.get_prompt_chat(messages)

    def get_response(self, prompt: str) -> str:
        """Get the response from the model"""
        response = prompt.split("ASSISTANT: ")[-1].replace("</s>", "").strip()
        return response


if __name__ == "__main__":
    messages = [
        {
            "role": "system",
            "content": "A chat between a curious user and an artificial intelligence assistant. The assistant gives helpful, detailed, and polite answers to the user's questions.",
        },
        {"role": "user", "content": "Hi"},
        {"role": "assistant", "content": "Hello."},
        {"role": "user", "content": "Who are you?"},
        {"role": "assistant", "content": "I am Abzuito."},
    ]
    format = Format()
    prompt = format.get_prompt(messages)
    print("Prompt:")
    print(prompt)
    response = format.get_response(prompt)
    print("-------")
    print("Response:")
    print(response)
