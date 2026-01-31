#!/usr/bin/env python3
"""BZPP 정보보안 채용공고 크롤러"""

import urllib.request
import urllib.parse
import json
from datetime import datetime


def fetch_recruit_list(page_num=1, page_size=30):
    """채용공고 목록을 가져옵니다."""
    url = 'https://www.bzpp.co.kr/api/recruit/getRecruitList'

    payload = {
        'cdPeople': '',
        'listFlag': '',
        'orderBy': 'NORMAL',
        'searchBizArea1': '',
        'searchBizArea2': '',
        'searchJob1': '',
        'searchJob2': '',
        'searchStartCareer': '',
        'searchEndCareer': '',
        'searchPosition': '',
        'searchEmpType': '',
        'searchEdu': '',
        'searchAddr1': '',
        'cdCollection': '',
        'gbCollection': 'R',
        'seqChnParent': '',
        'pageNum': str(page_num),
        'pageSize': str(page_size),
        'startOffset': str((page_num - 1) * page_size),
        'endOffset': str(page_num * page_size),
        'srchTagName': '',
        'srchRecruitEnterpriseList': '',
        'gbTypeMenu': 'NONE',
        'attrCondition': '',
        'tagFlag': 'N',
        'positionTag': '',
        'isTagOpen': 'N',
        'closeFlag': 'N',
        'closeSearchText': '',
        'cdTheme': 'TM210107A00004',
        'themeTag': '정보보안,정보보호,침해사고,개인정보보호,CCNA,CCNP,CPPA,PIMS,CISA,CISSP,보안관제,화이트해커,보안진단,모의해킹,보안엔지니어,보안감사,클라우드보안,보안솔루션,사이버보안,PenetrationTesting,네트워크보안,보안구축,해킹대응,네트워크엔지니어,네트워크설계',
        'inTheme': '',
        'outTheme': 'BR210714A00130',
        'cdTypeTheme': 'CL80201',
        'themeCdGroup': '',
        'tabMenu': 'ALL',
        'bizToggle': 'Y',
        'searchGbCareerChk_1': '1',
        'searchGbCareerChk_2': '2',
        'searchGbCareerChk_3': '4',
        'searchAllCareer': 'N',
        'cdGroup': '',
        'cdGrType': '',
        'nmGroup': ''
    }

    data = urllib.parse.urlencode(payload).encode('utf-8')
    req = urllib.request.Request(url, data=data, method='POST')
    req.add_header('Content-Type', 'application/x-www-form-urlencoded')
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36')

    with urllib.request.urlopen(req, timeout=30) as response:
        return json.loads(response.read().decode('utf-8'))


BASE_URL = 'https://www.bzpp.co.kr'


def simplify_item(item):
    """필요한 필드만 추출합니다."""
    cd_business = item.get('CD_BUSINESS', '')
    return {
        'HOST': item.get('HOST', ''),
        'TITLE': item.get('TITLE', ''),
        'NM_LOC': item.get('NM_LOC', ''),
        'NM_TYPE': item.get('NM_TYPE', ''),
        'YMD_START': item.get('YMD_START', ''),
        'YMD_END': item.get('YMD_END', ''),
        'BIZ_TAG': item.get('BIZ_TAG', ''),
        'NUM_CAREERSTART': item.get('NUM_CAREERSTART', ''),
        'NUM_CAREEREND': item.get('NUM_CAREEREND', ''),
        'DETAILPATH': f'{BASE_URL}/biz/businessDetailView/{cd_business}' if cd_business else ''
    }


def fetch_all_recruits():
    """모든 채용공고를 가져옵니다."""
    page_size = 50
    first_page = fetch_recruit_list(page_num=1, page_size=page_size)

    total_count = first_page['result']['total_count']
    all_items = [simplify_item(item) for item in first_page['list']]

    print(f"총 {total_count}건의 공고를 수집합니다...")
    print(f"1페이지 완료 ({len(all_items)}/{total_count})")

    # 나머지 페이지 수집
    total_pages = (total_count + page_size - 1) // page_size
    for page in range(2, total_pages + 1):
        result = fetch_recruit_list(page_num=page, page_size=page_size)
        all_items.extend([simplify_item(item) for item in result['list']])
        print(f"{page}페이지 완료 ({len(all_items)}/{total_count})")

    # 중복 제거 (TITLE + HOST 기준)
    seen = set()
    unique_items = []
    for item in all_items:
        key = (item['HOST'], item['TITLE'])
        if key not in seen:
            seen.add(key)
            unique_items.append(item)

    return {
        'meta': {
            'total_count': total_count,
            'collected_count': len(unique_items),
            'collected_at': datetime.now().isoformat()
        },
        'list': unique_items
    }


def save_to_json(data, filename=None):
    """JSON 파일로 저장합니다."""
    if filename is None:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'bzpp_recruits_{timestamp}.json'

    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"저장 완료: {filename}")
    return filename


def main():
    print("BZPP 정보보안 채용공고 크롤링 시작...")
    data = fetch_all_recruits()
    filename = save_to_json(data)
    print(f"\n수집 완료!")
    print(f"- 총 공고 수: {data['meta']['collected_count']}건 (중복 제거됨)")
    print(f"- 저장 파일: {filename}")


if __name__ == '__main__':
    main()
