import random
import time
import statistics
import numpy as np


class WrongClientTypeException(Exception):
	"""Rzucany gdy wprowadzony klient jest nieobsługiwanego typu"""
	pass

class UnrecognizedModesException(Exception):
	"""Rzuczany gdy okienko zawiera nierozpoznane tryby działania"""
	pass


def GenenerateClientID():
	"""Generator nadający klientom unikatowe ID"""
	ID = 0
	while True:
		yield ID
		ID += 1 


def mean_df0(*args):
	"""Funkcja licząca średnio lub zwracająca zero gdy wywołana jest dla zbioru pustego"""
	try:
		total = 0
		i = 0
		for arg in args:
			total += arg
			i += 1
		mean = total / i
	except ZeroDivisionError:
		mean = 0
	return mean


class Klient():
	"""Klasa po której dziedziczą klasy wszystkich klientów"""
	def wejscie(self, type, ID, queue):
		if type not in ["A", "a", "B", "b"]:
			raise WrongClientTypeException("Klient musi byc typu A lub B")
	def wyjscie(self, type, done, queue):
		if type not in ["A", "a", "B", "b"]:
			raise WrongClientTypeException("Klient musi byc typu A lub B")
	def tick(self, queue):
		pass


class KlientZwykly(Klient):
	"""Klasa zawierająca metody klientów zwykłych"""
	def wejscie(self, type, ID, done, queue, okienko1, okienko2, okienko3, zwykly, kl_vip):
		"""Wprowadź do kolejki nowego klienta zwykłego"""
		super().wejscie(type, ID, queue)
		gen_time = time.time()
		if type in str(["A", "a"]):
			queue[0].append([ID, gen_time])
			#Jeśli okienko A "czekało" na klienta to natychmiast po wejściu obsłuż go
			if (len(queue[0]) == 1 and len(queue[2]) == 0):
				for okienko in [okienko1, okienko2, okienko3]:
					if (okienko.waiting == True and okienko.mode[0] == 1):
						okienko.kolejny(done, queue, zwykly, kl_vip)
						break
		elif type in str(["B", "b"]):
			queue[1].append([ID, gen_time])
			#Jeśli okienko B "czekało" na klienta to natychmiast po wejściu obsłuż go
			if (len(queue[1]) == 1 and len(queue[3]) == 0):
				for okienko in [okienko1, okienko2, okienko3]:
					if (okienko.waiting == True and okienko.mode[1] == 1):
						okienko.kolejny(done, queue, zwykly, kl_vip)
						break
	
	def wyjscie(self, type, done, queue):
		"""Obsłuż pierwszego zwykłego klienta danego typu"""
		super().wyjscie(type, done, queue)
		try:
			if type in str(["A", "a"]):
				d_client = queue[0].pop(0)
				done.append([d_client[0], round((time.time() - d_client[1]), 2)])
			elif type in str(["B", "b"]):
				d_client = queue[1].pop(0)
				done.append([d_client[0], round((time.time() - d_client[1]), 2)])
		except IndexError as e:
			print("Empty queue!")
		else:
			return d_client
	
	def tick(self, done, queue):
		"""Klienci zwykli nie potrzebują metody tick"""
		pass


class KlientVIP(Klient):
	"""Klasa zawierająca metody klientów VIP"""
	def wejscie(self, type, ID, done, queue, okienko1, okienko2, okienko3, zwykly, kl_vip):
		"""Wprowadź do kolejki nowego klienta zwykłego"""
		super().wejscie(type, ID, queue)
		gen_time = time.time()
		if type in str(["A", "a"]):
			queue[2].append([ID, gen_time])
			if (len(queue[0]) == 0) and (len(queue[2]) == 1):
				for okienko in [okienko1, okienko2, okienko3]:
					if (okienko.waiting == True and okienko.mode[0] == 1):
						okienko.kolejny(done, queue, zwykly, kl_vip)
						break
		elif type in str(["B", "b"]):
			queue[3].append([ID, gen_time])
			if (len(queue[1]) == 0 and len(queue[3]) == 1):
				for okienko in [okienko1, okienko2, okienko3]:
					if (okienko.waiting == True and okienko.mode[1] == 1):
						okienko.kolejny(done, queue, zwykly, kl_vip)
						break
	
	def wyjscie(self, type, done, queue):
		"""Obsłuż pierwszego klienta VIP danego typu"""
		super().wyjscie(type, done, queue)
		try:
			if type in str(["A", "a"]):
				d_client = queue[2].pop(0)
				done.append([d_client[0], round((time.time() - d_client[1]), 2)])
			elif type in str(["B", "b"]):
				d_client = queue[3].pop(0)
				done.append([d_client[0], round((time.time() - d_client[1]), 2)])
		except IndexError as e:
			print("Empty queue!")
		else:
			return d_client
	
	def tick(self, done, queue):
		""""Jeśli VIP czeka w kolejce ponad 10s to opuszcza ją pozostawiając komentarz"""
		if len(queue[2])>0:
			for klientVIP_A in queue[2]:
				if (time.time() - klientVIP_A[1] > 10):
					print("To skandaliczne!")
					self.wyjscie("A", done, queue)
		if len(queue[3])>0:
			for klientVIP_B in queue[3]:
				if (time.time() - klientVIP_B[1] > 10):
					print("To skandaliczne!")
					self.wyjscie("B", done, queue)
	
	
class Okienko():
	def __init__(self):
		#pierwsza liczba odpowiada obslugiwaniu klientow typu a, druga klientow typu b
		self.mode = [0, 0]
		self.waiting = False
		self.a_logs = []
		self.b_logs = []
		self.aVIP_logs = []
		self.bVIP_logs = []
		
	def toggle_a(self):
		self.mode[0] = 1 - self.mode[0]
	
	def toggle_b(self):
		self.mode[1] = 1 - self.mode[1]
	
	def kolejny(self, done, queue, zwykly, kl_vip):
		"""Ustal tryb dzialania okienka i przejdź do odpowiedniej funkcji"""
		self.waiting = False
		if self.mode == [1, 1]:
			self.next_ab(done, queue, zwykly, kl_vip)
		elif self.mode == [1, 0]:
			self.next_a(done, queue, zwykly, kl_vip)
		elif self.mode == [0, 1]:
			self.next_b(done, queue, zwykly, kl_vip)
		elif self.mode == [0, 0]:
			pass
		else:
			raise UnrecognizedModesException
		
	def next_ab(self, done, queue, zwykly, kl_vip):
		"""Obsłuż dowolnego klienta zgodnie z zasadami"""
		curr = [-1, -1]
		#Najpierw spróbuj obsluzyc pierwszego w kolejce VIP'a
		if len(queue[2])>0 and len(queue[3])>0:
			#Jeśli w kolejce są zarówno VIP a jak i VIP b, to obsłuż tego o najmniejszym ID (a więc czekającego najdłużej)
			if queue[2][0][0] < queue[3][0][0]:
				curr = kl_vip.wyjscie("A", done, queue)
				self.aVIP_logs.append(time.time() - curr[1])
			else:
				curr = kl_vip.wyjscie("B", done, queue)
				self.bVIP_logs.append(time.time() - curr[1])
		elif len(queue[2]) > 0:
			curr = kl_vip.wyjscie("A", done, queue)
			self.aVIP_logs.append(time.time() - curr[1])
		elif len(queue[3]) > 0:
			curr = kl_vip.wyjscie("B", done, queue)
			self.bVIP_logs.append(time.time() - curr[1])
		#Jezeli w kolecje nie ma VIPow to obsluz zwykłego zgodnie z tymi samymi zasadami
		elif (len(queue[0])>0 and len(queue[1])>0):
			if queue[0][0][0] < queue[1][0][0]:
				curr = zwykly.wyjscie("A", done, queue)
				self.a_logs.append(time.time() - curr[1])
			else:
				curr = zwykly.wyjscie("B", done, queue)
				self.b_logs.append(time.time() - curr[1])
		elif len(queue[0]) > 0:
			curr = zwykly.wyjscie("A", done, queue)
			self.a_logs.append(time.time() - curr[1])
		elif len(queue[1]) > 0:
			curr = zwykly.wyjscie("B", done, queue)
			self.b_logs.append(time.time() - curr[1])
		else:
#			print("Czekam na klienta")
			self.waiting = True
	
	def next_a(self, done, queue, zwykly, kl_vip):
		"""Obsłuż najstarszego klenta A, najpierw VIP"""
		curr = [-1, -1]
		if len(queue[2]) > 0:
			curr = kl_vip.wyjscie("A", done, queue)
			self.aVIP_logs.append(time.time() - curr[1])
		elif len(queue[0]) > 0:
			curr = zwykly.wyjscie("A", done, queue)
			self.a_logs.append(time.time() - curr[1])
		else:
#			print("Czekam na kl. A")
			self.waiting = True
		
	def next_b(self, done, queue, zwykly, kl_vip):
		"""Obsłuż najstarszego klenta A, najpierw VIP"""
		curr = [-1, -1]
		if len(queue[3]) > 0:
			curr = kl_vip.wyjscie("B", done, queue)
			self.bVIP_logs.append(time.time() - curr[1])
		elif len(queue[1]) > 0:
			curr = zwykly.wyjscie("B", done, queue)
			self.b_logs.append(time.time() - curr[1])
		else:
#			print("Czekam na kl. B")
			self.waiting = True


def Setup():
	"""Zainicjuj potrzebne zmienne i obiekty klas Okienko oraz Klient"""
	utime = time.time()
	#kolejne wiersze przeznaczone odpowiedio klientom:
	#zwylkly A, zwykly B, VIP A, VIP B
	queue = [[], [], [], []]
	obsl = []
	gen_ID = GenenerateClientID()
	zwykly = KlientZwykly()
	kl_vip = KlientVIP()
	okienko1 = Okienko()
	okienko2 = Okienko()
	okienko3 = Okienko()
	return (queue, obsl, zwykly, kl_vip, utime, gen_ID, okienko1, okienko2, okienko3)


def Zakoncz(okienko1, okienko2, okienko3):
	"""Policz średnie czasy obsługi, zwróć odpowiednie tabelki (np.array)"""
	for okienko in (okienko1, okienko2, okienko3):
		mean_zwykly_a = mean_df0(*okienko.a_logs)
		mean_zwykly_b = mean_df0(*okienko.b_logs)
		mean_VIP_a = mean_df0(*okienko.aVIP_logs)
		mean_VIP_b = mean_df0(*okienko.bVIP_logs)
#		print("Srednie:\n    VIP_a: ", round(mean_VIP_a, 3), "\n    VIP_b: ", round(mean_VIP_b, 3), "\n    reg_a: ", round(mean_zwykly_a, 3),  "\n    reg_b: ", round(mean_zwykly_b, 3), "\n")
	
	mean_zwykly_a = mean_df0(*(okienko1.a_logs + okienko2.a_logs + okienko3.a_logs))
	mean_zwykly_b = mean_df0(*(okienko1.b_logs + okienko2.b_logs + okienko3.b_logs))
	mean_zwykly_total = mean_df0(*(okienko1.a_logs + okienko2.a_logs + okienko3.a_logs + okienko1.b_logs + okienko2.b_logs + okienko3.b_logs))
	mean_VIP_a = mean_df0(*(okienko1.aVIP_logs + okienko2.aVIP_logs + okienko3.aVIP_logs))
	mean_VIP_b = mean_df0(*(okienko1.bVIP_logs + okienko2.bVIP_logs + okienko3.bVIP_logs))
	mean_VIP_total = mean_df0(*(okienko1.aVIP_logs + okienko2.aVIP_logs + okienko3.aVIP_logs + okienko1.bVIP_logs + okienko2.bVIP_logs + okienko3.bVIP_logs))
	tab_zwykly = np.array([
		["      ---      ", "Okienko1", "Okienko2", "Okienko3", "Łącznie"],
		["Sprawa A", "  %.3f  " % mean_df0(*okienko1.a_logs), "  %.3f  " % mean_df0(*okienko2.a_logs), "    %.3f  " % mean_df0(*okienko3.a_logs), "    %.3f  " % mean_zwykly_a],
		["Sprawa B", "  %.3f  " % mean_df0(*okienko1.b_logs), "  %.3f  " % mean_df0(*okienko2.b_logs), "    %.3f  " % mean_df0(*okienko3.b_logs), "    %.3f  " % mean_zwykly_b],
		[" Łącznie  ", "  %.3f  " % mean_df0(*(okienko1.a_logs + okienko1.b_logs)), "  %.3f  " % mean_df0(*(okienko2.a_logs + okienko2.b_logs)), "    %.3f  " % mean_df0(*(okienko3.a_logs + okienko3.b_logs)), "    %.3f  " % mean_zwykly_total]
	])
	tab_vip = np.array([
		["      ---      ", "Okienko1", "Okienko2", "Okienko3", "Łącznie"],
		["Sprawa A", "  %.3f  " % mean_df0(*okienko1.aVIP_logs), "  %.3f  " % mean_df0(*okienko2.aVIP_logs), "    %.3f  " % mean_df0(*okienko3.aVIP_logs), "    %.3f  " % mean_VIP_a],
		["Sprawa B", "  %.3f  " % mean_df0(*okienko1.bVIP_logs), "  %.3f  " % mean_df0(*okienko2.bVIP_logs), "    %.3f  " % mean_df0(*okienko3.bVIP_logs), "    %.3f  " % mean_VIP_b],
		[" Łącznie  ", "  %.3f  " % mean_df0(*(okienko1.aVIP_logs + okienko1.bVIP_logs)), "  %.3f  " % mean_df0(*(okienko2.aVIP_logs + okienko2.bVIP_logs)), "    %.3f  " % mean_df0(*(okienko3.aVIP_logs + okienko3.bVIP_logs)), "    %.3f  " % mean_VIP_total]
	])
	return (tab_zwykly, tab_vip)

