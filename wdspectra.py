#%%
import matplotlib.pyplot as plt
import numpy as np
from astropy import units as u
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import time

def get_dynamic_div_link(url):
    """
    Launches a Selenium-controlled Chrome browser to fetch the page.
    Waits for the <div id="spect_0"> to appear, and returns the link within it.
    """

    # Configure Chrome to run headless (no UI).
    chrome_options = Options()
    chrome_options.add_argument("--headless")  
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=chrome_options
    )

    try:
        driver.get(url)
        time.sleep(5)
        spect_div = driver.find_element(By.ID, "spect_0")
        link_tag = spect_div.find_element(By.TAG_NAME, "a")
        href = link_tag.get_attribute("href")

        return href

    except Exception as e:
        print(f"Error occurred: {e}")
        return None

    finally:
        driver.quit()


def fetch_star_spectrum(txt_url) -> str:
    """
    Given a wdid 
    constructs the MWDD URL for the corresponding text file
    and returns the text content if available.
    """
    response = requests.get(txt_url)

   
    if response.status_code == 200:
        print(f"Successfully retrieved data for {star_name}")
        return response.text  
    else:
        print(f"Failed to retrieve data. HTTP Status Code: {response.status_code}")
        return ""
    
def convert_spectrum():
    encoded_name = star_name.replace(" ", "%20")
    page_url = (
        "https://www.montrealwhitedwarfdatabase.org/WDs/"
        f"{encoded_name}/{encoded_name}.html"
    )
    spectrum_data = fetch_star_spectrum(get_dynamic_div_link(page_url))

    wavelength, flux = zip(*[tuple(map(float, item.split(','))) for item in spectrum_data.splitlines()[2:]])
    return spectrum_data.splitlines()[0],np.array(wavelength), np.array(flux)
#%%
global star_name

star_name = "Gaia DR3 4597049319640506624"
specdata, wave, flux = convert_spectrum()


# %%
fig, ax = plt.subplots()
ax.plot(wave,flux,label=specdata.split(',')[2])
ax.legend()
ax.set_ylim(0)
# %%