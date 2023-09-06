import database.user

translation = {
    'male': 'М', 'female': 'Ж'
}


def make_anketa(user_info):
    anketa = f'{user_info.username}'
    if user_info.gender:
        anketa += f', {translation[user_info.gender]}'
    if user_info.age:
        anketa += f'{user_info.age}'
    if user_info.bio:
        anketa += f'\n{user_info.bio}'
    return anketa


def translate_topic(topic):
    return topic