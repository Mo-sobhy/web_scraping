import csv
from itertools import zip_longest
from tkinter import *
import requests
from PIL import ImageTk
from PIL import Image
from bs4 import BeautifulSoup

root = Tk()
root.title("Wazzuf.com")
img=Image.open("photo1.jpg")
bck_end=ImageTk.PhotoImage(img)
root.geometry("301x200")
ll=Label(root,image=bck_end,)
ll.place(x=-1,y=-1)
et1=Entry(root,width=30,font=2)
et1.pack()
lb1=Label(root,fg="white")
lb1.pack()

def checklb():
    tf1=et1.get()
    jop_name = tf1
    job_title = []
    company_name = []
    locations_name = []
    skills = []
    links = []
    salary = []
    responsibilities = []
    date = []
    page_num = 0
    while True:
        # use request to fetch the url
        try:

            result = requests.get(f"https://wuzzuf.net/search/jobs/?a=hpb&q={jop_name}&start={page_num}")

            # save page content/markup
            src = result.content
            # print(src)

            # create soup object to parse content
            soup = BeautifulSoup(src, "lxml")

            page_limit = int(soup.find("strong").text)
            if (page_num > page_limit // 15):
                print("pages ended")
                break
            # print(soup)

            # find elements containing info we need
            # job titles, job skills, company names, location names
            job_titles = soup.find_all("h2", {"class": "css-m604qf"})
            company_names = soup.find_all("a", {"class": "css-17s97q8"})
            locations_names = soup.find_all("span", {"class": "css-5wys0k"})
            job_skills = soup.find_all("div", {"class": "css-y4udm8"})
            posted_old = soup.find_all("div", {"class": "css-do6t5g"})
            posted_new = soup.find_all("div", {"class": "css-4c4ojb"})
            posted = [*posted_new, *posted_old]

            page_num += 1

            print("page switched")
        except:
            print("error occurred")
            break

        # loop over returned lists to extract needed info into other lists
        for i in range(len(job_titles)):
            job_title.append(job_titles[i].text)
            company_name.append(company_names[i].text)
            locations_name.append(locations_names[i].text)
            skills.append(job_skills[i].text)
            links.append("https://wuzzuf.net" + job_titles[i].find("a").attrs['href'])
            date.append(posted[i].text)

    # for link in links:
    #     result = requests.get(link)
    #     src = result.content
    #     soup = BeautifulSoup(src, "lxml")
    #     salaries = soup.find("span", {"class":"css-47jx3m"})
    #     salary.append(salaries)

    # create csv file and fill it with values
    file_list = [job_title, company_name, date, locations_name, skills, links, salary]
    exported = zip_longest(*file_list)
    with open("jobsresult.csv", "w") as myfile:
        wr = csv.writer(myfile)
        wr.writerow(["job_title", "company_name", "date", "locations_name", "skills", "links", ])
        wr.writerows(exported)

btn1 = Button(root,text="Search",command=checklb,height=1,width=6,font=5,bg="red",background="grey",fg="white")
btn1.pack()
root.mainloop()
