import pygame
import time
import os
import numpy as np
pygame.init()
pygame.font.init()

fonte = pygame.font.Font(None,36)

white = (255,255,255)
black = (0,0,0)
gray = (150,150,150)

WIDTH = 1024
HEIGTH = 720
background = pygame.image.load("images/Menu_backgroud.webp")
background = pygame.transform.scale(background,(WIDTH,HEIGTH))
display = pygame.display.set_mode([WIDTH,HEIGTH])
pygame.display.set_caption("DnD 3.5 Table Finder")


class draw_rect:
    
    def __init__(self,pointx,pointy,larg,tall):
        self.x = pointx
        self.y = pointy
        self.w = larg
        self.h = tall
        self.rect = (self.x,self.y,self.w,self.h)
        self.center = (self.x/2,self.y/2)
        self.colide = pygame.Rect(self.x,self.y,self.w,self.h)
   
    def colors(self,color):
        col = {
            "white" : (255,255,255),
            "black" :(0,0,0)

        }
        return col[color]

        
    
    def draw(self,color,border,border_color):
         
         self.b_color = border_color
         if border > 0:
           pygame.draw.rect(display,self.colors(border_color),(self.x - 2,self.y-2,self.w +4,self.h+4),border) 
           pygame.draw.rect(display,color,self.rect)
         else:
            pygame.draw.rect(display,(color),(self.x,self.y,self.w,self.h))    

def f_drawrect(color,rect,border):
   if border > 0:
      pygame.draw.rect(display,(color),rect,border)
   else:
      pygame.draw.rect(display,(color),rect)

def f_display(text,coordinate):
   display.blit(text,coordinate)


def event_handler(event):
    global running
    if search_bar_rect.colide.collidepoint(event.pos):
            return "texting"
    elif results_rect.colide.collidepoint(event.pos):
            return "result"
    else:
        return None
     
def text_blinking_bar():
     blinking_bar.draw(black,0,"white")   
      
def screen():
    display.blit(background,(0,0))
    search_bar_rect.draw(white,2,"black")
    results_rect.draw(black,2,"white")
    scrollbar_back .draw(white,0,"white")
   
    scrollbar.draw(gray,0,white)

def texting(event,text):
    txt = fonte.render(text,1,black)
    txtrect = txt.get_rect()
    txtrect.x = search_bar_rect.x + 18
    
        
   
    text = text + event.unicode
    if len(text) > 0:
     
      blinking_bar.x = txtrect.x + txtrect.w
    else:
        blinking_bar.x = search_bar_rect.x + 5
    
    return text 
def result(text):
    
    tables = []
    path = "Tables"
    
    rect_table = []
    for dir, subpaste,files in os.walk(path):
        tables = []
        i = 0
        for names in files:
         
         if text == "" :
          
          tables.append(names[:-4])
          recs = pygame.Rect(results_rect.x,results_rect.y + (i*25) + 2,results_rect.w, 27)
          rect_table.append(recs)
          i = i + 1
          
         else:
            if names.find(text)  != - 1:
             recs = pygame.Rect(results_rect.x,results_rect.y + (i*25) + 2,results_rect.w, 27)
             rect_table.append(recs)
             tables.append(names[:-4])
             
             i += 1
            
    return tables,rect_table
    
def screen_update(text,*table_loader) :
    global cont_scrollbar,move_scrollbar
    i = 0
    j = 0
    screen()
    text_surface = fonte.render(text,1,black)
    f_display(text_surface,(search_bar_rect.x + 7, search_bar_rect.y + 3))
    k = move_scrollbar
    for table in table_loader:
         
    
        
        if i < 22 and k <= 0:       
            text_to_load = fonte.render(f"{table}",1,white)
            f_display(text_to_load,(results_rect.x + 2,results_rect.y +  2 + (i*25)))
            
            i += 1
        k-= 1
        j += 1
    scrollbar_back.draw(white,0,white)
    if j < 22 and j != 0:
       
        scrollbar.h = std_scrollbar_h
    elif j != 0:
        
        cont_scrollbar = j - 22
        scrollbar.h = (std_scrollbar_h / j )                                                                                                                                                                                         
    
    scrollbar.draw(gray,0,white)        
    

def open_table(txt):
      global running
      loop = True
      while loop == True:
        
        display.fill(black)
        try:    
            table_img = pygame.image.load(f"Tables/{txt}.png")
        except:
            return "texting"    
        
        table_image = pygame.transform.scale(table_img,(WIDTH * 0.95, HEIGTH * 0.95))
        img_surface = table_image.get_rect(center =( WIDTH / 2, HEIGTH/ 2))
        f_display(table_image,img_surface)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                loop = False
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                   return   
        pygame.display.update()    
      return "result"  

def move_scrollbarup(l,move):
   global move_scrollbar
   if scrollbar.y > std_scrollbar_y: 
    scrollbar.y -= move
    move_scrollbar -= 1
def move_scrollbardown(l,move):
    global move_scrollbar
   
    if (scrollbar.y  + scrollbar.h)  + move< ((scrollbar_back.y + scrollbar_back.h )) :
        scrollbar.y += move
        move_scrollbar += 1


move_scrollbar = 0
running  = True
search_bar_rect = draw_rect(WIDTH /10.5, HEIGTH * 0.05,WIDTH * 0.8,HEIGTH * 0.05)
results_rect = draw_rect(search_bar_rect.x,search_bar_rect.y +50,search_bar_rect.w, HEIGTH * 0.8)
cont_scrollbar = 0
scrollbar_back = draw_rect(results_rect.x + results_rect.w +2,results_rect.y -2,WIDTH *0.02,results_rect.h +4)
blinking_bar = draw_rect(search_bar_rect.x + 7,search_bar_rect.y + 2,WIDTH *0.002,search_bar_rect.h -4)
std_scrollbar_h = scrollbar_back.h 
std_scrollbar_y = scrollbar_back.y
scrollbar = draw_rect(scrollbar_back.x ,std_scrollbar_y ,scrollbar_back.w, std_scrollbar_h)

screen()
def main():
 text = ""
 global running,move_scrollbar
 clock = pygame.time.Clock()
 timer = 0
 dt = 0
 select = None
 table_loader = []
 table_colide = []
 i = 0
 running = True

 while running:
    if len(table_loader) > 22:
        
        scroll_move = std_scrollbar_h / (len(table_loader) - 21)
    for event in pygame.event.get():
     if event.type == pygame.QUIT:
            running = False
     if event.type == pygame.KEYDOWN:
         if event.key == pygame.K_ESCAPE:
             running = False       
     if select == None:     
          if event.type == pygame.MOUSEBUTTONDOWN :
           
            if event.button == 1:
               
                select = event_handler(event)
            elif results_rect.colide.collidepoint(pygame.mouse.get_pos()) :
             
              if event.button == 4 and scroll_move >= 0:
                move_scrollbarup(len(table_loader),scroll_move)

                
              if event.button == 5:
                  move_scrollbardown(len(table_loader),scroll_move)
    

                           
              
              
     screen_update(text)  
     if select == "texting":
        
        if event.type == pygame.KEYDOWN:
            move_scrollbar = 0
            scroll_move = 0
            scrollbar.y = std_scrollbar_y
            if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                select = open_table(text)
                text = ''
                screen_update(text,*table_loader)   
                
            else:    
                text = texting(event,text)
     
        if event.type == pygame.MOUSEBUTTONDOWN :
            
            if event.button == 1:
               
                select = event_handler(event)
            elif results_rect.colide.collidepoint(pygame.mouse.get_pos()) :
             
              if event.button == 4:
                move_scrollbarup(len(table_loader),scroll_move)
                
              if event.button == 5:
                  move_scrollbardown(len(table_loader),scroll_move)   
     table_loader,table_colide = result(text)   
     r = 0
     if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
          for r in table_colide:
               if r.collidepoint(event.pos):
                
                  text = table_loader[i + move_scrollbar]
                  select = "texting"
                  
               i += 1  
          if event.button == 1: 
            if timer == 0:  # First mouse click.
                        timer = 0.001  # Start the timer.
                    # Click again before 0.5 seconds to double click.
            elif timer < 0.5 and timer  > 0 :
                        
                        select = open_table(text)
                                         
                        text = ''
                       
                        
                        screen_update(text,*table_loader)   
                       
                        timer = 0            
           
            i = 0                        
         
    if timer != 0:
            timer += dt
            if timer >= 0.5:
                timer = 0     
    dt = clock.tick(30) / 1000                 
    keys = pygame.key.get_pressed()
    if keys[pygame.K_BACKSPACE]:
        text = text[:-1] 
        texting(event,text)
    
    screen_update(text,*table_loader)        
    
    if select == "texting":      
        if time.time() % 1 > 0.6:
          blinking_bar.draw(black,0,white)       
            
 
    pygame.time.wait(15)  
    pygame.display.flip()

