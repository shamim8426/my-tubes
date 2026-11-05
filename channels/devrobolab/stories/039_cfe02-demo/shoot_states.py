import sys
from pathlib import Path
from playwright.sync_api import sync_playwright
H = Path(__file__).parent
S = [("a_sidebar", dict(page="projects", sideHl=True, cx=150, cy=205)),
     ("b_modal", dict(page="projects", modal=True, f="d", name="Class 12 notes", desc="Physics and maths chapters", createHl=False, btnHl=False, cx=860, cy=620)),
     ("c_project", dict(page="project", name="Class 12 notes", files=["physics_ch1.pdf", "maths_formulas.txt"], plusHl=False, insHl=True, ins="Explain in simple Hinglish, with one example.", cx=1180, cy=420))]
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={"width": 1500, "height": 1100}); pg.goto((H / "ui.html").as_uri())
    for n, st in S:
        pg.evaluate("(s)=>ui(s)", st); pg.screenshot(path=str(H / f"state_{n}.png"))
    b.close()
