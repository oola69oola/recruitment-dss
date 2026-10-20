import os
import time
from playwright.sync_api import sync_playwright

DOCS_DIR = os.path.abspath("docs")
os.makedirs(DOCS_DIR, exist_ok=True)

CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

def capture_all():
    with sync_playwright() as p:
        browser = p.chromium.launch(
            executable_path=CHROME_PATH,
            headless=True,
            args=["--disable-web-security", "--no-sandbox"]
        )
        context = browser.new_context(
            viewport={"width": 1440, "height": 900},
            device_scale_factor=1.5
        )
        
        # Inject mock user session to allow direct access to dashboard
        context.add_init_script("""
            localStorage.setItem('recruitiq_user', JSON.stringify({
                id: 'recruiter-admin-1',
                email: 'hr.director@recruitiq.io',
                first_name: 'Dr. Sarah',
                last_name: 'Adeyemi',
                organization: 'Enterprise Talent Operations'
            }));
            localStorage.setItem('recruitiq_theme', 'light');
        """)
        
        page = context.new_page()

        # 1. Landing Page
        print("Capturing Landing Page...")
        page.goto("http://localhost:5173/#home", wait_until="networkidle")
        time.sleep(1)
        page.screenshot(path=os.path.join(DOCS_DIR, "screenshot_landing_page.png"), full_page=False)

        # 2. Login View
        print("Capturing Login View...")
        page.goto("http://localhost:5173/#login", wait_until="networkidle")
        time.sleep(1)
        page.screenshot(path=os.path.join(DOCS_DIR, "screenshot_login_view.png"), full_page=False)

        # 3. Dashboard - Step 1: Role Specification & 5D Criteria Gateway
        print("Capturing Step 1: Criteria Gateway...")
        page.goto("http://localhost:5173/#dashboard", wait_until="networkidle")
        time.sleep(2)
        page.locator("nav button:has-text('Job Setup & Criteria')").click()
        time.sleep(1.5)
        page.screenshot(path=os.path.join(DOCS_DIR, "screenshot_criteria_gateway.png"), full_page=False)

        # 4. Dashboard - Step 2: Resume Ingestion Gateway
        print("Capturing Step 2: Upload Resumes...")
        page.locator("nav button:has-text('Upload Resumes')").click()
        time.sleep(1.5)
        page.screenshot(path=os.path.join(DOCS_DIR, "screenshot_bulk_dropzone.png"), full_page=False)

        # 5. Dashboard - Step 3: Candidate Rankings Matrix
        print("Capturing Step 3: Candidate Rankings Matrix...")
        page.locator("nav button:has-text('Candidate Rankings')").click()
        time.sleep(1.5)
        # If no candidates yet, click 'Load 100 Benchmark Resumes' button if visible
        try:
            # Handle alert dialog automatically
            page.on("dialog", lambda dialog: dialog.accept())
            load_btn = page.locator("button:has-text('Load 100 Benchmark Resumes')")
            if load_btn.is_visible():
                print("Clicking 'Load 100 Benchmark Resumes'...")
                load_btn.click()
                time.sleep(6)
        except Exception as e:
            print("Benchmark loading notice:", e)

        page.screenshot(path=os.path.join(DOCS_DIR, "screenshot_ranking_matrix.png"), full_page=False)

        # 6. Dashboard - Step 4: Candidate Details & XAI Insights Dossier
        print("Capturing Step 4: Explainable AI Dossier...")
        page.locator("nav button:has-text('Candidate Details & Insights')").click()
        time.sleep(2)
        page.screenshot(path=os.path.join(DOCS_DIR, "screenshot_xai_dossier.png"), full_page=False)

        print("All screenshots successfully captured!")
        browser.close()

if __name__ == "__main__":
    capture_all()
