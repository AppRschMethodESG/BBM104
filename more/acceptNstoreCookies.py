import subprocess
import pyppeteer
from pyppeteer import launch
import asyncio
import re
import csv
import json
import time   


# Run the playwright install-deps command
#subprocess.run(["/opt/venv/bin/playwright", "install"], check=True)

# Run the playwright install-deps command
#subprocess.run(["/opt/venv/bin/playwright", "install-deps"], check=True)


ExpandHidden = False
#topLevelURL = 'https://www.siemens.com'
topLevelURL = 'https://group.mercedes-benz.com'
yearStart = 2023
yearEnd = 2014
years = [yearStart - i for i in range(yearStart - yearEnd + 1)]


# Define the script to check if the cookie banner exists
script_check_banner = """
() => {
    const shadowRoot = document.querySelector('#usercentrics-root')?.shadowRoot;
    if (shadowRoot) {
        const shadowButtons = Array.from(shadowRoot.querySelectorAll('button'));
        const shadowAcceptButton = shadowButtons.find(button => 
            button.textContent.includes('Accept All') || 
            button.textContent.includes('Accept all') ||
            button.innerText.includes('Accept All') ||
            button.innerText.includes('Accept all')
        );
        return shadowAcceptButton ? true : false;
    }
    return false;
}
"""

async def click_accept_cookies(page):
    try:
        # First take note if cookie banner exists
        initial_banner_present = await page.evaluate(script_check_banner)
        print(f"Cookie banner present: {initial_banner_present}")
        
        # Try to click the accept button
        script_click = """
        () => {
            let result = '';
            // Try to find button by text content
            const buttons = Array.from(document.querySelectorAll('button'));
            const acceptButton = buttons.find(button => 
                button.textContent.includes('Accept All') || 
                button.textContent.includes('Accept all') ||
                button.innerText.includes('Accept All') ||
                button.innerText.includes('Accept all')
            );
            
            if (acceptButton) {
                acceptButton.click();
                result += '  acceptButton clicked ';
            }
            
            // Try to access shadow DOM
            const shadowRoot = document.querySelector('#usercentrics-root')?.shadowRoot;
            if (shadowRoot) {
                const shadowButtons = Array.from(shadowRoot.querySelectorAll('button'));
                const shadowAcceptButton = shadowButtons.find(button => 
                    button.textContent.includes('Accept All') || 
                    button.textContent.includes('Accept all') ||
                    button.innerText.includes('Accept All') ||
                    button.innerText.includes('Accept all')
                );
                
                if (shadowAcceptButton) {
                    shadowAcceptButton.click();
                    result += '  shadowAcceptButton clicked ';
                }
            }

            return result || 'no button clicked';
        }
        """
        
        # Execute the click script
        click_result = await page.evaluate(script_click)
        print(f"Click result: {click_result}")
        
        if 'clicked' not in click_result:
            print("Could not find cookie accept button")
            return False

        # Must wait for at least 0.1 seconds; o/w, can cause false alarm
        await asyncio.sleep(1)
        # Wait for page to stabilize
        await page.waitForFunction('document.body.scrollHeight > 0', {'timeout': 5000})

        # Verify cookie banner is gone
        banner_still_present = await page.evaluate(script_check_banner)
        if not banner_still_present:
            print("Verified: Cookie banner is gone")
            # Wait for page to stabilize
            #await page.waitForFunction('document.body.scrollHeight > 0', {'timeout': 5000})
            return True
        else:
            print(f"Click result printed again: {click_result}")
            print("Warning: Cookie banner still present after click")
            return False

    except Exception as e:
        print(f"Error in click_accept_cookies: {str(e)}")
        return False




async def fully_loaded(browser, url):
    page = await browser.newPage()
    
    # Set user agent
    # !!!Note: This is critical to prevent the page from detecting the headless browser
    await page.setUserAgent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.53 Safari/537.36')
    # Modify the navigator.webdriver property
    await page.evaluateOnNewDocument('''() => {
        Object.defineProperty(navigator, 'webdriver', {
            get: () => undefined,
        });
    }''')
    
    # Navigate to the website and Measure time for networkidle2
    start_time = time.time()
    await page.goto(url, {'waitUntil': 'networkidle2'})
    networkidle2_time = time.time() - start_time
    print(f"Time taken to fully load page: {networkidle2_time:.2f} seconds")

    return page


async def acceptNstoreCookies():
    browser = await launch({
        'headless': True,
        'args': [
            '--disable-blink-features=AutomationControlled',
            '--no-sandbox',
            '--disable-setuid-sandbox',
            '--disable-dev-shm-usage',
            '--disable-accelerated-2d-canvas',
            '--no-first-run',
            '--no-zygote',
            '--single-process',
            '--disable-gpu',
            '--disable-web-security',
            '--disable-webrtc',
            '--disable-features=WebRTC',
            '--disable-webrtc-hw-decoding',
            '--disable-webrtc-hw-encoding',
            '--webrtc-ip-handling-policy=disable_non_proxied_udp',
            '--force-webrtc-ip-handling-policy',
            '--REDACTED'
        ]
    })

    try:

        #========================================
        print("Getting screenshot of the blocked page when bot is detected...")
        page = await browser.newPage()
        await page.goto(topLevelURL, {'waitUntil': 'networkidle2'})
        # Get and print the height of the page  
        pageHeight = await page.evaluate('document.body.scrollHeight')
        print('Page Height:', pageHeight)
        #await page.setViewport({'width': 1024, 'height': pageHeight * 1})
        await page.screenshot({'path': 'screenshot_BotDetected.png', 'fullPage': True})
        #========================================


        # Get the fully loaded page
        # !!!Note: The setUserAgent inside this is critical to prevent the page from detecting the headless browser
        page = await fully_loaded(browser, topLevelURL)
        print("Page fully loaded, moving on to the next line of code.")
        

        # Get and print the height of the page (before accepting cookies)
        await page.waitForFunction('document.body.scrollHeight > 0', {'timeout': 5000})
        pageHeight = await page.evaluate('document.body.scrollHeight')
        print('Page Height:', pageHeight)
        #await page.setViewport({'width': 1024, 'height': pageHeight * 1})
        await page.screenshot({'path': 'screenshot_CookiesPopup.png', 'fullPage': True})

        # Accept cookies
        await click_accept_cookies(page)
        # Wait for page to be fully loaded
        await asyncio.sleep(1)

        # Verify page height is valid before measuring
        await page.waitForFunction('document.body.scrollHeight > 0', {'timeout': 5000})
        pageHeight = await page.evaluate('document.body.scrollHeight')
        print('Page Height:', pageHeight)
        #await page.setViewport({'width': 1024, 'height': pageHeight * 1})
        await page.screenshot({'path': 'screenshot_CookiesAccepted.png', 'fullPage': True})
        #========================================
        banner_present = await page.evaluate(script_check_banner)
        print(f"Cookie banner present: {banner_present}")
        #========================================
        

        # Extract all URLs from the page
        urls = await page.evaluate('''() => Array.from(document.querySelectorAll('a')).map(a => a.href)''')
        # Save the URLs to urls0.csv
        with open('urls0.csv', 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['URL'])
            writer.writerows([[url] for url in urls])

        # Filter URLs based on the specified keywords
        keywords = [#'Investor', 
            'ESG', 'Sustainability', 'Environment', 'Corporate_Responsibility', 'Transparency']
        filteredUrls = [url for url in urls if any(re.search(keyword.replace('_', '[_-]'), url, re.IGNORECASE) for keyword in keywords)]
        # Save the filtered URLs to urls1.csv
        with open('urls1.csv', 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['URL'])
            writer.writerows([[url] for url in filteredUrls])

        await asyncio.sleep(1)

        # Save the webpage source to an .html file
        #pageContent = await page.content()
        #with open('page.html', 'w', encoding='utf-8') as f:
        #    f.write(pageContent)

    except Exception as error:
        print('Error:', error)
    finally:
        # Save the cookies and local storage
        cookies = await page.cookies()
        localStorage = await page.evaluate('''() => JSON.stringify(localStorage)''')
        with open('cookies.json', 'w', encoding='utf-8') as f:
            json.dump(cookies, f, indent=2)
        with open('localStorage.json', 'w', encoding='utf-8') as f:
            f.write(localStorage)

    # Close the browser
    await browser.close()


# Run the acceptNstoreCookies() function
asyncio.run(acceptNstoreCookies())
#asyncio.get_event_loop().run_until_complete(acceptNstoreCookies())