from typing import Dict


def recommend_packaging(
    product_length_mm: int,
    product_width_mm: int,
    product_height_mm: int,
    product_weight_kg: float,
    fragility_level: str,
    product_category: str,
) -> Dict:
    """
    Core packaging recommendation logic (MVP version)
    """

    # 1. Cushion allowance (mm)
    if fragility_level == "high":
        cushion = 30
    elif fragility_level == "medium":
        cushion = 20
    else:
        cushion = 10

    # 2. Inner box dimensions
    inner_length = product_length_mm + cushion
    inner_width = product_width_mm + cushion
    inner_height = product_height_mm + cushion

    # 3. Material selection
    if product_weight_kg > 5 or fragility_level == "high":
        material = "Corrugated Box"
        flute_type = "Double Wall"
        cushioning = "EPE Foam"
    else:
        material = "Corrugated Box"
        flute_type = "Single Wall"
        cushioning = "Bubble Wrap"

    # 4. Outer box dimensions
    board_thickness = 5
    outer_length = inner_length + board_thickness
    outer_width = inner_width + board_thickness
    outer_height = inner_height + board_thickness

    # 5. Cost estimation
    volume = outer_length * outer_width * outer_height / 1_000_000
    estimated_cost = round(200 * volume + (50 if cushioning == "EPE Foam" else 20), 2)

    # 6. Sustainability score
    sustainability_score = 70 if flute_type == "Single Wall" else 55

    return {
        "box_type": material,
        "flute_type": flute_type,
        "cushioning": cushioning,
        "inner_dimensions_mm": {
            "length": inner_length,
            "width": inner_width,
            "height": inner_height,
        },
        "outer_dimensions_mm": {
            "length": outer_length,
            "width": outer_width,
            "height": outer_height,
        },
        "estimated_cost_inr": estimated_cost,
        "sustainability_score": sustainability_score,
    }
