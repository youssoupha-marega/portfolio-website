import os

import django
from django.test import Client


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project_site.settings")
django.setup()


def main():
    print("\n=== TEST EN DIRECT DES PAGES ===\n")

    client = Client()
    urls = [
        ("/profil/nom=yama-sakho&profession=data-analyst/projets/", "Projets"),
        ("/profil/nom=yama-sakho&profession=data-analyst/services/", "Services"),
        ("/profil/nom=yama-sakho&profession=data-analyst/blog/", "Blog"),
    ]

    for url, page_name in urls:
        print(f"\nPage {page_name}: {url}")
        try:
            response = client.get(url)
            if response.status_code == 200:
                content = response.content.decode("utf-8")

                import re

                match = re.search(r'<h1[^>]*class="section-title"[^>]*>(.*?)</h1>', content, re.DOTALL)
                if match:
                    title_html = match.group(1)
                    title_text = re.sub(r"<[^>]+>", "", title_html).strip()
                    print(f"  Titre trouve: '{title_text}'")
                else:
                    print("  Titre non trouve dans le HTML")
                    if "{{ site_profile" in content:
                        print("  Code Django brut detecte dans le HTML")
            else:
                print(f"  Erreur {response.status_code}")
        except Exception as exc:
            print(f"  Exception: {exc}")


if __name__ == "__main__":
    main()
