import ollama

def main():
    """
    Main function to run the AI model test.
    """
    print("--- Testing AI Engine Connection ---")

    try:
        prompt = "In one short sentence, explain the importance of preserving endangered languages."
        print(f"Sending prompt: '{prompt}'")

        response = ollama.chat(
            model='llama3:8b',
            messages=[
                {'role': 'user', 'content': prompt},
            ]
        )

        ai_message = response['message']['content']

        print("\n--- AI Response ---")
        print(ai_message)
        print("--------------------")
        print("Success! The AI engine is working correctly.")

    except Exception as e:
        print("\n--- ERROR ---")
        print(f"An error occurred: {e}")
        print("Please ensure the Ollama application is running and you have pulled the 'llama3:8b' model.")

if __name__ == '__main__':
    main()