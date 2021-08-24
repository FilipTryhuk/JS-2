import unittest
import time

from projekt import *

class Test(unittest.TestCase):
	#wszystkie testy uzywaja sleep aby zasymulować rezczywiste odstępy pomiędzy kliknięciami przycisków
	
	def test_multipleClientsNoQueueTime(self):
		"""Sprwadź czy klient b został natychmiast obsłużony przez czekające okienko"""
		queue, obsl, zwykly, kl_vip, utime, gen_ID, okienko1, okienko2, okienko3 = Setup()
		okienko1.toggle_a()
		okienko2.toggle_b()
		okienko3.toggle_a()
		okienko3.toggle_b()
		zwykly.wejscie("a", next(gen_ID), obsl, queue, okienko1, okienko2, okienko3, zwykly, kl_vip)
		time.sleep(0.2)
		okienko2.kolejny(obsl, queue, zwykly, kl_vip)
		time.sleep(0.2)
		okienko1.kolejny(obsl, queue, zwykly, kl_vip)
		time.sleep(0.2)
		zwykly.wejscie("B", next(gen_ID), obsl, queue, okienko1, okienko2, okienko3, zwykly, kl_vip)
		tab_zwykly, tab_vip = Zakoncz(okienko1, okienko2, okienko3)
		self.assertTrue(float(tab_zwykly[2][3]) < 0.1)

	def test_vipPriority(self):
		"""Sprwadź czy klient vip został obsłużony przed klientem zwykłym, wbrew kolejności przyjścia"""
		queue, obsl, zwykly, kl_vip, utime, gen_ID, okienko1, okienko2, okienko3 = Setup()
		okienko1.toggle_a()
		okienko2.toggle_b()
		okienko3.toggle_a()
		okienko3.toggle_b()
		zwykly.wejscie("a", next(gen_ID), obsl, queue, okienko1, okienko2, okienko3, zwykly, kl_vip)
		time.sleep(0.2)
		kl_vip.wejscie("a", next(gen_ID), obsl, queue, okienko1, okienko2, okienko3, zwykly, kl_vip)
		time.sleep(0.2)
		okienko1.kolejny(obsl, queue, zwykly, kl_vip)
		time.sleep(0.2)
		okienko3.kolejny(obsl, queue, zwykly, kl_vip)
		tab_zwykly, tab_vip = Zakoncz(okienko1, okienko2, okienko3)
		self.assertTrue(float(tab_zwykly[3][3]) > float(tab_vip[3][1]))

	def test_vipAregularB(self):
		"""Sprwadź czy obsłużeni zostali obaj klienci"""
		queue, obsl, zwykly, kl_vip, utime, gen_ID, okienko1, okienko2, okienko3 = Setup()
		okienko1.toggle_a()
		okienko2.toggle_b()
		okienko3.toggle_a()
		okienko3.toggle_b()
		kl_vip.wejscie("a", next(gen_ID), obsl, queue, okienko1, okienko2, okienko3, zwykly, kl_vip)
		zwykly.wejscie("b", next(gen_ID), obsl, queue, okienko1, okienko2, okienko3, zwykly, kl_vip)
		time.sleep(0.2)
		okienko3.kolejny(obsl, queue, zwykly, kl_vip)
		time.sleep(0.2)
		okienko2.kolejny(obsl, queue, zwykly, kl_vip)
		tab_zwykly, tab_vip = Zakoncz(okienko1, okienko2, okienko3)
		self.assertTrue(len(queue[1]) == 0 and len(queue[2]) == 0)
		
	def test_vipBregularA(self):
		"""Sprwadź czy obsłużeni zostali obaj klienci"""
		queue, obsl, zwykly, kl_vip, utime, gen_ID, okienko1, okienko2, okienko3 = Setup()
		okienko1.toggle_a()
		okienko2.toggle_b()
		okienko3.toggle_a()
		okienko3.toggle_b()
		kl_vip.wejscie("B", next(gen_ID), obsl, queue, okienko1, okienko2, okienko3, zwykly, kl_vip)
		zwykly.wejscie("a", next(gen_ID), obsl, queue, okienko1, okienko2, okienko3, zwykly, kl_vip)
		time.sleep(0.2)
		okienko3.kolejny(obsl, queue, zwykly, kl_vip)
		time.sleep(0.2)
		okienko1.kolejny(obsl, queue, zwykly, kl_vip)
		tab_zwykly, tab_vip = Zakoncz(okienko1, okienko2, okienko3)
		self.assertTrue(len(queue[0]) == 0 and len(queue[3]) == 0)
		
	def test_onlyA(self):
		"""Sprawdź, czy czas oczekiwania jest równy 0, gdy żaden klient nie został obsłużony"""
		queue, obsl, zwykly, kl_vip, utime, gen_ID, okienko1, okienko2, okienko3 = Setup()
		okienko1.toggle_a()
		okienko2.toggle_b()
		okienko3.toggle_a()
		okienko3.toggle_b()
		zwykly.wejscie("a", next(gen_ID), obsl, queue, okienko1, okienko2, okienko3, zwykly, kl_vip)
		tab_zwykly, tab_vip = Zakoncz(okienko1, okienko2, okienko3)
		self.assertEqual(float(tab_zwykly[3][1]), 0)
		
	def test_vipTimeout(self):
		"""Sprawdź, czy klient VIP sam opuszcza kolejkę po 10 sekundach"""
		queue, obsl, zwykly, kl_vip, utime, gen_ID, okienko1, okienko2, okienko3 = Setup()
		okienko1.toggle_a()
		okienko2.toggle_b()
		okienko3.toggle_a()
		okienko3.toggle_b()
		zwykly.wejscie("a", next(gen_ID), obsl, queue, okienko1, okienko2, okienko3, zwykly, kl_vip)
		kl_vip.wejscie("B", next(gen_ID), obsl, queue, okienko1, okienko2, okienko3, zwykly, kl_vip)
		time.sleep(0.2)
		okienko1.kolejny(obsl, queue, zwykly, kl_vip)
		stop = 0
		while stop < 11:
			if (time.time() - utime > 1):
				utime = time.time()
				kl_vip.tick(obsl, queue)
				zwykly.tick(obsl, queue)
				stop += 1
		self.assertTrue(len(queue[0]) == 0 and len(queue[3]) == 0)
		
	def test_full_queue(self):
		"""Sprawdź czy klienci każdego typu zostali poprawnie obsłużeni"""
		queue, obsl, zwykly, kl_vip, utime, gen_ID, okienko1, okienko2, okienko3 = Setup()
		okienko1.toggle_a()
		okienko2.toggle_b()
		okienko3.toggle_a()
		okienko3.toggle_b()
		for i in range(4):
			zwykly.wejscie("a", next(gen_ID), obsl, queue, okienko1, okienko2, okienko3, zwykly, kl_vip)
			zwykly.wejscie("b", next(gen_ID), obsl, queue, okienko1, okienko2, okienko3, zwykly, kl_vip)
			kl_vip.wejscie("a", next(gen_ID), obsl, queue, okienko1, okienko2, okienko3, zwykly, kl_vip)
			kl_vip.wejscie("b", next(gen_ID), obsl, queue, okienko1, okienko2, okienko3, zwykly, kl_vip)
		for i in range(8):
			time.sleep(0.2)
			okienko1.kolejny(obsl, queue, zwykly, kl_vip)
			okienko2.kolejny(obsl, queue, zwykly, kl_vip)
		tab_zwykly, tab_vip = Zakoncz(okienko1, okienko2, okienko3)
		self.assertTrue(len(queue[0]) == 0 and len(queue[1]) == 0 and len(queue[2]) == 0 and len(queue[3]) == 0)
		
		
if __name__ == '__main__':
	unittest.main()