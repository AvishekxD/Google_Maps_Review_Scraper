## GoogleMaps review scraper
 
<p align="center"> 
  <img
    src="/step0.png"
    alt="Steps to get reviews"
    width="800" height="482"
  />
  <img
    src="/step1.png"
    alt="Steps to get reviews"
    width="800" height="482"
  />
</p>

---

>_steps -_ 
>
>_Search for the business on Google._ 
>_Open it in Google Maps._ 
>_Select the business → Go to Reviews._
>Copy the URL and paste it into Scrape.py on Line 89: | target_url = "Your_url"s
>_Run the scraper, then click Go back to webpage and scroll through the reviews section._
>_It’s set to 40 seconds on Line 21. Increase this value if you want to collect more reviews 😄_

---

**Review structure/Output Format -** 

{
    "name": "",
    "profile_pic": "",
    "time": "",
    "content": "",
    "stars": 5
}
