import io
path = 'login_response.txt'
with open(path, 'rb') as f:
    data = f.read()
try:
    print(data.decode('utf-8'))
except UnicodeDecodeError:
    print(data.decode('utf-16', errors='replace'))
