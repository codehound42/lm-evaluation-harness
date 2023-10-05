
class Format():
    """A class that manages prompt templates and keeps all conversation history"""

    system: str = (
        "Below is an instruction that describes a task. Write a response that appropriately completes the request."
    )

    def get_prompt_instruct(self, messages) -> str:
        ret = f"""{self.system}

### Instruction
{messages[0].get("content")}

### Response
{messages[1].get("content")}"""

        return ret

    def get_prompt_chat(self, messages) -> str:
        conversation = "\n".join(
            [
                f"USER: {(user['content']).strip()}\nASSISTANT: {(assistant['content']).strip()}"
                for user, assistant in zip(
                    messages[::2],
                    messages[1:-1:2] + [{"content": ""}],
                )
            ]
        )

        ret = f"""{self.system}

### Instruction
{conversation}

### Response
{messages[-1].get("content")}"""

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
        response = "### Response\n".join(prompt.split("### Response\n")[1:]).strip()
        return response


if __name__ == "__main__":
    # Test the format class
    messages = [
        {"role": "system", "content": "This is a system prompt."},
        {"role": "user", "content": "This is a user message."},
        {"role": "assistant", "content": "{{gen}}"},
    ]
    format = Format()
    prompt = format.get_prompt(messages)
    print("Prompt:")
    print(prompt)
    print("------")
    response = format.get_response(prompt)
    print("Response:")
    print(response)
