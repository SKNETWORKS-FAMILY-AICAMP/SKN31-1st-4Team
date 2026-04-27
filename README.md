# 📚중고차 정밀 시세 조회 및 자차 견적 서비스 🚘🚗

## ⭐️ 팀 구성
<div align="center">

**🔥SKN31-1ST-4TEAM🔥**
---

<table align="center">
  <tr>
    <td align="center" width="190px"><img src="./images/Tayo.png" width="100" style="object-fit: contain; aspect-ratio: 1/1;"></td>
    <td align="center" width="190px"><img src="./images/Rani.png" width="100" style="object-fit: contain; aspect-ratio: 1/1;"></td>
    <td align="center" width="190px"><img src="./images/Gani.png"width="100" style="object-fit: contain; aspect-ratio: 1/1;"></td>
    <td align="center" width="190px"><img src="./images/Rogi.png" width="100" style="object-fit: contain; aspect-ratio: 1/1;"></td>
  </tr>
  <tr>
    <td align="center"><b>안혁진</b></td>
    <td align="center"><b>박하린</b></td>
    <td align="center"><b>박연아</b></td>
    <td align="center"><b>김가율</b></td>
  </tr>
  <tr>
    <td align="center"><sub><b>PM</br>METHOD ENGINEERING</br>HTML</b></sub></td>
    <td align="center"><sub><b>STREAMLIT</br>DATABASE</br>HTML</b></sub></td>
    <td align="center"><sub><b>DATA CRAWLING</br>DATABASE</b></sub></td>
    <td align="center"><sub><b>DATA CRAWLING</br>STREAMLIT</b></sub></td>
  </tr>
  <tr>
    <td align="center"><a href="https://github.com/Jinxxxok"><img src="https://img.shields.io/badge/Jinxxxok-181717?style=for-the-badge&logo=github&logoColor=white"></a></td>
    <td align="center"><a href="https://github.com/MintRinne"><img src="https://img.shields.io/badge/MintRinne-181717?style=for-the-badge&logo=github&logoColor=white"></a></td>
    <td align="center"><a href="https://github.com/yeona9549"><img src="https://img.shields.io/badge/yeona9549-181717?style=for-the-badge&logo=github&logoColor=white"></a></td>
    <td align="center"><a href="https://github.com/Kim-gayul"><img src="https://img.shields.io/badge/Kimgayul-181717?style=for-the-badge&logo=github&logoColor=white"></a></td>
  </tr>
</table>

</div>

---
## 목차
 - [개요](#개요)
 - [사용법](#사용법)
 - [Github 폴더 구조](#-GitHub-폴더-구조)
 - [Tech Stack](#-Tech-Stack)
 - [ERD](#ERD)
 - [데이터 출처 및 활용 현황](#데이터-출처-및-활용-현황)
 - [팀원 회고](#팀원-회고)
---
## 개요
> <font size="3">중고차 시장 데이터를 수집·분석하여 차량의 평균 시세, 가격 범위, 자차 견적을 제공하고, \
사용자가 합리적인 가격으로 거래할 수 있도록 돕는 데이터 기반 플랫폼</font>

---
## 사용법

terminal에서 실행 후
>pip install ./requirement.txt

실행환경에서 실행
> streamlit run main.py 실행


---
## 📁 GitHub 폴더 구조

```
SKN31-1st-4Team/
├── README.md  
├── main.py                           # 메인 streamlit 구동 파일
├── requirement.txt                   # 써드파티 모듈 환경설정 파일
├── .gitignore
│
├── assets/
│   ├── app.css                       # 메인 css 파일
│   └── images/
│       └── main_top_banner.png       # 배너 사진
│
├── images/                           # README 사진
│   ├── Gani.png
│   ├── Rani.png
│   ├── Rogi.png
│   ├── Tayo.png
│   └── ERD_images.png
│
├── pages/  
│   ├── 01_Market_Price.py            # 1페이지
│   └── 02_My_Car.py                  # 2페이지
│
└── src/
    ├── car_repository.py             # MySQL에서 데이터를 가져오는 메소드 모음
    ├── data_processor.py             # DB에서 받은 데이터를 화면 출력용으로 가공하는 함수 모음
    ├── utils.py                      # Streamlit 화면 출력 관련 공통 함수 모음
    ├── __init__.py
    └── csv/
        ├── usedcar_info.csv          # 전체 차량 데이터셋 csv
        └── DB_init.py                # DB 제작 + CSV파일 적재용 파일 (1회 구동)
```
### 💪🏻 Tech Stack
<table align="center">
  <tr>
    <td align="center" width="220">
      <strong>Frontend</strong><br/><br/>
      <img src="https://img.shields.io/badge/HTML5-F06529?style=for-the-badge&logo=HTML5&logoColor=61DAFB" alt="HTML5"/>
      <img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white" alt="Streamlit"/>
    </td>
    <td align="center" width="220">
      <strong>Backend</strong><br/><br/>
      <img src="https://img.shields.io/badge/Python-4B8BBE?style=for-the-badge&logo=Python&logoColor=white" alt="Python"/>
      <img src="https://img.shields.io/badge/Jupyter-F37626?style=for-the-badge&logo=Jupyter&logoColor=white" alt="Jupyter"/>
      <img src="https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=Pandas&logoColor=white" alt="Pandas"/>
    </td>
    <td align="center" width="220">
      <strong>Data</strong><br/><br/>
      <img src="https://img.shields.io/badge/MySQL-4479A1?style=for-the-badge&logo=mysql&logoColor=white" alt="MySQL"/>
      <img src="https://img.shields.io/badge/selenium-01A71C?style=for-the-badge&logo=selenium&logoColor=white" alt="Selenium"/>
    </td>
  </tr>
</table>

### ERD
<td align="center" width="190px"><img src="./images/ERD_images.png" width="350" style="object-fit: contain; aspect-ratio: 1/1;"></td>



### 데이터 출처 및 활용 현황

Encar   중고차 실매물 시세 정보 (usedcar_info.csv)\
전국자동차매매사업조합연합회    자동차 매매업계 공인 시세 정보 (usedcar_info.csv)\
**약 3000 여대**

**활용현황:** \
민간·공공 중고차 데이터를 결합하여 브랜드·모델별 \
최적 시세 산출 및 사고 이력을 반영한 가치 평가 모델 구축에 활용함.

---

### 팀원 회고

...
