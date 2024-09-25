import requests
from bs4 import BeautifulSoup
import re
import pandas as pd 
import time
from multiprocessing import Pool, cpu_count
import os
# Define the headers
headers = {
    'Cookie': '_fbp=fb.1.1725442731784.62912296124359481; _ga=GA1.1.9185171.1725442732; OnlineJudge=bbivmjfmvd0n489hm7u3hehcad; _ga_DHVLGG8PSY=GS1.1.1727234373.1.0.1727234373.0.0.0; aws-waf-token=ba6651cc-f3a1-456a-bc79-830a649820ef:AQoAtcUmcCEIAAAA:r3iMj7twUFH4xnL4lJY/HhLHYQW8rkTJTg30bToxVKdKp9vwq4/stydWXm0uJxrPm27+tP49RGaueX237l82sxRybB3lZHtrpEKECVsU1Rd6j0R2Ha3Ae1Uroa3pWnS//Lmvf53EUNFXmWvp/jTfBpF9tP7VAbqT8Pr9bMFqwTLkbend1rnzh79TNseZzR0UBhA=; __gads=ID=b22ebd4eac47d9e0:T=1725442785:RT=1727245621:S=ALNI_MYK2iDXPuIGQOcyzRw4FMnMMEuGAg; __gpi=UID=00000eed21c98b63:T=1725442785:RT=1727245621:S=ALNI_MYNOQi_V9e8wDJan3gA4n3P3Fsqwg; __eoi=ID=75970f6a2c2de243:T=1725442785:RT=1727245621:S=AA-Afja8DmBbU0duQSmmAhUzj7KN; _ga_C81GGQEMJZ=GS1.1.1727245620.13.1.1727245824.0.0.0; FCNEC=%5B%5B%22AKsRol-xCHwOJiI0lJGls_fVXIqGXtp8ty_0S3U3__PAgTy4Wwb3xNLPKYR9MRgyjUyV26s2gIpjRHiKDxPY4bCgEbxQTnG8WkXfIj9cXSCMH8vU7hiNCUdXQmrz63jEKtblA1urP4-kRr9Fgj0pp-iRcebdnFQLvQ%3D%3D%22%5D%5D',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36'
}

def crawl_and_save_problem(i):
    try:
        url = f'https://www.acmicpc.net/problem/{i}'
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')   
        if response.status_code == 404:
            print(f"Problem {i} not found (404). Skipping...")
            return
        title= soup.title.text
        tier=soup.find('img', class_='solvedac-tier')['src'].split('/')[-1].replace('.svg','')
        correct_rating=soup.find_all('tr')[1].find_all('td')[-1].text
        submit=soup.find_all('tr')[1].find_all('td')[2].text
        category=[]
        source=[]
        similar_problem=[]

        try:
            category_soup=soup.find('section',id='problem_tags').find_all('a')
            for data in category_soup:
                category.append(data.text)
        except:
            print('category field is null')
        try:
            source_soup=soup.find('section',id='source').find_all('a')
            for data in source_soup:
                source.append(data.text)
        except:
            print('source field is null')
        
        try:
            similar_problem_soup=soup.find('section', id='problem_association').find_all('a')
            for data in similar_problem_soup:
                similar_problem.append(data.text.split('번')[0])
        except:
            print('similar_problem field is null')

        url = f'https://www.acmicpc.net/submit/{i}'
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser') 
        try:
            langauge_soup=soup.find('select', id='language').find_all('option')
        except:
            langauge_soup=[]
            print('do not submit')
        language=[]
        for data in langauge_soup:
            language.append(data.text)
        data={
            'Title': title,
            'Tier': tier,
            'Correct_Rating': correct_rating,
            'Submit': submit,
            'Category': category,
            'Similar_Problems': similar_problem,
            'Source': source,
            'Language': language
        }
        df = pd.DataFrame([data])
        print(df)
        if i == 1000:
            df.to_csv('output.csv', mode='w', index=False, header=True)
        else:
            df.to_csv('output.csv', mode='a', index=False, header=False)

        print(f"Problem {i} 데이터가 저장되었습니다.")
        # time.sleep(0.5)

    except Exception as e:
        print(e)
        print(f"Problem {i}에서 에러 발생: {e}")

def main():
    num_processes = cpu_count()
    with Pool(num_processes) as pool:
        pool.map(crawl_and_save_problem, range(1000, 36000))
if __name__ == "__main__":
    main()