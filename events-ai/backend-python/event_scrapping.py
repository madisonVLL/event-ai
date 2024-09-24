from urllib.request import urlopen
import requests
from bs4 import BeautifulSoup
import html2text

eventTypes = {"weddings": ["https://www.brides.com/story/brides-wedding-checklist-custom-wedding-to-do-list", 
                           "https://www.theknot.com/content/12-month-wedding-planning-countdown",
                           "https://www.minted.com/gifts/wedding-planning-checklist",
                           "https://assets.minted.com/image/upload/Minted_Onsite_Assets/2022/LP/Wedding/1831_ChecklistMasterClassMindyWeiss.pdf",
                           "https://www.zola.com/expert-advice/checklist/your-ultimate-wedding-planning-checklist",
                           "https://touchstay.com/blog/wedding-planning-checklist-and-guide",
                           "https://www.vaughnbarry.com/blog/wedding-planning-checklist",
                           "https://www.vogue.com/article/the-ultimate-month-by-month-wedding-planning-checklist",
                           "https://www.weddingswithverve.com/blog/wedding-planning-checklist",
                           "https://onefabday.com/wedding-checklist/"], 
              "birthdays": ["https://www.tagvenue.com/blog/party-planning-checklist/",
                            "https://www.thebash.com/articles/party-planning-checklist-stay-organized",
                            "https://checklist.com/birthday-party-checklist",
                            "https://www.thebash.com/articles/grown-up-birthday-party-planning-checklist",
                            "https://starsandstrikes.com/how-to-prepare-a-timeline-for-planning-a-birthday-party-2/"], 
              "childrens": ["https://www.hgtv.com/lifestyle/entertaining/planning-a-birthday-party",
                            "https://www.realsimple.com/holidays-entertaining/birthdays/childs-home-birthday-party-checklist",
                            "https://www.pbs.org/parents/thrive/your-birthday-party-timeline"],
              "baby shower": ["https://www.babylist.com/hello-baby/baby-shower-checklist?g_acctid=878-527-6823&g_adgroupid=139460489440&g_adid=599148935921&g_adtype=search&g_campaign=Content-MidPerformance&g_campaignid=12573456625&g_keyword=baby%20shower%20checklist&g_keywordid=kwd-328150832385&g_network=g&utm_campaign=Content-MidPerformance&utm_content=599148935921&utm_medium=paid-search&utm_source=g&utm_term=139460489440&gad_source=1&gclid=Cj0KCQjwo8S3BhDeARIsAFRmkOPUDulUgmuUBQCzS825f4_r3adpdlv8joNXiqKaAUE-LB30uHkWa4oaAtR6EALw_wcB",
                              "https://www.babylist.com/hello-baby/baby-shower-checklist",
                              "https://www.marthastewart.com/8214994/baby-shower-planning-timeline",
                              "https://www.minted.com/lp/baby-shower-planning-checklist", 
                              "https://www.foryourparty.com/blog/precious-arrival-perfect-baby-shower-timeline?srsltid=AfmBOorAwnhv4G7h0SsbOfr9dYSNuuGDrVDLmajEY4u3WmzoHT5nj-lN",
                              "https://bunniesbythebay.com/blogs/how-to-delight/checklist-how-to-host-the-perfect-baby-shower?srsltid=AfmBOopWEx18w7LTeRLOaemu_uc-yMXFjEazsIjG2IMj7ZJRbb28XQPa"],
              "general": ["https://www.thebash.com/articles/party-planning-checklist-stay-organized",
                          "https://www.realsimple.com/holidays-entertaining/entertaining/party-planning-checklist",
                          "https://www.lovetoknow.com/celebrations/parties/party-planning-checklist",
                          "https://whova.com/blog/event-planning-timeline/",
                          "https://www.dartmouth.edu/cse/docs/sampletimeline.pdf"],
                "dinner": [
                           "https://www.lacrema.com/planning-a-dinner-party/",
                           "https://yearandday.com/blogs/ourhours/your-dinner-party-checklist?srsltid=AfmBOooCAFzaWx75eRmpK5zFz5hLfY_gEMgok3VsjhHMPYiDwUY2K8J7",
]}

date_triggers = [
    "Day", "Days", "Month", "Months", "Week", "Weeks", "Year", "Years", 
    "Hour", "Hours", "Minute", "Minutes", "Second", "Seconds", 
    "Morning", "Afternoon", "Evening", "Night", "Sunrise", "Sunset", 
    "Noon", "Midnight", "Decade", "Century", "Millennium", "Quarter", 
    "Fortnight", "Epoch", "Era", "Moment", "Instant", "Phase", 
    "Period", "Season",   "Chronology", 
    "Interval", "Duration", "Span", "day", "days", "month", "months", "week",
    "weeks", "year", "years",  "hour", "hours", "minute", "minutes", "second",
    "morning", "afternoon", "evening", "night", "sunrise", "sunset", 
    "noon", "midnight", "decade", "century", "millennium", "quarter", 
    "fortnight", "epoch", "era", "moment", "instant", "phase", 
    "period", "season",   "chronology", 
    "interval", "duration", "span", "seconds", "DAY", "DAYS", "MONTH",
    "MONTHS", "WEEK", "WEEKS", "YEAR", "YEARS", 
    "HOUR", "HOURS", "MINUTE", "MINUTES", "SECOND", "MORNING", 
    "AFTERNOON", "EVENING", "NIGHT", "SUNRISE", "SUNSET", "NOON", 
    "MIDNIGHT", "DECADE", "CENTURY", "MILLENNIUM", "QUARTER", 
    "FORTNIGHT", "EPOCH", "ERA", "MOMENT", "INSTANT", "PHASE", 
    "PERIOD", "SEASON",   "CHRONOLOGY", 
    "INTERVAL", "DURATION", "SPAN", "SECONDS"
]

statements = {}


for key, value in eventTypes.items():
    #goes through individual websites within each category and checks to see
    #if they paragraph mentions the time interval
    for website in value:
        html = urlopen(website).read()
        soup = BeautifulSoup(html, features="html.parser")

        # kill all script and style elements
        for script in soup(["script", "style"]):
            script.extract()    # rip it out

        # get text
        text = soup.get_text()

        # break into lines and remove leading and trailing space on each
        lines = (line.strip() for line in text.splitlines())
        # break multi-headlines into a line each
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        # drop blank lines
        text = '\n'.join(chunk for chunk in chunks if chunk).splitlines()
        if key not in statements.keys():
            statements[key] = [text]
        else:
            statements[key].append(text)


'''
This section of code determines if there are any time triggers within any of the 
statements, in then spits the list by time tigger

this information is stored as a dictionary
'''

eventTimelineEvents = {}
for key in statements.keys():
    eventTimelineEvents[key] = []

#structure key = string, value = list of dictionaries

for event, web_content in statements.items():
    current_key = None
    current_timeline = []
    for web_section in web_content:
        for sentence in web_section:
            words = list(str(sentence).split(" "))
            for word in words:
                if word in date_triggers:
                    eventTimelineEvents[event].append({current_key: current_timeline})
                    current_key = sentence
                    current_timeline = []
            if current_key is not None and sentence != current_key:
                current_timeline.append(sentence)

                

