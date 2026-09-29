import math, os
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
S=os.path.dirname(os.path.abspath(__file__)); OUT=os.path.join(S,'out')
INK='#16201D'; PAPER='#F3F6F4'; FACE='#E3E9E6'; AMBER='#E5924F'; AMBER_D='#A6501B'
TEAL='#1B6A6F'; TEAL_L='#57BFC2'; GREY='#78847E'

def text_path(fontfile, s, x, y, size, tracking=0):
    f=TTFont(os.path.join(S,fontfile)); gs=f.getGlyphSet(); cmap=f.getBestCmap(); upm=f['head'].unitsPerEm
    sc=size/upm; d=[]; cx=x
    for ch in s:
        g=cmap[ord(ch)]; pen=SVGPathPen(gs)
        gs[g].draw(TransformPen(pen,(sc,0,0,-sc,cx,y)))
        d.append(pen.getCommands()); cx+=gs[g].width*sc+tracking
    return ' '.join(d), cx-tracking-x

def knob(cx,cy,r,ang,ptr,body=INK,w=None):
    a=math.radians(ang-90); w=w or r*0.28
    x2=cx+math.cos(a)*r*0.72; y2=cy+math.sin(a)*r*0.72
    return (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{body}"/>'
            f'<line x1="{cx}" y1="{cy}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{ptr}" stroke-width="{w:.1f}" stroke-linecap="round"/>')

def glyph(detail=True, face=FACE, body=INK, ptr=AMBER, wave=AMBER, screw='#A6B1AC'):
    """Three 500-series faceplates in a rack: Pre-Amp, EQ, Compressor. Knobs turn up left to right."""
    out=[]; w,h,gap,y0=96,300,28,106; x0=256-(3*w+2*gap)/2
    angles=[-120,-15,95] if detail else [-110,0,110]
    for i in range(3):
        x=x0+i*(w+gap); cx=x+w/2
        out.append(f'<rect x="{x}" y="{y0}" width="{w}" height="{h}" rx="16" fill="{face}"/>')
        if detail:
            out.append(f'<circle cx="{cx}" cy="{y0+18}" r="6" fill="{screw}"/><circle cx="{cx}" cy="{y0+h-18}" r="6" fill="{screw}"/>')
            out.append(knob(cx,y0+86,31,angles[i],ptr,body))
            out.append(knob(cx,y0+170,21,-angles[2-i]*0.8,ptr,body))
            out.append(f'<rect x="{cx-22}" y="{y0+222}" width="44" height="14" rx="7" fill="{body}"/>')
            out.append(f'<circle cx="{cx-22+7+i*15}" cy="{y0+229}" r="5" fill="{ptr}"/>')
        else:
            out.append(knob(cx,y0+110,36,angles[i],ptr,body,w=12))
            out.append(f'<circle cx="{cx}" cy="{y0+215}" r="13" fill="{body}"/>')
    return ''.join(out)

def tile(inner, bg=INK, rx=112):
    return f'<rect width="512" height="512" rx="{rx}" fill="{bg}"/>'+inner

def bot(bg=TEAL):
    """Bot avatar: one faceplate as a face. Two knobs for eyes, a VU meter for a mouth."""
    x,y,w,h=146,70,220,372
    o=[f'<rect width="512" height="512" fill="{bg}"/>',
       f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="30" fill="{FACE}"/>',
       f'<circle cx="256" cy="{y+22}" r="7" fill="#A6B1AC"/><circle cx="256" cy="{y+h-22}" r="7" fill="#A6B1AC"/>',
       knob(206,y+120,34,-35,AMBER,INK,w=11), knob(306,y+120,34,35,AMBER,INK,w=11)]
    # VU meter
    mx,my,mw,mh=186,y+196,140,96
    o.append(f'<rect x="{mx}" y="{my}" width="{mw}" height="{mh}" rx="14" fill="{INK}"/>')
    cx,cy,R=256,my+mh-16,58
    def arc(a0,a1,col,sw):
        p=lambda a:(cx+R*math.cos(math.radians(a-90)),cy+R*math.sin(math.radians(a-90)))
        (x1,y1),(x2,y2)=p(a0),p(a1)
        return f'<path d="M{x1:.1f} {y1:.1f} A{R} {R} 0 0 1 {x2:.1f} {y2:.1f}" fill="none" stroke="{col}" stroke-width="{sw}" stroke-linecap="round"/>'
    o.append(arc(-50,22,FACE,7)); o.append(arc(28,50,AMBER,7))
    a=math.radians(12-90); o.append(f'<line x1="{cx}" y1="{cy}" x2="{cx+math.cos(a)*(R-6):.1f}" y2="{cy+math.sin(a)*(R-6):.1f}" stroke="{TEAL_L}" stroke-width="6" stroke-linecap="round"/><circle cx="{cx}" cy="{cy}" r="8" fill="{FACE}"/>')
    # antenna LED
    o.append(f'<line x1="256" y1="{y}" x2="256" y2="{y-26}" stroke="{FACE}" stroke-width="10" stroke-linecap="round"/><circle cx="256" cy="{y-36}" r="15" fill="{AMBER}"/>')
    # button row
    for i in range(3): o.append(f'<rect x="{206+i*36}" y="{y+h-68}" width="28" height="16" rx="5" fill="{INK}"/>')
    return ''.join(o)

def svg(body, w=512, h=512, title=''):
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img"><title>{title}</title>{body}</svg>\n'

def lockup(dark=False, stacked=False, name='UTS 500 SERIES', tag='EQUALISER · PRE-AMP · COMPRESSOR'):
    ink=FACE if dark else INK; sub=('#A6B1AC' if dark else GREY); acc=AMBER if dark else AMBER_D
    t1,w1=text_path('archivo800.ttf',name,0,0,100,-1)
    t2,w2=text_path('plex500.ttf',tag,0,0,30,3.2)
    mark=tile(glyph(),bg=INK if not dark else '#1D2523')
    if not stacked:
        W=512+60+max(w1,w2)+20; H=512
        body=(f'<g>{mark}</g>'
              f'<path transform="translate(572 262)" d="{t1}" fill="{ink}"/>'
              f'<rect x="574" y="296" width="{w2:.0f}" height="6" rx="3" fill="{acc}"/>'
              f'<path transform="translate(572 356)" d="{t2}" fill="{sub}"/>')
        return svg(body,round(W),H,'UTS 500 Series')
    W=max(w1,w2,512)+80; H=512+60+100+80+20
    mx=(W-512)/2
    body=(f'<g transform="translate({mx} 0)">{mark}</g>'
          f'<path transform="translate({(W-w1)/2:.1f} 660)" d="{t1}" fill="{ink}"/>'
          f'<path transform="translate({(W-w2)/2:.1f} 730)" d="{t2}" fill="{sub}"/>')
    return svg(body,round(W),round(H),'UTS 500 Series')

files={
 'uts500-mark.svg': svg(tile(glyph()),title='UTS 500 Series'),
 'uts500-mark-flat.svg': svg(glyph(face=INK,body=FACE,ptr=AMBER_D,screw='#78847E'),title='UTS 500 Series'),
 'favicon.svg': svg(tile('<g transform="translate(256 256) scale(1.22) translate(-256 -256)">'+glyph(detail=False)+'</g>',rx=96),title='UTS 500 Series'),
 'discord-server-icon.svg': svg(f'<rect width="512" height="512" fill="{INK}"/>'+glyph(),title='UTS 500 Series'),
 'discord-bot-avatar.svg': svg(bot(),title='UTS Bot'),
 'uts500-lockup-light.svg': lockup(False),
 'uts500-lockup-dark.svg': lockup(True),
 'uts500-lockup-stacked-light.svg': lockup(False,True),
 'uts500-lockup-stacked-dark.svg': lockup(True,True),
 'site-lockup-light.svg': lockup(False,name='UTS MINI MIXING DESK',tag='500 SERIES MODULE DOCUMENTATION'),
 'site-lockup-dark.svg': lockup(True,name='UTS MINI MIXING DESK',tag='500 SERIES MODULE DOCUMENTATION'),
}
for n,c in files.items(): open(os.path.join(OUT,n),'w').write(c)
print('ok', list(files))
