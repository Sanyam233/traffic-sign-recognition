import { useState } from "react";
import "./App.css";
import axios from "axios";
import type { PredictionResult } from "./types/app";
import { getConfidenceColorClass } from "./utils/confidence";

function App() {
  const [image, setImage] = useState<string>("");
  const [result, setResult] = useState<PredictionResult | null>(null);
  const allowedImageTypes = ["image/jpeg", "image/png"];

  const handleImageUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;
    if (!allowedImageTypes.includes(file.type)) {
      return;
    }

    const imgUrl = URL.createObjectURL(file);
    setImage(imgUrl);

    const formData = new FormData();
    formData.append("image", file);

    try {
      const response = await axios.post(
        `${import.meta.env.VITE_SERVER_URL}/api/v1/image/classify`,
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        }
      );

      const data = response?.data?.rows?.[0];
      setResult(data);
    } catch (err) {
      if (axios.isAxiosError(err)) {
        console.error("Axios error:", err.response?.data);
      } else {
        console.error("Unexpected error:", err);
      }
    }
  };

  const confidenceClass = getConfidenceColorClass(result?.confidence);

  return (
    <>
      <h1>Traffic Sign Classifier</h1>
      <div className="home-container">
        <h3>
          Prediction:{" "}
          <span className={confidenceClass}>{result?.predictedLabel}</span>
        </h3>
        <h3>
          Confidence:{" "}
          <span className={confidenceClass}>{result?.confidence}</span>
        </h3>
        <div className="preview-image-container">
          {image && (
            <img src={image} alt="Uploaded Preview" className="preview-image" />
          )}
        </div>
        <input
          type="file"
          accept={allowedImageTypes.join(",")}
          onChange={handleImageUpload}
        />
      </div>
    </>
  );
}

export default App;
