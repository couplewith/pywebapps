
https://console.cloud.google.com/welcome?pli=1&project=agilebus123

# Oauth 인증  준비 구글에 API 등록 하기

1. API 및 서비스 를 선택
2. 사용자 인증 정보 : create credentials 선택
3. OAuth 2.0 클라이언트 ID 를 등록
4. 클라이언트 ID와 클라이언트비밀번호 를 복사 합니다.


엔드 /authorize 포인트는 리소스 소유자와 상호 작용하고 보호된 리소스에 액세스할 수 있는 권한을 얻는 데 사용됩니다. 
이를 더 잘 이해하기 위해 Google 계정을 사용하여 서비스에 로그인한다고 가정해 보겠습니다. 
먼저, 인증을 위해 서비스가 귀하를 Google로 리디렉션한 다음(아직 로그인하지 않은 경우) 동의 화면이 표시됩니다. 
여기에서 귀하의 일부 데이터(보호된 리소스)에 액세스하기 위해 서비스를 승인하라는 메시지가 표시됩니다. 
예를 들어 이메일 주소와 연락처 목록이 있습니다.



엔드포인트 의 요청 매개변수는 /authorize다음과 같습니다.

# 매개변수	설명
response_type	실행할 권한을 인증 서버에 알려줍니다.
response_mode	(선택사항) 승인 요청 결과의 형식이 지정되는 방식입니다. 값:
- query: 인증 코드 부여용. 302 Found트리거 리디렉션.
- fragment: 암시적 부여용입니다. 302 Found트리거 리디렉션.
- form_post: 200 OKHTML 양식에 숨겨진 매개변수로 포함된 응답 매개변수가 있습니다.
- web_message: 자동 인증용입니다. HTML5 웹 메시징을 사용합니다.
client_id	승인을 요청하는 애플리케이션의 ID입니다.
redirect_uri	URL을 보유합니다. 이 끝점에서 성공적으로 응답하면 이 URL로 리디렉션됩니다.
scope	애플리케이션에 필요한 공백으로 구분된 권한 목록입니다.
state	보안 목적으로 사용되는 불투명 값입니다. 이 요청 매개변수가 요청에 설정된 경우 의 일부로 애플리케이션에 반환됩니다 redirect_uri.
connection	비밀번호 없는 연결에 대한 연결 유형을 지정합니다.

 

# 2.인증 정보를 이용하여 프로필 가져오기

# * 받은 credential을 로딩합니다.
loaded_credentials = Credentials.from_authorized_user_info(flow.credentials)

# *  Google People API 클라이언트를 만듭니다.
people_service = build('people', 'v1', credentials=loaded_credentials)

# *  사용자의 프로필 정보를 가져옵니다.
person_info = people_service.people().get(
    resourceName='people/me',
    personFields='emailAddresses,photos'
).execute()

# *  이메일 정보 가져오기
email_addresses = person_info.get('emailAddresses', [])
if email_addresses:
    for email in email_addresses:
        print(f'Email: {email["value"]}')

# *  프로필 사진 가져오기
photos = person_info.get('photos', [])
if photos:
    for photo in photos:
        if 'default' in photo and photo['default']:
            photo_url = photo['url']
            print(f'Profile Photo URL: {photo_url}')