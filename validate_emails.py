import dns.resolver
import smtplib
import time

def verify_email(email):
    domain = email.split('@')[1]
    try:
        records = dns.resolver.resolve(domain, 'MX')
        # Try the highest priority MX record
        mxRecord = sorted(records, key=lambda x: x.preference)[0].exchange
        mxRecord = str(mxRecord)
        
        server = smtplib.SMTP(timeout=5)
        server.set_debuglevel(0)
        server.connect(mxRecord)
        server.helo(server.local_hostname)
        server.mail('contact@tranzmitai.com')
        code, message = server.rcpt(str(email))
        server.quit()
        
        # 250 means OK, but beware of Catch-All (will return 250 for anything)
        if code == 250:
            return True
        else:
            return False
    except Exception as e:
        # If timeout or other error, assume not validated or catch-all block
        return None

def check_catch_all(domain):
    return verify_email(f"this_is_a_fake_email_to_test_catchall_12345@{domain}")

people = [
    {"name": "Nikhil J", "domain": "cult.fit"},
    {"name": "Apurva Hendi", "domain": "ultrahuman.com"},
    {"name": "Bhoopendra Kumar", "domain": "fittr.com"},
    {"name": "Akshit Kumar", "domain": "fitpass.co.in"},
    {"name": "Rohan Gupta", "domain": "healthifyme.com"},
    {"name": "Paresh Patil", "domain": "goqii.com"},
    {"name": "Madhusmita Rawooth", "domain": "dozee.io"}
]

for p in people:
    first = p['name'].split()[0].lower()
    if len(p['name'].split()) > 1:
        last = p['name'].split()[1].lower()
    else:
        last = ""
        
    domain = p['domain']
    print(f"\nChecking domain: {domain}")
    
    is_catch_all = check_catch_all(domain)
    if is_catch_all:
        print(f"[!] {domain} is configured as a Catch-All. SMTP validation won't work reliably.")
        # Proceed with most common guess
        print(f" -> Best guess: {first}@{domain} or {first}.{last}@{domain}")
        continue
    elif is_catch_all is None:
        print(f"[!] {domain} MX check failed or timed out.")
        continue
        
    print(f"Good news! {domain} is not a catch-all. Testing permutations...")
    
    permutations = [
        f"{first}@{domain}",
        f"{first}.{last}@{domain}" if last else None,
        f"{first}{last}@{domain}" if last else None,
        f"{first[0]}{last}@{domain}" if last else None,
        f"{first[0]}.{last}@{domain}" if last else None
    ]
    
    found = False
    for email in filter(None, permutations):
        if verify_email(email):
            print(f"  [VALIDATED] {email}")
            found = True
            break
        time.sleep(1) # Be polite to SMTP servers
        
    if not found:
        print(f"  Could not validate any standard permutations for {p['name']}.")
