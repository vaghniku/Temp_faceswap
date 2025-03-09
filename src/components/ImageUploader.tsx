"use client";

import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Upload } from "lucide-react";
import Image from "next/image";
import { useCallback, useState } from "react";

interface ImageUploaderProps {
  title: string;
  onImageSelected: (file: File) => void;
  selectedImage?: string;
}

export default function ImageUploader({
  title = "Upload Image",
  onImageSelected,
  selectedImage,
}: ImageUploaderProps) {
  const [isDragging, setIsDragging] = useState(false);
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);

  const handleDragOver = useCallback((e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    setIsDragging(true);
  }, []);

  const handleDragLeave = useCallback(() => {
    setIsDragging(false);
  }, []);

  const handleDrop = useCallback(
    (e: React.DragEvent<HTMLDivElement>) => {
      e.preventDefault();
      setIsDragging(false);

      if (e.dataTransfer.files && e.dataTransfer.files[0]) {
        const file = e.dataTransfer.files[0];
        handleFile(file);
      }
    },
    [onImageSelected],
  );

  const handleFileInput = useCallback(
    (e: React.ChangeEvent<HTMLInputElement>) => {
      if (e.target.files && e.target.files[0]) {
        const file = e.target.files[0];
        handleFile(file);
      }
    },
    [onImageSelected],
  );

  const handleFile = (file: File) => {
    // Check if file is an image
    if (!file.type.match(/image.*/)) {
      alert("Please select an image file");
      return;
    }

    // Create preview URL
    const reader = new FileReader();
    reader.onload = (e) => {
      if (e.target?.result) {
        setPreviewUrl(e.target.result as string);
      }
    };
    reader.readAsDataURL(file);

    // Pass file to parent component
    onImageSelected(file);
  };

  return (
    <Card
      className={`w-full h-full flex flex-col items-center justify-center p-4 ${
        isDragging ? "border-primary border-2" : ""
      }`}
      onDragOver={handleDragOver}
      onDragLeave={handleDragLeave}
      onDrop={handleDrop}
    >
      <div className="text-lg font-medium mb-2">{title}</div>

      {previewUrl || selectedImage ? (
        <div className="relative w-full h-[150px] mb-4">
          <Image
            src={previewUrl || selectedImage || ""}
            alt="Preview"
            fill
            className="object-contain"
          />
        </div>
      ) : (
        <div className="flex flex-col items-center justify-center w-full h-[150px] border-2 border-dashed border-muted-foreground rounded-md mb-4">
          <Upload className="h-10 w-10 text-muted-foreground mb-2" />
          <p className="text-sm text-muted-foreground">
            Drag & drop or click to upload
          </p>
        </div>
      )}

      <div className="flex justify-center w-full">
        <Button
          variant="outline"
          onClick={() =>
            document.getElementById(`file-input-${title}`)?.click()
          }
        >
          Select Image
        </Button>
        <input
          id={`file-input-${title}`}
          type="file"
          accept="image/*"
          className="hidden"
          onChange={handleFileInput}
        />
      </div>
    </Card>
  );
}
