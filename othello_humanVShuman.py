import tkinter as tk
from tkinter import messagebox
import copy
from math import inf

TAILLE = 8
VIDE = '.'
NOIR = 'N'
BLANC = 'B'

DIRECTIONS = [(-1, -1), (-1, 0), (-1, 1),
              (0, -1),           (0, 1),
              (1, -1),  (1, 0),  (1, 1)]

#logique du jeu 

def initialiser_plateau():
    p = [[VIDE for _ in range(TAILLE)] for _ in range(TAILLE)]
    p[3][3], p[4][4] = BLANC, BLANC
    p[3][4], p[4][3] = NOIR, NOIR
    return p

def dans_plateau(r, c):
    return 0 <= r < TAILLE and 0 <= c < TAILLE

def adversaire(joueur):
    return NOIR if joueur == BLANC else BLANC

def coups_possibles(plateau, joueur):
    opp = adversaire(joueur)
    coups = set()
    for r in range(TAILLE):
        for c in range(TAILLE):
            if plateau[r][c] != VIDE:
                continue
            for dr, dc in DIRECTIONS:
                rr, cc = r + dr, c + dc
                found_opp = False
                while dans_plateau(rr, cc) and plateau[rr][cc] == opp:
                    found_opp = True
                    rr += dr
                    cc += dc
                if found_opp and dans_plateau(rr, cc) and plateau[rr][cc] == joueur:
                    coups.add((r, c))
                    break
    return coups

def appliquer_coup(plateau, joueur, pos):
    r0, c0 = pos
    plateau[r0][c0] = joueur
    opp = adversaire(joueur)
    for dr, dc in DIRECTIONS:
        rr, cc = r0 + dr, c0 + dc
        piste = []
        while dans_plateau(rr, cc) and plateau[rr][cc] == opp:
            piste.append((rr, cc))
            rr += dr
            cc += dc
        if piste and dans_plateau(rr, cc) and plateau[rr][cc] == joueur:
            for (pr, pc) in piste:
                plateau[pr][pc] = joueur

def compter_pions(plateau):
    n = sum(row.count(NOIR) for row in plateau)
    b = sum(row.count(BLANC) for row in plateau)
    return n, b

def heuristique (plateau) : 
    n, b = compter_pions (plateau)
    return n, b  #la machine si positif
def minmax (plateau, joueur, profondeur, max_depth) : 
    coups = coups_possibles (plateau, joueur)
    if profondeur == max_depth or not coups : 
        return heuristique(plateau), None
    if joueur == NOIR : 
         meilleur_score = -inf
         meilleur_coup = None

         
#interface graphique 

class OthelloGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Othello - Projet IA (Aimen Benkherfallah)")
        self.plateau = initialiser_plateau()
        self.joueur = NOIR
        self.boutons = [[None]*TAILLE for _ in range(TAILLE)]
        self.label_info = tk.Label(root, text="", font=("Helvetica", 14, "bold"))
        self.label_info.pack(pady=10)
        self.cadre_plateau = tk.Frame(root, bg="green")
        self.cadre_plateau.pack()

        #boutons
        for r in range(TAILLE):
            for c in range(TAILLE):
                b = tk.Button(self.cadre_plateau, width=4, height=2,
                              command=lambda r=r, c=c: self.jouer(r, c))
                b.grid(row=r, column=c, padx=1, pady=1)
                self.boutons[r][c] = b
        self.mettre_a_jour_affichage()

    def mettre_a_jour_affichage(self):
        coups = coups_possibles(self.plateau, self.joueur)
        n, b = compter_pions(self.plateau)
        joueur_txt = "Noir (N)" if self.joueur == NOIR else "Blanc (B)"
        self.label_info.config(text=f"Tour de : {joueur_txt} | Score N={n}  B={b}")

        for r in range(TAILLE):
            for c in range(TAILLE):
                val = self.plateau[r][c]
                bouton = self.boutons[r][c]
                if val == NOIR:
                    bouton.config(bg="black", state="disabled")
                elif val == BLANC:
                    bouton.config(bg="white", state="disabled")
                elif (r, c) in coups:
                    bouton.config(bg="#808080", state="normal")  # gris pour coup possible
                else:
                    bouton.config(bg="#228B22", state="disabled")  # vert foncé = vide non jouable

        if not coups:
            
            autre = adversaire(self.joueur)
            if not coups_possibles(self.plateau, autre):
                self.fin_de_partie()
            else:
                messagebox.showinfo("Othello", f"Aucun coup possible pour {joueur_txt}, il passe son tour.")
                self.joueur = autre
                self.mettre_a_jour_affichage()

    def jouer(self, r, c):
        coups = coups_possibles(self.plateau, self.joueur)
        if (r, c) not in coups:
            return
        appliquer_coup(self.plateau, self.joueur, (r, c))
        self.joueur = adversaire(self.joueur)
        self.mettre_a_jour_affichage()

    def fin_de_partie(self):
        n, b = compter_pions(self.plateau)
        if n > b:
            messagebox.showinfo("Fin", f"Partie terminée ! Noir gagne ({n} contre {b}).")
        elif b > n:
            messagebox.showinfo("Fin", f"Partie terminée ! Blanc gagne ({b} contre {n}).")
        else:
            messagebox.showinfo("Fin", f"Égalité parfaite ({n} - {b}) !")
        self.root.destroy()



if __name__ == "__main__":
    root = tk.Tk()
    app = OthelloGUI(root)
    root.mainloop()
