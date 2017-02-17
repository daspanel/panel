from flask import Blueprint, render_template
import requests
import json
from devourer import GenericAPI, APIMethod, APIError

bp = Blueprint('module1', __name__)

class TestApi(GenericAPI):
    users = APIMethod('get', '/api/?results={count}')

    def __init__(self, headers=None):
        params = {
            'url': 'https://randomuser.me',
            'auth': None,
            'load_json': True,
            'throw_on_error': True,
            'headers': headers
        }
        super(TestApi, self).__init__(**params)


@bp.route('/', methods=['GET'])
def home():
    """GET /: render homepage
    """
    myheaders={
        "pragma": "no-cache",
        "Accept": "application/json",
        "Authorization": "civmw76wg000001p2dwqxpvet",
    }

    api = TestApi(headers=myheaders)
    myusers = api.users(count=1)
    print myusers
    
    result = requests.get("https://randomuser.me/api/?results=5",
        headers={
            "pragma": "no-cache"
        },
        cookies={},
    )
    output = json.loads(result.content)
    #for rec in output['results']:
    #    print rec

    return render_template('/modules/module1/home.html', records=output['results'])



