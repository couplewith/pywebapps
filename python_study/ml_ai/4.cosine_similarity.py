from sklearn.metrics.pairwise import cosine_similarity

# 유사도 계산
# 벡터화된 데이터를 활용하여 각각의 게시글 간의 유사도를 측정
# 대표적인 방법으로는 코사인 유사도(Cosine Similarity)를 사용

cos_sim = cosine_similarity(X)

print(cos_sim)
