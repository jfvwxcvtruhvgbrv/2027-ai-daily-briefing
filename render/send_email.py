"""Gmail SMTP로 그날 호 메일 발송.

환경변수: GMAIL_ADDRESS, GMAIL_APP_PASSWORD(16자리 앱 비밀번호), MAIL_TO(쉼표로 여러 명)
사용: python -m render.send_email 2026-11-09
실패하면 종료코드 1 → GitHub Actions 실패 알림 메일이 온다.
"""
import os
import smtplib
import sys
from email.message import EmailMessage
from pathlib import Path


def main(date, out="out"):
    sender = os.environ.get("GMAIL_ADDRESS")
    pw = os.environ.get("GMAIL_APP_PASSWORD")
    to = [x.strip() for x in os.environ.get("MAIL_TO", "").split(",") if x.strip()]
    if not (sender and pw and to):
        print("[ERROR] GMAIL_ADDRESS / GMAIL_APP_PASSWORD / MAIL_TO Secret이 비어 있습니다", file=sys.stderr)
        return 1
    o = Path(out)
    msg = EmailMessage()
    msg["Subject"] = (o / f"subject-{date}.txt").read_text(encoding="utf-8").strip()
    msg["From"] = f"AI 데일리 <{sender}>"
    msg["To"] = ", ".join(to)
    msg.set_content((o / f"email-{date}.txt").read_text(encoding="utf-8"))
    msg.add_alternative((o / f"email-{date}.html").read_text(encoding="utf-8"), subtype="html")
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, timeout=60) as s:
            s.login(sender, pw.replace(" ", ""))
            s.send_message(msg)
    except Exception as ex:
        print(f"[ERROR] 메일 발송 실패: {ex}", file=sys.stderr)
        return 1
    print(f"[INFO] 메일 발송 완료 → {', '.join(to)}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
