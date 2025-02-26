import numpy as np
import pandas as pd

def generate_random_csv(file_name="random_data.csv", num_values=30720):
    # 20~250 사이의 랜덤한 정수 생성
    random_data = np.random.randint(20, 251, num_values)
    
    # 데이터프레임 생성 (한 줄짜리 CSV 구조)
    df = pd.DataFrame([random_data])
    
    # CSV 파일로 저장 (인덱스 없이, 헤더 없이 저장)
    df.to_csv(file_name, index=False, header=False)
    print(f"CSV 파일 '{file_name}' 생성 완료.")

# 실행
generate_random_csv()