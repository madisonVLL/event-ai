from urllib.request import urlopen
import requests
from bs4 import BeautifulSoup

eventTypes = {"weddings": ["https://www.brides.com/story/brides-wedding-checklist-custom-wedding-to-do-list", 
                           "https://www.theknot.com/content/12-month-wedding-planning-countdown",
                           "https://www.herecomestheguide.com/wedding-ideas/the-guide-brides-wedding-checklist",
                           "https://www.minted.com/gifts/wedding-planning-checklist",
                           "https://assets.minted.com/image/upload/Minted_Onsite_Assets/2022/LP/Wedding/1831_ChecklistMasterClassMindyWeiss.pdf",
                           "https://www.zola.com/expert-advice/checklist/your-ultimate-wedding-planning-checklist",
                           "https://touchstay.com/blog/wedding-planning-checklist-and-guide",
                           "https://www.vaughnbarry.com/blog/wedding-planning-checklist",
                           "https://www.vogue.com/article/the-ultimate-month-by-month-wedding-planning-checklist",
                           "https://www.hitched.co.uk/wedding-planning/organising-and-planning/wedding-checklist/",
                           "https://www.trulyengaging.com/wedding-planning-checklist",
                           "https://www.weddingswithverve.com/blog/wedding-planning-checklist",
                           "https://onefabday.com/wedding-checklist/"], 
              "birthdays": ["https://www.socialtables.com/blog/event-planning/party-planning-checklist/",
                            "https://www.tagvenue.com/blog/party-planning-checklist/",
                            "https://www.thebash.com/articles/party-planning-checklist-stay-organized",
                            "https://www.greenvelope.com/blog/birthday-party-checklist",
                            "https://checklist.com/birthday-party-checklist",
                            "https://www.thebash.com/articles/grown-up-birthday-party-planning-checklist",
                            "https://starsandstrikes.com/how-to-prepare-a-timeline-for-planning-a-birthday-party-2/"], 
              "childrens": ["https://www.hgtv.com/lifestyle/entertaining/planning-a-birthday-party",
                            "https://www.realsimple.com/holidays-entertaining/birthdays/childs-home-birthday-party-checklist",
                            "https://www.pbs.org/parents/thrive/your-birthday-party-timeline", 
                            "https://www.microsoft.com/en-us/microsoft-365-life-hacks/organization/kids-birthday-party-planning-checklist",
                            "https://parentguidenews.com/articles/birthdays/party-planning-timeline/"],
              "baby shower": ["https://www.babylist.com/hello-baby/baby-shower-checklist?g_acctid=878-527-6823&g_adgroupid=139460489440&g_adid=599148935921&g_adtype=search&g_campaign=Content-MidPerformance&g_campaignid=12573456625&g_keyword=baby%20shower%20checklist&g_keywordid=kwd-328150832385&g_network=g&utm_campaign=Content-MidPerformance&utm_content=599148935921&utm_medium=paid-search&utm_source=g&utm_term=139460489440&gad_source=1&gclid=Cj0KCQjwo8S3BhDeARIsAFRmkOPUDulUgmuUBQCzS825f4_r3adpdlv8joNXiqKaAUE-LB30uHkWa4oaAtR6EALw_wcB",
                              "https://www.pampers.com/en-us/pregnancy/baby-shower/article/baby-shower-checklist",
                              "https://www.thebump.com/a/baby-shower-checklist",
                              "https://www.babylist.com/hello-baby/baby-shower-checklist",
                              "https://www.marthastewart.com/8214994/baby-shower-planning-timeline",
                              "https://www.minted.com/lp/baby-shower-planning-checklist", 
                              "https://www.baby-chick.com/baby-shower-checklist/",
                              "https://www.foryourparty.com/blog/precious-arrival-perfect-baby-shower-timeline?srsltid=AfmBOorAwnhv4G7h0SsbOfr9dYSNuuGDrVDLmajEY4u3WmzoHT5nj-lN",
                              "https://www.greenvelope.com/blog/baby-shower-checklist",
                              "https://bunniesbythebay.com/blogs/how-to-delight/checklist-how-to-host-the-perfect-baby-shower?srsltid=AfmBOopWEx18w7LTeRLOaemu_uc-yMXFjEazsIjG2IMj7ZJRbb28XQPa"],
              "general": ["https://www.thebash.com/articles/party-planning-checklist-stay-organized",
                          "https://www.signupgenius.com/home/party-planning-checklist.cfm",
                          "https://www.greenvelope.com/blog/birthday-party-checklist",
                          "https://www.realsimple.com/holidays-entertaining/entertaining/party-planning-checklist",
                          "https://www.lovetoknow.com/celebrations/parties/party-planning-checklist"
                          ],
                "dinner": ["https://www.theinletnww.com/post/how-to-plan-the-perfect-dinner-event-a-timeline-based-guide/",
                           "https://www.lacrema.com/planning-a-dinner-party/",
                           "https://www.partyswizzle.com/dinnerpartychecklist.html?srsltid=AfmBOoo2IdrrixKKgKCzvQbhglv0PoUbRT4N7T4O-ZS7wfJKrUldl8cv",
                           "https://yearandday.com/blogs/ourhours/your-dinner-party-checklist?srsltid=AfmBOooCAFzaWx75eRmpK5zFz5hLfY_gEMgok3VsjhHMPYiDwUY2K8J7",
]}

date_triggers = [
    "Day", "Days", "Month", "Months", "Week", "Weeks", "Year", "Years", 
    "Hour", "Hours", "Minute", "Minutes", "Second", "Seconds", 
    "Morning", "Afternoon", "Evening", "Night", "Sunrise", "Sunset", 
    "Noon", "Midnight", "Decade", "Century", "Millennium", "Quarter", 
    "Fortnight", "Epoch", "Era", "Moment", "Instant", "Phase", 
    "Period", "Season", "Time", "Timeline", "Chronology", 
    "Interval", "Duration", "Span", "day", "days", "month", "months", "week",
    "weeks", "year", "years",  "hour", "hours", "minute", "minutes", "second",
    "morning", "afternoon", "evening", "night", "sunrise", "sunset", 
    "noon", "midnight", "decade", "century", "millennium", "quarter", 
    "fortnight", "epoch", "era", "moment", "instant", "phase", 
    "period", "season", "time", "timeline", "chronology", 
    "interval", "duration", "span", "seconds"
]

statements = {}

for key, value in eventTypes.items():
    #goes through individual websites within each category and checks to see
    #if they paragraph mentions the time interval
    for website in value:
        visted_page = requests.get(website)
        page_soup = BeautifulSoup(visted_page.text, "html.parser")
        body_soup = page_soup.body
        for info in body_soup.strings:
            if key not in statements.keys():
                statements[key] = [info]
            else:
                statements[key].append(info)

print(statements["dinner"])


        

