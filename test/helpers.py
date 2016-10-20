def id(state=[]):
    def f(result, item):
        if item['id'] > result:
            return item['id']
        else:
            return result
    return reduce(f, state, 0) + 1

def reducer_todos(state, action):
    if state is None:
        state = []
    if action['type'] == 'ADD_TODO':
        copy = state[:]
        copy.append({'id': id(state), 'text': action['text']})
        return copy
    return state

def reducer_todos_reverse(state, action):
    if state is None:
        state = []
    if action['type'] == 'ADD_TODO':
        copy = state[:]
        copy.insert(0, ({'id': id(state), 'text': action['text']}))
        return copy
    return state

def unknown_action():
    return {'type': 'UNKNOWN_ACTION'}

def add_todo(text):
    return {'type': 'ADD_TODO', 'text': text}
