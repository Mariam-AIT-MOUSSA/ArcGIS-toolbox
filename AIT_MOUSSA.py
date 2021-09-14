from arcpy import *
import os
TEXT=GetParameterAsText(0)
Feature_Path=GetParameterAsText(1)
Separator=GetParameterAsText(2)
entete=GetParameterAsText(3)
ChampX=GetParameterAsText(4)
ChampY=GetParameterAsText(5)
ChampZ=GetParameterAsText(6)
S_R=GetParameterAsText(7)
#nous allons commencer par creer notre couche de sortie
CreateFeatureclass_management (os.path.dirname(Feature_Path),os.path.basename(Feature_Path), "POINT",spatial_reference=S_R)
#nous allons extraire de notre fichier texte les donnees X et Y 
#puis on va inserer les points geometriques (X,Y) dans la couche de sortie

def insertinfeature(Feature,text):
    indiceX=0#pour stocker l'indice de X
    indiceY=0#pour stocker l'indice de X
    L1=[]
    A=Array()
    if entete==True:#cela signifie que les noms des champs sont dans la premiere ligne du fichier texte
       with open (text,"r")as T:
           F1=T.readline()
           L1=F1.split(Separator)#les elements de la liste sont les noms des champs
           for field in L1:
               if field==ChampX:
                   indiceX=L1.index(field)#on a alors maintenant l'indice des abscises
           F2=T.readlines()
           for line in F2:
               L2=[]
               L2=line.split(Separator)
               X=L2[indiceX]
               Y=L2[indiceX+1]#cela impose que les fichiers avec lesquelles nous travaillons ont le champ des Y juxtapose au champ des X
               
               A.append(Point(X,Y))
       with da.InsertCursor(Feature,["Shape@"])as cursor:
           for point in A:#on a stocke dans A tous les points gemetriques du fichier texte, on les insert dans la couche
               cursor.insertRow([PointGeometry(point)])
    else:#si les noms de fichier ne sont pas necessairement dans 1ere ligne
        with open (text,"r")as T:
            F1=T.readline()
            while F1==" ":#on continue a sauter les lignes jusqu'a trouver la primiere ligne dess noms 
                F1=T.readline()
            L1=F1.split(Separator)#l'algorithme est le meme
            for field in L1:
                if field==ChampX:
                    indiceX=L1.index(field)
            F2=T.readlines()
            for line in F2:
                L2=[]
                L2=line.split(Separator)
                X=L2[indiceX]
                Y=L2[indiceX+1]
                A.append(Point(X,Y))
        with da.InsertCursor(Feature,["Shape@"])as cursor:
            for point in A:
               cursor.insertRow([PointGeometry(point)])
    #pour ajouter les donnees attributaires des points on appelle la fonction ci-apres,
    #les donnees attributaires a charger dans la couche sont les coordonnees seulement!
    AddGeometryAttributes_management (Feature_Path, "POINT_X_Y_Z_M")
insertinfeature(Feature_Path,TEXT)           
                
        
      

