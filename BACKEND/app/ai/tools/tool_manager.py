from app.ai.tools.datetime_tool import DateTimeTool


class ToolManager:

    @classmethod
    def try_datetime(cls, message: str):
        return DateTimeTool.answer(message)

    @classmethod
    def use_tools(cls, message: str):
        datetime_result = cls.try_datetime(message)

        if datetime_result is not None:
            return datetime_result

        return None
