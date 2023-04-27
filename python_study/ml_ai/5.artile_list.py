import numpy as np


# 추천 목록 생성
# 사용자가 선호하는 게시글과 유사한 게시글을 추천 목록으로 생성


# 선호하는 게시글
preference = "딥러닝 기초"

# 선호하는 게시글의 벡터화
preference_vec = vectorizer.transform([preference])

# 코사인 유사도 계산
sim_scores = list(enumerate(cos_sim[preference_vec.toarray()[0]>0][0]))

# 유사도에 따라 정렬
sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

# 상위 10개 게시글 추천
top_n = 10
recommendations = [(cleaned_posts[i][0], sim) for i, sim in sim_scores[:top_n]]

print(recommendations)
