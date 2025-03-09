import cv2
import numpy as np
import face_recognition
import os
import argparse

def face_swap(source_image_path, target_image_path, output_path=None):
    # Load the source and target images
    source_image = face_recognition.load_image_file(source_image_path)
    target_image = face_recognition.load_image_file(target_image_path)
    
    # Convert images to RGB (face_recognition uses RGB, OpenCV uses BGR)
    source_image_rgb = cv2.cvtColor(source_image, cv2.COLOR_BGR2RGB)
    target_image_rgb = cv2.cvtColor(target_image, cv2.COLOR_BGR2RGB)
    
    # Find face landmarks in both images
    source_face_landmarks = face_recognition.face_landmarks(source_image)
    target_face_landmarks = face_recognition.face_landmarks(target_image)
    
    if not source_face_landmarks or not target_face_landmarks:
        print("No faces detected in one or both images.")
        return None
    
    # Get the first face from each image
    source_landmarks = source_face_landmarks[0]
    target_landmarks = target_face_landmarks[0]
    
    # Create mask for the source face
    source_face_points = np.array([point for feature in source_landmarks.values() for point in feature], dtype=np.int32)
    source_face_hull = cv2.convexHull(source_face_points)
    source_mask = np.zeros(source_image.shape[:2], dtype=np.uint8)
    cv2.fillConvexPoly(source_mask, source_face_hull, 255)
    
    # Create mask for the target face
    target_face_points = np.array([point for feature in target_landmarks.values() for point in feature], dtype=np.int32)
    target_face_hull = cv2.convexHull(target_face_points)
    target_mask = np.zeros(target_image.shape[:2], dtype=np.uint8)
    cv2.fillConvexPoly(target_mask, target_face_hull, 255)
    
    # Find the center of the target face
    target_face_center = np.mean(target_face_points, axis=0).astype(np.int32)
    
    # Calculate the bounding rectangle of the target face
    x, y, w, h = cv2.boundingRect(target_face_hull)
    
    # Find the center of the source face
    source_face_center = np.mean(source_face_points, axis=0).astype(np.int32)
    
    # Calculate the transformation matrix
    source_points = np.array([source_face_points[0], source_face_points[len(source_face_points)//3], 
                             source_face_points[2*len(source_face_points)//3]], dtype=np.float32)
    target_points = np.array([target_face_points[0], target_face_points[len(target_face_points)//3], 
                             target_face_points[2*len(target_face_points)//3]], dtype=np.float32)
    
    # Get the transformation matrix
    transformation_matrix = cv2.getAffineTransform(source_points, target_points)
    
    # Warp the source image to match the target face
    warped_source = cv2.warpAffine(source_image_rgb, transformation_matrix, 
                                  (target_image.shape[1], target_image.shape[0]), 
                                  borderMode=cv2.BORDER_REFLECT_101)
    
    # Create a mask for the warped source face
    warped_mask = cv2.warpAffine(source_mask, transformation_matrix, 
                               (target_image.shape[1], target_image.shape[0]), 
                               borderMode=cv2.BORDER_REFLECT_101)
    
    # Combine the masks
    combined_mask = cv2.bitwise_and(warped_mask, target_mask)
    
    # Create the output image
    output_image = target_image_rgb.copy()
    
    # Apply seamless cloning
    output_image = cv2.seamlessClone(warped_source, output_image, combined_mask, 
                                    tuple(target_face_center), cv2.NORMAL_CLONE)
    
    # Convert back to BGR for OpenCV
    output_image = cv2.cvtColor(output_image, cv2.COLOR_RGB2BGR)
    
    # Save the output image if a path is provided
    if output_path:
        cv2.imwrite(output_path, output_image)
        print(f"Face-swapped image saved to {output_path}")
    
    return output_image

def main():
    parser = argparse.ArgumentParser(description='Face Swap Application')
    parser.add_argument('--source', required=True, help='Path to the source face image')
    parser.add_argument('--target', required=True, help='Path to the target image')
    parser.add_argument('--output', default='output.jpg', help='Path to save the output image')
    parser.add_argument('--blend', type=int, default=50, help='Blend strength (0-100)')
    parser.add_argument('--alignment', type=int, default=50, help='Face alignment (0-100)')
    
    args = parser.parse_args()
    
    result = face_swap(args.source, args.target, args.output)
    
    if result is not None:
        # Display the result
        cv2.imshow('Face Swap Result', result)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
