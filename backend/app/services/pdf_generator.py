from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from datetime import datetime
import os


def generate_packaging_pdf(data: dict) -> str:
    """
    Generates a professional packaging recommendation PDF.
    Args:
        data: merged dict containing 'product_details' and recommendation keys.
    """
    os.makedirs("generated_pdfs", exist_ok=True)
    filename = f"packaging_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    file_path = os.path.join("generated_pdfs", filename)

    c = canvas.Canvas(file_path, pagesize=A4)
    width, height = A4
    
    # --- Layout Constants ---
    margin_x = 50
    curr_y = height - 50
    line_height = 20
    
    # --- Helper Functions ---
    def draw_header(text, y):
        c.setFont("Helvetica-Bold", 14)
        c.setFillColor(colors.darkblue)
        c.drawString(margin_x, y, text)
        c.setStrokeColor(colors.grey)
        c.line(margin_x, y - 5, width - margin_x, y - 5)
        c.setFillColor(colors.black)
        return y - 25

    def draw_key_value(key, value, x, y):
        c.setFont("Helvetica-Bold", 10)
        c.drawString(x, y, f"{key}:")
        c.setFont("Helvetica", 10)
        c.drawString(x + 100, y, str(value))

    # --- 1. Report Header ---
    c.setFont("Helvetica-Bold", 20)
    c.drawString(margin_x, curr_y, "Packaging Recommendation Report")
    
    c.setFont("Helvetica", 10)
    c.drawRightString(width - margin_x, curr_y, f"Date: {datetime.now().strftime('%Y-%m-%d')}")
    curr_y -= 40

    # --- 2. Product Summary ---
    product = data.get("product_details", {})
    curr_y = draw_header("Product Summary", curr_y)
    
    draw_key_value("Category", product.get("product_category", "N/A"), margin_x, curr_y)
    draw_key_value("Weight", f"{product.get('product_weight_kg', 0)} kg", margin_x + 250, curr_y)
    curr_y -= line_height
    draw_key_value("Dimensions", f"{product.get('product_length_mm')} x {product.get('product_width_mm')} x {product.get('product_height_mm')} mm", margin_x, curr_y)
    draw_key_value("Fragility", product.get("fragility_level", "N/A"), margin_x + 250, curr_y)
    curr_y -= line_height

    # AI Reasoning Block (Formal)
    if product.get("ai_confidence", 0) > 0:
        c.setStrokeColor(colors.lightgrey)
        c.setFillColor(colors.whitesmoke)
        c.rect(margin_x, curr_y - 60, width - 2*margin_x, 50, fill=1)
        c.setFillColor(colors.black)
        
        c.setFont("Helvetica-Bold", 10)
        c.drawString(margin_x + 10, curr_y - 25, "AI-Assisted Fragility Assessment")
        
        confidence_pct = int(product.get("ai_confidence") * 100)
        c.setFont("Helvetica-Oblique", 9)
        c.drawRightString(width - margin_x - 10, curr_y - 25, f"Confidence: {confidence_pct}%")

        c.setFont("Helvetica", 9)
        c.drawString(margin_x + 10, curr_y - 40, f"Analysis: {product.get('ai_reasoning')}")
        
        c.setFont("Helvetica-Oblique", 7)
        c.setFillColor(colors.grey)
        c.drawString(margin_x + 10, curr_y - 55, "Disclaimer: This assessment is AI-assisted and can be overridden by the user.")
        
        curr_y -= 80  # Space after block
    else:
        curr_y -= 25

    # --- Decision Summary (New) ---
    source = data.get("fragility_source", "user")
    ai_suggested = product.get("ai_suggested_fragility", "N/A")
    final_level = product.get("fragility_level", "N/A")

    c.setFont("Helvetica-Bold", 10)
    c.drawString(margin_x, curr_y, "Fragility Decision Summary:")
    c.setFont("Helvetica", 10)
    
    source_text = "User Selection"
    if source == "ai":
        source_text = "AI Recommendation (Accepted)"
    elif source == "user_override":
        source_text = "User Override"

    c.drawString(margin_x + 150, curr_y, f"Source: {source_text}")
    curr_y -= 15
    c.setFont("Helvetica", 9)
    c.setFillColor(colors.darkgrey)
    c.drawString(margin_x + 150, curr_y, f"(AI Suggested: {ai_suggested} | Final: {final_level})")
    c.setFillColor(colors.black)
    curr_y -= 30


    # --- 3. Recommended Specification ---
    curr_y = draw_header("Recommended Packaging", curr_y)
    
    draw_key_value("Box Type", data.get("box_type"), margin_x, curr_y)
    curr_y -= line_height
    draw_key_value("Material", data.get("flute_type"), margin_x, curr_y)
    curr_y -= line_height
    draw_key_value("Cushioning", data.get("cushioning"), margin_x, curr_y)
    curr_y -= 40

    # --- 4. Dimensions Table ---
    curr_y = draw_header("Box Dimensions (mm)", curr_y)
    
    # Table Header
    c.setFillColor(colors.lightgrey)
    c.rect(margin_x, curr_y - 5, width - 2 * margin_x, 20, fill=1, stroke=0)
    c.setFillColor(colors.black)
    c.setFont("Helvetica-Bold", 10)
    c.drawString(margin_x + 10, curr_y + 2, "Dimension")
    c.drawString(margin_x + 150, curr_y + 2, "Inner Box")
    c.drawString(margin_x + 300, curr_y + 2, "Outer Box")
    curr_y -= 25

    # Table Rows
    inner = data.get("inner_dimensions_mm", {})
    outer = data.get("outer_dimensions_mm", {})
    
    dims = ["length", "width", "height"]
    for d in dims:
        c.setFont("Helvetica-Bold", 10)
        c.drawString(margin_x + 10, curr_y, d.capitalize())
        c.setFont("Helvetica", 10)
        c.drawString(margin_x + 150, curr_y, str(inner.get(d, 0)))
        c.drawString(margin_x + 300, curr_y, str(outer.get(d, 0)))
        c.setStrokeColor(colors.lightgrey)
        c.line(margin_x, curr_y - 5, width - margin_x, curr_y - 5)
        curr_y -= 20
        
    curr_y -= 20

    # --- 5. Cost & Sustainability ---
    curr_y = draw_header("Analysis", curr_y)
    
    c.setFont("Helvetica-Bold", 12)
    c.drawString(margin_x, curr_y, "Estimated Cost:")
    c.setFont("Helvetica", 12)
    c.drawString(margin_x + 110, curr_y, f"INR {data.get('estimated_cost_inr', 0)}")
    
    c.drawRightString(width - margin_x, curr_y, f"Sustainability Score: {data.get('sustainability_score', 0)}/100")
    
    # Footer
    c.setFont("Helvetica-Oblique", 8)
    c.setFillColor(colors.grey)
    c.drawCentredString(width / 2, 30, "Generated by AI Packaging SaaS")

    c.showPage()
    c.save()
    return file_path
