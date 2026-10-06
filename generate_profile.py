from pathlib import Path
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, KeepTogether
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import A4

root=Path(__file__).parent
pdfmetrics.registerFont(TTFont('ProfileSans','/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'))
pdfmetrics.registerFont(TTFont('ProfileBold','/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'))
pdfmetrics.registerFontFamily('ProfileSans',normal='ProfileSans',bold='ProfileBold',italic='ProfileSans',boldItalic='ProfileBold')
styles=getSampleStyleSheet()
styles.add(ParagraphStyle(name='Name',fontName='ProfileBold',fontSize=25,leading=32,textColor=colors.HexColor('#08131c'),spaceAfter=10))
styles.add(ParagraphStyle(name='Role',fontName='ProfileSans',fontSize=10.2,leading=15,textColor=colors.HexColor('#3d555c'),spaceAfter=12))
styles.add(ParagraphStyle(name='BodyProfile',fontName='ProfileSans',fontSize=9,leading=14,spaceAfter=9,textColor=colors.HexColor('#273e46')))
styles.add(ParagraphStyle(name='HeadingProfile',fontName='ProfileBold',fontSize=11,leading=16,spaceBefore=15,spaceAfter=8,keepWithNext=True,textColor=colors.HexColor('#0b5643')))
styles.add(ParagraphStyle(name='SmallProfile',fontName='ProfileSans',fontSize=8,leading=12,textColor=colors.HexColor('#4a6067'),spaceAfter=7))
flow=[]
def p(text,style='BodyProfile'): return Paragraph(text,styles[style])
def section(title,texts):
 flow.append(p(title,'HeadingProfile'))
 for t in texts: flow.append(p(t))
flow += [p('Gürkan Çamok, MSc','Name'),p('Clinical Decision Support Systems Developer<br/>Evidence-Based Practice and Research Lead | Diabetes Case Manager','Role'),p('Anadolu Medical Center, Türkiye — in affiliation with Johns Hopkins Medicine<br/><link href="https://gurkancamok.github.io/" color="#0b5643">gurkancamok.github.io</link>','SmallProfile')]
section('PROFESSIONAL PROFILE',['Hands-on digital health software developer with a clinical background. Since 2023, I have designed and built products spanning clinical decision support, AI-supported wound-assessment research, medication education and research workflows. I take technical ownership across product definition, requirements analysis, application architecture, interface design, coding, testing and evaluation. My portfolio includes hospital-deployed systems, public applications and research prototypes.'])
section('SELECTED PRODUCT CONTRIBUTIONS',[
'<b>Digital Insulin Infusion Assistant — sole developer.</b> Requirements analysis, protocol-to-code translation, interface development, input checks, testing, shadow validation and implementation coordination. Institutionally approved and deployed hospital-wide in January 2026. In a 120-case paired shadow study, digital outputs matched an independently calculated protocol reference in all evaluated cases. Approximately 400 professionals were given access; this is not an active-user count.',
'<b>Clinical Research Hub — software developer.</b> Institutionally deployed and in hospital use. Browser and Firebase workflow for topic creation, search, specialty and project-type filtering, named topic selection and availability tracking. Project records report approximately 50 topics and 30 selections.',
'<b>Research Advisor Matching — creator and developer.</b> Institutionally deployed and in hospital use. Explainable expertise and capacity ranking, workload-aware recommendations and a local assignment trail. The underlying workflow reports approximately 100 allocations across 11 advisors; the public demonstration uses fictional data.',
'<b>GlucoGuide — designer and developer.</b> Structured oral antidiabetic medication education through an accessible browser interface and QR-link distribution.',
'<b>WoundGuard — technical co-developer and product lead.</b> Integration of pressure-injury image classification with separate clinician-reviewable guidance. Research prototype; external clinical performance remains to be established.',
'<b>AEGIS — developer.</b> Multi-domain computational clinical-risk prototype. The composite index requires independent validation before clinical interpretation.'])
section('RESEARCH AND IMPLEMENTATION BOUNDARIES',['The insulin study was conducted at one institution. Recorded-input digital calculations were performed by the developer the next day and did not influence treatment. Protocol concordance, task timing, usability and patient outcomes are separate evidence questions. No NHS deployment, CE marking or demonstrated patient-outcome improvement is claimed.'])
section('SELECTED RECOGNITION AND CONTRIBUTION',[
'2026 — Doktorclub Awards finalist, Health Professional of the Year.<br/>2026 — invited presentation on artificial intelligence in health technologies, İstanbul Yeni Yüzyıl University.<br/>2025 — WoundGuard third prize, innovative digital health products competition at the international health sciences congress, Istanbul.<br/>2025 — insulin assistant evaluation presented at the 3rd International Internal Medicine Nursing Congress.<br/>2022 — Doktorclub Awards finalist, Innovative Nurse of the Year.<br/>2018 — first prize for the Blood Loss Measurement Device, 1st International Innovative Nursing Congress.<br/>May 2017 — Honorable Mention, Innovation Project Competition, 5th Innovative Nursing Symposium.',
'Institutional work includes evidence-based research-group leadership and endocrine tumour-board coordination.'])
section('EDUCATION AND CONTINUING TECHNICAL DEVELOPMENT',['MSc. Selected structured learning includes Python and AI / machine-learning training at Ege University, IBM Artificial Intelligence Fundamentals and the University of Helsinki’s Elements of AI.'])
section('PUBLISHED WRITING AND INDEPENDENT COVERAGE',[
'<link href="https://www.ktm-journal.de/files/Public/KTM/Archiv/Inhaltsverzeichnisse/2026/Inhalt_KTM_10_2026.pdf" color="#0b5643"><b>KTM Krankenhaus Technik + Management</b></link> — Von der Anforderung zum Routinebetrieb. Published project feature, October 2026, issue 10, pages 39–41.',
'<link href="https://healthcare-in-europe.com/en/news/insulin-infusions-digital-safety.html" color="#0b5643"><b>Healthcare in Europe</b></link> — independent project feature by Wolfgang Behrends, 9 September 2026.',
'<link href="https://www.healthitanswers.net/the-workflow-gap-holding-back-healthcare-ai-adoption/" color="#0b5643"><b>Health IT Answers</b></link> — The Workflow Gap Holding Back Healthcare AI Adoption, 30 July 2026.',
'<link href="https://www.pulseit.news/opinion/opinion-why-clinician-led-digital-innovation-needs-infrastructure-not-isolated-projects/" color="#0b5643"><b>Pulse+IT</b></link> — Why clinician-led digital innovation needs infrastructure, not isolated projects, 4 September 2026.',
'<link href="https://www.healthcarebusinesstoday.com/validate-clinical-decision-support/" color="#0b5643"><b>Healthcare Business Today</b></link> — What Hospitals Should Validate Before Deploying Clinical Decision Support, August 2026.'])
section('FUTURE DEVELOPMENT',['Interests include explainable clinical software, AI-supported wound-assessment research and research workflow products. Proposed UK work starts with partner requirements, versioned specifications, independent review and clinician usability evaluation, followed by governed pilots before wider deployment.'])
flow.append(p('Professional identities: <link href="https://www.linkedin.com/in/gurkancamok" color="#0b5643">LinkedIn</link> · <link href="https://github.com/gurkancamok" color="#0b5643">GitHub</link> · ORCID 0000-0002-7437-3219','SmallProfile'))
def page(canvas,doc):
 canvas.saveState();w,h=A4
 canvas.setStrokeColor(colors.HexColor('#bdd5ca'));canvas.line(43,39,w-43,39)
 canvas.setFont('ProfileSans',7);canvas.setFillColor(colors.HexColor('#4a6067'))
 canvas.drawString(43,26,'Gürkan Çamok | Selected professional profile | Updated 6 October 2026')
 canvas.drawRightString(w-43,26,str(doc.page));canvas.restoreState()
doc=SimpleDocTemplate(str(root/'downloads/gurkan-camok-professional-profile.pdf'),pagesize=A4,rightMargin=43,leftMargin=43,topMargin=42,bottomMargin=54,title='Gürkan Çamok — Professional Profile',author='Gürkan Çamok')
doc.build(flow,onFirstPage=page,onLaterPages=page)
print('Professional profile PDF generated')
