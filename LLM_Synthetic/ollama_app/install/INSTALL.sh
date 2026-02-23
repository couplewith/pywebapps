

# 최신 릴리즈 페이지: https://github.com/ollama/ollama/releases (github.com in Bing)4

curl -L https://github.com/ollama/ollama/releases/download/v0.13.5/ollama-linux-amd64.tgz -o ollama-linux-amd64.tgz

sudo tar zx -C /usr/local   -f ollama-linux-amd64.tgz



# 기존 ollama 삭제 : 
Remove ollama libraries from your lib directory (either /usr/local/lib, /usr/lib, or /lib):

Uninstall

sudo systemctl stop ollama
sudo systemctl disable ollama
sudo rm /etc/systemd/system/ollama.service

sudo rm -r $(which ollama | tr 'bin' 'lib')





file /usr/local/bin/ollama
→ 이제 ELF 64-bit LSB pie executable, x86-64 로 나와야 정상입니다.


##############################################3
sudo useradd -r -s /bin/false -U -m -d /usr/share/ollama ollama
sudo usermod -a -G ollama $(whoami)

groupmod -g 2000 ollama
usermod  -g 2000 -u 2000  ollama




/etc/systemd/system/ollama.service


[Unit]
Description=Ollama Service
After=network-online.target

[Service]
ExecStart=/usr/bin/ollama serve
User=ollama
Group=ollama
Restart=always
RestartSec=3
Environment="PATH=$PATH"

[Install]
WantedBy=multi-user.target





systemctl daemon-reload

systemctl stop ollama

systemctl status ollama
systemctl start ollama


 로그 확인 
  journalctl -e -u ollama


DeepSeek 모델 다운로드 및 실행

bash
ollama pull deepseek
ollama run deepseek



#########################
sudo apt update
sudo apt install -y ca-certificates
sudo update-ca-certificates




#############################3

4. 루트 CA 직접 추가 (고급)
Ollama 레지스트리의 인증서 체인을 확인:

bash
openssl s_client -connect registry.ollama.ai:443 -showcerts
출력된 인증서 중 루트 CA를 /usr/local/share/ca-certificates/ollama.crt 로 저장

갱신:

bash
sudo update-ca-certificates




############################

루트 CA 블록 복사 : 출력된 인증서 중 루트 CA 부분을 통째로 복사합니다.
openssl s_client -connect registry.ollama.ai:443 -showcerts > b

b 에서 
 - 마지막 부분을 복사
-----BEGIN CERTIFICATE-----
MIID...
...내용...
-----END CERTIFICATE-----
-----BEGIN CERTIFICATE-----
MIIF...
...내용...
-----END CERTIFICATE-----



복사한 내용을 /usr/local/share/ca-certificates/ollama.crt 파일에 저장합니다:
cat a > /usr/local/share/ca-certificates/ollama.crt








4. CA 데이터베이스 갱신
bash
sudo update-ca-certificates
출력 예시:

코드
Updating certificates in /etc/ssl/certs...
1 added, 0 removed; done.
Running hooks in /etc/ca-certificates/update.d...
done.


##################################33333333




