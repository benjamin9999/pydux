import unittest
import pydux

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

if __name__ == '__main__':
    unittest.main()
