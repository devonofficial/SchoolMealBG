SchoolMealBG
=============
[NEIS Open API](https://open.neis.go.kr/portal/data/service/selectServicePage.do?infId=OPEN17320190722180924242823&infSeq=1)로 급식 정보를 불러와 바탕화면으로 만들어주는 프로그램입니다!

`제작자: 663415`

사용 방법
-------------
먼저 NEIS에서 인증키를 발급받고, 원하는 학교의 시도교육청코드와 표준학교코드를 구해주세요.

이후 아래와 같이 `credentials.json`을 작성해 `SchoolMealBG.py`와 같은 폴더에 넣어주면 됩니다.
```json
{
    "APIKey": "발급받은 인증키",
    "ProvinceCode" : "시도교육청코드", //충청남도교육청은 N10
    "SchoolCode" : "표준학교코드"      //공주사대부고는 7004629
}
```

만약 다른 바탕화면에 적용하고 싶다면 `📁img` 폴더의 `BG.png`를 삭제하고 원하는 사진으로 바탕화면을 바꿔주신 후 실행하면 됩니다.

파일 설명
-------------
```
📁SchoolMealBG
├── 📁font
│   ├── GmarketSansBold.otf
│   └── SCDream5.otf
├── 📁img
│   ├── METADATA
│   ├── Example.png
│   ├── overlay.png
│   ├── CleanBG.png   (미포함)
│   ├── BG.png        (미포함)
│   └── TodayMeal.png (미포함)
├── .gitignore
├── README.md
├── SchoolMealBG.py
└── credentials.json  (미포함)
``` 

### 📁font
- `GmarketSansBold.otf` : <br> G마켓 산스 Bold(제목에 사용) - [다운로드](https://corp.gmarket.com/fonts/)

- `SCDream5.otf` : <br> 에스코어 드림 5 Medium(본문에 사용) - [다운로드](https://s-core.co.kr/company/font2/)

### 📁img
- `METADATA` : <br> 비밀입니다😉 <!-- 확장자를 .png로 바꾸면 뭔가 나올지도...? -->

- `Example.png` : <br> 프로그램 예시 사진(실제 프로그램에서는 미사용)

- `overlay.png` : <br> 기존 바탕화면에 덮는 사진

- `CleanBG.png` : <br> 기존 바탕화면(자동으로 저장됨)

- `BG.png` : <br> 바탕화면 합성용 틀(자동으로 만들어짐)

- `TodayMeal.png` : <br> 완성된 바탕화면(자동으로 만들어짐)

### 이외
- `.gitignore` : <br> github에 올리지 않을 것들의 리스트

- `README.md` : <br> 지금 읽고 계신 바로 이 파일

- `SchoolMealBG.py` : <br> 메인 코드

- `credentials.json` : <br> 인증키를 저장하는 파일