# 필요한 모듈 임포트
from web3 import Web3
from web3.auto import w3

# Ethereum 노드에 연결
web3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/YOUR_INFURA_PROJECT_ID'))

# 랜덤한 프라이빗 키 생성
private_key = web3.eth.account.create().privateKey.hex()

# 프라이빗 키로 월렛 주소 생성
address = web3.eth.account.privateKeyToAccount(private_key).address

# 결과 출력
print("프라이빗 키: ", private_key)
print("월렛 주소: ", address)


#Python 언어와 web3 라이브러리를 사용하여 Ethereum 블록체인 월렛을 생성하는 방법을 보여줍니다.
# 코드 실행 시, Infura 프로젝트 ID를 YOUR_INFURA_PROJECT_ID 부분에 적절히 입력해야 합니다.
# 프라이빗 키와 월렛 주소가 출력됩니다.