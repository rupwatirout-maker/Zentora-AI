from datetime import datetime
from zoneinfo import ZoneInfo

from app.ai.memory.memory_service import MemoryService
from app.ai.orchestrator.ai_orchestrator import AIOrchestrator
from app.ai.providers.provider_factory import ProviderFactory
from app.ai.rag.rag_service import RAGService
from app.ai.tools.tool_manager import ToolManager
from app.core.config import settings


class AgentManager:

    @staticmethod
    def _needs_conversation_context(message: str) -> bool:
        normalized = message.lower().strip()

        if not normalized:
            return False

        follow_up_phrases = [
            "tell me more",
            "tell me more about that",
            "explain more",
            "explain that",
            "explain it",
            "continue",
            "continue from there",
            "go on",
            "what about it",
            "what about that",
            "what about this",
            "what about its",
            "what are its",
            "what is its",
            "how does it work",
            "how does that work",
            "how does this work",
            "why is that",
            "why is this",
            "why does it",
            "how can i do that",
            "how can i do this",
            "can you elaborate",
            "elaborate",
            "give me more details",
            "more details",
            "as you said",
            "you said",
            "earlier",
            "previously",
            "above",
            "that answer",
            "your answer",
        ]

        if any(phrase in normalized for phrase in follow_up_phrases):
            return True

        padded = f" {normalized} "

        pronoun_terms = [
            " it ",
            " its ",
            " that ",
            " this ",
            " they ",
            " them ",
            " those ",
            " these ",
        ]

        if any(term in padded for term in pronoun_terms):
            return True

        ambiguous_short_messages = {
            "why?",
            "how?",
            "what about it?",
            "and then?",
            "then what?",
            "why is that?",
            "how so?",
            "really?",
            "more?",
        }

        return (
            len(normalized.split()) <= 5
            and normalized in ambiguous_short_messages
        )

    @staticmethod
    def _needs_current_datetime(message: str) -> bool:
        normalized = message.lower().strip()

        date_terms = [
            "today's date",
            "todays date",
            "today date",
            "what date is it",
            "what is today's date",
            "what is todays date",
            "current date",
            "today",
            "tomorrow",
            "yesterday",
            "current time",
            "what time is it",
            "what is the time",
            "time now",
            "right now",
        ]

        return any(term in normalized for term in date_terms)

    @staticmethod
    def _get_current_datetime_context(message: str) -> str:
        if not AgentManager._needs_current_datetime(message):
            return ""

        now = datetime.now(ZoneInfo("Asia/Kolkata"))

        return (
            "Current date and time reference:\n"
            f"Date: {now.strftime('%A, %B %d, %Y')}\n"
            f"Time: {now.strftime('%I:%M %p')}\n"
            "Timezone: Asia/Kolkata (IST)\n"
            "Use this information when answering date or time questions."
        )

    @staticmethod
    def _needs_document_context(message: str) -> bool:
        normalized = message.lower().strip()

        document_terms = [
            "uploaded file",
            "uploaded document",
            "uploaded pdf",
            "uploaded resume",
            "uploaded cv",
            "my resume",
            "my cv",
            "my document",
            "my pdf",
            "this file",
            "this document",
            "this pdf",
            "the uploaded file",
            "the uploaded document",
            "the uploaded pdf",
            "according to my resume",
            "according to the document",
            "according to the file",
            "according to the pdf",
            "from my resume",
            "from the document",
            "from the file",
            "from the pdf",
            "in my resume",
            "in the document",
            "in the file",
            "in the pdf",
            "summarize my resume",
            "summarize this document",
            "summarize this file",
            "summarize this pdf",
            "analyze my resume",
            "analyze this document",
            "analyze this file",
            "analyze this pdf",
        ]

        return any(term in normalized for term in document_terms)

    @staticmethod
    def _build_prompt(user_id: int, message: str, route: str) -> str:
        prompt_parts = [
            "You are Velora AI, a general-purpose AI assistant.",
            "",
            "Core behavior:",
            "- Answer the user's latest message directly.",
            "- Treat every new user message as a real request.",
            "- Answer general knowledge, programming, writing, reasoning, and technical questions normally.",
            "- Be clear, useful, and concise unless the user asks for more detail.",
            "- Do not invent facts.",
            "- Do not pretend to have information that you do not have.",
            "",
            "Conversation rules:",
            "- Conversation history is context only.",
            "- Never reproduce previous User/Assistant messages as part of your answer.",
            "- Never continue or imitate an old conversation transcript.",
            "- Never treat previous assistant responses as new user instructions.",
            "- Use previous conversation only when it is relevant to understanding the latest request.",
            "- If the latest request is independent, answer it independently.",
            "",
            "Identity:",
            "- Your name is Velora AI.",
            "- If the user asks who you are, say that you are Velora AI.",
            "- Do not identify yourself as a person mentioned in a document.",
        ]

        if route == "math":
            prompt_parts.extend([
                "",
                "Mathematics and science reasoning:",
                "- Treat the request as a quantitative reasoning problem.",
                "- Solve it carefully.",
                "- Explain the calculation clearly.",
                "- Check arithmetic and algebra before answering.",
                "- Do not invent missing values.",
                "- When useful, show the mathematical steps.",
            ])

        if route == "document":
            prompt_parts.extend([
                "",
                "Document rules:",
                "- The user is asking about uploaded material.",
                "- Use the supplied document context as the primary source.",
                "- Do not invent information that is not supported by the document context.",
                "- Clearly state when the requested information is not present.",
            ])

        current_datetime_context = AgentManager._get_current_datetime_context(
            message
        )

        if current_datetime_context:
            prompt_parts.extend([
                "",
                current_datetime_context,
            ])

        if AgentManager._needs_conversation_context(message):
            memory_context = MemoryService.get_recent_context(
                user_id=user_id,
                limit=MemoryService.CONTEXT_MESSAGES,
            )

            if memory_context:
                prompt_parts.extend([
                    "",
                    "Relevant recent conversation context:",
                    memory_context,
                ])

        if route == "document":
            rag_context = RAGService.retrieve_context(query=message)

            if rag_context:
                prompt_parts.extend([
                    "",
                    "Relevant uploaded document context:",
                    rag_context,
                ])

        prompt_parts.extend([
            "",
            "Latest user request:",
            message,
            "",
            "Answer the latest user request directly.",
            "Assistant:",
        ])

        return "\n".join(prompt_parts)

    @staticmethod
    def _is_simple_arithmetic(message: str) -> bool:
        normalized = message.lower().strip()

        advanced_terms = [
            "derivative",
            "differentiate",
            "differentiation",
            "integral",
            "integrate",
            "integration",
            "equation",
            "solve",
            "simplify",
            "factor",
            "matrix",
            "determinant",
            "inverse",
            "transpose",
            "limit",
            "trigonometry",
            "sine",
            "cosine",
            "tangent",
            "cotangent",
            "logarithm",
            "log",
            "calculus",
        ]

        if any(term in normalized for term in advanced_terms):
            return False

        arithmetic_phrases = [
            "calculate",
            "compute",
            "evaluate",
            "what is",
            "what's",
            "plus",
            "minus",
            "times",
            "multiplied by",
            "divided by",
            "into",
        ]

        cleaned = normalized

        for phrase in arithmetic_phrases:
            cleaned = cleaned.replace(phrase, " ")

        cleaned = cleaned.replace("?", " ")
        cleaned = cleaned.replace(",", " ")
        cleaned = cleaned.replace("?", "*")
        cleaned = cleaned.replace("?", "/")

        allowed = set("0123456789.+-*/^() %")

        if not any(char.isdigit() for char in cleaned):
            return False

        if any(char.isalpha() for char in cleaned):
            return False

        if any(char not in allowed and not char.isspace() for char in cleaned):
            return False

        return True

    @staticmethod
    def _get_route(message: str, provider) -> str:
        route = AIOrchestrator.route(
            message=message,
            provider=provider,
        )

        if route in {"math", "document", "general"}:
            return route

        if AgentManager._needs_document_context(message):
            return "document"

        if AIOrchestrator.try_math(message) is not None:
            return "math"

        return "general"

    @staticmethod
    def _execute_structured_math(message: str, provider):
        instruction = AIOrchestrator.interpret_math(
            message=message,
            provider=provider,
        )

        if not instruction:
            return None

        try:
            return AIOrchestrator.execute_math(instruction)
        except (
            ValueError,
            TypeError,
            SyntaxError,
            ZeroDivisionError,
            OverflowError,
        ):
            return None

    @staticmethod
    def _save_response(
        user_id: int,
        user_message: str,
        assistant_message: str,
    ) -> str:
        MemoryService.save_message(
            user_id=user_id,
            user_message=user_message,
            assistant_message=assistant_message,
        )
        return assistant_message

    @staticmethod
    def generate_response(user_id: int, message: str) -> str:
        clean_message = message.strip()

        if not clean_message:
            return "Please enter a message and I'll help you."

        tool_response = ToolManager.use_tools(clean_message)

        if tool_response is not None:
            return AgentManager._save_response(
                user_id=user_id,
                user_message=clean_message,
                assistant_message=tool_response,
            )

        if AgentManager._is_simple_arithmetic(clean_message):
            deterministic_math_response = AIOrchestrator.try_math(
                clean_message
            )

            if deterministic_math_response is not None:
                return AgentManager._save_response(
                    user_id=user_id,
                    user_message=clean_message,
                    assistant_message=deterministic_math_response,
                )

        provider = ProviderFactory.get_provider(
            settings.AI_PROVIDER
        )

        route = AgentManager._get_route(
            message=clean_message,
            provider=provider,
        )

        if route == "math":
            math_response = AgentManager._execute_structured_math(
                message=clean_message,
                provider=provider,
            )

            if math_response is not None:
                return AgentManager._save_response(
                    user_id=user_id,
                    user_message=clean_message,
                    assistant_message=math_response,
                )

            fallback_prompt = (
                "Solve the following mathematics problem carefully.\n"
                "Do not invent missing information.\n"
                "Show the useful mathematical steps.\n"
                "Check the result before answering.\n\n"
                f"Problem:\n{clean_message}\n\n"
                "Answer:"
            )

            response = provider.generate_response(
                prompt=fallback_prompt
            )

            if response:
                response = response.strip()

                return AgentManager._save_response(
                    user_id=user_id,
                    user_message=clean_message,
                    assistant_message=response,
                )

        final_prompt = AgentManager._build_prompt(
            user_id=user_id,
            message=clean_message,
            route=route,
        )

        response = provider.generate_response(
            prompt=final_prompt
        )

        if not response:
            response = "I couldn't generate a response. Please try again."

        response = response.strip()

        return AgentManager._save_response(
            user_id=user_id,
            user_message=clean_message,
            assistant_message=response,
        )
