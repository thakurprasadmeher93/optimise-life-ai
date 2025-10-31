import os
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from datetime import datetime
EXPORT_DIR = os.getenv('EXPORT_DIR','/tmp/optimiselife_exports')
os.makedirs(EXPORT_DIR, exist_ok=True)
def generate_simple_report(calc_name, inputs, results, filename=None):
    if not filename:
        ts = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        filename = f"{calc_name}_report_{ts}.pdf"
    path = os.path.join(EXPORT_DIR, filename)
    doc = SimpleDocTemplate(path, pagesize=A4)
    styles = getSampleStyleSheet()
    story = []
    story.append(Paragraph(f"Optimise Life – AI™ | {calc_name} Report", styles['Title']))
    story.append(Spacer(1,12))
    story.append(Paragraph(f"Generated on: {datetime.now().strftime('%d-%b-%Y %H:%M:%S')}", styles['Normal']))
    story.append(Spacer(1,12))
    rows = [['Parameter','Value']]
    for k,v in inputs.items():
        rows.append([str(k), str(v)])
    t = Table(rows, hAlign='LEFT')
    t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.lightgrey),('GRID',(0,0),(-1,-1),0.5,colors.grey)]))
    story.append(t)
    story.append(Spacer(1,12))
    story.append(Paragraph('<b>Result</b>', styles['Heading3']))
    rows2 = [['Metric','Value']]
    for k,v in results.items():
        rows2.append([str(k), str(v)])
    t2 = Table(rows2, hAlign='LEFT')
    t2.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.lightgrey),('GRID',(0,0),(-1,-1),0.5,colors.grey)]))
    story.append(t2)
    story.append(Spacer(1,12))
    story.append(Paragraph('© 2025 Optimise Life – AI™ | www.optimiselife.in', styles['Normal']))
    doc.build(story)
    return path
