from models import model
from prompts import SYSTEM_PROMPT

from tools import get_user_order_history, calculate_right_refund_amount
from tools import issue_refund_ticket, check_today_date
from objects import AgentResponse
from langchain.agents import create_agent
from langchain.messages import HumanMessage, SystemMessage
from langgraph.checkpoint.memory import InMemorySaver
from dotenv import load_dotenv
from uuid import uuid4

load_dotenv()

agent = create_agent(
    model=model,
    system_prompt=SystemMessage(content=SYSTEM_PROMPT),
    tools=[get_user_order_history, calculate_right_refund_amount, issue_refund_ticket, check_today_date],
    response_format=AgentResponse,
    checkpointer=InMemorySaver()
)

def run_conversation():
    config = {"configurable" : {"thread_id": str(uuid4())}}

    question = HumanMessage(content="I have a request for a refund")
    conversation = True
    while conversation:
        response = agent.invoke({"messages": [question]},config=config)
        structured_response = response["structured_response"]
        print(structured_response.answer)
        conversation = structured_response.conversation

        if conversation:
            user_input = input("reply: \n")
            question = HumanMessage(content=user_input)

    print(f"Conversation is over !")

run_conversation()
        