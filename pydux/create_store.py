"""
python + redux == pydux

Redux: http://redux.js.org

A somewhat literal translation of Redux.

Closures in Python are over references, as opposed to
names in JavaScript, so they are read-only.  Single-
element arrays are used to create read/write closures.

"""


class ActionTypes(object):
    INIT = '@@redux/INIT'


class Store(object):
    def __init__(self, reducer, initial_state, enhancer):
        if enhancer is not None:
            if not hasattr(enhancer, '__call__'):
                raise TypeError('Expected the enhancer to be a function.')
            return enhancer(create_store)(reducer)

        if not hasattr(reducer, '__call__'):
            raise TypeError('Expected the reducer to be a function.')

        self.reducer = reducer
        self.initial_state = initial_state
        self.enhancer = enhancer
        # single-element arrays for r/w closure
        self.current_reducer = [reducer]
        self.current_state = [initial_state]
        self.current_listeners = [[]]
        self.next_listeners = [self.current_listeners[0]]
        self.is_dispatching = [False]
        self.dispatch({'type': ActionTypes.INIT})

    def ensure_can_mutate_next_listeners(self):
        if self.next_listeners[0] == self.current_listeners[0]:
            self.next_listeners[0] = self.current_listeners[0][:]

    def get_state(self):
        return self.current_state[0]

    def subscribe(self, listener):
        if not hasattr(listener, '__call__'):
            raise TypeError('Expected listener to be a function.')

        self.is_subscribed = [True]  # r/w closure

        self.ensure_can_mutate_next_listeners()
        self.next_listeners[0].append(listener)

        def unsubcribe():
            if not self.is_subscribed[0]:
                return
            self.is_subscribed[0] = False

            self.ensure_can_mutate_next_listeners()
            index = next_listeners[0].index(listener)
            self.next_listeners[0].pop(index)

        return unsubcribe

    def dispatch(self, action):
        if not isinstance(action, dict):
            raise TypeError('Actions must be a dict. '
                            'Use custom middleware for async actions.')

        if 'type' not in action:
            raise ValueError('Actions must have a "type" property. '
                             'Have you misspelled a constant?')

        if self.is_dispatching[0]:
            raise Exception('Reducers may not dispatch actions.')

        try:
            self.is_dispatching[0] = True
            self.current_state[0] = self.current_reducer[0](self.current_state[0], action)
        finally:
            self.is_dispatching[0] = False

        self.listeners = self.current_listeners[0] = self.next_listeners[0]
        for listener in self.listeners:
            listener()

        return action

    def replace_reducer(self, next_reducer):
        if not hasattr(next_reducer, '__call__'):
            raise TypeError('Expected the next_reducer to be a function')

        self.current_reducer[0] = next_reducer
        self.dispatch({'type': ActionTypes.INIT})


def create_store(reducer, initial_state=None, enhancer=None):
    """
    redux in a nutshell.

    observable has been omitted.

    Args:
        reducer: root reducer function for the state tree
        initial_state: optional initial state data
        enhancer: optional enhancer function for middleware etc.

    Returns:
        a Pydux store
    """
    return Store(reducer, initial_state, enhancer)
