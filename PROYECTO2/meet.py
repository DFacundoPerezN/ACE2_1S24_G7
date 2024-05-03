import pyautogui
import time

import webbrowser

def newMeet():
    xReunion = 230
    yReunion = 700
    #Abrimos el navegador predilecto y ponemos en el buscador el link de la pagina de meet
    webbrowser.open("https://meet.google.com")
    time.sleep(2)   #esperamos 1.5 segundos
    #Posicionamos el cursor (mouse) en la posicion especificada 
    pyautogui.moveTo(xReunion, yReunion)   #posicion del botón "Reunion Nueva"
    time.sleep(0.4)                   
    pyautogui.click()   #Se realiza un click  
    xIniciar = 300
    yIniciar = 760
    pyautogui.moveTo(xIniciar, yIniciar)   #posicion del botón "Iniciar una llamada ahora"
    time.sleep(0.4)                   
    pyautogui.click()   #Se realiza un click  
    time.sleep(6)   #esperamos 3 segundos
    #Para enviar el mensaje haremos que abra la sección de comentarios con uan combinación de teclas
    pyautogui.hotkey('ctrlleft', 'altleft', 'c')
    time.sleep(1)  
    pyautogui.write('Holis \nBienvenidos, chicos, al Curso Arquitectura de Computadores Y Ensambladores 2')
    pyautogui.press('Enter')

def closeMeet():
    xSalir = 1220
    ySalir = 980
    #Posicionamos el cursor (mouse) en la posicion especificada 
    pyautogui.moveTo(xSalir, ySalir)   #posicion del botón de colgar
    time.sleep(0.4)                   
    pyautogui.click()   #Se realiza un click  
    xIniciar = 1050
    yIniciar = 650
    pyautogui.moveTo(xIniciar, yIniciar)   #posicion del botón "Iniciar una llamada ahora"
    time.sleep(0.4)                   
    pyautogui.click()   #Se realiza un click  

if __name__ == '__main__':
    newMeet()

'''
# Open web browser
pyautogui.press('win')
pyautogui.typewrite('chrome')
pyautogui.press('enter')

# Wait for browser to open
time.sleep(2)

# Type in the meet URL
meet_url = "https://meet.google.com/your-meet-id"
pyautogui.typewrite(meet_url)
pyautogui.press('enter')

# Wait for the meeting to load
time.sleep(5)

# Join the meeting
join_button_location = pyautogui.locateOnScreen('join_button.png')
if join_button_location:
    join_button_center = pyautogui.center(join_button_location)
    pyautogui.click(join_button_center)
else:
    print("Join button not found")

# Wait for the meeting to start
time.sleep(10)

# Close the browser
pyautogui.hotkey('ctrl', 'w')
# Find and click on the microphone button to unmute
microphone_button_location = pyautogui.locateOnScreen('microphone_button.png')
if microphone_button_location:
    microphone_button_center = pyautogui.center(microphone_button_location)
    pyautogui.click(microphone_button_center)
else:
    print("Microphone button not found")

# Find and click on the camera button to start video
camera_button_location = pyautogui.locateOnScreen('camera_button.png')
if camera_button_location:
    camera_button_center = pyautogui.center(camera_button_location)
    pyautogui.click(camera_button_center)
else:
    print("Camera button not found")

# Find and click on the join now button to join the meeting
join_now_button_location = pyautogui.locateOnScreen('join_now_button.png')
if join_now_button_location:
    join_now_button_center = pyautogui.center(join_now_button_location)
    pyautogui.click(join_now_button_center)
else:
    print("Join now button not found")

# Wait for the meeting to continue
time.sleep(30)

# Find and click on the leave meeting button to exit the meeting
leave_meeting_button_location = pyautogui.locateOnScreen('leave_meeting_button.png')
if leave_meeting_button_location:
    leave_meeting_button_center = pyautogui.center(leave_meeting_button_location)
    pyautogui.click(leave_meeting_button_center)
else:
    print("Leave meeting button not found")

# Close the browser
pyautogui.hotkey('ctrl', 'w')'''
