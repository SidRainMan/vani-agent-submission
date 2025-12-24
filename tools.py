import json

# --- MOCK DATABASE ---
# Ideally load from a file, but for the assignment, this list acts as the DB
SCHEMES_DB = [
    {
        "name": "Lakshmir Bhandar",
        "rules": {"gender": "Female", "state": "West Bengal", "age_min": 25, "age_max": 60},
        "benefit": "Monthly financial assistance"
    },
    {
        "name": "Yuvashree",
        "rules": {"occupation": "Unemployed", "state": "West Bengal", "age_min": 18, "age_max": 45},
        "benefit": "Unemployment allowance"
    },
    {
        "name": "Krishak Bandhu",
        "rules": {"occupation": "Farmer", "state": "West Bengal"},
        "benefit": "Financial aid for farmers"
    },
    {
        "name": "Old Age Pension",
        "rules": {"age_min": 60, "income_limit": 100000},
        "benefit": "Monthly pension for senior citizens"
    }
]

def check_eligibility(user_profile):
    """Filters schemes based on hard rules."""
    eligible = []
    for s in SCHEMES_DB:
        rules = s.get("rules", {})
        
        # 1. State Check
        if "state" in rules and user_profile.get("state"):
            if rules["state"] != user_profile["state"]:
                continue
        
        # 2. Gender Check
        if "gender" in rules and user_profile.get("gender"):
            if rules["gender"].lower() != user_profile["gender"].lower():
                continue
        
        # 3. Age Check
        if user_profile.get("age"):
            try:
                age = int(user_profile["age"])
                if "age_min" in rules and age < rules["age_min"]: continue
                if "age_max" in rules and age > rules["age_max"]: continue
            except:
                pass # Ignore if age is not a number
        
        # 4. Occupation Check
        if "occupation" in rules and user_profile.get("occupation"):
             if rules["occupation"].lower() not in user_profile["occupation"].lower():
                 continue

        eligible.append(s)
    return eligible

def calculate_strength_score(user_profile, scheme):
    """Calculates a match score (0-100) for sorting."""
    score = 100
    rules = scheme.get("rules", {})
    
    # Penalize if income is close to limit
    if "income_limit" in rules and user_profile.get("income"):
        try:
            limit = rules["income_limit"]
            income = int(user_profile["income"])
            if income > limit: return 0
            # Higher income = Lower need score
            score -= (income / limit) * 20
        except: pass
            
    return int(max(0, score))

def validate_guardrails(user_profile, scheme):
    """Final safety check."""
    # Example: Ensure men don't get female-only schemes even if LLM hallucinates
    rules = scheme.get("rules", {})
    if rules.get("gender") == "Female" and user_profile.get("gender", "").lower() == "male":
        return "FAIL", "Gender Mismatch"
    return "PASS", "Safe"