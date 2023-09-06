from aiogram.types import InlineKeyboardButton

class Topics:
    topics = {
        'art': 'Исскуство',
        'sport': 'Спорт',
        'politics': 'Политика',
        'humor': 'Юмор',
        'science': 'Наука',
        'religion': 'Религия'

    }

    def get_topic_counts(self) -> dict[str, int]:
        return {key: 0 for key in self.topics.keys()}


    def get_buttons(self, topic_counts: dict | None = None) -> list[InlineKeyboardButton]:
        buttons = []
        if not topic_counts:
            for key in self.topics.keys():
                buttons.append(InlineKeyboardButton(self.topics[key], callback_data=key))
            return buttons
        else:
            ...