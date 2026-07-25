from transformers import AutoTokenizer
from transformers import AutoModelForCausalLM

from dataset import load_training_dataset
from config import MODEL_NAME

dataset = load_training_dataset()

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME
)

print(dataset[0])