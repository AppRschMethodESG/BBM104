//==============================================================================
// Parameters adjustable by the user
//==============================================================================

const topLevelURL = 'https://www.siemens.com/global/en/company/investor-relations.html';
// const topLevelURL = 'https://group.mercedes-benz.com/investors/';

//==============================================================================
// This flag determines whether there are hidden elements that need to be expanded
const ExpandHiddenParts = true; // false; // 
const yearStart = 2023;
const yearEnd = 2014;
const years = Array.from({ length: yearStart - yearEnd + 1 }, (_, i) => yearStart - i);
//==============================================================================


const puppeteer = require('puppeteer-extra');
const StealthPlugin = require('puppeteer-extra-plugin-stealth');
const fs = require('fs');

puppeteer.use(StealthPlugin());

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
      '--disable-gpu'
    ]
  });

  const page = await browser.newPage();

  // Set user agent
  await page.setUserAgent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.53 Safari/537.36');

  // Modify the navigator.webdriver property
  await page.evaluateOnNewDocument(() => {
    Object.defineProperty(navigator, 'webdriver', {
      get: () => undefined,
    });
  });

  try {
    // Navigate to the website
    await page.goto(topLevelURL, { waitUntil: 'networkidle2', timeout: 10000 });

    // Click 'Accept All Cookies'
    const timeout = 5000;
    await Promise.race([
      page.waitForSelector('::-p-aria(Accept All Cookies)', { timeout }),
      page.waitForSelector("#usercentrics-root >>> [data-testid='uc-accept-all-button']", { timeout }),
      page.waitForSelector(":scope >>> [data-testid='uc-accept-all-button']", { timeout })
    ])
      .then(element => element.click({
        button: 'left',
        offset: {
          x: 208,
          y: 10,
        },
      }));

    // Optionally, wait for a specific element to be visible
    await page.waitForSelector('text=Investor Relations', { timeout: 10000 });

    const targetPage = page;
    await Promise.race([
      targetPage.waitForSelector('::-p-aria(Financial Results, Publications, Events, Ad hoc, Related Party Transactions) >>> [role="generic"]'),
      targetPage.waitForSelector('div.cardNumber1 div.teaserCard__content span'),
      targetPage.waitForSelector('::-p-xpath(//*[@data-testid="teaser-card-container-flyout"]/div[2]/div/div/h2/span)'),
      targetPage.waitForSelector(':scope >>> div.cardNumber1 div.teaserCard__content span')
    ])
      .then(element => element.click({
        offset: {
          x: 114.5,
          y: 71.59375,
        },
      }));

    const promises = [];
    const startWaitingForEvents = () => {
      promises.push(targetPage.waitForNavigation());
    };

    await Promise.race([
      targetPage.waitForSelector('::-p-aria(Annual Reports) >>> [role="generic"]'),
      targetPage.waitForSelector('li.cardNumber2 div.teaserCard__content span'),
      targetPage.waitForSelector('::-p-xpath(//*[@data-testid="teaser-card-container"]/div[2]/div/div/h2/span)'),
      targetPage.waitForSelector(':scope >>> li.cardNumber2 div.teaserCard__content span'),
      targetPage.waitForSelector('::-p-text(Annual Reports)')
    ])
      .then(element => {
        element.click({
          offset: {
            x: 61,
            y: 17.4375,
          },
        });
        startWaitingForEvents();
      });

    await Promise.all(promises);

    // Function to click through sections based on years
    const clickSection = async (year) => {
      await Promise.race([
        targetPage.waitForSelector(`button[data-ste-element="Annual Reports ${year}"] span.accordion__icon`),
        targetPage.waitForSelector(`::-p-xpath(//button[@data-ste-element="Annual Reports ${year}"]/span[2])`),
        targetPage.waitForSelector(`:scope >>> button[data-ste-element="Annual Reports ${year}"] span.accordion__icon`)
      ])
        .then(element => element.click({
          offset: {
            x: 10,
            y: 10,
          },
        }));

    // Optionally, you can add a small delay to ensure stability
    await new Promise(resolve => setTimeout(resolve, 1000)); // Wait for 1 second

    };


    // Conditionally run the code based on the value of ExpandHidden
    if (ExpandHiddenParts) {
      // Loop through years and expand sections
      for (const year of years) {
        await clickSection(year);
      }
    }

    // Loop through years and expand sections
//    for (const year of years) {
//      await clickSection(year);
//    }

    // Wait for a specific element to ensure the page is fully loaded
    await page.waitForSelector('body');

    // Optionally, wait for a fixed amount of time to ensure stability
    await new Promise(resolve => setTimeout(resolve, 1000)); // Wait for 1 second

    // Get the height of the page
    const pageHeight = await page.evaluate(() => document.body.scrollHeight);

    // Print out pageHeight
    console.log('Page Height:', pageHeight);

    // Set the viewport size to twice the height of the page
    await page.setViewport({ width: 1080, height: pageHeight * 1 }); //1080  1920

    // Take a screenshot of the full page
    await page.screenshot({ path: 'screenshot.png', fullPage: true });  

    // Extract all URLs from the page
    const urls = await page.evaluate(() => Array.from(document.querySelectorAll('a')).map(a => a.href));

    // Filter URLs to keep only those that end with .pdf
    const pdfUrls = urls.filter(url => url.endsWith('.pdf'));

    // Save the filtered URLs to report_urls.csv
    const csvContent = 'URL\n' + pdfUrls.join('\n');
    fs.writeFileSync('report_urls.csv', csvContent, 'utf-8');
    //fs.writeFileSync('urls.txt', pdfUrls.join('\n'), 'utf-8');

    // Save the webpage source to an .html file
    const pageContent = await page.content();
    fs.writeFileSync('page.html', pageContent, 'utf-8');

  } catch (error) {
    console.error('Error:', error);
  } finally {
    // Close the browser
    await browser.close();
    console.log('Done! You can check the screenshot, URLs, and page source...');
  }
}

run();