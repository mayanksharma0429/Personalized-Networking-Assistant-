# app/services/fact_checker.py

import requests
import urllib.parse

def fact_check(query: str) -> str:
    """
    Wikipedia REST API ka use karke kisi topic ka quick summary (first paragraph) nikalta hai.
    """
    # Query ko URL format mein badalna (spaces ko hatana)
    formatted_query = urllib.parse.quote(query)
    url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{formatted_query}"
    
    headers = {
        'User-Agent': 'PersonalizedNetworkingAssistant/1.0 (info@example.com)'
    }
    
    try:
        # Wikipedia API ko call karna (timeout ke sath taaki app hang na ho)
        response = requests.get(url, headers=headers, timeout=5)
        
        if response.status_code == 404:
            return "Fact not found on Wikipedia."
            
        # Agar status code 200 (OK) nahi hai, toh exception throw karega
        response.raise_for_status()
        
        # JSON data extract karna
        data = response.json()
        
        # 'extract' key ke andar first paragraph hota hai
        if "extract" in data:
            return data["extract"]
        else:
            return "No summary found for this specific topic."
            
    except requests.exceptions.Timeout:
        return "Fact verification timed out. Please try again."
    except requests.exceptions.RequestException:
        # Network errors ya invalid JSON ke liye fallback message
        return "Could not verify the fact at this moment due to a network issue."
    except Exception:
        # Kisi aur anjaan error ke liye general fallback
        return "An unexpected error occurred while verifying the fact."
