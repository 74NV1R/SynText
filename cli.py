from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
from src.agent import syntext_app

def main():
    print("==================================================")
    print("   Syntext AI — Local Language Tutor (Qwen 14B)   ")
    print("==================================================")
    
    session_id = input("Enter session/thread ID (default: 'default_user'): ").strip() or "default_user"
    target_lang = input("Enter target language (default: 'German'): ").strip() or "German"
    
    config = {"configurable": {"thread_id": session_id}}
    
    print(f"\nSession started for {target_lang}. Type 'exit' or 'quit' to end.\n")
    
    while True:
        try:
            user_input = input("\nYou: ").strip()
            if not user_input:
                continue
            if user_input.lower() in ["exit", "quit"]:
                print("Ending session. Keep practicing!")
                break
                
            initial_state = {
                "messages": [HumanMessage(content=user_input)],
                "target_language": target_lang
            }
            
            # Stream or invoke state updates
            output = syntext_app.invoke(initial_state, config=config)
            
            # Find the final text response from the assistant
            for msg in reversed(output["messages"]):
                if isinstance(msg, AIMessage) and msg.content:
                    print(f"\nSyntext AI: {msg.content}")
                    break
            
        except KeyboardInterrupt:
            print("\nSession interrupted. Exiting...")
            break

if __name__ == "__main__":
    main()