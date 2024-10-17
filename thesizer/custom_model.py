# Load saved model and tokenizer
from transformers import AutoModelForSequenceClassification, AutoTokenizer, TextClassificationPipeline

# Load the fine-tuned model and tokenizer
new_model = AutoModelForSequenceClassification.from_pretrained('finetune_model')
new_tokenizer = AutoTokenizer.from_pretrained('finetune_model')

# Create a classification pipeline
classifier = TextClassificationPipeline(model=new_model, tokenizer=new_tokenizer)

# Add label mapping for sentiment analysis (assuming LABEL_0 = 'negative' and LABEL_1 = 'positive')
label_mapping = {0: 'negative', 1: 'positive'}

# Test the model
result = classifier("This movie was excellent.")

# Map the result to more meaningful labels
mapped_result = {'label': label_mapping[int(result[0]['label'].split('_')[1])], 'score': result[0]['score']}
print(mapped_result)