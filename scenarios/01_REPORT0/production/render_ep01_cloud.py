#!/usr/bin/env python3
"""EP01 automated Japanese-voice workprint render. NOT a final live-action film."""
import asyncio, csv, json, math, subprocess, sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import edge_tts

HERE=Path(__file__).resolve().parent
OUT=HERE/'build'; OUT.mkdir(exist_ok=True)
shots=list(csv.DictReader((HERE/'EP01_SHOTLIST.csv').open(encoding='utf-8-sig')))
speech=list(csv.DictReader((HERE/'EP01_TTS_KANA_LINES.csv').open(encoding='utf-8-sig')))
assert len(shots)==43 and len(speech)==39
assert sum(int(s['duration_s']) for s in shots)==510
START=[15.5,19.4,26.45,31.85,40,58.1,62.5,67.2,77,81.7,90.35,94.1,98.4,104.9,109.1,114,128,133.9,136,180,183.75,190.5,195,211,222,232.6,244,254,271,302,317,363,368,392,406,442,448,452,473]
END=[19.17,26.22,31.63,39.89,58,62.4,67.06,70.94,81.54,90.22,94.02,98.3,104.78,108.93,113.88,118.03,133.76,135.87,137.87,183.6,190.13,194.84,196.87,220.74,228.34,243.86,246.1,257.2,279.64,307.88,322.88,367.49,374.41,402.58,410.32,446.08,450.66,455.26,478.64]
assert len(START)==len(END)==39
FONTS=['/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc','/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf']
def ff(sz):
 for f in FONTS:
  if Path(f).exists():return ImageFont.truetype(f,sz)
 return ImageFont.load_default()
PAL={'01-01':('#08192c','#14799b'),'01-02':('#091e23','#1b8b83'),'01-03':('#180c16','#cc345a'),'01-04':('#0b1b32','#306f9c'),'01-05':('#091f30','#2a94ad'),'01-06':('#091e1c','#367c6f'),'01-07':('#180e28','#ae4168')}
SCENES={'01-01':'地下施設 / 予測','01-02':'閉鎖された通路','01-03':'21:19 / 公開系の判定','01-04':'再調査','01-05':'死亡ではなく受信断','01-06':'CAM03 / 本人性未確認','01-07':'REPORT ID:000 / 偽の音声'}
def rgb(h):return tuple(bytes.fromhex(h[1:]))
def make_frames():
 folder=OUT/'shots';folder.mkdir(exist_ok=True)
 concat=['ffconcat version 1.0']
 for i,shot in enumerate(shots):
  scene=shot['shot_id'][:5];b,c=map(rgb,PAL[scene])
  H,W=720,1280
  y=np.arange(H,dtype=np.float32)[:,None,None];x=np.arange(W,dtype=np.float32)[None,:,None]
  bg=np.array(b,dtype=np.float32)[None,None,:]
  a=np.array(c,dtype=np.float32)[None,None,:]
  mix=.15+.5*y/H+.12*x/W
  image=Image.fromarray(np.broadcast_to(bg*(1-mix)+a*mix*.25,(H,W,3)).astype('uint8'),'RGB')
  d=ImageDraw.Draw(image,'RGBA')
  d.rounded_rectangle((80,110,1200,567),radius=22,fill=(3,15,24,215),outline=(*c,225),width=3)
  if scene in ('01-01','01-02','01-03'):
   n=8 if scene=='01-01' else 2
   for j in range(n):
    xx=210+j*122 if n==8 else 410+j*400
    d.ellipse((xx-19,320,xx+19,359),fill=(1,8,17,255))
    d.rounded_rectangle((xx-24,354,xx+24,468),14,fill=(1,8,17,255))
   d.rounded_rectangle((435,150,885,287),9,fill=(6,27,40,240),outline=(*c,220),width=2)
   d.text((475,195),'INTERNAL / HOLD',font=ff(30),fill=(182,229,240,255))
   if scene=='01-03':d.text((480,248),'21:19 / PUBLIC',font=ff(25),fill=(231,112,139,255))
  elif scene in ('01-04','01-05'):
   for j in range(3):
    d.rectangle((190,205+j*93,780,255+j*93),fill=(18,46,66,230),outline=(67,154,177,180),width=2)
    d.line((220,226+j*93,360,215+j*93,470,233+j*93,710,220+j*93),fill=(100,193,203,255),width=3)
   d.ellipse((900,245,964,307),fill=(4,12,22,255))
   d.polygon((884,307,977,307,1025,478,838,478),fill=(4,12,22,255))
  elif scene=='01-06':
   d.ellipse((618,211,680,273),fill=(1,11,13,255))
   d.polygon((618,267,680,267,736,510,556,510),fill=(1,11,13,255))
   for j in range(23):
    d.line((95,135+j*18,1180,135+j*18),fill=(58,197,139,22),width=2)
   d.text((167,160),'CAM03  21:23:41',font=ff(25),fill=(145,208,177,255))
  else:
   for j,speaker in enumerate(['GEMMA','GLADIUS','ARCA']):
    xx=425+212*j
    d.ellipse((xx-55,240,xx+55,350),outline=(111+30*j,190-20*j,220,255),width=8)
    d.text((xx-67,380),speaker,font=ff(23),fill=(217,229,240,255))
   d.text((400,488),'PUBLIC / ARCHIVE REPLAY',font=ff(25),fill=(223,95,128,255))
  d.rectangle((0,0,W,78),fill=(1,7,14,242))
  d.text((53,22),'REPORT:0',font=ff(36),fill=(236,246,255,255))
  d.text((928,30),f'SCENE {scene}',font=ff(22),fill=(146,206,221,255))
  d.text((110,615),SCENES[scene],font=ff(29),fill=(226,237,242,255))
  d.text((110,677),'WORKPRINT / 43 CUTS / FINAL FOOTAGE PENDING',font=ff(14),fill=(146,150,163,255))
  file=folder/f'{i:03}.png';image.save(file)
  concat.extend([f"file '{file.resolve()}'",f"duration {shot['duration_s']}"])
 concat.append(f"file '{file.resolve()}'")
 (OUT/'shots.ffconcat').write_text('\n'.join(concat)+'\n')
def run(args):
 print('RUN',args[:9],flush=True)
 subprocess.run(args,check=True)
def duration(path):
 r=subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','default=nw=1:nk=1',str(path)],capture_output=True,text=True,check=True)
 return float(r.stdout.strip())
def srt():
 def fmt(t):
  ms=round(t*1000);hh,ms=divmod(ms,3600000);mm,ms=divmod(ms,60000);ss,ms=divmod(ms,1000)
  return f'{hh:02}:{mm:02}:{ss:02},{ms:03}'
 lines=[]
 for i,row in enumerate(speech):
  lines.append(f"{i+1}\n{fmt(START[i])} --> {fmt(END[i])}\n{row['tts_text_kana']}\n")
 (OUT/'episode1_kana.srt').write_text('\n'.join(lines),encoding='utf-8')
voices={'くろせ しゅうじ':'ja-JP-KeitaNeural','とうどう まこと':'ja-JP-KeitaNeural','かんざき れん':'ja-JP-KeitaNeural','ジェンマ':'ja-JP-KeitaNeural','グラディウス':'ja-JP-KeitaNeural','どうりょう':'ja-JP-KeitaNeural','にせ ジェンマ':'ja-JP-KeitaNeural','にせ グラディウス':'ja-JP-KeitaNeural'}
async def tts():
 folder=OUT/'voices';folder.mkdir(exist_ok=True)
 for row in speech:
  path=folder/(row['line_id']+'.mp3')
  if path.exists() and path.stat().st_size>1024:continue
  voice=voices.get(row['speaker_kana'],'ja-JP-NanamiNeural')
  # Distinct identity for each internal AI; same IDs in archive are broadcast imitations.
  persona={'ジェンマ':('ja-JP-KeitaNeural','-12Hz','-12%'),
           'グラディウス':('ja-JP-KeitaNeural','+12Hz','-5%'),
           'アルカ':('ja-JP-NanamiNeural','-12Hz','-14%'),
           'にせ ジェンマ':('ja-JP-KeitaNeural','-12Hz','-12%'),
           'にせ グラディウス':('ja-JP-KeitaNeural','+12Hz','-5%'),
           'にせ アルカ':('ja-JP-NanamiNeural','-12Hz','-14%')}
  voice,pitch,rate=persona.get(row['speaker_kana'],(voice,'+0Hz','-8%'))
  text=row['tts_text_kana'].replace('トレ、テサウルス','トレ、　テサウルス')
  for attempt in range(3):
   try:
    await edge_tts.Communicate(text,voice,rate=rate,pitch=pitch).save(str(path));break
   except Exception as e:
    if attempt==2:raise
    await asyncio.sleep(2**attempt)
  print('VOICE',row['line_id'],path.stat().st_size,flush=True)
def mix():
 video=OUT/'visual.mp4';cmd=['ffmpeg','-hide_banner','-nostdin','-y','-i',str(video)]
 filters=['[0:a]aformat=channel_layouts=stereo,volume=0.09[bg]']
 audit=[]
 for i,row in enumerate(speech):
  p=OUT/'voices'/(row['line_id']+'.mp3');cmd+=['-i',str(p)]
  clip_len=duration(p);space=END[i]-START[i]
  rate=max(1.,clip_len/max(.2,space-.1))
  # A long line must be flagged; avoid discarding any dialogue.
  if rate>1.18: raise RuntimeError(f"Speech too long {row['line_id']}: {clip_len:.1f}s, slot {space:.1f}s")
  delay=round(START[i]*1000)
  # Archive speaker replicas are low-bandwidth playback, distinct from real 3AI channels.
  speaker=row['speaker_kana']
  band=('highpass=f=420,lowpass=f=2500,' if speaker.startswith('にせ ') else
        'highpass=f=230,lowpass=f=4200,' if speaker in ('こうかいゲートウェイ','こうかいシステム') else
        '')
  filters.append(f'[{i+1}:a]aresample=48000,aformat=channel_layouts=stereo,{band}atempo={rate:.5f},volume=1.45,adelay={delay}|{delay}[v{i}]')
  audit.append({'line_id':row['line_id'],'voice_duration':round(clip_len,2),'speed':round(rate,3),'start':START[i],'qc_required':True,'speaker':row['speaker_kana'],'slot_end':END[i],'compression_flag':rate>1.10})
 filters.append('[bg]'+''.join(f'[v{i}]' for i in range(39))+'amix=inputs=40:duration=first:normalize=0,alimiter=limit=0.93[mix]')
 (OUT/'voice_alignment_qc.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2))
 cmd+=['-filter_complex',';'.join(filters),'-map','0:v:0','-map','[mix]','-c:v','copy','-c:a','aac','-b:a','192k','-ar','48000','-t','510','-movflags','+faststart',str(OUT/'EP01_JAPANESE_VOICE_WORKPRINT.mp4')]
 run(cmd)
def main():
 make_frames();srt()
 if not (OUT/'visual.mp4').exists():
  run(['ffmpeg','-hide_banner','-nostdin','-y','-safe','0','-f','concat','-i',str(OUT/'shots.ffconcat'),'-f','lavfi','-i','anoisesrc=color=brown:amplitude=0.018:sample_rate=48000:duration=510','-vf','fps=12,format=yuv420p','-c:v','libx264','-preset','veryfast','-crf','27','-r','12','-c:a','aac','-b:a','96k','-t','510','-movflags','+faststart',str(OUT/'visual.mp4')])
 assert abs(duration(OUT/'visual.mp4')-510)<.4
 asyncio.run(tts());mix()
 assert abs(duration(OUT/'EP01_JAPANESE_VOICE_WORKPRINT.mp4')-510)<.4
 print('PASS: 43 shots, 39 spoken lines, 510 seconds. This remains a workprint.')
if __name__=='__main__':main()
