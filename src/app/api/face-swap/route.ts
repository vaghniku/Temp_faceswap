import { NextRequest, NextResponse } from "next/server";
import { exec } from "child_process";
import { writeFile } from "fs/promises";
import path from "path";
import { v4 as uuidv4 } from "uuid";

export async function POST(request: NextRequest) {
  try {
    const formData = await request.formData();
    const sourceFile = formData.get("sourceImage") as File;
    const targetFile = formData.get("targetImage") as File;

    if (!sourceFile || !targetFile) {
      return NextResponse.json(
        { error: "Source and target images are required" },
        { status: 400 },
      );
    }

    // Create unique filenames
    const sourceFileName = `source-${uuidv4()}${path.extname(sourceFile.name)}`;
    const targetFileName = `target-${uuidv4()}${path.extname(targetFile.name)}`;
    const outputFileName = `output-${uuidv4()}.jpg`;

    // Define file paths
    const uploadsDir = path.join(process.cwd(), "uploads");
    const sourcePath = path.join(uploadsDir, sourceFileName);
    const targetPath = path.join(uploadsDir, targetFileName);
    const outputPath = path.join(uploadsDir, outputFileName);

    // Save uploaded files
    await writeFile(sourcePath, Buffer.from(await sourceFile.arrayBuffer()));
    await writeFile(targetPath, Buffer.from(await targetFile.arrayBuffer()));

    // Get blend strength and face alignment from form data (if provided)
    const blendStrength = formData.get("blendStrength") || "50";
    const faceAlignment = formData.get("faceAlignment") || "50";

    // Execute Python script with parameters
    return new Promise((resolve) => {
      // Use python3 command which is more commonly available
      exec(
        `python3 face_swap.py --source ${sourcePath} --target ${targetPath} --output ${outputPath} --blend ${blendStrength} --alignment ${faceAlignment}`,
        (error, stdout, stderr) => {
          if (error) {
            console.error(`Error: ${error.message}`);
            console.error(`stderr: ${stderr}`);
            resolve(
              NextResponse.json(
                { error: "Face swap processing failed" },
                { status: 500 },
              ),
            );
            return;
          }

          // Return the path to the processed image
          resolve(
            NextResponse.json({
              success: true,
              resultImage: `/uploads/${outputFileName}`,
              message: stdout,
            }),
          );
        },
      );
    });
  } catch (error) {
    console.error("API error:", error);
    return NextResponse.json(
      { error: "Internal server error" },
      { status: 500 },
    );
  }
}
