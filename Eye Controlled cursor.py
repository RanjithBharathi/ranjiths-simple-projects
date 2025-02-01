import cv2
import mediapipe as mp
import pyautogui

# Initialize face mesh with refined landmarks
face_mesh = mp.solutions.face_mesh.FaceMesh(refine_landmarks=True, min_detection_confidence=0.5, min_tracking_confidence=0.5)
screen_w, screen_h = pyautogui.size()  # Get screen dimensions
speed_factor = 1.5  # Adjust to improve movement speed
click_threshold = 0.006  # Adjust for blink detection sensitivity
previous_mouse_x, previous_mouse_y = 0, 0  # Store previous mouse coordinates for smoothing
smooth_factor = 0.5  # Factor for smoothing cursor movement

# Initialize camera capture
icam = cv2.VideoCapture(0)

def smooth_coordinates(new_x, new_y, prev_x, prev_y, smooth_factor):
    """Smooth cursor movement using a weighted average."""
    smoothed_x = int(prev_x * (1 - smooth_factor) + new_x * smooth_factor)
    smoothed_y = int(prev_y * (1 - smooth_factor) + new_y * smooth_factor)
    return smoothed_x, smoothed_y

while True:
    _, frame = icam.read() 
    frame = cv2.flip(frame, 1)  # Flip the frame horizontally
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # Process the frame using MediaPipe Face Mesh
    output = face_mesh.process(rgb_frame)
    landmark_points = output.multi_face_landmarks
    
    # Get frame dimensions
    frame_h, frame_w, _ = frame.shape

    if landmark_points:
        landmarks = landmark_points[0].landmark
        
        # Get coordinates for cursor control (e.g., use eye region landmarks)
        for index, landmark in enumerate(landmarks[474:478]):
            x = int(landmark.x * frame_w)
            y = int(landmark.y * frame_h)
            cv2.circle(frame, (x, y), 3, (0, 255, 0), -1)  # Draw a circle at each landmark
            
            # Control the mouse cursor with one of the eye landmarks
            if index == 1:  # Using landmark 475 (second in this slice)
                screen_x = screen_w / frame_w * x * speed_factor
                screen_y = screen_h / frame_h * y * speed_factor
                
                # Smooth the cursor movement
                smoothed_x, smoothed_y = smooth_coordinates(screen_x, screen_y, previous_mouse_x, previous_mouse_y, smooth_factor)
                pyautogui.moveTo(smoothed_x, smoothed_y)  # Move the cursor
                previous_mouse_x, previous_mouse_y = smoothed_x, smoothed_y  # Update previous coordinates

        # Track specific left-eye landmarks for blink detection
        left_eye_landmarks = [landmarks[145], landmarks[159]]  # Indices for left-eye landmarks
        for landmark in left_eye_landmarks:
            x = int(landmark.x * frame_w)
            y = int(landmark.y * frame_h)
            cv2.circle(frame, (x, y), 3, (0, 255, 255), -1)  # Highlight left-eye landmarks

        # Blink detection for left eye click
        eye_aspect_ratio = left_eye_landmarks[0].y - left_eye_landmarks[1].y  # Calculate eye aspect ratio for blink detection
        if eye_aspect_ratio < click_threshold:  # Check if blink detected
            pyautogui.click()  # Perform a left mouse click
            pyautogui.sleep(1)  # Add a small delay to avoid multiple clicks
    
    # Display the frame
    cv2.imshow('EYE CONTROLLED MOUSE', frame)

    # Break loop on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close all windows
icam.release()
cv2.destroyAllWindows()
