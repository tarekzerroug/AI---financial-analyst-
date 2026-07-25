from datasets import load_dataset


def to_chat(example):
    return {
        "messages": [
            {
                "role": "user",
                "content": example["instruction"] + "\n\n" + example["input"]
            },
            {
                "role": "assistant",
                "content": example["output"]
            }
        ]
    }


def load_training_dataset():
    dataset = load_dataset("FinGPT/fingpt-sentiment-train")

    dataset = dataset["train"].map(to_chat)

    return dataset