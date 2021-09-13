# -*- coding: utf-8 -*-
"""
Created on Sun Aug 29 17:23:06 2021

@author: jared
"""

import tkinter as tk
from PIL import Image,ImageTk
from tkinter import E,W,N,S,HORIZONTAL,END,DISABLED,NORMAL,INSERT,NW,NE
import random
import time


def window_start():
    global window
    global decks
    window = tk.Tk()
    window.title("Blackjack")
    window.geometry("1200x645+0+0")
    
    start_label = tk.Label(window,text="Ready to play?\n\nPick the number of decks.")
    start_label.pack(pady=(50,20))
    
    deck_list = [1,2,3,4,5,6,7,8]
    decks = tk.IntVar()
    deck_menu = tk.OptionMenu(window,decks,*deck_list)
    deck_menu.pack()
    
    play_btn = tk.Button(window,text="Play",command= start_game, width = 20, height = 5)
    play_btn.pack(pady = (30,0))
    
    window.mainloop()
    
def start_game():
    global canvas1
    global canvas2
    global count_info
    global deal_btn
    global deck_info
    global hit_btn
    global hold_btn
    global game_label
    
    cards_init(decks)
    for widgets in window.winfo_children():
       widgets.destroy()
       
    canvas1 = tk.Canvas(window, height = 275,bg='red')      
    canvas1.pack(fill=tk.X,pady=(0,0))
    
    canvas2 = tk.Canvas(window, height = 275, bg='green')      
    canvas2.pack(fill=tk.X,pady=(0,0))
    
    deck_info = tk.Label(text=str(decks.get())+" decks loaded with "+str(j)+" cards remaining.")
    deck_info.pack(side=tk.LEFT,padx=(10,30))
    
    count_info = tk.Label(text="Hand Count: "+str(hand_count)+"\nDealer Count: "+str(dealer_count)+"\nTotal Count: "+str(total_count)+"\nTrue Count: "+str(true_count))
    count_info.pack(side=tk.LEFT)
    
    deal_btn = tk.Button(text="DEAL",width = 25,height = 10, command=(lambda:deal()))
    deal_btn.pack(pady=(10,10),padx=(40,30),side = tk.LEFT)
    
    hit_btn = tk.Button(text="HIT",width = 15,height = 10, state=DISABLED, command=(lambda:hit()))
    hit_btn.pack(pady=(10,10),padx=(30,30),side = tk.RIGHT)
    
    hold_btn = tk.Button(text="HOLD",width = 15,height = 10, state=DISABLED, command=(lambda:hold()))
    hold_btn.pack(pady=(10,10),padx=(0,0),side = tk.RIGHT)
    
    game_label = tk.Label(text="Good Luck!")
    game_label.pack(pady=(10,10),padx=(0,30),side = tk.RIGHT)
    
    window.mainloop()

def hit():
    global hand_x
    global hit_btn
    global hand_count
    if hand_count<=21:
        num = random.randint(0,len(all_cards))
        photo_1 = Image.open(all_cards[num].file)
        photo_1 = photo_1.resize((150,225), Image.ANTIALIAS)
        img = ImageTk.PhotoImage(photo_1)  
        img1=img
        canvas2.create_image(hand_x,25, anchor=NW,image=img1)
        hand_x += 155
        label = tk.Label(canvas2,image=img1)
        label.image = img1
        update_hand(num)
        check_wins()
    
    if hand_count>21:
        for each in hand:
            if each.value == 11:
                hand_count-=10
                count_info.config(text="Hand Count: "+str(hand_count)+"\nDealer Count: "+str(dealer_count)+"\nTotal Count: "+str(total_count)+"\nTrue Count: "+str(true_count))
                continue
    if hand_count>21:
        hit_btn.config(state=DISABLED)
        bust()

def bust():
    hold_btn.config(state=DISABLED)
    hit_btn.config(state=DISABLED)
    check_wins()
    deal_btn.config(state=NORMAL)
    
def cards_init(decks):
    global total_count
    global hand_count
    global dealer_count
    global true_count
    global all_cards
    
    total_count = 0
    hand_count = 0
    dealer_count = 0
    true_count = 0
    
    all_cards = []
    suits = ['clubs','diamonds','hearts','spades']
    numbers = ['2','3','4','5','6','7','8','9','10','ace','jack','queen','king']
    i=0
    global j
    j=0
    while i < decks.get():
        for num in numbers:
            for suit in suits:
                try:
                    value1 = int(num)
                except:
                    if num == 'ace':
                        value1 = 11
                    elif num == 'jack':
                        value1 = 10
                    elif num == 'queen':
                        value1 = 10
                    else:
                        value1 = 10
                if value1 >= 10:
                    count1 = 1
                elif value1 < 7:
                    count1 = -1
                else:
                    count1 = 0
                file1 = num+"_of_"+suit+".png"
                all_cards.append(cards(file1,value1,count1,j,False))
                j+=1
        i+=1
    print(str(decks.get())+" decks loaded for a total of "+str(j)+" cards.")

def deal():
    #selects 4 random cards from the all_cards list to display as a hand
    global switch
    global hand_count
    global dealer_count
    global dealer_x
    global hand_x
    global hand
    global dealer
    global holdvar
    holdvar = False
    
    hand = []
    dealer = []
    hand_count = 0
    dealer_count = 0
    dealer_x = 30
    hand_x = 30
    
    deal_btn.config(state=DISABLED)
    hold_btn.config(state=NORMAL)
    hit_btn.config(state=NORMAL)
    switch = 0
    i=0
    while i<4:
        select = random.randint(0,len(all_cards)-1)
        display(select)
        switch+=1
        i+=1
        time.sleep(0.5)
    check_jack()

def check_jack():
    if dealer_count == 21 and hand_count ==21:
        game_label.config(text="PUSH!!")
        time.sleep(0.5)
        flip_card()
        time.sleep(0.5)
        window.update()
        reset()
    elif hand_count == 21:
        game_label.config(text="BLACKJACK!!")
        time.sleep(0.5)
        flip_card()
        time.sleep(0.5)
        window.update()
        reset()
    elif dealer_count == 21:
        game_label.config(text="DEALER BACKJACK!!")
        time.sleep(0.5)
        flip_card()
        window.update()
        time.sleep(0.5)
        reset()

def hold():
    global dealer_x
    global hold_btn
    global holdvar
    
    hold_btn.config(state=DISABLED)
    time.sleep(0.5)
    flip_card()
    time.sleep(0.5)
    while dealer_count <17:
        num = random.randint(0,len(all_cards))
        photo_1 = Image.open(all_cards[num].file)
        photo_1 = photo_1.resize((150,225), Image.ANTIALIAS)
        img = ImageTk.PhotoImage(photo_1)  
        img1=img
        canvas1.create_image(dealer_x,25, anchor=NW,image=img1)
        dealer_x += 155
        label = tk.Label(canvas2,image=img1)
        label.image = img1
        window.update()
        update_dealer(num)
        time.sleep(0.5)
    holdvar = True
    check_wins()

def reset():
    global hand_count
    global dealer_count
    global true_count
    global total_count
    
    #tk.messagebox.showinfo("GAME ENDED",  "Game resetting in 3 seconds...")
    time.sleep(3)
    
    hand_count = 0
    dealer_count = 0
    canvas1.delete("all")
    canvas2.delete("all")
    deal_btn.config(state=NORMAL)
    hold_btn.config(state=NORMAL)
    hit_btn.config(state=NORMAL)
    game_label.config(text="GOOD LUCK!!")
    #update_hand()
    #update_dealer()
    window.update()
        
def flip_card():
    global dealer_down
    
    photo_1 = Image.open(dealer_down.file)
    photo_1 = photo_1.resize((150,225), Image.ANTIALIAS)
    img = ImageTk.PhotoImage(photo_1)  
    img3 = img
    canvas1.create_image(185,25, anchor=NW,image=img3)
    label = tk.Label(canvas1,image=img3)
    label.image = img3
    window.update()

def check_wins():
    global holdvar
    if hand_count > dealer_count and hand_count < 22 and holdvar == True:
        game_label.config(text="YOU WIN!!")
        window.update()
        reset()
    elif hand_count > 21:
        game_label.config(text="YOU BUST!!\nDEALER WINS!!")
        time.sleep(0.5)
        flip_card()
        window.update()
        reset()
    elif dealer_count > hand_count and dealer_count < 22:
        game_label.config(text="DEALER WINS!!")
        window.update()
        reset()
    elif dealer_count > 21:
        game_label.config(text="DEALER BUSTS!!\nYOU WIN!!")
        window.update()
        reset()
    elif dealer_count == hand_count:
        game_label.config(text="PUSH!!")
        window.update()
        reset()

def display(num):
    #how to create the image and display
    global img
    global photo_1
    global dealer_x
    global hand_x
    global dealer_down
    
    photo_1 = Image.open(all_cards[num].file)
    photo_1 = photo_1.resize((150,225), Image.ANTIALIAS)
    img = ImageTk.PhotoImage(photo_1)  
    if switch == 0:
        img1=img
        canvas2.create_image(hand_x,25, anchor=NW,image=img1)
        hand.append(all_cards[num])
        hand_x += 155
        label = tk.Label(canvas2,image=img1)
        label.image = img1
        update_hand(num)
    elif switch == 1:
        img2 = img
        canvas1.create_image(dealer_x,25, anchor=NW,image=img2)
        dealer.append(all_cards[num])
        dealer_x += 155
        label = tk.Label(canvas1,image=img2)
        label.image = img2
        update_dealer(num)
    elif switch == 2:
        img4 = img
        canvas2.create_image(hand_x,25, anchor=NW,image=img4)
        hand.append(all_cards[num])
        hand_x += 155
        label = tk.Label(canvas1,image=img4)
        label.image = img4
        update_hand(num)
    elif switch == 3:
        dealer_down = all_cards[num]
        photo_1 = Image.open('back_of_card.png')
        photo_1 = photo_1.resize((150,225), Image.ANTIALIAS)
        img = ImageTk.PhotoImage(photo_1)  
        img3 = img
        canvas1.create_image(dealer_x,25, anchor=NW,image=img3)
        dealer.append(all_cards[num])
        dealer_x += 155
        label = tk.Label(canvas1,image=img3)
        label.image = img3
        update_dealer(num)
    else:
        print("Error")
    window.update()

def update_hand(num):
    global total_count
    global hand_count
    global j
    total_count+=all_cards[num].count
    hand_count+=all_cards[num].value
    true_count=round(total_count/decks.get(),2)
    hand.append(num)
    del all_cards[num]
    j-=1
    count_info.config(text="Hand Count: "+str(hand_count)+"\nDealer Count: "+str(dealer_count)+"\nTotal Count: "+str(total_count)+"\nTrue Count: "+str(true_count))
    deck_info.config(text=str(decks.get())+" decks loaded with "+str(j)+" cards remaining.")
    
def update_dealer(num):
    global total_count
    global dealer_count
    global j
    total_count+=all_cards[num].count
    dealer_count+=all_cards[num].value
    true_count=round(total_count/decks.get(),2)
    dealer.append(num)
    del all_cards[num]
    j-=1
    count_info.config(text="Hand Count: "+str(hand_count)+"\nDealer Count: "+str(dealer_count)+"\nTotal Count: "+str(total_count)+"\nTrue Count: "+str(true_count))
    deck_info.config(text=str(decks.get())+" decks loaded with "+str(j)+" cards remaining.")

class cards: 
    def __init__(self, file, value, count, num, status): 
        self.file = file
        self.value = value 
        self.count = count
        self.num = num
        self.status = status

window_start()