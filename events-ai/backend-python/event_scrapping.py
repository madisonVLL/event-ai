from urllib.request import urlopen
import requests
import typing
from bs4 import BeautifulSoup
import html2text


eventTypes: dict[str, list[str]] = {"weddings": ["https://www.brides.com/story/brides-wedding-checklist-custom-wedding-to-do-list", 
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


def upperFirstCase(triggers: list[str]) -> list[str]:
    '''
    This function makes a list in which the first letter of a word is 
    upper case, the whole word uppercase, and the original word

    inputs:
    triggers - list of strings

    returns
    list of strings
    '''
    triggers_upper = [each[0].upper() + each[1:] for each in triggers.copy()]
    triggers_caps = [each.upper() for each in triggers.copy()]
    return triggers + triggers_upper + triggers_caps

NUMBER_TRIGGERS = upperFirstCase([str(i) for i in range(0, 10)] + ["one", "two", "three", "four",
    "five", "six", "seven", "eight", "nine", "ten","eleven", "twelve", "thirteen",
    "fourteen", "fifteen", "sixteen", "seventeen", "eighteen", "nineteen", "twenty",
    "twenty-one", "twenty-two", "twenty-three", "twenty-four", "of"])

DATE_TRIGGERS = upperFirstCase([
    "day", "days", "month", "months", "week",
    "weeks", "year", "years",  "hour", "hours", "minute", "minutes", "second",
    "morning", "afternoon", "evening", "night", "sunrise", "sunset", 
    "noon", "midnight", "decade", "century", "millennium", "quarter", 
    "fortnight", "epoch", "era", "moment", "instant", "phase", 
    "period", "season",   "chronology", 
    "interval", "duration", "span", "seconds"
])

PREP_TIME_TRIGGERS = upperFirstCase(["before", "after", "during", "for", 
    "at", "on", "in", "throughout", "past", "out", "of"])

PUNCTUATION = [
    ".", "?", "!", "'", "\"", 
    "{", "}", "/", "\\", "|", "@", "#", "$", "%", "^", "&", "*", "_", "~", "`",
    ">", "<"
]

def isFullSentence(sentence: list[str]) -> bool:
    """
    defining a complete sentence by if a word ends with any of the puntioan above

    also checks to see if there is some non sensical punctuation
    """
    endingPunctuation: list[str] = [".", "?", "!"]
    for each in sentence:
        if each[-1] in endingPunctuation:
            return True
        for letter in each:
            if letter in PUNCTUATION:
                return True
    return False

def checkTigger(sentence: list[str], trigger: list[str]) -> bool:
    '''
    checks to see if the sentence contains one of the date triggers defined above

    inputs:
    sentence - list of strings

    trigger - list of strings to determine if a string in sentence matches

    returns True if there is a word in triggers, false otherwise
    '''
    for word in sentence:
        if word in trigger:
            return True
    return False


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

eventTimelineEvents: dict[str, list[dict[str, str]]] = {}
for key in statements.keys():
    eventTimelineEvents[key] = []

#structure key = string, value = list of dictionaries

for event, web_content in statements.items():
    current_key = None
    current_timeline = []
    for web_section in web_content:
        for sentence in web_section:
            words = list(str(sentence).split(" "))
            if checkTigger(words, DATE_TRIGGERS) and checkTigger(words, NUMBER_TRIGGERS) \
            and not isFullSentence(words) and checkTigger(words, PREP_TIME_TRIGGERS):
                eventTimelineEvents[event].append({current_key: current_timeline})
                current_key = sentence
                current_timeline = []
            if current_key is not None and sentence != current_key:
                current_timeline.append(sentence)

print(eventTimelineEvents["weddings"])
   





'''
Things to check before creating a new key

has some sort of number or of
has a date trigger

Optional
- prepositions
'''






