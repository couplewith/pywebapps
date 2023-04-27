from sklearn.feature_extraction.text import TfidfVectorizer

# 단어 벡터화
# 전처리된 데이터를 토큰화하고 벡터화합니다. 이를 위해 Scikit-learn의 TfidfVectorizer를 사용합니다.

vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform([content for title, content in cleaned_posts])

print(X.shape)
