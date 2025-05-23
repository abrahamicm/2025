from transformers import MarianMTModel, MarianTokenizer

src = "en"
tgt = "es"
model_name = f'Helsinki-NLP/opus-mt-{src}-{tgt}'

tokenizer = MarianTokenizer.from_pretrained(model_name)
model = MarianMTModel.from_pretrained(model_name)

texto = "This is a test"
tokens = tokenizer(texto, return_tensors="pt", padding=True)
translated = model.generate(**tokens)
print(tokenizer.decode(translated[0], skip_special_tokens=True))
