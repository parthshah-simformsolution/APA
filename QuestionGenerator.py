from pprint import pprint
from QGen import *

# Create an instance of the QuestionGenerator class
qe=QuestionGenerator()

# Example text
text = "Albert Einstein was born in Ulm, Germany, on March 14, 1879. He developed the theory of relativity."

# Generate questions from the text
questions = qe.predict_shortq(text)

# Print the generated questions
for i, question in enumerate(questions, start=1):
    print(f"Question {i}: {question}")
