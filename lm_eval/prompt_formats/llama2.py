
class Format():
    """A class that manages prompt templates and keeps all conversation history"""

    b_inst: str = "[INST]"
    e_inst: str = "[/INST]"
    b_sys: str = "<<SYS>>\n"
    e_sys: str = "\n<</SYS>>\n\n"

    def get_prompt(self, messages) -> str:
        """Get the prompt for generation"""
        assert isinstance(messages, list), "The 'messages' parameter should be a list."

        prompt = "".join([
                f"<s>{self.b_inst} {(prompt['content']).strip()} {self.e_inst} {(answer['content']).strip()} </s>"
            for prompt, answer in zip(
                messages[::2],
                messages[1::2],
            )
        ])

        system_msg = None
        if messages[0]["role"] == "system":
            system_msg = messages[0]["content"]
            messages = messages[1:]

        assert len(messages) >= 1, "Need at least 1 messages"

        prompt = f"<s>{self.b_inst} "
        if system_msg:
            prompt += f"{self.b_sys} {system_msg} {self.e_sys}"

        first_message = messages.pop(0)
        prompt += f"{first_message['content']} {self.e_inst} "

        for msg in messages:
            if msg['role'] == "user":
                prompt += "<s>"

            prompt += f"{self.b_inst} {msg['content']} {self.e_inst}"
            if msg['role'] == "assistant":
                prompt += "</s>"

        return prompt

    def get_response(self, prompt: str) -> str:
        """Get the response from the model"""
        response = prompt.split(self.e_inst)[-1].replace(" </s>", "").strip()
        return response


if __name__ == "__main__":
    # Test the format class
    messages = [
        {"role": "system", "content": "This is a system prompt."},
        {"role": "user", "content": "This is user message no. 1."},
        {"role": "assistant", "content": "This is assistant message no. 1."},
        {"role": "user", "content": "This is user message no. 2."},
        {"role": "assistant", "content": "This is assistant message no. 2."},
    ]

    format = Format()
    prompt = format.get_prompt(messages)
    print("Prompt:")
    print(prompt)
    response = format.get_response(prompt)
    print("-------")
    print("Response:")
    print(response)
