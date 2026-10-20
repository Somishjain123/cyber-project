import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

def create_presentation():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_slide_layout = prs.slide_layouts[6]

    # Color Palette: Cyber / Tech Theme
    C_BG = RGBColor(15, 23, 42)          # Deep Slate Navy #0F172A
    C_CARD = RGBColor(30, 41, 59)        # Card background #1E293B
    C_CYAN = RGBColor(56, 189, 248)      # Accent Cyan #38BDF8
    C_TEXT_WHITE = RGBColor(248, 250, 252) # Pure Light #F8FAFC
    C_TEXT_MUTED = RGBColor(148, 163, 184) # Muted Grey #94A3B8
    C_GREEN = RGBColor(74, 222, 128)     # Accent Green #4ADE80
    C_RED = RGBColor(248, 113, 113)      # Accent Coral/Red #F87171

    def add_background(slide):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
        bg.fill.solid()
        bg.fill.fore_color.rgb = C_BG
        bg.line.color.rgb = C_BG
        return bg

    def add_header(slide, title_text, category="CYBERSECURITY & CRYPTOGRAPHY PROJECT"):
        tb = slide.shapes.add_textbox(Inches(0.8), Inches(0.5), Inches(11.7), Inches(1.1))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

        p1 = tf.paragraphs[0]
        p1.text = category.upper()
        p1.font.size = Pt(11)
        p1.font.bold = True
        p1.font.color.rgb = C_CYAN
        p1.font.name = "Arial"

        p2 = tf.add_paragraph()
        p2.text = title_text
        p2.font.size = Pt(24)
        p2.font.bold = True
        p2.font.color.rgb = C_TEXT_WHITE
        p2.font.name = "Arial"
        p2.space_before = Pt(4)

    def add_card(slide, left, top, width, height, title, body_bullets, accent_color=C_CYAN):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        card.fill.solid()
        card.fill.fore_color.rgb = C_CARD
        card.line.color.rgb = RGBColor(51, 65, 85)
        card.line.width = Pt(1)

        tb = slide.shapes.add_textbox(left + Inches(0.3), top + Inches(0.25), width - Inches(0.6), height - Inches(0.5))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

        p_title = tf.paragraphs[0]
        p_title.text = title
        p_title.font.size = Pt(18)
        p_title.font.bold = True
        p_title.font.color.rgb = accent_color
        p_title.font.name = "Arial"

        for b in body_bullets:
            p = tf.add_paragraph()
            p.text = "•  " + b
            p.font.size = Pt(13)
            p.font.color.rgb = C_TEXT_WHITE
            p.font.name = "Arial"
            p.space_before = Pt(8)

    # ---------------- SLIDE 1: TITLE SLIDE ----------------
    s1 = prs.slides.add_slide(blank_slide_layout)
    add_background(s1)

    tb1 = s1.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(11.3), Inches(3.8))
    tf1 = tb1.text_frame
    tf1.word_wrap = True
    
    p = tf1.paragraphs[0]
    p.text = "CYBERSECURITY & CRYPTOGRAPHY"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = C_CYAN
    p.font.name = "Arial"

    p = tf1.add_paragraph()
    p.text = "Classical Ciphers: Attack & Prevention"
    p.font.size = Pt(38)
    p.font.bold = True
    p.font.color.rgb = C_TEXT_WHITE
    p.font.name = "Arial"
    p.space_before = Pt(10)

    p = tf1.add_paragraph()
    p.text = "A Hands-On Demonstration of Caesar & Substitution Ciphers, Vulnerabilities, and Modern Defense Mechanisms"
    p.font.size = Pt(16)
    p.font.color.rgb = C_TEXT_MUTED
    p.font.name = "Arial"
    p.space_before = Pt(14)

    # Meta card at bottom
    meta_card = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.0), Inches(5.4), Inches(11.3), Inches(1.1))
    meta_card.fill.solid()
    meta_card.fill.fore_color.rgb = C_CARD
    meta_card.line.color.rgb = RGBColor(51, 65, 85)

    tb_meta = s1.shapes.add_textbox(Inches(1.3), Inches(5.6), Inches(10.7), Inches(0.8))
    tf_m = tb_meta.text_frame
    p = tf_m.paragraphs[0]
    p.text = "Project By: Somish Jain   |   GitHub: github.com/Somishjain123/cyber-project   |   Stack: Python, Tkinter"
    p.font.size = Pt(13)
    p.font.color.rgb = C_CYAN
    p.font.bold = True
    p.font.name = "Arial"

    # ---------------- SLIDE 2: PROJECT OVERVIEW & MOTIVATION ----------------
    s2 = prs.slides.add_slide(blank_slide_layout)
    add_background(s2)
    add_header(s2, "Project Overview & Core Objectives", "1. INTRODUCTION")

    add_card(s2, Inches(0.8), Inches(1.8), Inches(3.6), Inches(5.0),
             "Background", [
                 "Classical ciphers form the bedrock of cryptographic history.",
                 "Caesar & Substitution ciphers are intuitive but mathematically fragile.",
                 "Understanding how these algorithms break is foundational to mastering modern secure systems."
             ], C_CYAN)

    add_card(s2, Inches(4.8), Inches(1.8), Inches(3.6), Inches(5.0),
             "Problem Statement", [
                 "Monolithic shifts and static substitutions leak statistical characteristics.",
                 "Small keyspaces allow trivial brute-force exploitation.",
                 "Letter distribution patterns in human languages allow rapid cryptanalysis without known keys."
             ], C_RED)

    add_card(s2, Inches(8.8), Inches(1.8), Inches(3.7), Inches(5.0),
             "Key Contributions", [
                 "Interactive Python GUI application for live demonstration.",
                 "Implementation of automated brute-force with English scoring.",
                 "Frequency analysis attack engine.",
                 "Multi-shift and hybrid defense architecture to withstand attacks."
             ], C_GREEN)

    # ---------------- SLIDE 3: CLASSICAL CIPHERS EXPLAINED ----------------
    s3 = prs.slides.add_slide(blank_slide_layout)
    add_background(s3)
    add_header(s3, "Classical Ciphers Architecture & Mechanics", "2. THEORETICAL FOUNDATION")

    add_card(s3, Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.0),
             "Caesar Cipher (Shift Cipher)", [
                 "Type: Monoalphabetic substitution cipher.",
                 "Mathematical Rule: E_k(x) = (x + k) mod 26, D_k(y) = (y - k) mod 26.",
                 "Key Space: Extremely small, exactly 25 non-trivial keys.",
                 "Vulnerability: Trivially broken via exhaustive search in seconds.",
                 "Use Case: Historical military communications (Julius Caesar)."
             ], C_CYAN)

    add_card(s3, Inches(6.8), Inches(1.8), Inches(5.7), Inches(5.0),
             "Monoalphabetic Substitution Cipher", [
                 "Type: Arbitrary 1-to-1 mapping of alphabet letters.",
                 "Key Space: 26! ≈ 4.03 × 10^26 possible permutations.",
                 "False Sense of Security: While immune to brute force, it preserves the frequency distribution of the plaintext language.",
                 "Vulnerability: Defeated by Frequency Analysis and n-gram statistical pattern matching."
             ], C_CYAN)

    # ---------------- SLIDE 4: ATTACK VECTORS ----------------
    s4 = prs.slides.add_slide(blank_slide_layout)
    add_background(s4)
    add_header(s4, "Cryptanalysis & Attack Methodologies", "3. ATTACK DEMONSTRATIONS")

    add_card(s4, Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.0),
             "Attack 1: Brute Force Attack", [
                 "Target: Caesar Cipher.",
                 "Mechanism: Iterates through all 25 possible shift keys in milliseconds.",
                 "English Frequency Scoring: Applies chi-square / standard English letter scoring (ETAOIN SHRDLU).",
                 "Automated Ranking: Automatically surfaces the most probable plaintext to the analyst without human inspection."
             ], C_RED)

    add_card(s4, Inches(6.8), Inches(1.8), Inches(5.7), Inches(5.0),
             "Attack 2: Frequency Analysis Attack", [
                 "Target: Substitution Cipher.",
                 "Mechanism: Analyzes character occurrences in the ciphertext.",
                 "Statistical Rule: In English, 'E' (~12.7%), 'T' (~9.1%), and 'A' (~8.2%) dominate.",
                 "Result: High-frequency ciphertext characters correlate directly to high-frequency alphabet letters, exposing the substitution key."
             ], C_RED)

    # ---------------- SLIDE 5: APPLICATION GUI & IMPLEMENTATION ----------------
    s5 = prs.slides.add_slide(blank_slide_layout)
    add_background(s5)
    add_header(s5, "Software Architecture & Desktop GUI", "4. IMPLEMENTATION")

    # Left: Details
    add_card(s5, Inches(0.8), Inches(1.8), Inches(5.0), Inches(5.0),
             "System Design", [
                 "Built with Python & Tkinter for a responsive, cross-platform interface.",
                 "cipher_logic.py: Decoupled cryptographic core containing pure algorithms and testable logic.",
                 "main.py: GUI driver with interactive tabs, status bars, and real-time computation.",
                 "Modular tabs: Caesar, Substitution, Attacks, and Defenses.",
                 "Includes test suites in test_logic.py validating 100% of cipher logic."
             ], C_CYAN)

    # Right: Screenshot
    img_path = r"e:\cyber project\screenshots\main_gui.png"
    if os.path.exists(img_path):
        s5.shapes.add_picture(img_path, Inches(6.1), Inches(1.8), width=Inches(6.4))

    # ---------------- SLIDE 6: ATTACK IN ACTION (SCREENSHOTS) ----------------
    s6 = prs.slides.add_slide(blank_slide_layout)
    add_background(s6)
    add_header(s6, "Live Cryptanalysis: Brute Force & Frequency Analysis", "5. ATTACK SIMULATION")

    img_bf = r"e:\cyber project\screenshots\brute_force.png"
    if os.path.exists(img_bf):
        s6.shapes.add_picture(img_bf, Inches(0.8), Inches(1.8), width=Inches(5.6))

    img_fa = r"e:\cyber project\screenshots\frequency_analysis.png"
    if os.path.exists(img_fa):
        s6.shapes.add_picture(img_fa, Inches(6.8), Inches(1.8), width=Inches(5.7))

    # ---------------- SLIDE 7: PREVENTION & HARDENING ----------------
    s7 = prs.slides.add_slide(blank_slide_layout)
    add_background(s7)
    add_header(s7, "Countermeasures & Defense Mechanisms", "6. PREVENTION STRATEGIES")

    add_card(s7, Inches(0.8), Inches(1.8), Inches(5.0), Inches(5.0),
             "Multi-Shift & Hybrid Defenses", [
                 "Multi-Shift (Polyalphabetic): Uses an array of shift keys repeating cyclically across the message (Vigenère principle).",
                 "Flattening Frequencies: Identical plaintext characters encrypt to different ciphertext characters, neutralizing single-character frequency analysis.",
                 "Hybrid Layering: Combines Caesar shift with full substitution mapping.",
                 "Result: Thwarts both single-shift brute force and direct frequency matching."
             ], C_GREEN)

    img_def = r"e:\cyber project\screenshots\multi_shift_hybrid.png"
    if os.path.exists(img_def):
        s7.shapes.add_picture(img_def, Inches(6.1), Inches(1.8), width=Inches(6.4))

    # ---------------- SLIDE 8: RESULTS & COMPARISON ----------------
    s8 = prs.slides.add_slide(blank_slide_layout)
    add_background(s8)
    add_header(s8, "Comparative Security Matrix & Experimental Findings", "7. ANALYSIS")

    # Table
    table_shape = s8.shapes.add_table(5, 4, Inches(0.8), Inches(1.8), Inches(11.7), Inches(4.5))
    table = table_shape.table

    # Column widths
    table.columns[0].width = Inches(2.6)
    table.columns[1].width = Inches(3.0)
    table.columns[2].width = Inches(3.0)
    table.columns[3].width = Inches(3.1)

    headers = ["Encryption Method", "Key Space Complexity", "Vulnerability Level", "Defense Efficacy"]
    data = [
        ["Caesar Cipher", "25 Keys", "Critical (Brute Force in <1ms)", "Low - Not secure for real data"],
        ["Substitution Cipher", "26! (~4 × 10^26)", "High (Vulnerable to Frequency Analysis)", "Moderate - Easily cracked with text samples"],
        ["Multi-Shift Cipher", "26^L (L = Key Length)", "Low against simple Caesar brute force", "High - Flattens single-letter frequencies"],
        ["Hybrid (Caesar + Sub)", "Layered Complexity", "Very Low against basic classical attacks", "Maximum - Multi-layer obfuscation"]
    ]

    for col_idx, h in enumerate(headers):
        cell = table.cell(0, col_idx)
        cell.fill.solid()
        cell.fill.fore_color.rgb = RGBColor(51, 65, 85)
        p = cell.text_frame.paragraphs[0]
        p.text = h
        p.font.bold = True
        p.font.size = Pt(13)
        p.font.color.rgb = C_CYAN
        p.font.name = "Arial"

    for row_idx, row in enumerate(data):
        for col_idx, val in enumerate(row):
            cell = table.cell(row_idx + 1, col_idx)
            cell.fill.solid()
            cell.fill.fore_color.rgb = C_CARD if row_idx % 2 == 0 else RGBColor(22, 32, 48)
            p = cell.text_frame.paragraphs[0]
            p.text = val
            p.font.size = Pt(12)
            p.font.color.rgb = C_TEXT_WHITE
            p.font.name = "Arial"

    # ---------------- SLIDE 9: CONCLUSION & FUTURE WORK ----------------
    s9 = prs.slides.add_slide(blank_slide_layout)
    add_background(s9)
    add_header(s9, "Conclusion & Future Directions", "8. CONCLUSION")

    add_card(s9, Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.0),
             "Key Takeaways", [
                 "Security through obscurity fails: Large key spaces alone do not guarantee security if statistical properties leak.",
                 "Frequency analysis easily breaks monoalphabetic substitution despite massive 26! possibilities.",
                 "Polyalphabetic and hybrid approaches bridge the gap towards modern block and stream ciphers (such as AES).",
                 "Demonstrated full lifecycle: Implementation → Vulnerability Analysis → Exploitation → Mitigation."
             ], C_CYAN)

    add_card(s9, Inches(6.8), Inches(1.8), Inches(5.7), Inches(5.0),
             "Future Enhancements", [
                 "Automated Bigram and Trigram frequency substitution solver.",
                 "Kasiski examination module for multi-shift period detection.",
                 "Integration of modern symmetric (AES) and asymmetric (RSA) algorithms.",
                 "Web-based interactive sandbox version using FastAPI and React."
             ], C_CYAN)

    # ---------------- SLIDE 10: THANK YOU ----------------
    s10 = prs.slides.add_slide(blank_slide_layout)
    add_background(s10)

    tb10 = s10.shapes.add_textbox(Inches(1.5), Inches(2.2), Inches(10.3), Inches(3.5))
    tf10 = tb10.text_frame
    tf10.word_wrap = True

    p = tf10.paragraphs[0]
    p.text = "Thank You!"
    p.font.size = Pt(44)
    p.font.bold = True
    p.font.color.rgb = C_CYAN
    p.font.name = "Arial"
    p.alignment = PP_ALIGN.CENTER

    p = tf10.add_paragraph()
    p.text = "Questions & Discussion"
    p.font.size = Pt(22)
    p.font.color.rgb = C_TEXT_WHITE
    p.font.name = "Arial"
    p.space_before = Pt(10)
    p.alignment = PP_ALIGN.CENTER

    p = tf10.add_paragraph()
    p.text = "GitHub Repository: https://github.com/Somishjain123/cyber-project"
    p.font.size = Pt(15)
    p.font.color.rgb = C_TEXT_MUTED
    p.font.name = "Arial"
    p.space_before = Pt(24)
    p.alignment = PP_ALIGN.CENTER

    out_path = r"e:\cyber project\Classical_Ciphers_Presentation.pptx"
    prs.save(out_path)
    print(f"Presentation saved successfully to: {out_path}")

if __name__ == "__main__":
    create_presentation()
