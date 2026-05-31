import json
import urllib.request
import urllib.error

for username, password in [('admin', 'admin123'), ('learner1', 'learner123')]:
    data = json.dumps({'username': username, 'password': password}).encode('utf-8')
    request = urllib.request.Request(
        'http://127.0.0.1:8002/api/auth/login/',
        data=data,
        headers={'Content-Type': 'application/json'}
    )
    try:
        with urllib.request.urlopen(request) as response:
            body = response.read().decode('utf-8')
            print(f'{username} OK {response.status}')
            print(body)
    except urllib.error.HTTPError as e:
        print(f'{username} FAIL {e.code}')
        print(e.read().decode('utf-8'))
    except Exception as e:
        print(f'{username} ERROR', e)
