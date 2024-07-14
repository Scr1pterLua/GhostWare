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
import random
import math
#Values for sliders
ragesmoothing = 0
legitsmoothing = 0
recoilamount = 0
legitfov = 0
ragefov = 0
TrueSmoothing = False
holding = False
hastarget = False
locked = False
triggerbotdelay = 0
maxtriggerbotdelay = 0
disrage = 0
dislegit = 0
#-----------------
ScreenY = 1920
ScreenX = 1080
#-----------------
cansee = False
GunControl = 1
MaxEntityRead = 64
canshoot = False
canbuy = False
isscoped = False
recoilcan = True
watermark = True
defusecheck = False
healthcheck = False
listener_threadee = False
gui_visible = False
isgui = False
color = 1
skelly = False
tracer = False
box = False
teamchecky = False
def leftclick():
    return win32api.GetKeyState(win32con.VK_XBUTTON1) < 0
def middleclick():
    return win32api.GetKeyState(win32con.VK_XBUTTON2) < 0
def toggle_gui_visibility():
    global gui_visible
    if gui_visible:
       
        gui_visible = False
    else:
        
        gui_visible = True

def on_delete_key(event):

       toggle_gui_visibility()

def listen_for_delete_key():
    keyboard.on_press_key("home", on_delete_key)
    

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
        if "Counter-Strike 2" in title or "GhostLite" in title:
            return True
    return False





try:
   pm = pymem.Pymem("cs2.exe")
   
   setconsolestatus()

except:
    
    print(colorama.Fore.RED + "[GHOST] [SYSTEM] [ERROR]" + colorama.Fore.WHITE)
    
      
    
    
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
m_hPlayerPawn = client_dll['client.dll']['classes']['CCSPlayerController']['fields']['m_hPlayerPawn']
m_iIDEntIndex = client_dll["client.dll"]["classes"]["C_CSPlayerPawnBase"]["fields"]["m_iIDEntIndex"]
m_bIsDefusing = client_dll['client.dll']['classes']['C_CSPlayerPawn']['fields']['m_bIsDefusing']
m_bIsScoped = client_dll['client.dll']['classes']['C_CSPlayerPawn']['fields']['m_bIsScoped']
m_iHealth = client_dll['client.dll']['classes']['C_BaseEntity']['fields']['m_iHealth']
m_bIsBuyMenuOpen = m_bIsScoped = client_dll['client.dll']['classes']['C_CSPlayerPawn']['fields']['m_bIsBuyMenuOpen']
m_iShotsFired = client_dll['client.dll']['classes']['C_CSPlayerPawn']['fields']['m_iShotsFired']



client = pymem.process.module_from_name(pm.process_handle, "client.dll").lpBaseOfDll
mouse = Controller()









def triggerbot():
    


    while True:
        try:
            if not GetWindowText(GetForegroundWindow()) == "Counter-Strike 2":
                continue
            if maxtriggerbotdelay == 0 and triggerbotdelay == 0:
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
                global locked
                entityHp = pm.read_int(entity + m_iHealth)
                if entityHp > 0:
                    
                        time.sleep(random.uniform(triggerbotdelay, maxtriggerbotdelay))
                        mouse.click(Button.left)
                
                        locked = True
                    
                    
                    
                    
                    
                else:
                    
                    locked = False
            
            locked = False
                    
                    
                
           

            
            
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
    global legitsmoothing
    global TrueSmoothing
    
    if not head_pos[0] == 0:
       newx = center_x / head_pos[0]
       newx = math.floor(newx)
       if TrueSmoothing:
          if newx == 0:
       
            newx = legitsmoothing - math.floor(center_x / center_y / head_pos[0] )
       
          else:
       
            newx = -legitsmoothing + math.floor(center_x / center_y / head_pos[0]) 
       else:
           if newx == 0:
       
            newx = legitsmoothing 
       
           else:
       
            newx = -legitsmoothing 



    if not head_pos[1] == 0:
       newy = center_y /  head_pos[1]
       newy = math.floor(newy)
       if TrueSmoothing:
          if newy == 0:
       
            newy = legitsmoothing - math.floor(center_y / center_x / head_pos[1]) 
       
          else:
       
            newy = -legitsmoothing + math.floor(center_y / center_x / head_pos[1]) 
       else:
           if newy == 0:
       
            newy = legitsmoothing 
       
           else:
       
            newy = -legitsmoothing 

  
    def ifplayerinfovthenlockon():
       
    # Assuming center_x and center_y are defined elsewhere

       ispress = leftclick()  # Assuming leftclick() is defined elsewhere
      
       global locked
       global holding
       if ispress or locked:
        
           
           ctypes.windll.user32.mouse_event(0x0001, newx   , newy  , 0, 0)
       else:
           holding = False
    ifplayerinfovthenlockon()
# ESP function
def rageaimbot(head_pos,center_x,center_y):
  
    newx = 0
    newy = 0
    global ragesmoothing
    global TrueSmoothing
    
    if not head_pos[0] == 0:
       
       newx = center_x / head_pos[0]
       newx = math.floor(newx)
       if TrueSmoothing:
          if newx == 0:
       
            newx = ragesmoothing  - math.floor(center_x / center_y / head_pos[0] ) 
       
          else:
       
            newx = -ragesmoothing  + math.floor(center_x / center_y / head_pos[0]) 
       else:
           if newx == 0:
       
            newx = ragesmoothing 
       
           else:
       
            newx = -ragesmoothing 
        



    if not head_pos[1] == 0:
       newy = center_y /  head_pos[1]
       newy = math.floor(newy)
       if TrueSmoothing:
          if newy == 0:
       
            newy = ragesmoothing  - math.floor(center_y /  center_x / head_pos[1])
       
          else:
       
            newy = -ragesmoothing  + math.floor(center_y / center_x / head_pos[1]) 
       else:
           if newy == 0:
       
            newy = ragesmoothing
       
           else:
       
            newy = -ragesmoothing 
  
    def ifplayerinfovthenlockon():
       
    # Assuming center_x and center_y are defined elsewhere

       
       isleftclicker = middleclick()
       global locked
       global holding
       if isleftclicker:
         
          
           ctypes.windll.user32.mouse_event(0x0001, newx   , newy  , 0, 0)
           
           
       else:
           holding = False
    ifplayerinfovthenlockon()
# ESP function
def rocel():
    ispress = leftclick()  # Assuming leftclick() is defined elsewhere\
    isleftclicker = middleclick()
    global recoilamount
    
       
    if ispress and recoilcan or isleftclicker and GetWindowText(GetForegroundWindow()) == "Counter-Strike 2":
      
          
          
      
        ctypes.windll.user32.mouse_event(0x0001, 0   , recoilamount  , 0, 0)
   

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
        "head": 6, "chest": 0, "left_hand": 10,
        "right_hand": 15, "left_leg": 24, "right_leg": 27
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
    leftXX = head_pos[0] - deltaZ // 3.5
    rightXX = head_pos[0] + deltaZ // 3.5
    leftX = head_pos[0] - deltaZ // 4.5
    rightX = head_pos[0] + deltaZ // 4.5
    center_x = ScreenY / 2
    center_y = ScreenX / 2

   
    
    
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
        
        draw_list.add_line(leftXX, leg_pos[1], leftXX, head_pos[1], healthcolor, 1)
    
    

    

    
    
                 
         
 

    distance = math.sqrt((head_pos[0] - center_x)**2 + (head_pos[1] - center_y)**2)


    threshold_distance = ragefov


    if distance <= threshold_distance and not ragesmoothing == 0:
       if not distance <= disrage:

  
        rageaimbot(head_pos,center_x,center_y)
        colorr = imgui.get_color_u32_rgba(1, 0.1, 0.1, 1)
    
    
    
    if distance <= threshold_distance and not legitsmoothing == 0:
       if not distance <= dislegit:
         
    
          
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
        draw_list.add_line(head_pos[0], head_pos[1],chest_pos[0], chest_pos[1], colorr, 1)
       
        draw_list.add_line(chest_pos[0], chest_pos[1],right_leg_pos[0], right_leg_pos[1], colorr, 1)
        draw_list.add_line(chest_pos[0], chest_pos[1],left_leg_pos[0], left_leg_pos[1],colorr, 1)
        draw_list.add_line(chest_pos[0], chest_pos[1],right_hand_pos[0], right_hand_pos[1], colorr, 1)
        draw_list.add_line(chest_pos[0], chest_pos[1],left_hand_pos[0], left_hand_pos[1], colorr, 1)
    rocel()
    
    


               
            


                
            
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
    global gui_visible
    global ragesmoothing
    global skelly
    global legitsmoothing
    global box
    global ragefov
    global legitfov
    global teamchecky
    global tracer
    global healthcheck
    global recoilamount
    global maxtriggerbotdelay
    global triggerbotdelay
    global color
    global TrueSmoothing
    global disrage
    global dislegit
    if not glfw.init():
        print("Could not initialize OpenGL context")
        exit(1)

    # Create a windowed mode window and its OpenGL context
   
    #windowe = glfw.create_window(ScreenY, ScreenX, "ImGui with GLFW Example", None, None)
    hwndd = glfw.get_win32_window(window)
    style = win32gui.GetWindowLong(hwndd, win32con.GWL_STYLE)
    style &= ~(win32con.WS_CAPTION | win32con.WS_THICKFRAME)
    win32gui.SetWindowLong(hwndd, win32con.GWL_STYLE, style)
  
 
    
    if not window:
        glfw.terminate()
        return

    # Make the window's context current
    glfw.make_context_current(window)

    # Create an ImGui context and a renderer for GLFW
    imgui.create_context()
    impl = GlfwRenderer(window)

    

    # Loop until the user closes the window
    while True:
        if gui_visible:
             ex_style = win32con.WS_EX_TRANSPARENT
             win32gui.SetWindowLong(hwndd, win32con.GWL_EXSTYLE, ex_style)
             
        else:
             ex_style = win32con.WS_EX_TRANSPARENT | win32con.WS_EX_LAYERED
             win32gui.SetWindowLong(hwndd, win32con.GWL_EXSTYLE, ex_style)

        # Poll for and process events
        if gui_visible:
            glfw.poll_events()
            impl.process_inputs()

        # Start a new ImGui frame
            imgui.new_frame()
            #imgui.set_next_window_position(0, 0)
            imgui.set_next_window_size(450, 325)
        
        
        
            
            imgui.begin("GhostWare",flags = imgui.WINDOW_NO_RESIZE)
        
            superchangeddd, ragefov = imgui.slider_float("Fov",  math.floor(ragefov), 0,100)
            
            
            changed, ragesmoothing = imgui.slider_float("AimBot Speed", math.floor(ragesmoothing), 0,15)
            ragesmoothing = math.floor(ragesmoothing)
          
            superchangedzxzxcv, disrage = imgui.slider_float("AimBot Smoother", math.floor(disrage), 0,5)
            
            superchangedzxzx, legitsmoothing = imgui.slider_float("LegitBot Speed", math.floor(legitsmoothing), 0,15)
            legitsmoothing = math.floor(legitsmoothing)
            
            superchangedzxzxc, dislegit = imgui.slider_float("LegitBot Smoother", math.floor(dislegit), 0,5)
            
            

            
            
         
            superchangeddd, recoilamount = imgui.slider_float("RecoilControl", math.floor(recoilamount), 0,5)
            recoilamount = math.floor(recoilamount)
           
            superchangedddx, triggerbotdelay = imgui.slider_float("TriggerBotDelay", triggerbotdelay, 0,0.1)
            
            superchangedddz, maxtriggerbotdelay = imgui.slider_float("MaxTriggerBotDelay", maxtriggerbotdelay, 0,0.1)
            superchangedddzz, color = imgui.slider_float("ColorMode",  math.floor(color), 1,4)
           
            if imgui.button("TeamCheck"):
                
                if  teamchecky:
                
                    teamchecky = False
                else:
                    teamchecky = True
            if imgui.button("Box Esp"):
                
                if  box:
                
                    box = False
                else:
                    box = True
            if imgui.button("Bone Esp"):
                
                if skelly:
                
                    skelly = False
                else:
                    skelly = True
            if imgui.button("SnapLines"):
                
                if tracer:
                
                    tracer = False
                else:
                    tracer = True
            if imgui.button("HealthBar"):
                
                if healthcheck:
                
                    healthcheck = False
                else:
                    healthcheck = True
                
                
        
            
        
            imgui.end()
            imgui.end_frame()
            gl.glClearColor(0, 0, 0, 0)
            gl.glClear(gl.GL_COLOR_BUFFER_BIT)
        
            
            
            
    
        
        
        

      
            imgui.render()
            impl.render(imgui.get_draw_data())
            glfw.swap_buffers(window)
        else:
            glfw.poll_events()
            impl.process_inputs()
            imgui.new_frame()
            imgui.set_next_window_size(ScreenY, ScreenX)
            imgui.set_next_window_position(0, 0)
            imgui.begin("overlay", flags=imgui.WINDOW_NO_TITLE_BAR | imgui.WINDOW_NO_RESIZE | imgui.WINDOW_NO_SCROLLBAR | imgui.WINDOW_NO_COLLAPSE | imgui.WINDOW_NO_BACKGROUND)
            draw_list = imgui.get_window_draw_list()
        
      
        
       
    

    
        
    
        
       
         
           


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


isgui = True

listener_threadex = threading.Thread(target=main)
listener_threadex.start()
listener_threader = threading.Thread(target=triggerbot)
listener_threader.start()


# Create the gradient background

