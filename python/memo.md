# Activate the environment

```
pyenv activate AAJA
pip install -r requirements.txt
```

then  run   

```
python main.py
```

to get schedule.json file.

requirements.txt is created by running

```
pip freeze > requirements.txt
``` 

if you use [Postman](https://web.postman.co/workspace/) to test, use OAuth2.0 and set Token, then Header prefix to `JWT `

Example Get call is `GET https://builder.guidebook.com/open-api/v1.1/sessions/?guide=215066`