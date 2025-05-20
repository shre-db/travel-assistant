from dotenv import load_dotenv
load_dotenv()
import os

SERPAPI_API_KEY = os.environ["SERPAPI_API_KEY"]

from langchain.agents import tool
from random import choice, randint
from datetime import datetime, timedelta
from langchain_community.agent_toolkits.load_tools import load_tools
from model import llm


# Tool: Get Weather
@tool("get_weather", return_direct=False, description="Get weather forecast for a location and date. Input format: 'location, YYYY-MM-DD'.")
def get_weather(input_str: str) -> str:
    """Actual implementation (keep your docstring)"""
    try:
        location, date = map(str.strip, input_str.split(','))
        # TODO: Integrate with a real weather API
        weather_condition = ["Sunny", "Rainy", "Cloudy", "Snowy"]
        temperature = [22, 18, 15, -5]
        # Simulate a weather condition and temperature
        import random
        condition = random.choice(weather_condition)
        temp = random.choice(temperature)
        return f"Weather for {location} on {date} {condition}, {temp}°C."
    except ValueError:
        return "Invalid input format. Expected 'location, YYYY-MM-DD"

# Tool: Search Hotels
@tool("search_hotels", return_direct=False, description="Search for hotels based on location, arrival date, and departure date. Input format: 'location, YYYY-MM-DD, YYYY-MM-DD'.")
def search_hotels(input_str: str) -> str:
    """Actual implementation (keep your docstring)"""
    try:
        location, arrival_date, depart_date = map(str.strip, input_str.split(','))
        # TODO: Integrate with a real hotel search API
        # Simulate hotel search results
        hotels = ["Hotel A", "Hotel B", "Hotel C"]
        return f"Hotels for {location} from {arrival_date} to {depart_date}: {', '.join(hotels)}"
    except ValueError:
        return "Invalid input format. Expected three parameters (location, arrival date, departure date): 'location, YYYY-MM-DD, YYYY-MM-DD'."
    
# Tool: Search Attractions
@tool("search_attactions", return_direct=False, description="Search for attraction sites based on location, interest and budget. Input format: 'location, interest, budget'")
def search_attractions(query: str) -> str:
    """Find top-rated attractions. Input: 'location, interest, budget'"""
    try:
        location, interest, budget = map(str.strip, query.split(','))
        
        # Mock attraction database
        mock_attractions = {
            'paris': {
                'museum': [
                    "Louvre Museum (Priority Access Ticket)",
                    "Musée d'Orsay Impressionist Masterpieces",
                    "Palace of Versailles Guided Tour"
                ],
                'food': [
                    "Montmartre Food & Wine Walking Tour",
                    "Secret Food Tours: Marais District",
                    "French Cooking Class with Chef Marie"
                ]
            },
            'tokyo': {
                'culture': [
                    "Senso-ji Temple & Asakusa Cultural Walk",
                    "Sumo Morning Practice Tour",
                ],
                'shopping': [
                    "Ginza Luxury Boutique Experience",
                    "Akihabara Electronics & Anime Tour"
                ]
            }
        }
        
        # Generate mock response
        default = ["City Walking Tour", "Local Market Visit", "Historical District Exploration"]
        attractions = mock_attractions.get(location.lower(), {}).get(interest.lower(), default)
        
        # Add budget-based filtering
        budget_levels = {
            "low": ("Free Walking Tour", "Public Park Visit"),
            "medium": ("Guided Group Tour", "Museum Entry Pass"),
            "high": ("Private VIP Experience", "Helicopter Tour")
        }
        attractions.extend(budget_levels.get(budget.lower(), ()))
        
        return f"Top {interest} attractions in {location}: {', '.join(attractions[:3])}"
    
    except ValueError:
        return "Error: Please use format 'location, interest, budget'"

# Tool: Get Flights
@tool("transport_options", return_direct=False, description="Check transport between locations. Input: 'origin, destination, date/time'")
def transport_options(route: str) -> str:
    """Check transport between locations. Input: 'origin, destination, date/time'"""
    try:
        origin, dest, datetime_str = map(str.strip, route.split(','))
        
        # Mock transport options
        options = []
        transport_types = [
            ("Train", "high-speed rail", 60, 120),
            ("Bus", "intercity coach", 120, 180),
            ("Flight", "regional aircraft", 45, 300)
        ]
        
        # Generate 3 mock options
        for _ in range(3):
            transport_type, description, base_duration, base_price = choice(transport_types)
            duration = base_duration + randint(-15, 30)
            price = base_price + randint(-50, 100)
            
            options.append(
                f"{transport_type}: {description}\n"
                f"⏱️ {duration} mins | 💶 €{price} | "
                f"🚩 {origin.capitalize()} Central → {dest.capitalize()} Central"
            )
            
        return "Available transport:\n" + "\n\n".join(options)
    
    except ValueError:
        return "Error: Please use format 'origin, destination, date/time'"

# Tool: Get Visa Requirements

@tool("get_visa_requirements", return_direct=False, description="Get visa requirements for a traveler of a given nationality visiting a destination. Input format: 'nationality, destination'")
def get_visa_requirements(nationality: str, destination: str) -> str:
    """
    Get visa requirements for a traveller of a given nationality visiting a destination.
    Args:
        nationality (str): Country of citizenship.
        destination (str): Destination country.
    Returns:
        str: Visa information.
    """
    # TODO: Integrate with a real visa info API
    return f"Visa requirements for {nationality} traveling to {destination}: Visa on arrival."

# @tool("things_to_ask", return_direct=False, description="Get information such as missing details from the user. Input format: 'query'")
# def things_to_ask(query: str):
#     return f"Proceed with asking additiona linformation from the user."


# Load tools with proper configuration
tools = load_tools(["serpapi", "llm-math"],
                  llm=llm,
                  serpapi_api_key=SERPAPI_API_KEY)

# Add custom tool to the tools list
tools.extend([get_weather, search_hotels, search_attractions, transport_options])
