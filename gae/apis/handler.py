import endpoints
from protorpc import message_types
from protorpc import messages
from protorpc import remote


class Greeting(messages.Message):
    message = messages.StringField(1)


class GreetingCollection(messages.Message):
    """Collection of Greetings."""
    items = messages.MessageField(Greeting, 1, repeated=True)


STORED_GREETINGS = GreetingCollection(items=[
    Greeting(message='hello world!'),
    Greeting(message='goodbye world!'),
])


@endpoints.api(name='test', version='v1', base_path='/api/')
class TestAPI(remote.Service):

    @endpoints.method(message_types.VoidMessage, GreetingCollection,
                      path='get', http_method='GET', name='get')
    def list_greetings(self, unused_request):
        return STORED_GREETINGS
