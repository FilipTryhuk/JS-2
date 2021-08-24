from tkinter import *
import projekt

if __name__ == '__main__':
	queue, obsl, zwykly, kl_vip, utime, gen_ID, okienko1, okienko2, okienko3 = projekt.Setup()
	
	#sprawdz czy klasy zostaly poprawnie zainicjalizowane
	try:
		kl_vip
		okienko1
	except NameError:
		print("Błąd inicjalizacji!")
	
	#Funkcje interfejsu odpowiedzialne za dodawanie nowych klientów do kolejki
	def nowy_a():
		zwykly.wejscie("a", next(gen_ID), obsl, queue, okienko1, okienko2, okienko3, zwykly, kl_vip)
		a.set(len(queue[0]))
	def nowy_b():
		zwykly.wejscie("b", next(gen_ID), obsl, queue, okienko1, okienko2, okienko3, zwykly, kl_vip)
		b.set(len(queue[1]))
	def nowy_vip_a():
		kl_vip.wejscie("a", next(gen_ID), obsl, queue, okienko1, okienko2, okienko3, zwykly, kl_vip)
		vip_a.set(len(queue[2]))
	def nowy_vip_b():
		kl_vip.wejscie("b", next(gen_ID), obsl, queue, okienko1, okienko2, okienko3, zwykly, kl_vip)
		vip_b.set(len(queue[3]))

	#Funkcje interfejsu odpowiedzialne za przesłanie następnego klienta do obsługi w wybranym okienku
	#oraz ukatualnienie wyświetlanej liczby osób w kolejce
	def next_o1():
		okienko1.kolejny(obsl, queue, zwykly, kl_vip)
		a.set(len(queue[0]))
		b.set(len(queue[1]))
		vip_a.set(len(queue[2]))
		vip_b.set(len(queue[3]))
	def next_o2():
		okienko2.kolejny(obsl, queue, zwykly, kl_vip)
		a.set(len(queue[0]))
		b.set(len(queue[1]))
		vip_a.set(len(queue[2]))
		vip_b.set(len(queue[3]))
	def next_o3():
		okienko3.kolejny(obsl, queue, zwykly, kl_vip)
		a.set(len(queue[0]))
		b.set(len(queue[1]))
		vip_a.set(len(queue[2]))
		vip_b.set(len(queue[3]))
	
	#Funkcje interfejsu odpowiedzialne za przełączanie trybów działania okienek
	def toggle_a_o1():
		okienko1.toggle_a()
	def toggle_b_o1():
		okienko1.toggle_b()
	def toggle_a_o2():
		okienko2.toggle_a()
	def toggle_b_o2():
		okienko2.toggle_b()
	def toggle_a_o3():
		okienko3.toggle_a()
	def toggle_b_o3():
		okienko3.toggle_b()
		
	#Funkcja odpowiedzialna za wyświetlenie tabelek na ekranie 
	def end_task():
		ktab1, ktab2 = projekt.Zakoncz(okienko1, okienko2, okienko3)
		r00.config(text = ktab1[0][0])
		r01.config(text = ktab1[0][1])
		r02.config(text = ktab1[0][2])
		r03.config(text = ktab1[0][3])
		r04.config(text = ktab1[0][4])
		r10.config(text = ktab1[1][0])
		r11.config(text = ktab1[1][1])
		r12.config(text = ktab1[1][2])
		r13.config(text = ktab1[1][3])
		r14.config(text = ktab1[1][4])
		r20.config(text = ktab1[2][0])
		r21.config(text = ktab1[2][1])
		r22.config(text = ktab1[2][2])
		r23.config(text = ktab1[2][3])
		r24.config(text = ktab1[2][4])
		r30.config(text = ktab1[3][0])
		r31.config(text = ktab1[3][1])
		r32.config(text = ktab1[3][2])
		r33.config(text = ktab1[3][3])
		r34.config(text = ktab1[3][4])
		
		v00.config(text = ktab2[0][0])
		v01.config(text = ktab2[0][1])
		v02.config(text = ktab2[0][2])
		v03.config(text = ktab2[0][3])
		v04.config(text = ktab2[0][4])
		v10.config(text = ktab2[1][0])
		v11.config(text = ktab2[1][1])
		v12.config(text = ktab2[1][2])
		v13.config(text = ktab2[1][3])
		v14.config(text = ktab2[1][4])
		v20.config(text = ktab2[2][0])
		v21.config(text = ktab2[2][1])
		v22.config(text = ktab2[2][2])
		v23.config(text = ktab2[2][3])
		v24.config(text = ktab2[2][4])
		v30.config(text = ktab2[3][0])
		v31.config(text = ktab2[3][1])
		v32.config(text = ktab2[3][2])
		v33.config(text = ktab2[3][3])
		v34.config(text = ktab2[3][4])
		
		
	#Inicjowanie interfejsu oraz początkowego stanu zmiennych	
	root = Tk()
	root.title('App')
	root.geometry("600x600")
	frame0 = Frame(root)
	frame0.pack(side=TOP, pady=20)
	label = Label(root, text="Dodaj klienta", font=30, fg="blue")
	label.pack(side=TOP)
	a = StringVar()
	a.set(len(queue[0]))
	b = StringVar()
	b.set(len(queue[1]))
	vip_a = StringVar()
	vip_a.set(len(queue[2]))
	vip_b = StringVar()
	vip_b.set(len(queue[3]))
	var = []
	reset = 0
	for i in range(6):
		var.append(IntVar())
	
	
	#frame1 przechowuje przyciski dodawania klientow
	frame1 = Frame(root)
	frame1.pack(side=TOP)
	addA_button = Button(frame1, text="Nowy A", width=10, command=nowy_a)
	addB_button = Button(frame1, text="Nowy B", width=10, command=nowy_b)
	addVIPa_button = Button(frame1, text="Nowy VIP A", width=10, command=nowy_vip_a)
	addVIPb_button = Button(frame1, text="Nowy VIP B", width=10, command=nowy_vip_b)
	addA_button.pack(side=LEFT, padx=2, pady=5)
	addB_button.pack(side=LEFT, padx=2, pady=5)
	addVIPa_button.pack(side=LEFT, padx=2, pady=5)
	addVIPb_button.pack(side=LEFT, padx=2, pady=5)
	
	
	#frame2 przechowuje liczniki klientów w kolejkach
	frame2 = Frame(root)
	frame2.pack(side=TOP, pady=10)
	dispA = Label(frame2, textvariable = a)
	dispB = Label(frame2, textvariable = b)
	dispVIPa = Label(frame2, textvariable = vip_a)
	dispVIPb = Label(frame2, textvariable = vip_b)
	dispA.pack(side = LEFT, padx=50)
	dispB.pack(side = LEFT, padx=50)
	dispVIPa.pack(side = LEFT, padx=50)
	dispVIPb.pack(side = LEFT, padx=50)
	
	
	#frame3 przechowuje okienka
	frame3 = Frame(root)
	frame3.pack(side=TOP, pady=30)
	fo1 = Frame(frame3, relief=GROOVE, borderwidth=4)
	fo1.pack(side=LEFT, padx=5)
	nexto1 = Button(fo1, text="Następny", width=12, command=next_o1)
	nexto1.pack(side=TOP, padx=5, pady=5)
	check_frame1 = Frame(fo1)
	check_frame1.pack(side=TOP)
	c1a = Checkbutton(check_frame1, text="A", variable=var[0], onvalue=1, offvalue=0, command=toggle_a_o1)
	c1a.pack(side=LEFT)
	c1b = Checkbutton(check_frame1, text="B", variable=var[1], onvalue=1, offvalue=0, command=toggle_b_o1)
	c1b.pack(side=RIGHT)
	
	fo2 = Frame(frame3, relief=GROOVE, borderwidth=4)
	fo2.pack(side=LEFT, padx=5)
	nexto2 = Button(fo2, text="Następny", width=12, command=next_o2)
	nexto2.pack(side=TOP, padx=5, pady=5)
	check_frame2 = Frame(fo2)
	check_frame2.pack(side=TOP)
	c2a = Checkbutton(check_frame2, text="A", variable=var[2], onvalue=1, offvalue=0, command=toggle_a_o2)
	c2a.pack(side=LEFT)
	c2b = Checkbutton(check_frame2, text="B", variable=var[3], onvalue=1, offvalue=0, command=toggle_b_o2)
	c2b.pack(side=RIGHT)
	
	fo3 = Frame(frame3, relief=GROOVE, borderwidth=4)
	fo3.pack(side=LEFT, padx=5)
	nexto3 = Button(fo3, text="Następny", width=12, command=next_o3)
	nexto3.pack(side=TOP, padx=5, pady=5)
	check_frame3 = Frame(fo3)
	check_frame3.pack(side=TOP)
	c3a = Checkbutton(check_frame3, text="A", variable=var[4], onvalue=1, offvalue=0, command=toggle_a_o3)
	c3a.pack(side=LEFT)
	c3b = Checkbutton(check_frame3, text="B", variable=var[5], onvalue=1, offvalue=0, command=toggle_b_o3)
	c3b.pack(side=RIGHT)
	
	
	#frame4 przechowuje przycisk zakończ
	frame4 = Frame(root, relief=RIDGE, borderwidth=6)
	frame4.pack(side=TOP)
	end = Button(frame4, text="Zakończ i zaktualizuj", width=25, command=end_task)
	end.pack()
	
	
	#frame5 i frame6 przechowuje przechowuje tabelki ze statystykami, początkowo niewidoczne
	frame5 = Frame(root)
	frame5.pack(side=TOP, pady=20)
	
	frame_e1 = Frame(frame5)
	frame_e1.pack(side=TOP)
	r00 = Label(frame_e1, text="")
	r00.pack(side=LEFT)
	r01 = Label(frame_e1, text="")
	r01.pack(side=LEFT)
	r02 = Label(frame_e1, text="")
	r02.pack(side=LEFT)
	r03 = Label(frame_e1, text="")
	r03.pack(side=LEFT)
	r04 = Label(frame_e1, text="")
	r04.pack(side=LEFT)
	
	frame_e2 = Frame(frame5)
	frame_e2.pack(side=TOP)
	r10 = Label(frame_e2, text="")
	r10.pack(side=LEFT)
	r11 = Label(frame_e2, text="")
	r11.pack(side=LEFT)
	r12 = Label(frame_e2, text="")
	r12.pack(side=LEFT)
	r13 = Label(frame_e2, text="")
	r13.pack(side=LEFT)
	r14 = Label(frame_e2, text="")
	r14.pack(side=LEFT)
	
	frame_e3 = Frame(frame5)
	frame_e3.pack(side=TOP)
	r20 = Label(frame_e3, text="")
	r20.pack(side=LEFT)
	r21 = Label(frame_e3, text="")
	r21.pack(side=LEFT)
	r22 = Label(frame_e3, text="")
	r22.pack(side=LEFT)
	r23 = Label(frame_e3, text="")
	r23.pack(side=LEFT)
	r24 = Label(frame_e3, text="")
	r24.pack(side=LEFT)
	
	frame_e4 = Frame(frame5)
	frame_e4.pack(side=TOP)
	r30 = Label(frame_e4, text="")
	r30.pack(side=LEFT)
	r31 = Label(frame_e4, text="")
	r31.pack(side=LEFT)
	r32 = Label(frame_e4, text="")
	r32.pack(side=LEFT)
	r33 = Label(frame_e4, text="")
	r33.pack(side=LEFT)
	r34 = Label(frame_e4, text="")
	r34.pack(side=LEFT)
	
	
	frame6 = Frame(root)
	frame6.pack(side=TOP)
	
	frame_d1 = Frame(frame6)
	frame_d1.pack(side=TOP)
	v00 = Label(frame_d1, text="")
	v00.pack(side=LEFT)
	v01 = Label(frame_d1, text="")
	v01.pack(side=LEFT)
	v02 = Label(frame_d1, text="")
	v02.pack(side=LEFT)
	v03 = Label(frame_d1, text="")
	v03.pack(side=LEFT)
	v04 = Label(frame_d1, text="")
	v04.pack(side=LEFT)
	
	frame_d2 = Frame(frame6)
	frame_d2.pack(side=TOP)
	v10 = Label(frame_d2, text="")
	v10.pack(side=LEFT)
	v11 = Label(frame_d2, text="")
	v11.pack(side=LEFT)
	v12 = Label(frame_d2, text="")
	v12.pack(side=LEFT)
	v13 = Label(frame_d2, text="")
	v13.pack(side=LEFT)
	v14 = Label(frame_d2, text="")
	v14.pack(side=LEFT)
	
	frame_d3 = Frame(frame6)
	frame_d3.pack(side=TOP)
	v20 = Label(frame_d3, text="")
	v20.pack(side=LEFT)
	v21 = Label(frame_d3, text="")
	v21.pack(side=LEFT)
	v22 = Label(frame_d3, text="")
	v22.pack(side=LEFT)
	v23 = Label(frame_d3, text="")
	v23.pack(side=LEFT)
	v24 = Label(frame_d3, text="")
	v24.pack(side=LEFT)
	
	frame_d4 = Frame(frame6)
	frame_d4.pack(side=TOP)
	v30 = Label(frame_d4, text="")
	v30.pack(side=LEFT)
	v31 = Label(frame_d4, text="")
	v31.pack(side=LEFT)
	v32 = Label(frame_d4, text="")
	v32.pack(side=LEFT)
	v33 = Label(frame_d4, text="")
	v33.pack(side=LEFT)
	v34 = Label(frame_d4, text="")
	v34.pack(side=LEFT)
	

	root.mainloop()















### Proba dzialania metod okienek
#	okienko1.toggle_a()
#	okienko2.toggle_b()
#	okienko3.toggle_a()
#	okienko3.toggle_b()
#	print(queue)
#	okienko1.kolejny(obsl, queue, zwykly, kl_vip)
#	print(queue)
#	time.sleep(0.75)
#	zwykly.wejscie("b", next(gen_ID), obsl, queue, okienko1, okienko2, okienko3, zwykly, kl_vip)
#	print(queue)
#	time.sleep(0.75)
#	zwykly.wejscie("a", next(gen_ID), obsl, queue, okienko1, okienko2, okienko3, zwykly, kl_vip)
#	print(queue)
#	time.sleep(0.75)
#	okienko3.kolejny(obsl, queue, zwykly, kl_vip)
#	zwykly.wejscie("b", next(gen_ID), obsl, queue, okienko1, okienko2, okienko3, zwykly, kl_vip)
#	time.sleep(4.5)
#	okienko3.kolejny(obsl, queue, zwykly, kl_vip)
#	print(queue)
#	tab_zwykly, tab_vip = Zakoncz(okienko1, okienko2, okienko3)
#	print(tab_zwykly, "\n\n", tab_vip)
#	queue, obsl, zwykly, kl_vip, utime, gen_ID, okienko1, okienko2, okienko3 = Setup()
#	print("\n\n\n", queue, obsl, utime, gen_ID, okienko3.a_logs, okienko3.b_logs, okienko3.aVIP_logs, okienko3.bVIP_logs)

### Proba dzialania w petli
#	stop = 0
#	while stop < 7:
#		if (time.time() - utime > 1):
#			utime = time.time()
#			kl_vip.tick(obsl)
#			zwykly.tick(obsl)
#			stop += 1
#			print("minela sekunda!")
#			if stop == 5:
#				print("      ", queue)
#				okienko1.kolejny(obsl)
#				okienko1.kolejny(obsl)
#				print("      ", queue)

### Objasnienie nazewnictwa tabelek
#	#wyświetl całą kolejkę:
#	print(queue)
#	#wyświetl wszystkich klientów danego rodzaju w kolejce (w tym przypadku zwyklych A):
#	print(queue[0])
#	#wyświetl danego klienta (w tym przypadku pierwszego typu zwykły A)
#	print(queue[0][0])
#	#wyświetl dany parametr klienta (tutaj ID powyższego klienta)
#	print(queue[0][0][0])