# -*- coding: utf-8 -*-
import io, sys

SRC = "/sessions/jolly-gallant-cannon/mnt/uploads/index.html"
OUT = "/sessions/jolly-gallant-cannon/mnt/outputs/index.html"

s = io.open(SRC, encoding="utf-8").read()

def row(tid, tags, th, en, steps, thx, enx, sev):
    steps_html = "".join(
        '<li><span class="bi-th">{}</span><span class="bi-en">{}</span></li>'.format(a, b)
        for a, b in steps
    )
    return (
        '<tr id="row-{tid}" class="tc-row"><td class="tc-id">{tid}</td>'
        '<td class="tc-name">{tags}<span class="bi-th-name">{th}</span><span class="bi-en-name">{en}</span></td>'
        '<td class="tc-steps"><ol>{steps}</ol></td>'
        '<td class="tc-expected"><span class="bi-th-exp">{thx}</span><span class="bi-en-exp">{enx}</span></td>'
        '<td class="col-sev"><span class="sev-tag sev-{sev}">{sevU}</span></td>'
        '<td class="result-cell"><select class="result-select" data-id="{tid}" onchange="saveResult(this)">'
        '<option value="">—</option><option value="pass">✅ Pass</option>'
        '<option value="fail">❌ Fail</option><option value="blocked">⚠️ Blocked</option>'
        '<option value="na">N/A</option></select></td>'
        '<td><input class="notes-line" type="text" data-notes="{tid}" placeholder="หมายเหตุ..." oninput="saveNote(this)"></td></tr>'
    ).format(tid=tid, tags=tags, th=th, en=en, steps=steps_html, thx=thx, enx=enx,
             sev=sev, sevU=sev.upper())

NEW = '<span class="tag tag-new">v3.0 New</span>'
UI = '<span class="tag tag-ui">UI</span>'
HW = '<span class="tag tag-hardware">Hardware</span>'
CP = '<span class="tag tag-critical">Critical Path</span>'
DSLR = '<span class="tag tag-dslr">DSLR</span>'
NEGT = '<span class="tag tag-negative">Negative</span>'

rows = []

# A — UI / NAVIGATION CONSOLIDATION
rows.append(row("TC-UI-101", NEW+UI,
  "รวม icon เป็นอันเดียว — ต้องเปิด Config ก่อนจึงใช้งานได้",
  "Consolidated single icon — requires opening Config first",
  [("เปิดแอป ดูแถบเครื่องมือ", "Open app, inspect toolbar"),
   ("กด icon รวม", "Click the consolidated icon"),
   ("เปิด Config แล้วลองใช้อีกครั้ง", "Open Config, retry")],
  "เหลือ icon เดียวแทนชุดเดิม · เมนู/ฟังก์ชันเข้าถึงได้หลังเปิด Config · ไม่มี icon ซ้ำซ้อน",
  "Single icon replaces the old set. Functions reachable after Config opens. No duplicate icons.", "p2"))

rows.append(row("TC-UI-102", NEW+UI,
  "ย้าย Video Result + Sticker Page ไปอยู่ใน Event / Frame / Media",
  "Video Result & Sticker page relocated into Event/Frame/Media",
  [("เปิด Event → Frame → Media", "Open Event → Frame → Media"),
   ("หา Video Result และ Sticker settings", "Locate Video Result & Sticker settings"),
   ("ตรวจว่าหน้าเดิมถูกย้ายออก", "Confirm old standalone pages removed")],
  "ตั้งค่า Video Result และ Sticker อยู่ใน Media ของ Frame · ไม่มีหน้าเดิมแยกซ้ำ · ค่าเดิมยังคงอยู่",
  "Both settings live under Frame's Media tab. No duplicate legacy pages. Existing values preserved.", "p2"))

rows.append(row("TC-UI-103", NEW+UI,
  "Event Page ย้ายไปเป็น setting ภายในหน้า EVENT",
  "Event Page moved to be a setting inside the EVENT screen",
  [("เปิดหน้า EVENT", "Open EVENT screen"),
   ("หา setting ของ Event Page", "Find Event Page setting"),
   ("แก้ค่า แล้ว save", "Edit value, save")],
  "Event Page เป็น setting ย่อยในหน้า EVENT · แก้แล้ว save ค่าคงอยู่ · ไม่มี navigation เดิมที่กำพร้า",
  "Event Page is a sub-setting of EVENT. Edits save & persist. No orphaned old nav entry.", "p2"))

# B — CAMERA
rows.append(row("TC-C-101", NEW+HW,
  "Warning dialog: เปิดโปรแกรมโดยไม่ได้ต่อกล้อง",
  "Warning dialog on launch when no camera connected",
  [("ถอดกล้องทั้งหมด", "Disconnect all cameras"),
   ("เปิดแอป", "Launch app"),
   ("สังเกต dialog ที่ขึ้น", "Observe dialog shown")],
  "แสดง warning 'ไม่พบกล้อง' ชัดเจน อ่านเข้าใจ · ไม่ crash · มีทางไปต่อ/ลองใหม่",
  "Clear 'No camera detected' warning. No crash. Provides retry / next step.", "p1"))

rows.append(row("TC-C-102", NEW+HW+CP,
  "Global Camera Rotation — ปรับครั้งเดียว apply ทุก Frame / ทุกช่อง",
  "Global camera rotation applies to every frame & slot at once",
  [("มี Event ที่มีหลาย Frame หลายช่อง", "Event with multiple frames & slots"),
   ("ตั้ง Global Rotation = 90°", "Set global rotation = 90°"),
   ("เปิดดูทุก Frame", "Inspect all frames")],
  "ทุก Frame/ช่องหมุน 90° พร้อมกันจากการตั้งครั้งเดียว · ไม่ต้องแก้ทีละกล่อง · บันทึกค่าได้",
  "All frames/slots rotate 90° from a single setting. No per-slot editing needed. Value persists.", "p1"))

rows.append(row("TC-C-103", NEW+DSLR,
  "Default Camera Setup อ่านค่าตรงจาก hardware (1200D / 1300D)",
  "Default camera setup reads values directly from hardware",
  [("ต่อ Canon 1200D/1300D", "Connect Canon 1200D/1300D"),
   ("เปิดแอป โหลด default setup", "Open app, load default setup"),
   ("เทียบค่าที่แสดงกับค่าจริงบนกล้อง", "Compare shown values vs. on-camera")],
  "ค่า default อ่านตรงจากกล้อง ตรงกับ hardware · ภาพถ่ายในแสงปกติไม่มืด/ไม่เพี้ยน",
  "Defaults read live from hardware & match. Photos in normal light not dark/skewed.", "p2"))

rows.append(row("TC-C-104", NEW+HW+NEGT,
  "Camera lost connection: popup loop ต้องไม่ติดค้าง — ออก/จัดการได้",
  "Camera lost-connection popup must not trap the user in a loop",
  [("กำลังใช้งานหน้าถ่าย", "In capture screen"),
   ("ทำให้กล้อง lost connection", "Force camera lost connection"),
   ("ลองปิด popup / ออกจากหน้า", "Try to dismiss popup / exit page")],
  "popup แจ้ง lost connection ที่ถูกต้อง (ไม่ใช่ 'หา object ไม่เจอ') · ปิด/ออกจากหน้าได้ ไม่วน loop ค้าง",
  "Correct lost-connection popup (not 'object not found'). Dismissable; no infinite loop / stuck screen.", "p1"))

# C — PRINTER & FRAME
rows.append(row("TC-P-101", NEW,
  "Margin box แสดงแนวตั้งเมื่อสลับเป็น Portrait",
  "Margin box renders vertically when switched to Portrait",
  [("ไป Printer settings", "Open Printer settings"),
   ("สลับ orientation เป็น Portrait", "Switch orientation to Portrait"),
   ("ดูกล่อง margin", "Inspect margin box")],
  "กล่อง margin ปรับเป็นแนวตั้งตาม Portrait อัตโนมัติ · ค่าถูกต้อง · งานพิมพ์ออกตรง margin",
  "Margin box flips to vertical for Portrait automatically. Values correct. Print respects margins.", "p2"))

rows.append(row("TC-EF-101", NEW,
  "Preview frame พร้อม thumbnail (รูปพรีวิว 1, 2, 3, 4)",
  "Frame preview shows thumbnails 1/2/3/4",
  [("สร้าง/เปิด Frame ที่มีหลายช่อง", "Open frame with multiple slots"),
   ("ดูหน้า preview frame", "View frame preview screen")],
  "แสดงกรอบพร้อม thumbnail พรีวิวลำดับ 1,2,3,4 ครบ · ตรงกับ shot จริง · โหลดไว",
  "Frame shown with preview thumbnails 1–4. Matches actual shots. Loads quickly.", "p2"))

# D — EVENT SETUP
rows.append(row("TC-SET-101", NEW,
  "Event Search — ค้นหา Event จากรายการได้",
  "Event search filters the event list",
  [("มี Event หลายรายการ", "Have multiple events"),
   ("พิมพ์คำค้นในช่อง search", "Type a query in search box")],
  "รายการกรองตามคำค้นแบบ real-time · ค้นจากชื่อ/วันที่ได้ · ไม่มีรายการผิด",
  "List filters in real time by name/date. Correct matches only.", "p2"))

rows.append(row("TC-SET-102", NEW,
  "Export ผลการค้นหา Event",
  "Export event search results",
  [("ค้นหา Event ให้ได้ผลลัพธ์", "Run an event search"),
   ("กด Export", "Click Export"),
   ("เปิดไฟล์ที่ได้", "Open exported file")],
  "Export เฉพาะผลที่ค้นเจอ · ไฟล์เปิดได้ ข้อมูลครบถูกต้อง · ไม่รวม event ที่ไม่ตรงคำค้น",
  "Exports only matched results. File opens, data complete & correct. Excludes non-matches.", "p3"))

rows.append(row("TC-SET-103", NEW+CP,
  "Export / Import Event พร้อม checkbox เลือก Event",
  "Export/Import events with selection checkboxes",
  [("เลือก Event ด้วย checkbox บางรายการ", "Tick some events via checkbox"),
   ("Export → ไปอีกเครื่อง → Import", "Export → other machine → Import"),
   ("ตรวจ Event ที่นำเข้า", "Verify imported events")],
  "Export เฉพาะที่ติ๊ก · Import คืนค่า Event ครบ (frame/media/setting) · ไม่ทับของเดิมผิด · ไม่ corrupt",
  "Exports only ticked events. Import restores them fully (frames/media/settings). No wrong overwrite or corruption.", "p1"))

# E — MONETIZATION
rows.append(row("TC-PAY-101", NEW,
  "Multi-Cam เป็นฟีเจอร์เสียเงินเพิ่ม (tier-gated)",
  "Multi-Cam is a paid add-on, gated by tier",
  [("ใช้บัญชีที่ไม่มีสิทธิ์ Multi-Cam", "Account without Multi-Cam entitlement"),
   ("ลองเปิด Multi-Cam", "Attempt to enable Multi-Cam"),
   ("ปลดล็อกด้วยสิทธิ์/จ่ายเงิน แล้วลองอีกครั้ง", "Unlock via entitlement, retry")],
  "ถ้าไม่มีสิทธิ์ → ใช้ Multi-Cam ไม่ได้ + แจ้ง upgrade ชัดเจน · เมื่อมีสิทธิ์ → ใช้ได้ปกติ · ไม่ bypass ได้",
  "No entitlement → Multi-Cam blocked with clear upgrade prompt. With entitlement → works. No bypass.", "p2"))

rows.append(row("TC-PAY-102", NEW,
  "Migrate Coupon จากระบบ SIXSHEET เดิมมาระบบใหม่",
  "Migrate coupons from legacy SIXSHEET system",
  [("มีคูปองในระบบเดิม", "Coupons exist in legacy system"),
   ("รัน migration", "Run migration"),
   ("ใช้คูปองที่ย้ายมาในบูธ", "Redeem a migrated coupon in booth")],
  "คูปองเดิมถูกย้ายครบ · สถานะ (ใช้แล้ว/คงเหลือ) ถูกต้อง · ใช้ในระบบใหม่ได้ · ไม่ซ้ำ/ไม่หาย",
  "All legacy coupons migrated. Status (used/remaining) correct. Redeemable in new system. No dup/loss.", "p3"))

rows_html = "\n".join(rows)

MODULE16 = (
'\n<!-- ════════════════════════════════ -->\n'
'<!-- MODULE 16 — v3.0.0 ADDITIONS: COVERAGE GAPS               -->\n'
'<!-- 14 cases for v3.0.0 features not covered by Modules 01-15. -->\n'
'<!-- ═════════════════════════════════ -->\n'
'<div class="section-title" id="mod16">MODULE 16 — v3.0.0 ADDITIONS: COVERAGE GAPS <span class="th-h">รายการเพิ่ม v3.0.0 — ฟีเจอร์ที่ยังไม่มีใน Module 01–15</span></div>\n'
'<div class="section-subtitle">เฉพาะฟีเจอร์ v3.0.0 / 3.0.0-c ที่ยังไม่ถูกครอบคลุม · อ้างอิงจาก Feature Backlog (Google Sheet) · Consolidate Icon · Video/Sticker Relocate · Event Page Setting · No-Camera Warning · Global Rotation · Default Camera Setup · Lost-Connection Popup · Portrait Margin · Frame Thumbnail · Event Search/Export/Import · Multi-Cam Tier · Coupon Migration</div>\n'
'<div class="test-module"><div class="module-header"><div><span class="module-name">v3.0.0 ADDITIONS — COVERAGE GAPS</span><br><span class="mod-th">เคสเสริมสำหรับฟีเจอร์ 3.0.0 ที่ยังไม่มีใน suite หลัก</span></div><span class="module-count">14 cases</span></div>\n'
"<table><thead><tr><th class='col-id'>ID</th><th class='col-test'>Test Case<span class='col-th'>รายการทดสอบ</span></th><th class='col-steps'>Steps<span class='col-th'>ขั้นตอน</span></th><th class='col-expected'>Expected Result<span class='col-th'>ผลที่คาดหวัง</span></th><th class='col-sev'>Sev</th><th class='col-result'>Result<span class='col-th'>ผล</span></th><th class='col-notes'>Notes<span class='col-th'>หมายเหตุ</span></th></tr></thead><tbody>\n"
+ rows_html +
'\n</tbody></table></div>\n'
'<div class="critical-alert" style="margin-top:16px;"><span class="sev">v3.0.0 NEW</span><div class="content"><div class="title">Module 16 — 14 v3.0.0 Additions (coverage gaps)</div><div class="detail">UI/Navigation: Consolidate Icon (1) · Video+Sticker Relocate (1) · Event Page Setting (1). Camera: No-Camera Warning (1) · Global Rotation (1) · Default Setup from HW (1) · Lost-Connection Popup (1). Printer/Frame: Portrait Margin (1) · Frame Thumbnail (1). Event Setup: Search (1) · Export Search (1) · Export/Import Event (1). Monetization: Multi-Cam Tier-gated (1) · Coupon Migration (1). ทุกเคสอ้างอิงจาก Feature Backlog และไม่ซ้ำกับ 193 cases เดิม · ID เริ่มที่ 101 เพื่อไม่ชนของเดิม.</div><span class="det-th">14 รายการฟีเจอร์ 3.0.0 ที่ยังไม่ถูกครอบคลุมใน Module อื่น</span></div></div>\n\n\n'
)

# --- Insert Module 16 before CRITICAL FINDINGS section ---
anchor = '<div class="section-title">CRITICAL FINDINGS — P0/P1 TRACKER'
assert anchor in s, "anchor not found"
s = s.replace(anchor, MODULE16 + anchor, 1)

# --- Update totals ---
s = s.replace("const TOTAL=193;", "const TOTAL=207;", 1)
s = s.replace("193 Test Cases · 15 Modules", "207 Test Cases · 16 Modules", 1)
s = s.replace('<div class="sum-item total"><div class="num">193</div>',
              '<div class="sum-item total"><div class="num">207</div>', 1)
s = s.replace('<strong id="cnt-empty">193</strong>', '<strong id="cnt-empty">207</strong>', 1)
s = s.replace('<span class="filter-count" id="fc-all">193</span>',
              '<span class="filter-count" id="fc-all">207</span>', 1)
s = s.replace('<span class="filter-count" id="fc-empty">193</span>',
              '<span class="filter-count" id="fc-empty">207</span>', 1)
# title attribute
s = s.replace('<title>CAP*TURES v1.0 — Test Suite v4 TH/EN</title>',
              '<title>CAP*TURES v1.0 — Test Suite v4 TH/EN (+v3.0.0 Additions)</title>', 1)

io.open(OUT, "w", encoding="utf-8").write(s)

# sanity checks
import re
ids = sorted(set(re.findall(r'TC-[A-Z]+-\d+', s)))
sel = s.count('class="result-select"')
print("written:", OUT)
print("total result-selects:", sel)
print("module16 present:", 'id="mod16"' in s)
print("TOTAL=207 present:", "const TOTAL=207;" in s)
print("new ids present:", [i for i in ["TC-UI-101","TC-UI-102","TC-UI-103","TC-C-101","TC-C-102","TC-C-103","TC-C-104","TC-P-101","TC-EF-101","TC-SET-101","TC-SET-102","TC-SET-103","TC-PAY-101","TC-PAY-102"] if i in s])
