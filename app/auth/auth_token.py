import http.client
import json


def create_auth_header_with_permissions(
    domain,
    client_id,
    client_secret,
    api_audience
):
    conn = http.client.HTTPSConnection(domain)
    payload = f'{{"client_id":"{client_id}",\
"client_secret":"{client_secret}",\
"audience":"{api_audience}","grant_type":"client_credentials"}}'
    headers = {'content-type': "application/json"}
    conn.request("POST", "/oauth/token", payload, headers)
    res = conn.getresponse()
    data = res.read()
    token = json.loads(data.decode('utf-8'))['access_token']
    return {'authorization': f'Bearer {token}'}
