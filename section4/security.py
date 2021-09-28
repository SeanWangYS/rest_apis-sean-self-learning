from werkzeug.security import safe_str_cmp
from user import User

users = [
    User(1, 'bob', 'asdf'), 
    User(1, 'Rolf', 'asdf')
]

username_mapping = {u.username: u for u in users}
userid_mapping = {u.id: u for u in users}

def authenticate(username, password):   # used it to log in users 
    user = username_mapping.get(username, None)
    if user and safe_str_cmp(user.password, password):  # 建議比較字串時，使用 safe_str_cmp(), 可確保跨系統跨python版本間的運作
        return user

def identity(payload):  # use it to idenfity when client send a new request. payload is the token which client sent
    user_id =  payload['identity']
    return userid_mapping.get(user_id, None)

