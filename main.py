from transformers import pipeline
from pprint import pprint
from pydantic import BaseModel, ConfigDict, SerializeAsAny
from typing import Any, Callable, Generic, TypeVar

I = TypeVar("I")
O = TypeVar("O")
M = TypeVar("M")

class Runnable(BaseModel, Generic[I, O]):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    
    name: str | None = None
    
    def invoke(self, data: I) -> O:
        raise NotImplementedError("Subclasses is not implemented")
    
    def __or__(self, other: Any) -> 'RunnableSequence':
        if isinstance(other, Runnable):
            return RunnableSequence.model_construct(
                first=self, 
                second=other,
            )
        if callable(other):
            return RunnableSequence.model_construct(
                first=self,
                second=RunnableLambda.model_construct(func=other, name=other.__name__),
                name=other.__name__,
            )
        return NotImplemented
    
    def __ror__(self, other: Any) -> Any:
        if callable(other):
            return RunnableSequence.model_construct(
                first=RunnableLambda.model_construct(func=other),
                second=self,
                name=other.__name__,
            )
        return NotImplemented
    
class RunnableLambda(Runnable[I, O]):
    func: Callable[[I], O]
    
    def invoke(self, data: I) -> O:
        return self.func(data)
    
class RunnableSequence(Runnable[I, O], Generic[I, M, O]):
    first: SerializeAsAny[Runnable[I, M]]
    second: SerializeAsAny[Runnable[M, O]]
    
    def invoke(self, data: I) -> O:
        return self.second.invoke(self.first.invoke(data))

# Strongly typed input data
class TicketInput(BaseModel):
    customer_id: int
    message: str

# Strongly typed output data
class ProcessedTicket(BaseModel):
    customer_id: int
    sentiment: str
    urgency: str
    summary: str

class SentimentAnalyser(Runnable[TicketInput, dict]):
    name: str = "sentiment_analyser"
    model_version: str = "2.1-stable"
    
    def invoke(self, ticket: TicketInput) -> dict:
        msg_lower = ticket.message.lower()
        
        # Simulated NLP sentiment
        sentiment = "negative" if "broken" in msg_lower or "angry" in msg_lower else "neutral"
        urgency = "high" if "broken" in msg_lower or "urgent" in msg_lower else "low"
        
        return {
            "customer_id": ticket.customer_id,
            "sentiment": sentiment,
            "urgency": urgency,
            "summary": ticket.message[:40] + "..."
        }

class TicketParser(Runnable[dict, ProcessedTicket]):
    name: str = "ticket_parser"
    
    def invoke(self, raw_dict: dict) -> ProcessedTicket:
        return ProcessedTicket(**raw_dict)

def route_ticket(ticket: ProcessedTicket) -> dict:
    destination = "engineering_team" if "high" in ticket.urgency else "general_support"
    return {
        "status": "routed",
        "assigned_to": destination,
        "ticket_details": ticket.model_dump()
    }

ticket_pipeline = SentimentAnalyser() | TicketParser() | route_ticket

incoming_ticket = TicketInput(
    customer_id=1337,
    message="The payment portal is broken! Urgent fix is needed ASAP!"
)

final_output = ticket_pipeline.invoke(incoming_ticket)

print("--- PIPELINE EXECUTION RESULT ---")
pprint(final_output)

print("--- INSIGHT: THE PYDANTIC SCHEMA OF THE PIPELINE ---")
pprint(ticket_pipeline.model_dump(exclude_none=True))

