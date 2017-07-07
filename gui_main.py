from client import danmu,danmu_gui,socket_connect
from multiprocessing import Process, Queue
if __name__ == "__main__":
    q = Queue()
    pw = Process(target=danmu_gui.invoke_gui, args=(q,))
    pr = Process(target=socket_connect.invoke_sock, args=(q,))
    pw.start()
    pr.start()