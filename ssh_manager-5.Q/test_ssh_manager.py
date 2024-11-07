from SSHManager import SSHManager

# Sunucu bilgileri ve kullanıcı adı/parola
hosts = ["192.168.1.10", "192.168.1.11", "192.168.1.12"]  # Sunucu IP adreslerinizi buraya yazın
username = "kullanici_adi"
password = "sifre"

# SSHManager sınıfını oluştur
manager = SSHManager(username=username, password=password)

# Tüm sunucularda komut çalıştırma
results = manager.execute_parallel(hosts, "uname -a")
for host, output in results.items():
    print(f"{host} output:\n{output}")
