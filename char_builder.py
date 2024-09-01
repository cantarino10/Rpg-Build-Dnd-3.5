import pygame
import random
import os
import pandas as pd
import time
import multiprocessing


pygame.init()
pygame.font.init()

WIDTH = 1024
HEIGTH = 720
font = pygame.font.Font(None, 25)
white = (255,255,255)
black = (0,0,0)
display = pygame.display.set_mode([WIDTH,HEIGTH])
pygame.display.set_caption("RPG 3.5 Character Builder")


running = True

class weapons:  # Class to load weapons and yoru caracteristics
   def __init__(self):
      self.simple = pd.read_excel("Weapons/Light Weapons.xlsx", sheet_name= "Planilha1",index_col= 0)
      self.martial = pd.read_excel("Weapons/Light Weapons.xlsx",sheet_name="Planilha2",index_col=0)
      self.exotic= pd.read_excel("Weapons/Light Weapons.xlsx", sheet_name= "Planilha3",index_col= 0)
      self.all = pd.concat([self.simple,self.martial,self.exotic])
      self.know = [""]   
     

class armors: # Class to load armors and your characteristics
   def __init__(self)      :
     self.armor_all = pd.read_excel("Weapons/Light Weapons.xlsx", sheet_name= "Planilha4",index_col= 0)
     self.shield_all = pd.read_excel("Weapons/Light Weapons.xlsx", sheet_name= "Planilha5",index_col= 0)
     
     self.know = "" 
     self.names = []

   def select(self):
      if self.know != "":
        for i in range(len(self.armor_all)):
          
           if self.armor_all.iloc[i]["Category"] in self.know:
              self.names.append(self.armor_all.index[i])
   


class rectang:  #Class to draw rectangles
    def __init__(self,x,y,w,h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.colide = pygame.Rect(self.x,self.y,self.w,self.h)
        
class data: #Character Caracteristics class
   def __init__(self):
     self.weapon = ""
     self.Name = ""
     self.lvl = 1
     self.race = ""
     self.clas = ""
     self.feat = 0 
     self.BBA = 0
     self.meele_attack = 0
     self.ranged_attack = 0
     self.hp = 0
     self.initiaive = 0
     self.fort = 0
     self.ref = 0
     self.will = 0
     self.skills = {}
     self.nskills = 0
     self.mskill = 0
     self.hd = 0
     self.tBBA = []
     self.speed = 30
     self.ca = 0
     self.size = "Medium" 
     self.armor = ""
     self.shield_proficiency = []
     self.shield = ""
   

   def matributes(self):  # Atributes modifiers
     global atr_mod
    
     self.mstr = mod_calculator(self.str)
     self.mdex = mod_calculator(self.dex)
     self.mcon = mod_calculator(self.con)
     self.mint = mod_calculator(self.int)
     self.mwis = mod_calculator(self.wis)
     self.mcha = mod_calculator(self.cha)
     atr_mod = [self.mstr,self.mdex,self.mcon,self.mint,self.mwis,self.mcha]
     
   
   def atributes(self,*matr):   #Atributes
     self.str = matr[0]
     self.dex = matr[1]
     self.con = matr[2]
     self.int = matr[3]
     self.wis = matr[4]
     self.cha = matr[5]
   def atributes_to_list(self):
      global atribut
      atribut = [self.str,self.dex,self.con,self.int,self.wis,self.cha]

   def display_header(self):
      font = pygame.font.Font(None,30)
      text = font.render(f"{self.Name}",1,black)  
      display.blit(text,(name_rect.x + 1,name_rect.y + 5))
      text = font.render(f"{self.lvl}",1,black)  
      display.blit(text,(lvl_rect.x + 2,lvl_rect.y + 7))
      text = font.render(f"{self.clas}",1,black)
      display.blit(text,(class_rect.x + 1,class_rect.y +5))
      text = font.render(f"{self.race}",1,black)
      display.blit(text,(race_rect.x + 1,race_rect.y +5))
   
   def class_csv(self):
      nv = self.lvl - 1
      class_data = pd.read_csv(f"Classes/{char.clas}.csv")   
 
      self.BBA = int(class_data["BBA"][nv])
      self.fort = int(class_data["Fort"][nv]) + self.mcon
      self.ref = int(class_data["Refl"][nv]) + self.mdex
      self.wil = int(class_data["Vont"][nv]) + self.mwis
      self.nskills = 0
      self.hd = int(class_data["Hit Die"][0])
      self.mskill = int(class_data["Skill multiplier"][0]) 
      self.nskills += ((self.mskill + self.mint) * (nv + 4))
      self.initiaive = self.mdex
      self.meele_attack = self.BBA + self.mstr
      self.ranged_attack = self.BBA + self.mdex
      self.tBBA = []
      self.ca += self.mdex
      i = 0
      self.abilities = []
      if char.clas == "Bard":
       self.abilities = ["Bardic music,bardic knowledge,"]

      for ab in class_data["Habilidades"]:
          self.abilities.append(ab)  
          i+=1
          if i >= nv:
             break
      if self.BBA < 6:
         self.tBBA = [self.BBA]
         
      else:   
        for i in range(int(self.BBA/ 3) ):
           if self.BBA - (5 * i) >0:
            self.tBBA.append(self.BBA - (5 * i))
    
     
      i = nv
      r = 0
    
      while i > 0 :
         r += random.randint(1,self.hd)
         i -=1
      self.hp = self.hd + r + (self.mcon * self.lvl)
   
   def distribut_skills(self):
 
      safety = 0   
      x = self.nskills
      limit = self.lvl + 3
      h = list(self.skills.keys())
      while x > 0 and safety <99:
       
         rd = random.randint(1, len(h)) - 1
        
         if x > limit:
            aux = random.randint(1, limit)
            
         else:
            aux = random.randint(1, x)   
            
         skill = h[rd]
         if  (self.skills[skill] + aux) <= limit:
           self.skills[skill] += aux
           
           x -= aux
         else:
            add = limit - self.skills[skill]
            self.skills[skill] += add
            x -= add
            safety += 1
      
      for  i in self.skills:
         if "(Str)" in i :
            self.skills[i] += self.mstr
         elif "(Dex)" in i :
            self.skills[i] += self.mdex
         elif "(Int)" in i:
            self.skills[i] += self.mint
         elif "(Con)" in i:
            self.skills[i] += self.mcon
         elif "(Wis)" in i:
            self.skills[i] += self.mwis
         elif "(Cha)" in i:
            self.skills[i] += self.mcha
            
def show_atributes(atribute,modifier):
    display.fill(black)
    for i in range(6):
      pygame.draw.rect(display,white,atribute[i])
      pygame.draw.rect(display,white,modifier[i])
      

def const_atribute_rect():
    global WIDTH,HEIGTH
    recs = [] 
    recs_mod = []   
    for i in range(6): 
       for j in range(2): 
        rect = pygame.Rect(50 + ((j * WIDTH * 0.045) + 5)  ,HEIGTH * 0.12 + (i * ((HEIGTH * 0.04) + 5) ), WIDTH * 0.04, HEIGTH * 0.04)
        if j == 0:
            recs.append(rect)
        else:
            recs_mod.append(rect)    
        
    return recs,recs_mod      

def random_atributes():
    mod = []
    roll = True
    while roll == True:
      total = []  
      for j in range(6):  
        sume = []
        for i in range(4) :
             sume.append(random.randint(1,6))
        sume.sort()
        sume = sume[-3::]
        sumat = sum(sume)
        if sumat >= 14:
         roll = False
        total.append(sumat)    
    for i in total:
       if i >= 10:
          mod.append(int((i - 10) / 2))
       else:
          mod.append(int((i-11) / 2)       )
   
    return total,mod
    
def display_atribute(rec,modrec,atr,mod):
   show_atributes(atr_rect,mod_rect)
   i = 0
   font = pygame.font.Font(None, 30)
   sumt = 0
   for rect in rec:
      text = font.render(f"{atr[i]}",1,black)
      text_center = text.get_rect(center = ( 25 + rect.x + (rect.w - rect.x)/2, rect.y + (rect.w/2) ))
      display.blit(text, text_center)
      
      text = font.render(f"{mod[i]}",1,black)
      text_center = text.get_rect(center = (modrec[i].x + (modrec[i].w)/2, modrec[i].y + (modrec[i].w/2) ))
      display.blit(text, text_center)
      sumt += atr[i]
      i += 1  
   text = font.render(f"{sumt}",1,white)
   text_center = text.get_rect(center =(25 + rec[5].x + (rec[5].w - rec[5].x)/2, dice.y + (dice.w/2) ))
   display.blit(text,text_center) 
   show_rects()
   show_titles()
   char.display_header()
 

def show_titles():
  font = pygame.font.Font(None, 30)
  text = font.render("Name",1,white)
  text_center = text.get_rect(center =((( name_rect.x + name_rect.w ) / 2), (name_rect.y ) / 2))
  display.blit(text,text_center)  
  text = font.render("Lvl",1,white)
  text_center = text.get_rect(center =(( lvl_rect.x +( lvl_rect.w  / 2), (name_rect.y ) / 2)))
  display.blit(text,text_center)  
  text = font.render("Race",1,white)
  text_center = text.get_rect(center =(( race_rect.x +( race_rect.w  / 2), (name_rect.y ) / 2)))
  display.blit(text,text_center)  
  text = font.render("Class",1,white)
  text_center = text.get_rect(center =(( class_rect.x +( class_rect.w  / 2), (name_rect.y ) / 2)))
  display.blit(text,text_center)  

  text = font.render("STR",1,white)
  display.blit(text,(7, atr_rect[0].y + 5) )  
  text = font.render("DEX",1,white)
  display.blit(text,(7, atr_rect[1].y + 5) )  
  text = font.render("CON",1,white)
  display.blit(text,(7, atr_rect[2].y + 5) )  
  text = font.render("INT",1,white)
  display.blit(text,(7, atr_rect[3].y + 5) )  
  text = font.render("WIS",1,white)
  display.blit(text,(7, atr_rect[4].y + 5) )  
  text = font.render("CHA",1,white)
  display.blit(text,(7, atr_rect[5].y + 5) )  
  
  
def show_rects():
   pygame.draw.rect(display,white,name_rect.colide) 
   pygame.draw.rect(display,white,lvl_rect.colide)  
   
   pygame.draw.rect(display,white,race_rect.colide)
 
   pygame.draw.rect(display,white,class_rect.colide)
def class_race_rect_show():
   pygame.draw.rect(display,white,race_show_rect.colide)
   pygame.draw.rect(display,white,class_show_rect.colide)

def get_input(text, type,x,y,txt_len,only_number):
   typing = True
   w = 0
   while typing:
      pygame.draw.rect(display,white,type)   
      if time.time() % 1 > 0.5:
           bar = pygame.Rect(x + w,y + 1,2,33)
           pygame.draw.rect(display,(0,0,0),bar,) 
      font = pygame.font.Font(None,30)
      text_to_show = font.render(f"{text}",1,black)
      text_rect = text_to_show.get_rect()
      w  = text_rect.w 
      display.blit(text_to_show,(x + 1,y + 5))     
      pygame.display.update()
      for event in pygame.event.get():
         if event.type == pygame.QUIT:
            pygame.quit()
         if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
               typing = False
               if only_number == True and text == "":
                  text = 1
                  
            elif event.key == pygame.K_BACKSPACE:
               text = text [:-1]
            elif only_number == True: 
                if event.unicode.isdigit() and len(text) < 2:
                   text = text + event.unicode

            elif len(text) < txt_len:
               
               text = text + event.unicode 
            else:
               pass     
    
   return text

def display_classes(*probability):
  
   
   global classes_text,race_text

   i= 0
   for classe in classes_text:
      text = font.render(f"{classe}",1,black)
      display.blit(text,(class_show_rect.x + 2,class_show_rect.y + 2 + (i * 25)))
      if i > 0:    
       prob = probability[i - 1] * 100
       text = font.render(f"{prob:.1f}%",1,black)
       display.blit(text,(class_show_rect.x + class_rect.w - 50,class_show_rect.y + 2 + (i * 25)))
      i += 1
   i = 0   
   for race in race_text:
      text = font.render(f"{race}",1,black)
      display.blit(text,(race_show_rect.x + 2,race_show_rect.y + 2 +(i*25)))
      i += 1


def creat_rect_class(option):
      rect_classes = []
      for dire,subpaste,files in os.walk(option):
        i = 0
        classes = ["Random"]
        if option == "Classes":
         rect_classes  = [pygame.Rect(class_show_rect.x + 2,class_show_rect.y + 2 +(i * 25),class_show_rect.w,class_show_rect.h/20)]
         i = 1
         for names in files:
            classes.append(names[:-4])
            recs = pygame.Rect(class_show_rect.x + 2,class_show_rect.y + 2 +(i * 25),class_show_rect.w,class_show_rect.h/20)
            i += 1
            rect_classes.append(recs)  
        else:
          rect_classes  = [pygame.Rect(race_show_rect.x + 2,class_show_rect.y + 2 +(i * 25),class_show_rect.w,class_show_rect.h/20)]
          i = 1
          for names in files:            
            classes.append(names[:-4])
            recs = pygame.Rect(race_show_rect.x + 2,race_show_rect.y + 2 +(i * 25),race_show_rect.w,class_show_rect.h/20)
            i += 1
            rect_classes.append(recs)   
         
      return rect_classes,classes

def class_probab():
   atrib = [char.mstr,char.mdex,char.mcon,char.mint,char.mwis,char.mcha]
   p = pd.read_csv("class_probabilities.csv", index_col = 0)
   probability = list( p.index)
   final_probability = []
   for i in probability:
      val = p.loc[i].mul(atrib) 
    
      val = val.sum()
      if val < 0:
         val = 0
      final_probability.append(val)

   final_probability =pd.Series(final_probability, index=probability)
   total = final_probability.sum()
   final_probability = final_probability.div(total)
   final_probability = list(final_probability.values)
    
     
   return final_probability,probability


def mod_calculator(atribut):

   if atribut >= 10:
      atr_mod = int((atribut - 10) / 2)
   else:
      atr_mod = int((atribut-11) / 2)      
   return atr_mod

def race_adjustment():

   match char.race:
      
      case "Dwarf":
         char.speed = 20
         char.con += 2
         char.cha -= 2
        
      case "Elf":
        
         char.dex += 2
         char.str -= 2
      case "Gnome":
         char.size = "Small"
         char.skills["Craft(Alchemy) (Int)"] = 2 
         char.con -= 2
         char.str+=2  
      case "Half-Elf":
       pass
      case "Half-Orc":
         char.str+=2
         char.wis-=2
         char.cha-=2
      case "Halfling":
         char.size = "Small"
         char.str -=2
         char.dex +=2
      case "Human":
         char.feat += 1
         char.nskills += 3 + char.lvl 

def class_adjustment():

   match char.clas:
      case "Barbarian":
         armor.know = ["Light", "Medium"]
         char.shield_proficiency = list(armor.shield_all.index[:-1])
         weapon.know = list(weapon.simple.index) + list(weapon.martial.index)   
         char.skills = {
            "Climb (Str)" : 0 ,
            "Craft (Int)" : 0 ,
            "Handle Animal (Cha)" : 0  ,
            "Intimidate (Cha)" : 0  , 
            "Jump (Str)" : 0 , 
            "Listen (Wis)" : 0 ,
            "Ride (Dex)" : 0 , 
            "Survival (Wis)" : 0 , 
            "Swim (Str)" : 0 

         }
      case "Bard" :
          armor.know = ["Light"]
          char.shield_proficiency = list(armor.shield_all.index[:-1])
          weapon.know = list(weapon.simple.index) + ["Longsword","Rapier","Shortsword","Shortbow","Whip"]
          char.skills = {
            "Appraise (Int)" :0 , 
            "Balance (Dex)" : 0 , 
            "Bluff (Cha)" : 0 ,
            "Climb (Str) " : 0 ,
            "Concentration (Con)" :0 , 
            "Craft (Int)" : 0 , 
            "Decipher Script (Int)" : 0 , 
            "Diplomacy (Cha)" : 0 , 
            "Disguise (Cha)" : 0 , 
            "Escape Artist (Dex)"  : 0 ,
            "Gather Information (Cha)" : 0 , 
            "Hide (Dex)" : 0 , 
            "Jump (Str)": 0 , 
            "Knowledge(Arcana) (Int)" :0 ,
            "Knowledge(Architeture) (Int)" : 0,
            "Knowledge(Dungeon) (Int)" : 0,
            "Knowledge(Geography) (Int)" : 0,
            "Knowledge(History) (Int)" : 0,
            "Knowledge(Local) (Int)": 0,
            "Knowledge(Nature) (Int)": 0,
            "Knowledge(Nobility) (Int)" : 0,
            "Knowledge(Religion) (Int)" : 0, 
            "Knowledge(The Planes) (Int)" : 0,
            "Listen (Wis)" : 0 , 
            "Move Silently (Dex)" : 0 ,
            "Perform (Cha)" : 0  , 
            "Profession (Wis)" :0 , 
            "Sense Motive (Wis)" : 0  , 
            "Sleight of Hand (Dex)" : 0 , 
            "Speak Language (None)" : 0, 
            "Spellcraft (Int)" : 0,  
            "Swim (Str)" : 0 , 
            "Tumble (Dex)" : 0 , 
            "Use Magic Device (Cha)" : 0 

         }  
      case "Cleric":
        weapon.know = list(weapon.simple.index)
        char.shield_proficiency = list(armor.shield_all.index[:-1])
        armor.know = ["Light","Medium","Heavy"]
        char.skills = {   
            "Concentration (Con)" : 0 , 
            "Craft (Int)" : 0 , 
            "Decipher Script (Int)" : 0 , 
            "Diplomacy (Cha)" : 0 , 
            "Heal (Wis)" : 0 , 
            "Knowledge(Arcana) (Int)" : 0 ,
            "Knowledge(History) (Int)" : 0,
            "Knowledge(Religion) (Int)" : 0, 
            "Knowledge(The Planes) (Int)" : 0,
            "Profession (Wis)" :0 , 
            "Spellcraft (Int)" : 0  
         }
      case  "Druid":
         armor.names = ["Padded","Leather","Hide"] 
         char.shield_proficiency = ["Shield, light wooden","Shield, heavy wooden"]
         weapon.know = ["Club", "Dagger", "Dart", "Quarterstaff", "Scimitar", "Sickle", "Shortspear", "Sling", "Spear"]
         char.skills = {   
            
            "Concentration (Con)" : 0 , 
            "Craft (Int)" : 0 , 
            "Diplomacy (Cha)" : 0 , 
            "Disguise (Cha)" : 0 , 
            "Escape Artist (Dex)"  : 0 ,
            "Gather Information (Cha)" :0, 
            "Handle Animal(Cha)" : 0,
            "Heal (Wis)" : 0,
            "Knowledge(Nature) (Int)": 0,
            "Listen (Wis)" :0, 
            "Profession (Wis)" :0, 
            "Ride (Dex)" : 0,
            "Spellcraft (Int)" : 0,  
            "Survival (Wis)" : 0,
            "Swim (Str)" : 0
           

         }
      case "Fighter"  :
         armor.know = ["Light", "Medium", "Heavy"]
         char.shield_proficiency = list(armor.shield_all.index[:])
         weapon.know = list(weapon.simple.index) + list(weapon.martial.index)
         char.skills = {
            
            "Climb (Str) " :0,
            "Craft (Int)" : 0, 
            "Handle Animal (Cha)" : 0,
            "Intimidate (Cha)" : 0,           
            "Jump (Str)": 0, 
            "Ride (Dex)" : 0,
            "Swim (Str)" :0
            
         }
      case "Monk" :
         
         weapon.know = ["Unarmed Strike","Club", "Crossbow, light", "Crossbow, heavy", "Dagger", "Handaxe", "Javelin", "Kama", "Nunchaku", "Quarterstaff", "Sai", "Shuriken", "Siangham"]
         char.skills = {
            
            "Balance (Dex)" : 0, 
            "Climb (Str) " : 0,
            "Concentration (Con)" :0, 
            "Diplomacy (Cha)" : 0, 
            "Escape Artist (Dex)"  : 0,
            "Hide (Dex)" : 0, 
            "Jump (Str)": 0, 
            "Knowledge(Arcana) (Int)" : 0,
            "Knowledge(Religion) (Int)" : 0, 
            "Listen (Wis)" : 0, 
            "Move Silently (Dex)" : 0,
            "Perform (Cha)" :0, 
            "Profession (Wis)" :0, 
            "Sense Motive (Wis)" :0, 
            "Sleight of Hand (Dex)" : 0, 
            "Spot (Wis)" : 0, 
            "Swim (Str)" : 0, 
            "Tumble (Dex)" : 0
            
         }   
      case "Paladin":
         armor.know = ["Light", "Medium", "Heavy"]
         char.shield_proficiency = list(armor.shield_all.index[:-1])
         weapon.know = list(weapon.simple.index) + list(weapon.martial.index)
         char.skills = {
        
            "Concentration (Con)" : 0, 
            "Craft (Int)" : 0, 
            "Handle Animel (Cha)" : 0,
            "Heal (Wis)" : 0,
            "Knowledge(Nobility) (Int)" : 0,
            "Knowledge(Religion) (Int)" : 0, 
            "Profession (Wis)" :0, 
            "Ride (Dex)" : 0,
            "Sense Motive (Wis)" : 0
            
         }  
      case "Ranger":
         armor.know = ["Light", "Medium"]
         char.shield_proficiency = list(armor.shield_all.index[:-1])
         weapon.know = list(weapon.simple.index) + list(weapon.martial.index)
         char.skills = {
          
            "Climb (Str) " : 0,
            "Concentration (Con)" : 0, 
            "Craft (Int)" : 0, 
            "Handle Animal(Cha)" : 0,
            "Heal (Wis)" : 0,
            "Hide (Dex)" : 0, 
            "Jump (Str)": 0, 
            "Knowledge(Dungeon) (Int)" : 0,
            "Knowledge(Geography) (Int)" : 0,
            "Knowledge(Nature) (Int)": 0,
            "Listen (Wis)" : 0, 
            "Move Silently (Dex)" : 0,
            "Profession (Wis)" :0, 
            "Ride (Dex)" : 0,
            "Search (Int)" : 0,   
            "Survival (Wis)" : 0,
            "Swim (Str)" : 0, 
            "Use Rope (Dex))" : 0

         }  
      case "Rogue":  
         armor.know = ["Light"]   
         char.shield_proficiency = ""
         weapon.know = list(weapon.simple.index) + ["Crossbow, hand", "Rapier", "Sap", "Shortbow", "Shortsword"]
         char.skills = {
            "Appraise (Int)" :0  , 
            "Balance (Dex)" : 0, 
            "Bluff (Cha)" : 0,
            "Climb (Str) " : 0,
            "Craft (Int)" : 0, 
            "Decipher Script (Int)" : 0, 
            "Diplomacy (Cha)" : 0,
            "Disable Device (Int)" : 0, 
            "Disguise (Cha)" : 0, 
            "Escape Artist (Dex)"  :0,
            "Gather Information (Cha)" : 0, 
            "Hide (Dex)" : 0, 
            "Intimidate (Cha)" : 0,
            "Jump (Str)": 0, 
            "Listen (Wis)" : 0, 
            "Move Silently (Dex)" : 0,
            "Open Lock (Dex)" : 0,
            "Perform (Cha)" : 0, 
            "Profession (Wis)" :0, 
            "Search (Int)" :0,
            "Sense Motive (Wis)" : 0, 
            "Sleight of Hand (Dex)" : 0, 
            "Spot (Wis)" : 0, 
            "Spellcraft (Int)" : 0,  
            "Swim (Str)" : 0, 
            "Tumble (Dex)" : 0, 
            "Use Magic Device (Cha)" :0,
            "Use Rope (Dex))" : 0

         }  
      case "Sorcerer": 
         armor.know = ""
         char.shield_proficiency = ""
         weapon.know = list(weapon.simple.index) 
         char.skills = {
           
            "Bluff (Cha)" : 0,
            "Concentration (Con)" : 0, 
            "Craft (Int)" :0, 
            "Knowledge(Arcana) (Int)" : 0,
            "Profession (Wis)" :0, 
            "Spellcraft (Int)" : 0  
            
         }  
      case "Wizard":
         armor.know = ""
         char.shield_proficiency = ""
         weapon.know = ["Club", "Dagger", "Crossbow, heavy", "Crossbow, light","Quarterstaff"]
         char.skills = {
           
            
            "Concentration (Con)" :0, 
            "Decipher Script (Int)" : 0, 
            "Craft (Int)" : 0, 
            "Knowledge(Arcana) (Int)" : 0,
            "Knowledge(Architeture) (Int)" : 0,
            "Knowledge(Dungeon) (Int)" : 0,
            "Knowledge(Geography) (Int)" : 0,
            "Knowledge(History) (Int)" : 0,
            "Knowledge(Local) (Int)": 0,
            "Knowledge(Nature) (Int)": 0,
            "Knowledge(Nobility) (Int)" : 0,
            "Knowledge(Religion) (Int)" : 0, 
            "Knowledge(The Planes) (Int)" : 0,
            "Profession (Wis)" :0, 
            "Spellcraft (Int)" : 0  
            
            
         }  


def check_skill(skill):         
   if skill in char.skills:
      return True
   else:
      False
def race_skills():
   match char.race:
      
        
       
      case "Elf":
       weapon.know += ["Longsword","Longbow"]
       if check_skill("Spot (Wis)") == True:
          x = char.skills["Spot (Wis)"]
          char.skills["Spot (Wis)"] = x + 2
       else:  
         char.skills["Spot (Wis)"] = 2

       if check_skill("Listen (Wis)") == True:
          x = char.skills["Listen (Wis)"]
          char.skills["Listen (Wis)"] = x + 2
       else:  
         char.skills["Listen (Wis)"] = 2

         
       if check_skill("Search (Int)") == True:
          x = char.skills["Search (Int)"]
          char.skills["Search (Int)"] = x + 2
       else:  
         char.skills["Search (Int)"] = 2
      

      case "Gnome":   
       if check_skill("Listen (Wis)") == True:
          x = char.skills["Listen (Wis)"]
          char.skills["Listen (Wis)"] = x + 2
       else:  
         char.skills["Listen (Wis)"] = 2

      case "Half-Elf":
       if check_skill("Spot (Wis)") == True:
          x = char.skills["Spot (Wis)"]
          char.skills["Spot (Wis)"] = x + 1
       else:  
         char.skills["Spot (Wis)"] = 1

       if check_skill("Listen (Wis)") == True:
          x = char.skills["Listen (Wis)"]
          char.skills["Listen (Wis)"] = x + 1
       else:  
         char.skills["Listen (Wis)"] = 1

         
       if check_skill("Search (Int)") == True:
          x = char.skills["Search (Int)"]
          char.skills["Search (Int)"] = x + 1
       else:  
         char.skills["Search (Int)"] = 1

       if check_skill("Diplomacy (Cha)") == True:
          x = char.skills["Diplomacy (Cha)"]
          char.skills["Diplomacy (Cha)"] = x + 2
       else:  
         char.skills["Diplomacy (Cha)"] = 2

       if check_skill("Gather Information (Cha)") == True:
          x = char.skills["Gather Information (Cha)"]
          char.skills["Gather Information (Cha)"] = x + 2
       else:  
         char.skills["Gather Information (Cha)"] = 2

     
      case "Halfling":
       if check_skill("Climb (Str)") == True:
          x = char.skills["Climb (Str)"]
          char.skills["Climb (Str)"] = x + 2
       else:  
         char.skills["Climb (Str)"] = 2

       if check_skill("Jump (Str)") == True:
          x = char.skills["Jump (Str)"]
          char.skills["Jump (Str)"] = x + 2
       else:  
         char.skills["Jump (Str)"] = 2

         
       if check_skill("Move Silently (Dex)") == True:
          x = char.skills["Move Silently (Dex)"]
          char.skills["Move Silently (Dex)"] = x + 2
       else:  
         char.skills["Move Silently (Dex)"] = 2
       if check_skill("Listen (Wis)") == True:
          x = char.skills["Listen (Wis)"]
          char.skills["Listen (Wis)"] = x + 2
       else:  
         char.skills["Listen (Wis)"] = 2
  
      

def lvl_adjust(*atr):
  
   
   points = int(char.lvl / 4)
   aux = list(atr)
  
   aux2 = list(atr)
   
   aux2.sort()
  
   aux2 = aux2[::-1]
   while points > 0:
      i = 0
      while i < 6:
         if aux2[i] % 2 == 1:
            for j in range(6):
               if aux[j] == aux2[i]:
                  aux[j] += 1
                  points -= 1
                  if points <0:
                     
                     return aux
                  aux2 = aux.copy()
                  aux2.sort()
                  
                  aux2 = aux2[::-1]
                  i = 0
                  break
         i+=1   
      for h in range(6):
         if aux[h] == aux2[0]:
            aux[h] += points
            
            return aux
         
def display_data(text,x,y):
   txt = font.render(f"{text}",1,white)
   display.blit(txt,(x,y))

def display_skills(text,x,y):
   font = pygame.font.Font(None,23)
   txt = font.render(f"{text}",1,white)
   display.blit(txt,(x,y))

def print_skills():
   g = 0
   h = 0
   display_data(f"Skillpoints : {char.nskills} ", class_rect.x + class_rect.w + 40,  class_rect.y + 40)

   for i,j in char.skills.items():
     if g > 25:
        h = 1
        g = 0
     if j > 0:
      display_skills(f"{i} = {j}",race_rect.x +  (race_rect.w * 1.5 ) + (WIDTH * 0.18 *h) , HEIGTH * (0.03 * g) + 35 + ( class_rect.y + class_rect.h))
      g += 1
   pygame.draw.rect(display,white,(race_rect.x +  (race_rect.w * 1.5 ) -10, HEIGTH * 0.13, 380,HEIGTH * 0.81),2)
def update():

  i = 0
  up = True
  while True: 
     
     
      display.fill(black)
      show_rects()
      display_atribute(atr_rect,mod_rect,[char.str,char.dex,char.con,char.int,char.wis,char.cha],atr_mod)   
      if up ==  True:
    
       char.class_csv()
       char.shield_proficiency = ""
   
       shield  = False
       class_adjustment()
       armor.select()
       select_weapon()
   
       if armor.know != "":
        select_armor()
       if char.weapon.Hands == 1 and char.shield_proficiency != "" and char.weapon.Category != "Ranged":
          
          shield = True
          select_shield()
     
       char.distribut_skills()
       race_skills()
       up = False  
      
      display_data(f"Initiative : {char.initiaive}", WIDTH * 0.15, HEIGTH * 0.21)
      display_data(f"Feats : {char.feat}", WIDTH * 0.15, HEIGTH * 0.25)
      display_data(f"HP : {char.hp}", WIDTH * 0.15, HEIGTH * 0.13)
      display_data(f"CA :  {char.ca}",WIDTH * 0.15, HEIGTH * 0.17)
      display_data(f"BBA : {char.BBA}", 10, HEIGTH * 0.51)
      display_data(f"Fortitude : {char.fort}, Reflexes : {char.ref}, Will : {char.wil} ", 10, HEIGTH * 0.63)
      display_data(f"Attack Meele : ", 10, HEIGTH * 0.55)
      display_data(f"Attack Ranged : ", 10, HEIGTH * 0.59)
      escape_font = pygame.font.SysFont("Arial",25,bold= True,italic=True)
      if time.time() % 1 > 0.5:
        return_text = escape_font.render("Press Esc To Return",1,(255,0,0))
        display.blit(return_text,(WIDTH * 0.7,HEIGTH * 0.94))   
      if char.weapon.loc["Category"] != "Ranged":
         dmg = char.mstr * int(char.weapon.loc["Hands"])
      else:
         dmg = 0   
      
      
      display_data(f"Weapon : {char.weapon.name}  = {char.weapon.loc[f"Damage({char.size})"]}  + {dmg}  {char.weapon.loc["Critical"]}" ,10,HEIGTH * 0.8)
      if armor.know != "":
        display_data(f"Armor : {char.armor.name}, Bonus CA : {char.armor.loc["CA Bonus"]}, Max dex : {char.armor.loc["Max Dex"]} ", 10, HEIGTH * 0.84)
      if shield == True  :
         shield_name = char.shield.name
         display_data(f"Shield : {shield_name}, Bonus CA : {char.shield.loc["CA Bonus"]} ", 10, HEIGTH * 0.88)
      
      print_skills()   
     
      for event in pygame.event.get():
         if event.type == pygame.QUIT:
            pygame.quit()
         if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
               return
      x = 0 
     
      for i in char.tBBA:
     
        if x < len(char.tBBA) - 1:
          display_data(f" +{i} /",150 + (x * WIDTH * 0.04), HEIGTH * 0.51)
          display_data(f" +{i + char.mstr} /",150 + (x * WIDTH * 0.04), HEIGTH * 0.55)
          display_data(f" +{i + char.mdex} /",150 + (x * WIDTH * 0.04), HEIGTH * 0.59)  
        else:
           display_data(f" +{i} ",150 + (x * WIDTH * 0.04), HEIGTH * 0.51)
           display_data(f" +{i + char.mstr} ",150 + (x * WIDTH * 0.04),HEIGTH * 0.55)
           display_data(f" +{i + char.mdex} ",150 + (x * WIDTH * 0.04), HEIGTH * 0.59)    
        x += 1 
      j = 0  
      display_data("Class Abilities" , 390,HEIGTH * 0.10)
  
      for i in char.abilities:
         if i != "-":
            display_skills(i,320,HEIGTH * 0.14 + ( j * HEIGTH * 0.035))
            j+= 1
      class_border = pygame.rect.Rect(310,HEIGTH * 0.13,315, (HEIGTH * 0.16) - (HEIGTH * 0.14) +  (j * HEIGTH * 0.035) - 15 )
      pygame.draw.rect(display,white,class_border,2)   
      pygame.display.update()
  
      
def select_weapon():
  
  size = len(weapon.know)
  weapon_know = weapon.know
  if char.dex > char.str:
    
    weapon_know = []
    for i in weapon.know:
       a = weapon.all.loc[i]
       if a.loc["Category"] == "Ranged":
     
          weapon_know.append(a.name)
         

  size = len(weapon_know)       
  rd = random.randint(0, size - 1)
  char.weapon = weapon.all.loc[weapon_know[rd]]
def select_armor():
   size = len(armor.names) 
   rd = random.randint(0, size - 1)
   char.armor = armor.armor_all.loc[armor.names[rd]]
   char.ca = 10 + int(char.armor.loc["CA Bonus"])
   if int(char.armor.loc["Max Dex"]) < char.mdex:
       char.ca += int(char.armor.loc["Max Dex"])
   else:
       char.ca += char.mdex   
   if char.size == "Small":
       char.ca+= 1

def select_shield():
   size = len(char.shield_proficiency) 
   rd = random.randint(0, size - 1)
   char.shield = armor.shield_all.loc[char.shield_proficiency[rd]]
   char.ca += int(char.shield.loc["CA Bonus"])
   

rand = True
char = data()
dice_icon = pygame.image.load("images/reroll2_img.png")
dice_icon = pygame.transform.scale(dice_icon,(WIDTH * 0.05, HEIGTH * 0.05))
dice = rectang( 5, HEIGTH  * 0.4,WIDTH * 0.05,HEIGTH * 0.05)
name_rect = rectang(10,30,WIDTH * 0.25,HEIGTH * 0.05)
lvl_rect = rectang(15 + name_rect.w,30, WIDTH * 0.05,HEIGTH*0.05)
race_show_rect = rectang( 10 +  lvl_rect.x + lvl_rect.w, HEIGTH * 0.12, WIDTH * 0.2, HEIGTH * 0.6)
race_rect = rectang( race_show_rect.x,lvl_rect.y,race_show_rect.w,lvl_rect.h)
class_show_rect = rectang( race_show_rect.x + race_show_rect.w + 10, race_show_rect.y,race_show_rect.w,race_show_rect.h )
class_rect = rectang(class_show_rect.x,race_rect.y,class_show_rect.w,race_rect.h)
generate_button = pygame.image.load("images/generate_button.png")
generate_button = pygame.transform.scale(generate_button,(WIDTH * 0.12, HEIGTH * 0.08))
generate = rectang(WIDTH * 0.85, HEIGTH * 0.9, WIDTH * 0.09, HEIGTH*0.06)
fild_fill = False
atr_mod = []
atribut = []
text = ""

classes_rect, classes_text = creat_rect_class("Classes")
race_text_rect, race_text = creat_rect_class("Races")
atr_rect,mod_rect = const_atribute_rect()
weapon = weapons()
armor = armors()

def main():

 pygame.init()
 pygame.font.init()
 display = pygame.display.set_mode([WIDTH,HEIGTH])
 pygame.display.set_caption("RPG 3.5 Character Builder")
  
 global generate_button
 running = True
 rand = True
 field_fill = False 
 while running == True:

   if rand == True:
      
       atribut,atr_mod = random_atributes()
       char.feat = 0
       char.atributes(*atribut) 
       char.matributes()       
       rand = False 
       probability, classes_keys = class_probab()

   display_atribute(atr_rect,mod_rect,atribut,atr_mod)   
   class_race_rect_show()
   display_classes(*probability)
   display.blit(dice_icon,(dice.x,dice.y))
   display.blit(generate_button,(generate.x,generate.y))
 

   for event in pygame.event.get():
        if event.type == pygame.QUIT:
          
            running = False
        if event.type == pygame.KEYDOWN:
           if event.key == pygame.K_ESCAPE:
              running == False
              return    
        if event.type == pygame.MOUSEBUTTONDOWN:
           if event.button == 1 :
            if dice.colide.collidepoint(event.pos):
              rand = True
            elif name_rect.colide.collidepoint(event.pos):
              char.Name =  get_input(char.Name,name_rect.colide,name_rect.x,name_rect.y,20,False)   
             
            elif lvl_rect.colide.collidepoint(event.pos):
               lvl =  get_input(str(char.lvl),lvl_rect.colide,lvl_rect.x,lvl_rect.y,2,True)    
               lvl = int(lvl)
               if lvl != "" :
                  if lvl <= 20:
                   char.lvl = (lvl)
                  else: 
                     char.lvl = 20 
               atribut = lvl_adjust(*atribut)
               
                  

            elif class_show_rect.colide.collidepoint(event.pos):
               i = 0
               for r in classes_rect:
                
                  if r.collidepoint(event.pos):
                     char.clas = classes_text[i]
                  i += 1
            elif race_show_rect.colide.collidepoint(event.pos):
               i = 0
               for r in race_text_rect:
                  
                  if r.collidepoint(event.pos):
                     
                     char.race = race_text[i]
                  i += 1   
            elif generate.colide.collidepoint(event.pos) and field_fill == True :
             
               if char.race == "Random":
                  rnd = random.randint(1 , len(race_text) - 1)
                  char.race = race_text[rnd]
                 
               if char.clas == "Random" :
                  
                  e = str(random.choices(classes_keys,probability))
                  char.clas = e[2:-2]
               
               race_adjustment()  
               char.atributes_to_list()
               
               if int(char.lvl) > 3:
                       
                 atribut = lvl_adjust(*atribut)
                 char.atributes(*atribut)
                            
               char.matributes()  
               char.feat += int( char.lvl/3)
               update()
               
            else:
               j = 0
               for h in atr_rect:
                  if h.collidepoint(event.pos):
                     atribut[j] = int( get_input(str(atribut[j]),h,h.x,h.y,2,True))
                     char.atributes(*atribut)
                     char.matributes() 
                     probability, classes_keys = class_probab()
                                     
                  j +=1 
   if char.Name != "" and char.lvl != "" and char.clas != "" and char.race != "":
       generate_button = pygame.image.load("images/generate_button_green.png")
       generate_button = pygame.transform.scale(generate_button,(WIDTH * 0.12, HEIGTH * 0.08))
       field_fill = True
   else:
      generate_button = pygame.image.load("images/generate_button.png")
      generate_button = pygame.transform.scale(generate_button,(WIDTH * 0.12, HEIGTH * 0.08)) 
      field_fill = False
   
   pygame.time.wait(10)       
   pygame.display.flip()

if __name__ == "__main__":
   main()