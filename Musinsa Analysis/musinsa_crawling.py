import requests
from bs4 import BeautifulSoup
import re
import time
import csv
import numpy as np

def make_soup_for_page(page): #특정 page를 크롤링하는 함수
     #"http://store.musinsa.com/app/items/lists/003/?category=&d_cat_cd=003&&sort=emt_high&display_cnt=100&page="
    url = "http://store.musinsa.com/app/items/lists/001001/?category=&d_cat_cd=001001&sort=emt_high&display_cnt=150&page="
    url_len = len(url)
    url = url[:url_len]+str(page)#해당 page의 url을 동적으로 받아옴
    source_code = requests.get(url)
    plain_text = source_code.text
    page_soup = BeautifulSoup(plain_text, 'lxml')
    return page_soup #Beatuitiful soup 객체 page_soup를  반환


def find_a_href(soup): #page_soup를 받아  특정 상품으로의 링크를 가져오는 함수
    links_list = []
    goods_list = soup.find_all('div', {'class': "list_img"})  # div 태그의 class가 "list_img"인 부분을 모두 찾아 리스트로 반환
    p = re.compile(r"<a href=\"(.*?)\">")  # 링크에 해당하는 패턴을 컴파일

    for good in goods_list:
        link = p.search(str(good)).group(1)
        links_list.append(link)
    return links_list  # 상품 세부 정보(해당 페이지)로의 링크들을 저장한 리스트


def make_soup_for_good(link): #특정제품의 정보를 받아오는 함수
    url_good = "http://store.musinsa.com" + link
    source_code = requests.get(url_good)
    plain_text = source_code.text
    good_soup = BeautifulSoup(plain_text, 'html5lib')
    return good_soup #특정 제품에 대한 beautiful soup 객체를 반환


def find_bottom_details(good_soup):  #상품의 기본정보를 저장하는 함수

    try: #우선 세부 사이즈 정보를 저장한 테이블의 존재 유무를 확인
        sizes_list = [s.text for s in
                      good_soup.find('table', {'class': 'table_th_grey'}).find('tbody').find_all('th')[1:]]
    except:
        sizes_list = []

    finally:
        good_details = []

        cnt_sizes = 1
        if len(sizes_list) != 0: # 사이즈 테이블이 존재하는 경우
            cnt_sizes = len(sizes_list)

        for i in range(cnt_sizes):  # 제품별로 출시되는 사이즈 종류의 개수가 다르므로 cnt_sizes개 만큼 데이터 생성
            tmp = []

            # 브랜드
            brand = good_soup.find('p', {'class': 'brand'}).find('span').text
            tmp.append(brand)
            # 제품명
            name = good_soup.find('span', {'class': 'product_title'}).find('span', {'class': 'product_title_eng'}).text
            tmp.append(name)
            # 제품 분류
            category = re.compile(r">(.*)$").search(good_soup.find('p', {'class': 'item_categories'}).text).group(
                1).strip()
            tmp.append(category)
            # 가격
            price = re.compile(r"\d+[,]\d+").search(good_soup.find('span', {'id': 'goods_price'}).text).group()
            tmp.append(price)
            # 좋아요
            likes = good_soup.find('span', {'class': 'prd_like_cnt'}).text
            tmp.append(likes)

            if (len(sizes_list) != 0):  # 사이즈 변수의 테이블이 존재
                L = good_soup.find('table', {'class': 'table_th_grey'}).find('tbody').find_all('td', {
                    'class': 'goods_size_val'})
                if (len(L) % 5 == 0):  # 세부사이즈 5항목 모두 존재
                    size_details = [s.text for s in L[i * 5:(i + 1) * 5]]
                else:
                    size_details = [np.nan, np.nan, np.nan, np.nan, np.nan]  # 세부사이즈 모두 존재 않으면 비워둠

                size = sizes_list[i]

            elif (len(sizes_list) == 0):  # 사이즈 변수의 테이블이 존재안함
                size_details = [np.nan, np.nan, np.nan, np.nan, np.nan]
                size = np.nan

            # 사이즈
            tmp.append(size)

            # 총장 허리단면 허벅지단면 밑위 밑단단면
            for val in size_details:
                tmp.append(val)
            # 이미지
            img = "https:" + re.compile(r"src=\"(.*?)\"").search(
                str(good_soup.find('div', {'class': 'product-img'}).find('img'))).group(1)
            tmp.append(img)

            # if(len(tmp)!=12):
            # continue

            good_details.append(tmp)

        return good_details # 제품별 기본정보를 리스트로 저장한 이중 리스트 good_details를 리턴


def find_reviews(good_soup): #해당 제품의 구매후기를 가져오는 함수
    reviews = []
    for chd in good_soup.find('div', {'id': 'estimate_list'}).div.div.children:

        if type(chd) == type( chd.parent.div):  # <class 'bs4.element.Tag'> 만 뽑기  ##그런데 isinstance(chd, bs4.element.Tag) 왜 안먹을까?
            try:
                name = chd.find('div', {'class': 'content_object'}).a.text
                name = re.sub(r"\s구매", "", name).strip()
                name = name.replace('\xa0', ' ')  # xa0로 인해 오류나는 경우 있어 변환
                size = chd.find('div', {'class': 'content_object'}).a.span.text[:-2].strip()
                date = chd.find('span', {'class': 'date'}).text.strip()
                rating = re.search('\w+(?=\"><)', str(chd.find('div', {'class': 'tit'}))).group()[6:]
                title = chd.find('div', {'class': 'tit'}).text.strip()
                comment = chd.find('span', {'class': 'content-review'}).text.strip()

                reviews.append([name, size, date, rating, title, comment])

            except Exception as e:
                continue

    return reviews #r제품별 구매후기를 리스트로 저장한 이중 리스트  reviews를 반환




if __name__ == "__main__":

    # 상품 하나를 test
    start = time.time()
    soup1 = make_soup_for_page(1)
    link_list1 = find_a_href(soup1)
    good_soup1 = make_soup_for_good(link_list1[1])

    good1 = find_bottom_details(good_soup1)
    reviews1 = find_reviews(good_soup1)

    end = time.time()
    print("time for a good :", end - start)
    print(good1)
    print(reviews1)


if __name__ == "__main__":
    # 전체 약 20000개의 상품
    s = time.time()
    fp1 = open("data_bottom1.csv", 'a', newline='', encoding='cp949')
    fp2 = open("data_T_reviews.csv", 'a', newline='', encoding='cp949')
    wr1 = csv.writer(fp1)
    wr2 = csv.writer(fp2)

    for i in range(1, 206):
        page_soup = make_soup_for_page(i)
        for link in find_a_href(page_soup):
            try:
                good_soup = make_soup_for_good(link)

                for found in find_bottom_details(good_soup): #제품 기본정보를 한줄씩 파일 출력
                    wr1.writerow(found)

                for review in find_reviews(good_soup): #역시 구매후기를 한줄씩 파일출력
                    wr2.writerow(review)

            except:
                continue

    fp1.close()
    fp2.close()
    e = time.time()
    print("time for a page:", (e - s))
