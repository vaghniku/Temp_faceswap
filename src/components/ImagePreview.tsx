"use client";

import { Card } from "@/components/ui/card";
import Image from "next/image";

interface ImagePreviewProps {
  title: string;
  imageSrc?: string;
  isLoading?: boolean;
}

export default function ImagePreview({
  title,
  imageSrc,
  isLoading = false,
}: ImagePreviewProps) {
  return (
    <Card className="w-full h-full flex flex-col items-center p-4 bg-background">
      <div className="text-lg font-medium mb-2">{title}</div>
      <div className="relative w-full h-[250px] flex items-center justify-center">
        {isLoading ? (
          <div className="animate-pulse flex flex-col items-center justify-center">
            <div className="h-32 w-32 rounded-full bg-muted mb-4"></div>
            <div className="h-4 w-32 bg-muted rounded"></div>
          </div>
        ) : imageSrc ? (
          <Image src={imageSrc} alt={title} fill className="object-contain" />
        ) : (
          <div className="flex items-center justify-center w-full h-full border-2 border-dashed border-muted-foreground rounded-md">
            <p className="text-sm text-muted-foreground">No image to display</p>
          </div>
        )}
      </div>
    </Card>
  );
}
