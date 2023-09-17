import cv2
import dlib
import time
from scipy.spatial import distance
from imutils import face_utils

def eye_aspect_ratio(eye):
    A = distance.euclidean(eye[1], eye[5])
    B = distance.euclidean(eye[2], eye[4])
    C = distance.euclidean(eye[0], eye[3])
    ear = (A + B) / (2.0 * C)
    return ear

# Inicializar dlib's face detector y el facial landmark predictor
predictor_path = "shape_predictor_68_face_landmarks.dat"
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(predictor_path)

# Índices para los landmarks de los ojos
(lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
(rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]

cap = cv2.VideoCapture(0)

EAR_THRESHOLD = 0.2
COUNTER = 0
BLINKS = 0
TOTAL_BLINKS = 0
START_TIME = time.time()
LAST_MINUTE_TIME = time.time()
EYES_CLOSED_START = None
MAX_EYES_CLOSED_TIME = 0

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    rects = detector(gray, 0)

    for rect in rects:
        shape = predictor(gray, rect)
        shape = face_utils.shape_to_np(shape)
        leftEye = shape[lStart:lEnd]
        rightEye = shape[rStart:rEnd]
        
        # Dibujar recuadros alrededor de los ojos
        leftEyeHull = cv2.convexHull(leftEye)
        (x, y, w, h) = cv2.boundingRect(leftEyeHull)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 1)

        rightEyeHull = cv2.convexHull(rightEye)
        (x, y, w, h) = cv2.boundingRect(rightEyeHull)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 1)
        
        # Continuar con la detección de parpadeos
        leftEAR = eye_aspect_ratio(leftEye)
        rightEAR = eye_aspect_ratio(rightEye)
        ear = (leftEAR + rightEAR) / 2.0
        
        if ear < EAR_THRESHOLD:
            COUNTER += 1
            if EYES_CLOSED_START is None:
                EYES_CLOSED_START = time.time()
                
            current_closed_duration = time.time() - EYES_CLOSED_START
            cv2.putText(frame, f"Eyes closed for: {current_closed_duration:.2f} seconds", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        else:
            if EYES_CLOSED_START is not None:
                eyes_closed_duration = time.time() - EYES_CLOSED_START
                MAX_EYES_CLOSED_TIME = max(MAX_EYES_CLOSED_TIME, eyes_closed_duration)
                EYES_CLOSED_START = None

            if COUNTER >= 3:
                BLINKS += 1
                TOTAL_BLINKS += 1
                COUNTER = 0

    elapsed_time = time.time() - START_TIME
    BPS = BLINKS / elapsed_time
    BPM = (TOTAL_BLINKS / (elapsed_time / 60))

    if time.time() - LAST_MINUTE_TIME >= 60:
        BLINKS = 0
        LAST_MINUTE_TIME = time.time()

    info1 = f"Total Parpadeos: {TOTAL_BLINKS} - Parpadeos por minuto: {BPM:.2f}"
    info2 = f"PxS: {BPS:.2f} - Maximo tiempo ojos cerrados: {MAX_EYES_CLOSED_TIME:.2f} s"

    cv2.putText(frame, info1, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
    cv2.putText(frame, info2, (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
    
    cv2.imshow("Frame", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
