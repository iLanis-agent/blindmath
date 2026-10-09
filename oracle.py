# Blind math oracle - mirrors engine.js float ops exactly (math.floor(x+0.5) == JS Math.round for positive magnitudes).
import math, json

def round1(x):
    return math.floor(x * 10 + 0.5) / 10

def inside_mount(wTop, wMid, wBot, dLeft, dMid, dRight, deduction):
    widths = [wTop, wMid, wBot]; drops = [dLeft, dMid, dRight]
    for w in widths:
        if not (w > 0): return {"error": "widths must be positive"}
    for d in drops:
        if not (d > 0): return {"error": "drops must be positive"}
    if not (deduction >= 0): return {"error": "deduction must not be negative"}
    wMin = min(widths); wMax = max(widths); dMax = max(drops)
    orderWidth = round1(wMin - deduction)
    if not (orderWidth > 0): return {"error": "deduction leaves no width"}
    bow = round1(wMax - wMin)
    square = "square opening" if bow <= 1 else "out of square by %g cm - expect small light gaps at the wide end" % bow
    return {"orderWidth": orderWidth, "orderDrop": round1(dMax), "bow": bow, "square": square}

def slats(drop, slatW, overlap):
    if not (drop > 0): return {"error": "drop must be positive"}
    if not (slatW > 0): return {"error": "slat width must be positive"}
    if not (overlap >= 0): return {"error": "overlap must not be negative"}
    if overlap >= slatW: return {"error": "overlap must be less than slat width"}
    pitch = slatW - overlap
    n = math.ceil(drop / pitch)
    coverage = round1(n * slatW - (n - 1) * overlap)
    return {"count": n, "pitch": round1(pitch), "coverage": coverage}

def split_span(span, maxWidth):
    if not (span > 0): return {"error": "span must be positive"}
    if not (maxWidth > 0): return {"error": "max width must be positive"}
    n = math.ceil(span / maxWidth)
    each = round1(span / n)
    if n == 1: verdict = "one blind does it"
    elif each < 40: verdict = "%d narrow blinds - a valance helps the joins" % n
    else: verdict = "%d blinds, even split" % n
    return {"count": n, "each": each, "verdict": verdict}

cases = []
def im(*a): cases.append({"tool": "inside", "args": list(a), "expect": inside_mount(*a)})
def sl(*a): cases.append({"tool": "slats", "args": list(a), "expect": slats(*a)})
def sp(*a): cases.append({"tool": "split", "args": list(a), "expect": split_span(*a)})

# inside mount: happy paths
im(120.4, 120.0, 120.7, 140, 140.3, 139.8, 1)      # defaults
im(60, 60, 60, 100, 100, 100, 0.5)                 # tiny square window
im(200, 199.2, 201.5, 180, 179.5, 181, 1)          # big, out of square
im(90.5, 91.5, 90.0, 150, 150, 150, 1.5)           # bow exactly 1.5 -> out of square
im(100, 100.9, 100.5, 120, 121, 120.5, 1)          # bow 0.9 -> square
im(45, 45.3, 44.8, 60, 61, 60.5, 0.5)
im(150, 150, 150, 200, 200, 200, 2)
im(80.25, 80.25, 80.25, 90.05, 90.05, 90.05, 0.75) # decimals
im(300, 299, 301, 250, 251, 249, 1.2)              # huge opening
im(100, 102, 101, 100, 100, 100, 0)                # zero deduction
# inside mount: errors
im(-1, 120, 120, 140, 140, 140, 1)                 # negative width
im(120, 0, 120, 140, 140, 140, 1)                  # zero width
im(120, 120, 120, -5, 140, 140, 1)                 # negative drop
im(120, 120, 120, 140, 0, 140, 1)                  # zero drop
im(120, 120, 120, 140, 140, 140, -0.5)             # negative deduction
im(1.0, 1.0, 1.0, 100, 100, 100, 1.0)              # deduction eats all width
im(0.9, 1.1, 1.0, 100, 100, 100, 1.5)              # deduction leaves no width

# slats: happy paths
sl(140, 5, 0.5)                                    # defaults
sl(100, 5, 0.5)
sl(90, 2.5, 0.3)                                   # slim slat
sl(200, 9, 1)                                      # wide slat
sl(4.5, 5, 0.5)                                    # single slat exactly
sl(4.6, 5, 0.5)                                    # spills to 2
sl(150, 6.3, 0)                                    # zero overlap
sl(120, 5, 1.5)
sl(88.8, 4.4, 0.4)
sl(250, 10, 2)
# slats: errors
sl(0, 5, 0.5)                                      # zero drop
sl(-10, 5, 0.5)                                    # negative drop
sl(100, 0, 0.5)                                    # zero slat width
sl(100, 5, -0.1)                                   # negative overlap
sl(100, 5, 5)                                      # overlap == slat width
sl(100, 5, 6)                                      # overlap > slat width

# split: happy paths
sp(300, 180)                                       # defaults
sp(150, 180)                                       # single blind
sp(180, 180)                                       # exactly one
sp(181, 180)                                       # spills to two
sp(600, 180)                                       # 4 blinds (600/180=3.33 -> 4, each 150)
sp(500, 120)                                       # 5 of 100
sp(240, 100)                                       # 3 of 80
sp(95, 30)                                         # 4 of 23.8 -> narrow verdict
sp(123.4, 50.5)                                    # decimals
sp(1000, 250)                                      # 4 of 250
sp(39, 50)                                         # single narrow, still "one blind"
sp(79.9, 40)                                       # 2 of 40 -> even split (not narrow)
sp(79.9, 45)                                       # 2 of 40 -> even
# split: errors
sp(0, 180)
sp(-100, 180)
sp(300, 0)
sp(300, -10)

with open("expected.json", "w") as f:
    json.dump(cases, f, indent=1)
print(len(cases), "cases written")
