"""
Parse exam tickets from prombez24.com, with answers, in Anki format
"""

import requests
from bs4 import BeautifulSoup


def get_html(url):
    r = requests.get(url)
    return r.text


def get_data(html):
    file = open("../tk_1/prombez/prombez.txt", "w", encoding='utf-8')

    soup = BeautifulSoup(html, 'lxml')

    exams = soup.find_all('div', class_='question row')

    for exam in exams:
        question = exam.find('div', class_='question__text').text
        find_answer = exam.find_all('div', class_='question__answers-list')
        file.write('\n__' + question + '__\n')

        for ans in find_answer:
            answer = ans.find_all('div', class_='question__answers-list-item')

            for i in answer:
                final_ans = i.find('div', class_='checkbox').find('span', class_='label').text
                file.write('- ' + final_ans + '\n')

            for a in answer:
                if a.find('input', value='true'):
                    final_ans = a.find('div', class_='checkbox').find('span', class_='label').text
                    file.write('?\n' + final_ans + '\n')
                    
            file.write('\n' + '\n' '---' + '\n')
    file.close()


def main():
    # url = 'https://prombez24.com/ticket/ordered?testId=152&page=0&size=257'
    # url = 'https://prombez24.com/ticket/ordered?testId=204&page=0&size=167'
    url = 'https://prombez24.com/ticket/ordered?testId=152&page=0&size=200'
    get_data(get_html(url))


if __name__ == '__main__':
    main()
