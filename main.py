import os
import httpx
import logging
import uuid
from datetime import datetime, date
from typing import Optional, List, Dict, Any
from fastapi import FastAPI, HTTPException, Depends, Query
from pydantic import BaseModel, Field, validator
from dotenv import load_dotenv

# Load Zorin OS / Ubuntu Environment Variables
load_dotenv()

# Advanced Logging for Agent Observability
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("PetLet-Agent-Core")

app = FastAPI(
    title="Pet Let Agentic Tool Server",
    description="High-fidelity Action Layer for Autonomous Property Management.",
    version="2.0.0"
)

# --- MODELS / SCHEMAS ---

class GuestRequest(BaseModel):
    booking_id: str = Field(..., example="PL-9923")
    property_id: str = Field(..., example="BEACH-FRONT-01")

class CheckoutExtension(GuestRequest):
    requested_date: date = Field(..., description="The date the guest wants to leave")
    buffer_hours: int = Field(default=2, description="Maintenance buffer between guests")

    @validator('requested_date')
    def date_must_be_future(cls, v):
        if v < date.today():
            raise ValueError('Extension date must be in the future')
        return v

# --- REUSABLE LOGIC LAYER ---

class PMSConnector:
    """Manual REST Client for PMS Integration (No No-Code tools)"""
    def __init__(self):
        self.api_key = os.getenv("PMS_API_KEY", "DEV_MODE_KEY")
        self.base_url = os.getenv("PMS_API_URL", "https://api.petlet.net/v1")

    async def check_room_availability(self, property_id: str, target_date: date) -> bool:
        """Simulates a call to check if the next guest arrives on target_date."""
        # In production: GET /calendar/{property_id}/availability
        logger.info(f"Checking availability for {property_id} on {target_date}")
        return True # Mocking a 'Clear' calendar

    async def update_booking_status(self, booking_id: str, new_date: date) -> Dict:
        """Executes the state change in the PMS."""
        logger.info(f"Executing PMS Update for {booking_id}")
        # Simulated API Patch
        return {"status": "Updated", "id": booking_id, "new_checkout": str(new_date)}

# --- AGENTIC TOOL ENDPOINTS ---

@app.get("/tools/verify-and-extend")
async def tool_verify_and_extend(
    booking_id: str, 
    property_id: str, 
    requested_date: str,
    pms: PMSConnector = Depends()
):
    """
    COMPLEX TOOL: The AI Agent uses this to:
    1. Verify current calendar conflicts
    2. Check cleaning crew schedules
    3. Update the PMS if clear
    """
    target_date = datetime.strptime(requested_date, "%Y-%m-%d").date()
    
    # Step 1: Logic Check (Agentic Reasoning Support)
    is_available = await pms.check_room_availability(property_id, target_date)
    
    if not is_available:
        return {
            "status": "denied",
            "observation": "Calendar conflict detected. The room is booked for a new guest on that date."
        }

    # Step 2: Action Layer (The 'Close the Loop' phase)
    pms_result = await pms.update_booking_status(booking_id, target_date)
    
    return {
        "status": "success",
        "action_taken": "modification_complete",
        "observation": f"Booking {booking_id} extended. PMS records updated successfully.",
        "raw_data": pms_result
    }

@app.get("/health")
def health():
    return {"status": "active", "os": "Linux-Zorin-17", "container": "Docker-Ready"}
