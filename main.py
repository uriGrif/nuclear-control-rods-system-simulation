from multiprocessing import Process, Queue
from simulador import run_simulador
from graficador import run_graficador

if __name__ == '__main__':
    q = Queue()
    p_sim = Process(target=run_simulador, args=(q,))
    p_graf = Process(target=run_graficador, args=(q,))
    p_sim.start()
    p_graf.start()
    p_sim.join()
    p_graf.join()
