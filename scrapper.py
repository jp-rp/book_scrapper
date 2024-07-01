import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core import output_parsers
from langchain_openai import ChatOpenAI

load_dotenv()
url = "https://books.toscrape.com/"
model = ChatOpenAI(model="gpt-4-turbo")
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a helpful business analyst. Use the following context in HTML format to answer user queries about books. Answer the questions to the best of your knowledge. HTML: {context} ",
        ),
        ("human", "{query}"),
    ]
)


def scrape_website(url):
    response = requests.get(url)

    if response.status_code == 200:
        doc = BeautifulSoup(response.content, "html.parser").prettify()
        return doc
    else:
        print(response.status_code)


chain = prompt | model | output_parsers.StrOutputParser()
document = scrape_website(url)

while True:
    query = input(">>")

    result = chain.invoke({"context": document, "query": query})
    print(result)
