import threading  # Import modul threading untuk membuat thread
import math        # Import modul math untuk pembagian data
from queue import Queue  # Queue untuk menyimpan hasil sementara antar thread

# Fungsi yang akan dijalankan oleh setiap thread
def partial_sum(start, end, result_queue):
    """Menjumlahkan angka dari start hingga end, lalu hasilnya dimasukkan ke queue."""
    total = 0
    for i in range(start, end + 1):  # Loop dari start ke end
        total += i
    result_queue.put(total)  # Simpan hasil ke antrian agar bisa diambil di thread utama
    

if __name__ == "__main__":
    # Input dari pengguna
    # start_num = int(input("Input angka awal: "))         #untuk input angka awal
    # end_num = int(input("Input angka akhir: "))          #untuk angka akhir
    # thread_count = int(input("Thread yang digunakan: ")) #untuk Thread yang ingin digunakan
    start_num = 1
    end_num = 10
    thread_count = 4
    # Pastikan jumlah thread minimal 2
    if thread_count < 2: # Jika Thread kurang dari 2
        print("Minimal thread yang digunakan adalah 2.") # maka kasih peringatan
        exit() # dan menghentikan program

    result_queue = Queue()     # queue untuk menampung hasil penjumlahan (secara parsial)

    # Hitung berapa banyak angka yang akan dikerjakan setiap thread
    total_numbers = end_num - start_num + 1 # menghitung jumlah total angka yang akan di jumlahkan
    chunk_size = math.ceil(total_numbers / thread_count)  # Bagi rata ke setiap thread

    threads = []  # List untuk menyimpan semua thread

    # Buat dan mulai setiap thread
    for i in range(thread_count): # memulai looping sebanyak jumlah thread
        sub_start = start_num + i * chunk_size # menentukan awal thread ke i
        sub_end = min(sub_start + chunk_size - 1, end_num)  # Jangan melebihi angka akhir

        # Buat thread baru untuk menjumlahkan sebagian data
        t = threading.Thread(target=partial_sum, args=(sub_start, sub_end, result_queue)) # inisiasi variabel untuk menyimpan thread
        threads.append(t) # menggabungkan thread ke list
        t.start()  # Jalankan thread

    # Tunggu semua thread selesai
    for t in threads:
        t.join()

    # Ambil semua hasil dari queue dan jumlahkan
    total_sum = 0
    while not result_queue.empty(): #selama queue masih ada
        total_sum += result_queue.get() # tambahkan ke total

    # Tampilkan hasil akhir
    print(f"Hasil penjumlahan: {total_sum}")
