from transformers import pipeline

classifier = pipeline(
    "sentiment-analysis",
    model="distilbert-base-uncased-finetuned-sst-2-english",
)

texts = [
    "I love this tutorial!",
    "This is terrible",
    "Docker and Hugging Face work great together",
    "I'm not sure about this",
]

for text in texts:
    result = classifier(text)
    print(result)
