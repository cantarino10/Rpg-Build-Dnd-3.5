import numpy as np
import pygame
import sys,os
import time,multiprocessing,char_builder

pygame.init()
pygame.font.init()

WIDTH = 1024
HEIGTH =700
display = pygame.display.set_mode([WIDTH,HEIGTH])
pygame.display.set_caption("Dnd 3.5 Life Calculator")

dmg_fonte = pygame.font.Font(None,20)
base_fonte = pygame.font.Font(None,26)

rect_sound = pygame.Rect(WIDTH -90,HEIGTH -80,60,60 )
rect_reset = pygame.Rect(WIDTH *0.02 + 5,HEIGTH -65,60,60 )

pygame.mixer.music.set_volume(0.2)

white = (255,255,255)
black = (0,0,0)

valid_value = False
typelife = False   
typetextname = False
back_sound = True
typetext = False

array_load = np.load('life_calcultaor_parameters.npz')
names = np.load("names.npy")
lifes = np.load("life.npy")
sound = array_load["arr_0"]       
dmg_take = array_load["arr_1"]  
dmg_healed = array_load["arr_2"]      
life_pos_counter = array_load["arr_3"] 
life_counter = array_load["arr_4"] 
alive = array_load["arr_5"] 
tex = array_load["arr_6"]
text_all = ['','','','','','']
life_all = ['','','','','','']
j = 0
for i in names:
   text_all[j] = i
   j += 1
   
j = 0
for i in lifes:
   life_all[j] = i
   j += 1
   




value = 0
negative = 1



def f_display(text,coordinate):
   display.blit(text,coordinate)

def f_drawrect(color,rect,border):
   if border > 0:
      pygame.draw.rect(display,(color),rect,border)
   else:
      pygame.draw.rect(display,(color),rect)
def rect_create():
   global WIDTH

   rec_x = 10
   rec_y = 10 
   rec_w = int(WIDTH/6.5)
   rec_h = 32
   rec_name = []
   rec_life = []
   for i in range(6):
      for j in range(2):
         
       recs = pygame.Rect(rec_x + ((rec_w) * j +50 ) , i * (rec_y + 90) +30,rec_w/((3* j) + 1),rec_h)
       if j == 0 :
        rec_name.append(recs)
       else :
        rec_life.append(recs)   
        
   return rec_name,rec_life

def rect_design(rec_l,rec_n):
   
   for r in rec_l:
      pygame.draw.rect(display,(255,255,255),r)
   for r in rec_n:   
      pygame.draw.rect(display,(255,255,255),r)
      

def print_text(*text_to_print):
   global rect
   j = -1
   for i in text_to_print:
      j += 1
      input_rect = (10,j*100 +30 ,160,32)
      rect = pygame.draw.rect(display,white,input_rect)
      
      f_drawrect(black,input_rect,3)
     
      if i != "":
         text_surface = base_fonte.render(f"{i}",True,(0,0,0))
        
         f_display(text_surface,(rect.x + 4,rect.y+7))
             
            

def print_life(*life_to_print):
   life_fonte = pygame.font.Font(None,22)
   j = -1
   for i in life_to_print:
      j += 1
   
      input_rect = pygame.Rect(215,j*100 +30.5 ,160/4 + 5,32)
      f_drawrect(white,input_rect,0)
      f_drawrect(black,input_rect,2)
     
            
      if i != "":
         text_surface = life_fonte.render(f"{i}",True,(0,0,0))
         f_display(text_surface,(input_rect.x + 4,input_rect.y + 10))
                 
         
def print_life_change(*counter):
   global alive,sound,dmg_take

   life_fonte = pygame.font.Font(None,25)
   color = (0,255,0)
   line = 0
   number_position = 0
   adjust = np.zeros(6)
   dmg_tak = 0
   dmg_heal = 0
   for i in counter:
      sum = 0
      count = 0
      dmg_tak = 0
      dmg_heal = 0
      for j in i:
       
       if number_position > 1150:
         adjust[line] += 30 
         count = 0
       number_position = 310 + (count * 35 )
                
       if j  > 0:
         if j + sum >= i[0]:
            color = (0,0,255)
         else:
            color = (0,255,0)   
         if j + sum> i[0]:
            sum = i[0]
         else:
            sum = sum + j
            dmg_heal += j
         text_surface = life_fonte.render(f"{sum}",True,color)
         f_display(text_surface,(number_position, 40+ (line * 100) + adjust[line]))
         count += 1 
         alive[line] = True
               
       elif  j < 0:
         dmg_tak -= j     
         
         if sum + j > - 10:
            sum = sum +j
            text_surface = life_fonte.render(f"{sum}",True,(255,0,0))
            alive[line] = True  
         else:
            sum = sum + j
            text_surface = life_fonte.render(f"{sum} - DEAD -",True,(255,0,0))
            if sound[line] == True:
               
               dmg_take[line] = dmg_tak
               dmg_healed[line] = dmg_heal - i[0]
               sound_dead = pygame.mixer.Sound("Sounds/dead.wav")          
               sound_dead.play()
               sound[line] = False
            alive[line] = False
         f_display(text_surface,(number_position, 40 + (line * 100) +adjust[line]  ))  
         
         count += 1
       else:
         break 
       mod = line
       draw_bar(i[0],sum,line)
       f_drawrect((155,155,155),(170,33 + (mod *100),44,27),0)   
       f_drawrect(black,(170,30 + (mod *100),46,32),2)
       sum_surface = life_fonte.render (f"{sum}",True,(0,0,0))
       f_display(sum_surface,(178,40 +(mod * 100) ))
      line = line + 1       
      if line > 6:
         line = 0 
        

def draw_bar(total_life,current_life,char):
   life_fonte = pygame.font.Font(None,25)
   if current_life == 0:
       bar_life = 0 
   else:
       bar_life = current_life/total_life
   
   bar = (13 ,(char *100) + 62,(157 * bar_life),24)
   black_bar = (13 ,(char *100) + 62,157 ,24)  

   if bar_life > 0.5:
      color = (0,150,0)
   elif bar_life > 0.25 and bar_life <= 0.5:
      color = (180,180,0)   
   else:
     color = (220,0,0)
   f_drawrect(black,black_bar,0)
   f_drawrect(color,bar,0)  
   text_surface = life_fonte.render(f"{current_life} / {total_life}",True,(225,225,225))   
   text_rect = text_surface.get_rect(center=(160/2, ((char*100) + 75)))
   f_display(text_surface,text_rect)


def print_life_now_rect(*rect_reset,):
    img_reset_life = pygame.image.load("images/reset_button.png")
    img_reset_life = pygame.transform.scale(img_reset_life, (50,30))
    j = 0
    for g in rect_reset:
       display.blit(img_reset_life, g)   
       pygame.draw.rect(display,(155,155,155),(170,33 + (j *100),44,27))
       pygame.draw.rect(display,(0,0,0),(170,30 + (j *100),46,32),2)
       j += 1
     
def write_name(event,rec,text,h):
    global typetextname
                
    for event in pygame.event.get():
       if event.type == pygame.MOUSEBUTTONDOWN:
            if  not rec.collidepoint(event.pos):
             typetextname  = False 
             return text
     
       if event.type == pygame.QUIT:
           pygame.quit()
           sys.exit()  
       if event.type == pygame.KEYDOWN:
         if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
             np.savez('life_calcultaor_parameters',sound,dmg_take,dmg_healed,life_pos_counter,life_counter,alive,text_all,life_all)
             np.save("names", text_all)
             
             typetextname = False 
             
         elif event.key == pygame.K_BACKSPACE or len(text) > 16:
              text = text[:-1] 
         elif len(text) < 16:
              text = text + event.unicode     
    return text            
  
def write_life(event,rec,text,j):
  global typelife,valid_value,negative,alive,sound
  sound_read = pygame.mixer.Sound("Sounds/Fight_sound.wav")  
  Typing = True    
  while Typing == True:    
   for event in pygame.event.get():
       if event.type == pygame.MOUSEBUTTONDOWN:
         if not rec.collidepoint(event.pos):
            typelife  = False 
            return text
       
       if event.type == pygame.QUIT:
           pygame.quit()
           sys.exit()  
       if event.type == pygame.KEYDOWN:
         np.savez('life_calcultaor_parameters',sound,dmg_take,dmg_healed,life_pos_counter,life_counter,alive,text_all,life_all)
         np.save("names", text_all)
         np.save("life", life_all) 
         if (event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER) and text != "-" and text  !="":
             
              negative = 1
              valid_value = True
              Typing = False
              if life_pos_counter[j] == 0:
                  sound_read.play()
              if alive[j] == False:
                 sound_read.play()
                 sound[j] = True
                 life_counter[j:j+1] = 0
                 life_pos_counter[j] = 0   
                 
              else:
                 typelife = True 
         elif event.key == pygame.K_BACKSPACE :
              text = text[:-1]
         if event.unicode == "-":
            negative += 1   
               
         if (event.unicode.isdigit() or (event.unicode == "-" and negative < 3)) and len(text) < 4 :
             text = text + event.unicode
             

       pygame.time.wait(5)
       pygame.display.update()                         
   return text      
    

def sound_controler(sound):
   fonte = pygame.font.Font(None,35)
   fonte2 = pygame.font.Font(None,22)
   escape_font = pygame.font.SysFont("Arial",25,bold= True,italic=True)
   if  sound:
      sound_icon = pygame.image.load("images/sound_image.png")
   else:   
      sound_icon = pygame.image.load("images/nosound_image.png")
   sound_icon = pygame.transform.scale(sound_icon,(110,80))
   rect = sound_icon.get_rect(center = (WIDTH - 40, HEIGTH  -40 ))
   display.blit(sound_icon,(rect))

   reset_icon = pygame.image.load("images/reset_button.png")
   reset_icon = pygame.transform.scale(reset_icon,(110,80))
   rect_reset = reset_icon.get_rect(center =( WIDTH * 0.05,HEIGTH - 40))
   display.blit(reset_icon,rect_reset)
   text_name = fonte.render("Name        HP  ",1,(0,0,0))
   text_life = fonte2.render("Dmg ",1,(0,0,0))
   display.blit(text_name,(60,5))
   display.blit(text_life,(220,2))
   text_life = fonte2.render("Heal ",1,(0,0,0))
   display.blit(text_life,(220,15))
   text_reset = fonte.render("Reset",1,(255,255,255))
   display.blit(text_reset,(WIDTH * 0.028,HEIGTH - 90))
   if time.time() % 1 > 0.5:
    return_text = escape_font.render("Press Esc To Return",1,(0,0,0))
    display.blit(return_text,(WIDTH * 0.6,HEIGTH * 0.92))  
def Checkrect(rec):
   return rec.y / 91


def create_rect_resetlife(*rects):
   liferec = []
   for i in rects:
      recs = pygame.Rect(i.x + i.w,i.y,i.w,i.h)
   
      liferec.append(recs)
   return liferec      


def main():
    global base_fonte,display,typetextname,rects,typelife,valid_value,back_sound,life_counter,life_pos_counter,alive,text_all,life_all
    
    pygame.mixer.music.load("Sounds/battle_sound.wav")
  
    runing = False
    background = pygame.image.load("images/background_LifeCounter.jpg")
    background = pygame.transform.scale(background, (1280,720))
    rects = rect_create()     
    rect_reset_life = create_rect_resetlife(*rects[1])  
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.2)
    
    
    while not runing :
     
    
     display.blit(background,(0,0)) 
     sound_controler(back_sound)    
     print_life_now_rect(*rect_reset_life)
     print_text(*text_all)
     print_life(*life_all)
     print_life_change(*life_counter)   
    
     for event in pygame.event.get():
      if event.type == pygame.QUIT:
         pygame.quit()
         sys.exit()
      if event.type == pygame.KEYDOWN:
         if event.key == pygame.K_ESCAPE:
          runing = True       
          
      if event.type == pygame.MOUSEBUTTONDOWN:
         if rect_sound.collidepoint(event.pos):
             if back_sound == True:
              pygame.mixer.music.set_volume(0.0)
             else:
               pygame.mixer.music.set_volume(0.2)          
             back_sound = not back_sound
             
         if rect_reset.collidepoint(event.pos):
            
            text_all = ['','','','','','']
            life_all = ['','','','','','']
            life_pos_counter = np.zeros(6).astype(int)
            life_counter = np.zeros((6,50)).astype(int)
            alive = np.ones(6).astype(int)

         for rec in rects[0]:
            if  rec.collidepoint(event.pos):
             h = int(Checkrect(rec) )
             text_all[h] = text_all[h]
             
             typetextname = True
             
             break            
         for recl in rects[1]:
            if recl.collidepoint(event.pos):
              j = int(Checkrect(recl))
                     
              life_all[j] = life_all[j] 
              typelife = True
              break
         for i in range(6):
            if rect_reset_life[i].collidepoint(event.pos):
              
              life_counter[i] = 0
              life_pos_counter[i] = 0
          
               
      while typetextname == True:
        while typetextname == True: 
         text_all[h] =   write_name(event,rec,text_all[h],h)    
         print_text(*text_all)
         if time.time() % 1 > 0.5:
             bar = pygame.Rect((len(text_all[h]) * 9.5) + 14,(h * 100) +34,1.5,23)
             pygame.draw.rect(display,(0,0,0),bar,) 
         pygame.time.wait(5)
         pygame.display.update() 
         
        if text_all[h] != "":
         typelife = True
         
         j = h 
      while typelife == True:
         c = time.time()
         life_all[j] = write_life(event, recl, life_all[j],j)
         print_life(*life_all)
         if alive[j] == False:
            display.blit(background,(0,0))     
            
            print_text(*text_all)
            print_life(*life_all)
            print_life_now_rect(*rect_reset_life)
            print_life_change(*life_counter)
            sound_controler(back_sound)  
            taken_surface = dmg_fonte.render(f"Damage Taken = {dmg_take[j]}",True,(150,0,0))
            display.blit(taken_surface,(13,(j*100) + 90))   
            healed_surface = dmg_fonte.render(f"Damage Healed = {dmg_healed[j]}",True,(0,250,0))
            display.blit(healed_surface,(13,(j*100) + 110))   
         
         if valid_value == True:
           if life_all[j] != "" and life_all[j] != 0:
            value = int(life_all[j])
            life_all[j] = ""
            life_counter[j,life_pos_counter[j]] = value
            life_pos_counter[j] += 1
            valid_value = False
            print_life_change(*life_counter)  
           
           typelife = True 
         if time.time() % 1 > 0.5:
            
             barr = pygame.Rect((len(life_all[j]) * 8.5) + 220,(j *100) +34,1.5,23)
             pygame.draw.rect(display,(0,0,0),barr) 
        
        
         pygame.time.wait(5)
         pygame.display.update() 
         pygame.display.flip()    
     np.savez('life_calcultaor_parameters',sound,dmg_take,dmg_healed,life_pos_counter,life_counter,alive,text_all,life_all)
     np.save("names", text_all) 
     np.save("life", life_all) 
     pygame.time.wait(15)
     pygame.display.flip()

