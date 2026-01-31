# BZPP 정보보안 채용공고 크롤러

비즈니스피플(bzpp.co.kr)에서 정보보안 관련 채용공고를 수집하는 Python 크롤러입니다.

## 요구사항

- Python 3.6+
- 추가 패키지 불필요 (표준 라이브러리만 사용)

## 사용법

```bash
python3 crawler.py
```

실행 시 자동으로 모든 정보보안 채용공고를 수집하고 JSON 파일로 저장합니다.

## 출력 파일

`bzpp_recruits_YYYYMMDD_HHMMSS.json` 형식으로 저장됩니다.

### JSON 구조

```json
{
  "meta": {
    "total_count": 232,
    "collected_count": 222,
    "collected_at": "2026-01-31T11:22:22"
  },
  "list": [
    {
      "HOST": "회사명",
      "TITLE": "공고 제목",
      "NM_LOC": "지역",
      "NM_TYPE": "정규직/계약직",
      "YMD_START": "20260130",
      "YMD_END": "20260301",
      "BIZ_TAG": "관련 키워드",
      "NUM_CAREERSTART": "최소 경력(년)",
      "NUM_CAREEREND": "최대 경력(년)",
      "DETAILPATH": "https://www.bzpp.co.kr/biz/businessDetailView/BR..."
    }
  ]
}
```

### 필드 설명

| 필드 | 설명 |
|------|------|
| HOST | 채용 회사명 |
| TITLE | 채용공고 제목 |
| NM_LOC | 근무 지역 |
| NM_TYPE | 고용 형태 (정규직, 계약직 등) |
| YMD_START | 공고 시작일 (YYYYMMDD) |
| YMD_END | 공고 마감일 (YYYYMMDD) |
| BIZ_TAG | 관련 키워드 (쉼표 구분) |
| NUM_CAREERSTART | 최소 경력 요건 (년) |
| NUM_CAREEREND | 최대 경력 요건 (년) |
| DETAILPATH | 채용공고 상세 페이지 URL |

## 수집 대상

정보보안 테마(TM210107A00004)에 해당하는 채용공고:
- 정보보안, 정보보호, 침해사고, 개인정보보호
- CCNA, CCNP, CPPA, PIMS, CISA, CISSP
- 보안관제, 화이트해커, 보안진단, 모의해킹
- 보안엔지니어, 보안감사, 클라우드보안
- 네트워크보안, 사이버보안 등

## 라이선스

MIT
