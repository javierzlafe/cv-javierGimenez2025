"""Generate the web CV and PDF from the user's November 2026 source CV."""
from pathlib import Path
from html import escape
import re
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, KeepTogether
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.colors import HexColor
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from pypdf import PdfReader
import pypdfium2 as pdfium

ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / 'output/pdf/Javier_Gimenez_CV_2026.pdf'
TITLE = 'Mobile & Full Stack Developer | IA y automatización'
PROFILE = ('Desarrollador de software con experiencia en aplicaciones móviles y soluciones transaccionales. '
           'Desarrollo con Flutter y Dart, y experiencia en .NET y Xamarin en proyectos de identidad digital. '
           'Combino conocimientos de React, React Native y backend con integración de IA y automatización. '
           'Docente de desarrollo web, mobile e IA y mentor técnico.')
JOBS = [
    ('Dicsys', 'Mobile Developer', '2023 - 2025', [
        'Desarrollé aplicaciones móviles con Flutter y Dart, con funcionalidades de geolocalización y seguimiento de paquetes.',
        'Colaboré en una solución transaccional para un laboratorio de análisis de semillas.']),
    ('GYL Group', '.NET / Xamarin Developer', '2022 - 2023', [
        'Participé en una aplicación vinculada al RENAPER con reconocimiento facial y detección de movimiento.',
        'Colaboré en una aplicación para registrar y almacenar información de degustaciones de vinos.']),
    ('Coderhouse', 'Docente de Desarrollo Web, Mobile e IA', '2021 - Actualidad', [
        'Formación en HTML, CSS, JavaScript, React y React Native, con preparación de proyectos y evaluaciones.',
        'Dictado de clases de Prompt Engineering y automatización de procesos con herramientas de IA.']),
    ('INTI', 'Mentor en Programación', '2022 - 2023', [
        'Brindé acompañamiento técnico en proyectos y orientación profesional a participantes.']),
]
PROJECTS = [
    ('Cropbase', 'Plataforma de gestión agrícola con IA · En desarrollo', [
        'Diseño de flujos de ingreso de datos desde WhatsApp, procesamiento asistido por IA y validación humana.',
        'Arquitectura propuesta con JavaScript, Supabase, autenticación Google y despliegue web.']),
    ('Automatizaciones con IA', 'Proyectos y prototipos', [
        'Diseño de flujos con n8n y Make para clasificación de mensajes, extracción de datos y revisión humana.'])
]
SKILLS = [
    ('Mobile', 'Flutter, Dart, React Native, Expo, Xamarin.'),
    ('Frontend', 'JavaScript, React, HTML5, CSS3, Vite, SASS, Bootstrap.'),
    ('Backend e integraciones', 'Node.js, Java, Spring Boot, APIs REST, Webhooks, Postman.'),
    ('Datos y estado', 'SQL, SQLite, Firebase, Supabase, Redux Toolkit, RTK Query, Context API, AsyncStorage.'),
    ('Herramientas y métodos', 'Git, GitHub, Jira, Scrum, metodologías ágiles.')
]
AI = [
    ('Integración y automatización', 'APIs de LLMs, Prompt Engineering, respuestas estructuradas, extracción de datos, n8n, Make; integraciones con Gmail, WhatsApp y Slack.'),
    ('Patrones y plataformas', 'RAG, Human-in-the-Loop, Prompt Chaining, Context Engineering; OpenAI / ChatGPT, Gemini, Claude, Google AI Studio.'),
    ('Conocimientos complementarios', 'Prompt Caching, Message Batches y MCP.')
]

def text(value):
    return escape(value)

def bullets(items):
    return '<ul>' + ''.join('<li>' + text(x) + '</li>' for x in items) + '</ul>'

def lines(items):
    return '<p>' + '<br>'.join('<strong>' + text(a) + ':</strong> ' + text(b) for a,b in items) + '</p>'

def write_html():
    jobs = ''.join(f'<article><div class="job-title"><h3>{text(company)} · {text(role)}</h3><span>{text(dates)}</span></div>{bullets(items)}</article>' for company,role,dates,items in JOBS)
    projects = ''.join(f'<article><h3>{text(name)}</h3><p class="project-status">{text(status)}</p>{bullets(items)}</article>' for name,status,items in PROJECTS)
    html = f'''<!DOCTYPE html>
<html lang="es"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>CV · Javier Gimenez | Mobile, Full Stack e IA</title><link rel="stylesheet" href="cv.css"></head><body>
<nav class="toolbar" aria-label="Opciones del currículum"><a href="index.html">← Volver al portfolio</a><div><a class="download" href="output/pdf/Javier_Gimenez_CV_2026.pdf" download>Descargar PDF</a><button type="button" id="printCV">Imprimir / Guardar PDF</button></div></nav>
<main class="resume"><header><h1>Javier Gimenez</h1><p class="headline">{text(TITLE)}</p><p class="contact">Mar del Plata, Argentina<br><a href="mailto:gimenezjavier.jig@gmail.com">gimenezjavier.jig@gmail.com</a> · <a href="tel:+541156385296">+54 11 5638 5296</a><br><a href="https://www.linkedin.com/in/javier-gimenez-jig/">linkedin.com/in/javier-gimenez-jig</a> · <a href="https://github.com/javierzlafe">github.com/javierzlafe</a></p></header>
<section><h2>Perfil profesional</h2><p>{text(PROFILE)}</p></section><section><h2>Experiencia profesional</h2>{jobs}</section><section><h2>Proyectos e iniciativas</h2>{projects}</section><section><h2>Competencias técnicas</h2>{lines(SKILLS)}</section><section><h2>Inteligencia artificial y automatización</h2>{lines(AI)}</section></main><script src="cv.js" defer></script></body></html>'''
    (ROOT / 'cv.html').write_text(html, encoding='utf-8')

def update_portfolio():
    p = ROOT / 'index.html'
    html = p.read_text(encoding='utf-8')
    html = html.replace('<title>Javier Gimenez | Frontend & Mobile Developer</title>', '<title>Javier Gimenez | Mobile, Full Stack e IA</title>')
    html = html.replace('Javier Gimenez. Desarrollo frontend y mobile con React y React Native. Experiencia en Dicsys, G&L Group y docencia en Coderhouse.', 'Javier Gimenez. Desarrollo mobile, full stack e integración de IA. Flutter, Dart, React y automatización. Experiencia en Dicsys, GYL Group, Coderhouse e INTI.')
    html = html.replace('Mar del Plata, Argentina · Disponibilidad full time', 'Mar del Plata, Argentina · Desarrollo e integración de IA')
    html = html.replace('Frontend &<br>Mobile Developer', 'Mobile, Full Stack<br>& AI Integration')
    html = re.sub(r'<p class="hero-description">.*?</p>', '<p class="hero-description">Desarrollo aplicaciones móviles con <strong>Flutter y Dart.</strong> Mi experiencia abarca geolocalización, seguimiento de paquetes y soluciones transaccionales. También diseño integraciones de IA y automatizaciones, y formo desarrolladores.</p>', html)
    html = re.sub(r'<div class="hero-tags">.*?</div>', '<div class="hero-tags"><span>Flutter / Dart</span><span>React / React Native</span><span>IA generativa</span><span>n8n / Make</span></div>', html)
    html = html.replace('G&L Group', 'GYL Group')
    html = html.replace('<span>Coderhouse</span><a href="#experiencia">', '<span>Coderhouse</span><span>INTI</span><a href="#experiencia">')
    rows = ''.join(f'<article class="experience-row"><div class="experience-company"><h3>{text(company)}</h3><span>{text(dates)}</span></div><div><h4>{text(role)}</h4>{bullets(items)}</div></article>' for company,role,dates,items in JOBS)
    start = html.index('<div class="experience-list">')
    end = html.index('</section>', start)
    html = html[:start] + '<div class="experience-list">' + rows + '</div></div>' + html[end:]
    featured = '<div class="featured-projects">' + ''.join(f'<article class="featured-project"><p class="eyebrow">{text(status)}</p><h3>{text(name)}</h3>{bullets(items)}</article>' for name,status,items in PROJECTS) + '</div><h3 class="project-group-title">Otros proyectos web publicados</h3>'
    if '<div class="featured-projects">' not in html:
        html = html.replace('<div class="projects-grid">', featured + '<div class="projects-grid">', 1)
    html = html.replace('Algunos trabajos y desarrollos realizados en distintos rubros y contextos.', 'Iniciativas de IA y automatización en desarrollo, junto con sitios web publicados.')
    start=html.index('<div class="skills-grid">'); end=html.index('</section>',start)
    groups=[('Mobile','Flutter, Dart, React Native, Expo, Xamarin'),('Frontend y backend','JavaScript, React, Node.js, Java, Spring Boot, APIs REST'),('IA y automatización','LLM APIs, n8n, Make, RAG, Human-in-the-Loop')]
    cards=''.join(f'<article class="skill-card"><small>0{i+1}</small><h3>{text(name)}</h3><div class="skill-list">'+''.join('<span>'+text(skill)+'</span>' for skill in values.split(', '))+'</div></article>' for i,(name,values) in enumerate(groups))
    html=html[:start]+'<div class="skills-grid">'+cards+'</div><p class="tools-note">Datos y estado: <strong>SQL · SQLite · Firebase · Supabase · Redux Toolkit · RTK Query</strong><br>Trabajo en equipo: <strong>Git · GitHub · Jira · Scrum</strong></p></div>'+html[end:]
    html=html.replace('Trabajo con React y React Native para crear experiencias web y mobile. También exploro la integración de IA y la automatización con n8n y Make para ampliar las posibilidades de los productos.', 'Mi experiencia mobile incluye Flutter, Dart y Xamarin, junto con conocimientos de React y React Native. Diseño integraciones de modelos de lenguaje y automatizaciones con n8n y Make, incorporando validación humana en los flujos.')
    html=html.replace('Conversemos sobre oportunidades en desarrollo frontend y mobile.', 'Conversemos sobre desarrollo mobile, full stack e integración de IA.')
    html=html.replace('Mar del Plata, Argentina<br>Disponibilidad full time', 'Mar del Plata, Argentina<br>Mobile · Full Stack · IA')
    html=html.replace('Javier Gimenez · Frontend & Mobile Developer','Javier Gimenez · Mobile, Full Stack e IA')
    html=html.replace('<a href="cv.html" class="btn btn-primary">Ver currículum ↗</a>', '<a href="output/pdf/Javier_Gimenez_CV_2026.pdf" class="btn btn-primary" download>Descargar CV ↓</a>')
    p.write_text(html,encoding='utf-8')

def write_pdf():
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    ink=HexColor('#182c25'); muted=HexColor('#45564c'); green=HexColor('#346442')
    styles={
        'name':ParagraphStyle('name',fontName='Helvetica-Bold',fontSize=27,leading=30,textColor=ink,spaceAfter=5),
        'title':ParagraphStyle('title',fontName='Helvetica-Bold',fontSize=11.3,leading=15,textColor=green,spaceAfter=7),
        'contact':ParagraphStyle('contact',fontName='Helvetica',fontSize=8.8,leading=12,textColor=muted,spaceAfter=0),
        'section':ParagraphStyle('section',fontName='Helvetica-Bold',fontSize=10,leading=13,textColor=green,spaceBefore=12,spaceAfter=6),
        'body':ParagraphStyle('body',fontName='Helvetica',fontSize=9.4,leading=12.6,textColor=ink,spaceAfter=4),
        'job':ParagraphStyle('job',fontName='Helvetica-Bold',fontSize=9.7,leading=13,textColor=ink,spaceBefore=5,spaceAfter=3),
        'bullet':ParagraphStyle('bullet',fontName='Helvetica',fontSize=9.4,leading=12.6,textColor=ink,leftIndent=9,firstLineIndent=-7,spaceAfter=2),
    }
    story=[]
    def p(value,style='body'):return Paragraph(value,styles[style])
    story.extend([p('Javier Gimenez','name'),p(text(TITLE),'title'),p('Mar del Plata, Argentina | +54 11 5638 5296 | <link href="mailto:gimenezjavier.jig@gmail.com">gimenezjavier.jig@gmail.com</link>','contact'),p('<link href="https://www.linkedin.com/in/javier-gimenez-jig/">linkedin.com/in/javier-gimenez-jig</link> | <link href="https://github.com/javierzlafe">github.com/javierzlafe</link>','contact')])
    story.extend([p('PERFIL PROFESIONAL','section'),p(text(PROFILE))])
    story.append(p('EXPERIENCIA PROFESIONAL','section'))
    for company,role,dates,items in JOBS:
        story.append(KeepTogether([p(f'{text(company)} | {text(role)} <font color="#526256">| {text(dates)}</font>','job')]+[p('- '+text(x),'bullet') for x in items]))
    story.append(p('PROYECTOS E INICIATIVAS','section'))
    for name,status,items in PROJECTS:
        story.append(KeepTogether([p(f'{text(name)} | {text(status)}','job')]+[p('- '+text(x),'bullet') for x in items]))
    story.append(p('COMPETENCIAS TÉCNICAS','section'))
    story.append(p('<br/>'.join(f'<b>{text(a)}:</b> {text(b)}' for a,b in SKILLS)))
    story.append(p('INTELIGENCIA ARTIFICIAL Y AUTOMATIZACIÓN','section'))
    story.append(p('<br/>'.join(f'<b>{text(a)}:</b> {text(b)}' for a,b in AI)))
    doc=SimpleDocTemplate(str(OUTPUT),pagesize=A4,rightMargin=38,leftMargin=38,topMargin=32,bottomMargin=30,title='Javier Gimenez - CV 2026',author='Javier Gimenez')
    doc.build(story)
    reader=PdfReader(str(OUTPUT))
    if len(reader.pages)!=1: raise RuntimeError(f'Expected one page, got {len(reader.pages)}')
    content=reader.pages[0].extract_text()
    for token in ['Dicsys','GYL Group','INTI','Cropbase','Flutter','n8n']:
        assert token in content, token
    assert '\ufffd' not in content
    renders=ROOT/'tmp/pdfs';renders.mkdir(parents=True,exist_ok=True)
    pdf=pdfium.PdfDocument(str(OUTPUT))
    pdf[0].render(scale=1.7).to_pil().save(str(renders/'updated-1.png'))
    print(f'PDF validated: {len(reader.pages)} page, {len(content.split())} words, selectable text')

if __name__=='__main__':
    write_html()
    update_portfolio()
    write_pdf()
