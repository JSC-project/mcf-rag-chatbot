from pydantic_ai import Agent


rag_agent = Agent(
    model = "google-gla:gemini-2.5-flash",
    retries = 1,
    system_prompt= ("You are an expert in civil defence. Always answerr based on knowledge from the lanceDb database. Do not make up any answers"
        "If you cant fin a good answer, it is better that your answer is, Sorry i don't know that"
        "It is very important that your asnwer is short and clear. Do not give out more information then is neccessary"
        "Always give a link to the source"
        ),
    
    output_type = RagResponse
)