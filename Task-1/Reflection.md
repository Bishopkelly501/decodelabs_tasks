# Reflection

## Decode Labs Prompt Engineering Project 1

### Objective

The objective of this project was to design a prompt that extracts structured information from unstructured customer text and returns the result as valid JSON.

### My Approach

I started by creating a system prompt that clearly defined the AI's role as an information extraction assistant. I added strict instructions to ensure that the AI returns only valid JSON, avoids extra explanations, and uses `null` for missing values.

To improve consistency, I used triple-quote (`"""`) delimiters to separate the instructions from the customer input. I also included three few-shot examples to demonstrate the expected input and output format. This helps the AI understand the required extraction pattern and produce more reliable results.

### Challenges

One challenge was understanding how to design prompts that consistently produce structured JSON without additional conversational text. I also learned the importance of delimiters, deterministic prompting, and few-shot prompting in improving the quality and reliability of AI-generated outputs.

### What I Learned

From this project, I learned:
- How to write a structured system prompt.
- The difference between zero-shot and few-shot prompting.
- How delimiters improve prompt clarity.
- Why JSON is important for AI automation and APIs.
- Why deterministic outputs are essential for reliable AI systems.

### Conclusion

This project improved my understanding of prompt engineering and showed me how carefully designed prompts can transform unstructured text into structured, machine-readable data suitable for AI and automation workflows.