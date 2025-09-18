import os
import json
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import google.generativeai as genai
from dotenv import load_dotenv

# --- INITIAL SETUP ---

# Load environment variables from the .env file
load_dotenv()

# Create the FastAPI app instance
app = FastAPI(
    title="Artisan Marketplace Assistant API",
    description="An API to generate marketing content for local artisans using Google's Gemini AI."
)

# Configure CORS (Cross-Origin Resource Sharing)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins, can restrict this in production
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods
    allow_headers=["*"],  # Allows all headers
)

# --- GEMINI API CONFIGURATION ---

# Get the API key from the environment variables
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Check if the API key is available
if not GOOGLE_API_KEY:
    raise ValueError("Google API key not found. Please set it in the .env file.")

# Configure the generative AI model
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-2.5-flash-lite')


# --- DATA MODELS (using Pydantic) ---

# Model for generating Product Content
class ProductRequest(BaseModel):
    product_name: str
    materials: str
    artisan_notes: str
    
    class Config:
        schema_extra = {
            "example": {
                "product_name": "Hand-painted Jaipuri Blue Pottery Vase",
                "materials": "Quartz powder, glass, fuller's earth",
                "artisan_notes": "Made by a third-generation artisan. Features a traditional floral motif inspired by royal gardens."
            }
        }

# Model for generating an Artisan Bio
class ArtisanBioRequest(BaseModel):
    artisan_name: str
    location: str
    craft_specialization: str
    personal_story: str # e.g., "Learned from my father, have been practicing for 15 years"
    
    class Config:
        schema_extra = {
            "example": {
                "artisan_name": "Ramesh Kumar",
                "location": "Jaipur, Rajasthan",
                "craft_specialization": "Blue Pottery",
                "personal_story": "I am a third-generation artist, carrying on the craft taught to me by my father and grandfather. Our family has been creating blue pottery for over 70 years."
            }
        }


# --- API ENDPOINTS ---

@app.get("/", tags=["Root"])
def read_root():
    """A simple root endpoint to confirm the server is running."""
    return {"message": "Welcome to the Artisan Assistant API! Visit /docs for more."}

@app.post("/api/generate-content", tags=["Content Generation"])
async def generate_product_content(request: ProductRequest):
    """
    Receives product details and generates marketing content, including SEO tags.
    """
    try:
        # ---The prompt is updated---
        prompt = f"""
        You are an expert in e-commerce marketing and storytelling for traditional Indian artisans. 
        Your task is to generate compelling marketing content based on the product details provided.
        The tone should be authentic, warm, and celebratory of the craft's heritage.

        Product Details:
        - Product Name: "{request.product_name}"
        - Key Materials: "{request.materials}"
        - Artisan's Notes: "{request.artisan_notes}"

        Generate the following content and provide the output as a single, clean JSON object with these exact keys: "product_title", "product_description", "instagram_post", "hashtags", "whatsapp_message", "seo_tags".

        - "product_title": A creative, SEO-friendly title for an e-commerce listing.
        - "product_description": A 2-paragraph, story-driven description.
        - "instagram_post": An engaging caption for an Instagram post, using emojis.
        - "hashtags": A string of 5-7 relevant hashtags, separated by spaces.
        - "whatsapp_message": A very short (1-2 lines), friendly message for sharing on WhatsApp.
        - "seo_tags": A string of 10-15 comma-separated keywords and tags suitable for Etsy, Amazon, and other marketplaces. Include material, craft type, color, style, and potential use cases.
        """
        
        # Call the Gemini API to get the content
        response = model.generate_content(prompt)
        
        # Clean the response and load it as JSON
        cleaned_response_text = response.text.strip().replace('```json', '').replace('```', '')
        content_json = json.loads(cleaned_response_text)
        
        return content_json

    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Failed to parse AI response as JSON.")
    except Exception as e:
        print(f"An error occurred: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while generating content.")


@app.post("/api/generate-bio", tags=["Content Generation"])
async def generate_artisan_bio(request: ArtisanBioRequest):
    """
    Receives artisan details and generates a professional, story-driven bio.
    """
    try:
        prompt = f"""
        You are an expert biographer and storyteller who specializes in writing warm and professional "About the Artisan" sections.
        Your task is to craft a compelling, short bio (1-2 paragraphs) from the details provided.
        The tone should build a personal connection with potential customers and highlight the artisan's dedication and heritage.

        Artisan Details:
        - Name: "{request.artisan_name}"
        - Location: "{request.location}"
        - Craft: "{request.craft_specialization}"
        - Personal Story: "{request.personal_story}"

        Generate a compelling bio based on these details. Return the output as a single JSON object with the key "artisan_bio".
        """
        
        response = model.generate_content(prompt)
        
        cleaned_response_text = response.text.strip().replace('```json', '').replace('```', '')
        bio_json = json.loads(cleaned_response_text)
        
        return bio_json
        
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Failed to parse AI response as JSON.")
    except Exception as e:
        print(f"An error occurred: {e}")

        raise HTTPException(status_code=500, detail="An error occurred while generating the bio.")
