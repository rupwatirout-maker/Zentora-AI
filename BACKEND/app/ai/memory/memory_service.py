from collections import defaultdict


class MemoryService:
    _memory = defaultdict(list)
    MAX_MESSAGES = 10
    CONTEXT_MESSAGES = 6

    @classmethod
    def save_message(cls, user_id, user_message, assistant_message):
        cls._memory[user_id].append(
            {
                "user": user_message,
                "assistant": assistant_message,
            }
        )

        if len(cls._memory[user_id]) > cls.MAX_MESSAGES:
            cls._memory[user_id] = cls._memory[user_id][-cls.MAX_MESSAGES:]

    @classmethod
    def get_context(cls, user_id):
        history = cls._memory.get(user_id, [])

        if not history:
            return ""

        context = []

        for message in history:
            context.append(f"User: {message['user']}")
            context.append(f"Assistant: {message['assistant']}")

        return "\n".join(context)

    @classmethod
    def get_recent_context(cls, user_id, limit=None):
        history = cls._memory.get(user_id, [])

        if not history:
            return ""

        limit = limit or cls.CONTEXT_MESSAGES
        recent_history = history[-limit:]

        context = []

        for message in recent_history:
            context.append(f"User: {message['user']}")
            context.append(f"Assistant: {message['assistant']}")

        return "\n".join(context)

    @classmethod
    def clear_memory(cls, user_id):
        cls._memory.pop(user_id, None)

    @classmethod
    def has_memory(cls, user_id):
        return bool(cls._memory.get(user_id))
