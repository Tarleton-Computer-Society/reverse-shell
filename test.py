import pyautogui
import cv2
import sounddevice as sd
from scipy.io.wavfile import write
import sounddevice as sd
import soundfile as sf
import wavio as wv
def screenshot(filename):
    filen = pyautogui.screenshot()
    filen.save(f'{filename}.png')
    
    
def takpic(filename):
 

    cap = cv2.VideoCapture(0) # video capture source camera (Here webcam of laptop) 
    ret,frame = cap.read() # return a single frame in variable `frame`
    
    while(True):
        cv2.imshow('img1',frame) #display the captured image
        if cv2.waitKey(1) & 0xFF == ord('y'): #save on pressing 'y' 
            cv2.imwrite(f'{filename}.png',frame)
            cv2.destroyAllWindows()
            break

    cap.release()
    
def recordaudio(filename,duration):
 

    samplerate = 44100  # Hertz
    seconds = duration
    filename = f'{filename}.wav'
    
    myrecording = sd.rec(int(seconds * samplerate), samplerate=samplerate,
                         channels=1)
    sd.wait()
    sf.write(filename, myrecording, samplerate)
    
   
    
recordaudio("testaudi",6) 