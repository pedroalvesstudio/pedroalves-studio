#!/usr/bin/env python3
"""Build a faithful, Spanish-localized Kodara page from the original Mooni Webflow HTML.
Preserve the original DOM hierarchy/classes, Webflow IX, Flowbase widgets and GSAP.
"""
import os, re, json, urllib.request, urllib.parse, colorsys, hashlib
from bs4 import BeautifulSoup, NavigableString

URL='https://mooni-webflow-template.webflow.io/'
DEST='projetos/mooni'
os.makedirs(DEST+'/assets',exist_ok=True)
req=urllib.request.Request(URL,headers={'User-Agent':'Mozilla/5.0 (compatible; PedroAlvesStudio/1.0)'})
with urllib.request.urlopen(req,timeout=60) as response: source=response.read().decode('utf-8')
soup=BeautifulSoup(source,'html.parser')
assert len(soup.select('section.section-large'))>=10, 'Original source incomplete'
assert soup.select_one('.carousel-horizontal') and soup.select_one('.w-slider'), 'Original carousel or testimonials missing'
assert len(soup.select('.w-tab-link'))>=4, 'Original rotating tabs missing'

translations={
'All plans are':'Todos los planes tienen','30% OFF':'30 % DE DESCUENTO','for a limited time!':'¡por tiempo limitado!','www.mooni.com':'www.kodara.dev',
'Home':'Inicio','Contact':'Contacto','Licence':'Licencia','Contact Sales':'Hablar con ventas',
'Mooni Fuels Innovation':'Kodara impulsa la innovación','Pioneering Cutting Edge Software':'Creamos software de última generación','Solutions':'Soluciones',
'Mooni helps developers write cleaner, faster and more reliable code. Optimize performance, catch issues early, and ship with confidence.':'Kodara ayuda a los desarrolladores a escribir código más limpio, rápido y fiable. Optimiza el rendimiento, detecta problemas a tiempo y publica con confianza.',
'Get Started':'Empezar','it’s free':'es gratis','Making development effortless for':'Simplificamos el desarrollo para','2,500+ companies':'más de 2500 empresas',
'Empower Innovation!':'¡Impulsa la innovación!','The perfect balance of speed and security':'El equilibrio perfecto entre velocidad y seguridad',
'Shorten review cycles and reduce back-and-forth with smart code suggestions and automated checking.':'Acorta las revisiones y reduce las idas y venidas con sugerencias inteligentes de código y comprobaciones automáticas.',
'Uptime that never misses a commit. Zero interruptions.':'Disponibilidad constante para cada commit. Sin interrupciones.',
'Lines of code analyzed and optimized for maintainability.':'Líneas de código analizadas y optimizadas para facilitar el mantenimiento.',
'Developers powered by Mooni. Join our growing community.':'Desarrolladores que trabajan con Kodara. Únete a nuestra comunidad.',
'Performance issues resolved. Catch and fix slowdowns.':'Problemas de rendimiento resueltos. Detecta y elimina las ralentizaciones.',
'Smarter Development':'Desarrollo más inteligente',
'Ship faster without sacrificing quality, boost performance and stability.':'Publica más rápido sin sacrificar calidad, rendimiento ni estabilidad.',
'Refactor Automation':'Refactorización automática',
'Scale your code base in seconds. Upgrade structure and consistency with refactor actions.':'Escala tu código en segundos. Mejora su estructura y consistencia con acciones de refactorización.',
'Live Feedback':'Comentarios en tiempo real',
'Get instant improvements as you write. Mooni flags weak spots, risks and readability issues.':'Recibe mejoras al escribir. Kodara señala puntos débiles, riesgos y problemas de legibilidad.',
'Performance Insights':'Análisis de rendimiento','Track speed, memory and render performance.':'Controla la velocidad, la memoria y el rendimiento de renderizado.',
'Clean Code':'Código limpio','Mooni helps you keep your code clean from the 1st commit.':'Kodara te ayuda a mantener tu código limpio desde el primer commit.',
'Error Prevention':'Prevención de errores','Catch mistakes in logic and risky patterns early.':'Detecta a tiempo errores de lógica y patrones de riesgo.',
'Mooni Our Pricing':'Precios de Kodara','Mooni Pricing Plans':'Planes y precios de Kodara','Monthly':'Mensual','Yearly':'Anual',
'Standard Plan':'Plan Estándar','Choose a plan for better code.':'Elige un plan para escribir mejor código.',
'Plus Plan':'Plan Plus','Discover all Mooni has to offer.':'Descubre todo lo que Kodara puede ofrecerte.',
'/ Month':'/ mes',
'Enhance your workflow with smart code suggestions and core insights.':'Mejora tu flujo de trabajo con sugerencias inteligentes de código y análisis esenciales.',
'Unlock advanced performance analytics and priority support for seamless scaling.':'Accede a análisis avanzados de rendimiento y asistencia prioritaria para crecer sin complicaciones.',
'30 day':'30 días de','60 day':'60 días de','activity logs':'historial de actividad',
'analysis runs per month':'análisis al mes','Core integrations included':'Integraciones esenciales incluidas',
'Smart code suggestions':'Sugerencias inteligentes de código','Email support':'Soporte por correo',
'Advanced integrations + API access':'Integraciones avanzadas y acceso API','Collaborative team features':'Funciones de colaboración en equipo','Priority support':'Soporte prioritario',
'Mooni Our FAQs':'Preguntas frecuentes de Kodara','Questions & Answers':'Preguntas y respuestas',
'Questions about getting started? Here’s everything you need to know about how Mooni helps you write cleaner and more reliable code.':'¿Quieres empezar? Aquí tienes todo lo que necesitas saber para escribir código más limpio y fiable con Kodara.',
'What is Mooni and who is it for?':'¿Qué es Kodara y para quién está pensado?',
'Does Mooni integrate with my existing tools?':'¿Kodara se integra con mis herramientas?',
'Can Mooni help with performance optimization?':'¿Puede Kodara optimizar el rendimiento?',
'How do I get started?':'¿Cómo puedo empezar?',
'Yes. Mooni connects seamlessly with modern development environments and version control platforms, so you can improve code without changing your workflow.':'Sí. Kodara se integra con entornos de desarrollo modernos y plataformas de control de versiones para mejorar tu código sin cambiar tu flujo de trabajo.',
'More questions? Visit our':'¿Más preguntas? Visita nuestra','docs':'documentación','or':'o','send us a message':'escríbenos',
'Mooni Integrations':'Integraciones de Kodara','Integrate your favorite tools':'Integra tus herramientas favoritas',
'Mooni connects with your favorite tools so you can automate tasks and keep you projects in sync.':'Kodara se conecta con tus herramientas favoritas para automatizar tareas y mantener tus proyectos sincronizados.',
'Sync your development workflow across':'Sincroniza tu flujo de desarrollo entre','devices.':'dispositivos.',
'Automate code tasks with thousands of':'Automatiza tareas de código con miles de','connected integrations':'integraciones conectadas',
'Send Mooni':'Envía los','reports and insights':'informes y análisis de Kodara','directly to Lunio.':'directamente a Lunio.',
'Collaborate, track and analyze performance in':'Colabora, supervisa y analiza el rendimiento con',
'Get instant code':'Recibe al instante','alerts and updates':'alertas y novedades de código','within Vanta.':'en Vanta.',
'Optimize creative and':'Optimiza proyectos creativos e','interactive projects':'interactivos','for better performance.':'para obtener un mejor rendimiento.',
'Real Feedback':'Opiniones reales','Mooni Testimonials':'Testimonios sobre Kodara',
'Real stories from teams transforming workflows with Mooni.':'Experiencias de equipos que transforman su manera de trabajar con Kodara.',
'Developer':'Desarrollador','Before Mooni,':'Antes de Kodara,',
'managing our operations felt like juggling too many balls at once. Now, everything is consolidated into one simple yet powerful platform.':'gestionar nuestras operaciones parecía hacer malabares. Ahora todo está reunido en una plataforma sencilla y potente.',
'Mooni has completely revolutionized how':'Kodara ha transformado por completo cómo','our team works.':'trabaja nuestro equipo.',
'The intuitive design and robust features allowed':'Su diseño intuitivo y sus funciones avanzadas nos permitieron',
'us to streamline':'simplificar','complex workflows that used to take hours. We were able to onboard new team members in record time.':'procesos complejos que antes requerían horas. Incorporamos a nuevos miembros del equipo en tiempo récord.',
'Stars out of 5':'Estrellas sobre 5','4 minutes':'4 minutos','Response time':'Tiempo de respuesta','See 96+ Reviews':'Ver más de 96 opiniones',
'Stay in the Dev Loop Now':'Mantente al día del desarrollo',
'Get early access to updates, feature rollouts, and roadmap insights. Stay ahead by knowing what’s coming next.':'Accede antes que nadie a novedades, funciones y nuestra hoja de ruta. Descubre lo que viene.',
'Exclusive Developer Perks Access':'Ventajas exclusivas para desarrolladores',
'Enjoy benefits like early API access, beta features, and priority support. Get hands-on experience with Mooni.':'Disfruta de acceso anticipado a la API, funciones beta y soporte prioritario. Prueba Kodara en primicia.',
'Track Real-Time Project Progress':'Sigue el progreso de tus proyectos en tiempo real',
'Follow development milestones and get transparent project updates. Stay informed about each phase.':'Sigue los hitos y recibe actualizaciones claras sobre el progreso de cada proyecto.',
'Shape the Future of Mooni Together':'Construyamos juntos el futuro de Kodara',
'Contribute feedback, suggest features, and help refine the platform. Your insights help us build better tools.':'Comparte tus ideas, propone funciones y ayúdanos a mejorar la plataforma.',
'Start Your':'Empieza tu','7-day free trial':'prueba gratuita de 7 días','Free 7-day trial':'7 días de prueba gratis','No credit card required':'Sin tarjeta de crédito',
'From 300+ Customer Reviews':'Basado en más de 300 opiniones',
'Empowering developers to write better code, ship faster, and perform smarter. From first commit to final deploy.':'Ayudamos a los desarrolladores a escribir mejor código, publicar más rápido y optimizar el rendimiento. Del primer commit al despliegue final.',
'Features':'Funciones','Code Analysis':'Análisis de código','Auto Refactor Tools':'Herramientas de refactorización','Error Detection':'Detección de errores','New':'Nuevo',
'Individual Developers':'Desarrolladores independientes','Startups':'Startups','Engineering Teams':'Equipos de ingeniería',
'Enterprise Plans':'Planes para empresas','Resources':'Recursos','Style Guide':'Guía de estilo','Changelog':'Registro de cambios',
'Define the pattern':'Marca el camino','Privacy Policy':'Política de privacidad','Terms of Service':'Términos de servicio',
}
# Start with the untouched source to retain exact hierarchy and data-w-id triggers.
for node in soup.find_all(string=True):
    if not isinstance(node,NavigableString) or node.parent.name in ('script','style','svg','noscript','title'):continue
    original=str(node)
    normalized=original.strip()
    if not normalized:continue
    text=translations.get(normalized)
    if text is None:
        text=re.sub(r'\bMooni\b','Kodara',normalized,flags=re.I)
        if text==normalized:continue
    before=original[:len(original)-len(original.lstrip())]
    after=original[len(original.rstrip()):]
    node.replace_with(before+text+after)
for tag in soup.find_all(True):
    if tag.has_attr('alt'):
        tag['alt']=re.sub('mooni','Kodara',tag['alt'],flags=re.I)
    if tag.name=='a' and tag.get('href','') in ('/contact','/utilities/licence','/utilities/404','/utilities/style-guide','/utilities/changelog'):
        tag['href']='#'
    if tag.name=='a' and tag.get('href')=='/':tag['href']='#inicio'
    if tag.has_attr('aria-current'):del tag['aria-current']
    if tag.has_attr('class') and 'w--current' in tag['class']:tag['class']=[c for c in tag['class'] if c!='w--current']

soup.html['lang']='es'
soup.title.string='kodara — Plataforma inteligente para desarrolladores'
for meta in soup.select('meta[name="description"],meta[property="og:description"],meta[name="twitter:description"]'):
    meta['content']='Kodara acelera tu desarrollo con análisis inteligente, refactorización y herramientas para crear software de calidad.'
for meta in soup.select('meta[property="og:title"],meta[name="twitter:title"]'):
    meta['content']='kodara — Desarrollo inteligente'
# Distinct original symbol: interlocking code chevrons inside an open ring.
symbol='''<svg viewBox="0 0 48 48" xmlns="http://www.w3.org/2000/svg" aria-hidden="true"><rect x="2" y="2" width="44" height="44" rx="13" fill="#6BE7BD"/><path d="M19 15L10 24L19 33M29 15L38 24L29 33M27 11L21 37" fill="none" stroke="#0A1720" stroke-width="3.4" stroke-linejoin="round" stroke-linecap="round"/></svg>'''
brand='<span class="kodara-wordmark">'+symbol+'<span>kodara</span></span>'
for navimg in soup.select('a.nav-logo img'):
    navimg.replace_with(BeautifulSoup(brand,'html.parser'))
# Replacement for embedded original wordmark in footer, not images in content cards.
for img in soup.select('img'):
    if 'mooni' in (img.get('alt','')+' '+img.get('src','')).lower() and ('logo' in img.get('class',[]) or 'logo' in img.get('alt','').lower()):
        img.replace_with(BeautifulSoup(brand,'html.parser'))
for img in soup.select('.footer-logo img,.footer-brand img'):
    img.replace_with(BeautifulSoup(brand,'html.parser'))
# Avoid marketing claims presented as real customers/testimonials for a fictional demo brand.
for el in soup.find_all(string=True):
    if '© Flowbase.' in str(el):el.replace_with('© 2026 kodara · Diseño y desarrollo: PedroAlves Studio')
    if str(el).strip()=='www.mooni.com':el.replace_with('www.kodara.dev')
# Preserve distinct structures but disable links to nonexistent template utility pages.
for a in soup.select('a[href^="/"]'):
    if a.get('href') not in ('/','#inicio'):a['href']='#'
main=soup.select_one('section.section-large')
if main:main['id']='inicio'

# Restore exact original external styling, scripts and plugin behavior, but vendor the CSS
# into our own assets to apply palette adjustments without touching geometry.
styles=soup.select('link[rel="stylesheet"][href*="mooni-webflow-template.shared"]')
def transform_hex(m):
    hx=m.group(0)
    raw=hx[1:]
    if len(raw) not in (3,6,8):return hx
    try:
        if len(raw)==3:raw=''.join(c*2 for c in raw)
        rgb=[int(raw[i:i+2],16) for i in (0,2,4)]
        h,s,v=colorsys.rgb_to_hsv(*[x/255 for x in rgb])
        # Transform only oranges/reds of the original palette; neutral contrast preserved.
        if (h<.13 or h>.975) and s>.47 and v>.22:
            nh=.443 # mint-green teal
            ns=min(.90,max(.50,s))
            nrgb=colorsys.hsv_to_rgb(nh,ns,v)
            result='#'+''.join(f'{int(x*255):02x}' for x in nrgb)
            if len(raw)==8:result+=raw[6:]
            return result
    except:pass
    return hx
for link in styles:
    old=link['href']
    try:
        css=urllib.request.urlopen(urllib.request.Request(old,headers={'User-Agent':'Mozilla/5.0'}),timeout=40).read().decode('utf-8')
        css=re.sub(r'#[a-fA-F0-9]{3,8}\b',transform_hex,css)
        with open(DEST+'/assets/kodara-original.css','w') as f:f.write(css)
        link['href']='./assets/kodara-original.css'
    except Exception as exc:
        print('CSS vendor fallback:',exc)
# Keep original Webflow scripts to preserve native interactions and GSAP/Flowbase.
style=soup.new_tag('style',id='kodara-brand-palette')
style.string='''
:root{--kodara-primary:#6BE7BD;--kodara-muted:#9AF4D6}
.kodara-wordmark{display:inline-flex;gap:10px;align-items:center;color:#F7FBFC;font-family:Parkinsans,Inter,sans-serif;font-weight:700;letter-spacing:-.055em;font-size:25px;white-space:nowrap}
.kodara-wordmark svg{width:37px;height:37px;display:block;flex-shrink:0}
.nav-logo{display:inline-flex;align-items:center}
.text-color-gradient-brand{background-image:linear-gradient(110deg,#6BE7BD 20%,#B1FCE6 85%)!important;-webkit-background-clip:text!important;background-clip:text!important;color:transparent!important}
.badge-primary,.banner-badge{border-color:rgba(107,231,189,.5)!important;color:#85F4D1!important}
.hero-background,.bg-lights{filter:hue-rotate(118deg) saturate(.83)}
.hero-button-border,.circle-gradient{filter:hue-rotate(120deg)}
::selection{background:#6BE7BD;color:#071820}
.w-webflow-badge{display:none!important}
@media(max-width:479px){.kodara-wordmark{font-size:21px}.kodara-wordmark svg{width:32px;height:32px}}
'''
soup.head.append(style)
for bad in soup.select('a.w-webflow-badge'):bad.decompose()
# Don't reference old corporate domain or visual identity.
for link in soup.select('link[rel="shortcut icon"],link[rel="apple-touch-icon"]'):link.decompose()
favicon=soup.new_tag('link',rel='icon',type='image/svg+xml',href='./assets/kodara-icon.svg')
soup.head.append(favicon)
open(DEST+'/assets/kodara-icon.svg','w').write(symbol)
output='<!DOCTYPE html>\n'+str(soup)
with open(DEST+'/index.html','w',encoding='utf-8') as f:f.write(output)
test=BeautifulSoup(output,'html.parser')
checks={
 'sections':len(test.select('section.section-large')),
 'testimonial_slider':len(test.select('.w-slider')),
 'rotating_tabs':len(test.select('.w-tab-link')),
 'ticker':len(test.select('[fb-carousel]')),
 'pricing_cards':len(test.select('[class*="pricing"]')),
 'language':test.html.get('lang'),
 'title':test.title.text,
 'source_bytes':len(source),'output_bytes':len(output)
}
print('KODARA_BUILD',json.dumps(checks,ensure_ascii=False))
assert checks['sections']>=10 and checks['testimonial_slider']>=1 and checks['rotating_tabs']>=4 and checks['ticker']>=1
