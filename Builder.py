import pygame
import char_builder,lifec,dice_roller,search_Table





pygame.init()
pygame.font.init()
WIDTH,HEIGHT = 1024,700

back_sound = pygame.mixer.music.load("Sounds/menu_sound.mp3")
background = pygame.image.load("images/background.jpg")
background = pygame.transform.scale(background,(1024,720))
colors ={
   "white" : (255,255,255),
   "black" : (0,0,0),
   "red" : (255,0,0),
   "green" : (0,255,0),
   "blue" : (0,0,255),
   "gray" : (125,125,125)
}
class rect_:
   def __init__(self,x,y,w, h ,button):
      
      self.x = x
      self.y = y
      self.w = w
      self.h =h 
      self.button = button
      self.button = pygame.transform.scale(self.button,(self.w,self.h))
      self.colide = pygame.rect.Rect(self.x,self.y,self.w,self.h)
   def display(self,screen):  
      screen.blit(self.button,(self.x,self.y))


def design_opening(screen):
   
   fade_img = pygame.Surface((1280,720)).convert_alpha()
   fade_img.fill(colors["black"])
   fade_alpha = float(255)
   fade_alpha2 = float(255)
   fade = fade_img.get_rect()
   crushdie = True
   screen.fill(colors["black"])
   logo = pygame.image.load("images/logo_dnd.jpeg")
   logo = pygame.transform.scale(logo,(600,300))
   rect = logo.get_rect(center = (WIDTH / 2, HEIGHT / 2 ))
   while fade_alpha > 0:
    fade_img.set_alpha(fade_alpha)
    screen.blit(logo,(rect))
    screen.blit(fade_img, fade)
    fade_alpha -= 0.3
    pygame.display.update()
    
   logo_gygax = pygame.image.load("images/logo_gygax.png")
   logo_gygax = pygame.transform.scale(logo_gygax,(550,700))
   rect1 = logo_gygax.get_rect(center = (WIDTH / 2, HEIGHT / 2 ))
   fade_img.fill(colors["black"])
   crush_n_die = pygame.mixer.Sound("Sounds/crush_and_die.wav") 
   x = 230
   i = 0.05
   
   while fade_alpha2 > 0:
    for event in pygame.event.get():
         if event.type == pygame.QUIT:
               pygame.quit()
    if fade_alpha2 < x and crushdie == True:
         crush_n_die.play()
         x = 250
         crushdie = False
    fade_img.set_alpha(fade_alpha2)
    screen.blit(logo_gygax,rect1)
    screen.blit(fade_img, fade)
    i += 0.002
    fade_alpha2 -= i
    pygame.display.update()

def draw_rect(button):
   global HEIGHT,WIDTH
   rect = []
   for i in range(5):
      r = rect_(10, HEIGHT * 0.1 + (i* 100),WIDTH * 0.19,HEIGHT  * 0.11,button)
      rect.append(r)
   return rect   
sound = True

def call_extern(sel):
   global sound

   match sel:
      
      case 0:
       
        char_builder.main()
        
        
      case 1:
  
         lifec.main()
         
      case 2:
   
         dice_roller.main()
         
      case 3:
         
       search_Table.main()
         
      case 4:
        
         return False
   return True            
  

def main():
 global WIDTH,HEIGHT,background
 menu_button  = pygame.image.load("images/button_red.png")
 sound_rect = pygame.rect.Rect(WIDTH * 0.92,HEIGHT * 0.85, 100,100)
 button_sound = pygame.image.load("images/sound_image.png")
 button_sound = pygame.transform.scale(button_sound,(sound_rect.w,sound_rect.h))  
 button_nosound = pygame.image.load("images/nosound_image.png")
 button_nosound = pygame.transform.scale(button_nosound,(sound_rect.w,sound_rect.h))  
 global sound
 screen = pygame.display.set_mode([WIDTH, HEIGHT],pygame.RESIZABLE)
 pygame.display.set_caption("Dnd 3.5 Builder")
 
 font = pygame.font.Font(None, 32)
 rect = draw_rect(menu_button) 
 menu_text = ["Char Builder","Life Counter", "Dice Roller", "Search Table","Quit"] 
 running = True
 sound_button = button_sound
 design_opening(screen) 
 pygame.mixer.music.play(-1)
 pygame.mixer.music.set_volume(0.1) 
 while running == True:
   
   font = pygame.font.Font(None, int( WIDTH * 0.03))
   pygame.display.set_caption("Dnd 3.5 Builder")
 
   screen.blit(background,(0,0))
   screen.blit(sound_button,(sound_rect.x,sound_rect.y))
   for j in range(len(rect)):
      i = rect[j]
      text =  font.render(f"{menu_text[j]}",1,colors["white"])
      text_surface = text.get_rect(center = (i.x +(i.w/2),i.y + (i.h/2) ))
      i.display(screen)
      screen.blit(text,text_surface)
   
   for event in pygame.event.get():
      if event.type == pygame.VIDEORESIZE:
          WIDTH = event.w
          HEIGHT = event.h
          screen = pygame.display.set_mode([WIDTH, HEIGHT],pygame.RESIZABLE)
          sound_rect = pygame.rect.Rect(WIDTH * 0.92,HEIGHT * 0.85, 100,100)
          menu_button  = pygame.image.load("images/button_red.png")
          menu_button = pygame.transform.scale(menu_button,(WIDTH * 0.19,HEIGHT * 0.11))
          rect = draw_rect(menu_button) 
          background = pygame.image.load("images/background.jpg")
          background = pygame.transform.scale(background,(WIDTH,HEIGHT))


          button_sound = pygame.transform.scale(button_sound,(sound_rect.w,sound_rect.h))  
      if event.type == pygame.MOUSEBUTTONDOWN:
         if event.button == 1:
            for i in range(5):
               if rect[i].colide.collidepoint(event.pos):
                 

                  running = call_extern(i)
                  if i == 1:
                   sound = False
                   sound_button = button_nosound
                   pygame.mixer.music.set_volume(0.0001) 
                  
               elif sound_rect.collidepoint(event.pos):
                  sound  = not sound
                  if sound == True:
                     sound_button = button_sound
                     pygame.mixer.music.set_volume(0.1) 
                  else:
                     sound_button = button_nosound
                     pygame.mixer.music.set_volume(0.0) 
      elif event.type == pygame.QUIT:
         running = False


   pygame.time.wait(15) 
   pygame.display.update()     

 pygame.quit()

if __name__ == '__main__':
 
   main()

   