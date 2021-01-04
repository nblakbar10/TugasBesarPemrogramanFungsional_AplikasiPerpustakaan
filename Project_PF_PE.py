import multiprocessing
import time
from datetime import datetime as date
import sys
import os
import pymysql

db = pymysql.connect(
  host="localhost",
  user="root",
  passwd="",
  database="project_pf"
)

arynama,arynim,aryjudul,arytglpinjam,arylamapinjam = [],[],[],[],[]
yess = ["1","y","ya","Ya","yes","iya"]
noo = ["2","n","no","tidak"]
gg = ("="*30)
sekarang = date.now().strftime('%Y-%m-%d')
print(sekarang)

def menu():

    print('''
    *********************  \033[34mSIBUDI\033[0m  **********************
    **** Sistem Peminjaman Buku Perpustakaan Digital ****
    Pilih Menu :
    1. Pinjam Buku
    2. Kembalikan Buku
    3. Cetak Struk Bukti Pinjam
    4. Cek Daftar Buku Lengkap
    5. Lihat History Peminjam Buku
    6. Lihat Peraturan Perpustakaan
    7. Matikan Aplikasi\033[0m
    *****************************************************
    ''')
    while True:
        try:
            pil = int(input('\nMasukkan Pilihan Anda : '))
            if(pil==1):
                pinjambuku()
                ulang()
            elif(pil==2):
                kembalikanbuku()
                ulang()
            elif(pil==3):
                cetakstruk()
                ulang()
            elif(pil==4):
                daftarbuku()
                ulang()
            elif(pil==5):
                daftarpinjam()
                ulang()
            elif(pil==6):
                peraturan()
                ulang()
            elif(pil==7):
                print("Terima Kasih, Sampai jumpa kembali.")
                quit()
            else:
                print('Pilihan tidak tersedia\033[0m')
                ulang()
        except ValueError:
            print("Inputan anda salah ! Silahkan ulangi kembali...")

def ulang():
    ulang = input('Apakah anda ingin mencoba lagi ? \n1.Ya\n2.Tidak\n-> ')
    print(gg)
    if ulang in yess:
        menu()
    elif ulang in noo:
        print('Terima kasih, sampai jumpa kembali!')
        quit()
    else:
        print('\033[31mInputan anda salah ! Pilih (Ya) atau (Tidak) !\033[0m')
        ulang()


def pinjambuku():
    print("Silahkan masukkan data diri Anda\n")
    nama = str(input("\033[34mNama Peminjam Buku : "))
    while True:
        try:
            nim = int(input("NIM : "))
            break
        except ValueError:
            print("NIM hanya Berupa Angka...")
    judul = str(input("Judul Buku : "))
    tglpinjam = date.now().strftime('%Y-%m-%d')
    lamapinjam = int(input("Lama Pinjam : "))
    konfirm = str(input("Apakah data diri anda sudah benar?  \n1.Ya\n2.Tidak\n-> "))
    for i in range(1):
        cursor = db.cursor()
        sql = "INSERT INTO datapinjam (nama, nim, judul, tglpinjam, lamapinjam) VALUES (%s, %s, %s, %s, %s)"
        val = (nama, nim, judul, tglpinjam, lamapinjam)
        cursor.execute(sql, val)
        db.commit()

        #arynama.append(nama)
        #arynim.append(nim)
        #aryjudul.append(judul)
        #arytglpinjam.append(tglpinjam)
        #arylamapinjam.append(lamapinjam)
        if (konfirm in yess):
            print('Terimakasih telah meminjam buku ditempat kami, kami berharap agar anda dapat mengembalikan buku dengan tepat waktu\n')
            print('\033[31m*******Silahkan Ambil Struk Anda*******')
            print('_____________________________________________________')
            #kode untuk cetak struknya
            #struk = "struk.txt"
            sys.stdout = open("struk.txt", "w")
            print('''
                    *********************  SIBUDI  **********************
                    **** Sistem Peminjaman Buku Perpustakaan Digital ****
                    **************** Struk Bukti Pinjam *****************
                ''')

            print
            print('\t\t\tTanggal : ',tglpinjam,'-',date.now().strftime('%m - %Y'))
            print("\t\t\tNama Peminjam Buku : ",nama)
            print("\t\t\tNIM : ",nim)
            print("\t\t\tJudul Buku : ",judul)
            print("\t\t\tTanggal Peminjaman : ",tglpinjam,'-',date.now().strftime('%m - %Y'))
            print("\t\t\tLama Pinjam : ",lamapinjam, 'Hari')
            print('''
                    ***Terima Kasih Telah Meminjam Buku Ditempat Kami***
                    ***Struk Harap Dibawa pada saat pengembalian Buku***
                    ''')
            sys.stdout.close()
            sys.stdout = sys.__stdout__         #ini supaya pas file .txt nya diclose programnya ga muncul error, dan berulang ke kondisi "Apakah anda ingin mencoba lagi?
            time.sleep(1)
            os.system("struk.txt")
        else:
            print('Silahkan ulangi input data diri anda!')
            pinjambuku()

def kembalikanbuku():
    nama = str(input("\033[34mNama Peminjam Buku : "))
    while True:
        try:
            nim = int(input("NIM : "))
            break
        except ValueError:
            print("Inputan anda salah ! Silahkan ulangi kembali...")
    judul = str(input("Judul Buku : "))
    tglpinjam = str(input("Tanggal Pinjam : "))
    lamapinjam = int(input("Lama Pinjam : "))
    tglsekarang = sekarang
    konfirm = str(input("Apakah data diri anda sudah benar?  \n1.Ya\n2.Tidak\n-> "))
    if (konfirm == 'Ya' or konfirm == 'ya' or konfirm == 'Y' or konfirm == 'y' or konfirm == '1'):
        if (tglpinjam == tglsekarang) or (tglpinjam <= tglsekarang):
            cursor = db.cursor()
            sql = "DELETE FROM datapinjam WHERE nama=%s"
            val = (nama, )
            cursor.execute(sql, val)
            db.commit()
            print('Terimakasih telah mengembalikan buku dengan tepat waktu')
            print('=============================================================\n')

        else:
            print("\033[31mANDA TERLAMBAT MENGEMBALIKAN BUKU, ANDA AKAN DIKENAKAN DENDA 50.000 rupiah PER HARINYA")
            totalterlambat = tglpinjam+lamapinjam
            print("Lama Anda Telat : ", totalterlambat, "Hari")
            denda = 50000 * totalterlambat
            print("Jadi total denda yang harus anda bayar adalah = ", denda)

    else:
        print('Silahkan ulangi input data diri anda!')
        kembalikanbuku()

def cetakstruk():
    #nanti disini bakalan langsung redirect ke file .txt yang isinya berupa struk
    #os.startfile("")
    print('\033[31m*******Silahkan Ambil Struk Anda*******\033[0m')
    time.sleep(1)
    os.system("struk.txt")

def hitungdenda(tglpinjam, lamapinjam):
    totalterlambat = tglpinjam + lamapinjam
    print("Lama Anda Telat : ", totalterlambat, "Hari")
    denda = 50000 * totalterlambat
    print("Jadi total denda yang harus anda bayar adalah = ", denda)

def daftarbuku():
    #nanti disini dimasukkan file .txt yang isinya daftar buku di perpustakaan, nanti pas tampilannya mungkin bisa pop-up.
    #os.startfile("")
    print('\033[31mDaftar Buku Lengkap sedang diproses, mohon tunggu...\033[0m')
    time.sleep(2)
    os.system("daftarbuku.txt")

def daftarpinjam():
    print("Daftar History Peminjaman Buku: \n")
    print("Nama : %s\t\nNIM : %s\t\nJudul Buku : %s\t\nTanggal Pinjam : %s\t\nTanggal Kembali : %s"% (arynama,arynim,aryjudul,arytglpinjam,arytglkembali))

def peraturan():
    print('''Peraturan Peminjaman Buku :
1. Peminjaman maksimal 2 (dua) buku.
2. Lama peminjaman 1 (satu) minggu dari tanggal peminjaman.
3. Setiap peminjam harus mengembalikan pinjaman buku, majalah, surat kabar dan lain-lain sesuai 
   dengan waktu yang sudah ditentukan oleh perpustakaan.
4. Peminjam wajib mendapatkan & memiliki Struk Bukti Pinjam saat akan hendak meminjam buku.
5. Saat mengembalikan buku, peminjam wajib membawa dan Struk Kertas Bukti Pinjam kepada
   pengawas perpus.
6. Perpanjangan masa peminjaman buku hanya boleh dilakukan satu kali.
7. Apabila buku-buku,majalah,surat kabar yang dipinjam rusak atau hilang harap segera melapor 
   kepada pengelola atau petugas perpustakaan.''')

    print('''Sanksi :
1. Keterlambatan pengembalian buku dikenakan sanksi denda sesuai dengan peraturan dan tata 
   tertib yang telah ditentukan, yaitu Rp. 10.000,- untuk 1 (satu) buku per hari.
2. Apabila buku yang dipinjam rusak atau hilang, maka peminjam wajib mengganti dengan buku 
   yang sama, atau membayar 3 (tiga) kali lipat dari harga buku tersebut (ditambah biaya sanksi 
   denda keterlambatan pengembalian buku bila ada).
3. Bagi pemustaka yang tidak mematuhi peraturan dan tata tertib Perpustakaan, maka di hari 
   selanjutnya tidak akan dilayani.''')
    time.sleep(1)

if __name__ == '__main__':
    while(True):
        menu()
