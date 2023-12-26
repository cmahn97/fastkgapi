from fastapi import FastAPI, Query 
from typing import List  # List 타입을 위한 typing 모듈 가져오기
import pandas as pd  
import uvicorn  

app = FastAPI()  # FastAPI 앱 인스턴스 생성

# 데이터 로드
df = pd.read_csv("kg3.csv")  

# 첫 번째 페이지로 이동
@app.get("/")  # 루트 경로('/')에 대한 GET 요청 처리
async def read_item():
    return {"message": "Welcome to our app"}  # 환영 메시지 출력

@app.get("/diagnosis")  # '/diagnosis' 경로에 대한 GET 요청 처리
async def get_diagnosis_list(symptom_ids: List[int] = Query(...)):
    dat = df[df['y_index'].isin(symptom_ids)]  # 주어진 증상 ID에 해당하는 데이터 필터링

    return {'diagnosis_ids': dat['x_index'].unique().tolist()}  # 진단 ID 목록 반환

@app.get("/symptoms")  # '/symptoms' 경로에 대한 GET 요청 처리
async def get_symptom_list(diagnosis_ids: List[int] = Query(...), excluded_symptom_ids: List[int] = Query(...)):
    dat = df[df['x_index'].isin(diagnosis_ids)]  # 주어진 진단 ID에 해당하는 데이터 필터링

    if excluded_symptom_ids:  # 제외할 증상 ID가 있는 경우
        dat = dat[~dat['y_index'].isin(excluded_symptom_ids)]  # 해당 증상 ID 제외

    return {'symptom_ids': dat['y_index'].unique().tolist()}  # 증상 ID 목록 반환
