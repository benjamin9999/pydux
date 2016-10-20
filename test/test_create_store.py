from __future__ import absolute_import
import unittest
from mock import MagicMock
import pydux
from .helpers import *


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
            {'id': 1, 'text': 'Hello'}
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

    def test_applies_reducer_initial(self):
        '''applies the reducer to the initial state'''
        store = pydux.create_store(reducer_todos, [
            {
                'id': 1,
                'text': 'Hello'
            }
        ])
        self.assertEqual(store.get_state(), [
            {
                'id': 1,
                'text': 'Hello'
            }
        ])

        store.dispatch(unknown_action())
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

    def test_preserves_state_replacing(self):
        '''preserves the state when replacing a reducer'''
        store = pydux.create_store(reducer_todos)
        store.dispatch(add_todo('Hello'))
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

        store.replace_reducer(reducer_todos_reverse)
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

        store.dispatch(add_todo('Perhaps'))
        self.assertEqual(store.get_state(), [
            {
                'id': 3,
                'text': 'Perhaps'
            },
            {
                'id': 1,
                'text': 'Hello'
            },
            {
                'id': 2,
                'text': 'World'
            }
        ])

        store.replace_reducer(reducer_todos)
        self.assertEqual(store.get_state(), [
            {
                'id': 3,
                'text': 'Perhaps'
            },
            {
                'id': 1,
                'text': 'Hello'
            },
            {
                'id': 2,
                'text': 'World'
            }
        ])

        store.dispatch(add_todo('Surely'))
        self.assertEqual(store.get_state(), [
            {
                'id': 3,
                'text': 'Perhaps'
            },
            {
                'id': 1,
                'text': 'Hello'
            },
            {
                'id': 2,
                'text': 'World'
            },
            {
                'id': 4,
                'text': 'Surely'
            }
        ])

    def test_supports_multiple_subscriptions(self):
        '''supports multiple subscriptions'''
        store = pydux.create_store(reducer_todos)
        listenerA = MagicMock()
        listenerB = MagicMock()

        unsubscribeA = store.subscribe(listenerA)
        store.dispatch(unknown_action())
        self.assertEqual(listenerA.call_count, 1)
        self.assertEqual(listenerB.call_count, 0)

        store.dispatch(unknown_action())
        self.assertEqual(listenerA.call_count, 2)
        self.assertEqual(listenerB.call_count, 0)

        unsubscribeB = store.subscribe(listenerB)
        self.assertEqual(listenerA.call_count, 2)
        self.assertEqual(listenerB.call_count, 0)

        store.dispatch(unknown_action())
        self.assertEqual(listenerA.call_count, 3)
        self.assertEqual(listenerB.call_count, 1)

        unsubscribeA()
        self.assertEqual(listenerA.call_count, 3)
        self.assertEqual(listenerB.call_count, 1)

        store.dispatch(unknown_action())
        self.assertEqual(listenerA.call_count, 3)
        self.assertEqual(listenerB.call_count, 2)

        unsubscribeB()
        self.assertEqual(listenerA.call_count, 3)
        self.assertEqual(listenerB.call_count, 2)

        store.dispatch(unknown_action())
        self.assertEqual(listenerA.call_count, 3)
        self.assertEqual(listenerB.call_count, 2)

        unsubscribeA = store.subscribe(listenerA)
        self.assertEqual(listenerA.call_count, 3)
        self.assertEqual(listenerB.call_count, 2)

        store.dispatch(unknown_action())
        self.assertEqual(listenerA.call_count, 4)
        self.assertEqual(listenerB.call_count, 2)
