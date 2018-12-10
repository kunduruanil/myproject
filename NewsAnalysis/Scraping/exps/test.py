from newspaper import Article

url="https://telanganatoday.com/krishnamurthy-subramanian-appointed-as-chief-economic-advisor"
article = Article(url, language='en')
article.download()
article.parse()
article.nlp()
print(article.publish_date)
print(article.top_image)

print(article.keywords)
print(article.summary)
