#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Import de librairies ou de fichiers externes
from Header import *
from Journalisation import *
from GestionFichier import *
from Requeter import *

############################################
### Classe Application
### Classe de la fenêtre principale
############################################

#global curseur

class Application:
    
    def __init__(self):
      
      # Connexion à la base
      self.dbConnection = MyDatabaseConnection(HOSTNAME, LOGIN, MDP, BASE)
      
      MainInterface = gtk.Builder()
      MainInterface.add_from_file("TIFO.glade") # On fait le lien avec le fichier GLADE
      MainInterface.connect_signals(self) # Connexion des signaux définis

      self.window = MainInterface.get_object("MainWindows")
      self.Proprietes()
 
      self.ViewPortDepouillement = MainInterface.get_object("ViewPortDepouillement")
      self.VisuDepouillement = MainInterface.get_object("VisuDepouillement")
      self.VisuDepouillement.modify_base(gtk.STATE_NORMAL, gtk.gdk.color_parse("aquamarine"))
      self.ViewPortDepouillement.modify_base(gtk.STATE_NORMAL, gtk.gdk.color_parse("blue"))
      InsererTexte(self.VisuDepouillement,"Toto\nTaat\njjj")
      self.TitreDepouillement = MainInterface.get_object("TitreDepouillement")
      self.TitreDepouillement.set_text("<b><big><span background='grey'>Dépouillement des fichiers Enregistrements</span></big></b>")
      self.TitreDepouillement.set_justify(gtk.JUSTIFY_CENTER)
      self.TitreDepouillement.set_use_markup(True)
      self.window.show_all()     

        
    def Proprietes(self): #Il est possible que ça surcharge des propriétés du fichier Glade
      self.window.set_position(gtk.WIN_POS_CENTER)
      self.window.set_title(TITRE)
      self.window.resize(LARGEUR,HAUTEUR) 
      self.window.set_default_size(LARGEUR,HAUTEUR)
      #self.window.set_icon_from_file("icone.png")      

    def on_MenuItemQuit_click(self,event):
        self.dbConnection.close() ## On pense bien à fermer la base
        
        # Suppression des fichiers issus de l'interprétation Python
        for item in os.listdir("."):
          if re.search(".pyc$",item):
            os.remove(item)
        
        self.window.destroy()
        exit(0)

    def on_MenuItemOuvrir_click(self,event):
        FileChooser=gtk.FileChooserDialog(
        title="Sélection d'un fichier Enregistrement",
        action=gtk.FILE_CHOOSER_ACTION_OPEN,
        buttons=(gtk.STOCK_CANCEL,gtk.RESPONSE_CANCEL,gtk.STOCK_OPEN,gtk.RESPONSE_OK))
        FileChooser.set_current_folder(os.getcwd())

        MonFiltre = gtk.FileFilter()
        MonFiltre.set_name("Fichier Enregistrement")
        MonFiltre.add_pattern("*OLDI*[!.txt]")
        FileChooser.add_filter(MonFiltre)

        Response = FileChooser.run()
        if Response == gtk.RESPONSE_OK:
          FileChooser.hide()
          IdFichier = OuvrirFichier(FileChooser.get_filename())          
          ExtraireDonneesFichiers(self.dbConnection,self.window,self.VisuDepouillement,IdFichier,FileChooser.get_filename())
        FileChooser.destroy()

    def on_MenuItemSave_click(self,event):
        print "J'ai clique sur Enregistrer"

    def on_MenuItemSaveAs_click(self,event):
        FileChooser=gtk.FileChooserDialog(title="Enregistrement d'un fichier dépouillé",
        action=gtk.FILE_CHOOSER_ACTION_SAVE,
        buttons=(gtk.STOCK_CANCEL,gtk.RESPONSE_CANCEL,gtk.STOCK_SAVE,gtk.RESPONSE_OK))
        FileChooser.set_current_folder(os.getcwd())

        MonFiltre = gtk.FileFilter()
        MonFiltre.set_name("Fichier Dépouillé")
        MonFiltre.add_pattern("*.txt")
        FileChooser.add_filter(MonFiltre)

        Response = FileChooser.run()
        if Response == gtk.RESPONSE_OK:
          return FileChooser.get_filename()
        FileChooser.destroy()

    def on_MenuItemPrint_click(self,event):
      print_op = gtk.PrintOperation()

      res = print_op.run(gtk.PRINT_OPERATION_ACTION_PRINT_DIALOG, None)

    def on_MenuItemSettings_click(self,event):
      MainInterface = gtk.Builder()
      MainInterface.add_from_file("Settings.glade") # On fait le lien avec le fichier GLADE
      MainInterface.connect_signals(self) # Connexion des signaux définis

      self.window = MainInterface.get_object("window1")
      self.window.show()


    def on_MenuItemAPropos_click(self,event):
      print "J'ai appuyé sur About"

if __name__ == "__main__":
	Application()
	gtk.main()
