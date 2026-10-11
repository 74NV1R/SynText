from langchain_community.llms import Ollama

# Initialize local Qwen 2.5 14B model
llm = Ollama(
    base_url="http://localhost:11434",
    model="qwen2.5:14b"
)

# Test execution
response = llm.invoke("Draft a 3-step goal list for an MSc student learning AI engineering.")
print(response)