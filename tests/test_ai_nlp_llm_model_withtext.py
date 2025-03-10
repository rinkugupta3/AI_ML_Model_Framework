import spacy
import google.generativeai as genai

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# Configure Gemini API
genai.configure(api_key="AIzaSyC-jC_ZGabKz5IH-GXP9L7k8JXrH8lLcd4")
model = genai.GenerativeModel('gemini-1.5-pro')

# Sample Text
text = "What are the Apple Inc. sales reported in 3rd quarter.  " \
       "Provide complete detail sales of each apple product in 3rd quarter."

# NLP (spaCy)
doc = nlp(text)
entities = [(ent.text, ent.label_) for ent in doc.ents]
print("Extracted Entities:", entities) # -->  [('Apple Inc.', 'ORG'), ('the 3rd quarter', 'iPhone 16')]

# LLM (Gemini) - Ask a question based on the entities
prompt = f"Based on the text: '{text}' and the extracted entities: {entities}, summarize the earnings report focusing on key figures. "
response = model.generate_content(prompt)
print("\nLLM Summary:")
print(response.text)