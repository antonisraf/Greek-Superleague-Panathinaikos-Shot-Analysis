import json
import time
import random
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

urls = [
    "https://www.sofascore.com/football/match/apo-levadiakos-panathinaikos/Yobsnbc#id:14151977",
    "https://www.sofascore.com/football/match/ae-kifisia-panathinaikos/YobszeY#id:14151961",
    "https://www.sofascore.com/football/match/panathinaikos-olympiacos-fc/VobsYob#id:14151978",
    "https://www.sofascore.com/football/match/panetolikos-panathinaikos/YobsePc#id:14151962",
    "https://www.sofascore.com/football/match/atromitos-athens-panathinaikos/Yobsmbc#id:14151988",
    "https://www.sofascore.com/football/match/aris-thessaloniki-panathinaikos/Yobscpb#id:14151991",
    "https://www.sofascore.com/football/match/asteras-aktor-panathinaikos/YobsRBc#id:14152000",
    "https://www.sofascore.com/football/match/nps-volos-panathinaikos/YobsjZgc#id:14152006",
    "https://www.sofascore.com/football/match/paok-panathinaikos/Yobsbpb#id:14152018",
    "https://www.sofascore.com/football/match/mgs-panserraikos-panathinaikos/YobsXBc#id:14152020",
    "https://www.sofascore.com/football/match/aek-athens-panathinaikos/Yobsapb#id:14152030",
    "https://www.sofascore.com/football/match/ae-larisa-panathinaikos/Yobsppb#id:14152032",
    "https://www.sofascore.com/football/match/nps-volos-panathinaikos/YobsjZgc#id:14152045",
    "https://www.sofascore.com/football/match/paok-panathinaikos/Yobsbpb#id:14152052",
    "https://www.sofascore.com/football/match/mgs-panserraikos-panathinaikos/YobsXBc#id:14159112",
    "https://www.sofascore.com/football/match/aek-athens-panathinaikos/Yobsapb#id:14159111",
    "https://www.sofascore.com/football/match/atromitos-athens-panathinaikos/Yobsmbc#id:14159125",
    "https://www.sofascore.com/football/match/ae-kifisia-panathinaikos/YobszeY#id:14159131",
    "https://www.sofascore.com/football/match/panathinaikos-olympiacos-fc/VobsYob#id:14159139",
    "https://www.sofascore.com/football/match/ae-larisa-panathinaikos/Yobsppb#id:14159147",
    "https://www.sofascore.com/football/match/panathinaikos-ofi-crete/QobsYob#id:14159157",
    "https://www.sofascore.com/football/match/aris-thessaloniki-panathinaikos/Yobscpb#id:14159161"
]

pao_players = [
    "Karol Świderski", "Anass Zaroury", "Cyriel Dessers", "Andreas Tetteh", 
    "Miloš Pantović", "Tonny Vilhena", "Pavlos Pantelidis", "Georgios Kyriopoulos", 
    "Giannis Bokos", "Renato Sanches", "Facundo Pellistri", "Anastasios Bakasetas", 
    "Adriano Jagušić", "Santino Andino", "Vicente Taborda", "Moussa Sissoko", 
    "Filip Đuričić", "Adam Gnezda Čerin", "Manolis Siopis", "Georgios Kyriakopoulos", 
    "Pedro Chirivella", "Sotiris Kontouris", "Markos Spatharis", "Ahmed Touba", 
    "Davide Calabria", "Tin Jedvaj", "Erik Palmer-Brown", "Javier Hernández", 
    "Sverrir Ingi Ingason", "Giannis Kotsiras", "Georgios Katris", "Alban Lafont"
]

options = webdriver.ChromeOptions()
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
options.set_capability("goog:loggingPrefs", {"performance": "ALL"})
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

all_pao_shots = []

try:
    for url in urls:
        print(f"\nΣκανάρισμα: {url}")
        driver.get(url)
        time.sleep(random.uniform(5, 7))

        try:
            stats_btn = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Statistics')]"))
            )
            driver.execute_script("arguments[0].click();", stats_btn)
            time.sleep(2)
        except: continue

        driver.execute_script("window.scrollTo(0, 500);")
        time.sleep(4)

        logs = [json.loads(lr["message"])["message"] for lr in driver.get_log("performance")]
        target_id = next((x["params"]["requestId"] for x in logs if 'shotmap' in x.get('params', {}).get('headers', {}).get(':path', '')), None)

        if target_id:
            try:
                response = driver.execute_cdp_cmd('Network.getResponseBody', {'requestId': target_id})
                data = json.loads(response.get('body', ''))
                raw_shots = data.get('shotmap', [])
                
                if raw_shots:
                    df = pd.DataFrame(raw_shots)
                    df['player_name'] = df['player'].apply(lambda p: p['name'] if isinstance(p, dict) else 'Unknown')
                    
                    
                    pao_only = df[df['player_name'].isin(pao_players)].copy()
                    
                    if not pao_only.empty:
                        
                        pao_only['X'] = pao_only['playerCoordinates'].apply(lambda c: c['x'])
                        pao_only['Y'] = pao_only['playerCoordinates'].apply(lambda c: c['y'])
                        
                        
                        pao_only['minute'] = pao_only.get('time', 0)
                        
                    
                        pao_only['is_goal'] = pao_only['shotType'].apply(lambda x: 1 if str(x).lower() == 'goal' else 0)
                        pao_only['xg'] = pao_only.get('xg', None)
                        pao_only['body_part'] = pao_only.get('bodyPart', None)
                        pao_only['situation'] = pao_only.get('situation', None)
                        pao_only['match_id'] = url.split('/')[-1]

                        
                        cols = ['player_name', 'minute', 'X', 'Y', 'is_goal', 'shotType', 'xg', 'body_part', 'situation', 'match_id']
                        all_pao_shots.append(pao_only[cols])
                        print(f"Βρέθηκαν {len(pao_only)} σουτ.")
            except Exception as e:
                print(f"Σφάλμα data: {e}")

        time.sleep(random.uniform(8, 12))

    if all_pao_shots:
        final_df = pd.concat(all_pao_shots, ignore_index=True)
        final_df.to_csv('pao_full_stats_with_minutes.csv', index=False)
        print("\n--- ΟΛΟΚΛΗΡΩΘΗΚΕ ---")
        print(f"Συνολικά σουτ: {len(final_df)}")
    else:
        print("Δεν βρέθηκαν δεδομένα.")

finally:
    driver.quit()