from bardapi import Bard

token = ''
bard = Bard(token=token)
query = """
Answer in yes or no. Check if the following statement is factually correct. Check years, names, locations, historical events, numbers, or any other named entity. "1. In 1987, Russian military lieutenant Stanislav Petrov prevented a nuclear war between the United States and Russia by not retaliating against a false alarm of American missile attacks." ?
"""
answer = bard.get_answer(query)['content']
print (answer)
