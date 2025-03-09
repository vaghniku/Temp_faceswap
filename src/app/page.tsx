"use client";

import ActionButtons from "@/components/ActionButtons";
import AdjustmentControls from "@/components/AdjustmentControls";
import FaceSwapHeader from "@/components/FaceSwapHeader";
import ImageUploadSection from "@/components/ImageUploadSection";
import PreviewSection from "@/components/PreviewSection";
import { useState } from "react";

export default function Page() {
  const [sourceFile, setSourceFile] = useState<File | null>(null);
  const [targetFile, setTargetFile] = useState<File | null>(null);
  const [sourcePreview, setSourcePreview] = useState<string | undefined>();
  const [targetPreview, setTargetPreview] = useState<string | undefined>();
  const [resultImage, setResultImage] = useState<string | undefined>();
  const [isProcessing, setIsProcessing] = useState(false);
  const [blendStrength, setBlendStrength] = useState(50);
  const [faceAlignment, setFaceAlignment] = useState(50);

  const handleSourceImageSelected = (file: File) => {
    setSourceFile(file);
    const reader = new FileReader();
    reader.onload = (e) => {
      setSourcePreview(e.target?.result as string);
    };
    reader.readAsDataURL(file);
  };

  const handleTargetImageSelected = (file: File) => {
    setTargetFile(file);
    const reader = new FileReader();
    reader.onload = (e) => {
      setTargetPreview(e.target?.result as string);
    };
    reader.readAsDataURL(file);
  };

  const handleSwapFaces = async () => {
    if (!sourceFile || !targetFile) {
      alert("Please select both source and target images");
      return;
    }

    setIsProcessing(true);
    setResultImage(undefined);

    try {
      // Create form data to send to the API
      const formData = new FormData();
      formData.append("sourceImage", sourceFile);
      formData.append("targetImage", targetFile);
      formData.append("blendStrength", blendStrength.toString());
      formData.append("faceAlignment", faceAlignment.toString());

      // Call the API endpoint
      const response = await fetch("/api/face-swap", {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || "Failed to process images");
      }

      const data = await response.json();

      // Set the result image from the API response
      // Add a timestamp to prevent caching
      setResultImage(`${data.resultImage}?t=${new Date().getTime()}`);
    } catch (error) {
      console.error("Error processing images:", error);
      alert(
        "An error occurred while processing the images: " +
          (error instanceof Error ? error.message : String(error)),
      );
    } finally {
      setIsProcessing(false);
    }
  };

  const handleDownload = () => {
    if (!resultImage) return;

    // Create a temporary link element
    const link = document.createElement("a");
    link.href = resultImage;
    link.download = "face-swap-result.jpg";
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  const handleReset = () => {
    setSourceFile(null);
    setTargetFile(null);
    setSourcePreview(undefined);
    setTargetPreview(undefined);
    setResultImage(undefined);
    setBlendStrength(50);
    setFaceAlignment(50);
  };

  return (
    <div className="min-h-screen bg-background">
      <FaceSwapHeader />
      <main className="container mx-auto py-8 space-y-8">
        <ImageUploadSection
          onSourceImageSelected={handleSourceImageSelected}
          onTargetImageSelected={handleTargetImageSelected}
          sourceImage={sourcePreview}
          targetImage={targetPreview}
        />

        <PreviewSection
          sourceImage={sourcePreview}
          targetImage={targetPreview}
          resultImage={resultImage}
          isProcessing={isProcessing}
        />

        <AdjustmentControls
          blendStrength={blendStrength}
          faceAlignment={faceAlignment}
          onBlendStrengthChange={setBlendStrength}
          onFaceAlignmentChange={setFaceAlignment}
          disabled={!resultImage}
        />

        <ActionButtons
          onSwapFaces={handleSwapFaces}
          onDownload={handleDownload}
          onReset={handleReset}
          isProcessing={isProcessing}
          hasResult={!!resultImage}
          hasImages={!!sourceFile && !!targetFile}
        />
      </main>
    </div>
  );
}
