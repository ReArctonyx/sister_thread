# import os, re dan threading
import os, re
from threading import Thread

# import time
import time

# buat kelas ip_check
class ip_check(Thread):
    
    # fungsi __init__; init untuk assign IP dan hasil respons = -1
    def __init__ (self,ip):
        Thread.__init__(self)
        self.ip = ip
        self.status = -1
    
    # fungsi utama yang diekseskusi ketika thread berjalan
    def run(self):
        # lakukan ping dengan perintah ping -n (gunakan os.popen())
        ping = os.popen("ping -q -c2 "+self.ip,"r")
        
        # loop forever
        while True:
            # baca hasil respon setiap baris
            line = ping.readline()
            
            # break jika tidak ada line lagi
            if not line: break
            
            
            # baca hasil per line dan temukan pola Received = x
            igot = re.findall(ip_check.lifeline,line)
            
            # tampilkan hasilnya
            if igot:
                self.status = int(igot[0])
                

            
# buat regex untuk mengetahui isi dari r"Received = (\d)"
ip_check.lifeline = re.compile(r"(\d) received")
report = ("No response","Partial Response","Alive")


# catat waktu awal
start = time.time()

# buat list untuk menampung hasil pengecekan
pinglist = []

# lakukan ping untuk 20 host
for suffix in range(1,20):
    # tentukan IP host apa saja yang akan di ping
    ip = "192.168.200."+str(suffix)

    
    # panggil thread untuk setiap IP
    current = ip_check(ip)
    
    # masukkan setiap IP dalam list
    pinglist.append(current)
    
    # jalankan thread
    current.start()

# untuk setiap IP yang ada di list
for el in pinglist:
    
    # tunggu hingga thread selesai
    el.join()
    
    # dapatkan hasilnya
    print ("Status from ",el.ip,"is",report[el.status])
    

# catat waktu berakhir
stop = time.time()

# tampilkan selisih waktu akhir dan awal
print ((stop-start))
