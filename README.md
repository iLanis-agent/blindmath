# Blind math

Window blind sizing arithmetic, no surprises on delivery day. A static site with three calculators:

- **Inside-mount size** - measure the opening in three places; the order width comes from the smallest width minus the maker's clearance deduction, and the order drop from the longest drop. Flags out-of-square openings.
- **Venetian slats** - drop, slat width and overlap become a slat count and the real top-to-bottom coverage.
- **Split a wide span** - a wide window becomes an even split of blinds under a per-blind width limit.

Live site: https://ilanis-agent.github.io/blindmath/

## Labeled norms

These are common trade norms, not manufacturer spec - the UI labels them and your maker's numbers win:

- Clearance deduction defaults to 1 cm (many makers take 0.5-1.5 cm for inside mounts).
- Slat overlap defaults to 0.5 cm.
- Widest single blind defaults to 180 cm (a common roller limit; check your supplier).
- All results round to 0.1 cm.

## Layout

- `engine.js` - pure arithmetic and text rendering, shared by the page and the tests.
- `index.html` - landing page. `app.html` - the calculators.
- `oracle.py` - independent Python mirror of the engine's exact float operations.
- `expected.json` - 50 oracle-generated cases. `test.js` - runs every case against the engine plus render checks.

## Tests

```
python3 oracle.py   # regenerate expected.json
node test.js        # 180 checks, 0 failures
```
