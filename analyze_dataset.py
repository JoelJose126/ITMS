from datasets import load_dataset
import pandas as pd

print("Downloading Bitext dataset...")
dataset = load_dataset("Bitext/Bitext-customer-support-llm-chatbot-training-dataset")

# Convert to pandas for easier analysis
df = pd.DataFrame(dataset['train'])

print("\n--- Dataset Info ---")
print(df.info())

print("\n--- Sample Rows (First 10) ---")
print(df.head(10).to_string())

print("\n--- Unique Categories ---")
print(df['category'].unique())

print("\n--- Unique Intents ---")
print(df['intent'].unique())

# Save a sample to CSV for the user to see in the workspace
df.head(100).to_csv("bitext_sample_100.csv", index=False)
print("\nSaved first 100 rows to bitext_sample_100.csv")