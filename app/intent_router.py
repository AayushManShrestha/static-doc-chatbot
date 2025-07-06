# app/intent_router.py

def detect_intent(user_input: str) -> str | None:
    query = user_input.strip().lower()

    greetings = [
        "hello", "hi", "hey", 
        "who are you", 
        "tell me about yourself",
        "what is your job",
        "what do you do"
    ]

    farewells = [
        "bye", "goodbye", "see you", "talk to you later"
    ]

    # Check for greeting intent
    if any(phrase in query for phrase in greetings):
        return "I am a chatbot from Adex. Ask me anything about the company."

    # Check for farewell intent
    if any(phrase in query for phrase in farewells):
        return "Bye, have a good day!"

    return None  # no hardcoded intent matched