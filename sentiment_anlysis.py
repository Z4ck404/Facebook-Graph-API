import requests
def feedback(text):
    list = ("text",)
    list =list +(text,)
    data = [list,]
    response = requests.post('http://text-processing.com/api/sentiment/', data=data)
    if (response.json().get("label")=="pos"):
        return "positive"
    elif(response.json().get("label")=="neg"):
        return "negative"
    else:
        return "neutral"
