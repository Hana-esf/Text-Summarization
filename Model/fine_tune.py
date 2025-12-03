import pandas as pd
import numpy as np
from transformers import BartTokenizer, BartForConditionalGeneration, Trainer, TrainingArguments
from datasets import Dataset, DatasetDict
import torch
import logging
import os
from sklearn.model_selection import train_test_split
from tqdm import tqdm
from rich.console import Console
from rich.logging import RichHandler

# Configure logging
console = Console()
file_handler = logging.FileHandler('training.log')
file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
rich_handler = RichHandler(console=console, show_time=False, show_level=True, show_path=False)

logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(file_handler)
logger.addHandler(rich_handler)

# Check for GPU availability
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
logger.info("Using device: %s", device)

# Define paths
model_save_path = './results/model'
last_checkpoint = './results/checkpoint'

# Training arguments
training_args = TrainingArguments(
    output_dir='./results',          # output directory
    evaluation_strategy="epoch",     # evaluation strategy to use
    learning_rate=2e-5,              # learning rate
    per_device_train_batch_size=4,  # batch size for training
    per_device_eval_batch_size=4,   # batch size for evaluation
    num_train_epochs=3,             # number of training epochs
    weight_decay=0.01,              # strength of weight decay
    logging_dir='./logs',           # directory for storing logs
    logging_steps=10,
    save_steps=500,                 # save checkpoint every 500 steps
    save_total_limit=3,             # limit the total number of checkpoints
    report_to="none",               # Avoid logging to external platforms
)

def load_or_train_model():
    resume_from_checkpoint = None
    if os.path.isdir(last_checkpoint):
        resume_from_checkpoint = last_checkpoint
        logger.info("Resuming training from checkpoint: %s", last_checkpoint)

    if os.path.isdir(model_save_path):
        # Load the model
        logger.info("Loading pre-trained model...")
        model = BartForConditionalGeneration.from_pretrained(model_save_path).to(device)
        tokenizer = BartTokenizer.from_pretrained(model_save_path)
        logger.info("Model loaded successfully.")
    else:
        # Train and save the model
        logger.info("Model not found. Training model...")
        
        # Load dataset from JSON
        try:
            data = pd.read_json('formatted_dataset.json')
            logger.info("Dataset loaded from 'formatted_dataset.json'.")
        except Exception as e:
            logger.error("Error loading dataset: %s", e)
            raise

        # Split into training and validation datasets
        train_df, val_df = train_test_split(data, test_size=0.1, random_state=42)
        logger.info("Data split into training and validation sets.")

        # Convert to Hugging Face Dataset
        train_dataset = Dataset.from_pandas(train_df)
        val_dataset = Dataset.from_pandas(val_df)
        datasets = DatasetDict({
            'train': train_dataset,
            'validation': val_dataset
        })
        logger.info("Dataset converted to Hugging Face Dataset format.")

        # Initialize tokenizer and model
        tokenizer = BartTokenizer.from_pretrained('facebook/bart-large')
        model = BartForConditionalGeneration.from_pretrained('facebook/bart-large').to(device)
        logger.info("Tokenizer and model initialized and moved to device.")

        def preprocess_function(examples):
            # Tokenize the inputs and targets
            inputs = tokenizer(examples['Body'], max_length=1024, truncation=True, padding='max_length')
            targets = tokenizer(examples['Abstract'], max_length=150, truncation=True, padding='max_length')
            
            # Create a dictionary with encoded inputs and targets
            model_inputs = inputs
            model_inputs['labels'] = targets['input_ids']
            
            return model_inputs

        # Optimize the tokenization process by using multiprocessing
        logger.info("Tokenizing the dataset with optimized map function...")
        encoded_datasets = datasets.map(preprocess_function, batched=True, num_proc=os.cpu_count())
        logger.info("Dataset tokenized.")

        # Define the Trainer
        trainer = Trainer(
            model=model,                         # the instantiated Transformers model to be trained
            args=training_args,                  # training arguments, defined above
            train_dataset=encoded_datasets['train'],         # training dataset
            eval_dataset=encoded_datasets['validation'],     # evaluation dataset
        )
        logger.info("Trainer instantiated.")

        # Train the model with progress bar
        logger.info("Starting model training...")
        try:
            # Wrap the training process with a tqdm progress bar
            trainer.train(resume_from_checkpoint=resume_from_checkpoint)
            logger.info("Model training complete.")
        except Exception as e:
            logger.error("Error during training: %s", e)
            raise

        # Save the model
        logger.info("Saving the model...")
        model.save_pretrained(model_save_path)
        tokenizer.save_pretrained(model_save_path)
        logger.info("Model saved successfully.")

    return model, tokenizer

# Load or train the model
model, tokenizer = load_or_train_model()

# Generate summaries for some example texts
def generate_summary(text):
    inputs = tokenizer(text, return_tensors="pt", max_length=1024, truncation=True)
    inputs = {key: value.to(device) for key, value in inputs.items()}  # Move inputs to GPU if available
    summary_ids = model.generate(inputs["input_ids"], max_length=150, num_beams=4, length_penalty=2.0, early_stopping=True)
    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    return summary

# Test the summarization
sample_text = "Your long article or body text goes here."
logger.info("Generating summary for sample text...")
print(generate_summary(sample_text))
