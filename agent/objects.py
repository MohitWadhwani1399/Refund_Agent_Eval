from pydantic import BaseModel,Field

class AgentResponse(BaseModel):
    """
    Represents the response from an agent.
    """
    answer: str = Field(description="The content of the agent's response for user question.")
    conversation:bool = Field(description="Indicates whether conversation should continue or not. If agent has made the decision about the refund this should be False, otherwise it should be True.",default=True)


class PurchaseItem(BaseModel):
    """
    Represents a purchase item.
    """
    name: str = Field(description="The name of the purchased item.")
