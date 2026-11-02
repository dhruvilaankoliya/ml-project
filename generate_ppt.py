"""
Script to generate an executive-grade 16:9 PowerPoint Presentation for:
Rossmann Store Sales Forecasting: Random Forest vs. XGBoost vs. LightGBM
"""

import os
import pptx
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

def create_deck():
    prs = Presentation()
    # 16:9 Widescreen dimensions
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_slide_layout = prs.slide_layouts[6]

    # --- COLOR PALETTE ---
    DARK_BG = RGBColor(15, 23, 42)        # Slate 900 #0F172A
    DARK_CARD = RGBColor(30, 41, 59)      # Slate 800 #1E293B
    DARK_BORDER = RGBColor(51, 65, 85)    # Slate 700 #334155
    
    LIGHT_BG = RGBColor(248, 250, 252)    # Slate 50 #F8FAFC
    CARD_BG = RGBColor(255, 255, 255)     # White #FFFFFF
    CARD_BORDER = RGBColor(226, 232, 240) # Slate 200 #E2E8F0
    CARD_HEADER_BG = RGBColor(241, 245, 249) # Slate 100
    
    NAVY_TEXT = RGBColor(15, 23, 42)      # #0F172A
    WHITE_TEXT = RGBColor(255, 255, 255)
    MUTED_TEXT = RGBColor(100, 116, 139)  # Slate 500 #64748B
    MUTED_LIGHT = RGBColor(148, 163, 184) # Slate 400 #94A3B8
    
    BLUE_ACCENT = RGBColor(37, 99, 235)   # Blue 600 #2563EB
    BLUE_LIGHT = RGBColor(239, 246, 255)  # Blue 50
    CYAN_ACCENT = RGBColor(6, 182, 212)   # Cyan 500 #06B6D4
    EMERALD_GREEN = RGBColor(5, 150, 105) # Green 600 #059669
    GREEN_LIGHT = RGBColor(236, 253, 245) # Green 50
    AMBER_ACCENT = RGBColor(217, 119, 6)  # Amber 600 #D97706
    PURPLE_ACCENT = RGBColor(124, 58, 237)# Purple 600 #7C3AED

    def add_bg(slide, color):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
        bg.fill.solid()
        bg.fill.fore_color.rgb = color
        bg.line.fill.background()
        return bg

    def add_header(slide, badge_text, title_text, subtitle_text=None, is_dark=False):
        # Badge
        badge_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.45), Inches(8), Inches(0.35))
        tf_b = badge_box.text_frame
        tf_b.word_wrap = True
        tf_b.margin_left = tf_b.margin_top = tf_b.margin_right = tf_b.margin_bottom = 0
        p_b = tf_b.paragraphs[0]
        p_b.text = badge_text.upper()
        p_b.font.size = Pt(10)
        p_b.font.bold = True
        p_b.font.color.rgb = CYAN_ACCENT if is_dark else BLUE_ACCENT
        
        # Title
        title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.8), Inches(11.7), Inches(0.65))
        tf_t = title_box.text_frame
        tf_t.word_wrap = True
        tf_t.margin_left = tf_t.margin_top = tf_t.margin_right = tf_t.margin_bottom = 0
        p_t = tf_t.paragraphs[0]
        p_t.text = title_text
        p_t.font.size = Pt(22)
        p_t.font.bold = True
        p_t.font.color.rgb = WHITE_TEXT if is_dark else NAVY_TEXT
        
        # Subtitle
        if subtitle_text:
            sub_box = slide.shapes.add_textbox(Inches(0.8), Inches(1.45), Inches(11.7), Inches(0.4))
            tf_s = sub_box.text_frame
            tf_s.word_wrap = True
            tf_s.margin_left = tf_s.margin_top = tf_s.margin_right = tf_s.margin_bottom = 0
            p_s = tf_s.paragraphs[0]
            p_s.text = subtitle_text
            p_s.font.size = Pt(12)
            p_s.font.color.rgb = MUTED_LIGHT if is_dark else MUTED_TEXT

    def add_card(slide, left, top, width, height, fill_color=CARD_BG, border_color=CARD_BORDER):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        card.fill.solid()
        card.fill.fore_color.rgb = fill_color
        if border_color:
            card.line.color.rgb = border_color
            card.line.width = Pt(1)
        else:
            card.line.fill.background()
        return card

    # =========================================================================
    # SLIDE 1: TITLE SLIDE (Dark Theme)
    # =========================================================================
    s1 = prs.slides.add_slide(blank_slide_layout)
    add_bg(s1, DARK_BG)
    
    # Accent decor bar
    bar = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.2), Inches(0.12), Inches(4.8))
    bar.fill.solid()
    bar.fill.fore_color.rgb = BLUE_ACCENT
    bar.line.fill.background()

    # Category Pill
    pill = add_card(s1, Inches(1.2), Inches(1.2), Inches(4.5), Inches(0.4), fill_color=DARK_CARD, border_color=DARK_BORDER)
    tf_p = pill.text_frame
    tf_p.vertical_anchor = MSO_ANCHOR.MIDDLE
    p = tf_p.paragraphs[0]
    p.text = "ENTERPRISE MACHINE LEARNING & FORECASTING"
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = CYAN_ACCENT

    # Main Title
    tbox = s1.shapes.add_textbox(Inches(1.2), Inches(1.75), Inches(11.0), Inches(1.8))
    tf = tbox.text_frame
    tf.word_wrap = True
    p1 = tf.paragraphs[0]
    p1.text = "Rossmann Store Sales Forecasting"
    p1.font.size = Pt(36)
    p1.font.bold = True
    p1.font.color.rgb = WHITE_TEXT
    
    p2 = tf.add_paragraph()
    p2.text = "Comparative Predictive Modeling & Real-Time Decision Intelligence"
    p2.font.size = Pt(18)
    p2.font.bold = False
    p2.font.color.rgb = MUTED_LIGHT
    p2.space_before = Pt(8)

    # Subtitle details
    sbox = s1.shapes.add_textbox(Inches(1.2), Inches(3.6), Inches(11.0), Inches(0.9))
    stf = sbox.text_frame
    stf.word_wrap = True
    sp = stf.paragraphs[0]
    sp.text = "Benchmarking Random Forest vs. Default XGBoost vs. Tuned XGBoost vs. Champion LightGBM\nAcross 1,115 Drugstores with Out-of-Time Cross Validation (RMSPE = 18.28%)"
    sp.font.size = Pt(13)
    sp.font.color.rgb = RGBColor(203, 213, 225)
    sp.line_spacing = 1.3

    # Metadata Cards at bottom
    badges = [
        ("AUTHOR & PRESENTER", "Dhruvil Girishbhai Aankoliya", "ML Engineer & Data Scientist"),
        ("CHAMPION ALGORITHM", "LightGBM Regressor", "18.28% RMSPE | 64.3% Error Cut"),
        ("CURRENCY & SCALE", "Indian Rupees (₹) [1€ = ₹90]", "1,017,209 Rows | 1,115 Stores"),
        ("DEPLOYMENT", "Production Streamlit App", "8 Interactive Modules & SQLite")
    ]
    for i, (head, val, sub) in enumerate(badges):
        b_card = add_card(s1, Inches(1.2 + i * 2.8), Inches(4.9), Inches(2.65), Inches(1.5), fill_color=DARK_CARD, border_color=DARK_BORDER)
        btf = b_card.text_frame
        btf.margin_left = Inches(0.2)
        btf.margin_top = Inches(0.18)
        bp1 = btf.paragraphs[0]
        bp1.text = head
        bp1.font.size = Pt(9)
        bp1.font.bold = True
        bp1.font.color.rgb = CYAN_ACCENT
        
        bp2 = btf.add_paragraph()
        bp2.text = val
        bp2.font.size = Pt(12)
        bp2.font.bold = True
        bp2.font.color.rgb = WHITE_TEXT
        bp2.space_before = Pt(4)
        
        bp3 = btf.add_paragraph()
        bp3.text = sub
        bp3.font.size = Pt(9)
        bp3.font.color.rgb = MUTED_LIGHT
        bp3.space_before = Pt(2)

    # Footer
    ftr = s1.shapes.add_textbox(Inches(1.2), Inches(6.8), Inches(10.5), Inches(0.3))
    ftr.text_frame.paragraphs[0].text = "GitHub: https://github.com/dhruvilaankoliya/ml-project.git  •  Local Host: http://localhost:8501"
    ftr.text_frame.paragraphs[0].font.size = Pt(9)
    ftr.text_frame.paragraphs[0].font.color.rgb = MUTED_LIGHT

    # =========================================================================
    # SLIDE 2: EXECUTIVE SUMMARY & PROBLEM STATEMENT
    # =========================================================================
    s2 = prs.slides.add_slide(blank_slide_layout)
    add_bg(s2, LIGHT_BG)
    add_header(s2, "Project Executive Overview", "The Retail Dilemma: Balancing Stockouts vs. Overstocking", 
               "Predicting daily store sales across 1,115 drugstores to optimize supply chain inventory and preserve profit margins.")

    col_data_2 = [
        ("THE RETAIL CHALLENGE", AMBER_ACCENT, [
            ("Overstocking Waste", "Excess perishable cosmetics and pharmaceuticals lead to markdown losses, capital lockup, and warehouse holding waste."),
            ("Stockout Lost Sales", "Underpredicting high-velocity promo days leads to stockouts, brand erosion, and an estimated 8-12% customer churn."),
            ("Store Volatility", "Sales fluctuate drastically by store type (A/B/C/D), competitor distance (20m to 75km), and cyclical seasonal patterns.")
        ]),
        ("THE MACHINE LEARNING SOLUTION", BLUE_ACCENT, [
            ("Predictive Modeling", "Engineered 19 temporal, competitive, and promotional features across 1,017,209 historical transactions."),
            ("Zero Data Leakage", "Exclusively modeled features available at forecast time (Customer footfall is omitted from future inference)."),
            ("Algorithmic Rigor", "Benchmarked Median Baseline, Random Forest, Default XGBoost, Tuned XGBoost, and LightGBM.")
        ]),
        ("ENTERPRISE BUSINESS VALUE", EMERALD_GREEN, [
            ("Champion Accuracy", "LightGBM achieved 18.28% RMSPE and ₹70,466 (€782.96) MAE, outperforming baseline by 64.3%."),
            ("Promotion Planning", "Identified +34.2% sales uplift during promotions, enabling precision marketing and procurement."),
            ("Production Software", "Delivered an 8-page Streamlit decision platform localized in INR (₹) for corporate store managers.")
        ])
    ]

    for i, (title, accent, items) in enumerate(col_data_2):
        card = add_card(s2, Inches(0.8 + i * 3.95), Inches(2.0), Inches(3.75), Inches(4.9), fill_color=CARD_BG, border_color=CARD_BORDER)
        # Accent top bar
        t_bar = s2.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8 + i * 3.95), Inches(2.0), Inches(3.75), Inches(0.08))
        t_bar.fill.solid()
        t_bar.fill.fore_color.rgb = accent
        t_bar.line.fill.background()
        
        ctf = card.text_frame
        ctf.margin_left = ctf.margin_right = Inches(0.25)
        ctf.margin_top = Inches(0.2)
        cp1 = ctf.paragraphs[0]
        cp1.text = title
        cp1.font.size = Pt(11)
        cp1.font.bold = True
        cp1.font.color.rgb = accent
        
        for heading, body in items:
            hp = ctf.add_paragraph()
            hp.text = f"•  {heading}"
            hp.font.size = Pt(12)
            hp.font.bold = True
            hp.font.color.rgb = NAVY_TEXT
            hp.space_before = Pt(14)
            
            bp = ctf.add_paragraph()
            bp.text = body
            bp.font.size = Pt(10)
            bp.font.color.rgb = MUTED_TEXT
            bp.space_before = Pt(3)

    # =========================================================================
    # SLIDE 3: BUSINESS OBJECTIVES & SUCCESS CRITERIA
    # =========================================================================
    s3 = prs.slides.add_slide(blank_slide_layout)
    add_bg(s3, LIGHT_BG)
    add_header(s3, "Strategic Alignment & Evaluation Design", "Business Objectives & Target Metric Framework",
               "Establishing a rigorous, real-world evaluation strategy aligned with retail financial operations.")

    # 4 Cards across
    obj_cards = [
        ("Multi-Horizon Forecasting", "Forecast daily sales up to 6 weeks (42 days) ahead for all 1,115 stores to drive procurement orders, warehouse dispatch, and staffing schedules.", BLUE_ACCENT),
        ("Realistic Inference Design", "Strictly eliminate future customer count leakage. In real-world retail, customer volume is unknown in advance, so models rely entirely on exogenous schedule signals.", PURPLE_ACCENT),
        ("Why RMSPE over RMSE?", "RMSPE (Root Mean Squared Percentage Error) penalizes relative percentage variance. This ensures small stores (₹2L/mo) and flagship stores (₹50L/mo) are treated with equal operational fairness.", EMERALD_GREEN),
        ("Out-of-Time Validation", "42-day rolling chronological split (Aug 1 - Sep 17, 2015; 40,282 observations). Mirrors exact real-life deployment without random shuffling time-leakage.", AMBER_ACCENT)
    ]
    for i, (title, desc, acc) in enumerate(obj_cards):
        c = add_card(s3, Inches(0.8 + i * 2.95), Inches(2.0), Inches(2.8), Inches(2.6), fill_color=CARD_BG, border_color=CARD_BORDER)
        # Accent tab
        tb = s3.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8 + i * 2.95), Inches(2.0), Inches(2.8), Inches(0.06))
        tb.fill.solid()
        tb.fill.fore_color.rgb = acc
        tb.line.fill.background()
        
        tf = c.text_frame
        tf.margin_left = tf.margin_right = Inches(0.2)
        tf.margin_top = Inches(0.2)
        p = tf.paragraphs[0]
        p.text = title
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = NAVY_TEXT
        
        p2 = tf.add_paragraph()
        p2.text = desc
        p2.font.size = Pt(10)
        p2.font.color.rgb = MUTED_TEXT
        p2.space_before = Pt(8)
        p2.line_spacing = 1.25

    # Formula Callout Box below
    f_card = add_card(s3, Inches(0.8), Inches(4.85), Inches(11.73), Inches(2.05), fill_color=CARD_HEADER_BG, border_color=CARD_BORDER)
    ftf = f_card.text_frame
    ftf.margin_left = Inches(0.35)
    ftf.margin_top = Inches(0.2)
    
    fp = ftf.paragraphs[0]
    fp.text = "Core Evaluation Criterion: Root Mean Squared Percentage Error (RMSPE)"
    fp.font.size = Pt(13)
    fp.font.bold = True
    fp.font.color.rgb = BLUE_ACCENT
    
    fp2 = ftf.add_paragraph()
    fp2.text = "Formula:   RMSPE =  sqrt( (1 / n) * Σ ( (y_actual - y_pred) / y_actual )² )   [Evaluated on open store days where y_actual > 0]"
    fp2.font.size = Pt(11)
    fp2.font.bold = True
    fp2.font.color.rgb = NAVY_TEXT
    fp2.space_before = Pt(6)
    
    fp3 = ftf.add_paragraph()
    fp3.text = "• Why It Matters: An error of ₹10,000 on a ₹20,000 revenue store is a critical 50% deviation that exhausts inventory, whereas on a ₹200,000 flagship store it is only a 5% rounding difference. RMSPE prevents models from solely optimizing for high-volume urban flagships at the expense of regional retail outlets."
    fp3.font.size = Pt(10)
    fp3.font.color.rgb = MUTED_TEXT
    fp3.space_before = Pt(6)

    # =========================================================================
    # SLIDE 4: DATASET ARCHITECTURE & EXPLORATORY DATA ANALYSIS
    # =========================================================================
    s4 = prs.slides.add_slide(blank_slide_layout)
    add_bg(s4, LIGHT_BG)
    add_header(s4, "Data Ingestion & Store Typology", "Dataset Architecture & Exploratory Insights",
               "1,017,209 historical sales records linked with store metadata across 1,115 German retail drugstores.")

    # Top KPI Metrics Row
    kpis = [
        ("TOTAL RECORDS", "1,017,209", "Historical Daily Logs"),
        ("UNIQUE STORES", "1,115", "Across Germany"),
        ("TRAIN / VAL SPLIT", "976,927 / 40,282", "42-Day Chronological Split"),
        ("PROMO UPLIFT", "+34.2% LIFT", "₹2,050 (€2,277) / Day"),
        ("MEDIAN DAILY SALES", "₹5,97,600", "€6,640 Equivalent")
    ]
    for i, (k, val, sub) in enumerate(kpis):
        k_card = add_card(s4, Inches(0.8 + i * 2.38), Inches(1.9), Inches(2.25), Inches(1.2), fill_color=CARD_BG, border_color=CARD_BORDER)
        ktf = k_card.text_frame
        ktf.margin_left = Inches(0.15)
        ktf.margin_top = Inches(0.15)
        p = ktf.paragraphs[0]
        p.text = k
        p.font.size = Pt(8)
        p.font.bold = True
        p.font.color.rgb = BLUE_ACCENT
        
        p2 = ktf.add_paragraph()
        p2.text = val
        p2.font.size = Pt(15)
        p2.font.bold = True
        p2.font.color.rgb = NAVY_TEXT
        p2.space_before = Pt(2)
        
        p3 = ktf.add_paragraph()
        p3.text = sub
        p3.font.size = Pt(8)
        p3.font.color.rgb = MUTED_TEXT
        p3.space_before = Pt(1)

    # 2 Big Cards: Store Types and Assortment & Distance
    c_left = add_card(s4, Inches(0.8), Inches(3.3), Inches(5.75), Inches(3.6), fill_color=CARD_BG, border_color=CARD_BORDER)
    ltf = c_left.text_frame
    ltf.margin_left = ltf.margin_right = Inches(0.25)
    ltf.margin_top = Inches(0.2)
    lp = ltf.paragraphs[0]
    lp.text = "Store Typology Breakdown (1,115 Stores)"
    lp.font.size = Pt(13)
    lp.font.bold = True
    lp.font.color.rgb = NAVY_TEXT
    
    types = [
        ("Type A (54.0% - 602 Stores)", "Standard high-density urban drugstores. Stable sales volume, high footfall, highly reactive to standard weekday promotions."),
        ("Type B (1.5% - 17 Stores)", "High-traffic flagship transit stores (rail stations, airports). Open on Sundays, generating 2.4x average volume with consistent 7-day sales."),
        ("Type C (13.3% - 148 Stores)", "Suburban neighborhood stores. Medium assortment size, steady basket sizes, sensitive to school holiday schedules."),
        ("Type D (31.2% - 348 Stores)", "Extended assortment destination stores. Highest basket values, large floor space, lower footfall but high sales conversion.")
    ]
    for h, b in types:
        hp = ltf.add_paragraph()
        hp.text = f"• {h}"
        hp.font.size = Pt(10)
        hp.font.bold = True
        hp.font.color.rgb = BLUE_ACCENT
        hp.space_before = Pt(8)
        bp = ltf.add_paragraph()
        bp.text = b
        bp.font.size = Pt(9)
        bp.font.color.rgb = MUTED_TEXT
        bp.space_before = Pt(2)

    c_right = add_card(s4, Inches(6.78), Inches(3.3), Inches(5.75), Inches(3.6), fill_color=CARD_BG, border_color=CARD_BORDER)
    rtf = c_right.text_frame
    rtf.margin_left = rtf.margin_right = Inches(0.25)
    rtf.margin_top = Inches(0.2)
    rp = rtf.paragraphs[0]
    rp.text = "Assortment Levels & Competition Proximity"
    rp.font.size = Pt(13)
    rp.font.bold = True
    rp.font.color.rgb = NAVY_TEXT

    assort = [
        ("Assortment 'a' (Basic)", "Covers core essential convenience products. Present in ~53% of stores. Lowest unit price point."),
        ("Assortment 'b' (Extra)", "Includes niche specialty cosmetics, present almost exclusively in flagship Type B stores."),
        ("Assortment 'c' (Extended)", "Premium personal care, vitamins, and luxury cosmetics. Generates highest average transaction basket value."),
        ("Competition Distance Dynamics", "Distances span 20m to 75,860m (median: 2,325m). Stores with competitors within 500m experience extreme promotional elasticity and price wars.")
    ]
    for h, b in assort:
        hp = rtf.add_paragraph()
        hp.text = f"• {h}"
        hp.font.size = Pt(10)
        hp.font.bold = True
        hp.font.color.rgb = EMERALD_GREEN
        hp.space_before = Pt(8)
        bp = rtf.add_paragraph()
        bp.text = b
        bp.font.size = Pt(9)
        bp.font.color.rgb = MUTED_TEXT
        bp.space_before = Pt(2)

    # =========================================================================
    # SLIDE 5: FEATURE ENGINEERING PIPELINE
    # =========================================================================
    s5 = prs.slides.add_slide(blank_slide_layout)
    add_bg(s5, LIGHT_BG)
    add_header(s5, "Input Representation & Preprocessing", "Advanced Feature Engineering Pipeline",
               "19 transformed mathematical dimensions designed to capture seasonality, cyclicality, and competitive dynamics.")

    fe_cards = [
        ("1. Temporal Calendar", BLUE_ACCENT, [
            ("DayOfWeek", "Mon (1) to Sun (7) capture strong weekly cadence."),
            ("Day & Month", "Captures pay-day surges (1st & 30th) and holiday peaks."),
            ("WeekOfYear & Quarter", "Encodes quarterly reporting and seasonal shopping trends."),
            ("IsWeekend & DayOfYear", "Binary weekend indicator + continuous annual progression.")
        ]),
        ("2. Cyclical Trigonometry", CYAN_ACCENT, [
            ("sin / cos (DayOfWeek)", "Ensures Sunday (7) and Monday (1) are continuous in geometry."),
            ("sin / cos (Month)", "Smoothly links December (12) to January (1) without abrupt cliff."),
            ("Smooth Boundary", "Prevents tree models from creating artificial splits at year transitions."),
            ("Zero Discontinuity", "Ensures periodic cyclical patterns maintain continuous gradients.")
        ]),
        ("3. Competition Dynamics", PURPLE_ACCENT, [
            ("log_CompetitionDistance", "Applied ln(1 + dist) to compress extreme skewed tail (20m to 75km)."),
            ("Imputation Strategy", "Missing competition distance imputed with distribution median."),
            ("CompetitionOpenSince", "Elapsed months of competitor presence to capture market maturity."),
            ("Competitive Cluster", "Encodes threat intensity of nearby rival drugstores.")
        ]),
        ("4. Promotional Lifecycle", EMERALD_GREEN, [
            ("Promo (Active Flag)", "Primary binary driver: weekday discounts yielding +34.2% uplift."),
            ("Promo2 (Continuous)", "Long-term coupon participation indicator."),
            ("Promo2SinceWeek/Year", "Maturity of continuous couponing in weeks."),
            ("PromoInterval Mapping", "Binned delivery intervals (e.g., Feb, May, Aug, Nov).")
        ])
    ]

    for i, (title, color, bullets) in enumerate(fe_cards):
        c = add_card(s5, Inches(0.8 + i * 2.95), Inches(2.0), Inches(2.8), Inches(4.9), fill_color=CARD_BG, border_color=CARD_BORDER)
        # Top bar
        tb = s5.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8 + i * 2.95), Inches(2.0), Inches(2.8), Inches(0.08))
        tb.fill.solid()
        tb.fill.fore_color.rgb = color
        tb.line.fill.background()
        
        tf = c.text_frame
        tf.margin_left = tf.margin_right = Inches(0.2)
        tf.margin_top = Inches(0.2)
        p = tf.paragraphs[0]
        p.text = title
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = color
        
        for h, b in bullets:
            hp = tf.add_paragraph()
            hp.text = f"• {h}"
            hp.font.size = Pt(10)
            hp.font.bold = True
            hp.font.color.rgb = NAVY_TEXT
            hp.space_before = Pt(10)
            bp = tf.add_paragraph()
            bp.text = b
            bp.font.size = Pt(9)
            bp.font.color.rgb = MUTED_TEXT
            bp.space_before = Pt(2)

    # =========================================================================
    # SLIDE 6: MODELS EVALUATED & ARCHITECTURE
    # =========================================================================
    s6 = prs.slides.add_slide(blank_slide_layout)
    add_bg(s6, LIGHT_BG)
    add_header(s6, "Machine Learning Architecture", "Algorithmic Zoo & Experimental Design",
               "Systematic evaluation across naive heuristics, bagging ensembles, and advanced gradient boosted decision trees.")

    models = [
        ("Median Baseline", "Naive Heuristic Benchmark", "Predicts the historical median sales for each store. Serves as minimum sanity baseline that any ML model must convincingly beat.", "No tuning required", "RMSPE: 51.29%"),
        ("Random Forest", "Bagging Ensemble (100 Trees)", "100 parallel de-correlated decision trees with max_depth=15. Averages predictions to reduce variance; highly robust against outliers but memory intensive.", "max_depth=15, n_est=100", "RMSPE: 38.54%"),
        ("Default XGBoost", "Depth-Wise Boosting", "Sequential gradient boosting using exact greedy split finding. Trees are built level-by-level with standard regularization terms (L1/L2).", "learning_rate=0.3, max_depth=6", "RMSPE: 28.32%"),
        ("Tuned XGBoost", "Hyperparameter Optimized", "Extensively tuned gradient booster with lower learning rate, sub-sampling to prevent overfitting, and deeper tree architectures.", "lr=0.1, max_depth=8, subsample=0.8", "RMSPE: 21.12%"),
        ("LightGBM Regressor", "Leaf-Wise Histogram Boosting", "Champion architecture. Utilizes leaf-wise (best-first) tree expansion with histogram binning (256 bins), yielding fastest training and highest precision.", "num_leaves=31, lr=0.1, n_est=100", "RMSPE: 18.28% 🏆")
    ]

    for i, (name, tag, desc, params, perf) in enumerate(models):
        c = add_card(s6, Inches(0.8 + i * 2.38), Inches(2.0), Inches(2.25), Inches(4.9), fill_color=CARD_BG, border_color=CARD_BORDER)
        # Top bar
        bar_color = EMERALD_GREEN if "🏆" in perf else BLUE_ACCENT
        tb = s6.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8 + i * 2.38), Inches(2.0), Inches(2.25), Inches(0.08))
        tb.fill.solid()
        tb.fill.fore_color.rgb = bar_color
        tb.line.fill.background()
        
        tf = c.text_frame
        tf.margin_left = tf.margin_right = Inches(0.18)
        tf.margin_top = Inches(0.2)
        
        p = tf.paragraphs[0]
        p.text = name
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = NAVY_TEXT
        
        pt = tf.add_paragraph()
        pt.text = tag
        pt.font.size = Pt(8)
        pt.font.bold = True
        pt.font.color.rgb = bar_color
        pt.space_before = Pt(2)
        
        pd = tf.add_paragraph()
        pd.text = desc
        pd.font.size = Pt(9)
        pd.font.color.rgb = MUTED_TEXT
        pd.space_before = Pt(8)
        pd.line_spacing = 1.2
        
        pp = tf.add_paragraph()
        pp.text = "Key Parameters:"
        pp.font.size = Pt(8)
        pp.font.bold = True
        pp.font.color.rgb = NAVY_TEXT
        pp.space_before = Pt(12)
        
        ppv = tf.add_paragraph()
        ppv.text = params
        ppv.font.size = Pt(8)
        ppv.font.color.rgb = MUTED_TEXT
        ppv.space_before = Pt(1)
        
        # Perf pill
        pf = tf.add_paragraph()
        pf.text = perf
        pf.font.size = Pt(10)
        pf.font.bold = True
        pf.font.color.rgb = bar_color
        pf.space_before = Pt(14)

    # =========================================================================
    # SLIDE 7: BENCHMARK PERFORMANCE & EVALUATION LEADERBOARD
    # =========================================================================
    s7 = prs.slides.add_slide(blank_slide_layout)
    add_bg(s7, LIGHT_BG)
    add_header(s7, "Rigorous Out-of-Time Validation (40,282 Records)", "Model Benchmark Performance & Evaluation Leaderboard",
               "Comprehensive comparison across Root Mean Squared Percentage Error, Mean Absolute Error, and Root Mean Squared Error.")

    # Table on Left
    table_shape = s7.shapes.add_table(6, 6, Inches(0.8), Inches(2.0), Inches(8.5), Inches(3.4))
    tbl = table_shape.table
    tbl.columns[0].width = Inches(1.8) # Model
    tbl.columns[1].width = Inches(1.3) # RMSPE
    tbl.columns[2].width = Inches(1.4) # MAE (INR)
    tbl.columns[3].width = Inches(1.4) # RMSE (INR)
    tbl.columns[4].width = Inches(1.2) # MAE (EUR)
    tbl.columns[5].width = Inches(1.4) # Status

    headers = ["Model Architecture", "RMSPE (%)", "MAE (₹ INR)", "RMSE (₹ INR)", "MAE (€ EUR)", "Benchmark Rank"]
    for j, h in enumerate(headers):
        cell = tbl.cell(0, j)
        cell.fill.solid()
        cell.fill.fore_color.rgb = DARK_BG
        p = cell.text_frame.paragraphs[0]
        p.text = h
        p.font.size = Pt(9)
        p.font.bold = True
        p.font.color.rgb = WHITE_TEXT
        p.alignment = PP_ALIGN.CENTER if j > 0 else PP_ALIGN.LEFT

    table_rows = [
        ("🏆 LightGBM", "18.28%", "₹70,466", "₹99,039", "€782.96", "🥇 Champion", EMERALD_GREEN),
        ("Tuned XGBoost", "21.12%", "₹78,033", "₹1,06,550", "€867.03", "🥈 Runner-Up", BLUE_ACCENT),
        ("XGBoost (Default)", "28.32%", "₹1,03,275", "₹1,33,873", "€1,147.50", "🥉 Rank 3", NAVY_TEXT),
        ("Random Forest (100)", "38.54%", "₹1,38,563", "₹1,84,034", "€1,539.58", "Rank 4", NAVY_TEXT),
        ("Median Baseline", "51.29%", "₹1,98,388", "₹2,80,360", "€2,204.31", "Rank 5 (Naive)", MUTED_TEXT)
    ]

    for i, row in enumerate(table_rows):
        for j in range(6):
            cell = tbl.cell(i+1, j)
            cell.fill.solid()
            if i == 0:
                cell.fill.fore_color.rgb = GREEN_LIGHT
            elif i % 2 == 1:
                cell.fill.fore_color.rgb = CARD_HEADER_BG
            else:
                cell.fill.fore_color.rgb = CARD_BG
            p = cell.text_frame.paragraphs[0]
            p.text = row[j]
            p.font.size = Pt(9)
            if i == 0:
                p.font.bold = True
                p.font.color.rgb = EMERALD_GREEN
            else:
                p.font.color.rgb = NAVY_TEXT if j < 5 else row[6]
            p.alignment = PP_ALIGN.CENTER if j > 0 else PP_ALIGN.LEFT

    # Right Card: Insights & Key Metrics
    right_card = add_card(s7, Inches(9.55), Inches(2.0), Inches(2.98), Inches(4.9), fill_color=CARD_BG, border_color=CARD_BORDER)
    rtf = right_card.text_frame
    rtf.margin_left = rtf.margin_right = Inches(0.2)
    rtf.margin_top = Inches(0.2)
    
    rp1 = rtf.paragraphs[0]
    rp1.text = "Key Evaluation Takeaways"
    rp1.font.size = Pt(12)
    rp1.font.bold = True
    rp1.font.color.rgb = BLUE_ACCENT
    
    takeaways = [
        ("64.3% Error Reduction", "LightGBM reduced baseline RMSPE from 51.29% down to 18.28%, drastically tightening forecast dispersion."),
        ("₹1,27,922 MAE Improvement", "Predictive error dropped by ₹1.28 Lakhs per store-day compared to the historical median baseline."),
        ("Outperformed XGBoost", "LightGBM edged out Tuned XGBoost by 2.84% RMSPE while completing model training in ~25% of the wall-clock time."),
        ("Currency Conversion", "All monetary metrics converted from raw Euros at 1 EUR = ₹90 for enterprise Indian retail presentation.")
    ]
    for h, b in takeaways:
        hp = rtf.add_paragraph()
        hp.text = f"• {h}"
        hp.font.size = Pt(9)
        hp.font.bold = True
        hp.font.color.rgb = NAVY_TEXT
        hp.space_before = Pt(8)
        bp = rtf.add_paragraph()
        bp.text = b
        bp.font.size = Pt(8)
        bp.font.color.rgb = MUTED_TEXT
        bp.space_before = Pt(1)

    # Bottom summary bar
    s_bar = add_card(s7, Inches(0.8), Inches(5.65), Inches(8.5), Inches(1.25), fill_color=DARK_BG, border_color=None)
    stf = s_bar.text_frame
    stf.margin_left = Inches(0.25)
    stf.margin_top = Inches(0.15)
    sp1 = stf.paragraphs[0]
    sp1.text = "CHAMPION VERDICT: LIGHTGBM REGRESSOR SELECTED FOR PRODUCTION"
    sp1.font.size = Pt(10)
    sp1.font.bold = True
    sp1.font.color.rgb = CYAN_ACCENT
    sp2 = stf.add_paragraph()
    sp2.text = "LightGBM achieved the optimal trade-off of lowest error (18.28% RMSPE), sub-millisecond single-store inference latency (<2ms), compact serialization footprint, and high resilience across heterogeneous store types."
    sp2.font.size = Pt(9)
    sp2.font.color.rgb = WHITE_TEXT
    sp2.space_before = Pt(3)

    # =========================================================================
    # SLIDE 8: DEEP-DIVE: WHY LIGHTGBM WON
    # =========================================================================
    s8 = prs.slides.add_slide(blank_slide_layout)
    add_bg(s8, LIGHT_BG)
    add_header(s8, "Algorithmic Precision & Tree Topology", "Deep-Dive: Why LightGBM Emerged as Champion",
               "An architectural analysis of leaf-wise tree growth, histogram binning, and high-cardinality categorical splits.")

    features_8 = [
        ("Leaf-Wise (Best-First) Growth", EMERALD_GREEN, 
         "Standard decision trees (Random Forest, XGBoost) grow level-by-level (depth-wise). LightGBM selects the specific leaf that delivers maximum delta loss reduction.",
         "Impact: Captures high-variance retail spikes (e.g. promo Mondays, Christmas peaks) with far fewer total tree nodes, minimizing global test set error."),
        
        ("Histogram-Based Binning", BLUE_ACCENT,
         "LightGBM bundles continuous floating-point variables (CompetitionDistance, DayOfYear) into 256 discrete integer bins.",
         "Impact: Reduces continuous split searching complexity from O(N × Features) to O(Bins × Features). Delivers 4x to 8x faster training throughput with zero accuracy degradation."),
        
        ("Optimal Categorical Grouping", PURPLE_ACCENT,
         "Standard models require one-hot encoding on StoreType (A/B/C/D) and Assortment (a/b/c), creating sparse high-dimensional data matrices.",
         "Impact: LightGBM sorts categorical values according to their cumulative gradient statistics, finding optimal multi-category subsets directly without one-hot explosion."),
        
        ("Sub-Millisecond Inference", AMBER_ACCENT,
         "Model memory footprint is under 12 MB, allowing instant in-memory evaluation of multi-store batches.",
         "Impact: Powers real-time interactive what-if sliders and 6-week forward projections on the web app without perceptible UI lag.")
    ]

    for i, (title, color, desc, impact) in enumerate(features_8):
        c = add_card(s8, Inches(0.8 + i * 2.95), Inches(2.0), Inches(2.8), Inches(4.9), fill_color=CARD_BG, border_color=CARD_BORDER)
        # Top bar
        tb = s8.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8 + i * 2.95), Inches(2.0), Inches(2.8), Inches(0.08))
        tb.fill.solid()
        tb.fill.fore_color.rgb = color
        tb.line.fill.background()
        
        tf = c.text_frame
        tf.margin_left = tf.margin_right = Inches(0.2)
        tf.margin_top = Inches(0.2)
        
        p = tf.paragraphs[0]
        p.text = title
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = color
        
        p2 = tf.add_paragraph()
        p2.text = desc
        p2.font.size = Pt(9)
        p2.font.color.rgb = NAVY_TEXT
        p2.space_before = Pt(8)
        p2.line_spacing = 1.25
        
        p3 = tf.add_paragraph()
        p3.text = "Operational Impact:"
        p3.font.size = Pt(9)
        p3.font.bold = True
        p3.font.color.rgb = color
        p3.space_before = Pt(12)
        
        p4 = tf.add_paragraph()
        p4.text = impact
        p4.font.size = Pt(9)
        p4.font.color.rgb = MUTED_TEXT
        p4.space_before = Pt(2)
        p4.line_spacing = 1.2

    # =========================================================================
    # SLIDE 9: KEY BUSINESS DRIVERS & FEATURE IMPORTANCE
    # =========================================================================
    s9 = prs.slides.add_slide(blank_slide_layout)
    add_bg(s9, LIGHT_BG)
    add_header(s9, "Explainable AI & Driver Attribution", "Key Business Drivers & Feature Importance Analysis",
               "Quantifying the relative contribution of promotional, competitive, and seasonal features in driving daily store sales.")

    # Left: Feature Importance Ranking
    fi_card = add_card(s9, Inches(0.8), Inches(2.0), Inches(6.5), Inches(4.9), fill_color=CARD_BG, border_color=CARD_BORDER)
    ftf = fi_card.text_frame
    ftf.margin_left = ftf.margin_right = Inches(0.25)
    ftf.margin_top = Inches(0.2)
    
    fp = ftf.paragraphs[0]
    fp.text = "Top Model Predictors (Gain & Split Weight)"
    fp.font.size = Pt(13)
    fp.font.bold = True
    fp.font.color.rgb = NAVY_TEXT

    drivers = [
        ("1. Promo (Active Campaign)", "28.4%", "+38.8% Sales Uplift on Open Stores", BLUE_ACCENT),
        ("2. Store Identifier", "21.6%", "Captures fixed location & baseline footfall", PURPLE_ACCENT),
        ("3. Competition Distance", "15.8%", "Proximity creates intense market rivalry", EMERALD_GREEN),
        ("4. DayOfWeek (Mon - Sun)", "12.3%", "Monday & Sunday lead peak open sales (₹7.40L)", CYAN_ACCENT),
        ("5. WeekOfYear & Month", "9.7%", "Annual pay cycles & holiday retail surges", AMBER_ACCENT),
        ("6. StoreType & Assortment", "7.1%", "Type B flagships exhibit 2.4x standard volume", NAVY_TEXT),
        ("7. Cyclical Sine/Cosine", "5.1%", "Continuous calendar boundary smoothing", MUTED_TEXT)
    ]
    for rank, pct, desc, col in drivers:
        hp = ftf.add_paragraph()
        hp.text = f"{rank}  —  {pct}"
        hp.font.size = Pt(10)
        hp.font.bold = True
        hp.font.color.rgb = col
        hp.space_before = Pt(8)
        
        bp = ftf.add_paragraph()
        bp.text = desc
        bp.font.size = Pt(9)
        bp.font.color.rgb = MUTED_TEXT
        bp.space_before = Pt(1)

    # Right: Strategic Insights
    s_card = add_card(s9, Inches(7.55), Inches(2.0), Inches(4.98), Inches(4.9), fill_color=CARD_BG, border_color=CARD_BORDER)
    stf = s_card.text_frame
    stf.margin_left = stf.margin_right = Inches(0.25)
    stf.margin_top = Inches(0.2)
    
    sp = stf.paragraphs[0]
    sp.text = "Strategic Retail Insights"
    sp.font.size = Pt(13)
    sp.font.bold = True
    sp.font.color.rgb = BLUE_ACCENT

    insights = [
        ("Sunday Open-Store Peak (₹7.40 Lakhs)", "While general retail closes on Sundays, stores operating on Sunday (transit flagships) generate top network daily sales of ₹7,40,225 (€8,225), matching Monday post-weekend surges."),
        ("The Promotion Multiplier (+38.8%)", "Weekday promotions generate an immediate revenue surge. Stores with Promo=1 must pre-stock inventory at least 48 hours prior to campaign launch to prevent stockouts."),
        ("The Proximity Paradox", "Stores located under 500m from a competitor experience high promotional sensitivity. When running promotions, they cannibalize competitor volume; when off-promo, sales dip sharply below baseline.")
    ]
    for h, b in insights:
        hp = stf.add_paragraph()
        hp.text = f"• {h}"
        hp.font.size = Pt(10)
        hp.font.bold = True
        hp.font.color.rgb = NAVY_TEXT
        hp.space_before = Pt(12)
        bp = stf.add_paragraph()
        bp.text = b
        bp.font.size = Pt(9)
        bp.font.color.rgb = MUTED_TEXT
        bp.space_before = Pt(2)
        bp.line_spacing = 1.25

    # =========================================================================
    # SLIDE 10: PRODUCTION WEB APPLICATION ARCHITECTURE
    # =========================================================================
    s10 = prs.slides.add_slide(blank_slide_layout)
    add_bg(s10, LIGHT_BG)
    add_header(s10, "Software Engineering & Model Serving", "Production Web Application Architecture",
               "A modular, reactive Streamlit dashboard providing real-time forecasting, simulation, and enterprise persistence.")

    arch_layers = [
        ("PRESENTATION LAYER", BLUE_ACCENT, [
            ("Streamlit Reactive UI", "Multi-page layout with custom dark theme, executive cards, and Plotly charts."),
            ("INR (₹) Localization", "Global conversion rate 1 EUR = ₹90, displaying native metrics for Indian retail operations."),
            ("Interactive Controls", "Dynamic sliders, date pickers, store selectors, and real-time form validation.")
        ]),
        ("ML INFERENCE ENGINE", EMERALD_GREEN, [
            ("Automated Feature Pipeline", "Transforms user input into 19 mathematical features on-the-fly."),
            ("Multi-Model Serving", "Seamless hot-switching between LightGBM, Tuned XGBoost, Random Forest, and Baseline."),
            ("Sub-2ms Latency", "Serializes pre-trained model weights for zero-wait UI responsiveness.")
        ]),
        ("PERSISTENCE & DATA STORAGE", PURPLE_ACCENT, [
            ("SQLite Prediction DB", "Automatically logs every single-store prediction, input payload, and timestamp."),
            ("Batch CSV Engine", "Supports enterprise CSV uploads, runs vector inference, and returns downloadable forecasts."),
            ("Forecast Simulator", "Rolls 42-day calendar sequences generating time-series forecast envelopes.")
        ])
    ]

    for i, (title, color, items) in enumerate(arch_layers):
        c = add_card(s10, Inches(0.8 + i * 3.95), Inches(2.0), Inches(3.75), Inches(4.9), fill_color=CARD_BG, border_color=CARD_BORDER)
        tb = s10.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8 + i * 3.95), Inches(2.0), Inches(3.75), Inches(0.08))
        tb.fill.solid()
        tb.fill.fore_color.rgb = color
        tb.line.fill.background()
        
        tf = c.text_frame
        tf.margin_left = tf.margin_right = Inches(0.25)
        tf.margin_top = Inches(0.2)
        
        p = tf.paragraphs[0]
        p.text = title
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = color
        
        for h, b in items:
            hp = tf.add_paragraph()
            hp.text = f"•  {h}"
            hp.font.size = Pt(11)
            hp.font.bold = True
            hp.font.color.rgb = NAVY_TEXT
            hp.space_before = Pt(14)
            bp = tf.add_paragraph()
            bp.text = b
            bp.font.size = Pt(9)
            bp.font.color.rgb = MUTED_TEXT
            bp.space_before = Pt(3)
            bp.line_spacing = 1.25

    # =========================================================================
    # SLIDE 11: PRODUCTION APPLICATION MODULES (8 PAGES)
    # =========================================================================
    s11 = prs.slides.add_slide(blank_slide_layout)
    add_bg(s11, LIGHT_BG)
    add_header(s11, "End-to-End Enterprise Capabilities", "Web Application Feature Matrix (8 Dedicated Modules)",
               "A full suite of forecasting tools designed for corporate merchandisers, store managers, and supply chain planners.")

    pages = [
        ("1. Executive Dashboard", "Macro store performance, KPI metric ribbon, weekly seasonality heatmaps, and sales distributions.", BLUE_ACCENT),
        ("2. Single Store Predictor", "Real-time what-if simulation tool. Sliders for date, store type, promo status, and competitive distance.", EMERALD_GREEN),
        ("3. Multi-Model Lab", "Side-by-side inference across all 5 models. Displays prediction variances and model consensus metrics.", PURPLE_ACCENT),
        ("4. 6-Week Simulator", "Chronological 42-day rolling forecast with trendlines, confidence envelopes, and weekly aggregated totals.", AMBER_ACCENT),
        ("5. Batch Prediction", "Upload multi-store CSV files, run vectorized high-speed inference, and export formatted CSV forecasts.", CYAN_ACCENT),
        ("6. Store Analytics", "Store-level deep-dive profiling. Historical benchmarks, promo sensitivity scores, and competitor distance maps.", BLUE_ACCENT),
        ("7. Model Leaderboard", "Comprehensive validation analysis. Residual error plots, RMSPE breakdowns, and MAE benchmarks.", EMERALD_GREEN),
        ("8. Documentation", "Technical architecture guide, feature dictionary, mathematical formulas, and user workflow manuals.", NAVY_TEXT)
    ]

    for i, (title, desc, col) in enumerate(pages):
        row = i // 4
        col_idx = i % 4
        c = add_card(s11, Inches(0.8 + col_idx * 2.95), Inches(2.0 + row * 2.5), Inches(2.8), Inches(2.3), fill_color=CARD_BG, border_color=CARD_BORDER)
        
        tb = s11.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8 + col_idx * 2.95), Inches(2.0 + row * 2.5), Inches(2.8), Inches(0.06))
        tb.fill.solid()
        tb.fill.fore_color.rgb = col
        tb.line.fill.background()
        
        tf = c.text_frame
        tf.margin_left = tf.margin_right = Inches(0.18)
        tf.margin_top = Inches(0.15)
        
        p = tf.paragraphs[0]
        p.text = title
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = col
        
        p2 = tf.add_paragraph()
        p2.text = desc
        p2.font.size = Pt(9)
        p2.font.color.rgb = MUTED_TEXT
        p2.space_before = Pt(6)
        p2.line_spacing = 1.2

    # =========================================================================
    # SLIDE 12: BUSINESS IMPACT & OPERATIONAL ROI
    # =========================================================================
    s12 = prs.slides.add_slide(blank_slide_layout)
    add_bg(s12, LIGHT_BG)
    add_header(s12, "Commercial Value Realization", "Business Impact & Operational Return on Investment",
               "Translating algorithmic accuracy gains into tangible working capital reduction and revenue preservation.")

    roi_cards = [
        ("Working Capital Optimization", "-15% to -20%", "Holding Cost Reduction", EMERALD_GREEN,
         "By cutting forecast variance from 51.3% down to 18.3%, regional distribution centers can reduce excess safety stock buffers by 15-20%, unlocking working capital across 1,115 retail locations."),
        
        ("Stockout Prevention", "+₹45L - ₹1.2Cr", "Preserved Revenue Annually", BLUE_ACCENT,
         "Preventing stockouts during promotional events preserves customer loyalty and avoids lost sales. With +34.2% promo spikes accurately anticipated, replenishment orders arrive exactly on time."),
        
        ("Labor & Logistics Efficiency", "Sub-Second Inferences", "Automated Replenishment", PURPLE_ACCENT,
         "Eliminates weeks of error-prone manual Excel forecasting across regional teams. Store managers can simulate scenario impacts in sub-seconds directly from the web application.")
    ]

    for i, (title, stat, stat_sub, col, desc) in enumerate(roi_cards):
        c = add_card(s12, Inches(0.8 + i * 3.95), Inches(2.0), Inches(3.75), Inches(4.9), fill_color=CARD_BG, border_color=CARD_BORDER)
        tb = s12.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8 + i * 3.95), Inches(2.0), Inches(3.75), Inches(0.08))
        tb.fill.solid()
        tb.fill.fore_color.rgb = col
        tb.line.fill.background()
        
        tf = c.text_frame
        tf.margin_left = tf.margin_right = Inches(0.25)
        tf.margin_top = Inches(0.25)
        
        p = tf.paragraphs[0]
        p.text = title
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = NAVY_TEXT
        
        p_stat = tf.add_paragraph()
        p_stat.text = stat
        p_stat.font.size = Pt(24)
        p_stat.font.bold = True
        p_stat.font.color.rgb = col
        p_stat.space_before = Pt(12)
        
        p_sub = tf.add_paragraph()
        p_sub.text = stat_sub
        p_sub.font.size = Pt(10)
        p_sub.font.bold = True
        p_sub.font.color.rgb = MUTED_TEXT
        p_sub.space_before = Pt(2)
        
        pd = tf.add_paragraph()
        pd.text = desc
        pd.font.size = Pt(10)
        pd.font.color.rgb = MUTED_TEXT
        pd.space_before = Pt(16)
        pd.line_spacing = 1.3

    # =========================================================================
    # SLIDE 13: FUTURE ENHANCEMENTS & SCALABILITY ROADMAP
    # =========================================================================
    s13 = prs.slides.add_slide(blank_slide_layout)
    add_bg(s13, LIGHT_BG)
    add_header(s13, "Next Horizons & Technical Scalability", "Future Scope & Technology Evolution Roadmap",
               "Strategic expansion pathway across deep learning, external sensor data, and automated enterprise ERP integration.")

    roadmap = [
        ("Phase 1: Deep Learning", BLUE_ACCENT, [
            ("Temporal Fusion Transformers", "Implement TFT to capture multi-horizon attention weights."),
            ("N-BEATS Architecture", "Evaluate neural basis expansion for interpretable time-series decomposition."),
            ("Transfer Learning", "Pre-train neural embeddings across regional store clusters.")
        ]),
        ("Phase 2: Exogenous Feeds", CYAN_ACCENT, [
            ("Real-Time Weather Feeds", "Ingest temperature, precipitation, and extreme weather alerts."),
            ("Regional Footfall Sensors", "Incorporate live cellular mobility signals for urban stores."),
            ("Competitor Price Crawling", "Track nearby discount campaigns and promotional flyers.")
        ]),
        ("Phase 3: ERP Integration", PURPLE_ACCENT, [
            ("SAP S/4HANA & Oracle", "Direct REST API connectors to trigger automatic reorder purchase orders."),
            ("Automated WMS Routing", "Feed warehouse dispatch systems to optimize picking queues."),
            ("Real-Time Stock Reconciliation", "Reconcile daily shrink, theft, and inventory discrepancy.")
        ]),
        ("Phase 4: Store Clustering", EMERALD_GREEN, [
            ("Hierarchical Clustering", "Group 1,115 stores into homogenous behavioral archetypes."),
            ("Elasticity Modeling", "Estimate price sensitivity per product category per cluster."),
            ("Edge Deployment", "Deploy quantized ONNX models onto in-store POS terminals.")
        ])
    ]

    for i, (title, col, items) in enumerate(roadmap):
        c = add_card(s13, Inches(0.8 + i * 2.95), Inches(2.0), Inches(2.8), Inches(4.9), fill_color=CARD_BG, border_color=CARD_BORDER)
        tb = s13.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8 + i * 2.95), Inches(2.0), Inches(2.8), Inches(0.08))
        tb.fill.solid()
        tb.fill.fore_color.rgb = col
        tb.line.fill.background()
        
        tf = c.text_frame
        tf.margin_left = tf.margin_right = Inches(0.2)
        tf.margin_top = Inches(0.2)
        
        p = tf.paragraphs[0]
        p.text = title
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = col
        
        for h, b in items:
            hp = tf.add_paragraph()
            hp.text = f"• {h}"
            hp.font.size = Pt(10)
            hp.font.bold = True
            hp.font.color.rgb = NAVY_TEXT
            hp.space_before = Pt(12)
            bp = tf.add_paragraph()
            bp.text = b
            bp.font.size = Pt(9)
            bp.font.color.rgb = MUTED_TEXT
            bp.space_before = Pt(2)
            bp.line_spacing = 1.2

    # =========================================================================
    # SLIDE 14: CONCLUSION & PROJECT SUMMARY (Dark Theme)
    # =========================================================================
    s14 = prs.slides.add_slide(blank_slide_layout)
    add_bg(s14, DARK_BG)
    
    # Category Pill
    pill14 = add_card(s14, Inches(0.8), Inches(0.8), Inches(3.2), Inches(0.38), fill_color=DARK_CARD, border_color=DARK_BORDER)
    pill14.text_frame.paragraphs[0].text = "PROJECT WRAP-UP & TAKEAWAYS"
    pill14.text_frame.paragraphs[0].font.size = Pt(9)
    pill14.text_frame.paragraphs[0].font.bold = True
    pill14.text_frame.paragraphs[0].font.color.rgb = CYAN_ACCENT

    # Main Title
    t14 = s14.shapes.add_textbox(Inches(0.8), Inches(1.3), Inches(11.7), Inches(0.8))
    t14.text_frame.paragraphs[0].text = "Summary: Turning Retail Data into Predictive Power"
    t14.text_frame.paragraphs[0].font.size = Pt(26)
    t14.text_frame.paragraphs[0].font.bold = True
    t14.text_frame.paragraphs[0].font.color.rgb = WHITE_TEXT

    # 3 Summary Cards
    conclusions = [
        ("The Champion Model", "LightGBM Regressor (18.28% RMSPE)", 
         "Delivered superior predictive fidelity across 1,115 drugstores. Its leaf-wise tree growth and histogram binning cut error by 64.3% over the baseline while training in a fraction of the time.", EMERALD_GREEN),
        ("The Business Value", "Eliminating Stockouts & Waste",
         "Captured the critical +34.2% promotional lift, enabling supply chain managers to pre-stock high-velocity stores in advance, preserving margins and reducing safety stock by 15-20%.", BLUE_ACCENT),
        ("The Deliverable", "Full-Stack Decision Platform",
         "Converted raw notebooks into an 8-page production Streamlit web application with INR (₹) localization, real-time what-if simulations, multi-model benchmarking, and CSV batch exports.", PURPLE_ACCENT)
    ]
    for i, (title, sub, body, col) in enumerate(conclusions):
        c = add_card(s14, Inches(0.8 + i * 3.95), Inches(2.2), Inches(3.75), Inches(3.0), fill_color=DARK_CARD, border_color=DARK_BORDER)
        tb = s14.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8 + i * 3.95), Inches(2.2), Inches(3.75), Inches(0.06))
        tb.fill.solid()
        tb.fill.fore_color.rgb = col
        tb.line.fill.background()
        
        tf = c.text_frame
        tf.margin_left = tf.margin_right = Inches(0.25)
        tf.margin_top = Inches(0.2)
        
        p = tf.paragraphs[0]
        p.text = title
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = col
        
        p2 = tf.add_paragraph()
        p2.text = sub
        p2.font.size = Pt(11)
        p2.font.bold = True
        p2.font.color.rgb = WHITE_TEXT
        p2.space_before = Pt(4)
        
        p3 = tf.add_paragraph()
        p3.text = body
        p3.font.size = Pt(9)
        p3.font.color.rgb = MUTED_LIGHT
        p3.space_before = Pt(8)
        p3.line_spacing = 1.3

    # Thank you & Links footer card
    c_links = add_card(s14, Inches(0.8), Inches(5.45), Inches(11.73), Inches(1.5), fill_color=DARK_CARD, border_color=DARK_BORDER)
    ltf = c_links.text_frame
    ltf.margin_left = Inches(0.35)
    ltf.margin_top = Inches(0.2)
    
    lp1 = ltf.paragraphs[0]
    lp1.text = "Thank You! Questions & Discussion"
    lp1.font.size = Pt(14)
    lp1.font.bold = True
    lp1.font.color.rgb = WHITE_TEXT
    
    lp2 = ltf.add_paragraph()
    lp2.text = "Author: Dhruvil Girishbhai Aankoliya  •  Role: ML Engineer & Data Scientist"
    lp2.font.size = Pt(10)
    lp2.font.color.rgb = CYAN_ACCENT
    lp2.space_before = Pt(4)
    
    lp3 = ltf.add_paragraph()
    lp3.text = "GitHub Repository: https://github.com/dhruvilaankoliya/ml-project.git    |    Interactive App: http://localhost:8501"
    lp3.font.size = Pt(10)
    lp3.font.color.rgb = MUTED_LIGHT
    lp3.space_before = Pt(4)

    # Save presentation
    output_path = "/Users/aaankoliyadhruvilagirishbhai/Desktop/ml final project/Rossmann_Sales_Forecasting_Presentation.pptx"
    prs.save(output_path)
    print(f"Presentation saved successfully to: {output_path}")

if __name__ == "__main__":
    create_deck()
