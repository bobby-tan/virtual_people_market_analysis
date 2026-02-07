import json
from agentfield import AgentRouter
from pydantic import BaseModel, Field

# Group related reasoners with a router
reasoners_router = AgentRouter(prefix="demo", tags=["example"])

@reasoners_router.reasoner()
async def echo(message: str) -> dict:
    print('echo')
    """
    Simple echo reasoner - works without AI configured.

    Example usage:
    curl -X POST http://localhost:8080/api/v1/execute/my-agent.demo_echo \
      -H "Content-Type: application/json" \
      -d '{"input": {"message": "Hello World"}}'
    """
    return {
        "original": message,
        "echoed": message,
        "length": len(message)
    }
    
class ResearchResults(BaseModel):
    """Structured output for sentiment analysis."""
    summary: str = Field(description="Summary of the market research result from every persona")

class PriceAndProductDescription(BaseModel):
    """Structured output for sentiment analysis."""
    product_description: str = Field(description="Product description based on user input")
    price: float = Field(ge=0.0, description="Price of item based on user input") 

@reasoners_router.reasoner()
async def entrypoint(message: str) -> dict:
    """
    Simple echo reasoner - works without AI configured.

    Example usage:
    curl -X POST http://localhost:8080/api/v1/execute/my-agent.demo_echo \
      -H "Content-Type: application/json" \
      -d '{"input": {"message": "Hello World"}}'
    """
    print('entry 1')
    result = await reasoners_router.ai(
        system="You are a language parser.",
        user=f"Given this message: {message}. Extract price and product description information",
        schema=PriceAndProductDescription
    )
    
    print('entry 2')
    r1 = await agent_1_sentiment(result.product_description, result.price)
    r1_dict = json.loads(r1)
    print('entry 3')

    # Add a note for observabilitys
    reasoners_router.app.note(
        f"Analyzed sentiment: {r1_dict.reasoning} (confidence: {r1_dict.probability})",
        tags=["reasoning", "probability"]
    )
    print('entry 4')
    
    r2 = await agent_2_sentiment(result.product_description, result.price)
    r2_dict = json.loads(r2)



    # Add a note for observabilitys
    reasoners_router.app.note(
        f"Analyzed sentiment: {r2_dict.reasoning} (confidence: {r2_dict.probability})",
        tags=["reasoning", "probability"]
    )
    
    r3 = await agent_3_sentiment(result.product_description, result.price)
    r3_dict = json.loads(r3)

    # Add a note for observabilitys
    reasoners_router.app.note(
        f"Analyzed sentiment: {r3_dict.reasoning} (confidence: {r3_dict.probability})",
        tags=["reasoning", "probability"]
    )
    
    r4 = await agent_4_sentiment(result.product_description, result.price)
    r4_dict = json.loads(r4)

    print('entry 10')


    # Add a note for observabilitys
    reasoners_router.app.note(
        f"Analyzed sentiment: {r4_dict.reasoning} (confidence: {r4_dict.probability})",
        tags=["reasoning", "probability"]
    )
    
    r5 = await agent_5_sentiment(result.product_description, result.price)
    r5_dict = json.loads(r5)

    # Add a note for observabilitys
    reasoners_router.app.note(
        f"Analyzed sentiment: {r5_dict.reasoning} (confidence: {r5_dict.probability})",
        tags=["reasoning", "probability"]
    )
    print('entry 15')
    
    
    ressearch_results = await reasoners_router.ai(
        system="You are a professional market research presenter. We will be giving you information from 5 groups of participants with each data point having probability of purchase and reasoning. Present the results in a professional manner. ",
        user=f"Given this results from participants: {r1}, {r2}, {r3}, {r4}, {r5}. Consolidate this to nice summary of research result. Provide recommendation.",
        schema=ResearchResults
    )
    
    print('entry 4')
    

    return ressearch_results.model_dump()

# 🔧 Uncomment when AI is configured in main.py:
# class PurchaseResults(BaseModel):
#     """Structured output for sentiment analysis."""
#     probability: float = Field(ge=0.0, le=1.0, description="Probablility of persona buying this item")
#     reasoning: str = Field(description="Explanation of why this is the case")


# 🔧 Uncomment when AI is configured in main.py:
class PurchaseResults(BaseModel):
    """Structured output for sentiment analysis."""
    probability: float = Field(ge=0.0, le=1.0, description="Probablility of persona buying this item")
    reasoning: str = Field(description="Explanation of why this is the case")
  

@reasoners_router.reasoner()
async def agent_1_sentiment(product_description: str, price: float) -> dict:
    """
    AI-powered sentiment analysis with structured output.

    Example usage:
    curl -X POST http://localhost:8080/api/v1/execute/my-agent.demo_analyze_sentiment \
      -H "Content-Type: application/json" \
      -d '{"input": {"text": "I love this product!"}}'
    """
    # Access AI directly through the router's app instance
    print('analyze_sentiment')
    result = await reasoners_router.ai(
        system="You are a 22-year-old male living in a fast-paced urban center like Los Angeles or New York. You are browsing a local pop-up market and come across a limited-edition, tech-integrated backpack. It’s stylish and fits your 'modern nomad' aesthetic, but it costs $85. You are checking your banking app and thinking about the 'Purchase Level'—is this a 'High' value investment for your daily commute, or should you stick to your current gear? Walk us through your decision to buy or walk away.",
        user=f"Tell me the probability of you buying this item: {product_description}, given the price is {price}. Also, remember to provide reasons for your decision.",
        schema=PurchaseResults
    )

    # Add a note for observability
    reasoners_router.app.note(
        f"Analyzed sentiment: {result.reasoning} (confidence: {result.probability})",
        tags=["sentiment", "analysis"]
    )

    return result.model_dump()
  
  
@reasoners_router.reasoner()
async def agent_2_sentiment(product_description: str, price: float) -> dict:
    """
    AI-powered sentiment analysis with structured output.

    Example usage:
    curl -X POST http://localhost:8080/api/v1/execute/my-agent.demo_analyze_sentiment \
      -H "Content-Type: application/json" \
      -d '{"input": {"text": "I love this product!"}}'
    """
    # Access AI directly through the router's app instance
    result = await reasoners_router.ai(
        system="ou are a 26-year-old female exploring a weekend artisan fair in a trendy neighborhood. You find a set of hand-poured, sustainable soy candles with unique botanical scents. They are priced at $25 each ('Low' to 'Medium' purchase level). You’re thinking about your home office vibe and whether these support a small business you’d want to post about. What factors—brand story, scent, or price—ultimately convince you to make the purchase?",
        user=f"Tell me the probability of you buying this item: {product_description}, given the price is {price}. Also, remember to provide reasons for your decision.",
        schema=PurchaseResults
    )

    # Add a note for observability
    reasoners_router.app.note(
        f"Analyzed sentiment: {result.reasoning} (confidence: {result.probability})",
        tags=["sentiment", "analysis"]
    )

    return result.model_dump()
  
@reasoners_router.reasoner()
async def agent_3_sentiment(product_description: str, price: float) -> dict:
    """
    AI-powered sentiment analysis with structured output.

    Example usage:
    curl -X POST http://localhost:8080/api/v1/execute/my-agent.demo_analyze_sentiment \
      -H "Content-Type: application/json" \
      -d '{"input": {"text": "I love this product!"}}'
    """
    # Access AI directly through the router's app instance
    print('analyze_sentiment')
    result = await reasoners_router.ai(
        system="You are a 45-year-old male homeowner living in a suburban area like Illinois or Ohio. At a home and garden expo, you see a high-end, ergonomic power tool set. It's a 'High' purchase level item at $95. You already have tools, but these promise better efficiency for your weekend projects. You’re weighing the 'Review Rating' in your head and considering if the long-term utility justifies the immediate cost. Describe your logic.",
        user=f"Tell me the probability of you buying this item: {product_description}, given the price is {price}. Also, remember to provide reasons for your decision.",
        schema=PurchaseResults
    )

    # Add a note for observability
    reasoners_router.app.note(
        f"Analyzed sentiment: {result.reasoning} (confidence: {result.probability})",
        tags=["sentiment", "analysis"]
    )

    return result.model_dump()
  
  
@reasoners_router.reasoner()
async def agent_4_sentiment(product_description: str, price: float) -> dict:
    """
    AI-powered sentiment analysis with structured output.

    Example usage:
    curl -X POST http://localhost:8080/api/v1/execute/my-agent.demo_analyze_sentiment \
      -H "Content-Type: application/json" \
      -d '{"input": {"text": "I love this product!"}}'
    """
    # Access AI directly through the router's app instance
    print('analyze_sentiment')
    result = await reasoners_router.ai(
        system="You are a 48-year-old female living on the East Coast, shopping at a high-end seasonal boutique. You encounter a premium, locally-sourced wool cardigan. It’s a 'High' purchase level item. You value durability and classic style over fast fashion. You are checking the fabric quality and thinking about how many 'Previous Purchases' you've made of this brand. Does the 'Discount Applied' (or lack thereof) change your mind?",
        user=f"Tell me the probability of you buying this item: {product_description}, given the price is {price}. Also, remember to provide reasons for your decision.",
        schema=PurchaseResults
    )

    # Add a note for observability
    reasoners_router.app.note(
        f"Analyzed sentiment: {result.reasoning} (confidence: {result.probability})",
        tags=["sentiment", "analysis"]
    )

    return result.model_dump()
  
@reasoners_router.reasoner()
async def agent_5_sentiment(product_description: str, price: float) -> dict:
    """
    AI-powered sentiment analysis with structured output.

    Example usage:
    curl -X POST http://localhost:8080/api/v1/execute/my-agent.demo_analyze_sentiment \
      -H "Content-Type: application/json" \
      -d '{"input": {"text": "I love this product!"}}'
    """
    # Access AI directly through the router's app instance
    print('analyze_sentiment')
    result = await reasoners_router.ai(
        system="You are a 65-year-old retiree enjoying a morning at a regional farmers' and crafts market. You see a beautifully crafted wooden rocking chair or a piece of local art. You aren't looking for 'trends' anymore; you want comfort, reliability, and perhaps something to pass down. You're looking at the 'Review Rating' (word-of-mouth from the vendor) and deciding if this 'High' purchase level item is a worthy treat for your home. What determines your 'Yes'?",
        user=f"Tell me the probability of you buying this item: {product_description}, given the price is {price}. Also, remember to provide reasons for your decision.",
        schema=PurchaseResults
    )

    # Add a note for observability
    reasoners_router.app.note(
        f"Analyzed sentiment: {result.reasoning} (confidence: {result.probability})",
        tags=["sentiment", "analysis"]
    )

    return result.model_dump()
