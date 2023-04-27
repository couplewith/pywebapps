import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Python의 Scikit-learn 라이브러리를 활용하여
# 블로그 게시글을 추천 분류하는 콘텐츠 기반 필터링 알고리즘을 구현

# 게시글 데이터
articles = [
    {
        "id": 1,
        "title": "코로나19 대응 관련 정보",
        "content": "코로나19 대응 관련해서 최신 정보를 알려드립니다.",
        "tags": ["코로나19", "바이러스", "감염병"],
        "published_at": "2021-03-15"
    },
    {
        "id": 2,
        "title": "가을에 먹기 좋은 식재료 추천",
        "content": "가을에 먹기 좋은 식재료를 소개합니다.",
        "tags": ["식재료", "가을", "레시피"],
        "published_at": "2021-09-23"
    },
    {
        "id": 3,
        "title": "여행지 추천 - 제주도",
        "content": "제주도 여행을 가보세요. 멋진 자연 경관과 맛있는 음식을 즐길 수 있습니다.",
        "tags": ["여행", "제주도", "자연경관"],
        "published_at": "2022-01-05"
    }
]

# 게시글에서 태그 정보 추출
tags = []
for article in articles:
    tags.append(" ".join(article["tags"]))

# TF-IDF 벡터화
vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(tags)

#
