import os
import json
import asyncio
import random
from dotenv import load_dotenv
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import TextMessage
from autogen_agentchat.teams import RoundRobinGroupChat
import difflib
from autogen_ext.models.openai import OpenAIChatCompletionClient

# Load API key
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError('Please set the OPENAI_API_KEY environment variable.')

model_client = OpenAIChatCompletionClient(model='gpt-4o', api_key=api_key)

# Load knowledge base
with open("knowledge_base.json", "r") as f:
    knowledge_base = json.load(f)

# Function to find an answer from the knowledge base
import difflib

def find_answer(query):
    query_lower = query.lower()

    # Combine all categories
    all_questions = []
    mapping = {}

    for category in knowledge_base:
        for item in knowledge_base[category]:
            question = item["question"].lower()
            all_questions.append(question)
            mapping[question] = item["answer"]

    # Find closest match using difflib
    closest_match = difflib.get_close_matches(query_lower, all_questions, n=1, cutoff=0.6)

    if closest_match:
        return mapping[closest_match[0]]
    
    return None


# Add friendly follow-up
follow_ups = [
    "Is there anything else I can help you with?",
    "Feel free to ask if you have more questions!",
    "I'm here if you need further assistance!",
    "Let me know if you have any other questions!",
    "Happy to help with anything else you need!",
    "If you have more queries, just ask!",
    "Don't hesitate to reach out for further help!",
    "Is there any other information you need?",
    "I'm available for any other questions you might have!",
    "Please ask if something else comes up!",
    "Let me know if you need more details!",
    "Always here to assist you with any questions!",
    "Can I help you with anything else today?",
    "Feel free to reach out for more support!",
    "If you need further clarification, just ask!"
]


def format_response(answer):
    return f"{answer} {random.choice(follow_ups)}"

# Define agents
return_agent = AssistantAgent(
    name='ReturnAgent',
    model_client=model_client,
    system_message="You are the Return Agent. Only handle return-related questions based on the knowledge base."
)

orders_agent = AssistantAgent(
    name='OrdersAgent',
    model_client=model_client,
    system_message="You are the Orders Agent. Only handle order-related questions based on the knowledge base."
)

payment_agent = AssistantAgent(
    name='PaymentAgent',
    model_client=model_client,
    system_message="You are the Payment Agent. Only handle payment-related questions based on the knowledge base."
)

team = RoundRobinGroupChat(
    participants=[return_agent, orders_agent, payment_agent],
    max_turns=3
)

async def main():
    print("Welcome to Customer Support!")
    print("Type your query below (or type 'exit' to quit):")

    while True:
        user_question = input("\nYou: ")
        if user_question.lower().strip() == "exit":
            print("Goodbye!")
            break

        # Find answer in knowledge base
        matched_answer = find_answer(user_question)

        if matched_answer:
            final_response = format_response(matched_answer)
            print(f"\nAgent: {final_response}")
        else:
            print("\nAgent: Sorry, I couldn't find an answer in the knowledge base.")

if __name__ == "__main__":
    asyncio.run(main())
