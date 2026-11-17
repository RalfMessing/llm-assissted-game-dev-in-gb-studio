#!/usr/bin/env python3
"""Erzeugt alle Assets + .gbsres-Dateien fuer das GB-Studio-4.3.2-Grundspiel."""
import hashlib, json, os, uuid
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NS = uuid.UUID("6f1c2a54-9d0e-4b8a-9a77-2f3c1d5e8b10")
def uid(name): return str(uuid.uuid5(NS, name))

BG = [(0xE0,0xF8,0xCF),(0x86,0xC0,0x6C),(0x30,0x68,0x50),(0x07,0x18,0x21)]
SPR = {'.':(0x65,0xFF,0x00),'w':(0xE0,0xF8,0xCF),'l':(0x86,0xC0,0x6C),'k':(0x07,0x18,0x21)}
SOLID = 0x0F

def wjson(rel, obj):
    p = os.path.join(ROOT, rel); os.makedirs(os.path.dirname(p), exist_ok=True)
    txt = json.dumps(obj, indent=2, ensure_ascii=False)
    txt = "".join(f"\\u{ord(ch):04x}" if 0x80 <= ord(ch) <= 0x9F else ch for ch in txt)  # A6: Icon-Zeichen sichtbar escapen
    with open(p, "w", encoding="utf-8") as f: f.write(txt)

def sha1(p): return hashlib.sha1(open(p,"rb").read()).hexdigest()

def compress(arr):  # identisch zu compress8bitNumberArray (GB Studio 4)
    out, last, cnt = "", -1, 0
    for v in arr:
        if v != last:
            if cnt == 1: out += "!"
            elif cnt > 0: out += f"{cnt:x}+"
            cnt, last = 0, v
            out += f"{v % 256:02x}"
        cnt += 1
    if cnt == 1: out += "!"
    elif cnt > 0: out += f"{cnt:x}+"
    return out

# ---------------------------------------------------------------- Tiles (8x8)
def T(rows):
    rows = [r for r in rows.split()]
    assert len(rows) == 8 and all(len(r) == 8 for r in rows), rows
    return [[int(c) for c in r] for r in rows]

TILES = {
 "grass": T("11111111 11121111 11111111 11111121 12111111 11111111 11112111 11111111"),
 "flower":T("11111111 11011111 10301111 11011111 11111121 11111111 12111111 11111111"),
 "path":  T("00000000 00000100 00000000 01000000 00000000 00000010 00100000 00000000"),
 "sky":   T("00000000 00000000 00000000 00000000 00000000 00000000 00000000 00000000"),
 "fence": T("11311111 13031111 33033333 00000000 33033333 13031111 13031111 12321111"),
 "roof":  T("33333333 22232222 22232222 33333333 22222223 22222223 33333333 22232222"),
 "eave":  T("22232222 22232222 33333333 22222223 22222223 33333333 33333333 22222222"),
 "wall":  T("00000000 00000000 00000000 11111111 00000000 00000000 00000000 11111111"),
 "window":T("00000000 03333330 03222230 03333330 03222230 03333330 00000000 11111111"),
 "door":  T("00333300 03222230 03222230 03222230 03222330 03222230 03222230 03222230"),
}
TREE16 = """
1111133333311111
1113322222233111
1132211222222311
1322112222222231
1321122222222231
3221222222222223
3222222222222223
3222222222221223
3222222222212223
1322222222122231
1332222222222331
1113332222333111
1111113333111111
1111113223111111
1111113223111111
1111133333311111""".split()
for i,(ox,oy) in enumerate([(0,0),(8,0),(0,8),(8,8)]):
    TILES[["tree_tl","tree_tr","tree_bl","tree_br"][i]] = [[int(TREE16[oy+y][ox+x]) for x in range(8)] for y in range(8)]
def bordered(t, left=False, right=False):
    t = [r[:] for r in t]
    for r in t:
        if left: r[0] = 3
        if right: r[7] = 3
    return t
# A4: Innenraum-Tiles + begehbare Haustuer
TILES["entry"]  = [r[:] for r in TILES["door"]]          # gleiches Bild wie "door", aber BEGEHBAR (A4-Tuerfeld)
TILES["dark"]   = T("33333333 33333333 33333333 33333333 33333333 33333333 33333333 33333333")
TILES["floor"]  = T("11112111 11112111 11112111 22222222 21111111 21111111 21111111 22222222")
TILES["iwall"]  = T("00000000 01000100 00000000 00010001 00000000 01000100 00000000 00010001")
TILES["iwall_b"]= T("00000000 00000000 00000000 00000000 33333333 22222222 22222222 33333333")
TILES["mat"]    = T("11111111 13333331 13232321 13323231 13232321 13323231 13333331 11111111")
TABLE16 = """
1111111111111111 1333333333333331 3222222222222223 3200000000000023
3200000000000023 3200000000000023 3200000000000023 3200000000000023
3200000000000023 3222222222222223 3333333333333333 1322311111132231
1322311111132231 1322311111132231 1333311111133331 1111111111111111""".split()
BED16 = """
3333333333333333 3000000000000003 3022222002222203 3022222002222203
3000000000000003 3333333333333333 3111111111111113 3121212121212123
3111111111111113 3121212121212123 3111111111111113 3121212121212123
3111111111111113 3121212121212123 3111111111111113 3121212121212123
3111111111111113 3121212121212123 3111111111111113 3121212121212123
3111111111111113 3333333333333333 1322311111132231 1333311111133331""".split()
assert len(TABLE16) == 16 and len(BED16) == 24 and all(len(r) == 16 for r in TABLE16 + BED16)
for ty in range(2):
    for tx in range(2): TILES[f"table_{tx}{ty}"] = [[int(TABLE16[ty*8+y][tx*8+x]) for x in range(8)] for y in range(8)]
for ty in range(3):
    for tx in range(2): TILES[f"bed_{tx}{ty}"] = [[int(BED16[ty*8+y][tx*8+x]) for x in range(8)] for y in range(8)]
# A5: offene Tueroeffnung (dunkel, BEGEHBAR). Die geschlossene Tuer ist ein Actor (Sprite "door") darueber.
TILES["doorway_l"] = T("00333333 03333333 03333333 03333333 03333333 03333333 03333333 03333333")
TILES["doorway_r"] = T("33333300 33333330 33333330 33333330 33333330 33333330 33333330 33333330")
TILES["crate"]     = T("33333333 32222223 32322323 32233223 32233223 32322323 32222223 33333333")
TILES["wall_l"] = bordered(TILES["wall"], left=True)
TILES["wall_r"] = bordered(TILES["wall"], right=True)
TILES["roof_l"] = bordered(TILES["roof"], left=True)
TILES["roof_r"] = bordered(TILES["roof"], right=True)
TILES["eave_l"] = bordered(TILES["eave"], left=True)
TILES["eave_r"] = bordered(TILES["eave"], right=True)
SOLID_TILES = {"fence","roof","eave","wall","window","door","wall_l","wall_r","roof_l","roof_r","eave_l","eave_r",
               "tree_tl","tree_tr","tree_bl","tree_br",
               # A4 Innenraum: Waende + Moebel massiv; "entry", "floor", "mat" sind begehbar
               "dark","iwall","iwall_b","table_00","table_10","table_01","table_11",
               "bed_00","bed_10","bed_01","bed_11","bed_02","bed_12",
               "crate"}                                    # A5: Kisten in der Werkstatt massiv; doorway_* begehbar

class Map:
    def __init__(s, w=20, h=18, base="grass"):
        s.w, s.h = w, h; s.t = [[base]*w for _ in range(h)]
    def set(s, x, y, name):
        if 0 <= x < s.w and 0 <= y < s.h: s.t[y][x] = name
    def tree(s, x, y):
        for dx,dy,n in [(0,0,"tree_tl"),(1,0,"tree_tr"),(0,1,"tree_bl"),(1,1,"tree_br")]: s.set(x+dx,y+dy,n)
    def house(s, x, y):  # 4x4: Dach, Traufe, Fenster-Wand, Tuer-Wand
        s.set(x,y,"roof_l");  s.set(x+1,y,"roof");  s.set(x+2,y,"roof");  s.set(x+3,y,"roof_r")
        s.set(x,y+1,"eave_l");s.set(x+1,y+1,"eave");s.set(x+2,y+1,"eave");s.set(x+3,y+1,"eave_r")
        s.set(x,y+2,"wall_l");s.set(x+1,y+2,"window");s.set(x+2,y+2,"window");s.set(x+3,y+2,"wall_r")
        s.set(x,y+3,"wall_l");s.set(x+1,y+3,"door");s.set(x+2,y+3,"wall");s.set(x+3,y+3,"wall_r")
    def image(s):
        im = Image.new("RGB", (s.w*8, s.h*8))
        px = im.load()
        for ty in range(s.h):
            for tx in range(s.w):
                tile = TILES[s.t[ty][tx]]
                for y in range(8):
                    for x in range(8): px[tx*8+x, ty*8+y] = BG[tile[y][x]]
        return im
    def collisions(s):
        return [SOLID if s.t[y][x] in SOLID_TILES else 0 for y in range(s.h) for x in range(s.w)]

def unique_tiles(im):
    w,h = im.size; seen=set()
    for ty in range(0,h,8):
        for tx in range(0,w,8): seen.add(im.crop((tx,ty,tx+8,ty+8)).tobytes())
    return len(seen)

# ---------------------------------------------------------------- Wald
forest = Map()
for x in range(0,20,2): forest.tree(x,0); forest.tree(x,16)
for y in range(2,16,2):
    forest.tree(0,y)
    if y != 8: forest.tree(18,y)          # Ausgang rechts (Zeilen 8-9)
for (x,y) in [(5,3),(9,4),(13,3),(15,5),(4,12),(8,11),(12,13),(15,11)]: forest.tree(x,y)
for x in range(2,20):
    forest.set(x,8,"path"); forest.set(x,9,"path")
for (x,y) in [(3,4),(11,2),(7,14),(14,9-2),(10,10),(16,14),(3,14),(11,6)]:
    if forest.t[y][x] == "grass": forest.set(x,y,"flower")

# ---------------------------------------------------------------- Dorf
village = Map()
for x in range(0,20,2): village.tree(x,0); village.tree(x,16)
for y in range(2,16,2):
    village.tree(18,y)
    if y != 8: village.tree(0,y)          # Eingang links (Zeilen 8-9)
village.house(3,2); village.house(11,2); village.house(13,11)
for x in range(0,14):
    village.set(x,8,"path"); village.set(x,9,"path")
for y in range(6,8): village.set(4,y,"path"); village.set(12,y,"path")
for y in range(10,12): 
    for x in range(8,13): village.set(x,y,"path")   # Dorfplatz
for x in range(2,9): village.set(x,13,"fence")
# A4: Haus 1 (links oben) wird betretbar. Doppeltuer (4..5, 5) = Tuerfeld/Trigger, begehbar.
#     Doppelt breit, weil der Spieler 16 px (2 Tiles) breit ist und sonst nicht hineinpasst.
HOUSE_DOOR_X, HOUSE_DOOR_Y = 4, 5
village.set(HOUSE_DOOR_X, HOUSE_DOOR_Y, "entry"); village.set(HOUSE_DOOR_X+1, HOUSE_DOOR_Y, "entry")
for y in range(6,8): village.set(HOUSE_DOOR_X+1, y, "path")

# ---------------------------------------------------------------- A4: Hausinneres (neue Szene)
house = Map(base="floor")
for x in range(20): house.set(x,0,"dark"); house.set(x,17,"dark")       # Rahmen oben/unten
for y in range(18): house.set(0,y,"dark"); house.set(19,y,"dark")       # Rahmen links/rechts
for x in range(1,19):
    house.set(x,1,"iwall"); house.set(x,2,"iwall"); house.set(x,3,"iwall_b")   # Rueckwand (massiv)
house.set(4,2,"window"); house.set(14,2,"window")
for ty in range(2):                                                      # Tisch 2x2 bei (5..6, 9..10)
    for tx in range(2): house.set(5+tx, 9+ty, f"table_{tx}{ty}")
for ty in range(3):                                                      # Bett 2x3 an der Rueckwand (15..16, 4..6)
    for tx in range(2): house.set(15+tx, 4+ty, f"bed_{tx}{ty}")
EXIT_X, EXIT_Y = 9, 17                                                   # Rueckkehrobjekt: Fussmatte im Tuerausschnitt
house.set(EXIT_X, EXIT_Y, "mat"); house.set(EXIT_X+1, EXIT_Y, "mat")
HOUSE_SPAWN = (9, 15, "up")                  # A4.3: Ankunft im Haus, 1 Reihe Abstand zur Fussmatte
VILLAGE_SPAWN_FROM_HOUSE = (4, 7, "down")    # A4.4: Ankunft vor dem Haus, 1 Reihe Abstand zur Tuer
# ---------------------------------------------------------------- A5: Tueren als Oeffnung + Werkstatt
# Haus 1 (A4) und Haus 2 (A5) zeigen im Hintergrund eine OFFENE, begehbare Tueroeffnung.
# Verschlossen = Tuer-Actor (Sprite "door", ohne Kollisionsgruppe -> blockiert den Spieler) steht darauf.
# Geoeffnet    = Tuer-Actor deaktiviert -> Oeffnung sichtbar, Trigger darunter erreichbar.
village.set(HOUSE_DOOR_X, HOUSE_DOOR_Y, "doorway_l"); village.set(HOUSE_DOOR_X+1, HOUSE_DOOR_Y, "doorway_r")
WS_DOOR_X, WS_DOOR_Y = 12, 5                 # A5: Werkstatt-Tuer = Haus 2 (rechts oben), 2 Tiles breit
village.set(WS_DOOR_X, WS_DOOR_Y, "doorway_l"); village.set(WS_DOOR_X+1, WS_DOOR_Y, "doorway_r")
for y in range(6,8): village.set(WS_DOOR_X+1, y, "path")
SWITCH_X, SWITCH_Y = 15, 7                   # A5: Schalter rechts neben der Werkstatt, belegt (15..16, 6..7)
VILLAGE_SPAWN_FROM_WS = (12, 7, "down")      # A5.6: Ankunft vor der Werkstatt, 1 Reihe Abstand zur Tuer
KEY_X, KEY_Y = 12, 6                         # A5R: Schluessel im Wald (Kollisionsbox (12..13, 6))
# A6: neue Sammel-Gegenstaende (Actor-Tile = untere linke Ecke, Kollisionsbox (x..x+1, y))
MUSHROOM_POS = [("forest", 3, 11), ("village", 5, 15)]   # A6.1: Typ "Pilz", 2 Stueck (in zwei Szenen)
APPLE_POS    = [("house", 12, 12)]                       # A6.1: Typ "Apfel", 1 Stueck (Hausinneres, A4)
GEM_POS      = [("workshop", 16, 10)]                    # A6.1: Typ "Kristall", 1 Stueck (Werkstatt, A5)

workshop = Map(base="floor")                 # A5.6: Zielszene "Workshop" (Werkstatt-Inneres)
for x in range(20): workshop.set(x,0,"dark"); workshop.set(x,17,"dark")
for y in range(18): workshop.set(0,y,"dark"); workshop.set(19,y,"dark")
for x in range(1,19):
    workshop.set(x,1,"iwall"); workshop.set(x,2,"iwall"); workshop.set(x,3,"iwall_b")
workshop.set(9,2,"window"); workshop.set(10,2,"window")
for ty in range(2):                                       # zwei Werkbaenke (Tisch-Tiles)
    for tx in range(2): workshop.set(4+tx, 7+ty, f"table_{tx}{ty}"); workshop.set(13+tx, 7+ty, f"table_{tx}{ty}")
for (x,y) in [(2,4),(3,4),(2,5),(16,4),(17,4),(17,5),(2,12),(2,13),(3,13),(17,13)]:
    workshop.set(x,y,"crate")
WS_EXIT_X, WS_EXIT_Y = 9, 17                              # Rueckweg: Fussmatte unten
workshop.set(WS_EXIT_X, WS_EXIT_Y, "mat"); workshop.set(WS_EXIT_X+1, WS_EXIT_Y, "mat")
WS_SPAWN = (9, 15, "up")                                  # A5.6: Ankunft, 1 Reihe Abstand zur Matte
for (x,y) in [(2,14),(4,15),(6,14),(8,15),(3,15),(7,15),(16,8),(15,9),(9,3),(10,6)]:
    if village.t[y][x] == "grass": village.set(x,y,"flower")

# ---------------------------------------------------------------- Titelbild
FONT = {
 'W':"10001 10001 10001 10101 10101 11011 10001", 'A':"01110 10001 10001 11111 10001 10001 10001",
 'L':"10000 10000 10000 10000 10000 10000 11111", 'D':"11110 10001 10001 10001 10001 10001 11110",
 'O':"01110 10001 10001 10001 10001 10001 01110", 'R':"11110 10001 10001 11110 10100 10010 10001",
 'F':"11111 10000 10000 11110 10000 10000 10000", 'B':"11110 10001 10001 11110 10001 10001 11110",
 'E':"11111 10000 10000 11110 10000 10000 11111", 'N':"10001 11001 10101 10011 10001 10001 10001",
 'T':"11111 00100 00100 00100 00100 00100 00100", 'U':"10001 10001 10001 10001 10001 10001 01110",
}
title = Map(base="sky")
for x in range(20):
    for y in range(10,18): title.set(x,y,"grass")
for x in [0,2,4,6,12,14,16,18]: title.tree(x,10)
title.house(8,8)
title_im = title.image(); px = title_im.load()
def draw_text(txt, x0, y0, scale, pitch, shadow):
    for i,ch in enumerate(txt):
        rows = FONT[ch].split()
        for gy,row in enumerate(rows):
            for gx,c in enumerate(row):
                if c != "1": continue
                for sy in range(scale):
                    for sx in range(scale):
                        X = x0+i*pitch+gx*scale+sx; Y = y0+gy*scale+sy
                        if shadow: px[X+1,Y+1] = BG[2]
                        px[X,Y] = BG[3]
for i in range(2): pass
draw_text("WALDDORF", 16, 14, 2, 16, True)
draw_text("ABENTEUER", 44, 40, 1, 8, False)

# ---------------------------------------------------------------- Sprites
def sprite_img(frames, path):
    w = 16*len(frames); im = Image.new("RGB",(w,16)); p = im.load()
    for i,fr in enumerate(frames):
        rows = fr.split(); assert len(rows)==16 and all(len(r)==16 for r in rows), (path, i, [len(r) for r in rows])
        for y,r in enumerate(rows):
            for x,c in enumerate(r): p[i*16+x,y] = SPR[c]
    im.save(path); return im

def count_slices(im):
    s=set()
    for x in range(0, im.size[0], 8): s.add(im.crop((x,0,x+8,16)).tobytes())
    return len(s)

H_TOP = """................ .....kkkkkk..... ....kllllllk.... ...kllllllllk..."""
HERO_DOWN = H_TOP + """
...kllkkkkllk... ...klkwwwwklk... ...kkwkwwkwkk... ....kwkwwkwk.... ....kwwwwwwk....
...kkkwwwwkkk... ..kwkllllllkwk.. ..kwkllllllkwk.. ...kkllkkllkk... ....kllllllk...."""
HERO_UP = H_TOP + """
...kllllllllk... ...kllllllllk... ...kllllllllk... ....kllllllk.... ....kkllllkk....
...kkkkkkkkkk... ..kwkllllllkwk.. ..kwkllllllkwk.. ...kkllllllkk... ....kllllllk...."""
HERO_RIGHT = H_TOP + """
...kllllkkkkk... ...klllkwwwwk... ...klllkwwkwk... ....kllkwwkwk... ....kkwwwwwwk...
....kkkkkkkk.... ....kllwwllk.... ....kllwwllk.... ....kkllllkk.... ....kllllllk...."""
LEGS_IDLE = " ....kkk..kkk.... ....kkk..kkk...."
LEGS_STEP = " ....kkk..kkk.... .........kkk...."
LEGS_SIDE_IDLE = " ......kkkk...... ......kkkk......"
hero_frames = [HERO_DOWN+LEGS_IDLE, HERO_DOWN+LEGS_STEP, HERO_UP+LEGS_IDLE, HERO_UP+LEGS_STEP,
               HERO_RIGHT+LEGS_SIDE_IDLE, HERO_RIGHT+LEGS_IDLE]

ELDER_DOWN = """................ ......kkkk...... .....kkkkkk..... ...kkkkkkkkkk... ....kwwwwwwk....
....kwkwwkwk.... ....kwwwwwwk.... ....kwwwwwwk.... ...kkwwwwwwkk... ..kllkwwwwkllk..
..kllllwwllllk.. ..kwkllllllkwk.. ...kllllllllk... ...kllllllllk... ....kkkkkkkk.... ....kk....kk...."""
ELDER_UP = """................ ......kkkk...... .....kkkkkk..... ...kkkkkkkkkk... ....kwwwwwwk....
....kwwwwwwk.... ....kwwwwwwk.... ....kwwwwwwk.... ...kkkwwwwkkk... ..kllllllllllk..
..kllllllllllk.. ..kwkllllllkwk.. ...kllllllllk... ...kllllllllk... ....kkkkkkkk.... ....kk....kk...."""
ELDER_RIGHT = """................ .......kkkk..... ......kkkkkk.... ....kkkkkkkkkk.. .....kwwwwwwk...
.....kwwwwkwk... .....kwwwwwwwk.. .....kwwwwwwk... .....kwwwwwwwk.. ....kllkwwwwk...
....klllkwwk.... ....kllllkk..... ....kllwllk..... ....klllllk..... .....kkkkkk..... .....kk..kk....."""
SIGN = """................ ................ .kkkkkkkkkkkkkk. .kwwwwwwwwwwwwk. .kwkkkwkkwkkkwk.
.kwwwwwwwwwwwwk. .kwkkwkkkwkkwwk. .kwwwwwwwwwwwwk. .kkkkkkkkkkkkkk. ......kllk......
......kllk...... ......kllk...... ......kllk...... ......kllk...... ....kkkllkkk.... ....kkkkkkkk...."""

# A1 Schatztruhe: Frame 0 = geschlossen, Frame 1 = geoeffnet
CHEST_CLOSED = """................ ................ ................ ................ ...kkkkkkkkkk...
..kllllllllllk.. .kllwllllllwllk. .kllllllllllllk. .kllllllllllllk. .kkkkkkkkkkkkkk.
.klllkkwwkklllk. .kllwkwkkwkwllk. .klllkkwwkklllk. .kllwllkkllwllk. .kllllllllllllk. .kkkkkkkkkkkkkk."""
CHEST_OPEN = """................ ..kkkkkkkkkkkk.. .kllllllllllllk. .kllwllllllwllk. .kllllllllllllk.
.kkkkkkkkkkkkkk. .kkkkkkkkkkkkkk. .kwkwwkwkwwkwkk. .kkwwkwwwkwwkwk. .kkkkkkkkkkkkkk.
.klllkkkkkklllk. .kllwlkwwklwllk. .kllllkkkkllllk. .kllwllllllwllk. .kllllllllllllk. .kkkkkkkkkkkkkk."""

# A2 Waechter: 1 Frame, Blick nach unten, Helm + Speer. Sprite-Typ "fixed" -> zeigt IMMER dieses Bild,
#    egal welche Richtung der Actor intern hat (A2.2 / A2.7).
GUARD = """..............k. .....kkkkkk..kwk ....kllllllk..k. ...kllllllllk.k. ...kkkkkkkkkk.k.
....kwkwwkwk..k. ....kwwwwwwk..k. ....kwwkkwwk..k. ...kkkwwwwkkk.k. ..kllllkkllllkk.
..klkllkkllklkk. ..kwkllllllkwkk. ...kkkkkkkkkk.k. ....kllllllk..k. ....kkk..kkk..k. ....kkk..kkk..k."""

# A3 Muenze: 1 Frame, liegt "auf dem Boden" (untere Haelfte des 16x16-Rasters)
COIN = """................ ................ ................ ................ .......kk....... .....kkkkkk.....
....kwwwlllk.... ...kwwwkwlllk... ...kwwlkwlllk... ..kkwllkwlllkk.. ..kklllkwlllkk.. ...klllkwlllk...
...klllkwlllk... ....kllllllk.... .....kkkkkk..... .......kk......."""

# A5 Schalter (Hebel): Zustand "" = AUS (Hebel links), Zustand "On" = AN (Hebel rechts, gespiegelt)
SWITCH_OFF = """................ ................ ..kk............ .kwwk........... .kwwk........... ..kkk...........
....kk.......... .....kk......... ......kk........ .......kk....... .......kk....... ...kkkkkkkkkk...
..kllllllllllk.. ..klkkllllkklk.. ..kllllllllllk.. ..kkkkkkkkkkkk.."""
SWITCH_ON = " ".join(r[::-1] for r in SWITCH_OFF.split())
# A5 Tuer (geschlossen): nur untere 16x8 px = genau die zwei Tuer-Tiles; obere Haelfte transparent
DOOR = """................ ................ ................ ................ ................ ................
................ ................ kkkkkkkkkkkkkkkk kllllllkkllllllk kllwwllkkllwwllk kllllllkkllllllk
klllllwkkwlllllk kllwwllkkllwwllk kllllllkkllllllk kkkkkkkkkkkkkkkk"""
# A5R Schluessel: liegt "auf dem Boden" (untere Haelfte), wie die Muenze
KEY = """................ ................ ................ ................ ................ ................
................ ................ ................ ..kkkk.......... .kwllwk......... .kl..lkkkkkkkkk.
.kl..llllllllllk .kwllwkkkkklklk. ..kkkk.....kkkk. ................"""

# A6 Pilz / Apfel / Kristall: liegen "auf dem Boden" (Kollisionsbox untere 16x8 px), wie Muenze und Schluessel
MUSHROOM = """................ ................ ................ ................ ................ .....kkkkkk.....
...kkwwllwwkk... ..kwwllllllwwk.. .kllwwllllwwllk. .kllwwllllwwllk. .kkkkkkkkkkkkkk. .....kwwwwk.....
.....kwwkwk..... .....kwwwwk..... ......kkkk...... ................"""
APPLE = """................ ................ ................ ................ ........k....... .......k.kkk....
.......kkllk.... .....kkkkkk..... ....kllllllk.... ...kllwlllllk... ...klwllllllk... ...kllllllllk...
...kllllllllk... ....kllllllk.... .....kkkkkk..... ................"""
GEM = """................ ................ ................ ................ ................ ....kkkkkkkk....
...kwwlwwlllk... ..kwwlwwlllllk.. .kkkkkkkkkkkkkk. ..kwwlwllllllk.. ...kwlwlllllk... ....kwwllllk....
.....kwlllk..... ......kllk...... .......kk....... ................"""
# A6 Inventar-Icons (8x8) als Zeichen der Standardschrift "GBS Mono" ('#' = Tinte, '.' = Hintergrund).
# Sie ersetzen nur Felder, die in der Schrift LEER (Schachbrett) sind: 0x81, 0x8D, 0x8F, 0x90, 0x9D.
ICON_GLYPHS = {
 0x81: "..####.. .#....#. #.####.# #.#..#.# #.#..#.# #.####.# .#....#. ..####..",   # Muenze
 0x8D: "........ .###.... #...#### #...#.## #...#.#. .###.... ........ ........",   # Schluessel
 0x8F: "..####.. .##..##. #.####.# ######## ..#..#.. ..#..#.. ..####.. ........",   # Pilz
 0x90: "....#... ...#.... .##.##.. #.#####. #.#####. #######. .#####.. ..#.#...",   # Apfel
 0x9D: "........ .######. #.#..#.# ######## .#....#. ..#..#.. ...##... ........",   # Kristall
}
ICON = {k: chr(c) for k, c in [("coin", 0x81), ("key", 0x8D), ("mushroom", 0x8F), ("apple", 0x90), ("gem", 0x9D)]}

def patch_font_icons():
    """A6.4: Icons in die Standardschrift schreiben (idempotent). Index 0 = Tinte, 3 = Hintergrund."""
    path = f"{ROOT}/assets/fonts/gbs-mono.png"
    im = Image.open(path); assert im.mode == "P" and im.size == (128, 112)
    px = im.load()
    for code, rows in ICON_GLYPHS.items():
        rows = rows.split(); assert len(rows) == 8 and all(len(r) == 8 for r in rows), hex(code)
        i = code - 32; cx, cy = (i % 16) * 8, (i // 16) * 8
        for y in range(8):
            for x in range(8): px[cx+x, cy+y] = 0 if rows[y][x] == "#" else 3
    im.save(path)

# ---------------------------------------------------------------- A7: Gegner "Slime"
# 2 Frames (wabert dauerhaft, Sprite-Typ "fixed"), Kollisionsbox = untere 16x8 px wie beim Spieler.
SLIME_0 = """................ ................ ................ ................ ................ ................
......kkkk...... ....kkllllkk.... ...kllllllllk... ..kllwkllwkllk.. ..kllwkllwkllk.. .kllllllllllllk.
.kllllkkkkllllk. .kllllllllllllk. ..kkkkkkkkkkkk.. ................"""
SLIME_1 = """................ ................ ................ ................ ................ ................
................ .....kkkkkk..... ..kkllllllllkk.. .kllwwkllkwwllk. .kllwkkllkkwllk. kllllllllllllllk
kllllkkkkkkllllk kllllllllllllllk .kkkkkkkkkkkkkk. ................"""
SPRITE_SLIME = uid("sprite/slime")
ENEMY_START = (8, 14)          # A7.1/A7.2: Patrouillenstart im Wald (Kollisionsbox (8..9, 14))
ENEMY_RADIUS = 2               # A7.3/A7.4: Erkennungsradius (Chebyshev, Tiles)
ENEMY_SPEED = 0.5              # A7.6: Spieler = 1 px/Frame, Gegner = 0,5 px/Frame
ENEMY_CATCH_TEXT = ["Der Schleim hat\ndich erwischt!", "Zur\u00fcck zum\nTitelbildschirm."]
# A7: globale Variablen (Zustand + Rechenwerte des Gegners)
A7_VARS = [("18","EnemyX"),("19","EnemyY"),("20","EnemyPlayerX"),("21","EnemyPlayerY"),
           ("22","EnemyDX"),("23","EnemyDY"),("24","EnemyADX"),("25","EnemyADY"),("26","EnemyDist"),
           ("27","EnemyChasing"),("28","EnemyPatrolDir"),("29","EnemyPatrolSteps"),("30","EnemyBlocked"),
           ("31","EnemyMoved"),("32","EnemyNewX"),("33","EnemyNewY"),("34","EnemyStepX"),("35","EnemyStepY")]
EV = {n: i for i, n in A7_VARS}

def tile(name, sliceX, x):
    return {"id": uid(name), "x": x, "y": 0, "sliceX": sliceX, "sliceY": 0, "flipX": False, "flipY": False,
            "palette": 0, "paletteIndex": 0, "objPalette": "OBP0", "priority": False}
def frame(key, sx):
    return {"id": uid(key), "tiles": [tile(key+"/l", sx, 0), tile(key+"/r", sx+8, 8)]}
def anim(key, slices):
    return {"id": uid(key), "frames": [frame(f"{key}/f{i}", s) for i,s in enumerate(slices)]}
def empty_anim(key):
    return {"id": uid(key), "frames": [{"id": uid(key+"/f0"), "tiles": []}]}

def sprite_res(key, name, fname, anim_type, flip_left, anim_slices, im, bounds):
    anims = []
    for i in range(8):
        sl = anim_slices[i] if i < len(anim_slices) else None
        anims.append(anim(f"{key}/a{i}", sl) if sl else empty_anim(f"{key}/a{i}"))
    bx,by,bw,bh = bounds
    return {"_resourceType":"sprite","id":uid(key),"name":name,"symbol":f"sprite_{name}",
            "states":[{"id":uid(key+"/state"),"name":"","animationType":anim_type,"flipLeft":flip_left,"animations":anims}],
            "numTiles":count_slices(im),"canvasOriginX":0,"canvasOriginY":0,"canvasWidth":16,"canvasHeight":16,
            "boundsX":bx,"boundsY":by,"boundsWidth":bw,"boundsHeight":bh,"animSpeed":15,
            "filename":fname,"width":im.size[0],"height":im.size[1],
            "checksum":sha1(os.path.join(ROOT,"assets/sprites",fname))}

SPRITE_HERO, SPRITE_ELDER, SPRITE_SIGN = uid("sprite/hero"), uid("sprite/elder"), uid("sprite/sign")
SPRITE_CHEST = uid("sprite/chest")
SPRITE_GUARD = uid("sprite/guard")         # A2
SPRITE_COIN = uid("sprite/coin")           # A3
SPRITE_SWITCH, SPRITE_DOOR, SPRITE_KEY = uid("sprite/switch"), uid("sprite/door"), uid("sprite/key")   # A5
SPRITE_MUSHROOM, SPRITE_APPLE, SPRITE_GEM = uid("sprite/mushroom"), uid("sprite/apple"), uid("sprite/gem")   # A6
SWITCH_STATE_ON = "On"                     # A5: Animations-Zustand "Schalter an" ("" = aus)
CHEST_STATE_OPEN = "Open"                  # A1: Animations-Zustand der geoeffneten Truhe ("" = geschlossen)

def build_assets():
    # Hintergruende
    bgs = {"title_screen": title_im, "forest": forest.image(), "village": village.image(),
           "house": house.image(),                                        # A4
           "workshop": workshop.image()}                                  # A5
    for name, im in bgs.items():
        n = unique_tiles(im); assert n <= 192, (name, n)
        print(f"BG {name}: {n} unique tiles")
        im.save(f"{ROOT}/assets/backgrounds/{name}.png")
        wjson(f"assets/backgrounds/{name}.png.gbsres", {"_resourceType":"background","id":uid("bg/"+name),
              "name":name,"symbol":f"bg_{name}","tileColors":"","filename":f"{name}.png","width":20,"height":18,
              "imageWidth":160,"imageHeight":144,"autoColor":False})
    # Wiederverwendbare Basis-Tiles (Tileset)
    names = ["grass","flower","path","sky","fence","tree_tl","tree_tr","tree_bl","tree_br",
             "roof_l","roof","roof_r","eave_l","eave","eave_r","wall_l","window","door","wall","wall_r"]
    ts = Map(w=len(names), h=1); ts.t = [names]
    ts.image().save(f"{ROOT}/assets/tilesets/basic_tiles.png")
    wjson("assets/tilesets/basic_tiles.png.gbsres", {"_resourceType":"tileset","id":uid("tileset/basic"),
          "name":"basic_tiles","symbol":"tileset_basic_tiles",
          "width":len(names),"height":1,"imageWidth":len(names)*8,"imageHeight":8,"filename":"basic_tiles.png"})
    # Sprites
    sp = f"{ROOT}/assets/sprites"
    hero = sprite_img(hero_frames, f"{sp}/hero.png")
    # multi_movement: [idle R, idle L, idle U, idle D, walk R, walk L, walk U, walk D]
    wjson("assets/sprites/hero.png.gbsres", sprite_res("sprite/hero","hero","hero.png","multi_movement",True,
          [[64],None,[32],[0],[80,64],None,[48,32],[16,0]], hero, (0,0,16,8)))
    elder = sprite_img([ELDER_DOWN, ELDER_UP, ELDER_RIGHT], f"{sp}/elder.png")
    wjson("assets/sprites/elder.png.gbsres", sprite_res("sprite/elder","elder","elder.png","multi",True,
          [[32],None,[16],[0]], elder, (0,-8,16,16)))
    sign = sprite_img([SIGN], f"{sp}/sign.png")
    wjson("assets/sprites/sign.png.gbsres", sprite_res("sprite/sign","sign","sign.png","fixed",False,
          [[0]], sign, (0,-8,16,16)))
    # A1: Truhe – ZWEI Animations-Zustaende mit je genau EINEM Frame:
    #     Zustand ""     (Standard) = geschlossen  -> Bild-Spalte 0
    #     Zustand "Open"            = geoeffnet    -> Bild-Spalte 16
    # Ein Zustand mit nur einem Frame kann nicht animieren -> kein Flackern (Fix fuer A1.1/A1.3/A1.6).
    chest = sprite_img([CHEST_CLOSED, CHEST_OPEN], f"{sp}/chest.png")
    res = sprite_res("sprite/chest","chest","chest.png","fixed",False, [[0]], chest, (0,-8,16,16))
    open_state = sprite_res("sprite/chest_open","chest","chest.png","fixed",False, [[16]], chest, (0,-8,16,16))["states"][0]
    open_state["name"] = CHEST_STATE_OPEN
    res["states"].append(open_state)
    wjson("assets/sprites/chest.png.gbsres", res)
    # A2: Waechter – Typ "fixed", ein Frame (Blick nach unten), keine Animation
    guard = sprite_img([GUARD], f"{sp}/guard.png")
    wjson("assets/sprites/guard.png.gbsres", sprite_res("sprite/guard","guard","guard.png","fixed",False,
          [[0]], guard, (0,-8,16,16)))
    # A3: Muenze – Typ "fixed", ein Frame, Kollisionsbox = untere 16x8 px (ein Tile hoch, wie der Spieler)
    coin = sprite_img([COIN], f"{sp}/coin.png")
    wjson("assets/sprites/coin.png.gbsres", sprite_res("sprite/coin","coin","coin.png","fixed",False,
          [[0]], coin, (0,0,16,8)))
    # A5: Schalter – Typ "fixed" (Drehung bei Interaktion aendert das Bild NICHT), zwei Zustaende mit je 1 Frame
    sw = sprite_img([SWITCH_OFF, SWITCH_ON], f"{sp}/switch.png")
    res = sprite_res("sprite/switch","switch","switch.png","fixed",False, [[0]], sw, (0,-8,16,16))
    on_state = sprite_res("sprite/switch_on","switch","switch.png","fixed",False, [[16]], sw, (0,-8,16,16))["states"][0]
    on_state["name"] = SWITCH_STATE_ON
    res["states"].append(on_state)
    wjson("assets/sprites/switch.png.gbsres", res)
    # A5: Tuer – Kollisionsbox = untere 16x8 px (genau die Tuer-Tiles)
    door = sprite_img([DOOR], f"{sp}/door.png")
    wjson("assets/sprites/door.png.gbsres", sprite_res("sprite/door","door","door.png","fixed",False,
          [[0]], door, (0,0,16,8)))
    # A5R: Schluessel – wie die Muenze
    key = sprite_img([KEY], f"{sp}/key.png")
    wjson("assets/sprites/key.png.gbsres", sprite_res("sprite/key","key","key.png","fixed",False,
          [[0]], key, (0,0,16,8)))
    # A6: neue Gegenstaende – wie die Muenze (fixed, 1 Frame, Kollisionsbox untere 16x8 px)
    for name, art in [("mushroom", MUSHROOM), ("apple", APPLE), ("gem", GEM)]:
        im = sprite_img([art], f"{sp}/{name}.png")
        wjson(f"assets/sprites/{name}.png.gbsres", sprite_res(f"sprite/{name}", name, f"{name}.png", "fixed", False,
              [[0]], im, (0,0,16,8)))
    # A7: Gegner-Sprite "slime" (fixed, 2 Frames = Wabern; Kollisionsbox wie Spieler)
    slime = sprite_img([SLIME_0, SLIME_1], f"{sp}/slime.png")
    wjson("assets/sprites/slime.png.gbsres", sprite_res("sprite/slime", "slime", "slime.png", "fixed", False,
          [[0, 16]], slime, (0,0,16,8)))
    # A6.4: Inventar-Icons in die Standardschrift
    patch_font_icons()

# ---------------------------------------------------------------- Script-Bausteine
_ev = [0]
def ev(command, args=None, children=None):
    _ev[0] += 1
    e = {"id": uid(f"event/{_ev[0]}"), "command": command, "args": args or {}}
    if children is not None: e["children"] = children
    return e
def evk(key, command, args=None, children=None):
    e = {"id": uid("event/"+key), "command": command, "args": args or {}}
    if children is not None: e["children"] = children
    return e
num = lambda v: {"type":"number","value":v}
TRUE, FALSE = {"type":"true"}, {"type":"false"}
def text(*pages): return ev("EVENT_TEXT", {"text": list(pages), "avatarId": "", "minHeight": 4, "maxHeight": 7,
                                           "position": "bottom", "showFrame": "true", "clearPrevious": True,
                                           "textX": 1, "textY": 1, "textHeight": 5, "closeWhen": "key", "closeButton": "a"})
def switch_scene(scene_id, x, y, direction, fade="2"):
    return ev("EVENT_SWITCH_SCENE", {"sceneId": scene_id, "x": num(x), "y": num(y), "direction": direction, "fadeSpeed": fade})
def set_var(var, value): return ev("EVENT_SET_VALUE", {"variable": var, "value": value})
def if_var(var, t, f): return ev("EVENT_IF", {"condition": {"type":"variable","value":var}, "__collapseElse": False},
                                  {"true": t, "false": f})
def call(script_id, name, extra=None):
    a = {"customEventId": script_id, "__name": name}; a.update(extra or {})
    return ev("EVENT_CALL_CUSTOM_EVENT", a)
def comment(txt): return ev("EVENT_COMMENT", {"text": txt, "__collapse": False})

# ---------------------------------------------------------------- IDs
SC_TITLE, SC_FOREST, SC_VILLAGE = uid("scene/title"), uid("scene/forest"), uid("scene/village")
V_MET_ELDER, V_READ_SIGN, V_VISITED, V_TITLE_CHOICE = "0", "1", "2", "3"
V_CHEST_OPENED = "4"                       # A1: 0 = Truhe zu, 1 = Truhe offen (bleibt dauerhaft)
CHEST_X, CHEST_Y = 11, 12                  # A1: Position der Truhe im Wald (Tile, untere linke Ecke)
GUARD_X, GUARD_Y = 2, 11                   # A2: Waechter im Dorf (Tile, untere linke Ecke) -> belegt (2..3, 10..11)
GUARD_DIR = "down"                         # A2: feste Blickrichtung (muss zum Sprite-Bild passen)
GUARD_TEXT = "Willkommen in\nunserem Dorf."  # A2.5: exakt der vorgegebene Text (Zeilenumbruch nur fuer die Box)
V_COIN_COUNT = "5"                         # A3: Muenzzaehler (Startwert 0)
V_COIN_TAKEN = ["6", "7", "8"]             # A3: je Muenze 0 = liegt noch, 1 = eingesammelt (dauerhaft)
COIN_POS = [(3, 6), (16, 13), (6, 14)]     # A3.1: feste Positionen im Wald (Tile, Kollisionsbox = (x..x+1, y))
CHEST_TEXT = "M\u00fcnze gefunden!"         # A3R.2: neuer Truhentext
COIN_DEBUG_TEXT = "M\u00fcnzen: $05$\nSchl\u00fcssel: $10$\nSchalter: $09$"   # A3.2 + A5: Debug (CoinCount, KeyTaken, SwitchOn)
# A6.4 Fix v2: GB Studio rendert den Text einer Box in einen Kachelpuffer von nur 52 Kacheln (0xCC-0xFF).
#   Jedes Zeichen der Monospace-Schrift belegt 1 Kachel, auch Leerzeichen; Zeilenumbrueche kosten nichts.
#   Die erste Fassung (~170 Zeichen) lief ueber: der Puffer begann von vorn und ueberschrieb die oberen
#   Zeilen (Muenzen + Schluessel verschwanden). Jetzt: nur Icon + Anzahl je Typ, Einrueckung ueber textX
#   (kostet keine Kacheln) -> 40 Kacheln, Reserve fuer zweistellige Werte.
INV_TEXT_X = 4                              # Einrueckung der Box in Kacheln (gratis, statt Leerzeichen)
INV_TILE_BUDGET = 52                        # Text-Kachelpuffer der GB-Studio-Engine
def _inv_line(icon, var): return f"{ICON[icon]} x{'$'}{int(var):02d}{'$'}"
INVENTORY_TEXT = "\n".join([      # !S0! = Text sofort
    "!S0!INVENTAR", "",
    _inv_line("coin", "5"), "",            # A6R.1: CoinCount (A3)
    _inv_line("key", "10"), "",            # A6R.1: KeyTaken (A5)
    _inv_line("mushroom", "11"), "",
    _inv_line("apple", "14"), "",
    _inv_line("gem", "16"), "",
    "B: Schlie\u00dfen"])
EMOTE_QUESTION = "70a4ce25-1fe4-4ab1-aee9-21255e70fb76"
EMOTE_LOVE = "edf96d29-9a08-4813-b2d3-46e0996f89f2"

SCRIPTS = {}
def script(key, name, symbol, desc, body, actors=None, variables=None):
    sid = uid("script/"+key)
    SCRIPTS[key] = {"_resourceType":"script","id":sid,"name":name,"symbol":symbol,"description":desc,
                    "variables": variables or {}, "actors": actors or {}, "script": body}
    return sid

S_START = uid("script/start_new_game"); S_TITLE = uid("script/title_menu")
S_TO_VILLAGE = uid("script/to_village"); S_TO_FOREST = uid("script/to_forest")
S_ELDER = uid("script/talk_elder"); S_SIGN = uid("script/read_forest_sign")
S_CHEST_OPEN = uid("script/open_treasure_chest"); S_CHEST_INIT = uid("script/treasure_chest_init")
S_GUARD = uid("script/talk_guard")         # A2
S_COIN_COLLECT = uid("script/collect_coin"); S_COIN_INIT = uid("script/coin_init")   # A3
S_COIN_DEBUG = uid("script/show_coin_counter")                                       # A3.2
SC_HOUSE = uid("scene/house")                                                        # A4
S_TO_HOUSE = uid("script/to_house"); S_HOUSE_TO_VILLAGE = uid("script/house_to_village")  # A4
V_SWITCH_ON = "9"                          # A5: 0 = Schalter aus / Werkstatt-Tuer zu, 1 = an / offen (EINZIGE Wahrheitsquelle)
V_KEY_TAKEN = "10"                         # A5R: 0 = Schluessel liegt, 1 = eingesammelt = Haustuer (A4) offen
SC_WORKSHOP = uid("scene/workshop")
# A6: Bestaende der neuen Typen (Count = EINZIGE Bestandsquelle je Typ) + Einsammel-Sperre je Objekt (Taken)
V_MUSHROOM_COUNT, V_MUSHROOM_TAKEN = "11", ["12", "13"]
V_APPLE_COUNT, V_APPLE_TAKEN = "14", ["15"]
V_GEM_COUNT, V_GEM_TAKEN = "16", ["17"]
S_ITEM_COLLECT = uid("script/collect_item")                                         # A6.2
S_INVENTORY = uid("script/open_inventory")
S_ENEMY_AI, S_ENEMY_CATCH = uid("script/enemy_ai"), uid("script/enemy_catch_player")   # A7
SIGN_X, SIGN_Y = 6, 7                                                                  # Schild im Wald (A7.5: massiv)                                          # A6.3 / A6.4
S_SWITCH_TOGGLE, S_SWITCH_INIT = uid("script/switch_toggle"), uid("script/switch_init")
S_DOOR_INIT = uid("script/door_init")
S_DOOR_LOCKED_WS, S_DOOR_LOCKED_HOUSE = uid("script/door_locked_workshop"), uid("script/door_locked_house")
S_KEY_COLLECT = uid("script/collect_key")
S_TO_WS, S_WS_TO_VILLAGE = uid("script/to_workshop"), uid("script/workshop_to_village")

def build_scripts():
    script("start_new_game", "game/Start New Game", "script_start_new_game",
        "Setzt alle Spielfortschritts-Variablen zurueck und startet im Wald.", [
        comment("Fortschritt zuruecksetzen"),
        set_var(V_MET_ELDER, FALSE), set_var(V_READ_SIGN, FALSE), set_var(V_VISITED, FALSE),
        evk("chest/reset", "EVENT_SET_VALUE", {"variable": V_CHEST_OPENED, "value": FALSE}),
        evk("coin/reset/count", "EVENT_SET_VALUE", {"variable": V_COIN_COUNT, "value": FALSE}),
        *[evk(f"coin/reset/{i+1}", "EVENT_SET_VALUE", {"variable": v, "value": FALSE}) for i, v in enumerate(V_COIN_TAKEN)],
        evk("a5/reset/c", "EVENT_COMMENT", {"text": "A5.1: Schalter aus (Tuer zu); A5R: Schluessel liegt (Haustuer zu)", "__collapse": False}),
        evk("a5/reset/switch", "EVENT_SET_VALUE", {"variable": V_SWITCH_ON, "value": FALSE}),
        evk("a5/reset/key", "EVENT_SET_VALUE", {"variable": V_KEY_TAKEN, "value": FALSE}),
        evk("a6/reset/c", "EVENT_COMMENT", {"text": "A6.2: Inventar-Anfangsbestaende = 0 (Pilze, Aepfel, Kristalle + Sperren)", "__collapse": False}),
        *[evk(f"a6/reset/{v}", "EVENT_SET_VALUE", {"variable": v, "value": FALSE})
          for v in [V_MUSHROOM_COUNT, *V_MUSHROOM_TAKEN, V_APPLE_COUNT, *V_APPLE_TAKEN, V_GEM_COUNT, *V_GEM_TAKEN]],
        comment("Spielstart: Waldszene, Spieler links auf dem Weg"),
        switch_scene(SC_FOREST, 3, 9, "right", "2"),
    ])
    script("title_menu", "game/Title Menu", "script_title_menu",
        "Titelbildschirm: versteckt den Spieler und zeigt das Menue (Start Game / Steuerung).", [
        ev("EVENT_ACTOR_DEACTIVATE", {"actorId": "player"}),
        ev("EVENT_LOOP", {}, {"true": [
            ev("EVENT_CHOICE", {"variable": V_TITLE_CHOICE, "trueText": "Start Game", "falseText": "Steuerung"}),
            if_var(V_TITLE_CHOICE,
                   [call(S_START, "Start New Game")],
                   [text("Pfeiltasten:\nLaufen", "Taste A:\nSprechen / Lesen\n/ Oeffnen", "Rand der Karte:\nGebiet wechseln",
                         "Select:\nM\u00fcnzz\u00e4hler\nanzeigen (Debug)",
                         "Taste B:\nInventar auf/zu")]),
        ]}),
    ])
    script("to_village", "world/Warp To Village", "script_warp_to_village",
        "Uebergang Wald -> Dorf (Spieler erscheint am linken Dorfeingang).", [
        set_var(V_VISITED, TRUE),
        switch_scene(SC_VILLAGE, 2, 9, "right", "2"),
    ])
    script("to_forest", "world/Warp To Forest", "script_warp_to_forest",
        "Uebergang Dorf -> Wald (Spieler erscheint am rechten Waldausgang).", [
        switch_scene(SC_FOREST, 16, 9, "left", "2"),
    ])
    script("read_forest_sign", "interaction/Read Forest Sign", "script_read_forest_sign",
        "Wegweiser im Wald (A-Knopf). Merkt sich, dass das Schild gelesen wurde.", [
        text("Wegweiser:\n-> Dorf Lindenau\n   (Osten)"),
        if_var(V_VISITED, [text("Das Dorf kennst\ndu ja schon.")], []),
        set_var(V_READ_SIGN, TRUE),
    ])
    # Stand inkl. der spaeter in der GB-Studio-UI gemachten Aenderung (Muenzstand $05$ im Dialog)
    def ui_text(t, txt, min_h, section):
        t["args"]["text"] = [txt]; t["args"]["minHeight"] = min_h; t["args"]["__section"] = section; return t
    def collapse_else(e): e["args"]["__collapseElse"] = True; return e
    script("talk_elder", "interaction/Talk Elder", "script_talk_elder",
        "Dialog mit dem Dorfaeltesten. Actor-Parameter 'Elder' = sprechende Figur.", [
        if_var(V_MET_ELDER,
            [ev("EVENT_ACTOR_EMOTE", {"actorId": "0", "emoteId": EMOTE_LOVE}),
             ui_text(text("x"), "Schoen, dich\nwiederzusehen!\n$05$", 5, "layout")],
            [ev("EVENT_ACTOR_EMOTE", {"actorId": "0", "emoteId": EMOTE_QUESTION}),
             text("Willkommen in\nLindenau,\nWanderer!", "Ich bin der\nDorfaelteste."),
             collapse_else(if_var(V_READ_SIGN,
                    [ui_text(text("x"), "Du hast den\nWegweiser im Wald\ngelesen? Gut so!\n$05$", 7, "text")],
                    [ui_text(text("x"), "Im Wald steht ein\nWegweiser. Lies\nihn ruhig mal!\n$05$", 6, "text")])),
             set_var(V_MET_ELDER, TRUE)]),
    ], actors={"0": {"id": "0", "name": "Elder"}})
    # ------------------------------------------------ A1: Interaktive Schatztruhe
    CHEST_ACTOR = {"0": {"id": "0", "name": "Chest"}}
    def chest_text(key, *pages):
        n = _ev[0]; t = text(*pages); _ev[0] = n   # Zaehler zuruecksetzen -> bestehende Event-IDs bleiben stabil
        t["id"] = uid("event/"+key); return t
    script("open_treasure_chest", "interaction/Open Treasure Chest", "script_open_treasure_chest",
        "A1: Truhe oeffnen (A-Knopf). Nur einmal: Variable ChestOpened wird ZUERST gesetzt, "
        "dann Sprite-Zustand 'Open', dann CoinCount +1 (A3R), dann Nachricht 'Muenze gefunden!'. "
        "Ist die Truhe offen, passiert nichts. "
        "Actor-Parameter 'Chest' = die Truhe.", [
        evk("chest/open/if", "EVENT_IF", {"condition": {"type": "variable", "value": V_CHEST_OPENED},
                                          "__collapseElse": False}, {
            "true": [
                evk("chest/open/noop", "EVENT_COMMENT", {"text": "Bereits geoeffnet: nichts tun (A1.5)", "__collapse": False}),
            ],
            "false": [
                evk("chest/open/c1", "EVENT_COMMENT", {"text": "Sperre gegen Doppel-Oeffnen (A1.4)", "__collapse": False}),
                evk("chest/open/set", "EVENT_SET_VALUE", {"variable": V_CHEST_OPENED, "value": TRUE}),
                evk("chest/open/c2", "EVENT_COMMENT", {"text": "Sprite sofort auf Zustand 'Open' (A1.3)", "__collapse": False}),
                evk("chest/open/state", "EVENT_ACTOR_SET_STATE", {"actorId": "0", "spriteStateId": CHEST_STATE_OPEN, "loopAnim": True}),
                evk("chest/open/c3", "EVENT_COMMENT", {"text": "A3R.1: derselbe Muenzzaehler (CoinCount) +1", "__collapse": False}),
                evk("chest/open/coin", "EVENT_INC_VALUE", {"variable": V_COIN_COUNT}),
                chest_text("chest/open/text", CHEST_TEXT),
            ],
        }),
    ], actors=CHEST_ACTOR)
    script("treasure_chest_init", "interaction/Treasure Chest Init", "script_treasure_chest_init",
        "A1: Beim Laden der Szene das Aussehen der Truhe aus ChestOpened wiederherstellen (A1.6). "
        "Actor-Parameter 'Chest' = die Truhe.", [
        evk("chest/init/if", "EVENT_IF", {"condition": {"type": "variable", "value": V_CHEST_OPENED},
                                          "__collapseElse": False}, {
            "true":  [evk("chest/init/state_open", "EVENT_ACTOR_SET_STATE", {"actorId": "0", "spriteStateId": CHEST_STATE_OPEN, "loopAnim": True})],
            "false": [evk("chest/init/state_closed", "EVENT_ACTOR_SET_STATE", {"actorId": "0", "spriteStateId": "", "loopAnim": True})],
        }),
    ], actors=CHEST_ACTOR)
    # ------------------------------------------------ A2: NPC Waechter mit Dialog
    script("talk_guard", "interaction/Talk Guard", "script_talk_guard",
        "A2: Waechter am Dorfeingang (A-Knopf). Zeigt immer denselben Text, beliebig oft wiederholbar. "
        "Keine Bewegung, keine Drehung, keine Variablen. Der Spieler ist waehrend der Textbox gesperrt.", [
        evk("guard/c1", "EVENT_COMMENT", {"text": "A2: Kein 'Actor Face Towards' -> Waechter dreht sich nie (A2.7)", "__collapse": False}),
        evk("guard/text", "EVENT_TEXT", {"text": [GUARD_TEXT], "avatarId": "", "minHeight": 4, "maxHeight": 7,
                                         "position": "bottom", "showFrame": "true", "clearPrevious": True,
                                         "textX": 1, "textY": 1, "textHeight": 5, "closeWhen": "key", "closeButton": "a"}),
    ])
    # ------------------------------------------------ A3: Sammelobjekt (Muenze) mit Zaehler
    COIN_ACTOR = {"0": {"id": "0", "name": "Coin"}}
    COIN_VARS = {"V0": {"id": "V0", "name": "Taken", "passByReference": True}}
    script("collect_coin", "coins/Collect Coin", "script_collect_coin",
        "A3: Wird als 'On Hit: Player' der Muenze aufgerufen (Kollisionsgruppe 1 -> Beruehrung genuegt). "
        "Zaehlt nur, wenn 'Taken' noch 0 ist: Taken=1, Muenze deaktivieren (verschwindet sofort), CoinCount +1. "
        "Parameter: Actor 'Coin' = die Muenze, Variable 'Taken' = CoinNTaken dieser Muenze.", [
        evk("coin/collect/if", "EVENT_IF", {"condition": {"type": "variable", "value": "V0"}, "__collapseElse": False}, {
            "true": [
                evk("coin/collect/noop", "EVENT_COMMENT", {"text": "Schon eingesammelt: nichts zaehlen (A3.4)", "__collapse": False}),
            ],
            "false": [
                evk("coin/collect/c1", "EVENT_COMMENT", {"text": "Sperre zuerst setzen -> jede Muenze zaehlt nur einmal (A3.4)", "__collapse": False}),
                evk("coin/collect/set", "EVENT_SET_VALUE", {"variable": "V0", "value": TRUE}),
                evk("coin/collect/c2", "EVENT_COMMENT", {"text": "Muenze sofort entfernen (A3.3)", "__collapse": False}),
                evk("coin/collect/hide", "EVENT_ACTOR_DEACTIVATE", {"actorId": "0"}),
                evk("coin/collect/c3", "EVENT_COMMENT", {"text": "Zaehler um genau 1 erhoehen (A3.3)", "__collapse": False}),
                evk("coin/collect/inc", "EVENT_INC_VALUE", {"variable": V_COIN_COUNT}),
            ],
        }),
    ], actors=COIN_ACTOR, variables=COIN_VARS)
    script("coin_init", "coins/Coin Init", "script_coin_init",
        "A3.5: Beim Laden der Szene bereits eingesammelte Muenzen sofort entfernen. "
        "Parameter: Actor 'Coin' = die Muenze, Variable 'Taken' = CoinNTaken dieser Muenze.", [
        evk("coin/init/if", "EVENT_IF", {"condition": {"type": "variable", "value": "V0"}, "__collapseElse": False}, {
            "true": [evk("coin/init/hide", "EVENT_ACTOR_DEACTIVATE", {"actorId": "0"})],
            "false": [],
        }),
    ], actors=COIN_ACTOR, variables=COIN_VARS)
    script("show_coin_counter", "debug/Show Coin Counter", "script_show_coin_counter",
        "A3.2: Debug-Ausgabe des Muenzzaehlers (Select-Taste in allen Spielszenen). "
        "A5: zusaetzlich KeyTaken (Schluessel) und SwitchOn (Schalter) als 0/1. Spieler ist waehrenddessen gesperrt.", [
        evk("coin/debug/lock", "EVENT_SCRIPT_LOCK", {}),
        evk("coin/debug/text", "EVENT_TEXT", {"text": [COIN_DEBUG_TEXT], "avatarId": "", "minHeight": 4, "maxHeight": 7,
                                              "position": "bottom", "showFrame": "true", "clearPrevious": True,
                                              "textX": 1, "textY": 1, "textHeight": 5, "closeWhen": "key", "closeButton": "a"}),
        evk("coin/debug/unlock", "EVENT_SCRIPT_UNLOCK", {}),
    ])
    # ------------------------------------------------ A4: Tuer Dorf <-> Hausinneres
    hx, hy, hdir = HOUSE_SPAWN
    script("to_house", "world/Warp To House", "script_warp_to_house",
        "A4: Uebergang Dorf -> Hausinneres. Ausloeser: Trigger 'To House' auf dem Tuerfeld (Beruehrung). "
        "Spieler erscheint auf festem Feld vor der Fussmatte (nicht auf dem Rueckkehr-Trigger).", [
        evk("house/in/c1", "EVENT_COMMENT", {"text": f"A4.3: Ankunft ({hx}, {hy}), Blick {hdir}; Rueckkehr-Trigger liegt bei y = {EXIT_Y}", "__collapse": False}),
        evk("house/in/switch", "EVENT_SWITCH_SCENE", {"sceneId": SC_HOUSE, "x": num(hx), "y": num(hy), "direction": hdir, "fadeSpeed": "2"}),
    ])
    vx, vy, vdir = VILLAGE_SPAWN_FROM_HOUSE
    script("house_to_village", "world/Warp House To Village", "script_warp_house_to_village",
        "A4: Uebergang Hausinneres -> Dorf. Ausloeser: Trigger 'Exit House' auf der Fussmatte (Beruehrung). "
        "Spieler erscheint vor der Haustuer (nicht auf dem Tuer-Trigger).", [
        evk("house/out/c1", "EVENT_COMMENT", {"text": f"A4.4: Ankunft ({vx}, {vy}), Blick {vdir}; Tuer-Trigger liegt bei y = {HOUSE_DOOR_Y}", "__collapse": False}),
        evk("house/out/switch", "EVENT_SWITCH_SCENE", {"sceneId": SC_VILLAGE, "x": num(vx), "y": num(vy), "direction": vdir, "fadeSpeed": "2"}),
    ])
    # ------------------------------------------------ A5: Schalter mit Tuermechanismus
    c = lambda key, txt: evk(key, "EVENT_COMMENT", {"text": txt, "__collapse": False})
    def a5_text(key, *pages):
        return evk(key, "EVENT_TEXT", {"text": list(pages), "avatarId": "", "minHeight": 4, "maxHeight": 7,
                                       "position": "bottom", "showFrame": "true", "clearPrevious": True,
                                       "textX": 1, "textY": 1, "textHeight": 5, "closeWhen": "key", "closeButton": "a"})
    SW_ACTORS = {"0": {"id": "0", "name": "Switch"}, "1": {"id": "1", "name": "Door"}}
    ON_VAR = {"V0": {"id": "V0", "name": "On", "passByReference": True}}
    script("switch_toggle", "switch/Toggle Switch", "script_toggle_switch",
        "A5.3/A5.4/A5.5: Schalter per A-Knopf umlegen. Die Variable 'On' ist die EINZIGE Wahrheitsquelle: "
        "sie wird zuerst gesetzt, danach werden Schalter-Sprite und Tuer im selben Durchlauf daraus abgeleitet "
        "(nie widerspruechlich). AN: Zustand 'On' + Tuer-Actor deaktivieren (Tuer offen, Trigger erreichbar). "
        "AUS: Zustand '' + Tuer-Actor aktivieren (Tuer zu, blockiert). "
        "Parameter: Actor 'Switch' = Schalter, Actor 'Door' = Tuer, Variable 'On' = SwitchOn.", [
        evk("a5/toggle/if", "EVENT_IF", {"condition": {"type": "variable", "value": "V0"}, "__collapseElse": False}, {
            "true": [
                c("a5/toggle/c_off", "A5.4: AN -> AUS: Tuer sofort schliessen"),
                evk("a5/toggle/set_off", "EVENT_SET_VALUE", {"variable": "V0", "value": FALSE}),
                evk("a5/toggle/state_off", "EVENT_ACTOR_SET_STATE", {"actorId": "0", "spriteStateId": "", "loopAnim": True}),
                evk("a5/toggle/door_close", "EVENT_ACTOR_ACTIVATE", {"actorId": "1"}),
            ],
            "false": [
                c("a5/toggle/c_on", "A5.3: AUS -> AN: Tuer sofort oeffnen"),
                evk("a5/toggle/set_on", "EVENT_SET_VALUE", {"variable": "V0", "value": TRUE}),
                evk("a5/toggle/state_on", "EVENT_ACTOR_SET_STATE", {"actorId": "0", "spriteStateId": SWITCH_STATE_ON, "loopAnim": True}),
                evk("a5/toggle/door_open", "EVENT_ACTOR_DEACTIVATE", {"actorId": "1"}),
            ],
        }),
    ], actors=SW_ACTORS, variables=ON_VAR)
    script("switch_init", "switch/Switch Init", "script_switch_init",
        "A5.1/A5.7: Beim Laden der Szene das Aussehen des Schalters aus der Variable 'On' wiederherstellen. "
        "Parameter: Actor 'Switch' = Schalter, Variable 'On' = SwitchOn.", [
        evk("a5/swinit/if", "EVENT_IF", {"condition": {"type": "variable", "value": "V0"}, "__collapseElse": False}, {
            "true":  [evk("a5/swinit/on",  "EVENT_ACTOR_SET_STATE", {"actorId": "0", "spriteStateId": SWITCH_STATE_ON, "loopAnim": True})],
            "false": [evk("a5/swinit/off", "EVENT_ACTOR_SET_STATE", {"actorId": "0", "spriteStateId": "", "loopAnim": True})],
        }),
    ], actors={"0": {"id": "0", "name": "Switch"}}, variables=ON_VAR)
    script("door_init", "doors/Door Init", "script_door_init",
        "A5.1/A5.7/A5R.2: Beim Laden der Szene: ist 'Open' = 1, wird der Tuer-Actor sofort deaktiviert "
        "(Oeffnung frei, Trigger erreichbar). Sonst bleibt er aktiv und blockiert den Spieler. "
        "Wird fuer BEIDE Tueren benutzt: Werkstatt (Open = SwitchOn) und Haus 1 (Open = KeyTaken). "
        "Parameter: Actor 'Door' = Tuer, Variable 'Open'.", [
        evk("a5/doorinit/if", "EVENT_IF", {"condition": {"type": "variable", "value": "V0"}, "__collapseElse": False}, {
            "true":  [evk("a5/doorinit/open", "EVENT_ACTOR_DEACTIVATE", {"actorId": "0"})],
            "false": [c("a5/doorinit/closed", "Verschlossen: Tuer-Actor bleibt aktiv und blockiert (A5.2 / A5R.2)")],
        }),
    ], actors={"0": {"id": "0", "name": "Door"}},
       variables={"V0": {"id": "V0", "name": "Open", "passByReference": True}})
    script("door_locked_workshop", "doors/Locked Workshop Door", "script_locked_workshop_door",
        "A5.2: A-Knopf an der verschlossenen Werkstatt-Tuer. Nur Hinweistext; der Actor selbst blockiert den Spieler.", [
        a5_text("a5/locked_ws/text", "Die T\u00fcr ist\nverschlossen.", "Irgendwo muss\nein Schalter\nsein ..."),
    ])
    script("door_locked_house", "doors/Locked House Door", "script_locked_house_door",
        "A5R.2: A-Knopf an der verschlossenen Haustuer (A4). Nur Hinweistext; der Actor selbst blockiert den Spieler.", [
        a5_text("a5/locked_house/text", "Verschlossen.\nDu brauchst\neinen Schl\u00fcssel."),
    ])
    script("collect_key", "keys/Collect Key", "script_collect_key",
        "A5R.1: Wie 'Collect Coin' (On Hit: Player, Kollisionsgruppe 1), aber OHNE Muenzzaehler. "
        "Zaehlt nur, wenn 'Taken' noch 0 ist: Taken=1, Schluessel deaktivieren (verschwindet sofort). "
        "A5R.3: Der Schluessel wird NICHT verbraucht; Taken=1 bedeutet dauerhaft 'Haustuer offen'. "
        "Parameter: Actor 'Key' = Schluessel, Variable 'Taken' = KeyTaken.", [
        evk("a5/key/if", "EVENT_IF", {"condition": {"type": "variable", "value": "V0"}, "__collapseElse": False}, {
            "true": [c("a5/key/noop", "Schon eingesammelt: nichts tun (kein Doppelzaehlen)")],
            "false": [
                c("a5/key/c1", "Sperre zuerst setzen -> nur einmal einsammelbar"),
                evk("a5/key/set", "EVENT_SET_VALUE", {"variable": "V0", "value": TRUE}),
                c("a5/key/c2", "Schluessel sofort entfernen"),
                evk("a5/key/hide", "EVENT_ACTOR_DEACTIVATE", {"actorId": "0"}),
            ],
        }),
    ], actors={"0": {"id": "0", "name": "Key"}},
       variables={"V0": {"id": "V0", "name": "Taken", "passByReference": True}})
    wx_, wy_, wdir_ = WS_SPAWN
    script("to_workshop", "world/Warp To Workshop", "script_warp_to_workshop",
        "A5.6: Uebergang Dorf -> Werkstatt. Ausloeser: Trigger 'To Workshop' auf der Tueroeffnung; "
        "nur erreichbar, wenn der Tuer-Actor deaktiviert ist (Schalter an).", [
        c("a5/ws_in/c1", f"A5.6: Ankunft ({wx_}, {wy_}), Blick {wdir_}; Rueckweg-Trigger liegt bei y = {WS_EXIT_Y}"),
        evk("a5/ws_in/switch", "EVENT_SWITCH_SCENE", {"sceneId": SC_WORKSHOP, "x": num(wx_), "y": num(wy_), "direction": wdir_, "fadeSpeed": "2"}),
    ])
    vx_, vy_, vdir_ = VILLAGE_SPAWN_FROM_WS
    script("workshop_to_village", "world/Warp Workshop To Village", "script_warp_workshop_to_village",
        "A5.6: Rueckweg Werkstatt -> Dorf. Ausloeser: Trigger 'Exit Workshop' auf der Fussmatte. "
        "Spieler erscheint vor der Werkstatt (nicht auf dem Tuer-Trigger).", [
        c("a5/ws_out/c1", f"A5.6: Ankunft ({vx_}, {vy_}), Blick {vdir_}; Tuer-Trigger liegt bei y = {WS_DOOR_Y}"),
        evk("a5/ws_out/switch", "EVENT_SWITCH_SCENE", {"sceneId": SC_VILLAGE, "x": num(vx_), "y": num(vy_), "direction": vdir_, "fadeSpeed": "2"}),
    ])
    # ------------------------------------------------ A6: Einfaches Inventarsystem
    script("collect_item", "items/Collect Item", "script_collect_item",
        "A6.2: Wird als 'On Hit: Player' eines Gegenstands aufgerufen (Kollisionsgruppe 1 -> Beruehrung genuegt). "
        "Nur wenn 'Taken' noch 0 ist: Taken=1, Gegenstand deaktivieren (verschwindet sofort), 'Count' (Bestand "
        "GENAU dieses Typs) +1. Parameter: Actor 'Item' = Gegenstand, Variable 'Taken' = Sperre dieses Objekts, "
        "Variable 'Count' = Bestand des Typs (MushroomCount / AppleCount / GemCount).", [
        evk("a6/item/if", "EVENT_IF", {"condition": {"type": "variable", "value": "V0"}, "__collapseElse": False}, {
            "true": [c("a6/item/noop", "Schon eingesammelt: nichts zaehlen")],
            "false": [
                c("a6/item/c1", "Sperre zuerst setzen -> jedes Objekt zaehlt nur einmal"),
                evk("a6/item/set", "EVENT_SET_VALUE", {"variable": "V0", "value": TRUE}),
                c("a6/item/c2", "Gegenstand sofort entfernen (A6.2)"),
                evk("a6/item/hide", "EVENT_ACTOR_DEACTIVATE", {"actorId": "0"}),
                c("a6/item/c3", "Bestand genau dieses Typs um 1 erhoehen (A6.2)"),
                evk("a6/item/inc", "EVENT_INC_VALUE", {"variable": "V1"}),
            ],
        }),
    ], actors={"0": {"id": "0", "name": "Item"}},
       variables={"V0": {"id": "V0", "name": "Taken", "passByReference": True},
                  "V1": {"id": "V1", "name": "Count", "passByReference": True}})
    script("open_inventory", "inventory/Open Inventory", "script_open_inventory",
        "A6.3-A6.6 + A6R: Inventar per B-Knopf. Script-Lock -> Spiel steht still (Spieler, Actors, Timer). "
        "Sprites ausblenden, bildschirmfuellende Textbox mit Icon (Zeichen der Schrift) + Bestand je Typ. "
        "Die Bestaende werden DIREKT aus den Spielvariablen gelesen (CoinCount, KeyTaken, MushroomCount, "
        "AppleCount, GemCount) -> keine doppelte Buchfuehrung. Schliessen nur mit B, danach laeuft alles weiter. "
        "Waehrend eines Dialogs ist das Spiel gesperrt -> der B-Knopf-Script startet dort nicht (A6.6).", [
        c("a6/inv/c1", "A6.5: Spiel anhalten (Spieler/Actors/Timer/Knopf-Scripts stehen)"),
        evk("a6/inv/lock", "EVENT_SCRIPT_LOCK", {}),
        evk("a6/inv/hide", "EVENT_HIDE_SPRITES", {}),
        c("a6/inv/c2", "A6.4 / A6R.1 / A6R.2: Icon + Anzahl je Typ, Werte direkt aus den Variablen"),
        evk("a6/inv/text", "EVENT_TEXT", {"text": [INVENTORY_TEXT], "avatarId": "", "minHeight": 18, "maxHeight": 18,
                                          "position": "bottom", "showFrame": "true", "clearPrevious": True,
                                          "textX": INV_TEXT_X, "textY": 1, "textHeight": 16, "closeWhen": "key", "closeButton": "b"}),
        c("a6/inv/c3", "A6.3: mit B geschlossen -> alles laeuft wie zuvor weiter (A6.5)"),
        evk("a6/inv/show", "EVENT_SHOW_SPRITES", {}),
        evk("a6/inv/unlock", "EVENT_SCRIPT_UNLOCK", {}),
    ])
    # ------------------------------------------------ A7: Gegner mit Verfolgungsverhalten
    var = lambda n: {"type": "variable", "value": EV[n]}
    def op(t, a, b): return {"type": t, "valueA": a, "valueB": b}
    def un(t, a): return {"type": t, "value": a}
    sign = lambda v: op("min", op("max", v, num(-1)), num(1))          # Vorzeichen -1/0/+1 (Werte sind ganzzahlig)
    def setv(key, n, value): return evk(key, "EVENT_SET_VALUE", {"variable": EV[n], "value": value})
    def cond(key, condition, t, f):
        return evk(key, "EVENT_IF", {"condition": condition, "__collapseElse": False}, {"true": t, "false": f})
    def try_move(key, sx, sy):
        """Ein Schritt (1 Tile) mit Wandkollision. Danach: EnemyMoved = 0 -> blockiert, sonst bewegt."""
        return [
            setv(key+"/sx", "EnemyStepX", sx), setv(key+"/sy", "EnemyStepY", sy),
            evk(key+"/move", "EVENT_ACTOR_MOVE_RELATIVE", {"actorId": "0", "x": var("EnemyStepX"), "y": var("EnemyStepY"),
                "units": "tiles", "collideWith": ["walls"], "moveType": "horizontal", "lockDirection": []}),
            evk(key+"/pos", "EVENT_ACTOR_GET_POSITION", {"actorId": "0", "vectorX": EV["EnemyNewX"], "vectorY": EV["EnemyNewY"], "units": "tiles"}),
            setv(key+"/moved", "EnemyMoved", op("add", un("abs", op("sub", var("EnemyNewX"), var("EnemyX"))),
                                                       un("abs", op("sub", var("EnemyNewY"), var("EnemyY"))))),
            setv(key+"/ex", "EnemyX", var("EnemyNewX")), setv(key+"/ey", "EnemyY", var("EnemyNewY")),
        ]
    not_moved = op("eq", var("EnemyMoved"), num(0))
    def chain(key, moves):
        """Versucht die Schritte der Reihe nach, bis einer klappt (A7.5: Hindernis umgehen statt haengen)."""
        (sx, sy), rest = moves[0], moves[1:]
        body = try_move(key, sx, sy)
        if rest: body.append(cond(key+"/if", not_moved, chain(key+"/n", rest), []))
        return body
    sdx, sdy = sign(var("EnemyDX")), sign(var("EnemyDY"))
    chase = [
        c("a7/chase/c", "A7.3: Spieler im Radius -> 1 Feld auf ihn zu (Hauptachse, sonst Nebenachse, sonst ausweichen)"),
        setv("a7/chase/flag", "EnemyChasing", TRUE), setv("a7/chase/blk", "EnemyBlocked", num(0)),
        cond("a7/chase/axis", op("gte", var("EnemyADY"), var("EnemyADX")),
             chain("a7/chase/v", [(num(0), sdy), (sdx, num(0)), (num(1), num(0)), (num(-1), num(0))]),
             chain("a7/chase/h", [(sdx, num(0)), (num(0), sdy), (num(0), num(1)), (num(0), num(-1))])),
    ]
    flip = lambda key: setv(key, "EnemyPatrolDir", op("sub", num(0), var("EnemyPatrolDir")))
    patrol = [
        c("a7/patrol/c1", "A7.4: Verfolgung beendet -> aktuelles Feld = neues Ausgangsfeld, wieder 2 nach rechts / 2 nach links"),
        cond("a7/patrol/end", op("eq", var("EnemyChasing"), num(1)), [
            setv("a7/patrol/end/flag", "EnemyChasing", FALSE),
            setv("a7/patrol/end/dir", "EnemyPatrolDir", num(1)),
            setv("a7/patrol/end/steps", "EnemyPatrolSteps", num(0)),
        ], []),
        c("a7/patrol/c2", "A7.1: Patrouillenschritt (1x3-Bereich, Hin und Her)"),
        *try_move("a7/patrol/step", var("EnemyPatrolDir"), num(0)),
        cond("a7/patrol/blocked", not_moved, [
            c("a7/patrol/blk/c", "A7.5: Wand/Hindernis -> sofort umdrehen"),
            evk("a7/patrol/blk/inc", "EVENT_INC_VALUE", {"variable": EV["EnemyBlocked"]}),
            flip("a7/patrol/blk/flip"), setv("a7/patrol/blk/steps", "EnemyPatrolSteps", num(0)),
            cond("a7/patrol/stuck", op("gte", var("EnemyBlocked"), num(2)), [
                c("a7/patrol/stuck/c", "A7.5: links UND rechts blockiert -> 1 Feld nach unten/oben ausweichen (nie dauerhaft haengen)"),
                *chain("a7/patrol/stuck/mv", [(num(0), num(1)), (num(0), num(-1))]),
                setv("a7/patrol/stuck/reset", "EnemyBlocked", num(0)),
            ], []),
        ], [
            setv("a7/patrol/ok/blk", "EnemyBlocked", num(0)),
            evk("a7/patrol/ok/inc", "EVENT_INC_VALUE", {"variable": EV["EnemyPatrolSteps"]}),
            cond("a7/patrol/ok/turn", op("gte", var("EnemyPatrolSteps"), num(2)), [
                flip("a7/patrol/ok/flip"), setv("a7/patrol/ok/steps", "EnemyPatrolSteps", num(0)),
            ], []),
        ]),
    ]
    tick = [
        c("a7/tick/c", "Positionen in Tiles lesen, Chebyshev-Distanz = max(|dx|, |dy|)"),
        evk("a7/tick/epos", "EVENT_ACTOR_GET_POSITION", {"actorId": "0", "vectorX": EV["EnemyX"], "vectorY": EV["EnemyY"], "units": "tiles"}),
        evk("a7/tick/ppos", "EVENT_ACTOR_GET_POSITION", {"actorId": "player", "vectorX": EV["EnemyPlayerX"], "vectorY": EV["EnemyPlayerY"], "units": "tiles"}),
        setv("a7/tick/dx", "EnemyDX", op("sub", var("EnemyPlayerX"), var("EnemyX"))),
        setv("a7/tick/dy", "EnemyDY", op("sub", var("EnemyPlayerY"), var("EnemyY"))),
        setv("a7/tick/adx", "EnemyADX", un("abs", var("EnemyDX"))),
        setv("a7/tick/ady", "EnemyADY", un("abs", var("EnemyDY"))),
        setv("a7/tick/dist", "EnemyDist", op("max", var("EnemyADX"), var("EnemyADY"))),
        cond("a7/tick/radius", op("lte", var("EnemyDist"), num(ENEMY_RADIUS)), chase, patrol),
        evk("a7/tick/wait", "EVENT_WAIT", {"time": num(0.5), "frames": num(1), "units": "frames"}),
    ]
    script("enemy_ai", "enemy/Enemy AI", "script_enemy_ai",
        "A7: Gegner-KI. Wird als 'On Update' des Gegners aufgerufen. Startet IMMER am Patrouillenstart "
        "(Parameter StartX/StartY), patrouilliert 2 Felder rechts / 2 Felder links und verfolgt den Spieler, "
        "solange die Chebyshev-Distanz <= 2 ist. Bewegung nur Feld fuer Feld mit Wandkollision. "
        "Parameter: Actor 'Enemy', Variablen 'StartX'/'StartY' (Tiles, als Wert).", [
        c("a7/init/c", "A7.2: Bei jedem Szenenstart (Update-Thread startet neu): an den Patrouillenstart, Zustand zuruecksetzen"),
        evk("a7/init/pos", "EVENT_ACTOR_SET_POSITION", {"actorId": "0", "x": {"type": "variable", "value": "V0"},
                                                        "y": {"type": "variable", "value": "V1"}, "units": "tiles"}),
        setv("a7/init/chase", "EnemyChasing", FALSE), setv("a7/init/dir", "EnemyPatrolDir", num(1)),
        setv("a7/init/steps", "EnemyPatrolSteps", num(0)), setv("a7/init/blk", "EnemyBlocked", num(0)),
        evk("a7/loop", "EVENT_LOOP", {}, {"true": tick}),
    ], actors={"0": {"id": "0", "name": "Enemy"}},
       variables={"V0": {"id": "V0", "name": "StartX", "passByReference": False},
                  "V1": {"id": "V1", "name": "StartY", "passByReference": False}})
    script("enemy_catch_player", "enemy/Enemy Catch Player", "script_enemy_catch_player",
        "A7.7: 'On Hit: Player' des Gegners (Kollisionsgruppe 1 -> Felder ueberlappen bzw. Spieler laeuft hinein). "
        "Spiel anhalten, Nachricht zeigen, Gegner entfernen, zurueck zum Titelbildschirm (Startmenue) -> "
        "'Start Game' setzt den Spielstand zurueck. Parameter: Actor 'Enemy'.", [
        c("a7/catch/c1", "Alles anhalten (Gegner-KI, Spieler, Knopf-Scripts)"),
        evk("a7/catch/lock", "EVENT_SCRIPT_LOCK", {}),
        a5_text("a7/catch/text", *ENEMY_CATCH_TEXT),
        evk("a7/catch/hide", "EVENT_ACTOR_DEACTIVATE", {"actorId": "0"}),
        evk("a7/catch/unlock", "EVENT_SCRIPT_UNLOCK", {}),
        c("a7/catch/c2", "A7.7: ins Startmenue -> Neustart noetig"),
        evk("a7/catch/switch", "EVENT_SWITCH_SCENE", {"sceneId": SC_TITLE, "x": num(9), "y": num(9), "direction": "down", "fadeSpeed": "2"}),
    ], actors={"0": {"id": "0", "name": "Enemy"}})
    for key, res in SCRIPTS.items():
        folder, fname = res["name"].split("/")
        wjson(f"project/scripts/{folder}/{fname.lower().replace(' ','_')}.gbsres", res)

# ---------------------------------------------------------------- Szenen
def actor(key, idx, name, symbol, x, y, sprite, direction, script_body):
    return {"_resourceType":"actor","id":uid(key),"_index":idx,"symbol":symbol,"prefabId":"","name":name,
            "coordinateType":"tiles","x":x,"y":y,"frame":0,"animate":False,"spriteSheetId":sprite,"paletteId":"",
            "direction":direction,"moveSpeed":1,"animSpeed":15,"isPinned":False,"persistent":False,
            "collisionGroup":"","collisionExtraFlags":[],"prefabScriptOverrides":{},"script":script_body,
            "startScript":[],"updateScript":[],"hit1Script":[],"hit2Script":[],"hit3Script":[]}
def trigger(key, idx, name, symbol, x, y, w, h, script_body):
    return {"_resourceType":"trigger","id":uid(key),"_index":idx,"symbol":symbol,"prefabId":"","name":name,
            "x":x,"y":y,"width":w,"height":h,"prefabScriptOverrides":{},"script":script_body,"leaveScript":[]}
def scene(sid, idx, name, symbol, folder, wx, wy, bg, collisions, body, actors=(), triggers=()):
    res = {"_resourceType":"scene","id":sid,"_index":idx,"type":"TOPDOWN","name":name,"symbol":symbol,
           "x":wx,"y":wy,"width":20,"height":18,"backgroundId":uid("bg/"+bg),"tilesetId":"",
           "colorModeOverride":"none","paletteIds":[],"spritePaletteIds":[],"autoFadeSpeed":1,
           "script":body,"playerHit1Script":[],"playerHit2Script":[],"playerHit3Script":[],
           "collisions": compress(collisions) if collisions else ""}
    base = f"project/scenes/{folder}"
    wjson(f"{base}/scene.gbsres", res)
    for a in actors: wjson(f"{base}/actors/{a['name'].lower().replace(' ','_')}.gbsres", a)
    for t in triggers: wjson(f"{base}/triggers/{t['name'].lower().replace(' ','_')}.gbsres", t)

def coin_debug_key(scene_key):
    """A3.2: Select-Taste zeigt den Muenzzaehler (im Szenen-'On Init' gesetzt)."""
    return evk(f"coin/debug/{scene_key}/input", "EVENT_SET_INPUT_SCRIPT",
               {"input": ["select"], "override": True, "__scriptTabs": "press"},
               {"true": [evk(f"coin/debug/{scene_key}/call", "EVENT_CALL_CUSTOM_EVENT",
                             {"customEventId": S_COIN_DEBUG, "__name": "Show Coin Counter"})]})

def inventory_key(scene_key):
    """A6.3: B-Knopf oeffnet das Inventar (im Szenen-'On Init' gesetzt; GB Studio loescht Knopf-Scripts bei Szenenwechsel)."""
    return evk(f"a6/inv/{scene_key}/input", "EVENT_SET_INPUT_SCRIPT",
               {"input": ["b"], "override": True, "__scriptTabs": "press"},
               {"true": [evk(f"a6/inv/{scene_key}/call", "EVENT_CALL_CUSTOM_EVENT",
                             {"customEventId": S_INVENTORY, "__name": "Open Inventory"})]})

ITEM_TYPES = {   # A6: Typ -> (Sprite, Count-Variable, Taken-Variablen, Positionen, Anzeigename)
    "mushroom": (SPRITE_MUSHROOM, V_MUSHROOM_COUNT, V_MUSHROOM_TAKEN, MUSHROOM_POS, "Mushroom"),
    "apple":    (SPRITE_APPLE,    V_APPLE_COUNT,    V_APPLE_TAKEN,    APPLE_POS,    "Apple"),
    "gem":      (SPRITE_GEM,      V_GEM_COUNT,      V_GEM_TAKEN,      GEM_POS,      "Gem"),
}
def item_actors(scene_key, first_index):
    """A6.1/A6.2/A6.7: Gegenstands-Actors einer Szene (On Hit -> Collect Item, On Init -> Coin Init)."""
    res = []
    for typ, (sprite, count_var, taken_vars, positions, label) in ITEM_TYPES.items():
        for n, ((sk, x, y), taken) in enumerate(zip(positions, taken_vars), start=1):
            if sk != scene_key: continue
            key = f"actor/{sk}_{typ}_{n}"; aid = uid(key)
            name = f"{label} {n}" if len(positions) > 1 else label
            a = actor(key, first_index + len(res), name, f"actor_{typ}_{n}", x, y, sprite, "down",
                      [evk(f"a6/{typ}/{n}/hit", "EVENT_CALL_CUSTOM_EVENT",
                           {"customEventId": S_ITEM_COLLECT, "__name": "Collect Item", "$actor[0]$": aid,
                            "$variable[V0]$": {"type": "variable", "value": taken},
                            "$variable[V1]$": {"type": "variable", "value": count_var}})])
            a["collisionGroup"] = "1"        # 'script' = On Hit: Player (Beruehrung), wie Muenzen
            a["animSpeed"] = 255
            a["startScript"] = [evk(f"a6/{typ}/{n}/init", "EVENT_CALL_CUSTOM_EVENT",
                                    {"customEventId": S_COIN_INIT, "__name": "Coin Init", "$actor[0]$": aid,
                                     "$variable[V0]$": {"type": "variable", "value": taken}})]
            res.append(a)
    return res

def coin_actors(first_index):
    res = []
    for i, ((x, y), var) in enumerate(zip(COIN_POS, V_COIN_TAKEN)):
        n = i + 1; key = f"actor/forest_coin_{n}"; aid = uid(key)
        params = {"$actor[0]$": aid, "$variable[V0]$": {"type": "variable", "value": var}}
        a = actor(key, first_index + i, f"Coin {n}", f"actor_coin_{n}", x, y, SPRITE_COIN, "down",
                  [evk(f"coin/{n}/hit", "EVENT_CALL_CUSTOM_EVENT",
                       dict({"customEventId": S_COIN_COLLECT, "__name": "Collect Coin"}, **params))])
        a["collisionGroup"] = "1"            # A3: 'script' = On Hit: Player (Beruehrung statt A-Knopf)
        a["animSpeed"] = 255                 # keine Animation
        a["startScript"] = [evk(f"coin/{n}/init", "EVENT_CALL_CUSTOM_EVENT",
                                dict({"customEventId": S_COIN_INIT, "__name": "Coin Init"}, **params))]
        res.append(a)
    return res

def build_scenes():
    scene(SC_TITLE, 0, "Title Screen", "scene_title_screen", "title_screen", 60, 60, "title_screen", None,
          [call(S_TITLE, "Title Menu")])
    fc = forest.collisions()
    for dx in (0, 1):                        # A1.1: Truhe ist solide (2x2 Tiles), zusaetzlich zur Actor-Kollision
        for dy in (0, -1): fc[(CHEST_Y+dy)*20 + CHEST_X+dx] = SOLID
    chest_id = uid("actor/forest_chest")
    chest_actor = actor("actor/forest_chest", 1, "Treasure Chest", "actor_treasure_chest", CHEST_X, CHEST_Y,
                        SPRITE_CHEST, "down",
                        [evk("chest/actor/interact", "EVENT_CALL_CUSTOM_EVENT",
                             {"customEventId": S_CHEST_OPEN, "__name": "Open Treasure Chest", "$actor[0]$": chest_id})])
    chest_actor["animSpeed"] = 255             # A1: keine Animation ("None")
    chest_actor["startScript"] = [evk("chest/actor/init", "EVENT_CALL_CUSTOM_EVENT",
                             {"customEventId": S_CHEST_INIT, "__name": "Treasure Chest Init", "$actor[0]$": chest_id})]
    # A5R: Schluessel im Wald (Verhalten wie Muenze; Init-Script der Muenze wird wiederverwendet)
    key_id = uid("actor/forest_key")
    key_params = {"$actor[0]$": key_id, "$variable[V0]$": {"type": "variable", "value": V_KEY_TAKEN}}
    key_actor = actor("actor/forest_key", 5, "Key", "actor_key", KEY_X, KEY_Y, SPRITE_KEY, "down",
                      [evk("a5/key/actor/hit", "EVENT_CALL_CUSTOM_EVENT",
                           dict({"customEventId": S_KEY_COLLECT, "__name": "Collect Key"}, **key_params))])
    key_actor["collisionGroup"] = "1"          # 'script' = On Hit: Player (Beruehrung), wie die Muenzen
    key_actor["animSpeed"] = 255
    key_actor["startScript"] = [evk("a5/key/actor/init", "EVENT_CALL_CUSTOM_EVENT",
                                    dict({"customEventId": S_COIN_INIT, "__name": "Coin Init"}, **key_params))]
    for dx in (0, 1):                        # A7.5: Schild ist ein festes Objekt -> 2x2 massive Tiles (Gegner laeuft nicht hindurch)
        for dy in (0, -1): fc[(SIGN_Y+dy)*20 + SIGN_X+dx] = SOLID
    # A7: Gegner "Slime" (Kollisionsgruppe 1 -> 'script' = On Hit: Player)
    slime_id = uid("actor/forest_slime")
    slime = actor("actor/forest_slime", 7, "Slime", "actor_slime", ENEMY_START[0], ENEMY_START[1], SPRITE_SLIME, "down",
                  [evk("a7/actor/hit", "EVENT_CALL_CUSTOM_EVENT",
                       {"customEventId": S_ENEMY_CATCH, "__name": "Enemy Catch Player", "$actor[0]$": slime_id})])
    slime["collisionGroup"] = "1"
    slime["moveSpeed"] = ENEMY_SPEED         # A7.6
    slime["animSpeed"] = 15
    slime["updateScript"] = [evk("a7/actor/update", "EVENT_CALL_CUSTOM_EVENT",
                                 {"customEventId": S_ENEMY_AI, "__name": "Enemy AI", "$actor[0]$": slime_id,
                                  "$variable[V0]$": num(ENEMY_START[0]), "$variable[V1]$": num(ENEMY_START[1])})]
    scene(SC_FOREST, 1, "Forest", "scene_forest", "forest", 300, 60, "forest", fc,
          [coin_debug_key("forest"), inventory_key("forest")],
          actors=[actor("actor/forest_sign", 0, "Forest Sign", "actor_forest_sign", 6, 7, SPRITE_SIGN, "down",
                        [call(S_SIGN, "Read Forest Sign")]), chest_actor] + coin_actors(2) + [key_actor]
                 + item_actors("forest", 6) + [slime],
          triggers=[trigger("trigger/forest_exit", 0, "To Village", "trigger_to_village", 19, 8, 1, 2,
                            [call(S_TO_VILLAGE, "Warp To Village")])])
    vc = village.collisions()
    for dx in (0, 1):                        # A2.3: Waechter ist solide (2x2 Tiles), zusaetzlich zur Actor-Kollision
        for dy in (0, -1): vc[(GUARD_Y+dy)*20 + GUARD_X+dx] = SOLID
    guard_actor = actor("actor/village_guard", 1, "Guard", "actor_village_guard", GUARD_X, GUARD_Y,
                        SPRITE_GUARD, GUARD_DIR,
                        [evk("guard/actor/interact", "EVENT_CALL_CUSTOM_EVENT",
                             {"customEventId": S_GUARD, "__name": "Talk Guard"})])
    guard_actor["animSpeed"] = 255             # A2.2: keine Animation ("None"); kein startScript/updateScript -> keine Bewegung
    elder_id = uid("actor/village_elder")
    # A5: Schalter (solide 2x2 wie der Waechter) + zwei Tuer-Actors
    for dx in (0, 1):
        for dy in (0, -1): vc[(SWITCH_Y+dy)*20 + SWITCH_X+dx] = SOLID
    switch_id, ws_door_id, house_door_id = uid("actor/village_switch"), uid("actor/village_ws_door"), uid("actor/village_house_door")
    sw_params = {"$actor[0]$": switch_id, "$actor[1]$": ws_door_id,
                 "$variable[V0]$": {"type": "variable", "value": V_SWITCH_ON}}
    switch_actor = actor("actor/village_switch", 2, "Workshop Switch", "actor_workshop_switch", SWITCH_X, SWITCH_Y,
                         SPRITE_SWITCH, "down",
                         [evk("a5/switch/actor/interact", "EVENT_CALL_CUSTOM_EVENT",
                              dict({"customEventId": S_SWITCH_TOGGLE, "__name": "Toggle Switch"}, **sw_params))])
    switch_actor["animSpeed"] = 255
    switch_actor["startScript"] = [evk("a5/switch/actor/init", "EVENT_CALL_CUSTOM_EVENT",
                                       {"customEventId": S_SWITCH_INIT, "__name": "Switch Init", "$actor[0]$": switch_id,
                                        "$variable[V0]$": {"type": "variable", "value": V_SWITCH_ON}})]
    def door_actor(key, idx, name, symbol, x, y, door_id, open_var, locked_script, locked_name):
        a = actor(key, idx, name, symbol, x, y, SPRITE_DOOR, "down",
                  [evk(key + "/interact", "EVENT_CALL_CUSTOM_EVENT", {"customEventId": locked_script, "__name": locked_name})])
        a["animSpeed"] = 255                 # keine Animation; collisionGroup "" -> blockiert den Spieler
        a["startScript"] = [evk(key + "/init", "EVENT_CALL_CUSTOM_EVENT",
                                {"customEventId": S_DOOR_INIT, "__name": "Door Init", "$actor[0]$": door_id,
                                 "$variable[V0]$": {"type": "variable", "value": open_var}})]
        return a
    ws_door = door_actor("actor/village_ws_door", 3, "Workshop Door", "actor_workshop_door", WS_DOOR_X, WS_DOOR_Y,
                         ws_door_id, V_SWITCH_ON, S_DOOR_LOCKED_WS, "Locked Workshop Door")
    house_door = door_actor("actor/village_house_door", 4, "House Door", "actor_house_door", HOUSE_DOOR_X, HOUSE_DOOR_Y,
                            house_door_id, V_KEY_TAKEN, S_DOOR_LOCKED_HOUSE, "Locked House Door")
    scene(SC_VILLAGE, 2, "Village", "scene_village", "village", 540, 60, "village", vc,
          [coin_debug_key("village"), inventory_key("village")],
          actors=[actor("actor/village_elder", 0, "Elder", "actor_village_elder", 10, 11, SPRITE_ELDER, "down",
                        [call(S_ELDER, "Talk Elder", {"$actor[0]$": elder_id})]), guard_actor,
                  switch_actor, ws_door, house_door] + item_actors("village", 5),
          triggers=[trigger("trigger/village_exit", 0, "To Forest", "trigger_to_forest", 0, 8, 1, 2,
                            [call(S_TO_FOREST, "Warp To Forest")]),
                    # A4: Tuerfeld (2x1) genau auf den begehbaren Tuer-Tiles
                    trigger("trigger/village_house_door", 1, "To House", "trigger_to_house",
                            HOUSE_DOOR_X, HOUSE_DOOR_Y, 2, 1,
                            [evk("house/door/call", "EVENT_CALL_CUSTOM_EVENT",
                                 {"customEventId": S_TO_HOUSE, "__name": "Warp To House"})]),
                    # A5: Werkstatt-Tuer (2x1) genau auf der Tueroeffnung; nur erreichbar, wenn Tuer-Actor deaktiviert
                    trigger("trigger/village_ws_door", 2, "To Workshop", "trigger_to_workshop",
                            WS_DOOR_X, WS_DOOR_Y, 2, 1,
                            [evk("a5/ws_door/call", "EVENT_CALL_CUSTOM_EVENT",
                                 {"customEventId": S_TO_WS, "__name": "Warp To Workshop"})])])
    # A4: neue Szene "House" (Hausinneres)
    scene(SC_HOUSE, 3, "House", "scene_house", "house", 780, 60, "house", house.collisions(),
          [coin_debug_key("house"), inventory_key("house")], actors=item_actors("house", 0),
          triggers=[trigger("trigger/house_exit", 0, "Exit House", "trigger_exit_house", EXIT_X, EXIT_Y, 2, 1,
                            [evk("house/exit/call", "EVENT_CALL_CUSTOM_EVENT",
                                 {"customEventId": S_HOUSE_TO_VILLAGE, "__name": "Warp House To Village"})])])

def build_scene_workshop():
    # A5.6: neue Szene "Workshop" (Ziel der Schalter-Tuer) mit Rueckweg
    scene(SC_WORKSHOP, 4, "Workshop", "scene_workshop", "workshop", 1020, 60, "workshop", workshop.collisions(),
          [coin_debug_key("workshop"), inventory_key("workshop")], actors=item_actors("workshop", 0),
          triggers=[trigger("trigger/workshop_exit", 0, "Exit Workshop", "trigger_exit_workshop", WS_EXIT_X, WS_EXIT_Y, 2, 1,
                            [evk("a5/ws_exit/call", "EVENT_CALL_CUSTOM_EVENT",
                                 {"customEventId": S_WS_TO_VILLAGE, "__name": "Warp Workshop To Village"})])])

def build_project_settings():
    p = f"{ROOT}/project/settings.gbsres"; s = json.load(open(p))
    s.update({"startSceneId": SC_TITLE, "startX": 9, "startY": 9, "startDirection": "down",
              "startMoveSpeed": 1, "startAnimSpeed": 15, "defaultSceneTypeId": "TOPDOWN"})
    s["defaultPlayerSprites"] = {k: SPRITE_HERO for k in s["defaultPlayerSprites"]}
    # Tastatur-Belegung: NUR Pfeiltasten = Bewegung, Taste A = A-Knopf (Interaktion), Taste B = B-Knopf (Inventar).
    # Vorher lag "a" auf LINKS (WASD) und A/B auf Alt/z/j bzw. Strg/k/x -> Taste A lief nach links.
    # Grossbuchstaben zusaetzlich, damit es auch mit Feststelltaste / gedrueckter Shift-Taste (= Select) geht.
    s.update({"customControlsUp": ["ArrowUp"], "customControlsDown": ["ArrowDown"],
              "customControlsLeft": ["ArrowLeft"], "customControlsRight": ["ArrowRight"],
              "customControlsA": ["a", "A"], "customControlsB": ["b", "B"],
              "customControlsStart": ["Enter"], "customControlsSelect": ["Shift"]})
    wjson("project/settings.gbsres", s)
    wjson("project/variables.gbsres", {"_resourceType":"variables","variables":[
        {"id":V_MET_ELDER,"name":"MetElder","symbol":"var_met_elder"},
        {"id":V_READ_SIGN,"name":"ReadForestSign","symbol":"var_read_forest_sign"},
        {"id":V_VISITED,"name":"VisitedVillage","symbol":"var_visited_village"},
        {"id":V_TITLE_CHOICE,"name":"TitleChoice","symbol":"var_title_choice"},
        {"id":V_CHEST_OPENED,"name":"ChestOpened","symbol":"var_chest_opened"},
        {"id":V_COIN_COUNT,"name":"CoinCount","symbol":"var_coin_count"},
        *[{"id":v,"name":f"Coin{i+1}Taken","symbol":f"var_coin{i+1}_taken"} for i, v in enumerate(V_COIN_TAKEN)],
        {"id":V_SWITCH_ON,"name":"SwitchOn","symbol":"var_switch_on"},          # A5
        {"id":V_KEY_TAKEN,"name":"KeyTaken","symbol":"var_key_taken"},          # A5R
        {"id":V_MUSHROOM_COUNT,"name":"MushroomCount","symbol":"var_mushroom_count"},   # A6
        *[{"id":v,"name":f"Mushroom{i+1}Taken","symbol":f"var_mushroom{i+1}_taken"} for i, v in enumerate(V_MUSHROOM_TAKEN)],
        {"id":V_APPLE_COUNT,"name":"AppleCount","symbol":"var_apple_count"},
        {"id":V_APPLE_TAKEN[0],"name":"AppleTaken","symbol":"var_apple_taken"},
        {"id":V_GEM_COUNT,"name":"GemCount","symbol":"var_gem_count"},
        {"id":V_GEM_TAKEN[0],"name":"GemTaken","symbol":"var_gem_taken"},
        *[{"id":i,"name":n,"symbol":"var_"+"".join("_"+ch.lower() if ch.isupper() else ch for ch in n).lstrip("_")}
          for i, n in A7_VARS]],                                                         # A7
        "constants":[]})

if __name__ == "__main__":
    build_assets(); build_scripts(); build_scenes(); build_scene_workshop(); build_project_settings()
    # Kollisions-Selbsttest: Spawnpunkte / Trigger muessen begehbar sein
    def free(m, x, y): return m.collisions()[y*20+x] == 0
    # A1: Truhe muss von oben/unten/links/rechts erreichbar sein
    for p in [(CHEST_X,CHEST_Y+1),(CHEST_X,CHEST_Y-2),(CHEST_X-1,CHEST_Y),(CHEST_X+2,CHEST_Y)]:
        assert forest.collisions()[p[1]*20+p[0]] == 0, ("Truhe nicht erreichbar", p)
    for (m,pts) in [(forest,[(3,9),(4,9),(16,9),(17,9),(18,9),(19,9),(6,8),(7,8)]),
                    (village,[(0,9),(1,9),(2,9),(3,9),(10,9),(11,9)])]:
        for p in pts: assert free(m,*p), p
    # A2: Waechter darf Eingang/Weg nicht blockieren und muss von vorn, der Seite und hinten erreichbar sein
    vcol = village.collisions()
    for dx in (0, 1):
        for dy in (0, -1): vcol[(GUARD_Y+dy)*20 + GUARD_X+dx] = SOLID
    for p in [(0,8),(0,9),(1,8),(1,9),(2,9),(3,9),(2,8),(3,8)]:          # Eingang + Weg + Spawn bleiben frei (A2.1)
        assert vcol[p[1]*20+p[0]] == 0, ("Eingang blockiert", p)
    for p in [(GUARD_X,GUARD_Y-2),(GUARD_X+1,GUARD_Y-2),                 # hinten (oben, auf dem Weg)
              (GUARD_X+2,GUARD_Y),(GUARD_X+3,GUARD_Y),                   # Seite (rechts)
              (GUARD_X,GUARD_Y+1),(GUARD_X+1,GUARD_Y+1)]:                # vorn (unten)
        assert vcol[p[1]*20+p[0]] == 0, ("Waechter nicht erreichbar", p)
    # A3: Muenzen liegen auf freien Feldern, nicht auf Spawn/Trigger/anderen Actors, und sind erreichbar
    assert len(COIN_POS) >= 3                                               # A3.1
    fcol = forest.collisions()
    for dx in (0, 1):
        for dy in (0, -1): fcol[(CHEST_Y+dy)*20 + CHEST_X+dx] = SOLID
    blocked = {(CHEST_X+dx, CHEST_Y+dy) for dx in (0,1) for dy in (0,-1)} | {(6+dx, 7+dy) for dx in (0,1) for dy in (0,-1)}
    for (x, y) in COIN_POS:
        for dx in (0, 1):
            assert fcol[y*20+x+dx] == 0, ("Muenze auf massivem Tile", x, y)
            assert (x+dx, y) not in blocked, ("Muenze ueberlappt Actor", x, y)
        assert y not in (8, 9) or x < 17, ("Muenze am Ausgang", x, y)
    # Erreichbarkeit: Spieler (16x8, 8px-Raster) vom Spawn (3,9) aus per Breitensuche
    def walk(x, y): return all(0 <= x+dx < 20 and 0 <= y < 18 and fcol[y*20+x+dx] == 0 for dx in (0, 1))
    seen, todo = {(3, 9)}, [(3, 9)]
    while todo:
        cx, cy = todo.pop()
        for nx, ny in ((cx+1,cy),(cx-1,cy),(cx,cy+1),(cx,cy-1)):
            if (nx, ny) not in seen and walk(nx, ny): seen.add((nx, ny)); todo.append((nx, ny))
    for (x, y) in COIN_POS: assert (x, y) in seen, ("Muenze nicht erreichbar", x, y)
    # A4: Selbsttest Tuer/Teleporter
    def bfs(col, start):
        def ok(x, y): return all(0 <= x+dx < 20 and 0 <= y < 18 and col[y*20+x+dx] == 0 for dx in (0, 1))
        assert ok(*start), ("Spawn blockiert", start)
        seen, todo = {start}, [start]
        while todo:
            cx, cy = todo.pop()
            for nx, ny in ((cx+1,cy),(cx-1,cy),(cx,cy+1),(cx,cy-1)):
                if (nx, ny) not in seen and ok(nx, ny): seen.add((nx, ny)); todo.append((nx, ny))
        return seen
    def touches(px, py, tx, ty, tw, th):   # Spieler belegt (px..px+1, py)
        return any(tx <= px+dx < tx+tw and ty <= py < ty+th for dx in (0, 1))
    hcol = house.collisions()
    hreach = bfs(hcol, HOUSE_SPAWN[:2])                                     # A4.1 begehbar
    assert len(hreach) > 100, len(hreach)
    for p in [(0,10),(19,10),(5,2),(10,0),(5,9),(15,5),(8,17),(11,17)]:     # A4.1 Wand-/Moebelkollision
        assert hcol[p[1]*20+p[0]] == SOLID, ("nicht massiv", p)
    assert not touches(*HOUSE_SPAWN[:2], EXIT_X, EXIT_Y, 2, 1)              # A4.3 nicht auf Rueckkehrobjekt
    assert (EXIT_X, EXIT_Y) in hreach                                       # A4.4 Rueckkehr erreichbar
    assert [p for p in hreach if p[1] == EXIT_Y] == [(EXIT_X, EXIT_Y)]       # nur genau auf der Matte
    vcol2 = list(vcol)
    vreach = bfs(vcol2, VILLAGE_SPAWN_FROM_HOUSE[:2])
    assert not touches(*VILLAGE_SPAWN_FROM_HOUSE[:2], HOUSE_DOOR_X, HOUSE_DOOR_Y, 2, 1)   # A4.4
    assert (HOUSE_DOOR_X, HOUSE_DOOR_Y) in vreach and (2, 9) in vreach      # Tuer + Dorfeingang erreichbar
    door_cells = [p for p in vreach if touches(*p, HOUSE_DOOR_X, HOUSE_DOOR_Y, 2, 1)]
    assert door_cells == [(HOUSE_DOOR_X, HOUSE_DOOR_Y)], door_cells          # A4.2 nur direkt auf der Tuer
    # ------------------------------------------------ A5 / A5R Selbsttest
    va = village.collisions()
    for (ax, ay) in [(GUARD_X, GUARD_Y), (SWITCH_X, SWITCH_Y)]:              # Waechter + Schalter massiv (2x2)
        for dx in (0, 1):
            for dy in (0, -1): va[(ay+dy)*20 + ax+dx] = SOLID
    for (dx_, dy_) in [(WS_DOOR_X, WS_DOOR_Y), (WS_DOOR_X+1, WS_DOOR_Y), (HOUSE_DOOR_X, HOUSE_DOOR_Y), (HOUSE_DOOR_X+1, HOUSE_DOOR_Y)]:
        assert va[dy_*20+dx_] == 0, ("Tueroeffnung muss im Hintergrund begehbar sein", dx_, dy_)
    def with_doors(ws_open, house_open):                                     # Tuer-Actor (16x8) blockiert wie massiv
        col = list(va)
        for open_, (x0, y0) in [(ws_open, (WS_DOOR_X, WS_DOOR_Y)), (house_open, (HOUSE_DOOR_X, HOUSE_DOOR_Y))]:
            if not open_: col[y0*20+x0] = col[y0*20+x0+1] = SOLID
        return col
    for ws_open in (False, True):
        for house_open in (False, True):
            r = bfs(with_doors(ws_open, house_open), (2, 9))                 # Start: Dorfeingang vom Wald
            ws_cells = [p for p in r if touches(*p, WS_DOOR_X, WS_DOOR_Y, 2, 1)]
            hs_cells = [p for p in r if touches(*p, HOUSE_DOOR_X, HOUSE_DOOR_Y, 2, 1)]
            assert ws_cells == ([(WS_DOOR_X, WS_DOOR_Y)] if ws_open else []), ("A5.2/A5.6", ws_open, ws_cells)
            assert hs_cells == ([(HOUSE_DOOR_X, HOUSE_DOOR_Y)] if house_open else []), ("A5R.2/A5R.4", house_open, hs_cells)
            for need in [(SWITCH_X-2, SWITCH_Y), (SWITCH_X, SWITCH_Y+1), (WS_DOOR_X, WS_DOOR_Y+1),
                         (HOUSE_DOOR_X, HOUSE_DOOR_Y+1), (0, 9), VILLAGE_SPAWN_FROM_WS[:2],
                         VILLAGE_SPAWN_FROM_HOUSE[:2], (10, 12), (12, 15)]:
                assert need in r, ("Dorf: Feld nicht erreichbar", need, ws_open, house_open)
    assert not touches(*VILLAGE_SPAWN_FROM_WS[:2], WS_DOOR_X, WS_DOOR_Y, 2, 1)          # A5.6 nicht auf dem Trigger
    assert not touches(*VILLAGE_SPAWN_FROM_WS[:2], SWITCH_X, SWITCH_Y-1, 2, 2)
    assert not touches(*VILLAGE_SPAWN_FROM_WS[:2], WS_DOOR_X, WS_DOOR_Y, 2, 1)
    wcol = workshop.collisions()
    wreach = bfs(wcol, WS_SPAWN[:2])
    assert len(wreach) > 100, len(wreach)
    assert not touches(*WS_SPAWN[:2], WS_EXIT_X, WS_EXIT_Y, 2, 1)                     # A5.6 Rueckweg
    assert [p for p in wreach if p[1] == WS_EXIT_Y] == [(WS_EXIT_X, WS_EXIT_Y)]
    print("BG workshop unique tiles:", unique_tiles(workshop.image()))
    # A5R.1: Schluessel auf freiem, erreichbarem Feld; keine Ueberlappung mit Muenzen / Truhe / Schild / Weg-Ausgang
    for dx in (0, 1):
        assert fcol[KEY_Y*20+KEY_X+dx] == 0 and (KEY_X+dx, KEY_Y) not in blocked
        for (cx, cy) in COIN_POS: assert not (cy == KEY_Y and abs(cx - KEY_X) < 2), "Schluessel auf Muenze"
    assert (KEY_X, KEY_Y) in seen, "Schluessel nicht erreichbar"
    for name in ["SWITCH_OFF", "SWITCH_ON", "DOOR", "KEY"]:
        rows = globals()[name].split(); assert len(rows) == 16 and all(len(r) == 16 for r in rows), name
    # ------------------------------------------------ A6 Selbsttest
    maps = {"forest": fcol, "village": va, "house": hcol, "workshop": wcol}
    starts = {"forest": (3, 9), "village": (2, 9), "house": HOUSE_SPAWN[:2], "workshop": WS_SPAWN[:2]}
    occupied = {"forest": blocked | {(KEY_X+d, KEY_Y) for d in (0, 1)} | {(x+d, y) for x, y in COIN_POS for d in (0, 1)},
                "village": {(ax+dx, ay+dy) for (ax, ay) in [(GUARD_X, GUARD_Y), (SWITCH_X, SWITCH_Y), (10, 11)]
                            for dx in (0, 1) for dy in (0, -1)}, "house": set(), "workshop": set()}
    trig = {"forest": [(19, 8, 1, 2)], "village": [(0, 8, 1, 2), (HOUSE_DOOR_X, HOUSE_DOOR_Y, 2, 1), (WS_DOOR_X, WS_DOOR_Y, 2, 1)],
            "house": [(EXIT_X, EXIT_Y, 2, 1)], "workshop": [(WS_EXIT_X, WS_EXIT_Y, 2, 1)]}
    counts = {}
    for typ, (_, _, taken_vars, positions, _) in ITEM_TYPES.items():
        assert len(positions) == len(taken_vars), typ
        counts[typ] = len(positions)
        for (sk, x, y) in positions:
            col = maps[sk]; reach = bfs(col, starts[sk])
            for d in (0, 1):
                assert col[y*20+x+d] == 0, ("A6.1 Gegenstand auf massivem Tile", typ, sk, x, y)
                assert (x+d, y) not in occupied[sk], ("A6.1 Gegenstand ueberlappt Actor", typ, sk, x, y)
                occupied[sk].add((x+d, y))
            assert (x, y) in reach, ("A6.1 Gegenstand nicht erreichbar", typ, sk, x, y)
            assert not any(touches(x, y, *t) for t in trig[sk]), ("A6.1 Gegenstand auf Trigger", typ, sk, x, y)
            assert (x, y) != starts[sk], ("A6.1 Gegenstand auf Spawn", typ, sk)
    assert len(ITEM_TYPES) >= 3 and max(counts.values()) >= 2, counts                 # A6.1
    import re
    inv_lines = INVENTORY_TEXT.replace("!S0!", "").split("\n")
    worst = [re.sub(r"\$\d\d\$", "000", l) for l in inv_lines]                      # Werte bis 3-stellig
    assert all(INV_TEXT_X + len(l) <= 19 for l in worst), worst                          # nicht in den Rahmen
    assert sum(len(l) for l in worst) <= INV_TILE_BUDGET, sum(len(l) for l in worst)     # A6.4: Kachelpuffer
    assert len(inv_lines) <= 16                                                          # textHeight 16
    for k, v in [("coin", "$05$"), ("key", "$10$"), ("mushroom", "$11$"), ("apple", "$14$"), ("gem", "$16$")]:
        assert any(ICON[k] in l and v in l for l in inv_lines), k                         # A6.4 / A6R.1
    # ------------------------------------------------ A7 Selbsttest
    fcol7 = list(fcol)
    for dx in (0, 1):
        for dy in (0, -1): fcol7[(SIGN_Y+dy)*20 + SIGN_X+dx] = SOLID
    ex, ey = ENEMY_START
    for d in range(4):                                                     # A7.1: Route (x..x+2) + Breite 2 frei
        assert fcol7[ey*20+ex+d] == 0, ("A7.1 Patrouille blockiert", ex+d, ey)
    for (sx, sy) in [(3, 9), (16, 9)]:                                     # Spawns ausserhalb des Radius (+ 2 Felder Puffer)
        assert max(abs(sx-ex), abs(sy-ey)) > ENEMY_RADIUS + 2, ("A7: Gegner zu nah am Spawn", sx, sy)
    r7 = bfs(fcol7, (3, 9))
    assert (ex, ey) in r7 and (ex+2, ey) in r7, "A7: Gegner vom Spieler aus nicht erreichbar"
    for (x, y) in COIN_POS + [(KEY_X, KEY_Y), (3, 11)]:
        assert (x, y) in r7, ("A7: Schild-Kollision sperrt Gegenstand", x, y)
    assert ENEMY_SPEED < 1                                                  # A7.6 (Spieler startMoveSpeed = 1)
    assert [v for v, _ in A7_VARS] == [str(i) for i in range(18, 18+len(A7_VARS))]
    print("OK")
