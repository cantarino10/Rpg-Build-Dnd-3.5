import pygame
import time
import random,multiprocessing


pygame.init()
pygame.font.init()

WIDTH = 1024
HEIGTH = 720
font = pygame.font.Font(None, 28)
white = (255,255,255)
black = (0,0,0)
display = pygame.display.set_mode([WIDTH,HEIGTH])
pygame.display.set_caption("Dice Roller")

background = pygame.image.load("images/background.jpg")
background = pygame.transform.scale(background, (WIDTH,HEIGTH))

class dice_rect:
      def __init__(self,x,y,w =55,h = 60):
          self.x = x
          self.y = y
          self.w = w
          self.h = h 
          self.colide = pygame.Rect(self.x,self.y,self.w,self.h) 
          self.img = ""
      
      def show(self):
          display.blit(self.img,(self.x,self.y))
         
def create_rect(*a):
    
    rectang = []
    for i in a:
        r = pygame.rect.Rect(i.x + 80,i.y + 10,i.w *0.65,i.h * 0.45)
        rectang.append(r)
    return rectang

def import_dice(dice):

    img = pygame.image.load(f"images/{dice}.png")
    return pygame.transform.scale(img,(60,60))

d4,d6,d8,d10,d12,d20,d100 = dice_rect(10,40),dice_rect(10,140),dice_rect(10,240),dice_rect(10,340),dice_rect(10,440),dice_rect(10,540),dice_rect(10,640) 
dice_var = [d4,d6,d8,d10,d12,d20,d100]


def type_func(txt,rec):
    typing = True
    text = str(txt)
    while typing == True:
      pygame.draw.rect(display,white,rec)
      textx = font.render(f"{text}",1,black)
      display.blit(textx,(rec.x + 2,rec.y + 4))
    

      if time.time() % 1 > 0.5:
            bar = pygame.Rect(rec.x + (len(text) *((rec.w*0.95 )/3) -1),rec.y + 1,2,25)
            pygame.draw.rect(display,(0,0,0),bar,) 
      pygame.display.update()      
      for event in pygame.event.get():
           if event.type == pygame.MOUSEBUTTONDOWN:
               if not pygame.rect.Rect(rec.x,rec.y,rec.w,rec.h).collidepoint(event.pos):
                   return text
           if event.type == pygame.KEYDOWN:
               if event.key == pygame.K_ESCAPE:
                   return text
               
               elif event.unicode.isdigit() and len(text) < 3:
                   text += event.unicode
                   
               elif event.key == pygame.K_BACKSPACE:
              
                   text = text[:-1]    
               elif event.key == pygame.K_KP_ENTER or event.key == pygame.K_RETURN:
                   return text    
           elif event.type == pygame.QUIT:
               return

def roll_dice(dice,number):
    value = []
    for i in range(number):
      value.append(random.randint(1,dice) )
  
    return value  

def show_result(value,x,y):
   
   j =0
   h = 0
   fonte =  pygame.font.Font(None, 32)
   for i in value:  
       if j > 69:
           h += 20
           j = 0
       text = fonte.render(f"{i}, ",1,white)
       display.blit(text,((x + 110 ) + (j*10) + 30,y + h))
     
       j+= 3 
   sumd = sum(value)   
   text = pygame.font.Font(None,40).render(f"{sumd}",1,white)
   display.blit(text,(x, y + 40))
   return sumd
  
   
           
def main():
    
    pygame.display.set_caption("Dice Roller")
    reset_rect = []
    Rolling = True
    dice_count = [0,0,0,0,0,0,0]
    reset_button = pygame.image.load("images/reset_button.png")
    reset_button = pygame.transform.scale(reset_button,(50,50))
    input_rect = create_rect(*dice_var)
    dices = [4,6,8,10,12,20,100]
    sum_dices,dice_value = [0,0,0,0,0,0,0],[0,0,0,0,0,0,0]
    clear_button = pygame.image.load("images/clear_button.png")
    clear_button = pygame.transform.scale(clear_button,(100,50))
    clear_button_rect = dice_rect(WIDTH * 0.9,3,100,50)
    roll_button = pygame.image.load("images/ROLL_button.png")
    roll_button = pygame.transform.scale(roll_button,(100,55))    
    roll_button_rect = dice_rect(clear_button_rect.x - 110,2,100,50)
    hand_cursor = pygame.image.load("images/hand_cursor.png")    
    hand_cursor = pygame.transform.scale(hand_cursor,(20,20))
    
    for i in input_rect:
        r = pygame.rect.Rect(i.x + i.w  , i.y -10 ,50,50)
        reset_rect.append(r)

    mouse = True
  
    while Rolling == True:
             
        display.blit(background,(0,0))
        j = 0
        for i in input_rect:
            display.blit(reset_button,(reset_rect[j].x,reset_rect[j].y))
            display.blit(clear_button,(WIDTH * 0.90,3))
            display.blit(roll_button,(roll_button_rect.x,roll_button_rect.y))

            pygame.draw.rect(display,white,i)
            text = font.render(f"{dice_count[j]}",1,black)
            display.blit(text,(i.x +2,i.y+4))
            j+= 1

        d4.img = import_dice("d4")
        d6.img = import_dice("d6")
        d8.img = import_dice("d8")
        d10.img = import_dice("d10")
        d12.img = import_dice("d12")
        d20.img = import_dice("d20")
        d100.img = import_dice("d100")
        
        d4.show(),d6.show(),d8.show(),d10.show(),d12.show(),d20.show(),d100.show()
       
        pos = pygame.mouse.get_pos()
        

        for event in pygame.event.get():
           if clear_button_rect.colide.collidepoint(pygame.mouse.get_pos()) or roll_button_rect.colide.collidepoint(pygame.mouse.get_pos()):
                mouse = False
              
           else:
              mouse = True   
           for i in range(7):
                if dice_var[i].colide.collidepoint(pygame.mouse.get_pos()) or reset_rect[i].collidepoint(pygame.mouse.get_pos()):
                    mouse = False
               
           if event.type == pygame.KEYDOWN:
               if event.key == pygame.K_ESCAPE:
                   return
           elif event.type == pygame.QUIT:
               return
           elif event.type == pygame.MOUSEBUTTONDOWN:
               if event.button == 1:
                if clear_button_rect.colide.collidepoint(event.pos):
                    dice_count = [0,0,0,0,0,0,0]
                    dice_value = [0,0,0,0,0,0,0]
                    sum_dices = [0,0,0,0,0,0,0]

                if roll_button_rect.colide.collidepoint(event.pos):
                    for i in range(7):
                        if dice_count[i] != 0:
                         dice_value[i] = (roll_dice(dices[i],int(dice_count[i])))

                for i in range(len(input_rect)):
                 
                  if input_rect[i].collidepoint(event.pos):
                         dice_count[i] = int(type_func(dice_count[i],input_rect[i]))
                         break
                  elif reset_rect[i].collidepoint(event.pos):
                         dice_count[i] = 0
                         dice_value[i] = 0
                         
                         pygame.display.update()
                         break
                  elif dice_var[i].colide.collidepoint(event.pos) and dice_count[i] != 0:
                         dice_value[i] = (roll_dice(dices[i],int(dice_count[i])))
        
        for i in range(7):
           if dice_value[i] != 0 :
               sum_dices[i] = show_result(dice_value[i],input_rect[i].x,input_rect[i].y)                 
       
        text = pygame.font.Font(None,40).render(f"Total = {sum(sum_dices)}",1,black)
        display.blit(text,(400,3))
        if not mouse:
          pygame.mouse.set_visible(False)
          display.blit(hand_cursor,pos)    
        else:
           pygame.mouse.set_visible(True) 




        pygame.time.wait(5)  
        pygame.display.flip()


