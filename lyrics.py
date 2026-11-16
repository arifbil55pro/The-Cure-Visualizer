"""
lyrics.py - Data Lirik dan Timing untuk Vibe Coding Visualizer
Lagu: Olivia Rodrigo - The Cure (Bridge & Outro)
"""

# Konfigurasi Awal
SONG_TITLE = "The Cure"
ARTIST = "Olivia Rodrigo"
DEFAULT_START_TIME = 201.0  # 03:21 dalam detik (Awal bagian Bridge)

# Helper untuk konversi waktu "MM:SS" atau "MM:SS.ms" ke detik
def parse_time(time_str: str) -> float:
    parts = time_str.strip().split(":")
    if len(parts) == 2:
        minutes = float(parts[0])
        seconds = float(parts[1])
        return minutes * 60.0 + seconds
    return float(time_str)

# Timeline Lirik Lengkap Bridge & Outro
RAW_LYRICS = [
    # --- Bagian Bridge (Sebelum Ah-ah-ah: kurung & kurawal ORANGE, string PUTIH) ---
    {
        "time": "03:21",
        "end_time": "03:24",
        "code": 'why.cant( "you_come" ) { stitch: "me_up" };',
        "type_speed": 0.70
    },
    {
        "time": "03:24",
        "end_time": "03:27",
        "code": 'why.cant( "it_ever" ) { be: "enough" };',
        "type_speed": 0.70
    },
    {
        "time": "03:27",
        "end_time": "03:30",
        "code": 'why.cant( "you_come" ) { stitch: "me_up" };',
        "type_speed": 0.70
    },
    {
        "time": "03:30",
        "end_time": "03:35",
        "code": 'why.cant( "it_ever" ) { be: "enough" };',
        "type_speed": 0.65
    },
    # --- Index 4: Ah-ah-ah (Warna MERAH) ---
    {
        "time": "03:35",
        "end_time": "03:39",
        "code": '// Ah - ah - ah - ah...',
        "type_speed": 0.80
    },

    # --- Bagian Outro (Sesudah Ah-ah-ah: kurung & kurawal MERAH, string ORANGE) ---
    {
        "time": "03:39",
        "end_time": "03:44",
        "code": '{ its_not: "enough" };',
        "type_speed": 0.60
    },
    {
        "time": "03:45",
        "end_time": "03:49",
        "code": 'oh.because( "my_head" ) { is_full_of: "poison" }',
        "type_speed": 0.75
    },
    {
        "time": "03:49",
        "end_time": "03:53",
        "code": 'and( "my_heart" ) { is_full_of: "doubt" }',
        "type_speed": 0.75
    },
    {
        "time": "03:53",
        "end_time": "03:56.5",
        "code": 'i.got( "toxins" ) { in: "my_bloodstream" }',
        "type_speed": 0.80
    },
    {
        "time": "03:56.5",
        "end_time": "04:00",
        "code": 'you.tried_so_hard( to: "suck_out" )',
        "type_speed": 0.75
    },
    {
        "time": "04:00",
        "end_time": "04:03",
        "code": 'and( "it_feels" ) { like: "medication" }',
        "type_speed": 0.75
    },
    {
        "time": "04:03",
        "end_time": "04:06",
        "code": 'and( "its_good" ) { for_me: "im_sure" }',
        "type_speed": 0.75
    },
    {
        "time": "04:06",
        "end_time": "04:11",
        "code": 'but( "it_dont_matter" ) { how: "your_love_feels_anymore" }',
        "type_speed": 0.85
    },
    {
        "time": "04:11",
        "end_time": "04:16",
        "code": '{ itll_never_be: "the_cure" }',
        "type_speed": 0.65
    },
    {
        "time": "04:16",
        "end_time": "04:22",
        "code": '// The Cure - Olivia Rodrigo',
        "type_speed": 0.50
    }
]

# Palet Warna Syntax Highlighting
SYNTAX_COLORS = {
    # Merah Darah untuk lirik 'you', 'why', 'my_bloodstream', dan baris '// Ah - ah - ah - ah...'
    "blood_red": (230, 25, 35),

    # Hijau Tua untuk 'poison'
    "dark_green": (35, 150, 50),

    # Tanda Kurung () dan Kurawal {}
    "bracket_orange": (255, 135, 15),  # Orange sebelum ah-ah-ah..
    "bracket_red": (235, 35, 45),      # Merah sesudah ah-ah-ah..

    # String Lirik
    "string_white": (255, 255, 255),   # Putih sebelum ah-ah-ah..
    "string_orange": (255, 140, 20),   # Orange sesudah ah-ah-ah.. (menggantikan putih)
    "string": (255, 255, 255),

    # Warna Standar Syntax
    "keyword": (197, 134, 192),        # Ungu (#c586c0) - def, and, but, oh, if, return
    "function": (97, 175, 239),        # Biru (#61afef) - cant, tried_so_hard, because, got
    "property": (229, 192, 123),       # Kuning (#e5c07b) - stitch:, be:, is_full_of:, to:
    "variable": (224, 108, 117),       # Coral muda (#e06c75)
    "punctuation": (171, 178, 191),    # Abu-abu muda / putih (#abb2bf) - ;, ., :
    "comment": (106, 153, 85),         # Hijau muted (#6a9955)
    "default": (255, 255, 255),        # Putih
}

# Tokenizer otomatis
import re

TOKEN_SPECS = [
    ("comment", r'//.*|#.*'),
    ("string", r'"[^"]*"|\'[^\']*\''),
    ("property", r'\b[a-zA-Z_][a-zA-Z0-9_]*(?=\s*:)'),
    ("function", r'\b[a-zA-Z_][a-zA-Z0-9_]*(?=\s*\()'),
    ("keyword", r'\b(why|oh|and|but|i|you|def|return|if|else|in|for|while|import|from|class|try|except|with|as)\b'),
    ("bracket", r'[\(\)\{\}]'),
    ("punctuation", r'[\[\];:,\.]'),
    ("word", r'[a-zA-Z_][a-zA-Z0-9_]*'),
    ("space", r'\s+'),
    ("other", r'.'),
]

TOKEN_REGEX = re.compile('|'.join(f'(?P<{name}>{pattern})' for name, pattern in TOKEN_SPECS))

def tokenize_code(code_str: str, line_idx: int = 0):
    """
    Memecah baris kode menjadi pasangan (teks, tipe_warna):
    - Baris 'Ah - ah - ah..' -> Merah
    - 'you', 'why', 'my_bloodstream' -> Merah Darah
    - 'poison' -> Hijau Tua
    - kurung () dan kurawal {} sebelum ah ah ah.. -> Orange
    - kurung () dan kurawal {} sesudah ah ah ah.. -> Merah
    - string sebelum ah ah ah.. -> Putih
    - string sesudah ah ah ah.. -> Orange
    """
    tokens = []
    for match in TOKEN_REGEX.finditer(code_str):
        kind = match.lastgroup
        text = match.group()
        clean = text.strip('"\'')

        # 1. Baris vokal Ah - ah - ah.. -> Merah
        if "Ah" in text or "ah - ah" in text.lower():
            color_type = "blood_red"

        # 2. Merah Darah: you, why, my_bloodstream, you_come
        elif clean in ("why", "you", "my_bloodstream", "you_come"):
            color_type = "blood_red"

        # 3. Hijau Tua: poison
        elif "poison" in clean:
            color_type = "dark_green"

        # 4. Tanda Kurung () dan Kurawal {}
        elif text in ("(", ")", "{", "}"):
            if line_idx < 4:
                color_type = "bracket_orange"
            else:
                color_type = "bracket_red"

        # 5. String Lirik
        elif kind == "string":
            # Sebelum ah-ah-ah.. (line_idx < 4) -> Putih
            # Sesudah ah-ah-ah.. (line_idx > 4) -> Orange
            if line_idx < 4:
                color_type = "string_white"
            else:
                color_type = "string_orange"

        # 6. Komentar biasa
        elif kind == "comment":
            color_type = "comment"

        # 7. Property / Key
        elif kind == "property":
            color_type = "property"

        # 8. Function
        elif kind == "function":
            color_type = "function"

        # 9. Keyword
        elif kind == "keyword":
            color_type = "keyword"

        # 10. Punctuation biasa (;, ., :)
        elif kind in ("punctuation", "bracket"):
            color_type = "punctuation"

        elif kind == "word":
            color_type = "variable"
        elif kind == "space":
            color_type = "default"
        else:
            color_type = "default"

        tokens.append((text, color_type))
    return tokens

# Timeline data terstruktur beserta token warna
LYRICS_DATA = []
start_line_no = 24

for i, item in enumerate(RAW_LYRICS):
    t_start = parse_time(item["time"])
    t_end = parse_time(item["end_time"])
    item_tokens = tokenize_code(item["code"], line_idx=i)
    
    LYRICS_DATA.append({
        "line_index": i,
        "line_number": start_line_no + i,
        "start": t_start,
        "end": t_end,
        "duration": t_end - t_start,
        "code": item["code"],
        "tokens": item_tokens,
        "type_speed": item.get("type_speed", 0.75)
    })
