import tkinter as tk
import pymem, pymem.process
import win32gui
import win32con
import imgui
from imgui.integrations.glfw import GlfwRenderer
import glfw
import OpenGL.GL as gl
from requests import get
import os
import colorama
import time
import pygetwindow as gw
import keyboard
import threading
from pynput.mouse import Controller, Button
from win32gui import GetWindowText, GetForegroundWindow
import ctypes
import win32api
import win32con
triggerbotdelay = 0.008
ScreenY = 1920
ScreenX = 1080

GunControl = 2
MaxEntityRead = 64
canshoot = False
canbuy = False
isscoped = False
recoilcan = False
watermark = True
defusecheck = False
healthcheck = False
listener_threadee = False
gui_visible = False
isgui = False
color = 1
aimboter = False
def leftclick():
    return win32api.GetKeyState(win32con.VK_LBUTTON) < 0
def toggle_gui_visibility():
    global gui_visible
    if gui_visible:
        root.withdraw()  # Hide the Tkinter GUI
        gui_visible = False
    else:
        root.deiconify()  # Show the Tkinter GUI
        gui_visible = True

def on_delete_key(event):
    global isgui
    if isgui == True:
       toggle_gui_visibility()

def listen_for_delete_key():
    keyboard.on_press_key("home", on_delete_key)
    keyboard.wait("esc")  # This will block only this thread

listener_thread = threading.Thread(target=listen_for_delete_key)
listener_thread.daemon = True  # This makes sure the thread will close when the main program exits
listener_thread.start()






def setconsolestatus():
    os.system("cls")
    print(colorama.Fore.MAGENTA + "]-----------------[GHOST]------------------[" + colorama.Fore.WHITE)
    print(colorama.Fore.GREEN + "[GHOST] [SYSTEM-BYPASSER] [UNDETECTED]" + colorama.Fore.WHITE)
    print(colorama.Fore.LIGHTBLACK_EX + "[GHOST] [SYSTEM-VERSION] [V-2]" + colorama.Fore.WHITE)

def is_cs2_window_active():
    active_window = gw.getActiveWindow()
    
    if active_window is not None:
        title = active_window.title
        if "Counter-Strike 2" in title:
            return True
    return False




skelly = False
tracer = False
box = False
teamchecky = False
offsets = get('https://raw.githubusercontent.com/a2x/cs2-dumper/main/output/offsets.json').json()
client_dll = get('https://raw.githubusercontent.com/a2x/cs2-dumper/main/output/client.dll.json').json()
dwEntityList = offsets["client.dll"]["dwEntityList"]

dwLocalPlayerPawn = offsets["client.dll"]["dwLocalPlayerPawn"]

dwViewMatrix = offsets["client.dll"]["dwViewMatrix"]

m_iTeamNum = client_dll['client.dll']['classes']['C_BaseEntity']['fields']['m_iTeamNum']

m_lifeState = client_dll['client.dll']['classes']['C_BaseEntity']['fields']['m_lifeState']

m_pGameSceneNode = client_dll['client.dll']['classes']['C_BaseEntity']['fields']['m_pGameSceneNode']

m_modelState = client_dll['client.dll']['classes']['CSkeletonInstance']['fields']['m_modelState']

m_hPlayerPawn = client_dll['client.dll']['classes']['CCSPlayerController']['fields']['m_hPlayerPawn']

m_iIDEntIndex = client_dll["client.dll"]["classes"]["C_CSPlayerPawnBase"]["fields"]["m_iIDEntIndex"]
m_bIsDefusing = client_dll['client.dll']['classes']['C_CSPlayerPawn']['fields']['m_bIsDefusing']
m_bIsScoped = client_dll['client.dll']['classes']['C_CSPlayerPawn']['fields']['m_bIsScoped']
m_iHealth = client_dll['client.dll']['classes']['C_BaseEntity']['fields']['m_iHealth']
m_iLastBulletUpdate = client_dll['client.dll']['classes']['C_BaseCSGrenadeProjectile']['fields']['vecLastTrailLinePos']
m_vInitialPosition = client_dll['client.dll']['classes']['C_BaseCSGrenadeProjectile']['fields']['m_arrTrajectoryTrailPoints']
m_bIsBuyMenuOpen = m_bIsScoped = client_dll['client.dll']['classes']['C_CSPlayerPawn']['fields']['m_bIsBuyMenuOpen']
m_iShotsFired = client_dll['client.dll']['classes']['C_CSPlayerPawn']['fields']['m_iShotsFired']
os.system("cls")

try:
   pm = pymem.Pymem("cs2.exe")
   setconsolestatus()

except:
    print(colorama.Fore.RED + "[GHOST] [SYSTEM] [ERROR]" + colorama.Fore.WHITE)
    
    

client = pymem.process.module_from_name(pm.process_handle, "client.dll").lpBaseOfDll
mouse = Controller()









def triggerbot():


    while True:
        try:
            if not GetWindowText(GetForegroundWindow()) == "Counter-Strike 2":
                continue
            
            
            if not listener_threadee:
                continue
            player = pm.read_longlong(client + dwLocalPlayerPawn)
            entityId = pm.read_int(player + m_iIDEntIndex)

            if entityId > 0:
                entList = pm.read_longlong(client + dwEntityList)

                entEntry = pm.read_longlong(entList + 0x8 * (entityId >> 9) + 0x10)
                entity = pm.read_longlong(entEntry + 120 * (entityId & 0x1FF))

                entityTeam = pm.read_int(entity + m_iTeamNum)
                playerTeam = pm.read_int(player + m_iTeamNum)
                if entityTeam == playerTeam and teamchecky:
                    continue
                    
                entityHp = pm.read_int(entity + m_iHealth)
                if entityHp > 0:
                    
                  
                    time.sleep(triggerbotdelay)
                    mouse.press(Button.left)
                    
                    time.sleep(triggerbotdelay)
                    mouse.release(Button.left)
                    if recoilcan:
                        ctypes.windll.user32.mouse_event(0x0001, 0, GunControl,0, 0)
                    
                    
                

            time.sleep(triggerbotdelay)
            
        except KeyboardInterrupt:
            break
        except:
            pass



def w2s(mtx, posx, posy, posz, width, height):
    screenW = (mtx[12] * posx) + (mtx[13] * posy) + (mtx[14] * posz) + mtx[15]

    if screenW > 0.001:
        screenX = (mtx[0] * posx) + (mtx[1] * posy) + (mtx[2] * posz) + mtx[3]
        screenY = (mtx[4] * posx) + (mtx[5] * posy) + (mtx[6] * posz) + mtx[7]

        camX = width / 2
        camY = height / 2

        x = camX + (camX * screenX / screenW)//1
        y = camY - (camY * screenY / screenW)//1

        return [x, y]

    return [-999, -999]
def aimbot(head_pos,center_x,center_y):
  
    newx = 0
    newy = 0
    import math
    if not head_pos[0] == 0:
       newx = center_x / head_pos[0]
       newx = math.floor(newx)
       if newx == 0:
       
        newx = 8
       else:
        newx = -8



    if not head_pos[1] == 0:
       newy = center_y /  head_pos[1]
       newy = math.floor(newy)
       if newy == 0:
       
         newy = 10
       else:
         newy = -10

  
    def ifplayerinfovthenlockon():
       
    # Assuming center_x and center_y are defined elsewhere

       ispress = leftclick()  # Assuming leftclick() is defined elsewhere

       if ispress:
         
         ctypes.windll.user32.mouse_event(0x0001, newx - math.floor(head_pos[0] / center_x), newy - math.floor(head_pos[1] / center_y), 0, 0)
    ifplayerinfovthenlockon()
# ESP function



def esp(draw_list):
   
    
        
    view_matrix = read_view_matrix()
    local_player_pawn_addr, local_player_team = get_local_player_info()
    
    if not local_player_pawn_addr:
        return


    for i in range(MaxEntityRead):
        entity_pawn_addr = get_entity_pawn_address(i)
        
        if not entity_pawn_addr or entity_pawn_addr == local_player_pawn_addr:
            continue

        if not is_entity_alive(entity_pawn_addr):
            continue

        entity_team = pm.read_int(entity_pawn_addr + m_iTeamNum)
        
        if entity_team == local_player_team and teamchecky:
            continue
        Hp = pm.read_int(entity_pawn_addr + m_iHealth)
        if not Hp:
             if not Hp > 0:
                continue
         
        
       
        

        draw_entity_esp(draw_list, view_matrix, entity_pawn_addr)


def read_view_matrix():
    return [pm.read_float(client + dwViewMatrix + i * 4) for i in range(MaxEntityRead)]


def get_local_player_info():
    local_player_pawn_addr = pm.read_longlong(client + dwLocalPlayerPawn)
    try:
        local_player_team = pm.read_int(local_player_pawn_addr + m_iTeamNum)
    except:
        return None, None
    return local_player_pawn_addr, local_player_team


def get_entity_pawn_address(index):
    entity = pm.read_longlong(client + dwEntityList)
    
    if not is_cs2_window_active():
        return None
    if not entity:
        return None

    list_entry = pm.read_longlong(entity + ((8 * (index & 0x7FFF) >> 9) + 16))
    if not list_entry:
        return None

    entity_controller = pm.read_longlong(list_entry + (120) * (index & 0x1FF))
    if not entity_controller:
        return None

    entity_controller_pawn = pm.read_longlong(entity_controller + m_hPlayerPawn)
    if not entity_controller_pawn:
        return None

    list_entry = pm.read_longlong(entity + (0x8 * ((entity_controller_pawn & 0x7FFF) >> 9) + 16))
    if not list_entry:
        return None
  
    
        

    return pm.read_longlong(list_entry + (120) * (entity_controller_pawn & 0x1FF))


def is_entity_alive(entity_pawn_addr):
    return pm.read_int(entity_pawn_addr + m_lifeState) == 256


def draw_entity_esp(draw_list, view_matrix, entity_pawn_addr):
    BONE_POSITIONS = {
        "head": 6, "chest": 15, "left_hand": 10,
        "right_hand": 2, "left_leg": 23, "right_leg": 26
    }
    

    game_scene = pm.read_longlong(entity_pawn_addr + m_pGameSceneNode)
    bone_matrix = pm.read_longlong(game_scene + m_modelState + 0x80)

    bone_positions = {}
    try:
        for bone_name, bone_index in BONE_POSITIONS.items():
            base_addr = bone_matrix + bone_index * 0x20
            bone_positions[bone_name] = (
                pm.read_float(base_addr),
                pm.read_float(base_addr + 0x4),
                pm.read_float(base_addr + 0x8)
            )
    except:
        return

    # Get screen positions
    try:
        head_pos = w2s(view_matrix, *bone_positions["head"], ScreenY, ScreenX)
        chest_pos = w2s(view_matrix, *bone_positions["chest"], ScreenY, ScreenX)
        left_hand_pos = w2s(view_matrix, *bone_positions["left_hand"], ScreenY, ScreenX)
        right_hand_pos = w2s(view_matrix, *bone_positions["right_hand"], ScreenY, ScreenX)
        left_leg_pos = w2s(view_matrix, *bone_positions["left_leg"], ScreenY, ScreenX)
        right_leg_pos = w2s(view_matrix, *bone_positions["right_leg"], ScreenY, ScreenX)
    except:
        return

    # Draw ESP
    
    
    
    headX = pm.read_float(bone_matrix + BONE_POSITIONS["head"] * 0x20)
    headY = pm.read_float(bone_matrix + BONE_POSITIONS["head"]  * 0x20 + 0x4)
    headZ = pm.read_float(bone_matrix + BONE_POSITIONS["head"]  * 0x20 + 0x8) 
    head_pos = w2s(view_matrix, headX, headY, headZ, ScreenY, ScreenX)
   

    
    legZ = pm.read_float(bone_matrix + 28 * 0x20 + 0x8)

    leg_pos = w2s(view_matrix, headX, headY, legZ, ScreenY,ScreenX)

    deltaZ = abs(head_pos[1] - leg_pos[1])
    leftXX = head_pos[0] - deltaZ // 3
    rightXX = head_pos[0] + deltaZ // 3
    leftX = head_pos[0] - deltaZ // 4
    rightX = head_pos[0] + deltaZ // 4
   
    
    
    colorr = imgui.get_color_u32_rgba(1, 1, 1, 0.9)
    
    
    
    Hp = pm.read_int(entity_pawn_addr + m_iHealth)
    if defusecheck:
        isdefusing = pm.read_int(entity_pawn_addr + m_bIsDefusing)
        
        if isdefusing and Hp > 0:
           colorr = imgui.get_color_u32_rgba(1, 0.6, 0.1, 1)
        elif color == 1:
             colorr = imgui.get_color_u32_rgba(1, 1, 1, 1)
        elif color == 2:
             colorr = imgui.get_color_u32_rgba(0.6, 0.6, 0.6, 1)
        elif color == 3:
             colorr = imgui.get_color_u32_rgba(0.1, 0.33, 1, 1)
        elif color == 4:
             colorr = imgui.get_color_u32_rgba(1, 0.85, 0.1, 1)
    
    elif color == 1:
        colorr = imgui.get_color_u32_rgba(1, 1, 1, 1)
    elif color == 2:
        colorr = imgui.get_color_u32_rgba(0.65, 0.65, 0.65, 1)
    elif color == 3:
        colorr = imgui.get_color_u32_rgba(0.1, 0.33, 1, 1)
    elif color == 4:
        colorr = imgui.get_color_u32_rgba(1, 0.85, 0.1, 1)
    center_x = ScreenY / 2
    center_y = ScreenX / 2
    
    
    if canbuy:
        BuyMenuOpen = pm.read_int(entity_pawn_addr + m_bIsBuyMenuOpen)
        if BuyMenuOpen:
            colorr = imgui.get_color_u32_rgba(0.1, 1, 0.1, 1)
    if canshoot:
        ShotsFired = pm.read_int(entity_pawn_addr + m_iShotsFired)
        if ShotsFired:
            colorr = imgui.get_color_u32_rgba(1, 0.1, 0.8, 1)
    if isscoped:
        Scope = pm.read_int(entity_pawn_addr + m_bIsScoped)
        if Scope:
             scopecolor = imgui.get_color_u32_rgba(1, 0.1, 0.8, 1)
             draw_list.add_line(rightXX, head_pos[1], rightXX, leg_pos[1], scopecolor, 1)
    
   
    if healthcheck:
        
        healthcolor = imgui.get_color_u32_rgba(0.1, 0.1, 0.1, 0.1)
        if Hp >= 80:
           healthcolor = imgui.get_color_u32_rgba(0.1, 1, 0.1, 1)
        elif Hp >= 40:
            healthcolor = imgui.get_color_u32_rgba(1, 1, 0.1, 1)
        elif Hp > 0:
            healthcolor = imgui.get_color_u32_rgba(1, 0.1, 0.1, 1)
        elif Hp <= 0:
            healthcolor = imgui.get_color_u32_rgba(0.1, 0.1, 0.1, 0.1)
        
        draw_list.add_line(leftXX, head_pos[1], leftXX, leg_pos[1], healthcolor, 1)
    
    

    

    
 

    if aimboter:
      if head_pos[0] / center_x <= 1.0285 and head_pos[0] / center_x >= 0.975 or head_pos[0] / center_x <= 0.975 and head_pos[0] / center_x >= 1.0285:
        if head_pos[1] / center_y <= 1.0285 and head_pos[1] / center_y >= 0.89:
          aimbot(head_pos,center_x,center_y)
         

          
          colorr = imgui.get_color_u32_rgba(1, 0.1, 0.1, 1)
       

    

    
    
   


   
 
    
    
    if tracer:
            
            draw_list.add_line(center_x, center_y, head_pos[0], head_pos[1], colorr, 1)
    if box:
        
        draw_list.add_line(leftX, head_pos[1], rightX, head_pos[1], colorr,1)
        draw_list.add_line(leftX, leg_pos[1], rightX, leg_pos[1], colorr, 1)
        draw_list.add_line(leftX, head_pos[1], leftX, leg_pos[1], colorr, 1)
        draw_list.add_line(rightX, head_pos[1], rightX, leg_pos[1], colorr, 1)
    if skelly:
        draw_list.add_line(chest_pos[0], chest_pos[1],head_pos[0], head_pos[1], colorr, 1)
        draw_list.add_line(chest_pos[0], chest_pos[1], chest_pos[0], chest_pos[1], colorr, 1)
        draw_list.add_line(chest_pos[0], chest_pos[1],right_leg_pos[0], right_leg_pos[1], colorr, 1)
        draw_list.add_line(chest_pos[0], chest_pos[1],left_leg_pos[0], left_leg_pos[1],colorr, 1)
        draw_list.add_line(chest_pos[0], chest_pos[1],right_hand_pos[0], right_hand_pos[1], colorr, 1)
        draw_list.add_line(chest_pos[0], chest_pos[1],left_hand_pos[0], left_hand_pos[1], colorr, 1)
    


               
            


                
            
def main():
   
   
    if not glfw.init():
        print("Could not initialize OpenGL context")
        exit(1)
    glfw.window_hint(glfw.TRANSPARENT_FRAMEBUFFER, glfw.TRUE)
    window = glfw.create_window(ScreenY, ScreenX, "Overlay", None, None)

    hwnd = glfw.get_win32_window(window)

    style = win32gui.GetWindowLong(hwnd, win32con.GWL_STYLE)
    style &= ~(win32con.WS_CAPTION | win32con.WS_THICKFRAME)
    win32gui.SetWindowLong(hwnd, win32con.GWL_STYLE, style)

    ex_style = win32con.WS_EX_TRANSPARENT | win32con.WS_EX_LAYERED
    win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, ex_style)

    win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, -2, -2, 0, 0,
                          win32con.SWP_NOSIZE | win32con.SWP_NOACTIVATE)

    glfw.make_context_current(window)

    imgui.create_context()
    impl = GlfwRenderer(window)

    while not glfw.window_should_close(window):
        glfw.poll_events()
        impl.process_inputs()

        imgui.new_frame()
        imgui.set_next_window_size(ScreenY, ScreenX)
        imgui.set_next_window_position(0, 0)
        imgui.begin("overlay", flags=imgui.WINDOW_NO_TITLE_BAR | imgui.WINDOW_NO_RESIZE | imgui.WINDOW_NO_SCROLLBAR | imgui.WINDOW_NO_COLLAPSE | imgui.WINDOW_NO_BACKGROUND)
        draw_list = imgui.get_window_draw_list()
        
      
        
            
        if watermark:
       
           current_time = time.strftime("%Y-%m-%d", time.localtime())
           imgui.text_colored("Ghost | " + current_time, 0.1,0.1,0.1)
         
           


        esp(draw_list)

        imgui.end()
        imgui.end_frame()

        gl.glClearColor(0, 0, 0, 0)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT)
        
        imgui.render()
        impl.render(imgui.get_draw_data())

        glfw.swap_buffers(window)

    impl.shutdown()
    glfw.terminate()


    

# Function to handle window movement


# Function to close the window

# Function to minimize the window


# Function to create a toggle button

def toggle_button_color1(button):
    current_color = button.cget("bg")
    new_color = 'red'
    global skelly
    if current_color == 'red':
        new_color = 'green'
        
        button.config(bg=new_color, activebackground=new_color)
       
        skelly = True
    else:
         new_color = 'red'
         skelly = False
         button.config(bg=new_color, activebackground=new_color)
        
def toggle_button_color2(button):
    current_color = button.cget("bg")
    new_color = 'red'
    global teamchecky
    if current_color == 'red':
        new_color = 'green'
        
        button.config(bg=new_color, activebackground=new_color)
       
        teamchecky = True
    else:
         new_color = 'red'
         teamchecky = False
         button.config(bg=new_color, activebackground=new_color)
def toggle_button_color99(button):
    current_color = button.cget("bg")
    new_color = 'red'
    global watermark
    if current_color == 'red':
        new_color = 'green'
        
        button.config(bg=new_color, activebackground=new_color)
       
        watermark = True
    else:
         new_color = 'red'
         watermark = False
         button.config(bg=new_color, activebackground=new_color)
def toggle_button_color999(button):
    current_color = button.cget("bg")
    new_color = 'red'
    global defusecheck
    if current_color == 'red':
        new_color = 'green'
        
        button.config(bg=new_color, activebackground=new_color)
       
        defusecheck = True
    else:
         new_color = 'red'
         defusecheck = False
         button.config(bg=new_color, activebackground=new_color)
def toggle_button_color9(button):
    current_color = button.cget("bg")
    new_color = 'red'
    global box
    if current_color == 'red':
        new_color = 'green'
        
        button.config(bg=new_color, activebackground=new_color)
       
        box = True
    else:
         new_color = 'red'
         box = False
         button.config(bg=new_color, activebackground=new_color)
def toggle_button_color92(button):
    current_color = button.cget("bg")
    new_color = 'red'
    global healthcheck
    if current_color == 'red':
        new_color = 'green'
        
        button.config(bg=new_color, activebackground=new_color)
       
        healthcheck = True
    else:
         new_color = 'red'
         healthcheck = False
         button.config(bg=new_color, activebackground=new_color)
def toggle_button_color69(button):
    current_color = button.cget("bg")
    new_color = 'red'
    global recoilcan
    if current_color == 'red':
        new_color = 'green'
        
        button.config(bg=new_color, activebackground=new_color)
       
        recoilcan = True
    else:
         new_color = 'red'
         recoilcan = False
         button.config(bg=new_color, activebackground=new_color)
def toggle_button_color922(button):
    current_color = button.cget("bg")
    new_color = 'red'
    global isscoped
    if current_color == 'red':
        new_color = 'green'
        
        button.config(bg=new_color, activebackground=new_color)
       
        isscoped = True
    else:
         new_color = 'red'
         isscoped = False
         button.config(bg=new_color, activebackground=new_color)
def toggle_button_color9222(button):
    current_color = button.cget("bg")
    new_color = 'red'
    global canshoot
    if current_color == 'red':
        new_color = 'green'
        
        button.config(bg=new_color, activebackground=new_color)
       
        canshoot = True
    else:
         new_color = 'red'
         canshoot = False
         button.config(bg=new_color, activebackground=new_color)
def toggle_button_color92222(button):
    current_color = button.cget("bg")
    new_color = 'red'
    global canbuy
    if current_color == 'red':
        new_color = 'green'
        
        button.config(bg=new_color, activebackground=new_color)
       
        canbuy = True
    else:
         new_color = 'red'
         canbuy = False
         button.config(bg=new_color, activebackground=new_color)
def toggle_button_colorc(button):
    current_color = button.cget("bg")
    new_color = 'red'
    global tracer
    if current_color == 'red':
        new_color = 'green'
        
        button.config(bg=new_color, activebackground=new_color)
       
        tracer = True
    else:
         new_color = 'red'
         tracer = False
         button.config(bg=new_color, activebackground=new_color)
def toggle_button_coloru(button):
    current_color = button.cget("bg")
    new_color = 'red'
    global listener_threadee
    if current_color == 'red':
        new_color = 'green'
        
        button.config(bg=new_color, activebackground=new_color)
        listener_threadee = True
        
    else:
         new_color = 'red'
         listener_threadee = False
         button.config(bg=new_color, activebackground=new_color)
def toggle_button_coloruuu(button):
    current_color = button.cget("bg")
    new_color = 'red'
    global aimboter
    if current_color == 'red':
        new_color = 'green'
        
        button.config(bg=new_color, activebackground=new_color)
        aimboter = True
        
    else:
         new_color = 'red'
         aimboter = False
         button.config(bg=new_color, activebackground=new_color)
def toggle_button_colorcolor(button):
    current_color = 'white'
    global color
    if color == 3:
         new_color = 'yellow'
         color = 4
         
         
         button.config(bg=new_color, activebackground=new_color)
    elif color == 4:
         color = 1
         new_color = 'white'
         
         button.config(bg=new_color, activebackground=new_color)

    elif color == 1:
        new_color = 'gray'
        color = 2
        
        button.config(bg=new_color, activebackground=new_color)
        
        
    elif color == 2:
         new_color = 'blue' 
         color = 3
         
         button.config(bg=new_color, activebackground=new_color)



    

# Function to create a toggle button

def create_toggle_button1(parent, text, checked_color, unchecked_color):
    frame = tk.Frame(parent, bg='#1d1918')
    label = tk.Label(frame, text=text, width=15, anchor='w', bg='#1d1918', fg='white', font=("Helvetica", 10))
    label.pack(side='left', padx=2, pady=2)
    toggle = tk.Button(frame, bg=unchecked_color, activebackground=unchecked_color, relief='flat', width=2, height=1)
    toggle.config(command=lambda: toggle_button_color1(toggle))
    toggle.pack(side='right', padx=2, pady=2)
    return frame
def create_toggle_button2(parent, text, checked_color, unchecked_color):
    frame = tk.Frame(parent, bg='#1d1918')
    label = tk.Label(frame, text=text, width=15, anchor='w', bg='#1d1918', fg='white', font=("Helvetica", 10))
    label.pack(side='left', padx=2, pady=2)
    toggle = tk.Button(frame, bg=unchecked_color, activebackground=unchecked_color, relief='flat', width=2, height=1)
    toggle.config(command=lambda: toggle_button_color2(toggle))
    toggle.pack(side='right', padx=2, pady=2)
    return frame
def create_toggle_button9(parent, text, checked_color, unchecked_color):
    frame = tk.Frame(parent, bg='#1d1918')
    label = tk.Label(frame, text=text, width=15, anchor='w', bg='#1d1918', fg='white', font=("Helvetica", 10))
    label.pack(side='left', padx=2, pady=2)
    toggle = tk.Button(frame, bg=unchecked_color, activebackground=unchecked_color, relief='flat', width=2, height=1)
    toggle.config(command=lambda: toggle_button_color9(toggle))
    toggle.pack(side='right', padx=2, pady=2)
    return frame
def create_toggle_button92(parent, text, checked_color, unchecked_color):
    frame = tk.Frame(parent, bg='#1d1918')
    label = tk.Label(frame, text=text, width=15, anchor='w', bg='#1d1918', fg='white', font=("Helvetica", 10))
    label.pack(side='left', padx=2, pady=2)
    toggle = tk.Button(frame, bg=unchecked_color, activebackground=unchecked_color, relief='flat', width=2, height=1)
    toggle.config(command=lambda: toggle_button_color92(toggle))
    toggle.pack(side='right', padx=2, pady=2)
    return frame
def create_toggle_button69(parent, text, checked_color, unchecked_color):
    frame = tk.Frame(parent, bg='#1d1918')
    label = tk.Label(frame, text=text, width=15, anchor='w', bg='#1d1918', fg='white', font=("Helvetica", 10))
    label.pack(side='left', padx=2, pady=2)
    toggle = tk.Button(frame, bg=unchecked_color, activebackground=unchecked_color, relief='flat', width=2, height=1)
    toggle.config(command=lambda: toggle_button_color69(toggle))
    toggle.pack(side='right', padx=2, pady=2)
    return frame
def create_toggle_button922(parent, text, checked_color, unchecked_color):
    frame = tk.Frame(parent, bg='#1d1918')
    label = tk.Label(frame, text=text, width=15, anchor='w', bg='#1d1918', fg='white', font=("Helvetica", 10))
    label.pack(side='left', padx=2, pady=2)
    toggle = tk.Button(frame, bg=unchecked_color, activebackground=unchecked_color, relief='flat', width=2, height=1)
    toggle.config(command=lambda: toggle_button_color922(toggle))
    toggle.pack(side='right', padx=2, pady=2)
    return frame
def create_toggle_button9222(parent, text, checked_color, unchecked_color):
    frame = tk.Frame(parent, bg='#1d1918')
    label = tk.Label(frame, text=text, width=15, anchor='w', bg='#1d1918', fg='white', font=("Helvetica", 10))
    label.pack(side='left', padx=2, pady=2)
    toggle = tk.Button(frame, bg=unchecked_color, activebackground=unchecked_color, relief='flat', width=2, height=1)
    toggle.config(command=lambda: toggle_button_color9222(toggle))
    toggle.pack(side='right', padx=2, pady=2)
    return frame
def create_toggle_button92222(parent, text, checked_color, unchecked_color):
    frame = tk.Frame(parent, bg='#1d1918')
    label = tk.Label(frame, text=text, width=15, anchor='w', bg='#1d1918', fg='white', font=("Helvetica", 10))
    label.pack(side='left', padx=2, pady=2)
    toggle = tk.Button(frame, bg=unchecked_color, activebackground=unchecked_color, relief='flat', width=2, height=1)
    toggle.config(command=lambda: toggle_button_color92222(toggle))
    toggle.pack(side='right', padx=2, pady=2)
    return frame
def create_toggle_buttonc(parent, text, checked_color, unchecked_color):
    frame = tk.Frame(parent, bg='#1d1918')
    label = tk.Label(frame, text=text, width=15, anchor='w', bg='#1d1918', fg='white', font=("Helvetica", 10))
    label.pack(side='left', padx=2, pady=2)
    toggle = tk.Button(frame, bg=unchecked_color, activebackground=unchecked_color, relief='flat', width=2, height=1)
    toggle.config(command=lambda: toggle_button_colorc(toggle))
    toggle.pack(side='right', padx=2, pady=2)
    return frame
def create_toggle_buttonu(parent, text, checked_color, unchecked_color):
    frame = tk.Frame(parent, bg='#1d1918')
    label = tk.Label(frame, text=text, width=15, anchor='w', bg='#1d1918', fg='white', font=("Helvetica", 10))
    label.pack(side='left', padx=2, pady=2)
    toggle = tk.Button(frame, bg=unchecked_color, activebackground=unchecked_color, relief='flat', width=2, height=1)
    toggle.config(command=lambda: toggle_button_coloru(toggle))
    toggle.pack(side='right', padx=2, pady=2)
    return frame
def create_toggle_buttonuuu(parent, text, checked_color, unchecked_color):
    frame = tk.Frame(parent, bg='#1d1918')
    label = tk.Label(frame, text=text, width=15, anchor='w', bg='#1d1918', fg='white', font=("Helvetica", 10))
    label.pack(side='left', padx=2, pady=2)
    toggle = tk.Button(frame, bg=unchecked_color, activebackground=unchecked_color, relief='flat', width=2, height=1)
    toggle.config(command=lambda: toggle_button_coloruuu(toggle))
    toggle.pack(side='right', padx=2, pady=2)
    return frame
def create_toggle_buttoncolor(parent, text, unchecked_color):
    frame = tk.Frame(parent, bg='#1d1918')
    label = tk.Label(frame, text=text, width=15, anchor='w', bg='#1d1918', fg='white', font=("Helvetica", 10))
    label.pack(side='left', padx=2, pady=2)
    toggle = tk.Button(frame, bg=unchecked_color, activebackground=unchecked_color, relief='flat', width=2, height=1)
    toggle.config(command=lambda: toggle_button_colorcolor(toggle))
    toggle.pack(side='right', padx=2, pady=2)
    return frame
def create_toggle_buttoncolore(parent, text, checked_color, unchecked_color):
    frame = tk.Frame(parent, bg='#1d1918')
    label = tk.Label(frame, text=text, width=15, anchor='w', bg='#1d1918', fg='white', font=("Helvetica", 10))
    label.pack(side='left', padx=2, pady=2)
    toggle = tk.Button(frame, bg=unchecked_color, activebackground=unchecked_color, relief='flat', width=2, height=1)
    toggle.config(command=lambda: toggle_button_color99(toggle))
    toggle.pack(side='right', padx=2, pady=2)
    return frame
def create_toggle_buttoncolore9(parent, text, checked_color, unchecked_color):
    frame = tk.Frame(parent, bg='#1d1918')
    label = tk.Label(frame, text=text, width=15, anchor='w', bg='#1d1918', fg='white', font=("Helvetica", 10))
    label.pack(side='left', padx=2, pady=2)
    toggle = tk.Button(frame, bg=unchecked_color, activebackground=unchecked_color, relief='flat', width=2, height=1)
    toggle.config(command=lambda: toggle_button_color999(toggle))
    toggle.pack(side='right', padx=2, pady=2)
    
    return frame





# Function to create a color option

# Function to create a slider


# Initialize the main application window

root = tk.Tk()
root.title("GhostLite")
root.configure(bg='#1d1918')
root.attributes('-topmost', True)  # Make overlay stay on top
def center_window(window, width, height):
    # Get the screen width and height
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    
    # Calculate the position
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    
    # Set the geometry of the window
    window.geometry(f'{width}x{height}+{x}+{y}')

# Create the main window

menu_frame = tk.Frame(root, bg='#1d1918')
menu_frame.pack(side='left', fill='y', padx=5, pady=5)


# Main settings frame
main_frame = tk.Frame(root, bg='#1d1918')
main_frame.pack(side='left', padx=5, pady=5)
# Define the window size
window_width = 180
window_height = 510
root.withdraw()  # Hide the Tkinter GUI
# Center the window
center_window(root, window_width, window_height)

# Remove the default window decorations
root.overrideredirect(True)

# Create a custom title bar



# Bind the title bar to the window movement function


# Side menu buttons


#create_gradient(canvas, window_width, window_height, '#2a2521', '#1d1918')
# Section headers


# Add widgets to the main frame
sections = [
    ('SkeletonEsp', 'green', 'red'),
    ('BoxEsp', 'green', 'red'),
    ('TracerEsp', 'green', 'red'),
    ('DefuseEsp', 'green', 'red'),
    ('HealthEsp', 'green', 'red'),
    ('ScopeEsp', 'green', 'red'),
    ('ShotEsp', 'green', 'red'),
    ('BuyMenuEsp', 'green', 'red'),
    ('TriggerBot', 'green', 'red'),
    ('RecoilBot', 'green', 'red'),
    ('Aimbot', 'green', 'red'),
    ('TeamCheck', 'green', 'red'),
    ('WaterMark', 'red', 'green'),
    ('ColorMode', 'white')
    
    
    

    
]

for section in sections:
    if section[0] == "SkeletonEsp":
        widget = create_toggle_button1(main_frame, section[0], section[1], section[2])
    if section[0] == "TeamCheck":
        widget = create_toggle_button2(main_frame, section[0], section[1], section[2])
    if section[0] == "BoxEsp":
        widget = create_toggle_button9(main_frame, section[0], section[1], section[2])
    if section[0] == "HealthEsp":
        widget = create_toggle_button92(main_frame, section[0], section[1], section[2])
    if section[0] == "RecoilBot":
        widget = create_toggle_button69(main_frame, section[0], section[1], section[2])
    if section[0] == "ScopeEsp":
        widget = create_toggle_button922(main_frame, section[0], section[1], section[2])
    if section[0] == "BuyMenuEsp":
        widget = create_toggle_button92222(main_frame, section[0], section[1], section[2])
    if section[0] == "ShotEsp":
        widget = create_toggle_button9222(main_frame, section[0], section[1], section[2])
    if section[0] == "TriggerBot":
        widget = create_toggle_buttonu(main_frame, section[0], section[1], section[2])
    if section[0] == "Aimbot":
        widget = create_toggle_buttonuuu(main_frame, section[0], section[1], section[2])
    if section[0] == "TracerEsp":
        widget = create_toggle_buttonc(main_frame, section[0], section[1], section[2])
    if section[0] == "ColorMode":
        widget = create_toggle_buttoncolor(main_frame, section[0],section[1])
    if section[0] == "WaterMark":
        widget = create_toggle_buttoncolore(main_frame, section[0], section[1], section[2])
    if section[0] == "DefuseEsp":
        widget = create_toggle_buttoncolore9(main_frame, section[0], section[1], section[2])
    
    

    
    widget.pack(pady=2, fill='y')




# Run the main application loop




isgui = True
listener_threade = threading.Thread(target=main)
listener_threade.start()
listener_threader = threading.Thread(target=triggerbot)
listener_threader.start()

# Create the gradient background

root.mainloop()
