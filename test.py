import unittest
import pydux

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

def unknown_action():
    return {'type': 'UNKNOWN_ACTION'}

def add_todo(text):
    return {'type': 'ADD_TODO', 'text': text}

class TestCreateStore(unittest.TestCase):
    def test_exposes_public_api(self):
        '''exposes the public API'''
        store = pydux.create_store(lambda state,action: state)
        methods = dir(store)

        self.assertTrue('subscribe' in methods)
        self.assertTrue('dispatch' in methods)
        self.assertTrue('get_state' in methods)
        self.assertTrue('replace_reducer' in methods)

    def test_throws_reducer(self):
        '''throws if reducer is not a function'''
        self.assertRaises(TypeError, pydux.create_store)
        self.assertRaises(TypeError, pydux.create_store, 'test')
        self.assertRaises(TypeError, pydux.create_store, {})

    def test_passes_initial(self):
        '''passes the initial action and the initial state'''
        store = pydux.create_store(reducer_todos, [
            { 'id': 1, 'text': 'Hello' }
        ])
        self.assertEqual(store.get_state(), [
            {'id': 1, 'text': 'Hello'}
        ])

    def test_applies_reducer(self):
        '''applies the reducer to the previous state'''
        store = pydux.create_store(reducer_todos)
        self.assertEqual(store.get_state(), [])

        store.dispatch(unknown_action())
        self.assertEqual(store.get_state(), [])

        store.dispatch(add_todo('Hello'))
        self.assertEqual(store.get_state(), [
            {
                'id': 1,
                'text': 'Hello'
            }
        ])

        store.dispatch(add_todo('World'))
        self.assertEqual(store.get_state(), [
            {
                'id': 1,
                'text': 'Hello'
            },
            {
                'id': 2,
                'text': 'World'
            }
        ])





if __name__ == '__main__':
    unittest.main()
