import endpoints
from handler import TestAPI


APPLICATION = endpoints.api_server([
    TestAPI,

])
