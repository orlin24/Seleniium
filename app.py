import os
import schedule
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

# Fungsi untuk menjalankan tugas otomatisasi
def schedule_stream():
    print(f"Memulai otomatisasi pada {time.ctime()}")

    # Gunakan path temp_profile_dir yang sudah ada
    temp_profile_dir = "/var/folders/53/4_3p4mjx4db19466xx7qrgnw0000gn/T/tmp65e2cws1"
    profile_name = "Profile 5"

    # Setup Chrome options dengan profil sementara
    options = webdriver.ChromeOptions()
    options.add_argument(f"--user-data-dir={temp_profile_dir}")
    options.add_argument(f"--profile-directory={profile_name}")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)

    # Inisialisasi driver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

    try:
        # Langsung kunjungi URL YouTube Studio
        print("Mengakses YouTube Studio...")
        driver.get("https://studio.youtube.com/channel/UCWkTx313gKmgCiqJFQg8P8w")
        
        # Tunggu hingga elemen live-icon muncul dan klik
        print("Mencari live-icon...")
        live_icon = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="live-icon"]/tp-yt-iron-icon'))
        )
        live_icon.click()
        print("Live-icon berhasil diklik.")
        
        # Tunggu hingga elemen schedule-button muncul dan klik
        print("Mencari schedule-button...")
        schedule_button = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="schedule-button"]/ytcp-button-shape/button'))
        )
        schedule_button.click()
        print("Schedule-button berhasil diklik.")
        
        # Tunggu hingga elemen dropdown muncul dan klik
        print("Mencari dropdown trigger...")
        dropdown_trigger = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="dropdown-container"]//div[@id="trigger"]'))
        )
        dropdown_trigger.click()
        print("Dropdown trigger berhasil diklik.")
        
        # Tambahkan jeda untuk memastikan dropdown terbuka
        time.sleep(2)
        
        # Tunggu hingga opsi nomor 2 muncul dan klik (menggunakan indeks)
        print("Mencari opsi nomor 2 di dropdown...")
        dropdown_option_2 = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="broadcast-items"]/ytls-broadcast-menu-item-renderer[3]'))
        )
        dropdown_option_2.click()
        print("Opsi nomor 2 berhasil dipilih.")
        
        # Tunggu hingga tombol "Gunakan kembali setelan" muncul dan klik
        print("Mencari tombol 'Gunakan kembali setelan'...")
        reuse_settings_button = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, '//ytcp-button-shape/button[contains(., "Gunakan kembali setelan")]'))
        )
        reuse_settings_button.click()
        print("Tombol 'Gunakan kembali setelan' berhasil diklik.")
        
        # Tunggu hingga tombol "Berikutnya" muncul dan klik (langkah pertama)
        print("Mencari tombol 'Berikutnya' (langkah pertama)...")
        next_button = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, '//ytcp-button-shape/button[contains(., "Berikutnya")]'))
        )
        next_button.click()
        print("Tombol 'Berikutnya' (langkah pertama) berhasil diklik.")
        time.sleep(2)  # Tambahkan jeda untuk memastikan halaman berikutnya dimuat

        # Tunggu hingga tombol "Berikutnya" muncul dan klik (langkah kedua)
        print("Mencari tombol 'Berikutnya' (langkah kedua)...")
        next_button = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, '//ytcp-button-shape/button[contains(., "Berikutnya")]'))
        )
        next_button.click()
        print("Tombol 'Berikutnya' (langkah kedua) berhasil diklik.")
        time.sleep(5)  # Tambahkan jeda lebih lama untuk memastikan halaman berikutnya dimuat

        # Periksa apakah halaman sudah berpindah (mencari tombol "Selesai")
        print("Memastikan halaman terakhir dimuat...")
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, '//ytcp-button[@id="create-button"]//button[@aria-label="Selesai"]'))
        )
        print("Halaman terakhir berhasil dimuat (tombol 'Selesai' ditemukan).")

        # Tunggu hingga tombol "Selesai" muncul
        print("Mencari tombol 'Selesai'...")
        finish_button = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, '//ytcp-button[@id="create-button"]//button[@aria-label="Selesai" and contains(., "Selesai")]'))
        )
        print("Tombol 'Selesai' ditemukan di DOM.")

        # Periksa status tombol
        is_displayed = finish_button.is_displayed()
        is_enabled = finish_button.is_enabled()
        aria_disabled = finish_button.get_attribute("aria-disabled")
        print(f"Status tombol 'Selesai': displayed={is_displayed}, enabled={is_enabled}, aria-disabled={aria_disabled}")

        # Jika tombol disabled, tunggu hingga aktif
        if aria_disabled == "true" or not is_enabled:
            print("Tombol 'Selesai' dalam keadaan disabled. Menunggu hingga aktif...")
            WebDriverWait(driver, 30).until(
                lambda d: d.find_element(By.XPATH, '//ytcp-button[@id="create-button"]//button[@aria-label="Selesai"]').get_attribute("aria-disabled") == "false"
            )
            print("Tombol 'Selesai' sekarang aktif.")

        # Pastikan tombol terlihat dan dapat diklik
        driver.execute_script("arguments[0].scrollIntoView(true);", finish_button)
        time.sleep(1)  # Tambahkan jeda kecil setelah scroll

        # Tunggu hingga tombol benar-benar dapat diklik
        finish_button = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, '//ytcp-button[@id="create-button"]//button[@aria-label="Selesai" and contains(., "Selesai")]'))
        )
        print("Tombol 'Selesai' siap untuk diklik.")

        # Coba klik dengan ActionChains
        actions = ActionChains(driver)
        actions.move_to_element(finish_button).click().perform()
        print("Tombol 'Selesai' berhasil diklik menggunakan ActionChains.")

        # Jika ActionChains gagal, coba dengan JavaScript
        try:
            driver.execute_script("arguments[0].click();", finish_button)
            print("Tombol 'Selesai' juga diklik menggunakan JavaScript sebagai cadangan.")
        except Exception as js_error:
            print(f"Gagal klik dengan JavaScript: {str(js_error)}")

        # Jika semua cara gagal, coba klik biasa
        try:
            finish_button.click()
            print("Tombol 'Selesai' juga diklik menggunakan klik biasa sebagai cadangan.")
        except Exception as click_error:
            print(f"Gagal klik dengan cara biasa: {str(click_error)}")
        
        print(f"Streaming berhasil dijadwalkan pada {time.ctime()}")

    except Exception as e:
        print(f"Terjadi error: {str(e)}")
        # Tambahkan informasi tambahan untuk debugging
        print(f"URL saat error: {driver.current_url}")
        print(f"HTML halaman saat error: {driver.page_source[:500]}")  # Cetak sebagian HTML untuk analisis
        # Coba cari tombol "Selesai" untuk debugging
        try:
            finish_buttons = driver.find_elements(By.XPATH, '//ytcp-button[@id="create-button"]//button[contains(., "Selesai")]')
            print(f"Jumlah tombol dengan teks 'Selesai' yang ditemukan: {len(finish_buttons)}")
            for i, btn in enumerate(finish_buttons):
                print(f"Tombol 'Selesai' ke-{i+1}: aria-disabled={btn.get_attribute('aria-disabled')}, displayed={btn.is_displayed()}, enabled={btn.is_enabled()}")
        except Exception as debug_error:
            print(f"Gagal mencari tombol 'Selesai' untuk debugging: {str(debug_error)}")

    finally:
        driver.quit()

# Jadwalkan tugas untuk berjalan setiap hari pada waktu tertentu
# Misalnya, setiap hari pukul 11:20
schedule.every().day.at("12:03").do(schedule_stream)

# Loop untuk menjalankan scheduler
print("Scheduler dimulai. Menunggu waktu yang dijadwalkan...")
while True:
    schedule.run_pending()
    time.sleep(60)  # Cek setiap menit
