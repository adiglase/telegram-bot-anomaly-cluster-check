import re

medium_level_words = ['investasi', 'deposit', 'pinjaman online', 'transfer', 'pekerjaan', 'gaji', 'hadiah',
                'norek', 'nomor rekening', 'no. rek', 'http://', 'https://']
high_level_words = ['.apk', 'transaksi selesai', 'transaksi berhasil', 'udah masuk']

words = {
    'medium': medium_level_words,
    'high': high_level_words
}

file_path = 'chats/chat_hi.txt'

# Initialize word count dictionary
word_count = {word: 0 for word in medium_level_words + high_level_words}

def find_word(line, word):
    if re.search(re.escape(word), line, re.IGNORECASE):
        return True
    return False

def output_found_result(word_level, word):
    if word_level == 'medium':
        print('Found medium level word: ' + word)
    else:
        print('Found high level word: ' + word)

def is_found_word_in_line(line, words: list):
    for word in words:
        if find_word(line, word):
            return {
                'word': word,
            }
        
    return {}

def check_wa_chat_anomaly_level(file_name: str):
    is_found_medium_level = False
    is_found_high_level = False

    with open(file_name, 'r') as file:
        for line in file:
            if not is_found_medium_level and is_found_word_in_line(line, words['medium']):
                is_found_medium_level = True
            
            if not is_found_high_level and is_found_word_in_line(line, words['high']):
                is_found_high_level = True

    if is_found_high_level:
        return 'Chat terdeteksi anomaly dengan cluster High'
    elif is_found_medium_level:
        return 'Chat terdeteksi anomaly dengan cluster Medium'
    else:
        return 'Chat terdeteksi anomaly dengan cluster Basic'
