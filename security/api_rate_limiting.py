# ==============================================
# 🚀 INDUSTRY-LEADING API RATE LIMITING FOR AI EXECUTION
# ✅ Prevents Abuse, Ensures Fair Usage, and Protects Model APIs
# ==============================================

import time
import logging
from collections import defaultdict
from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordBearer

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')

# OAuth2 and API Key Configuration
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Rate Limiting Configuration (in requests per minute)
DEFAULT_RATE_LIMIT = 100  # Default rate limit for most users (100 requests per minute)
GUEST_RATE_LIMIT = 30  # Rate limit for guest users
ADMIN_RATE_LIMIT = 500  # Rate limit for admin users

# Data structure to store rate limit counters
request_counters = defaultdict(lambda: {'count': 0, 'last_reset': time.time()})

# ---------------------------------------------------------------
# Function to reset the rate limit counters at the beginning of each minute
# ---------------------------------------------------------------
def reset_rate_limit(user_id: str):
    """Reset the rate limit counter for a user at the start of a new minute."""
    current_time = time.time()
    if current_time - request_counters[user_id]['last_reset'] >= 60:
        request_counters[user_id]['count'] = 0  # Reset the count
        request_counters[user_id]['last_reset'] = current_time
        logging.info(f"✅ Rate limit for {user_id} has been reset.")

# ---------------------------------------------------------------
# Function to check and enforce the rate limit
# ---------------------------------------------------------------
def enforce_rate_limit(user_id: str):
    """Check if the user has exceeded their rate limit."""
    reset_rate_limit(user_id)  # Reset counter if a new minute has passed

    # Get the rate limit for the user based on their role
    rate_limit = get_rate_limit(user_id)

    if request_counters[user_id]['count'] >= rate_limit:
        logging.error(f"❌ User {user_id} has exceeded the rate limit of {rate_limit} requests per minute.")
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Rate limit exceeded. Please try again later."
        )
    else:
        # Increment the request counter
        request_counters[user_id]['count'] += 1
        logging.info(f"✅ User {user_id} made a request. Current count: {request_counters[user_id]['count']}")

# ---------------------------------------------------------------
# Function to determine the rate limit for the user based on their role
# ---------------------------------------------------------------
def get_rate_limit(user_id: str):
    """Determine the rate limit based on the user's role."""
    # Simulated user roles (replace with actual role checking from your IAM system)
    user_roles = {
        "guest_user": GUEST_RATE_LIMIT,
        "basic_user": DEFAULT_RATE_LIMIT,
        "admin_user": ADMIN_RATE_LIMIT
    }
    
    # Default rate limit for unknown users (or guests)
    return user_roles.get(user_id, DEFAULT_RATE_LIMIT)

# ---------------------------------------------------------------
# Function to monitor API usage and generate alerts
# ---------------------------------------------------------------
def monitor_api_usage():
    """Monitor the overall API usage and send alerts if necessary."""
    logging.info("🔹 Monitoring API usage...")

    # Simulate monitoring API requests and rate limits
    for user_id, data in request_counters.items():
        if data['count'] > 0:
            logging.info(f"User {user_id} has made {data['count']} requests in the last minute.")

# ---------------------------------------------------------------
# Function to simulate the API request flow and rate limiting
# ---------------------------------------------------------------
def api_request(user_id: str):
    """Simulate an API request and enforce rate limiting."""
    logging.info(f"🔹 User {user_id} is making an API request...")
    
    # Enforce rate limit before processing the request
    enforce_rate_limit(user_id)

    # Simulate processing the API request (e.g., AI model inference)
    time.sleep(0.2)  # Simulate request processing time

    logging.info(f"✅ API request for user {user_id} completed successfully.")
    return {"message": f"Request successful for user {user_id}."}

# ---------------------------------------------------------------
# Main function to run API rate limiting and monitoring
# ---------------------------------------------------------------
def main():
    """Main function to continuously handle API rate limiting and monitoring."""
    logging.info("🚀 Starting API Rate Limiting for AI Model Execution...")

    # Simulate API requests from different users (replace with actual user requests)
    users = ["guest_user", "basic_user", "admin_user"]
    
    for user in users:
        try:
            api_request(user)  # Simulate an API request
            time.sleep(1)  # Wait for the next request (simulate interval between requests)
        except HTTPException as e:
            logging.error(f"❌ Error: {e.detail}")
            break

    # Monitor overall API usage periodically
    while True:
        monitor_api_usage()
        sleep(60)  # Wait for the next monitoring cycle

if __name__ == "__main__":
    main()
