from datetime import datetime, timedelta
from zoneinfo import ZoneInfo


class DateTimeTool:
    TIMEZONE = "Asia/Kolkata"

    @classmethod
    def now(cls):
        return datetime.now(ZoneInfo(cls.TIMEZONE))

    @classmethod
    def get_date(cls):
        current = cls.now()
        return current.strftime("%A, %B %d, %Y")

    @classmethod
    def get_time(cls):
        current = cls.now()
        return current.strftime("%I:%M %p")

    @classmethod
    def get_tomorrow(cls):
        tomorrow = cls.now() + timedelta(days=1)
        return tomorrow.strftime("%A, %B %d, %Y")

    @classmethod
    def get_yesterday(cls):
        yesterday = cls.now() - timedelta(days=1)
        return yesterday.strftime("%A, %B %d, %Y")

    @classmethod
    def answer(cls, message: str):
        text = message.lower().strip()

        if "tomorrow" in text:
            return f"Tomorrow is {cls.get_tomorrow()}."

        if "yesterday" in text:
            return f"Yesterday was {cls.get_yesterday()}."

        if (
            "time" in text
            or "what time" in text
            or "time now" in text
        ):
            return (
                f"The current time is {cls.get_time()} "
                f"on {cls.get_date()} (IST)."
            )

        if (
            "date" in text
            or "today" in text
            or "what day" in text
        ):
            return f"Today is {cls.get_date()} (IST)."

        return None
