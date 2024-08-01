import os
import requests # type: ignore
import zipfile
from io import BytesIO

# 1. Adım: En son kararlı sürüm numarasını almak
version_url = "https://getwebdriver.com/chromedriver/api/LATEST_RELEASE_STABLE"
response = requests.get(version_url)

if response.status_code == 200:
    latest_version = response.text.strip()
    print("En Son Kararlı Sürüm:", latest_version)
else:
    raise Exception("En son sürüm numarasını almakta hata oluştu.")

# 2. Adım: ZIP dosyasını indirmek için URL'yi oluştur
download_url = f"https://storage.googleapis.com/chrome-for-testing-public/{latest_version}/win64/chromedriver-win64.zip"
response = requests.get(download_url)
print (download_url)
if response.status_code == 200:
    # ZIP dosyasını belleğe al
    with zipfile.ZipFile(BytesIO(response.content)) as z:
        # ZIP dosyasındaki `chromedriver-win64` klasöründeki dosyaları çıkart
        extract_to = r"C:\ChromeDriver"
        os.makedirs(extract_to, exist_ok=True)

        for file_info in z.infolist():
            # `chromedriver-win64` klasöründeki dosyaları bul
            if file_info.filename.startswith("chromedriver-win64/"):
                # Dosya yolunu güncelle ve çıkar
                extracted_path = os.path.join(extract_to, os.path.basename(file_info.filename))
                with z.open(file_info) as source, open(extracted_path, 'wb') as target:
                    target.write(source.read())
                
        print(f"Dosyalar '{extract_to}' dizinine çıkarıldı.")
else:
    raise Exception("ZIP dosyasını indirmekte hata oluştu.")
