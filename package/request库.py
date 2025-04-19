import requests

data = {"name":"germey","age":"25"}
# data = (('name','germey',('age','25')))
r = requests.get('https://www.httpbin.org/post', data=data)
print(r.text)


