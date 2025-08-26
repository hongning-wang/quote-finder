## Quote Lookup
Ever notice that people are much more receptive to the words of the greats of history than your voice? This project uses Gemini AI and FAISS to rephrase natural language input as a compelling quote from a historical figure.

Currently, this is built as an API for personal use. POST requests add quotes while GET requests query for quotes.


### Installation and Use
```shell
#Clone the repository
git clone https://github.com/hongning-wang/quote-finder.git
#Install dependencies
pip install -r requirements.txt
#Create database
python manage.py makemigrations api
python manage.py migrate api
```
Obtain a Gemini API id from Google. Then
```shell
#Add the API id as an environment secret
echo 'GEMINI_API_ID=[id]' > .env 
#Read quotes and create embeddings.
python manage.py fetch_quotes
python manage.py embed_quotes
#Start the server
python manage.py runserver
```

### Possible Next Steps
Create frontend component. Use Gemini API to rerank top k choices based on similarity to natural language input.