import time
from maps.maps import Maps

with Maps() as bot:
    bot.land_first_page()
    bot.search("dentist in New York State, USA")
    counter = 0
    while True:
        try:
            bot.click_card(counter)
            time.sleep(1.6)
            bot.parse_clinic()
            counter += 1
            print(counter)
        except:
            if bot.is_end():
                bot.scroll_to_end()
                time.sleep(2)
                if counter == bot.current_cards_number():
                    bot.convert_to_excel()
                    print("All clinics parsed successfully!")
                    break
                else:
                    pass
            else:
                bot.scroll_to_end()
                time.sleep(2)
                if counter == bot.current_cards_number():
                    bot.scroll_to_top()
                    time.sleep(1)
                    bot.scroll_to_end()
                    time.sleep(1)
                else:
                    pass