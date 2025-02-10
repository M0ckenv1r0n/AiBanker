from openai import OpenAI


class ChatGPTHandler:
    def __init__(self, api_key: str, system_prompt: str) -> None:
        self.client = OpenAI(api_key=api_key)
        self.conversation_context = [
            {"role": "system", "content": system_prompt}]

    def add_to_context(self, role: str, content: str) -> None:
        self.conversation_context.append({"role": role, "content": content})

    def send_request(self, user_message: str, model: str = "gpt-4o-mini", temperature: float = 1.0) -> str:
        # Add the user message to the conversation context
        self.add_to_context("user", user_message)

        response = self.client.chat.completions.create(
            model=model,
            messages=self.conversation_context,
            temperature=temperature

        )

        assistant_message = response.choices[0].message.content

        self.add_to_context("assistant", assistant_message)

        return assistant_message.replace("\n", "")