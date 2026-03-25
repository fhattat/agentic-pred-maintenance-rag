\# Alpha-V8 Endüstriyel Makine - Kapsamlı Teknik Bakım ve Arıza Teşhis Klavuzu



\## 1. SİSTEM MİMARİSİ VE SENSÖR AĞI

Alpha-V8 üniteleri, gerçek zamanlı veri akışı sağlayan 4 ana sensör ve 3 alt sinyal bileşeni (IMF - Intrinsic Mode Functions) ile donatılmıştır. 



\### 1.1. Sensör Spesifikasyonları

\* \*\*Vibration (mm/s^2):\*\* Gövde üzerindeki ivmeölçerden gelir. Mekanik dengesizliği ölçer.

\* \*\*Acoustic (dB):\*\* Rulman yataklarındaki yüksek frekanslı sürtünme seslerini takip eder.

\* \*\*Temperature (°C):\*\* Motor sargı ve yüzey sıcaklığıdır.

\* \*\*Current (Ampere):\*\* Motorun çektiği elektriksel yükü ifade eder.



\## 2. OPERASYONEL EŞİK DEĞERLERİ (KPI)



| Parametre | Normal Aralık | Uyarı (Warning) | Kritik (Critical) |

| :--- | :--- | :--- | :--- |

| Vibration | 0.60 - 0.90 | 1.10 - 1.25 | > 1.30 |

| Temperature | 60°C - 72°C | 76°C - 82°C | > 85°C |

| Current | 11.5A - 13.5A | 14.5A - 15.2A | > 15.5A |

| Acoustic | 0.50 - 0.70 | 0.85 - 0.95 | > 1.00 |



\## 3. ARIZA MODLARI VE KÖK NEDEN ANALİZİ (RCA)



\### 3.1. Tip A: Mekanik Yorgunluk ve Rulman Arızası

\* \*\*Belirtiler:\*\* Vibration > 1.25 VE Acoustic > 0.90.

\* \*\*Kök Neden:\*\* Genelde yağlama eksikliği veya eksenel kaçıklık.

\* \*\*Acil Müdahale:\*\* Makineyi durdurun, rulman yataklarını kontrol edin.



\### 3.2. Tip B: Elektriksel Aşırı Yük ve Isınma (Overload)

\* \*\*Belirtiler:\*\* Current > 15.0A VE Temperature > 80°C.

\* \*\*Kök Neden:\*\* Aşırı yük altında çalışma veya sargı kısa devresi başlangıcı.

\* \*\*Acil Müdahale:\*\* Yükü %20 azaltın, soğutma fanlarını kontrol edin.



\### 3.3. Tip C: Akustik Rezonans (Gevşek Parça)

\* \*\*Belirtiler:\*\* Sadece Acoustic değerinde ani sıçrama (> 1.10), diğer parametreler normal.

\* \*\*Kök Neden:\*\* Şasi bağlantı vidalarında gevşeme veya dış muhafaza titreşimi.



\## 4. GELİŞMİŞ ANALİZ NOTLARI (IMF ANALİZİ)

\* \*\*IMF\_1 Sinyali:\*\* Eğer IMF\_1 değeri 0.30'un üzerine çıkarsa, bu durum sensörde bir gürültü değil, yapısal bir çatlak başlangıcı olabilir.

\* \*\*Korelasyon Notu:\*\* Arıza (label: 1) durumlarında en belirgin öncü sinyal genellikle Vibration ve Current artışının eş zamanlı gerçekleşmesidir.



\## 5. BAKIM PROSEDÜRÜ

1\.  \*\*Önleyici Bakım:\*\* Her 500 saatlik çalışma sonrası sensör kalibrasyonu yapılmalıdır.

2\.  \*\*Kritik Müdahale:\*\* Herhangi bir parametre "Critical" eşiğini geçtiğinde sistem otomatik olarak "Fail-Safe" moduna alınmalıdır.

