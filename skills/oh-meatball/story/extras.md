# Oh Meatball - Zero-cost extras (the 3rd daily post)

Every extra is cut from footage we already paid for. They cost 0 vidIQ credits, need only `ffmpeg`, and render in under a minute.
Use them to keep the daily slot full, push viewers back to the story parts, and test hooks cheaply.

## File conventions
- `clips/ptNN.mp4`: the assembled, posted part (about 16 s; Pt 1 is 1080x1920, 24 fps, 48 kHz).
- `clips/ptNN_s1.mp4` and `clips/ptNN_s2.mp4`: the raw 8 s shots (shot 1 = setup, shot 2 = cliffhanger).
- To find which shot holds a line, a character or a gag, search `story/season1.md` (each part lists SHOT 1 and SHOT 2 with the speaker).
- Output goes to `extras/`. Caption text is written to `work/*.txt` so apostrophes and quotes never break `drawtext`.
- Every recipe re-encodes to 1080x1920, 24 fps, H.264 + AAC, and loudness-normalises to -14 LUFS.
- Keep top captions to 24 characters or fewer (they must fit 1080 px), and prefer raw `_s1`/`_s2` shots over assembled parts, which carry the burned-in "PART N+1 TOMORROW" text.
- Keep extras under 60 s. End every extra by pointing to the story: put "Watch Pt N" or "Full story on the channel" in the title or the pinned comment.

## Shared setup (run once per shell)
```bash
cd "${OM:-/home/user/skills/skills/oh-meatball}"
mkdir -p extras work
FONT=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf
NV="scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2,setsar=1,fps=24,format=yuv420p"
NA="aresample=48000,aformat=sample_fmts=fltp:channel_layouts=stereo"
ENC="-c:v libx264 -preset medium -crf 20 -pix_fmt yuv420p -r 24 -c:a aac -b:a 160k -ar 48000 -movflags +faststart"
TXT="fontfile=$FONT:fontcolor=white:borderw=6:bordercolor=black"
CX="x=(w-tw)/2"
cap(){ printf '%s' "$2" > "work/$1.txt"; }

# cut OUT "TOP CAPTION" SPEED spec...
#   spec = clip[:start[:duration[:label]]]   e.g. pt11_s1   pt04_s2:0:5   pt05_s2:5:3:#5
#   Concatenates the segments, applies SPEED (1 = normal, 1.5 = faster), puts TOP CAPTION on top
#   and an optional big LABEL near the bottom of each segment.
cut(){ local out=$1 capt=$2 sp=$3; shift 3; local in=() f="" c="" i=0 name st du lab
  for s in "$@"; do IFS=: read -r name st du lab <<<"$s"; local opt=()
    [ -n "$st" ] && opt+=(-ss "$st"); [ -n "$du" ] && opt+=(-t "$du")
    in+=("${opt[@]}" -i "clips/$name.mp4")
    local lf=""; [ -n "$lab" ] && { cap "lab$i" "$lab"; lf=",drawtext=$TXT:$CX:textfile=work/lab$i.txt:fontsize=150:y=h-520"; }
    f+="[$i:v]$NV,setpts=(PTS-STARTPTS)/$sp,fps=24$lf[v$i];[$i:a]$NA,atempo=$sp[a$i];"; c+="[v$i][a$i]"; i=$((i+1)); done
  cap cut "$capt"
  ffmpeg -v error -y "${in[@]}" -filter_complex "${f}${c}concat=n=$i:v=1:a=1[v][a];[v]drawtext=$TXT:$CX:textfile=work/cut.txt:fontsize=58:y=110[vo];[a]loudnorm=I=-14:TP=-1.5[ao]" \
    -map "[vo]" -map "[ao]" $ENC "extras/$out.mp4"; }
```

## Rotation
Day 1-3: Recap, Poll, Slow reaction. Day 4-6: Spotlight, Rewind, Detail zoom. Day 7-9: Supercut, Meme freeze, Iconic line.
Day 10-12: Cliffhanger countdown, Binge, Then vs now. Then repeat with newer parts. Double up on whichever format wins the Monday review.

---

## 1. "Previously on Oh Meatball" recap
The last 4 s of each of the 3 newest parts, behind a 1.5 s title card. Post it before the next story part to re-hook lapsed viewers.
```bash
cap r1 "PREVIOUSLY ON"; cap r2 "OH MEATBALL"; cap r3 "PART 13 IS NEXT"
ffmpeg -v error -y -f lavfi -i "color=c=0x1a0f0a:s=1080x1920:r=24:d=1.5" -f lavfi -t 1.5 -i "anullsrc=r=48000:cl=stereo" \
  -sseof -4 -i clips/pt10.mp4 -sseof -4 -i clips/pt11.mp4 -sseof -4 -i clips/pt12.mp4 -filter_complex "
[0:v]drawtext=$TXT:$CX:textfile=work/r1.txt:fontsize=80:y=h/2-130,drawtext=$TXT:$CX:textfile=work/r2.txt:fontsize=120:fontcolor=orange:y=h/2,setsar=1,format=yuv420p[t];[1:a]$NA[a0];
[2:v]$NV[v1];[2:a]$NA[a1];[3:v]$NV[v2];[3:a]$NA[a2];[4:v]$NV[v3];[4:a]$NA[a3];
[t][a0][v1][a1][v2][a2][v3][a3]concat=n=4:v=1:a=1[v][a];
[v]drawtext=$TXT:$CX:textfile=work/r3.txt:fontsize=70:y=h-300:enable='gte(t,10.5)'[vo];[a]loudnorm=I=-14:TP=-1.5[ao]" \
  -map "[vo]" -map "[ao]" $ENC extras/recap_pt10-12.mp4
```
Title template: `Previously on Oh Meatball... 😱 | Pts {A}-{B} Recap` / `Catch up before Pt {N} drops 🍝 | Oh Meatball`

## 2. Character spotlight ("Every {character} line")
Every shot in which one character speaks, back to back (6 shots = 48 s). Rotate: Smokey, Grandma Shelly, Biscuit, Pip, Baron.
```bash
# Smokey speaks in: Pt 4 S1, 6 S2, 8 S2, 15 S2, 24 S1, 27 S2 (from season1.md)
cut spotlight_smokey "EVERY SMOKEY LINE" 1 pt04_s1 pt06_s2 pt08_s2 pt15_s2 pt24_s1 pt27_s2
```
Title template: `Every {Character} line so far {emoji} | Oh Meatball` / `{Character} is the real main character? {emoji} | Oh Meatball`

## 3. "Who's right?" poll cut
Two opposing shots (one per side of an argument), then a 3 s split-screen freeze: "WHO'S RIGHT? COMMENT 1 OR 2". Built for comments.
```bash
cap p1 "TEAM BISCUIT?"; cap p2 "TEAM MEATBALL?"; cap p3 "WHO'S RIGHT?"; cap p4 "COMMENT 1 OR 2"
A=clips/pt21_s1.mp4; B=clips/pt21_s2.mp4
HALF="scale=1080:960:force_original_aspect_ratio=increase,crop=1080:960,setsar=1"
ffmpeg -v error -y -i $A -i $B -sseof -0.3 -i $A -sseof -0.3 -i $B -f lavfi -t 3 -i "anullsrc=r=48000:cl=stereo" -filter_complex "
[0:v]$NV,drawtext=$TXT:$CX:textfile=work/p1.txt:fontsize=80:y=200[v0];[0:a]$NA[a0];
[1:v]$NV,drawtext=$TXT:$CX:textfile=work/p2.txt:fontsize=80:y=200[v1];[1:a]$NA[a1];
[2:v]trim=end_frame=1,loop=71:1:0,setpts=N/24/TB,$HALF,drawtext=$TXT:text=1:fontsize=140:x=60:y=60[t];
[3:v]trim=end_frame=1,loop=71:1:0,setpts=N/24/TB,$HALF,drawtext=$TXT:text=2:fontsize=140:x=60:y=60[b];
[t][b]vstack,fps=24,format=yuv420p,drawtext=$TXT:$CX:textfile=work/p3.txt:fontsize=100:y=h/2-150:box=1:boxcolor=black@0.5,drawtext=$TXT:$CX:textfile=work/p4.txt:fontsize=70:y=h/2+10[v2];[4:a]$NA[a2];
[v0][a0][v1][a1][v2][a2]concat=n=3:v=1:a=1[v][a];[a]loudnorm=I=-14:TP=-1.5[ao]" \
  -map "[v]" -map "[ao]" $ENC extras/poll_pt21.mp4
```
Good pairs: Pt 21 (Biscuit vs Meatball), Pt 8 (Mama vs Smokey), Pt 10 (sign or not), Pt 18 (is Duchess evil?).
Title template: `Who's right: {A} or {B}? 🤔 | Oh Meatball` / `Team {A} or Team {B}? Comment 1 or 2 👇`

## 4. Slowed dramatic reaction
A 5 s reveal at half speed with a slow push-in and a two-stage caption ("WAIT FOR IT..." then the quote). Use it for the biggest twist of the week.
```bash
cap d1 "WAIT FOR IT..."; cap d2 "\"Baron is your father.\""
ffmpeg -v error -y -ss 3 -t 5 -i clips/pt22_s2.mp4 -filter_complex "
[0:v]$NV,setpts=2*(PTS-STARTPTS),fps=24,zoompan=z='min(zoom+0.0012,1.25)':d=1:x='iw/2-iw/zoom/2':y='ih/2-ih/zoom/2':s=1080x1920:fps=24,
drawtext=$TXT:$CX:textfile=work/d1.txt:fontsize=72:y=200:enable='lt(t,4)',drawtext=$TXT:$CX:textfile=work/d2.txt:fontsize=64:y=h-420:enable='gte(t,4)'[v];
[0:a]$NA,atempo=0.5,loudnorm=I=-14:TP=-1.5[a]" -map "[v]" -map "[a]" $ENC extras/slow_pt22.mp4
```
Title template: `Watch {character}'s face in slow motion 😱 | Oh Meatball Pt {N}` / `The moment everything changed 💔 | Oh Meatball`

## 5. Running-gag supercut
Every instance of one recurring gag. Spaghetti: Pt 3 S1, 4 S2, 7 S2, 11 S1, 17 S1, 27 S1. Also works for "every Grandma Shelly gossip" (Pt 5, 13, 29) and "Biscuit being a terrible spy" (Pt 11, 12, 19).
```bash
cut supercut_spaghetti "EVERY TIME MEATBALL STRESS-EATS" 1 pt03_s1 pt04_s2:0:5 pt07_s2 pt11_s1 pt17_s1 pt27_s1
```
Title template: `Every time Meatball stress-eats spaghetti 🍝 | Oh Meatball` / `{Gag} supercut: it never stops 😂 | Oh Meatball`

## 6. Cliffhanger countdown ("Rank these")
The last 3 s of five shot-2 cliffhangers, labelled #5 to #1. Viewers argue about the ranking in the comments.
```bash
cut cliffhangers_1 "RANK THESE CLIFFHANGERS" 1 pt05_s2:5:3:#5 pt09_s2:5:3:#4 pt14_s2:5:3:#3 pt18_s2:5:3:#2 pt22_s2:5:3:#1
```
Title template: `Rank these cliffhangers 1-5 😱 | Oh Meatball` / `The {N} most shocking moments so far 🔥 | Oh Meatball`

## 7. "Wait... go back" rewind
Play a shot, rewind 3 s at 2x in black and white with "WAIT... GO BACK", then replay that moment at half speed with a pointer caption. Best for subtle reactions (Duchess in Pt 18, the window in Pt 17).
```bash
cap w1 "WAIT... GO BACK"; cap w2 "LOOK AT DUCHESS'S FACE"
C=clips/pt18_s2.mp4
ffmpeg -v error -y -i $C -ss 4 -t 3 -i $C -ss 4 -t 3 -i $C -filter_complex "
[0:v]$NV[v0];[0:a]$NA[a0];
[1:v]$NV,reverse,setpts=(PTS-STARTPTS)/2,fps=24,hue=s=0,drawtext=$TXT:$CX:textfile=work/w1.txt:fontsize=90:y=h/2[v1];[1:a]$NA,areverse,atempo=2[a1];
[2:v]$NV,setpts=2*(PTS-STARTPTS),fps=24,drawtext=$TXT:$CX:textfile=work/w2.txt:fontsize=64:y=220[v2];[2:a]$NA,atempo=0.5[a2];
[v0][a0][v1][a1][v2][a2]concat=n=3:v=1:a=1[v][a];[a]loudnorm=I=-14:TP=-1.5[ao]" \
  -map "[v]" -map "[ao]" $ENC extras/rewind_pt18.mp4
```
Title template: `Wait... go back and look at {character} 👀 | Oh Meatball Pt {N}` / `Nobody noticed this in Pt {N} 🤯`

## 8. "Did you catch this?" detail zoom
Play up to time T, freeze for 1 s with a red box around a detail, then 2 s zoomed into that detail. Set T, X and Y by eye (X/Y = top-left of a 540x960 box in 1080x1920 space).
```bash
T=5.5; X=540; Y=200
cap c1 "DID YOU CATCH THIS?"
ffmpeg -v error -y -t $T -i clips/pt17_s2.mp4 -ss $T -i clips/pt17_s2.mp4 -f lavfi -t 3 -i "anullsrc=r=48000:cl=stereo" -filter_complex "
[0:v]$NV[v0];[0:a]$NA[a0];
[1:v]$NV,trim=end_frame=1,split[f1][f2];
[f1]loop=23:1:0,setpts=N/24/TB,drawbox=x=$X:y=$Y:w=540:h=960:color=red:t=12[z1];
[f2]crop=540:960:$X:$Y,scale=1080:1920,setsar=1,loop=47:1:0,setpts=N/24/TB,drawtext=$TXT:$CX:textfile=work/c1.txt:fontsize=80:y=200[z2];
[z1][z2]concat=n=2:v=1:a=0,format=yuv420p[fz];[2:a]$NA[a2];
[v0][a0][fz][a2]concat=n=2:v=1:a=1[v][a];[a]loudnorm=I=-14:TP=-1.5[ao]" \
  -map "[v]" -map "[ao]" $ENC extras/detail_pt17.mp4
```
Title template: `Did you catch this in Pt {N}? 👀 | Oh Meatball` / `The clue everyone missed 🧐 | Oh Meatball`

## 9. Meme freeze-frame
Play a funny moment, freeze on the best face, punch in 1.3x and hit a synthetic bass "boom", with a relatable POV caption on top. Pure shareability.
```bash
T=6; cap m1 "ME AFTER ONE SLIGHTLY BAD DAY"
ffmpeg -v error -y -t $T -i clips/pt11_s1.mp4 -ss $T -i clips/pt11_s1.mp4 -f lavfi -t 2.5 -i "sine=f=55:sample_rate=48000" -filter_complex "
[0:v]$NV[v0];[0:a]$NA[a0];
[1:v]$NV,trim=end_frame=1,loop=59:1:0,setpts=N/24/TB,crop=iw/1.3:ih/1.3,scale=1080:1920,setsar=1,format=yuv420p[v1];
[2:a]volume=4,afade=t=out:st=0.05:d=1.2,$NA[a1];
[v0][a0][v1][a1]concat=n=2:v=1:a=1[v][a];[v]drawtext=$TXT:$CX:textfile=work/m1.txt:fontsize=66:y=170[vo];[a]loudnorm=I=-14:TP=-1.5[ao]" \
  -map "[vo]" -map "[ao]" $ENC extras/meme_pt11.mp4
```
Title template: `{relatable POV} 😂 | Oh Meatball` / `Meatball is all of us 🍝`

## 10. Binge catch-up ("Parts A-B in 60 seconds")
Five assembled parts back to back at 1.5x (5 x 16 s / 1.5 = 53 s). Converts new viewers who landed mid-season.
```bash
cut binge_01-05 "PARTS 1-5 IN 60 SECONDS" 1.5 pt01 pt02 pt03 pt04 pt05
```
Title template: `Oh Meatball Parts {A}-{B} in 60 seconds ⏩` / `Missed it? The whole story so far 🍿 | Oh Meatball`

## 11. Iconic line x3 ("Say it again")
One quotable line three times: normal, black and white, then slow with a punch-in. Pick lines people quote in comments ("You picked the cute one", "Twenty minutes", "Get the dog").
```bash
cap i1 "SAY IT AGAIN, SMOKEY"
ffmpeg -v error -y -ss 3.5 -t 3 -i clips/pt08_s2.mp4 -filter_complex "
[0:v]$NV,split=3[a][b][c];[0:a]$NA,asplit=3[x][y][z];
[b]hue=s=0[b2];[c]setpts=2*PTS,fps=24,crop=iw/1.3:ih/1.3,scale=1080:1920,setsar=1[c2];[z]atempo=0.5[z2];
[a][x][b2][y][c2][z2]concat=n=3:v=1:a=1[v][au];[v]drawtext=$TXT:$CX:textfile=work/i1.txt:fontsize=72:y=200[vo];[au]loudnorm=I=-14:TP=-1.5[ao]" \
  -map "[vo]" -map "[ao]" $ENC extras/iconic_pt08.mp4
```
Title template: `"{line}" 💀 | Oh Meatball` / `The line that broke the comments 😭 | Oh Meatball Pt {N}`

## 12. Then vs now split-screen
Two matching shots stacked (top = earlier part, bottom = later part), each labelled, audio mostly from the newer one. Strongest for the wedding (Pt 1 vs Pt 30) and the porch (Pt 4 vs Pt 21).
```bash
cap n1 "PART 1"; cap n2 "PART 30"
HALF="scale=1080:960:force_original_aspect_ratio=increase,crop=1080:960,setsar=1"
ffmpeg -v error -y -i clips/pt01_s1.mp4 -i clips/pt30_s1.mp4 -filter_complex "
[0:v]$NV,$HALF,drawtext=$TXT:$CX:textfile=work/n1.txt:fontsize=70:y=40[t];
[1:v]$NV,$HALF,drawtext=$TXT:$CX:textfile=work/n2.txt:fontsize=70:y=40[b];
[t][b]vstack,format=yuv420p[v];
[0:a]$NA,volume=0.35[a0];[1:a]$NA[a1];[a0][a1]amix=inputs=2:duration=shortest:normalize=0,loudnorm=I=-14:TP=-1.5[a]" \
  -map "[v]" -map "[a]" -t 8 $ENC extras/then_now_01-30.mp4
```
Title template: `Part 1 vs Part 30: look how far they came 🥹 | Oh Meatball` / `Same porch, different story 💔 | Oh Meatball`

---

## Description for every extra (2 lines + tags)
```
{one-line hook}. Full story: Oh Meatball Pt 1 is on the channel - new part every day!
#shorts #catdrama #ai #animation #cat #ohmeatball
```
Pin a comment linking the newest story part. Never post an extra in the same hour as a story part.
