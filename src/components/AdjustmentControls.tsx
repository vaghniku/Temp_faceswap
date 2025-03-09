"use client";

import { Card } from "@/components/ui/card";
import { Label } from "@/components/ui/label";
import { Slider } from "@/components/ui/slider";

interface AdjustmentControlsProps {
  blendStrength: number;
  faceAlignment: number;
  onBlendStrengthChange: (value: number) => void;
  onFaceAlignmentChange: (value: number) => void;
  disabled?: boolean;
}

export default function AdjustmentControls({
  blendStrength = 50,
  faceAlignment = 50,
  onBlendStrengthChange,
  onFaceAlignmentChange,
  disabled = true,
}: AdjustmentControlsProps) {
  return (
    <Card className="w-full p-6 bg-background">
      <h2 className="text-2xl font-bold mb-6">Adjustment Controls</h2>
      <div className="space-y-6">
        <div className="space-y-2">
          <div className="flex justify-between">
            <Label htmlFor="blend-strength">Blend Strength</Label>
            <span className="text-sm text-muted-foreground">
              {blendStrength}%
            </span>
          </div>
          <Slider
            id="blend-strength"
            min={0}
            max={100}
            step={1}
            value={[blendStrength]}
            onValueChange={(values) => onBlendStrengthChange(values[0])}
            disabled={disabled}
          />
        </div>

        <div className="space-y-2">
          <div className="flex justify-between">
            <Label htmlFor="face-alignment">Face Alignment</Label>
            <span className="text-sm text-muted-foreground">
              {faceAlignment}%
            </span>
          </div>
          <Slider
            id="face-alignment"
            min={0}
            max={100}
            step={1}
            value={[faceAlignment]}
            onValueChange={(values) => onFaceAlignmentChange(values[0])}
            disabled={disabled}
          />
        </div>
      </div>
    </Card>
  );
}
