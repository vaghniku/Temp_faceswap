import argparse
import cv2
import numpy as np
import face_recognition
from PIL import Image

def face_swap(source_path, target_path, output_path, blend_strength=50, face_alignment=50):
    # Load the source and target images
    source_image = face_recognition.load_image_file(source_path)
    target_image = face_recognition.load_image_file(target_path)
    
    # Convert blend_strength and face_alignment to 0-1 range
    blend_factor = blend_strength / 100.0
    alignment_factor = face_alignment / 100.0
    
    # Find face landmarks in both images
    source_face_landmarks = face_recognition.face_landmarks(source_image)
    target_face_landmarks = face_recognition.face_landmarks(target_image)
    
    # Check if faces were found in both images
    if not source_face_landmarks or not target_face_landmarks:
        print("No faces found in one or both images")
        # Copy target image to output as fallback
        cv2.imwrite(output_path, cv2.cvtColor(target_image, cv2.COLOR_RGB2BGR))
        return
    
    # Convert to OpenCV format
    source_image = cv2.cvtColor(source_image, cv2.COLOR_RGB2BGR)
    target_image = cv2.cvtColor(target_image, cv2.COLOR_RGB2BGR)
    
    # Create mask for the source face
    source_mask = np.zeros(source_image.shape[:2], dtype=np.uint8)
    source_points = np.array([point for feature in source_face_landmarks[0].values() for point in feature], dtype=np.int32)
    cv2.fillConvexPoly(source_mask, source_points, 255)
    
    # Create mask for the target face
    target_mask = np.zeros(target_image.shape[:2], dtype=np.uint8)
    target_points = np.array([point for feature in target_face_landmarks[0].values() for point in feature], dtype=np.int32)
    cv2.fillConvexPoly(target_mask, target_points, 255)
    
    # Find bounding rectangles
    source_rect = cv2.boundingRect(source_points)
    target_rect = cv2.boundingRect(target_points)
    
    # Extract the face regions
    source_face = source_image[source_rect[1]:source_rect[1]+source_rect[3], source_rect[0]:source_rect[0]+source_rect[2]]
    target_face = target_image[target_rect[1]:target_rect[1]+target_rect[3], target_rect[0]:target_rect[0]+target_rect[2]]
    
    # Resize source face to match target face size
    source_face_resized = cv2.resize(source_face, (target_rect[2], target_rect[3]))
    
    # Create a mask for the resized source face
    source_mask_resized = cv2.resize(source_mask[source_rect[1]:source_rect[1]+source_rect[3], source_rect[0]:source_rect[0]+source_rect[2]], (target_rect[2], target_rect[3]))
    
    # Apply face alignment if needed (simplified version)
    if alignment_factor > 0:
        # Apply slight warping based on alignment factor
        rows, cols = source_face_resized.shape[:2]
        warp_factor = alignment_factor * 0.2  # Scale down for subtle effect
        src_points = np.float32([[0, 0], [cols-1, 0], [0, rows-1], [cols-1, rows-1]])
        dst_points = np.float32([[0, 0], [cols-1, 0], [int(warp_factor*cols), rows-1], [cols-1-int(warp_factor*cols), rows-1]])
        warp_mat = cv2.getPerspectiveTransform(src_points, dst_points)
        source_face_resized = cv2.warpPerspective(source_face_resized, warp_mat, (cols, rows))
        source_mask_resized = cv2.warpPerspective(source_mask_resized, warp_mat, (cols, rows))
    
    # Create a copy of the target image for the result
    result_image = target_image.copy()
    
    # Create a mask for seamless cloning
    mask_for_seamless = source_mask_resized.copy()
    
    # Apply color correction to better match the skin tones
    source_face_resized = cv2.addWeighted(source_face_resized, blend_factor, 
                                         target_face, 1-blend_factor, 0)
    
    # Use seamless cloning to blend the faces
    center = (target_rect[0] + target_rect[2]//2, target_rect[1] + target_rect[3]//2)
    result_image = cv2.seamlessClone(source_face_resized, result_image, mask_for_seamless, center, cv2.NORMAL_CLONE)
    
    # Save the result
    cv2.imwrite(output_path, result_image)
    print(f"Face swap completed and saved to {output_path}")

def main():
    parser = argparse.ArgumentParser(description='Face Swap Application')
    parser.add_argument('--source', required=True, help='Path to the source face image')
    parser.add_argument('--target', required=True, help='Path to the target image')
    parser.add_argument('--output', default='output.jpg', help='Path to save the output image')
    parser.add_argument('--blend', type=int, default=50, help='Blend strength (0-100)')
    parser.add_argument('--alignment', type=int, default=50, help='Face alignment (0-100)')
    
    args = parser.parse_args()
    
    face_swap(args.source, args.target, args.output, args.blend, args.alignment)

if __name__ == "__main__":
    main()
