import sys
from mistral_common.tokens.tokenizers.mistral import MistralTokenizer
from mistral_common.protocol.instruct.messages import UserMessage
from mistral_common.protocol.instruct.request import ChatCompletionRequest

# Load the Mistral v3 tokenizer
tokenizer = MistralTokenizer.v3(is_tekken=True)

def count_tokens_in_file(file_path):
    # Read the content of the file
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()

    # Create a ChatCompletionRequest with a UserMessage
    request = ChatCompletionRequest(messages=[UserMessage(content=text)])

    # Tokenize the request
    tokenized = tokenizer.encode_chat_completion(request)
    
    # Get the number of tokens
    token_count = len(tokenized.tokens)
    
    return token_count

if __name__ == "__main__":
    # Check if a filename was provided as an argument
    if len(sys.argv) != 2:
        print("Usage: python script.py <input_file_path>")
        sys.exit(1)

    file_path = sys.argv[1]
    
    try:
        # Count tokens and print the result
        token_count = count_tokens_in_file(file_path)
        print(f'The number of tokens in "{file_path}" is: {token_count}')
    except FileNotFoundError:
        print(f'Error: The file "{file_path}" was not found. Please check the filename and try again.')

