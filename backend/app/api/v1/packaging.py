from fastapi import APIRouter
from fastapi.responses import FileResponse
from pydantic import BaseModel

from app.ai.engine import recommend_packaging
from app.services.pdf_generator import generate_packaging_pdf

router = APIRouter()


class PackagingRequest(BaseModel):
    product_length_mm: int
    product_width_mm: int
    product_height_mm: int
    product_weight_kg: float
    fragility_level: str
    product_category: str
    # AI Metadata (Optional)
    ai_confidence: float = 0.0
    ai_reasoning: str = ""
    ai_suggested_fragility: str = ""


@router.post("/recommend-packaging")
def recommend(request: PackagingRequest):
    # 1. Determine Decision Source
    fragility_source = "user"
    if request.ai_suggested_fragility:
        if request.fragility_level == request.ai_suggested_fragility:
            fragility_source = "ai"
        else:
            fragility_source = "user_override"

    # 3. Logic
    request_dict = request.dict()
    request_dict.pop("ai_confidence", None)
    request_dict.pop("ai_reasoning", None)
    request_dict.pop("ai_suggested_fragility", None)
    packaging_result = recommend_packaging(**request_dict)
    
    # 2. LOGGING (ML Data)
    try:
        from app.services.data_logger import log_decision
        log_decision({
            "image_id": None, # Frontend update needed to capture this
            "category": request.product_category,
            "dimensions": {
                "l": request.product_length_mm, 
                "w": request.product_width_mm, 
                "h": request.product_height_mm
            },
            "ai_suggested_fragility": request.ai_suggested_fragility,
            "user_selected_fragility": request.fragility_level,
            "final_fragility_used": packaging_result.get("fragility_level", request.fragility_level),
            "fragility_source": fragility_source,
            "estimated_cost": packaging_result.get("estimated_cost_inr"),
            "sustainability_score": packaging_result.get("sustainability_score")
        })
    except Exception as e:
        print(f"Log integration failed: {e}")

    return {**packaging_result, "fragility_source": fragility_source}


@router.post("/recommend-packaging-pdf")
async def recommend_pdf(data: PackagingRequest):
    # 1. Determine Decision Source
    fragility_source = "user"
    if data.ai_suggested_fragility:
        if data.fragility_level == data.ai_suggested_fragility:
            fragility_source = "ai"
        else:
            fragility_source = "user_override"

    # 2. Logic (Get Recommendation)
    data_dict = data.dict()
    data_dict.pop("ai_confidence", None)
    data_dict.pop("ai_reasoning", None)
    data_dict.pop("ai_suggested_fragility", None)
    packaging_result = recommend_packaging(**data_dict)

    # 3. LOGGING (ML Data)
    try:
        from app.services.data_logger import log_decision
        log_decision({
            "image_id": None, # Frontend update needed to capture this
            "category": data.product_category,
            "dimensions": {
                "l": data.product_length_mm, 
                "w": data.product_width_mm, 
                "h": data.product_height_mm
            },
            "ai_suggested_fragility": data.ai_suggested_fragility,
            "user_selected_fragility": data.fragility_level,
            "final_fragility_used": packaging_result.get("fragility_level", data.fragility_level),
            "fragility_source": fragility_source,
            "estimated_cost": packaging_result.get("estimated_cost_inr"),
            "sustainability_score": packaging_result.get("sustainability_score")
        })
    except Exception as e:
        print(f"Log integration failed: {e}")

    # Merge result with input data for the PDF report
    report_data = {**packaging_result, "product_details": data.dict(), "fragility_source": fragility_source}
    pdf_path = generate_packaging_pdf(report_data)

    return FileResponse(
        pdf_path,
        media_type="application/pdf",
        filename="packaging_recommendation.pdf"
    )
