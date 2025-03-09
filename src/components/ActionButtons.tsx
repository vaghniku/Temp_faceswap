"use client";

import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Download, RotateCcw } from "lucide-react";

interface ActionButtonsProps {
  onSwapFaces: () => void;
  onDownload: () => void;
  onReset: () => void;
  isProcessing: boolean;
  hasResult: boolean;
  hasImages: boolean;
}

export default function ActionButtons({
  onSwapFaces,
  onDownload,
  onReset,
  isProcessing = false,
  hasResult = false,
  hasImages = false,
}: ActionButtonsProps) {
  return (
    <Card className="w-full p-6 bg-background">
      <div className="flex flex-wrap gap-4 justify-center md:justify-between">
        <Button
          onClick={onSwapFaces}
          disabled={isProcessing || !hasImages}
          className="min-w-[120px]"
        >
          {isProcessing ? "Processing..." : "Swap Faces"}
        </Button>

        <div className="flex gap-4">
          <Button
            variant="outline"
            onClick={onDownload}
            disabled={!hasResult}
            className="min-w-[120px]"
          >
            <Download className="mr-2 h-4 w-4" />
            Download
          </Button>

          <Button
            variant="destructive"
            onClick={onReset}
            className="min-w-[120px]"
          >
            <RotateCcw className="mr-2 h-4 w-4" />
            Start Over
          </Button>
        </div>
      </div>
    </Card>
  );
}
