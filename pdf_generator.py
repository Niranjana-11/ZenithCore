# pdf_generator.py
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, KeepTogether
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from io import BytesIO
import datetime

def generate_pdf_report(role, difficulty, topic, transcript_list):
    """
    Generates a beautifully formatted PDF session summary report in memory.
    Returns the raw bytes of the generated PDF.
    """
    buffer = BytesIO()
    
    # Page setup
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=54,  # 0.75 inch
        leftMargin=54,
        topMargin=54,
        bottomMargin=54
    )
    
    story = []
    
    # ----------------- STYLES -----------------
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=28,
        textColor=colors.HexColor('#1e3a8a'), # Dark Blue
        spaceAfter=15
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubTitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=11,
        leading=15,
        textColor=colors.HexColor('#475569'), # Slate Gray
        spaceAfter=25
    )
    
    h1_style = ParagraphStyle(
        'SectionH1',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=15,
        leading=19,
        textColor=colors.HexColor('#1e1b4b'), # Indigo
        spaceBefore=15,
        spaceAfter=8,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'BodyTextCustom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor('#1e293b'), # Dark Slate
        spaceAfter=8
    )

    bullet_style = ParagraphStyle(
        'BulletCustom',
        parent=body_style,
        leftIndent=15,
        firstLineIndent=-10,
        spaceAfter=5
    )
    
    meta_label_style = ParagraphStyle(
        'MetaLabel',
        parent=body_style,
        fontName='Helvetica-Bold',
        textColor=colors.HexColor('#475569')
    )
    
    verdict_style = ParagraphStyle(
        'VerdictText',
        parent=body_style,
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=colors.HexColor('#065f46') # Emerald Green
    )
    
    # ----------------- DOCUMENT HEADER -----------------
    story.append(Paragraph("🎙️ Interview Prep Coach", title_style))
    story.append(Paragraph(f"Official Mock Technical Interview Performance Report", subtitle_style))
    story.append(Spacer(1, 10))
    
    # Metadata Table
    meta_data = [
        [Paragraph("Role Target:", meta_label_style), Paragraph(role, body_style),
         Paragraph("Date Completed:", meta_label_style), Paragraph(datetime.date.today().strftime("%B %d, %Y"), body_style)],
        [Paragraph("Topic Area:", meta_label_style), Paragraph(topic, body_style),
         Paragraph("Difficulty Level:", meta_label_style), Paragraph(difficulty, body_style)]
    ]
    
    meta_table = Table(meta_data, colWidths=[90, 160, 100, 154])
    meta_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LINEBELOW', (0,-1), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 20))
    
    # ----------------- SCORE SUMMARY CARD -----------------
    # Compute Average Score
    scores = []
    all_strengths = []
    all_improvements = []
    
    for entry in transcript_list:
        if "score" in entry and entry["score"] is not None:
            scores.append(entry["score"])
        if "follow_up_score" in entry and entry["follow_up_score"] is not None and entry["follow_up_score"] > 0:
            scores.append(entry["follow_up_score"])
        if "strengths" in entry and entry["strengths"]:
            all_strengths.extend(entry["strengths"])
        if "improvement_tips" in entry and entry["improvement_tips"]:
            all_improvements.extend(entry["improvement_tips"])
        if "follow_up_strengths" in entry and entry["follow_up_strengths"]:
            all_strengths.extend(entry["follow_up_strengths"])
        if "follow_up_improvement_tips" in entry and entry["follow_up_improvement_tips"]:
            all_improvements.extend(entry["follow_up_improvement_tips"])
            
    avg_score = round(sum(scores) / len(scores), 1) if scores else 0.0
    
    if avg_score >= 8.5:
        verdict = "DISTINGUISHED / STRONG HIRE"
        verdict_color = colors.HexColor('#065f46')
        bg_card_color = colors.HexColor('#d1fae5')
    elif avg_score >= 7.0:
        verdict = "HIRE"
        verdict_color = colors.HexColor('#1e3a8a')
        bg_card_color = colors.HexColor('#dbeafe')
    elif avg_score >= 5.0:
        verdict = "BORDERLINE / NEEDS PRACTICE"
        verdict_color = colors.HexColor('#854d0e')
        bg_card_color = colors.HexColor('#fef3c7')
    else:
        verdict = "NO HIRE / NEEDS REVISION"
        verdict_color = colors.HexColor('#991b1b')
        bg_card_color = colors.HexColor('#fee2e2')

    verdict_style.textColor = verdict_color
    
    card_title_style = ParagraphStyle(
        'CardTitle',
        parent=body_style,
        fontName='Helvetica-Bold',
        fontSize=10,
        textColor=colors.HexColor('#475569'),
        spaceAfter=4
    )
    score_style = ParagraphStyle(
        'ScoreVal',
        parent=body_style,
        fontName='Helvetica-Bold',
        fontSize=28,
        leading=32,
        textColor=verdict_color
    )
    
    summary_card_data = [
        [
            Paragraph("OVERALL SCORE", card_title_style),
            Paragraph("RECRUITER ASSESSMENT", card_title_style)
        ],
        [
            Paragraph(f"{avg_score} <font size=14 textColor='#64748b'>/ 10</font>", score_style),
            Paragraph(verdict, verdict_style)
        ]
    ]
    summary_card = Table(summary_card_data, colWidths=[200, 304])
    summary_card.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), bg_card_color),
        ('TOPPADDING', (0,0), (-1,-1), 16),
        ('BOTTOMPADDING', (0,0), (-1,-1), 16),
        ('LEFTPADDING', (0,0), (-1,-1), 20),
        ('RIGHTPADDING', (0,0), (-1,-1), 20),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOX', (0,0), (-1,-1), 1.5, verdict_color),
    ]))
    story.append(summary_card)
    story.append(Spacer(1, 20))
    
    # ----------------- EXECUTIVE SUMMARY -----------------
    story.append(Paragraph("Executive Summary", h1_style))
    summary_paragraph = (
        f"The candidate has successfully completed a mock interview designed to simulate "
        f"a live evaluation loop. The session assessed knowledge of <b>{topic}</b> under "
        f"varying constraints. A multi-turn dialogue framework probed technical concepts "
        f"and evaluated response structure, technical depth, and communication clarity."
    )
    story.append(Paragraph(summary_paragraph, body_style))
    story.append(Spacer(1, 10))
    
    # ----------------- Q&A BREAKDOWN TABLE -----------------
    story.append(Paragraph("Session Breakdown Table", h1_style))
    
    th_style = ParagraphStyle(
        'TableHeader',
        parent=body_style,
        fontName='Helvetica-Bold',
        textColor=colors.white
    )
    
    table_data = [[
        Paragraph("Phase", th_style),
        Paragraph("Question Probe", th_style),
        Paragraph("Score", th_style),
        Paragraph("Technical Feedback", th_style)
    ]]
    
    for i, entry in enumerate(transcript_list):
        # Format main feedback (extract correctness before communication)
        main_fb = entry.get("feedback", "N/A")
        if "Communication:" in main_fb:
            main_fb = main_fb.split("Communication:")[0].replace("Correctness:", "").strip()
        if len(main_fb) > 130:
            main_fb = main_fb[:127] + "..."
            
        table_data.append([
            Paragraph(f"Q{i+1} Core", body_style),
            Paragraph(entry["question"][:55] + "...", body_style),
            Paragraph(f"<b>{entry['score']}/10</b>", body_style),
            Paragraph(main_fb, body_style)
        ])
        
        # Format follow-up feedback
        if entry.get("follow_up_question") and entry.get("follow_up_answer") != "[Skipped]":
            fu_fb = entry.get("follow_up_feedback", "N/A")
            if "Communication:" in fu_fb:
                fu_fb = fu_fb.split("Communication:")[0].replace("Correctness:", "").strip()
            if len(fu_fb) > 130:
                fu_fb = fu_fb[:127] + "..."
                
            table_data.append([
                Paragraph(f"Q{i+1} Follow-up", body_style),
                Paragraph(entry["follow_up_question"][:55] + "...", body_style),
                Paragraph(f"<b>{entry.get('follow_up_score', 0)}/10</b>", body_style),
                Paragraph(fu_fb, body_style)
            ])
            
    breakdown_table = Table(table_data, colWidths=[90, 150, 50, 214])
    breakdown_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1e1b4b')),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#f8fafc')]),
    ]))
    story.append(breakdown_table)
    story.append(Spacer(1, 20))
    
    # ----------------- STRENGTHS & WEAKNESSES -----------------
    # Deduplicate strengths and improvements
    all_strengths = list(dict.fromkeys(all_strengths))
    all_improvements = list(dict.fromkeys(all_improvements))
    
    if not all_strengths:
        all_strengths = ["Showed effort in responding to all technical questions", "Engaged with follow-up prompts"]
    if not all_improvements:
        all_improvements = ["Provide more specific details in code/design responses", "Explain architectural trade-offs explicitly"]
        
    story.append(Paragraph("Key Technical Strengths", h1_style))
    for s in all_strengths[:4]:
        story.append(Paragraph(f"• <b>{s}</b>", bullet_style))
    story.append(Spacer(1, 10))
    
    story.append(Paragraph("Areas for Growth & Focus", h1_style))
    for imp in all_improvements[:4]:
        story.append(Paragraph(f"• <b>{imp}</b>", bullet_style))
    story.append(Spacer(1, 10))
    
    # ----------------- ROADMAP -----------------
    story.append(Paragraph("Actionable Improvement Roadmap", h1_style))
    story.append(Paragraph(f"1. 📚 <b>Targeted Review:</b> Dedicate study sessions to: {', '.join(all_improvements[:2]) if all_improvements else 'core topics'}.", bullet_style))
    story.append(Paragraph("2. 💻 <b>Hands-on Practice:</b> Implement basic algorithmic patterns and design skeletons matching these focus areas.", bullet_style))
    story.append(Paragraph("3. ⏱️ <b>Mock Conditioning:</b> Practice verbal explanations structured around definition, complexity analysis, and edge cases under a 3-minute timer.", bullet_style))
    
    # Build Document
    doc.build(story)
    
    buffer.seek(0)
    pdf_bytes = buffer.getvalue()
    buffer.close()
    
    return pdf_bytes
