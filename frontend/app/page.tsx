"use client";

import { useState } from "react";

export default function Home() {
  const [formData, setFormData] = useState({
    product_length_mm: "",
    product_width_mm: "",
    product_height_mm: "",
    product_weight_kg: "",
    fragility_level: "medium",
    product_category: "electronics",
  });

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  // Image Upload State
  const [imageFile, setImageFile] = useState<File | null>(null);
  const [imagePreview, setImagePreview] = useState<string | null>(null);
  const [isUploading, setIsUploading] = useState(false);
  const [imageId, setImageId] = useState<string | null>(null);
  // AI Metadata
  const [aiMetadata, setAiMetadata] = useState({ confidence: 0, reasoning: "", suggested_level: "" });

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleImageChange = async (e: React.ChangeEvent<HTMLInputElement>) => {
    if (!e.target.files || !e.target.files[0]) return;

    const file = e.target.files[0];
    setImageFile(file);
    setImagePreview(URL.createObjectURL(file));

    setIsUploading(true);
    setError("");

    try {
      const uploadData = new FormData();
      uploadData.append("file", file);

      const res = await fetch("https://ai-packaging-backend.onrender.com/api/v1/upload-image", {
        method: "POST",
        body: uploadData,
      });

      if (!res.ok) {
        throw new Error("Image upload failed");
      }

      // ✅ THIS WAS MISSING
      const data = await res.json();

      // ✅ NOW data EXISTS
      if (data.suggested_fragility) {
        setFormData(prev => ({
          ...prev,
          fragility_level: data.suggested_fragility,
        }));

        setAiMetadata({
          confidence: data.confidence ?? 0,
          reasoning: data.analysis_note ?? "",
          suggested_level: data.suggested_fragility // Store for override check
        });

        // alert removed in favor of UI card
      }

    } catch (err) {
      const message = err instanceof Error ? err.message : "Failed to upload image";
      setError(message);
      console.error("Upload error:", err);
    } finally {
      setIsUploading(false);
    }
  };


  const [recommendation, setRecommendation] = useState<any>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (isUploading) return;

    setLoading(true);
    setError("");

    try {
      // 1. Get Recommendation Data (JSON)
      const res = await fetch("https://ai-packaging-backend.onrender.com/api/v1/recommend-packaging", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          ...formData,
          product_length_mm: Number(formData.product_length_mm),
          product_width_mm: Number(formData.product_width_mm),
          product_height_mm: Number(formData.product_height_mm),
          product_weight_kg: Number(formData.product_weight_kg),
          ai_confidence: aiMetadata.confidence,
          ai_reasoning: aiMetadata.reasoning,
          ai_suggested_fragility: (aiMetadata as any).suggested_level || null
        }),
      });

      if (!res.ok) throw new Error("Recommendation failed");

      const data = await res.json();
      setRecommendation(data);

      // Auto-scroll to summary
      setTimeout(() => window.scrollTo({ top: document.body.scrollHeight, behavior: 'smooth' }), 100);

    } catch (err) {
      setError(err instanceof Error ? err.message : "An unknown error occurred");
    } finally {
      setLoading(false);
    }
  };

  const handleDownloadPDF = async () => {
    try {
      const res = await fetch("https://ai-packaging-backend.onrender.com/api/v1/recommend-packaging-pdf", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        // Re-send same data to generate PDF
        body: JSON.stringify({
          ...formData,
          product_length_mm: Number(formData.product_length_mm),
          product_width_mm: Number(formData.product_width_mm),
          product_height_mm: Number(formData.product_height_mm),
          product_weight_kg: Number(formData.product_weight_kg),
          ai_confidence: aiMetadata.confidence,
          ai_reasoning: aiMetadata.reasoning,
          ai_suggested_fragility: (aiMetadata as any).suggested_level || null
        }),
      });

      if (!res.ok) throw new Error("PDF generation failed");

      const blob = await res.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = `packaging_report_${Date.now()}.pdf`;
      document.body.appendChild(a);
      a.click();
      a.remove();
    } catch (err) {
      setError("Failed to download PDF");
    }
  };

  const handleReset = () => {
    setFormData({
      product_length_mm: "",
      product_width_mm: "",
      product_height_mm: "",
      product_weight_kg: "",
      fragility_level: "medium",
      product_category: "electronics",
    });
    setImageFile(null);
    setImagePreview(null);
    setImageId(null);
    setAiMetadata({ confidence: 0, reasoning: "", suggested_level: "" });
    setRecommendation(null);
    setError("");
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  return (
    <main style={styles.container}>
      <div style={styles.card}>
        <h1 style={styles.title}>📦 Packaging Recommender</h1>
        <p style={styles.subtitle}>Enter product details to get AI suggestions</p>

        <form onSubmit={handleSubmit} style={styles.form}>

          {/* Image Upload Section */}
          <div style={styles.group}>
            <label style={styles.label}>Product Image</label>
            <div style={styles.imageUpload}>
              <input
                type="file"
                accept="image/png, image/jpeg"
                onChange={handleImageChange}
                style={styles.fileInput}
              />
              {isUploading && <span style={styles.uploadStatus}>Uploading...</span>}
              {imageId && <span style={styles.successStatus}>✓ Uploaded</span>}
            </div>
            {imagePreview && (
              <div style={styles.previewContainer}>
                <img src={imagePreview} alt="Preview" style={styles.previewImage} />
              </div>
            )}
          </div>

          <div style={styles.divider} />

          <div style={styles.row}>
            <div style={styles.group}>
              <label style={styles.label}>Length (mm)</label>
              <input
                name="product_length_mm"
                type="number"
                required
                min="1"
                style={styles.input}
                value={formData.product_length_mm}
                onChange={handleChange}
              />
            </div>
            <div style={styles.group}>
              <label style={styles.label}>Width (mm)</label>
              <input
                name="product_width_mm"
                type="number"
                required
                min="1"
                style={styles.input}
                value={formData.product_width_mm}
                onChange={handleChange}
              />
            </div>
          </div>

          <div style={styles.row}>
            <div style={styles.group}>
              <label style={styles.label}>Height (mm)</label>
              <input
                name="product_height_mm"
                type="number"
                required
                min="1"
                style={styles.input}
                value={formData.product_height_mm}
                onChange={handleChange}
              />
            </div>
            <div style={styles.group}>
              <label style={styles.label}>Weight (kg)</label>
              <input
                name="product_weight_kg"
                type="number"
                required
                min="0.1"
                step="0.1"
                style={styles.input}
                value={formData.product_weight_kg}
                onChange={handleChange}
              />
            </div>
          </div>

          <div style={styles.group}>
            <label style={styles.label}>Fragility Level</label>
            <select
              name="fragility_level"
              style={styles.select}
              value={formData.fragility_level}
              onChange={handleChange}
            >
              <option value="low">Low (Durable)</option>
              <option value="medium">Medium</option>
              <option value="high">High (Fragile)</option>
            </select>
          </div>

          {/* AI Assessment Card */}
          {aiMetadata.confidence > 0 && (
            <div style={{
              ...styles.aiCard,
              borderColor: formData.fragility_level !== (aiMetadata as any).suggested_level ? '#ff9800' : '#333'
            }}>
              <div style={styles.aiHeader}>
                <span style={styles.aiTitle}>🤖 AI Analysis</span>
                <span style={styles.aiBadge}>
                  {Math.round(aiMetadata.confidence * 100)}% Confidence
                </span>
              </div>
              <p style={styles.aiReason}>{aiMetadata.reasoning}</p>
              {formData.fragility_level !== (aiMetadata as any).suggested_level && (
                <p style={styles.aiOverride}>
                  ⚠️ You have overridden the AI suggestion.
                </p>
              )}
            </div>
          )}

          <div style={styles.group}>
            <label style={styles.label}>Category</label>
            <select
              name="product_category"
              style={styles.select}
              value={formData.product_category}
              onChange={handleChange}
            >
              <option value="electronics">Electronics</option>
              <option value="clothing">Clothing</option>
              <option value="home_goods">Home Goods</option>
              <option value="industrial">Industrial</option>
            </select>
          </div>

          {error && <p style={styles.error}>{error}</p>}

          {recommendation ? (
            <div style={styles.summaryCard}>
              <h3 style={styles.summaryTitle}>✅ Recommendation Ready</h3>

              <div style={styles.summaryGrid}>
                <div style={styles.summaryItem}>
                  <span style={styles.summaryLabel}>Packaging</span>
                  <span style={styles.summaryValue}>{recommendation.box_type}</span>
                </div>
                <div style={styles.summaryItem}>
                  <span style={styles.summaryLabel}>Material</span>
                  <span style={styles.summaryValue}>{recommendation.flute_type}</span>
                </div>
                <div style={styles.summaryItem}>
                  <span style={styles.summaryLabel}>Est. Cost</span>
                  <span style={styles.summaryValue}>₹{recommendation.estimated_cost_inr}</span>
                </div>
                <div style={styles.summaryItem}>
                  <span style={styles.summaryLabel}>Eco Score</span>
                  <span style={{ ...styles.summaryValue, color: '#4caf50' }}>
                    {recommendation.sustainability_score}/100
                  </span>
                </div>
              </div>

              <div style={styles.actionButtons}>
                <button type="button" onClick={handleDownloadPDF} style={styles.primaryButton}>
                  ⬇️ Download Official Report
                </button>
                <button type="button" onClick={handleReset} style={styles.secondaryButton}>
                  🔄 Start New Product
                </button>
              </div>
              <p style={styles.disclaimer}>⚠️ AI-assisted recommendation. Verify before production.</p>
            </div>
          ) : (
            <button
              type="submit"
              disabled={loading || isUploading}
              style={{ ...styles.button, opacity: (loading || isUploading) ? 0.7 : 1 }}
            >
              {loading ? "Analyzing & Generating..." : "Generate Recommendation"}
            </button>
          )}
        </form>
      </div>
    </main>
  );
}

const styles = {
  container: {
    minHeight: "100vh",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    backgroundColor: "#111",
    fontFamily: "system-ui, -apple-system, sans-serif",
    padding: "20px",
  },
  card: {
    backgroundColor: "#1a1a1a",
    padding: "2rem",
    borderRadius: "12px",
    width: "100%",
    maxWidth: "450px",
    boxShadow: "0 4px 6px rgba(0, 0, 0, 0.3)",
    border: "1px solid #333",
  },
  title: {
    margin: "0 0 0.5rem 0",
    color: "#fff",
    fontSize: "1.5rem",
    textAlign: "center" as const,
  },
  subtitle: {
    margin: "0 0 2rem 0",
    color: "#888",
    fontSize: "0.9rem",
    textAlign: "center" as const,
  },
  form: {
    display: "flex",
    flexDirection: "column" as const,
    gap: "1.2rem",
  },
  row: {
    display: "flex",
    gap: "1rem",
  },
  group: {
    display: "flex",
    flexDirection: "column" as const,
    flex: 1,
    gap: "0.4rem",
  },
  label: {
    color: "#ccc",
    fontSize: "0.85rem",
    fontWeight: 500,
  },
  input: {
    padding: "0.75rem",
    borderRadius: "6px",
    border: "1px solid #333",
    backgroundColor: "#222",
    color: "#fff",
    fontSize: "0.95rem",
    outline: "none",
  },
  select: {
    padding: "0.75rem",
    borderRadius: "6px",
    border: "1px solid #333",
    backgroundColor: "#222",
    color: "#fff",
    fontSize: "0.95rem",
    outline: "none",
  },
  button: {
    marginTop: "0.5rem",
    padding: "0.9rem",
    borderRadius: "6px",
    border: "none",
    backgroundColor: "#fff",
    color: "#000",
    fontSize: "1rem",
    fontWeight: 600,
    cursor: "pointer",
    transition: "all 0.2s",
  },
  error: {
    color: "#ff4444",
    fontSize: "0.85rem",
    textAlign: "center" as const,
    margin: 0,
  },
  imageUpload: {
    display: 'flex',
    alignItems: 'center',
    gap: '10px'
  },
  fileInput: {
    color: '#aaa',
    fontSize: '0.85rem'
  },
  previewContainer: {
    marginTop: '10px',
    borderRadius: '6px',
    overflow: 'hidden',
    border: '1px solid #333'
  },
  previewImage: {
    width: '100%',
    height: 'auto',
    display: 'block'
  },
  uploadStatus: {
    color: '#eda338',
    fontSize: '0.8rem'
  },
  successStatus: {
    color: '#4caf50',
    fontSize: '0.8rem'
  },
  divider: {
    height: '1px',
    backgroundColor: '#333',
    margin: '0.5rem 0'
  },
  aiCard: {
    backgroundColor: '#1e2022',
    padding: '1rem',
    borderRadius: '8px',
    border: '1px solid #333',
    marginBottom: '0.5rem'
  },
  aiHeader: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: '0.5rem'
  },
  aiTitle: {
    fontWeight: 600,
    color: '#bb86fc',
    fontSize: '0.9rem'
  },
  aiBadge: {
    backgroundColor: 'rgba(187, 134, 252, 0.1)',
    color: '#bb86fc',
    padding: '0.2rem 0.5rem',
    borderRadius: '4px',
    fontSize: '0.75rem'
  },
  aiReason: {
    fontSize: '0.85rem',
    color: '#ccc',
    margin: 0,
    lineHeight: 1.4
  },
  aiOverride: {
    fontSize: '0.8rem',
    color: '#ff9800',
    marginTop: '0.5rem',
    marginBottom: 0
  },
  summaryCard: {
    backgroundColor: '#252526',
    padding: '1.2rem',
    borderRadius: '8px',
    border: '1px solid #444',
    marginTop: '1rem',
    animation: 'fadeIn 0.5s ease-in'
  },
  summaryTitle: {
    margin: '0 0 1rem 0',
    color: '#fff',
    fontSize: '1.1rem',
    textAlign: 'center' as const
  },
  summaryGrid: {
    display: 'grid',
    gridTemplateColumns: '1fr 1fr',
    gap: '1rem',
    marginBottom: '1.5rem'
  },
  summaryItem: {
    display: 'flex',
    flexDirection: 'column' as const,
    gap: '0.2rem'
  },
  summaryLabel: {
    fontSize: '0.8rem',
    color: '#888'
  },
  summaryValue: {
    fontSize: '1rem',
    color: '#fff',
    fontWeight: 600
  },
  actionButtons: {
    display: 'flex',
    flexDirection: 'column' as const,
    gap: '0.8rem'
  },
  primaryButton: {
    width: '100%',
    padding: '0.9rem',
    borderRadius: '6px',
    border: 'none',
    backgroundColor: '#fff',
    color: '#000',
    fontSize: '0.95rem',
    fontWeight: 700,
    cursor: 'pointer'
  },
  secondaryButton: {
    width: '100%',
    padding: '0.8rem',
    borderRadius: '6px',
    border: '1px solid #555',
    backgroundColor: 'transparent',
    color: '#ccc',
    fontSize: '0.9rem',
    cursor: 'pointer'
  },
  disclaimer: {
    fontSize: '0.75rem',
    color: '#555',
    textAlign: 'center' as const,
    marginTop: '1rem'
  }
};
