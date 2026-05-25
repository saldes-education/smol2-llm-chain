from fastapi import FastAPI
from pydantic import BaseModel
from llm.llm import TicketInput, ticket_pipeline

app = FastAPI()

class LLMRequest(BaseModel):
    id: int
    message: str

@app.post("/llm")
def llm_route(body: LLMRequest):
    incoming_ticket = TicketInput(
        customer_id=body.id,
        message=body.message
    )
    return ticket_pipeline.invoke(incoming_ticket)