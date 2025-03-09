"use client";

import { Card } from "@/components/ui/card";
import ImageUploader from "./ImageUploader";

interface ImageUploadSectionProps {
  onSourceImageSelected: (file: File) => void;
  onTargetImageSelected: (file: File) => void;
  sourceImage?: string;
  targetImage?: string;
}

export default function ImageUploadSection({
  onSourceImageSelected,
  onTargetImageSelected,
  sourceImage,
  targetImage,
}: ImageUploadSectionProps) {
  return (
    <Card className="w-full p-6 bg-background">
      <h2 className="text-2xl font-bold mb-6">Upload Images</h2>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <ImageUploader
          title="Source Face"
          onImageSelected={onSourceImageSelected}
          selectedImage={sourceImage}
        />
        <ImageUploader
          title="Target Image"
          onImageSelected={onTargetImageSelected}
          selectedImage={targetImage}
        />
      </div>
    </Card>
  );
}
