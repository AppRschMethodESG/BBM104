// This flag determines whether there are hidden elements that need to be expanded
const ExpandHidden = false; // true; // 

//const topLevelURL = 'https://group.mercedes-benz.com/investors/';
const topLevelURL = 'https://group.mercedes-benz.com';
//const topLevelURL = 'https://www.google.com/search?q=Mercedes-Benz+Sustainability&rlz=1C1GCEB_enGB884GB884&oq=Mercedes-Benz+Sustainability&gs_lcrp=EgZjaHJvbWUyBggAEEUYOTIMCAEQABgUGIcCGIAEMgwIAhAAGBQYhwIYgAQyBwgDEAAYgAQyBwgEEAAYgAQyBwgFEAAYgAQyCAgGEAAYBxgeMgYIBxBFGDzSAQgzMDU0ajBqOagCALACAQ&sourceid=chrome&ie=UTF-8';
//const topLevelURL = 'https://www.siemens.com/global/en/company/investor-relations.html';

const yearStart = 2023;
const yearEnd = 2014;
const years = Array.from({ length: yearStart - yearEnd + 1 }, (_, i) => yearStart - i);

const puppeteer = require('puppeteer-extra');
const StealthPlugin = require('puppeteer-extra-plugin-stealth');
const fs = require('fs');
const UserAgent = require('user-agents');

puppeteer.use(StealthPlugin());
//console.log(StealthPlugin.availableEvasions);   // This reported undefined !?

async function run() {
  const browser = await puppeteer.launch({
    headless: true,
    args: [
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
      // Disable WebRTC
      '--disable-webrtc',
      '--disable-features=WebRTC',
      '--disable-webrtc-hw-decoding',
      '--disable-webrtc-hw-encoding',
      '--webrtc-ip-handling-policy=disable_non_proxied_udp',
      '--force-webrtc-ip-handling-policy',

      // Proxy settings
      '--REDACTED',

    ]
  });


  const page = await browser.newPage();

  // Generate and set random user agent
  //const userAgent = new UserAgent();
  //await page.setUserAgent(userAgent.random().toString());

  // Set user agent
  await page.setUserAgent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.53 Safari/537.36');

  // Modify the navigator.webdriver property
  await page.evaluateOnNewDocument(() => {
    Object.defineProperty(navigator, 'webdriver', {
      get: () => undefined,
    });
  });

  // Set the viewport size to twice the height of the page
//  await page.setViewport({ width: 1280, height: 720}); //1080  1920  1280 720


//======================================  
{

    // Navigate to the website
    await page.goto(topLevelURL, { waitUntil: 'networkidle2', timeout: 10000 });

    // Get the height of the page
    const pageHeight = await page.evaluate(() => document.body.scrollHeight);

    // Print out pageHeight
    console.log('Page Height:', pageHeight);

    // Set the viewport size to twice the height of the page
    await page.setViewport({ width: 1024, height: pageHeight * 1 }); //1280  1920

    // Take a screenshot of the full page
    await page.screenshot({ path: 'screenshotG.png', fullPage: true }); 

}
//======================================  



  try {
    // Navigate to the website
    await page.goto(topLevelURL, { waitUntil: 'networkidle2', timeout: 10000 });

    // Click 'Accept All'
    const timeout = 5000;
    const targetPage = page;
    await Promise.race([
      page.waitForSelector('::-p-aria(Accept All)', { timeout }),
      page.waitForSelector("#usercentrics-root >>>> [data-testid='uc-accept-all-button']", { timeout }),
      page.waitForSelector(":scope >>> [data-testid='uc-accept-all-button']", { timeout }),
      page.waitForSelector('::-p-text(Accept All)', { timeout })
    ])  
      .then(element => element.click({
//        button: 'left',
        offset: {
          x: 99.125,
          y: 40.375,
        },
      }));      



    // Wait for a specific element to ensure the page is fully loaded
//    await page.waitForSelector('body');

    // Optionally, wait for a fixed amount of time to ensure stability
    await new Promise(resolve => setTimeout(resolve, 1000)); // Wait for 1 second

    // Get the height of the page
    const pageHeight = await page.evaluate(() => document.body.scrollHeight);

    // Print out pageHeight
    console.log('Page Height:', pageHeight);

    // Set the viewport size to twice the height of the page
    await page.setViewport({ width: 1024, height: pageHeight * 1 }); //1280  1920

    // Take a screenshot of the full page
    await page.screenshot({ path: 'screenshotZ.png', fullPage: true });  



    // Wrap the code in a block to avoid the error of redeclaring block-scoped variable"      
    {
    // Extract all URLs from the page
    const urls = await page.evaluate(() => Array.from(document.querySelectorAll('a')).map(a => a.href));
    // Save the URLs to urls.csv
    const csvContent = 'URL\n' + urls.join('\n');
    fs.writeFileSync('urls0.csv', csvContent, 'utf-8');

    // Filter URLs based on the specified keywords
    const keywords = [ //'Investor', 
                      'ESG', 'Sustainability', 'Environment', 'Corporate_Responsibility', 'Transparency'];
    const filteredUrls = urls.filter(url => 
        keywords.some(keyword => new RegExp(keyword.replace('_', '[_-]'), 'i').test(url))
    );

    // Save the filtered URLs to urls1.csv
    const filteredCsvContent = 'URL\n' + filteredUrls.join('\n');
    fs.writeFileSync('urls1.csv', filteredCsvContent, 'utf-8');
    
    }


    // Optionally, wait for a fixed amount of time to ensure stability
    await new Promise(resolve => setTimeout(resolve, 1000)); // Wait for 1 second


    // Save the webpage source to an .html file
    const pageContent = await page.content();
    fs.writeFileSync('page.html', pageContent, 'utf-8');

  } catch (error) {
    console.error('Error:', error);
  } finally {

    // Save cookies and local storage
    const cookies = await page.cookies();
    const localStorage = await page.evaluate(() => JSON.stringify(localStorage));
    fs.writeFileSync('cookies.json', JSON.stringify(cookies, null, 2));
    fs.writeFileSync('localStorage.json', localStorage);

    // Close the browser
    await browser.close();
    console.log('Done! You can check the screenshot, URLs, and page source...');
  }
}

run();