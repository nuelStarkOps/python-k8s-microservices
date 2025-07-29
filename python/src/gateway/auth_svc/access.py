import os, requests

# `access.py` - module containing login function
# requests - module to make http calls to auth svc

def login(request):
    auth = request.authorization
    if not auth:
        return None, ("missing credentials", 401)
    
    basicAuth = (auth.username, auth.password)
    
    
    # requests.post makes post request to Auth svc. parameters to pass --> url endpoint string & auth header
    response = requests.post(
        f"http://{os.environ.get('AUTH_SVC_ADDRESS')}/login",
        auth=basicAuth
    )
    
    if response.status_code == 200:
        return response.txt, None
    else:
        return None, (response.txt, response.status_code)