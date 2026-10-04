import cv2, numpy as np
A = cv2.imread('/root/.claude/uploads/67a85adb-e901-5ab7-ad58-b6a573ad9b24/46e85240-image.jpg', 0)
B = cv2.imread('/root/.claude/uploads/67a85adb-e901-5ab7-ad58-b6a573ad9b24/ba88a3ab-image.png', 0)[380:1700, :]
tpl0 = cv2.resize(A[70:360, 15:420], None, fx=0.55, fy=0.55, interpolation=cv2.INTER_AREA)  # the bowl
base = 0.65/0.55
def search(angles, scales):
    best = None
    for a in angles:
        M = cv2.getRotationMatrix2D((tpl0.shape[1]/2, tpl0.shape[0]/2), a, 1.0)
        cs, sn = abs(M[0,0]), abs(M[0,1])
        nw = int(tpl0.shape[0]*sn + tpl0.shape[1]*cs); nh = int(tpl0.shape[0]*cs + tpl0.shape[1]*sn)
        M[0,2] += nw/2 - tpl0.shape[1]/2; M[1,2] += nh/2 - tpl0.shape[0]/2
        rot  = cv2.warpAffine(tpl0, M, (nw, nh))
        mk   = cv2.warpAffine(np.full(tpl0.shape, 255, np.uint8), M, (nw, nh))
        for s in scales:
            t = cv2.resize(rot, None, fx=s, fy=s, interpolation=cv2.INTER_AREA)
            m = cv2.resize(mk,  None, fx=s, fy=s, interpolation=cv2.INTER_AREA)
            if t.shape[0] >= B.shape[0] or t.shape[1] >= B.shape[1]: continue
            r = np.nan_to_num(cv2.matchTemplate(B, t, cv2.TM_CCORR_NORMED, mask=m), nan=0, posinf=0)
            _, mx, _, loc = cv2.minMaxLoc(r)
            if best is None or mx > best[0]: best = (mx, a, s, loc)
    return best
mx, a, s, loc = search(np.arange(14, 46, 2.0), np.arange(base*0.85, base*1.2, 0.04))
print(f'coarse: corr {mx:.4f}  a={a:+.1f}  s={s:.3f}')
mx, a, s, loc = search(np.arange(a-2.5, a+2.6, 0.5), np.arange(s*0.94, s*1.07, 0.015))
print(f'fine  : corr {mx:.4f}  a={a:+.2f}  s={s:.3f}  at {loc}')
print()
print(f'rotate the trace frame {a:+.2f} deg CCW to reach north-up')
print(f'=> PAGE UP  = true bearing {(-a) % 360:.1f} deg')
print(f'=> PAGE +X  = true bearing {(-a + 90) % 360:.1f} deg')
