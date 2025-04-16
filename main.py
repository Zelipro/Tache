from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.core.window import Window
from kivy.graphics import RoundedRectangle,Color
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRaisedButton
from kivy.clock import Clock

from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.selectioncontrol import MDCheckbox
from kivy.uix.checkbox import CheckBox
from kivy.uix.popup import Popup
from kivymd.uix.textfield import MDTextField
from kivy.uix.screenmanager import NoTransition
from kivymd.uix.scrollview import MDScrollView
import time as Tm

import os
Window.size = [380,620]

class TAFApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Light"
        self.Name = "Bienvenue M.Elisée"
        self.ind = 1 #Pour Ecrire ca en Animation
        Main = Builder.load_file("main.kv")
        self.Bg(Main)
        Main.ids.cr.transition=NoTransition()
        self.Bienvenue(Main)
        self.Tache = False
        Window.bind(on_request_close = self.CLOSE)
        return Main
    
    def Bienvenue(self,Main):
        ind = self.ind  +1 
        ind %= len(self.Name)
        Main.ids.Lab_iden.text = self.Name[:self.ind]
        self.ind = ind
        Clock.schedule_once(lambda dt : self.Bienvenue(Main),.15)
    
    def Bg(self,Main):
        bg = Main.ids.But_cont
        with bg.canvas.before:
            Color(1,0,0,1)
            rect = RoundedRectangle(pos = bg.pos,size = bg.size)
        bg.bind(pos = lambda instance ,value : self._update_data(instance,rect))
        bg.bind(size = lambda instance ,value : self._update_data(instance,rect))
    
    def CLOSE(self,*args): #Est appeler si l'on clique sur le petit button rouge de fermerture
        if self.root.ids.cr.current == "Page_2":
            self.rep7 = self.show_info(title = "Error",Message="Impossible de Partir \n il n'est pas encore 00h00",fonct=self.Ok6)
        else:
            self.stop()
        return True
    def Ok6(self,instance):
        self.rep7.dismiss()
        
    def _update_data(self,instance ,value):
        value.pos = instance.pos
        value.size = instance.size
    
    def Back(self):
        page = self.root.ids.cr.current
        pg = page.split("_")
        if int(pg[1]) > 1:
            self.root.ids.cr.current = "Page_1"
            self.root.ids.TopBar.title = "Travail a faire"
            try:
                Clock.unschedule(self.rep4)
            except:
                pass
        else:
            self.rep1 = self.show_info(title = "Question",Message = "Voullez vous quitter TAF ?",fonct = self.Ok)
    
    def show_info(self,title,Message ,fonct):
        Dig = MDDialog(
            title = title,
            text = Message,
            buttons = [
                MDRaisedButton(
                    text='Ok',
                    on_release = fonct
                )
            ]
        )
        Dig.open()
        return Dig
    
    def Ok(self,instance):
        self.rep1.dismiss()
        self.stop()
    
    def ChangeMode(self):
        Pg = self.root.ids.Lab_iden
        if self.theme_cls.theme_style == "Dark":
            self.theme_cls.theme_style = "Light"
            Pg.color = (0,0,0,1)
            self.root.ids.TopBar.right_action_items = [["weather-night",lambda x : self.ChangeMode()]]
        else:
            self.theme_cls.theme_style = "Dark"
            Pg.color = (1,1,0,1)
            self.root.ids.TopBar.right_action_items = [["weather-sunny",lambda x : self.ChangeMode()]]
    
    def New_Section(self,instance):
        self.root.ids.TopBar.title = "New Section"
        try:
            Clock.unschedule(self.schule1)
        except:
            pass
        
        try:
            self.root.ids.Page_2_Cont.clear_widgets()
            self.root.ids.cr.current = "Page_2"
            tous = self.FICHIER_FIC(os.getcwd() + '/Taches')
            for elmt in tous :
                if elmt == f"{Tm.strftime('%d')},{Tm.strftime('%m')},{Tm.strftime('%y')}":
                    self.Lieu2 = os.getcwd() + '/Taches/' + elmt
                    with open(self.Lieu2) as fil:
                        tous2 = fil.read()
                    tous2 = tous2.split("\n")
                    
                    self.Tous = tous2
                    
                    for i,elmt2 in enumerate(tous2):
                        if len(elmt2)>1:
                            elmt2 = elmt2.split(":")
                            
                            wr = self.root.ids.Page_2_Cont
                            Box = MDBoxLayout(orientation = 'horizontal',size_hint_y = None,)
                            Lab = MDLabel(
                                text = elmt2[0],
                                bold = True,
                            )
                            Box.add_widget(Lab)
                            wr.add_widget(Box)
                            
                            Chek = MDCheckbox()
                            
                            if elmt2[1]== "True":
                                Chek.active = True
                                
                            Box.add_widget(Chek)
                            #self.Ind2 = i
                            self.Modifier = True
                            Chek.bind(active = lambda instance ,value,ind = i: self.Modifi(instance,value,ind))
                    #self.Mettre_fin()
                    self.Tim()
                    
        except:
            self.Write_Me = "Pas de Tache "
            self.Tache = True
            self.Pas_Tache(1)
    
    def Pas_Tache(self,ind):
        Pge2 = self.root.ids.Page_2_Cont
        Lab = MDLabel(
            #text = self.Write_Me[:ind],
            halign = "center",
            bold = True,
        )
        Pge2.add_widget(Lab)
        self.do2(Lab,ind)
    
    def do2(self,Lab,ind):
        Lab.text = self.Write_Me[:ind]
        ind = (ind+1) % len(self.Write_Me)
        self.schule1 = Clock.schedule_once(lambda dt : self.do2(Lab,ind),.2)
        
    def Modifi(self,instance,value,ind):
        Tous = self.Tous
        if self.Modifier:
            for i,elmt in enumerate(Tous):
                if i == ind:
                    Tous[i] = ":".join([elmt.split(":")[0],str(value)])      
            Tous = "\n".join(Tous)  
            with open(self.Lieu2,"w") as fil:  
                fil.write(Tous)
    
    def FICHIER_FIC(self,rep):
        return [fic for fic in os.listdir(rep) if os.path.isfile(os.path.join(rep,fic))]
    
    def Last_work(self,instance):
        self.Lieu = os.getcwd() + '/Taches'
        fil = os.path.exists(self.Lieu)
        if not fil:
            self.rep2 = self.show_info(title = "Info",Message="Pas de Tâche passé !",fonct=self.Ok2)
        else:
            self.root.ids.cr.current = "Page_3"
            Page = self.root.ids.Page_3_Cont_2
            self.root.ids.TopBar.title = "Taf passé"
            All = self.FICHIER_FIC(self.Lieu)
            try:
                Page.clear_widgets()
            except:
                pass

            for i,elmt in enumerate(All):
                if i%2 == 0:
                    self.Box = MDGridLayout(cols = 1,size_hint_x =None,pos_hint = {"center_x":.5,"center_y":.5},spacing = 10)
                    Page.add_widget(self.Box)
                
                name = f"[b]{elmt}[/b]"
                if len(name) > 15:
                    name = f"{name[:11]}\n{name[11:]}"
                    
                But = MDRaisedButton(
                    text = name,
                    makup = True,
                    #size_hint_x = None,
                    
                )
                #Ici les press
                But.bind(on_release = self.appui)
                self.Box.add_widget(But)
    
    def appui(self,instance):
        Lay = MDGridLayout(cols = 3,spacing = 10,adaptive_height = True)
        Mettre = instance.text[3:-4]
        if "\n" in Mettre:
            Mettre = f"{Mettre.split('\n')[0]}{Mettre.split('\n')}"
        with open(os.getcwd() + "/Taches/" + Mettre) as fil:
            tous = fil.read()
        tous = tous.split("\n")
        i = 1
        for _,title in zip(range(3),["ID","Job","Do or Not"]):
            Lab = MDLabel(text = title,bold = True,color = (1,1,1,1),pos_hint = {"center_y":.5})
            Lay.add_widget(Lab)
            
        for elmt in tous:
            if len(elmt)>2:
                elmt = elmt.split(":")
                for _,title in zip(range(3),[str(i),elmt[0],elmt[1]]):
                    Lab = MDLabel(text = title,size_hint_y = None,pos_hint = {"center_y":.5})
                    Lay.add_widget(Lab)
                i+=1
        Scrol = MDScrollView(do_scroll_x = False,do_scroll_y = True)
        Scrol.add_widget(Lay)
        Box = MDBoxLayout(orientation =  'vertical',size_hint = (1,.8),pos_hint = {"center_y":.5})
        Box.add_widget(Scrol)
        But = MDRaisedButton(text = "Vu")
        
        But.bind(on_press = self.Ok7)
        Box.add_widget(But)
        
        self.rep8 = Popup(
            title = f"La Liste de {Mettre}",
            content = Box
        )
        self.rep8.open()
    
    def Ok7(self,instance):
        self.rep8.dismiss()
    def Ok2(self,instance):
        self.rep2.dismiss()
    
    def Add_Tache(self,instance):
        self.Lieu3 = os.getcwd() + '/Taches'
        if not os.path.exists(self.Lieu3):
            os.mkdir(self.Lieu3)
        Date = f"{Tm.strftime('%d')},{Tm.strftime('%m')},{Tm.strftime('%y')}"
        self.Lieu4 = self.Lieu3 + "/"+Date
        try:
            with open(self.Lieu4) as file:#Quant on ne met pas r ca s'ouvre automatique en mode lecture
                tous = file.read()
        except:
            tous = ""
        self.tous = tous.split("\n")
        self.rep3 = self.pop(title = "Veuillez entrez les informations",fonct = self.Ok3)
        #self.Mettre_fin()
        
    def pop(self,title,fonct):
        Lay = MDBoxLayout(orientation = 'vertical',size_hint = (1,0.2))
        self.Input = MDTextField(
            hint_text = "Exemple : Apprendre ATO",
            halign = "center"
        )
        Lay.add_widget(self.Input)
        
        But = MDRaisedButton(text = "Valider")
        But.bind(on_release=fonct)
        Lay.add_widget(But)
        Pop = Popup(
            title = title,
            content = Lay,
            size_hint = (0.9,0.3)
        )
       
        Pop.open()
        return Pop
    def Ok3(self,instance):
        if self.Input.text != "":
            self.tous.append(f"{self.Input.text}:False")
            self.tous = "\n".join(self.tous)
            with open(self.Lieu4,"w") as fil:
                fil.write(self.tous)
            
            self.Back()
        self.rep3.dismiss()
    
    def Mettre_fin(self):
        if f'{Tm.strftime("%H")},{Tm.strftime("%M")}' == '00,00':
            self.Modifier = False
            try:
                #with open(self.Lieu4) as fil:
                    #tous2 = fil.read()
                #tous2 = tous2.split("\n")
                tous2 = self.Tous
                
            except:
                tous2 = ""
            if tous2 == "":
                self.Parler("Pas de Tâche")
            else:
                nb = 0
                for elmt in tous2:
                    if len(elmt)>1:
                        elmt = elmt.split(":")
                        if elmt[1] == "False":
                            nb += 1
                if nb == 0:
                    self.Parler("Félicitation Vous avez tout accomplit")
                else:
                    self.Parler(f" {nb} tâche Non accomplit")
            
            
            
    def Parler(self,texte):
        # Générer un fichier audio avec Pico TTS
        os.system(f'pico2wave -l fr-FR -w sortie.wav "{texte}"')
        # Lire le fichier audio
        os.system('aplay sortie.wav')
           
        
    def Tim(self):
        #Tm.sleep(1)
        self.Mettre_fin()
        if self.Modifier:
            self.time = 24*3600 - (int(Tm.strftime("%H"))*3600+int(Tm.strftime("%M"))*60 + int(Tm.strftime("%S")))
            heur = f"{self.time//3600} h {(self.time%3600)//60} min {(self.time%3600)%60} sec"
            self.root.ids.BottomBar.title = f"T. restant : \n [b]{heur}[/b]"
            
        else:
            self.root.ids.BottomBar.title = "Time is Over"
            self.root.ids.BottomBar.right_action_items = [["block-helper",lambda x : self.Close()]]
        
        self.rep4 = Clock.schedule_once(lambda dt:self.Tim(),5)
            
    def Close(self):
        Clock.unschedule(self.rep4)
        self.rep6 = self.show_info(title = "Info",Message="Au revoir",fonct = self.Ok5)
    
    def Ok5(self,instace):
        self.rep6.dismiss()
        self.stop()
    
    def information(self):
        self.rep5 = self.show_info(title = "Information",Message="Name : Gestionnaire de TAF\nAuthor : Elisée ATIKPO \nVersion: 2.0\nToul:KivyMD,Kivy,Python3",fonct=self.Ok4)
    
    def Ok4(self,instance):
        self.rep5.dismiss()
TAFApp().run()