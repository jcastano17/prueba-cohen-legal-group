"""Print SVG samples for one style (style chosen via GYM_STYLE)."""
import json
import os
import sys
sys.path.insert(0, os.path.dirname(__file__))
import figures as F  # noqa: E402
from exercises import pair_fit, mini_svg  # noqa: E402

F.HIGHLIGHT = {"quads", "glutes"}
a, b = pair_fit("squat", 230, 260)
F.HIGHLIGHT = {"hamstrings", "glutes"}
c, d = pair_fit("rdl", 230, 260)
F.HIGHLIGHT = set()
m = mini_svg("thoracic", 150, 200)
print(json.dumps({"squat": [a, b], "rdl": [c, d], "mini": m}))
