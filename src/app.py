import time
import feedparser
from bs4 import BeautifulSoup
import html2text

from .journals import RSS_FEEDS
from .keywords import KEYWORDS
from .summarize import summarize_article
from .emailer import send_mail

def clean_html_to_text(html: str) -> str:
    """
    RSS 'summary' alanı çoğunlukla HTML içerir.
    Basit ve dayanıklı bir düz yazı dönüşümü yapalım.
    """
    if not html:
        return ""
    # Önce kaba HTML temizlik:
    soup = BeautifulSoup(html, "html.parser")
    # Kod blokları vs. çok uzunsa temizlenebilir
    for tag in soup(["script", "style"]):
        tag.decompose()
    h = str(soup)
    # html2text ile güvenli markdown->text dönüşümü
    h2t = html2text.HTML2Text()
    h2t.ignore_links = False
    h2t.body_width = 0
    text = h2t.handle(h)
    return text.strip()

def article_matches_keywords(title: str, summary_text: str) -> bool:
    base = (title + " " + summary_text).lower()
    return any(k.lower() in base for k in KEYWORDS)

def fetch_and_summarize() -> str:
    """
    Tüm RSS'leri gez, filtrele, özetle ve düz metin rapor üret.
    Dönen string boş değilse e-postaya gider.
    """
    report_parts = []
    print("Yeni makaleler kontrol ediliyor...")

    for journal, url in RSS_FEEDS.items():
        try:
            feed = feedparser.parse(url)
            entries = feed.entries or []
            section_parts = []

            for e in entries:
                title = getattr(e, "title", "").strip()
                summary_html = getattr(e, "summary", "") or getattr(e, "description", "")
                link = getattr(e, "link", "")

                if not title or not summary_html:
                    # Özeti olmayan girdileri atla
                    continue

                summary_text = clean_html_to_text(summary_html)
                if not article_matches_keywords(title, summary_text):
                    continue

                try:
                    bullets = summarize_article(title, summary_html)
                except Exception as ex:
                    print(f"OpenAI özetleme hatası ({title}): {ex}")
                    # Açık hata halinde orijinal özetten yararlan
                    bullets = f"- Özet bulunamadı/üretilemedi.\n- Orijinal metinden yararlanınız.\n- Link: {link}"

                section_parts.append(
                    f"**{title}**\n{bullets}\n\nMakaleyi Oku: {link}\n\n---\n"
                )

            if section_parts:
                report_parts.append(f"## {journal} - Yeni Makale Özetleri\n\n" + "".join(section_parts))

        except Exception as ex:
            print(f"RSS hatası ({journal}): {ex}")

    return "".join(report_parts).strip()

def main(run_forever: bool = False, interval_seconds: int = 7 * 24 * 60 * 60):
    """
    run_forever=False: tek seferlik çalıştırma (cron için ideal)
    run_forever=True : döngüde çalıştır (manuel/servis kullanımında)
    """
    while True:
        body = fetch_and_summarize()
        if body:
            try:
                send_mail(body)
                print("E-posta başarıyla gönderildi.")
            except Exception as ex:
                print(f"E-posta gönderme hatası: {ex}")
        else:
            print("Filtreye uyan yeni makale bulunamadı.")

        if not run_forever:
            break

        next_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time() + interval_seconds))
        print(f"Tamamlandı. Bir sonraki kontrol {next_time} ...")
        time.sleep(interval_seconds)

if __name__ == "__main__":
    # Varsayılan: tek seferlik (cron ile çağır)
    main(run_forever=False)
