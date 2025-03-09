"use client";

import { Card } from "@/components/ui/card";
import ImagePreview from "./ImagePreview";

interface PreviewSectionProps {
  sourceImage?: string;
  targetImage?: string;
  resultImage?: string;
  isProcessing: boolean;
}

export default function PreviewSection({
  sourceImage,
  targetImage,
  resultImage,
  isProcessing = false,
}: PreviewSectionProps) {
  return (
    <Card className="w-full p-6 bg-background">
      <h2 className="text-2xl font-bold mb-6">Preview</h2>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <ImagePreview title="Source Face" imageSrc={sourceImage} />
        <ImagePreview title="Target Image" imageSrc={targetImage} />
        <ImagePreview
          title="Result"
          imageSrc={resultImage}
          isLoading={isProcessing}
        />
      </div>
    </Card>
  );
}
