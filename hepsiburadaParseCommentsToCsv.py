from selenium import webdriver
import time
import csv
from math import ceil

commentCategoryValue = {"Çok İyi":5, "İyi":4, "Ne İyi / Ne Kötü":3, "Kötü":2, "Çok Kötü":1}

def GetLaptopPage(pageNumber):
    return f"https://www.hepsiburada.com/laptop-notebook-dizustu-bilgisayarlar-c-98?sayfa={pageNumber}"

def GetCommentPage(baseURL, pageNumber, commentRate):
    return f"{baseURL}?sayfa={pageNumber}&filtre={commentRate}"

driver = webdriver.Chrome("drivers\\chromedriver.exe")
driver.get(GetLaptopPage(2))

time.sleep(1)

laptopsUL   = driver.find_element_by_xpath("//ul[@class='product-list results-container do-flex list']")
laptopsLIs  = laptopsUL.find_elements_by_tag_name("li")

laptopCommentURLs = []

for LI in laptopsLIs:
    laptopLink = LI.find_element_by_tag_name("a").get_attribute("href")
    laptopCommentLink = laptopLink + "-yorumlari"
    laptopCommentURLs.append(laptopCommentLink)

for laptopCommentLink in laptopCommentURLs:
    driver.get(laptopCommentLink)
    time.sleep(1)

    commentCategoriesBlock      = driver.find_element_by_xpath("//div[@class='hermes-RateFilterBox-module-3K8Gz']")
    commentCategories           = commentCategoriesBlock.find_elements_by_xpath("//div[@class='hermes-RateFilter-module-Zdi01']")

    examineCategoryRates = []

    for x in commentCategories:
        categoryText         = x.find_element_by_css_selector("div.hermes-RateFilter-module-1Py-g").text
        categoryName         = categoryText[: categoryText.find("(")-1]
        categoryCommentCount = int(categoryText[categoryText.find("(")+1:-1])

        if categoryCommentCount == 0:
            continue
        
        examineCategoryRates.append([commentCategoryValue[categoryName], ceil(categoryCommentCount/20)])

    comments = []
    for commentRate, commentPageCount in examineCategoryRates:
        subComments = []
        for x in range(1, commentPageCount + 1):
            driver.get(GetCommentPage(laptopCommentLink, x, commentRate))
            time.sleep(1)
            print(f"{commentRate} değerlendirme puanlı sayfanın {x} numaralı alt sayfası açıldı.")
            
            commentsBlockOut = driver.find_element_by_xpath("//div[@class='paginationContentHolder']")
            commentsBlockIn  = commentsBlockOut.find_elements_by_css_selector("div.hermes-ReviewCard-module-34AJ_")

            for c in commentsBlockIn:
                try:
                    comment = c.find_element_by_css_selector("span[itemprop='description']").text
                    comment = comment.replace("\n", " ")
                    subComments.append([comment, commentRate])
                except:
                    pass

        comments.append(subComments)

    csvfile = open("C:\\Users\\abatox\\Desktop\\yorumlar.csv", "a", newline='', encoding='UTF-8')
    writer = csv.writer(csvfile, delimiter=" ")
    for c in comments:
        for x in c:
            writer.writerow(x)
    csvfile.close()
    print("Ürünün yorumları dosyaya işlendi.")
