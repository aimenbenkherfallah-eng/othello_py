import tkinter as tk
from tkinter import messagebox
import copy
from math import inf
TAILLE = 8
VIDE = '.'   
NOIR = 'N'   #machine
BLANC = 'B'  #humain
DIRECTIONS = [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]

#logique de jeu

def initialiser_plateau():
    p = [[VIDE for _ in range(TAILLE)] for _ in range(TAILLE)]
    p[3][3], p[4][4] = BLANC, BLANC
    p[3][4], p[4][3] = NOIR, NOIR
    return p

def dans_plateau(r,c): return 0 <= r < TAILLE and 0 <= c < TAILLE
def adversaire(j): return NOIR if j==BLANC else BLANC

def coups_possibles(plateau, joueur):
    opp = adversaire(joueur)
    coups=set()
    for r in range(TAILLE):
        for c in range(TAILLE):
            if plateau[r][c]!=VIDE: continue
            for dr,dc in DIRECTIONS:
                rr,cc=r+dr,c+dc
                found=False
                while dans_plateau(rr,cc) and plateau[rr][cc]==opp:
                    found=True; rr+=dr; cc+=dc
                if found and dans_plateau(rr,cc) and plateau[rr][cc]==joueur:
                    coups.add((r,c)); break
    return coups

def appliquer_coup(plateau,joueur,pos):
    r0,c0=pos; opp=adversaire(joueur)
    plateau[r0][c0]=joueur
    for dr,dc in DIRECTIONS:
        rr,cc=r0+dr,c0+dc; piste=[]
        while dans_plateau(rr,cc) and plateau[rr][cc]==opp:
            piste.append((rr,cc)); rr+=dr; cc+=dc
        if piste and dans_plateau(rr,cc) and plateau[rr][cc]==joueur:
            for (pr,pc) in piste: plateau[pr][pc]=joueur

def compter_pions(plateau):
    n=sum(r.count(NOIR) for r in plateau)
    b=sum(r.count(BLANC) for r in plateau)
    return n,b

#heuristique

heuristique_log = []
heuristique_log2 = []



def heuristique(plateau):
    n,b = compter_pions(plateau)
    return n - b 
def heuristique2(plateau):
    n,b = compter_pions(plateau)
    return n, b
#MinMax
def minmax(plateau, joueur, profondeur, max_depth):
    coups = coups_possibles(plateau, joueur)
    if profondeur==max_depth or not coups:
        h = heuristique(plateau)
        j = heuristique2(plateau)
        heuristique_log.append(h)
        heuristique_log2.append(j)
        return h, None
        

    if joueur == NOIR:  
        meilleur_score = -inf
        meilleur_coup = None
        for coup in coups:
            new_p = copy.deepcopy(plateau)
            appliquer_coup(new_p, joueur, coup)
            score, _ = minmax(new_p, BLANC, profondeur+1, max_depth)
            if score > meilleur_score:
                meilleur_score, meilleur_coup = score, coup
        return meilleur_score, meilleur_coup
    else:              
        pire_score = inf
        pire_coup = None
        for coup in coups:
            new_p = copy.deepcopy(plateau)
            appliquer_coup(new_p, joueur, coup)
            score, _ = minmax(new_p, NOIR, profondeur+1, max_depth)
            if score < pire_score:
                pire_score, pire_coup = score, coup
        return pire_score, pire_coup

#interface

class OthelloGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Othello by Aimen Benkherfallah")
        self.plateau = initialiser_plateau()
        self.joueur = BLANC  #humain commence
        self.profondeur = 2  #np = 2 "il est demandé dans l'enoncé du projet"
        self.boutons = [[None]*TAILLE for _ in range(TAILLE)]
        self.label_info = tk.Label(root, text="", font=("Helvetica", 14, "bold"))
        self.label_info.pack(pady=10)

          
        self.score_text = tk.Text(root, height=10, width=40)
        self.score_text.pack(pady=10)

        self.cadre_plateau = tk.Frame(root, bg="green")
        self.cadre_plateau.pack()

        for r in range(TAILLE):
            for c in range(TAILLE):
                b = tk.Button(self.cadre_plateau, width=4, height=2,
                              command=lambda r=r, c=c: self.jouer_humain(r, c))
                b.grid(row=r, column=c, padx=1, pady=1)
                self.boutons[r][c] = b
        self.mettre_a_jour_affichage()
        
    def afficher_scores(self):
        self.score_text.delete("1.0", tk.END)
        for v in heuristique_log:
            self.score_text.insert(tk.END, f"{v}\n") 
    def afficher_scores(self):
        self.score_text.delete("1.0", tk.END)
        for v in heuristique_log2:
            self.score_text.insert(tk.END, f"{v}\n") 

        

    def mettre_a_jour_affichage(self):
        coups = coups_possibles(self.plateau, self.joueur)
        n, b = compter_pions(self.plateau)
        joueur_txt = "Humain (Blanc)" if self.joueur==BLANC else "Machine (Noir)"
        self.label_info.config(text=f"Tour de : {joueur_txt} | Score N={n}  B={b}")

        for r in range(TAILLE):
            for c in range(TAILLE):
                val = self.plateau[r][c]
                bouton = self.boutons[r][c]
                if val == NOIR:
                    bouton.config(bg="black", state="disabled")
                elif val == BLANC:
                    bouton.config(bg="white", state="disabled")
                elif (r, c) in coups and self.joueur==BLANC:
                    bouton.config(bg="#6E6C6C", state="normal")  # gris= coup jouable
                else:
                    bouton.config(bg="#0F7E0F", state="disabled")  # vert= vide

        if not coups:
            autre = adversaire(self.joueur)
            if not coups_possibles(self.plateau, autre):
                self.fin_de_partie()
            else:
                self.joueur = autre
                self.root.after(500, self.tour_machine if self.joueur==NOIR else self.mettre_a_jour_affichage)

    def jouer_humain(self, r, c):
        coups = coups_possibles(self.plateau, BLANC)
        if (r, c) not in coups: return
        appliquer_coup(self.plateau, BLANC, (r, c))
        self.joueur = NOIR
        self.mettre_a_jour_affichage()
        self.root.after(700, self.tour_machine)

    def tour_machine(self):
        coups = coups_possibles(self.plateau, NOIR)
        if not coups:
            self.joueur = BLANC
            self.mettre_a_jour_affichage()
            return
        
        heuristique_log.clear()
        heuristique_log2.clear() #pour reenisialiser la liste de stockage des valeurs
          
        _, coup = minmax(self.plateau, NOIR, 0, self.profondeur)
        if coup:
            appliquer_coup(self.plateau, NOIR, coup)
        self.afficher_scores()
        self.joueur = BLANC
        self.mettre_a_jour_affichage()

    def fin_de_partie(self):
        n, b = compter_pions(self.plateau)
        if n > b:
            messagebox.showinfo("fin", f"partie terminée! machine gagne ({n}-{b})")
        elif b > n:
            messagebox.showinfo("fin", f"partie terminée!vous gagnez ({b}-{n})")
        else:
            messagebox.showinfo("fin", f"egalité parfaite ({n}-{b})")
        self.root.destroy()



if __name__ == "__main__":
    root = tk.Tk()
    app = OthelloGUI(root)
    root.mainloop()
