from PIL import Image, ImageStat
import os

def analyze_image_fragility(image_path: str) -> dict:
    """
    Analyzes an image to determine fragility heuristics.
    
    Heuristics:
    1. Aspect Ratio: Extreme ratios imply tipping risk or awkward shape (High Fragility).
    2. Brightness Variance: High variance *might* imply reflectivity/glossy surface (High Fragility).
       (Very naive heuristic for 'reflective').
    
    Returns:
        dict: {
            "suggested_fragility": "low" | "medium" | "high",
            "confidence": float (0.0 - 1.0),
            "reasoning": str
        }
    """
    try:
        with Image.open(image_path) as img:
            # 1. Aspect Ratio
            width, height = img.size
            ratio = width / height if height > 0 else 1.0
            
            # 2. Brightness/Reflectivity (Naive: Standard Deviation of greyscale)
            # Glossy objects often have high contrast highlights.
            greyscale = img.convert("L")
            stat = ImageStat.Stat(greyscale)
            stddev = stat.stddev[0]
            
            # Logic
            reasons = []
            score = 0  # 0 = Low, 1 = Medium, 2 = High
            
            # Ratio Check
            if ratio > 2.5 or ratio < 0.4:
                score += 2
                reasons.append(f"Extreme aspect ratio ({ratio:.2f}) indicates tipping risk")
            elif ratio > 1.8 or ratio < 0.6:
                score += 1
                reasons.append(f"Non-standard aspect ratio ({ratio:.2f})")
            
            # Reflectivity Check (Heuristic threshold)
            # High stddev implies high contrast (specular highlights)
            if stddev > 60: 
                score += 1
                reasons.append("High contrast surface detected (possible glass/gloss)")
            
            # Determine Final Fragility
            if score >= 2:
                fragility = "high"
                confidence = 0.85
            elif score == 1:
                fragility = "medium"
                confidence = 0.70
            else:
                fragility = "low"
                confidence = 0.60
                reasons.append("Standard shape and surface")

            return {
                "suggested_fragility": fragility,
                "confidence": confidence,
                "reasoning": "; ".join(reasons)
            }
            
    except Exception as e:
        print(f"Error analyzing image: {e}")
        return {
            "suggested_fragility": "medium",
            "confidence": 0.0,
            "reasoning": "Could not analyze image"
        }
