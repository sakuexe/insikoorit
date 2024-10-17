
### pip install transformers datasets scikit-learn accelerate

from sklearn.metrics import accuracy_score, precision_recall_fscore_support
from datasets import load_dataset
from transformers import AutoTokenizer
from transformers import AutoModelForSequenceClassification
from transformers import TrainingArguments, Trainer
import numpy as np


# Load the IMDb dataset, which contains text reviews and their corresponding labels
dataset = load_dataset('imdb')

# Load a pre-trained BERT tokenizer
tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")

# Define a function to tokenize the text data
def tokenize_function(examples):
    # Tokenize the text with padding and truncation to a max length of 128 tokens
    return tokenizer(examples["text"], padding="max_length", truncation=True, max_length=128)

# Apply the tokenization function to the dataset using batch processing for speed
tokenized_datasets = dataset.map(tokenize_function, batched=True)

# Select a small subset of the training and testing data for faster training and evaluation
small_train_dataset = tokenized_datasets["train"].shuffle(seed=42).select(range(1000))
small_eval_dataset = tokenized_datasets["test"].shuffle(seed=42).select(range(1000))

# Load a pre-trained BERT model for sequence classification with 5 possible output labels
model = AutoModelForSequenceClassification.from_pretrained("bert-base-uncased", num_labels=5)

# Define training arguments, including output directory and batch sizes for training and evaluation
training_args = TrainingArguments(
    output_dir="./test_trainer",                # Directory to store training outputs
    num_train_epochs=1,                         # Number of training epochs
    per_device_train_batch_size=8,              # Batch size for training
    per_device_eval_batch_size=8,               # Batch size for evaluation
    evaluation_strategy="epoch",                # Perform evaluation after each epoch
    logging_dir='/logs',                        # Directory for logging training information
 )

# Initialize the Trainer with the model, training arguments, and datasets
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=small_train_dataset,
    eval_dataset=small_eval_dataset
)

trainer.train()


# Define a function to compute evaluation metrics (accuracy, precision, recall, and F1 score)
def compute_metrics(pred):
    labels = pred.label_ids
    preds = pred.predictions.argmax(-1)
    precision, recall, f1, _ = precision_recall_fscore_support(labels, preds, average='micro')
    acc = accuracy_score(labels, preds)
    return {'accuracy': acc, 'f1': f1, 'precision': precision, 'recall': recall}
# Set the compute_metrics function in the Trainer to evaluate the model
trainer.compute_metrics = compute_metrics

# Evaluate the model using the defined metrics
eval_result = trainer.evaluate()
print(eval_result)

# Save the fine-tuned model and tokenizer for later uses
trainer.save_model("finetune_model")
tokenizer.save_pretrained("finetune_model")