
import os
import sys
import json
from dotenv import load_dotenv
from openai import OpenAI

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def test_keyword_generation(obligation):
    print(f"Testing Obligation: {obligation}")
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a legal search expert. Return a JSON object with a key 'keywords' containing 5-8 search terms for the given obligation. \n\nCRITICAL: You must predict the **exact words** a vendor would use to **limit** or **avoid** this obligation.\n- Example: If obligation is 'fix', search for 'refund', 'credit', 'obsolescence'.\n- Example: If obligation is 'indemnify', search for 'defend', 'hold harmless', 'control of defense'.\n- Example: If obligation is 'unlimited', search for 'cap', 'aggregate liability', 'fees paid'.\n\nFocus on specific nouns and verbs found in the contract text."},
                {"role": "user", "content": obligation}
            ],
            temperature=0.2,
            response_format={"type": "json_object"}
        )
        res_text = response.choices[0].message.content
        print(f"Raw Response: {res_text}")
        parsed = json.loads(res_text)
        keywords = parsed.get("keywords", [])
        print(f"Generated Keywords: {keywords}")
        
        # Check for critical terms
        critical_terms = ["refund", "reimburse", "terminate", "cap", "limit"]
        found_critical = [term for term in critical_terms if any(term in kw.lower() for kw in keywords)]
        print(f"Critical Terms Found: {found_critical}")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    # The failing obligation (User Case 4)
    ob = "The Licensee must guarantee that Licensed Products do not infringe patents or copyrights; if they do, the Licensee must (i) secure continued use rights, (ii) replace with non-infringing products."
    test_keyword_generation(ob)
