import os
import json
from openai import OpenAI
from dotenv import load_dotenv

def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')

def ask_question(client, thread, assistant_id, question):
    try:
        # Добавляем вопрос в тред
        client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=question
        )

        # Запускаем ассистента
        run = client.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=assistant_id,
            stream=True
        )

        print("\n🤔 Thinking...", end="\r")

        first_chunk = True
        for chunk in run:
            if chunk.event == "thread.message.delta":
                if first_chunk:
                    print("\n📚 Answer: ", end="")
                    first_chunk = False

                delta = chunk.data.delta
                if delta and delta.content:
                    for content in delta.content:
                        if content.type == "text":
                            print(content.text.value, end="", flush=True)

        print("\n")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        return False

    return True

def load_assistant_info():
    try:
        with open("assistant_info.json", "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        print("❌ Could not load 'assistant_info.json'. Run 'bootstrap.py' first.")
        return None

def main():
    clear_screen()
    print("🎓 Study Assistant")
    print("Type 'exit' or 'quit' to end the session\n")

    load_dotenv()
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    info = load_assistant_info()
    if not info:
        return

    assistant_id = info["assistant_id"]
    


    thread = client.beta.threads.create()

    while True:
        try:
            question = input("\n❓ Your question: ").strip()
            if question.lower() in ['exit', 'quit', 'q']:
                print("\n👋 Goodbye! Have a great study session!")
                break

            if not question:
                print("Please enter a valid question!")
                continue

            success = ask_question(client, thread, assistant_id, question)
            if not success:
                retry = input("Would you like to try another question? (y/n): ").lower()
                if retry != 'y':
                    break

        except KeyboardInterrupt:
            print("\n\n👋 Goodbye! Have a great study session!")
            break
        except Exception as e:
            print(f"\n❌ An unexpected error occurred: {str(e)}")
            retry = input("Would you like to try again? (y/n): ").lower()
            if retry != 'y':
                break

if __name__ == "__main__":
    main()
