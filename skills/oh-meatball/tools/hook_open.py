import sys, subprocess, os, math, shutil
from PIL import Image, ImageDraw, ImageFont
src, out, start, cx, cy, z0, l1, l2, TY = sys.argv[1], sys.argv[2], float(sys.argv[3]), float(sys.argv[4]), float(sys.argv[5]), float(sys.argv[6]), sys.argv[7], sys.argv[8], int(sys.argv[9])
FPS=30; HOLD=1.5; END=2.2; N=int(END*FPS)+1
W,H=1080,1920
d=out+'_f'; shutil.rmtree(d,ignore_errors=True); os.makedirs(d)
subprocess.run(['ffmpeg','-v','error','-ss',str(start),'-i',src,'-frames:v',str(N),f'{d}/%04d.png'],check=True)
F=ImageFont.truetype('/home/user/skills/skills/oh-meatball/brand/fonts/Anton-Regular.ttf',150)
def ease(u): return u*u*(3-2*u)
def zoom(t):
    if t<HOLD: return z0*(1+0.06*t/HOLD)          # slow push-in
    u=min(1,(t-HOLD)/(END-HOLD)); zh=z0*1.06
    return zh+(1-zh)*ease(u)
def text(im,alpha):
    dr=ImageDraw.Draw(im)
    y=TY
    for s,col in ((l1,(255,255,255)),(l2,(255,205,40))):
        if not s: continue
        f=F; sz=150
        while dr.textlength(s,font=f)>960: sz-=6; f=ImageFont.truetype(F.path,sz)
        w=dr.textlength(s,font=f)
        dr.text(((W-w)/2,y),s,font=f,fill=col+(alpha,),stroke_width=12,stroke_fill=(0,0,0,alpha))
        y+=175
frames=sorted(os.listdir(d))
HS=os.environ.get('HOLDSRC')
if HS:
    a,b=map(float,HS.split(','))
    hd=out+'_h'; shutil.rmtree(hd,ignore_errors=True); os.makedirs(hd)
    subprocess.run(['ffmpeg','-v','error','-ss',str(a),'-i',src,'-t',str(b-a),f'{hd}/%04d.png'],check=True)
    hf=sorted(os.listdir(hd))
    for i,f in enumerate(frames):
        t=i/FPS
        if t<HOLD:
            j=min(len(hf)-1,int(t/HOLD*len(hf)))
            shutil.copy(f'{hd}/{hf[j]}',f'{d}/{f}')
for i,f in enumerate(frames):
    t=i/FPS; z=zoom(t)
    im=Image.open(f'{d}/{f}').convert('RGB')
    cw,ch=W/z,H/z
    # pan centre from target to frame centre as zoom→1
    k=(z-1)/(z0*1.06-1) if z0>1 else 0
    px=W/2+(cx*W-W/2)*min(1,k); py=H/2+(cy*H-H/2)*min(1,k)
    x0=min(max(px-cw/2,0),W-cw); y0=min(max(py-ch/2,0),H-ch)
    im=im.transform((W,H),Image.EXTENT,(x0,y0,x0+cw,y0+ch),Image.BICUBIC)
    a=255 if t<1.6 else int(255*max(0,(1.9-t)/0.3))
    ov=Image.new('RGBA',(W,H),(0,0,0,0)); text(ov,a)
    im=Image.alpha_composite(im.convert('RGBA'),ov).convert('RGB')
    im.save(f'{d}/{f}')
cut=start+(N)/FPS
subprocess.run(['ffmpeg','-v','error','-y','-framerate',str(FPS),'-i',f'{d}/%04d.png',
 '-ss',str(cut),'-i',src,'-ss',str(start),'-i',src,
 '-filter_complex','[0:v]setsar=1[a];[1:v]setsar=1,setpts=PTS-STARTPTS[b];[a][b]concat=n=2:v=1:a=0[v]',
 '-map','[v]','-map','2:a','-c:v','libx264','-preset','medium','-crf','19','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-shortest','-movflags','+faststart',out],check=True)
print('ok',out)
