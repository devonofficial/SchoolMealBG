import ctypes, json, os, random, re, requests, sys, urllib3
from datetime import datetime, timedelta
from PIL import Image, ImageDraw, ImageFont

Hour = datetime.today().hour # 작동 시각
FilePath = os.path.dirname(os.path.abspath(__file__)) # 파일이 위치한 경로
DBExpireDays = 14 # 데이터베이스 최소 업데이트 주기(일)

# 작동 시각에 따라 MealCode 정의 - 0이면 점심, 1이면 저녁, 2이면 다음날 아침
# 최종적으로 바탕화면에 뜰 OutputDate 역시 정의
OutputDate = datetime.today().strftime("%Y%m%d")
if Hour >= 17:
    MealCode = 2
    OutputDate = (datetime.today() + timedelta(days=1)).strftime("%Y%m%d")
elif Hour >= 12:
    MealCode = 1
else:
    MealCode = 0

try:
    with open(FilePath+"/database.json", 'r', encoding="utf-8") as f:
        MealDB = json.load(f)
        # 데이터베이스 파일이 존재하지 않을 시 여기서 FileNotFoundError 발생
    OutputText = MealDB["MealInfo"][OutputDate][["중식","석식","조식"][MealCode]]
    # 현재 띄워야 할 급식 정보가 없을 시 여기서 KeyError 발생
    DateDiff = datetime.today() - datetime.strptime(MealDB["LastUpdateDate"], "%Y%m%d")
    if DateDiff.days > DBExpireDays or len(sys.argv) < 2 :
        raise FileNotFoundError
        # 마지막 데이터베이스 업데이트 날짜가 DBExpireDays일보다 전일 시 or 인자가 없이 전달되었을 시(수동으로 실행되었을 시) FileNotFoundError 발생
        
except (KeyError, FileNotFoundError):
    with open(FilePath+"/credentials.json", 'r', encoding="utf-8") as f:
        cred = json.load(f)
    params = {"KEY" : cred["APIKey"], "Type" : "json", "ATPT_OFCDC_SC_CODE" : cred["ProvinceCode"], "SD_SCHUL_CODE" : cred["SchoolCode"], "MLSV_FROM_YMD" : OutputDate}
    requestURL = "https://open.neis.go.kr/hub/mealServiceDietInfo"
    
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning) # request 시 뜨는 경고 메세지 안 뜨게 처리
    html = requests.get(requestURL, params=params, verify=False).text
    APIRespose = json.loads(html)["mealServiceDietInfo"][1]["row"]

    MealDict = {}
    for i in APIRespose: # API로 불러온 데이터 파싱
        MealDate = i["MLSV_YMD"]
        MealName = i["MMEAL_SC_NM"]
        Meal = re.sub("(\s*\(([0-9]*[\.])*\))|(\/고|\(공\)|\(즐\))","",i["DDISH_NM"]) # 알레르기 유발 식재료 정보, "/고", "(공)", "(즐)" 삭제
        Meal = re.sub("\s*<br\/>\s*","\n",Meal) # <br/>을 \n으로 교체
        try:
            MealDict[MealDate][MealName] = Meal
        except KeyError: # 해당 MealDate에 대응하는 키 값이 없을 때
            MealDict[MealDate] = {MealName : Meal}

    # 데이터베이스 작성
    WriteDB = {"LastUpdateDate" : OutputDate, "MealInfo" : MealDict}
    with open(FilePath+"/database.json", 'w', encoding="utf-8") as f:
        f.write(json.dumps(WriteDB, ensure_ascii=False, indent=4))

    try:
        OutputText = WriteDB["MealInfo"][OutputDate][["중식","석식","조식"][MealCode]]
    except KeyError:
        OutputText = "급식 정보를\n불러올 수\n없습니다."

# 월/일 정의하기
month = OutputDate[4:6]
if month.startswith("0"):
    month = month[1:]
day = OutputDate[6:]
if day.startswith("0"):
    day = day[1:]

# 만우절용 코드 - 4월 1일 당일 점심, 저녁 메뉴에 장난질
if month == '4' and day == '1' and MealCode != 2 and os.path.exists(FilePath+'/img/METADATA'):
    OutputText = re.sub("[ \t\r\f\v]","",OutputText) # \n을 제외한 공백 삭제
    RandomSum = 0
    WhileNum = 0
    while RandomSum < len(OutputText): # 랜덤 띄어쓰기 추가
        RandomSum += random.randrange(2,6)
        OutputText = OutputText[:RandomSum+WhileNum] + "  " + OutputText[RandomSum+WhileNum:]
        WhileNum += 2
    
    # 요소 합성
    target_image = Image.open(os.getenv('APPDATA')+'\Microsoft\Windows\Themes\TranscodedWallpaper').resize((1920,1080))
    target_image = target_image.convert('RGBA')
    bonobono = Image.open(FilePath+'/img/METADATA')
    target_image = Image.alpha_composite(target_image, bonobono)

    # 폰트 정의
    try:
        BigGulim = ImageFont.truetype('C:\Windows\Fonts\Gulim.ttc', size = 80)
        SmallGulim = ImageFont.truetype('C:\Windows\Fonts\Gulim.ttc', size = 50)
    except:
        BigGulim = ImageFont.truetype(FilePath+'/font/GmarketSansBold.otf', size = 80)
        SmallGulim = ImageFont.truetype(FilePath+'/font/SCDream5.otf', size = 50)

    # 텍스트 추가 및 바탕화면 설정
    drawmeal = ImageDraw.Draw(target_image)
    drawmeal.text((1214,176),f"만우절 {['점심', '저녁', '아침'][MealCode]}",fill="black",font=BigGulim,align='left')
    drawmeal.multiline_text((1220,304), OutputText, fill="black", font=SmallGulim, spacing=20, align="left")
    target_image.save(FilePath+"/img/TodayMeal.png")
    ctypes.windll.user32.SystemParametersInfoW(20, 0, FilePath+"/img/TodayMeal.png", 3)

# 기본 틀 제작하기
else:
    if os.path.exists(FilePath+'/img/BG.png') == False: # 기존에 만들어놓은 합성용 틀이 없을 시
        target_image = Image.open(os.getenv('APPDATA')+'\Microsoft\Windows\Themes\TranscodedWallpaper').resize((1920,1080))
        target_image.save(FilePath+"/img/CleanBG.png")

        # 요소 합성 및 저장
        target_image = target_image.convert('RGBA')
        overlay = Image.open(FilePath+'/img/overlay.png')
        target_image = Image.alpha_composite(target_image, overlay)
        target_image.save(FilePath+"/img/BG.png")

    # 폰트 정의
    Gsans = ImageFont.truetype(FilePath+'/font/GmarketSansBold.otf', size = 80)
    Edream = ImageFont.truetype(FilePath+'/font/SCDream5.otf', size = 50)

    # 텍스트 추가 및 바탕화면 설정
    bg_image = Image.open(FilePath+'/img/BG.png')
    drawmeal = ImageDraw.Draw(bg_image)
    drawmeal.text((1214,176),f"{month}월 {day}일 {['점심', '저녁', '아침'][MealCode]}",fill="white",font=Gsans,align='left')
    drawmeal.multiline_text((1220,304), OutputText, fill="white", font=Edream, spacing=20, align="left")
    bg_image.save(FilePath+"/img/TodayMeal.png")
    ctypes.windll.user32.SystemParametersInfoW(20, 0, FilePath+"/img/TodayMeal.png", 3)