from hello.models import Profile

def setUpUsers(use):
    for u in use:
        user = Profile(username = u["email"], email=u["email"],first_Name=u["f_name"], last_Name=u["l_name"],
                      password=u["password"])
        user.save()

def createUsers():
    return[
            {
                "email" : "hello@outlook.com",
                "f_name" : "tim",
                "l_name" : "jones",
                "password" : "ftlrdgd9797"
            },
            {
                "email" : "tang@outlook.com",
                "f_name" : "tang",
                "l_name" : "josh",
                "password" : "timetime123"
            },
            {
                "email" : "chang@outlook.com",
                "f_name" : "chang",
                "l_name" : "thomas",
                "password" : "firefire123"
            },
    ]