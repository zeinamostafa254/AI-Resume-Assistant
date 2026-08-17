import os

from dotenv import load_dotenv

from langchain_openai import ChatOpenAI

from memory import (
    add_ai_message,
    add_user_message,
    get_history,
)

from prompts import PROMPT_TEMPLATE

from rag import get_retriever


load_dotenv()


class ResumeChatbot:

    def __init__(self):

        self.retriever = get_retriever()

        self.llm = ChatOpenAI(
            model=os.getenv("OPENAI_API_MODEL"
            ),
            base_url=os.getenv("OPENAI_API_BASE"
            ),
            api_key=os.getenv(
                "OPENROUTER_API_KEY"
            ),
            temperature=0.3,
        )

    def _format_history(self):

        history = get_history()

        if not history:
            return "No previous conversation."

        return "\n".join(
            f"{message.type}: {message.content}"
            for message in history
        )

    def _retrieve_context(
        self,
        question,
    ):

        documents = self.retriever.invoke(
            question
        )

        return "\n\n".join(
            document.page_content
            for document in documents
        )

    def ask(
        self,
        question,
    ):

        add_user_message(question)

        history = self._format_history()

        context = self._retrieve_context(
            question
        )

        prompt = PROMPT_TEMPLATE.invoke(
            {
                "history": history,
                "context": context,
                "question": question,
            }
        )

        response = self.llm.invoke(
            prompt
        )

        answer = response.content

        add_ai_message(answer)

        return answer