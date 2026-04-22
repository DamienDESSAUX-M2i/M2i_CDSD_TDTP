from transformers import pipeline

model_name = "papluca/xlm-roberta-base-language-detection"
detector = pipeline("text-classification", model=model_name)

text = "Un texte dans ma lanque natale."

result = detector(text)

print(type(result))
print(result)
