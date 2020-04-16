#import os, request, threading, time dan lib request, error dan parse
import os
import requests
import threading
import urllib.request, urllib.error, urllib.parse
import time

#masukkan url image yang akan di download
url = "https://apod.nasa.gov/apod/image/1901/LOmbradellaTerraFinazzi.jpg"

#fungsi untuk menyambungkan ke range byte yang akan digunakan saat splitting buffer
def buildRange(value, numsplits):
    #masukkan variable untuk menampung range byte
    lst = []
    #perulangan sampai x
    for i in range(numsplits):
        #jika range masih 0 maka initialnya masih bernilai i(0) juga
        if i == 0:
            lst.append('%s-%s' % (i, int(round(1 + i * value/(numsplits*1.0) + value/(numsplits*1.0)-1, 0))))
        #jika i bukan 0 maka akan dilanjutkan dengan value range byte sebelumnya, range byte sebelumnya+range byte tambahan
        else:
            lst.append('%s-%s' % (int(round(1 + i * value/(numsplits*1.0),0)), int(round(1 + i * value/(numsplits*1.0) + value/(numsplits*1.0)-1, 0))))
    #return range byte
    return lst

#fungsi untuk mendownload secara konkuren sebanyak x number
class SplitBufferThreads(threading.Thread):
    """ Splits the buffer to ny number of threads
        thereby, concurrently downloading through
        ny number of threads.
    """
    #inisialisasi url dan range byte yang akan dipakai
    def __init__(self, url, byteRange):
        super(SplitBufferThreads, self).__init__()
        self.__url = url
        self.__byteRange = byteRange
        self.req = None
    #fungsi untuk requesting
    def run(self):
        self.req = urllib.request.Request(self.__url,  headers={'Range': 'bytes=%s' % self.__byteRange})
    #fungsi untuk mengambil data image secara konkuren
    def getFileData(self):
        return urllib.request.urlopen(self.req).read()

#fungsi utama
def main(url=None, splitBy=3):
    #ambil waktu mulai
    start_time = time.time()
    #error handling apabila url kosong
    if not url:
        print("Please Enter some url to begin download.")
        return
    #nama file
    fileName = url.split('/')[-1]
    #mengambil ukuran file/image yang akan di download dalam byte
    sizeInBytes = requests.head(url, headers={'Accept-Encoding': 'identity'}).headers.get('content-length', None)
    #menampilkan ukuran file/image yang akan di download dalam byte
    print("%s bytes to download." % sizeInBytes)
    #error handling jika image/file tidak memiliki ukuran atau tidak ada file yang bisa di download
    if not sizeInBytes:
        print("Size cannot be determined.")
        return
    #list untuk menampung file/image yang telah di download
    dataLst = []
    #perulangan sebanyak x
    for idx in range(splitBy):
        #menginisiasi range byte yang akan dipakai
        byteRange = buildRange(int(sizeInBytes), splitBy)[idx]
        #menjalankan fungsi SplitBufferThreads
        bufTh = SplitBufferThreads(url, byteRange)
        #memulai download
        bufTh.start()
        #...
        bufTh.join()
        #memasukkan part-part file yang didownload secara terpisah menjadi ke list
        dataLst.append(bufTh.getFileData())
    #decode data list
    content = b''.join(dataLst)

    #mengecek jika dataLst tidak kosong
    if dataLst:
        #mengecek jika file multiple
        if os.path.exists(fileName):
            #menghapus file
            os.remove(fileName)
        #menampilkan selisih waktu akhir dan waktu mulai
        print("--- %s seconds ---" % str(time.time() - start_time))
        #membuat/writing file yang telah di download
        with open(fileName, 'wb') as fh:
            fh.write(content)
        #menampilkan bahwa file telah di download
        print("Finished Writing file %s" % fileName)

if __name__ == '__main__':
    main(url)
