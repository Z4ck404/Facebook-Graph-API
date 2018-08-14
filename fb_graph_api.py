import facebook #for fb graph api call 
import sys #for handling exceptions 
import requests #for api calls
import re #for regular expressions
#check the feedback of a comment
token =" token here "
#extracting the price from the text using regex
def extract_price(text):
	pattern = re.compile(r'\d{3,6}\s*([Dd][Hh][Ss])?')
	matches = pattern.search(text)
	return matches.group(0)
#checking the sentiment of the text / comment and class weither negative or positive or neutral
def feedback(text):
    list = ("text",)
    list =list +(text,)
    data = [list,]
    response = requests.post('http://text-processing.com/api/sentiment/', data=data)
    return response.json().get("label")
    '''
    if (response.json().get("label")=="pos"):
        return "positive"
    elif(response.json().get("label")=="neg"):
        return "negative"
    else:
        return "neutral"
	'''
#check all the posts for the messages : 'text joint' in them 
def page_posts_messages(id_page):
	ls=[]
	for x in page_feed(id_page,token):
		id_post = x["id"]
		ls.append(post_text(x["message"]))
	return ls
'''
#extract all th comments from all the post of the page :
def page_posts_comments(id_page,token):
	ls=[]
	for x in page_feed(id_page,token):
		id_post = x["id"]
		if (post_comments(x["message"])):
			ls.append(post_comments(x["message"]))
	return ls
'''
#extract the feed of a fb page :
def page_feed(id_page):
	graph = facebook.GraphAPI(access_token=token, version="2.7")
	posts = graph.get_object(id=id_page, fields='feed')
	return posts["feed"]["data"]
#extract the text in a post :
def post_text(id_post):
	id=str(id_post)
	graph = facebook.GraphAPI(access_token=token, version="2.7")
	post = graph.get_object(id=id_post, fields='name')
	if (post):
		return post["name"]
	else:
		return id
#extract comments from a post :
def post_comments(id):
	id_post = str(id)
	graph = facebook.GraphAPI(access_token=token, version="2.7")
	post = graph.get_object(id=id_post, fields='comments')
	try:
		return post["comments"]["data"]
	except:
		print (sys.exc_info())
def treat_post(id):
	#dict(apple="green", banana="yellow", cherry="red")
	id_here = str(id)
	pos=0 #score de comments positifs
	neg=0 #score de coments negatifs
	neu=0 #score de comments neutres
	text = post_text(id_here)
	price = extract_price(text)
	
	for x in post_comments(id_here):
		if (x["message"]):
			if (feedback(x["message"]) == 'pos'):
				pos = pos +1
			elif(feedback(x["message"]) == 'neg'):
				neg = neg + 1 
			else :
				neu = neu + 1 
	return dict(text = id_here,price_extracted = price ,positivity=pos,negativity=neg,neutrality=neu)

	
