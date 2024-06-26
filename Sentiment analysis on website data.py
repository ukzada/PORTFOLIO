

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
plt.style.use('ggplot')
import nltk

df = pd.read_csv("/content/drive/MyDrive/Reviews.csv")

df.head()

example = df [ 'Text'][50]
print (example)

nltk.download('punkt')
nltk.word_tokenize (example)

tokens=nltk.word_tokenize(example)
nltk.download('averaged_perceptron_tagger')
tagged = nltk.pos_tag(tokens)
tagged [:10]

nltk.download('maxent_ne_chunker')
nltk.download('words')
entities = nltk. chunk.ne_chunk (tagged)
entities.pprint()

from nltk. sentiment import SentimentIntensityAnalyzer
from tqdm.notebook import tqdm
nltk.download('vader_lexicon')
sia =SentimentIntensityAnalyzer ()

sia.polarity_scores('I am so happy!')

sia.polarity_scores('This is the worst thing ever.')

sia.polarity_scores (example)

# Run the polarity score on the entire dataset
res = {}
for i, row in tqdm(df.iterrows(), total=len (df)):
    text = row['Text']
    myid = row['Id' ]
    res[myid] =sia.polarity_scores (text)

vaders = pd.DataFrame (res). T
vaders = vaders.reset_index().rename (columns={'index': 'Id'})
vaders = vaders.merge(df, how='left')

# Now we have sentiment score and metadata
vaders.head()

from bs4 import BeautifulSoup
import requests


def get_reviews_from_website(url):
    # Function to fetch reviews from a website
    # (You may need to customize this based on the structure of the website)
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    reviews = [review.text for review in soup.find_all('div', class_='description')]
    return reviews

def analyze_sentiment(review):
    # Function to analyze sentiment using SentimentIntensityAnalyzer
    sentiment_scores = sia.polarity_scores(review)
    return sentiment_scores

def main():
    # Website URL
    website_url = 'https://zevarhouse.com/product/starring-fashion-gold-coated-tops'

    # Fetch reviews from the website
    reviews = get_reviews_from_website(website_url)

    # Analyze sentiment for each review
    for i, review in enumerate(reviews, start=1):
        sentiment_scores = analyze_sentiment(review)
        print(f"Review: {review}")
        print(f" Sentiment Scores from SIA: {sentiment_scores}")
        print("\n" + "=" * 50 + "\n")

if __name__ == "__main__":
    main()

fig, axs = plt.subplots(1, 3, figsize=(12, 3))
sns.barplot (data=vaders, x='Score' , y='pos', ax=axs[0])
sns.barplot (data=vaders, x='Score', y='neu', ax=axs[1])
sns.barplot (data=vaders, x='Score', y='neg', ax=axs[2])
axs[0].set_title('Positive')
axs[1].set_title('Neutral')
axs[2].set_title('Negative')
plt.show()

from transformers import AutoTokenizer
from transformers import AutoModelForSequenceClassification
from scipy.special import softmax

MODEL = f"cardiffnlp/twitter-roberta-base-sentiment"
tokenizer = AutoTokenizer.from_pretrained (MODEL)
model = AutoModelForSequenceClassification.from_pretrained (MODEL)

# Run for Roberta Model
encoded_text = tokenizer(example, return_tensors='pt')
output = model(**encoded_text)
scores = output[0][0].detach().numpy()
scores = softmax(scores)
scores_dict = {
    'roberta_neg': scores[0],
    'roberta_neu': scores[1],
    'roberta_pos': scores[2]
}


print(scores_dict)

def polarity_scores_roberta (example):
    encoded_text= tokenizer (example, return_tensors='pt')
    output = model (**encoded_text)
    scores = output[0][0].detach().numpy()
    scores = softmax (scores)
    scores_dict = {
    'roberta_neg': scores[0],
    'roberta_neu': scores[1],
    'roberta_pos': scores[2]
}
    return scores_dict

res = {}
for i, row in tqdm (df.iterrows(), total=len (df)):
    try:
        text = row[ 'Text']
        myid = row['Id' ]
        vader_result = sia.polarity_scores (text)
        vader_result_rename = {}
        for key, value in vader_result.items():
            vader_result_rename [f"vader_{key}"] = value
        roberta_result = polarity_scores_roberta(text)
        both = {**vader_result_rename, **roberta_result}
        res[myid] = both
    except RuntimeError:
        print (f'Broke for id {myid}')

from transformers import pipeline

sent_pipeline = pipeline("sentiment-analysis")

sent_pipeline('While the jewelry design is fifty fifty, the durability of some pieces leaves room for improvement')

from bs4 import BeautifulSoup
import requests
from transformers import pipeline

# Replace 'your_website_url' with the actual URL of the product page
url = 'https://zevarhouse.com/product/24k-gold-coated-pair-of-gorgeous-karas/#reviews'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# Replace 'div' and 'your-class-name' with the actual tag and class name
reviews = soup.find_all('div', class_='description')
print(reviews)
# Process the extracted reviews as needed
for review in reviews:
    text_to_analyze = review.text

    # Perform sentiment analysis using transformers pipeline
    sentiment_pipeline = pipeline('sentiment-analysis')
    sentiment_result = sentiment_pipeline(text_to_analyze)[0]

    print(f"Review: {text_to_analyze}")
    print(f"Sentiment from roberta: {sentiment_result['label']} ({sentiment_result['score']:.2f})")
    print("\n" + "=" * 50 + "\n")  # Separation line for better readability

















