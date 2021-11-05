import pip._vendor.requests as requests
from datetime import datetime
import time

#outputs to your logfile
def log(file, status, message):
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    file.write('[' + status + '] '+ current_time + ' ' + message + '\n')

guessed = 'was_guessed'
notguessed = 'was_not_guessed'
guess = 'should_guess'
notguess = 'should_not_guess'
checked = 'was_checked'
notchecked = 'was_not_checked'

#config variables
counter = 1000000 #initial value to start counting down from
min_counter = 1 #lowest possible number
base_url = 'https://cpt-api.twentypoo.com/numberGuesses/'
cookie = 'gibberish' #SID cookie taken from twentypoo

should_counter=0 #count of entries that can be guessed
max_should_counter = 3000 #configurable goal of entries that can be guessed

in_range_counter = 0 #after guessed entry is found, this counts for the next amount of entries that should be guessed
in_range_value = 5 #amount of entries that should be guessed after finding a guessed number

avg_guess_length = 85 #average number of characters in a single guess. Used to lazily estimate number of guesses on a number

outfile = open('results.csv', 'w')
logfile = open('logfile.txt', 'w')

numbers_dict = {}

outfile.write('NUMBER,WASGUESSED,SHOULDGUESS,WASCHECKED,NUM_GUESSES\n')

s = requests.Session()

while (counter > min_counter and should_counter < max_should_counter):
    try:
        time.sleep(2) #so cokakoala doesn't get mad at me

        print('starting on num ' + str(counter) + ', found ' + str(should_counter) + ' so far')

        #call API
        temp_url = base_url + str(counter)
        r = s.get(temp_url, cookies={'SID':cookie})

        log(logfile,'INFO',str(counter)+' was checked with response ' + str(r.status_code))

        if r.status_code == 401: #401 unauthorized, your SID probably expired
            print('401')
            break
        while r.status_code == 429: #429 timeout, you sent too many requests too soon
            print('sleeping for ' + r.headers["Retry-After"])
            time.sleep(int(r.headers["Retry-After"]))
            print('woken up')

            r = s.get(temp_url, cookies={'SID':cookie})
            log(logfile,'INFO',str(counter)+' was checked with response ' + str(r.status_code))

        #if the API returned content longer than 4 (implying that this number has been guessed before)
        if len(r.content) > 4:
            log(logfile,'INFO',str(counter) + ' was guessed')

            #calculate number of guesses already made
            num_guesses = int(len(r.content) / avg_guess_length)
            if num_guesses == 0: #if the avg_guess_length misleads, sets this should_not_guess to 1
                num_guesses = 1
            numbers_dict[counter] = (guessed,notguess,checked,num_guesses)

            #if a number has already been guessed, mark the ones that came before it (within range) as should_guess
            in_range_counter = in_range_value #refresh the count of numbers that should be added
            within_this_range = counter + in_range_value #when a number has been guessed, this value is the highest number that should also be guessed
            
            while (within_this_range > counter):
                if (within_this_range in numbers_dict.keys() and numbers_dict[within_this_range][0] == notguessed and numbers_dict[within_this_range][1] == notguess):
                    numbers_dict[within_this_range] = (numbers_dict[within_this_range][0],guess,numbers_dict[within_this_range][2],numbers_dict[within_this_range][3])
                    should_counter = should_counter + 1
                    log(logfile,'INFO',str(within_this_range) + ' should be guessed (amended)')
                within_this_range = within_this_range - 1

        else: #if the number was not guessed
            log(logfile,'INFO',str(counter) + ' was not guessed')
            should_be_guessed = ''

            #determine whether number is within the range of numbers that should be guessed
            if (in_range_counter > 0):
                should_be_guessed = guess
                should_counter = should_counter + 1
                log(logfile,'INFO',str(counter) + ' should be guessed')
            else:
                should_be_guessed = notguess
                log(logfile,'INFO',str(counter) + ' should not be guessed')

            numbers_dict[counter] = (notguessed,should_be_guessed,checked,0)
            

    except Exception as e:
        log(logfile,'ERROR',str(e.__class__) + ' ' + str(e))
        print(str(e.__class__) + ' ' + str(e))

    finally:
        counter = counter - 1
        if in_range_counter > 0:
            in_range_counter = in_range_counter - 1


for key in numbers_dict:
    outfile.write(str(key)+','+numbers_dict[key][0]+','+numbers_dict[key][1]+','+numbers_dict[key][2]+','+str(numbers_dict[key][3])+'\n')

log(logfile,'INFO','stopped running')
outfile.close()
logfile.close()