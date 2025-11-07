import cv2
import numpy as np
import time
try:
    import mediapipe as mp
except Exception:
    mp = None

try:
    import pyttsx3
except Exception:
    pyttsx3 = None


def draw_transparent_circle(img, center, radius, color, alpha=0.45):
    overlay = img.copy()
    cv2.circle(overlay, center, radius, color, -1)
    cv2.addWeighted(overlay, alpha, img, 1 - alpha, 0, img)


def blend_text_block(img, text_lines, origin, max_width, line_height=18):
    # aggressive: slightly tighter default line height to reduce vertical spacing
    x, y = origin
    font_scale = 0.58
    thickness = 1
    for i, line in enumerate(text_lines):
        cv2.putText(img, line, (x, y + i * line_height), cv2.FONT_HERSHEY_SIMPLEX, font_scale, (240, 240, 240), thickness, cv2.LINE_AA)


def wrap_text_to_width(text, font, scale, thickness, max_width):
    """Wrap a single paragraph of text into lines that fit within max_width pixels."""
    words = text.split()
    if not words:
        return [""]
    lines = []
    cur = words[0]
    for w in words[1:]:
        test = cur + ' ' + w
        (tw, th), _ = cv2.getTextSize(test, font, scale, thickness)
        if tw <= max_width:
            cur = test
        else:
            lines.append(cur)
            cur = w
    lines.append(cur)
    return lines


def main():
    if mp is None:
        print("mediapipe is required. Install: pip install mediapipe opencv-python numpy")
        return

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Cannot open camera")
        return

    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(min_detection_confidence=0.6, min_tracking_confidence=0.5, max_num_hands=1)
    mp_draw = mp.solutions.drawing_utils

    # Aura definitions: (relative_x, relative_y), color BGR
    aura_defs = {
        "academic": ((0.78, 0.18), (30, 220, 120)),       # top-right (greenish)
        "professional": ((0.22, 0.28), (200, 150, 250)),  # left-mid (light purple)
        "conversational": ((0.12, 0.75), (210, 120, 40)), # bottom-left (orange)
        "playful": ((0.6, 0.75), (40, 120, 220)),         # bottom-right (blue)
    }

    tone_texts = {
        "academic": "Explain the p-value in an academic tone:\nThe p-value quantifies the probability of observing data as extreme as, or more extreme than, the observed data, assuming the null hypothesis is true.",
        "professional": "Explain the p-value in a professional tone:\nThe p-value quantifies the probability of observing data as extreme as, or more extreme than, the observed data, assuming the null hypothesis is true.",
        "conversational": "Explain the p-value in a conversational tone:\nThink of the p-value as the chance your surprising result might just be luck — lower means less likely due to chance.",
        "playful": "Explain the p-value in a playful tone:\nIt's the chance your \"amazing\" finding is just a fluke, like finding a unicorn doing your laundry.",
    }

    # caption (shortened/clean)
    caption_lines = [
        "hand-tracked aura dial,  same prompt, different voices",
    ]

    last_spoken_tone = None
    tts_engine = None
    if pyttsx3 is not None:
        try:
            tts_engine = pyttsx3.init()
            tts_engine.setProperty('rate', 170)
        except Exception:
            tts_engine = None

    # tightening factor: values <1 bring elements closer (0.8 means 20% closer)
    TIGHTEN = 0.8

    prev_time = time.time()

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)
        h, w = frame.shape[:2]

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb)

        overlay = frame.copy()

        # draw title top-left (tighter)
        title_scale = 0.95 * max(0.8, TIGHTEN) * 0.95
        cv2.putText(overlay, "ai has auras, too", (18, 32), cv2.FONT_HERSHEY_DUPLEX, title_scale, (255, 255, 255), 2, cv2.LINE_AA)

        # draw aura blobs
        for name, (rel, color) in aura_defs.items():
            cx = int(rel[0] * w)
            cy = int(rel[1] * h)
            # aggressive: much smaller circles for a denser layout, scaled by TIGHTEN
            draw_transparent_circle(overlay, (cx, cy), int(0.08 * w * TIGHTEN), color, alpha=0.18)
            draw_transparent_circle(overlay, (cx, cy), int(0.05 * w * TIGHTEN), color, alpha=0.22)
            draw_transparent_circle(overlay, (cx, cy), int(0.03 * w * TIGHTEN), color, alpha=0.3)
            # bring label much closer to the aura center (20% closer)
            label_offset = int(10 * TIGHTEN)
            cv2.putText(overlay, name, (cx - label_offset, cy), cv2.FONT_HERSHEY_SIMPLEX, 0.56 * max(0.85, TIGHTEN), (230, 230, 230), 1, cv2.LINE_AA)

        pointer = None
        pointer_thumb = None
        pointer_index = None
        if results.multi_hand_landmarks:
            hand = results.multi_hand_landmarks[0]
            # choose landmark 8 (index tip) and 4 (thumb tip) to draw two dots
            lm_index = hand.landmark[8]
            lm_thumb = hand.landmark[4]
            ix, iy = int(lm_index.x * w), int(lm_index.y * h)
            tx, ty = int(lm_thumb.x * w), int(lm_thumb.y * h)
            pointer_index = (ix, iy)
            pointer_thumb = (tx, ty)

            # midpoint between thumb and index used as control pointer
            mx, my = int((ix + tx) / 2), int((iy + ty) / 2)
            pointer = (mx, my)

            # draw control points and connecting line (thumb and index)
            cv2.circle(overlay, pointer_index, 10, (255, 255, 255), -1)
            cv2.circle(overlay, pointer_thumb, 10, (255, 255, 255), -1)
            cv2.line(overlay, pointer_index, pointer_thumb, (255, 255, 255), 3)
            # small midpoint marker
            cv2.circle(overlay, pointer, 6, (230, 230, 230), -1)

        # compute tone weights based on pointer location
        weights = {k: 0.0 for k in aura_defs.keys()}
        if pointer is not None:
            px, py = pointer
            # compute inverse-distance weights
            invs = {}
            for k, (rel, _) in aura_defs.items():
                cx = int(rel[0] * w)
                cy = int(rel[1] * h)
                d = max(1.0, np.hypot(px - cx, py - cy))
                invs[k] = 1.0 / d
            s = sum(invs.values())
            if s > 0:
                for k in weights:
                    weights[k] = invs[k] / s

        # determine dominant tone
        dominant = max(weights.items(), key=lambda kv: kv[1])[0] if any(weights.values()) else "professional"

        # draw bracketed dominant label near its aura center (like [playful] in ref)
        dom_rel, _ = aura_defs[dominant]
        dom_cx = int(dom_rel[0] * w)
        dom_cy = int(dom_rel[1] * h)
        try:
            # bracketed label offset above the aura (moved closer by TIGHTEN)
            bracket_x = dom_cx - int(18 * TIGHTEN)
            bracket_y = dom_cy - int(20 * TIGHTEN)
            cv2.putText(overlay, f"[{dominant}]", (bracket_x, bracket_y), cv2.FONT_HERSHEY_SIMPLEX, 0.6 * max(0.85, TIGHTEN), (245, 245, 245), 2, cv2.LINE_AA)
        except Exception:
            pass

        # render right-side prompt box
        # panel sizing (slightly adjust for tightened layout)
        panel_w = int(0.36 * w)
        panel_x = w - panel_w - int(12 * max(0.7, TIGHTEN))  # less right margin when tightened
        panel_y = 60

        # prepare and wrap text to fit panel width
        font_scale = 0.58 * max(0.85, TIGHTEN)
        thickness = 1
        max_text_w = panel_w - 16
        raw_paras = tone_texts[dominant].split("\n")
        wrapped_lines = []
        for p in raw_paras:
            wrapped_lines.extend(wrap_text_to_width(p, cv2.FONT_HERSHEY_SIMPLEX, font_scale, thickness, max_text_w))

        # compute panel height based on wrapped lines
        line_height = int(20 * max(0.8, TIGHTEN))
        padding = 12
        panel_h = padding * 2 + line_height * max(1, len(wrapped_lines))

        panel = overlay.copy()
        cv2.rectangle(panel, (panel_x, panel_y), (panel_x + panel_w, panel_y + panel_h), (28, 28, 28), -1)
        cv2.addWeighted(panel, 0.65, overlay, 0.35, 0, overlay)
        # reduce panel padding so text sits tighter (and use tighter font scale)
        panel_text_x = panel_x + int(8 * max(0.8, TIGHTEN))
        panel_text_y = panel_y + padding
        blend_text_block(overlay, wrapped_lines, (panel_text_x, panel_text_y), max_text_w, line_height=line_height)

        # clean caption: draw a single short caption line near the bottom-left (tighter)
        blend_text_block(overlay, caption_lines, (18, h - 36), w - 36, line_height=int(14 * max(0.8, TIGHTEN)))

        cv2.imshow('Aura Dial', overlay)

        # speak on tone change (throttle)
        now = time.time()
        if tts_engine and dominant != last_spoken_tone and now - prev_time > 1.2:
            try:
                tts_engine.say(tone_texts[dominant].split('\n')[-1])
                tts_engine.runAndWait()
                last_spoken_tone = dominant
                prev_time = now
            except Exception:
                pass

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q') or key == 27:
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
