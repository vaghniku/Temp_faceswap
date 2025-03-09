import tkinter as tk
from tkinter import filedialog, ttk
import cv2
import numpy as np
import face_recognition
import os
from PIL import Image, ImageTk
import threading

class FaceSwapApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Face Swap Application")
        self.root.geometry("800x600")
        self.root.configure(bg="#f0f0f0")
        
        self.source_image_path = None
        self.target_image_path = None
        self.result_image = None
        
        self.create_widgets()
    
    def create_widgets(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding=10)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = ttk.Label(main_frame, text="Face Swap Application", font=("Arial", 18, "bold"))
        title_label.pack(pady=10)
        
        # Image selection frame
        selection_frame = ttk.Frame(main_frame)
        selection_frame.pack(fill=tk.X, pady=10)
        
        # Source image selection
        source_frame = ttk.LabelFrame(selection_frame, text="Source Face")
        source_frame.pack(side=tk.LEFT, padx=10, fill=tk.BOTH, expand=True)
        
        self.source_canvas = tk.Canvas(source_frame, width=200, height=200, bg="#e0e0e0")
        self.source_canvas.pack(pady=5)
        
        source_button = ttk.Button(source_frame, text="Select Source Face", command=self.select_source_image)
        source_button.pack(pady=5)
        
        # Target image selection
        target_frame = ttk.LabelFrame(selection_frame, text="Target Image")
        target_frame.pack(side=tk.RIGHT, padx=10, fill=tk.BOTH, expand=True)
        
        self.target_canvas = tk.Canvas(target_frame, width=200, height=200, bg="#e0e0e0")
        self.target_canvas.pack(pady=5)
        
        target_button = ttk.Button(target_frame, text="Select Target Image", command=self.select_target_image)
        target_button.pack(pady=5)
        
        # Process button
        self.process_button = ttk.Button(main_frame, text="Swap Faces", command=self.process_images, state=tk.DISABLED)
        self.process_button.pack(pady=10)
        
        # Progress bar
        self.progress = ttk.Progressbar(main_frame, orient=tk.HORIZONTAL, length=300, mode='indeterminate')
        self.progress.pack(pady=5)
        
        # Result frame
        result_frame = ttk.LabelFrame(main_frame, text="Result")
        result_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        self.result_canvas = tk.Canvas(result_frame, bg="#e0e0e0")
        self.result_canvas.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Action buttons
        action_frame = ttk.Frame(main_frame)
        action_frame.pack(fill=tk.X, pady=10)
        
        self.save_button = ttk.Button(action_frame, text="Save Result", command=self.save_result, state=tk.DISABLED)
        self.save_button.pack(side=tk.LEFT, padx=10)
        
        reset_button = ttk.Button(action_frame, text="Reset", command=self.reset)
        reset_button.pack(side=tk.RIGHT, padx=10)
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        status_bar = ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def select_source_image(self):
        file_path = filedialog.askopenfilename(title="Select Source Face Image", 
                                             filetypes=[("Image files", "*.jpg;*.jpeg;*.png")])
        if file_path:
            self.source_image_path = file_path
            self.display_image(file_path, self.source_canvas)
            self.check_process_button()
            self.status_var.set(f"Source image selected: {os.path.basename(file_path)}")
    
    def select_target_image(self):
        file_path = filedialog.askopenfilename(title="Select Target Image", 
                                             filetypes=[("Image files", "*.jpg;*.jpeg;*.png")])
        if file_path:
            self.target_image_path = file_path
            self.display_image(file_path, self.target_canvas)
            self.check_process_button()
            self.status_var.set(f"Target image selected: {os.path.basename(file_path)}")
    
    def display_image(self, image_path, canvas):
        img = Image.open(image_path)
        canvas_width = canvas.winfo_width() or 200
        canvas_height = canvas.winfo_height() or 200
        
        # Resize image to fit canvas while maintaining aspect ratio
        img.thumbnail((canvas_width, canvas_height))
        
        photo = ImageTk.PhotoImage(img)
        canvas.config(width=img.width, height=img.height)
        canvas.create_image(0, 0, anchor=tk.NW, image=photo)
        canvas.image = photo  # Keep a reference to prevent garbage collection
    
    def check_process_button(self):
        if self.source_image_path and self.target_image_path:
            self.process_button.config(state=tk.NORMAL)
        else:
            self.process_button.config(state=tk.DISABLED)
    
    def process_images(self):
        self.progress.start()
        self.status_var.set("Processing images...")
        self.process_button.config(state=tk.DISABLED)
        
        # Run face swap in a separate thread to avoid freezing the UI
        threading.Thread(target=self.run_face_swap).start()
    
    def run_face_swap(self):
        try:
            # Load the source and target images
            source_image = face_recognition.load_image_file(self.source_image_path)
            target_image = face_recognition.load_image_file(self.target_image_path)
            
            # Convert images to RGB (face_recognition uses RGB, OpenCV uses BGR)
            source_image_rgb = cv2.cvtColor(source_image, cv2.COLOR_BGR2RGB)
            target_image_rgb = cv2.cvtColor(target_image, cv2.COLOR_BGR2RGB)
            
            # Find face landmarks in both images
            source_face_landmarks = face_recognition.face_landmarks(source_image)
            target_face_landmarks = face_recognition.face_landmarks(target_image)
            
            if not source_face_landmarks or not target_face_landmarks:
                self.root.after(0, lambda: self.status_var.set("No faces detected in one or both images."))
                self.root.after(0, self.progress.stop)
                return
            
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
            
            # Convert the result to PIL format for display
            self.result_image = cv2.cvtColor(output_image, cv2.COLOR_RGB2BGR)
            
            # Update UI in the main thread
            self.root.after(0, self.display_result)
            
        except Exception as e:
            self.root.after(0, lambda: self.status_var.set(f"Error: {str(e)}"))
            self.root.after(0, self.progress.stop)
    
    def display_result(self):
        # Convert OpenCV image to PIL format
        result_pil = Image.fromarray(cv2.cvtColor(self.result_image, cv2.COLOR_BGR2RGB))
        
        # Resize to fit canvas
        canvas_width = self.result_canvas.winfo_width()
        canvas_height = self.result_canvas.winfo_height()
        
        if canvas_width > 1 and canvas_height > 1:  # Ensure canvas has been drawn
            # Resize image to fit canvas while maintaining aspect ratio
            result_pil.thumbnail((canvas_width, canvas_height))
            
            # Display on canvas
            photo = ImageTk.PhotoImage(result_pil)
            self.result_canvas.config(width=result_pil.width, height=result_pil.height)
            self.result_canvas.create_image(0, 0, anchor=tk.NW, image=photo)
            self.result_canvas.image = photo  # Keep a reference
            
            # Update UI
            self.save_button.config(state=tk.NORMAL)
            self.status_var.set("Face swap completed successfully!")
        else:
            # If canvas not ready, try again after a short delay
            self.root.after(100, self.display_result)
        
        self.progress.stop()
        self.process_button.config(state=tk.NORMAL)
    
    def save_result(self):
        if self.result_image is not None:
            file_path = filedialog.asksaveasfilename(defaultextension=".jpg", 
                                                   filetypes=[("JPEG files", "*.jpg"), ("All files", "*.*")])
            if file_path:
                cv2.imwrite(file_path, self.result_image)
                self.status_var.set(f"Result saved to {file_path}")
    
    def reset(self):
        self.source_image_path = None
        self.target_image_path = None
        self.result_image = None
        
        self.source_canvas.delete("all")
        self.target_canvas.delete("all")
        self.result_canvas.delete("all")
        
        self.process_button.config(state=tk.DISABLED)
        self.save_button.config(state=tk.DISABLED)
        
        self.status_var.set("Ready")

if __name__ == "__main__":
    root = tk.Tk()
    app = FaceSwapApp(root)
    root.mainloop()
